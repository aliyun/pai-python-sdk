#  Copyright 2023 Alibaba, Inc. or its affiliates.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from __future__ import absolute_import

import glob
import os.path
import pathlib
import tarfile
import tempfile
from typing import Optional, Tuple, Union
from urllib.parse import parse_qs, urlparse

import oss2
from alibabacloud_credentials.client import Client as CredentialClient
from alibabacloud_credentials.models import Config as CredentialConfig
from oss2.credentials import Credentials, CredentialsProvider
from tqdm.autonotebook import tqdm

from .logging import get_logger

logger = get_logger(__name__)


class _ProgressCallbackTqdm(tqdm):
    def __call__(self, consumed_bytes, total_bytes):
        self.update(n=consumed_bytes - self.n)


def _upload_with_progress(
    filename,
    object_key,
    oss_bucket: oss2.Bucket,
):
    local_file_size = os.path.getsize(filename)
    with _ProgressCallbackTqdm(
        total=local_file_size,
        unit="B",
        unit_scale=True,
        desc=f"Uploading file: {filename}",
    ) as pbar:
        oss2.resumable_upload(
            bucket=oss_bucket,
            key=object_key,
            filename=filename,
            progress_callback=pbar,
            num_threads=os.cpu_count() * 2,
        )
        # Mark the progress as completed.
        pbar.update(n=pbar.total - pbar.n)


def _download_with_progress(
    filename,
    object_key,
    oss_bucket: oss2.Bucket,
):
    total = oss_bucket.get_object_meta(object_key).content_length
    with _ProgressCallbackTqdm(
        total=total,
        unit="B",
        unit_scale=True,
        desc=f"Downloading file: {filename}",
    ) as pbar:
        oss2.resumable_download(
            bucket=oss_bucket,
            key=object_key,
            filename=filename,
            progress_callback=pbar,
            num_threads=os.cpu_count(),
        )
        # Mark the progress as completed.
        pbar.update(n=pbar.total - pbar.n)


def is_oss_uri(uri: Union[str, bytes]) -> bool:
    """Determines whether the given uri is an OSS uri.

    Args:
        uri (Union[str, bytes]): A string in OSS URI schema:
            oss://<bucket_name>[.endpoint]/<path/to/file>,


    Returns:
        bool: True if the given uri is an OSS uri, else False.

    """
    return bool(uri and isinstance(uri, (str, bytes)) and str(uri).startswith("oss://"))


class OssUriObj(object):
    """A class that represents an OSS URI and provides some convenient methods."""

    def __init__(self, uri: str):
        """Constructor for class OssUriObj.

        Args:
            uri (str): A string in OSS URI schema: oss://<bucket_name>[.endpoint]/<path/to/file>,
                endpoint in uri is optional.
        """
        if not uri.startswith("oss://"):
            raise ValueError(
                "Invalid OSS URI schema, please provide a string starts with 'oss://'"
            )
        bucket_name, object_key, endpoint, role_arn = self.parse(uri)
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.endpoint = endpoint
        self.role_arn = role_arn

    @classmethod
    def from_bucket_key_endpoint(
        cls, bucket_name: str, object_key: str, endpoint: Optional[str] = None
    ) -> "OssUriObj":
        """Initialize an OSSUri object from bucket_name, object_key and endpoint.

        Args:
            bucket_name (str): The name of the OSS bucket.
            object_key (str): OSS object key/path.
            endpoint (str, optional): Endpoint for the OSS bucket.

        Returns:
            OssUriObj: An OssUriObj instance represents the specified OSS object.

        """
        # OSS object key could not contain leading slashes.
        # Document: https://help.aliyun.com/document_detail/273129.html
        if object_key.startswith("/"):
            logger.warning(
                "OSS object key should not contain leading slashes, the leading"
                " slashes will be removed."
            )
            object_key = object_key.lstrip("/")

        if endpoint:
            if endpoint.startswith("http://"):
                endpoint = endpoint.lstrip("http://")
            elif endpoint.startswith("https://"):
                endpoint = endpoint.lstrip("https://")

            uri = f"oss://{bucket_name}.{endpoint}/{object_key}"
        else:
            uri = f"oss://{bucket_name}/{object_key}"
        return OssUriObj(uri=uri)

    @classmethod
    def parse(cls, oss_uri: str) -> Tuple[str, str, str, str]:
        """Parse OSS uri string and returns a tuple of (bucket_name, object_key,
        endpoint, role_arn).

        Args:
            oss_uri (str): A string in OSS Uri schema: oss://{bucket_name}.{endpoint}/{object_key}.

        Returns:
            Tuple: An tuple of [bucket_name, object_key, endpoint, role_arn].

        """
        parsed_result = urlparse(oss_uri)
        if parsed_result.scheme != "oss":
            raise ValueError(
                "require OSS uri('oss://[bucket_name]/[object_key]') but "
                "given '{}'".format(oss_uri)
            )
        object_key = parsed_result.path
        if object_key.startswith("/"):
            object_key = object_key[1:]

        query = parse_qs(parsed_result.query)
        if "." in parsed_result.hostname:
            bucket_name, endpoint = parsed_result.hostname.split(".", 1)
        else:
            bucket_name = parsed_result.hostname
            # try to get OSS endpoint from url query.
            if "endpoint" in query:
                endpoint = query.get("endpoint")[0]
            elif "host" in query:
                endpoint = query.get("host")[0]
            else:
                endpoint = None
        role_arn = query.get("role_arn")[0] if "role_arn" in query else None

        return bucket_name, object_key, endpoint, role_arn

    def get_uri_with_endpoint(self, endpoint: str = None) -> str:
        """Get an OSS uri string contains endpoint.

        Args:
            endpoint (str): Endpoint of the OSS bucket.

        Returns:
            str: An string in OSS uri schema contains endpoint.

        """
        if not endpoint and not self.endpoint:
            raise ValueError("Unknown endpoint for the OSS bucket.")

        return "oss://{bucket_name}.{endpoint}/{object_key}".format(
            bucket_name=self.bucket_name,
            endpoint=endpoint or self.endpoint,
            object_key=self.object_key,
        )

    def get_dir_uri(self):
        """Returns directory in OSS uri string format of the original object."""
        _, dirname, _ = self.parse_object_key()
        dir_uri = f"oss://{self.bucket_name}{dirname}"
        return dir_uri

    @property
    def uri(self) -> str:
        """Returns OSS uri in string format."""
        return "oss://{bucket_name}/{object_key}".format(
            bucket_name=self.bucket_name,
            object_key=self.object_key,
        )

    def parse_object_key(self) -> Tuple[bool, str, str]:
        """Parse the OSS URI object key, returns a tuple of (is_dir, dir_path, file_name).

        Returns:
            namedtuple: An tuple of is_dir, dir_path, file_name.
        """
        object_key = self.object_key.strip()
        if object_key.endswith("/"):
            is_dir, dir_path, file_name = True, os.path.join("/", object_key), None
        else:
            idx = object_key.rfind("/")
            if idx < 0:
                is_dir, dir_path, file_name = False, "/", object_key
            else:
                is_dir, dir_path, file_name = (
                    False,
                    os.path.join("/", object_key[: idx + 1]),
                    object_key[idx + 1 :],
                )
        return is_dir, dir_path, file_name


def _tar_file(source_file, target=None):
    source_file = (
        source_file if os.path.isabs(source_file) else os.path.abspath(source_file)
    )
    if not os.path.exists(source_file):
        raise ValueError("source file not exists: %s", source_file)
    if os.path.isdir(source_file):
        arcname = ""
    else:
        arcname = os.path.basename(source_file)

    if not target:
        target = tempfile.mktemp()
    with tarfile.open(target, "w:gz") as tar:
        tar.add(name=source_file, arcname=arcname)
    return target


def _get_bucket_and_path(
    bucket: Optional[oss2.Bucket],
    oss_path: Union[str, OssUriObj],
) -> Tuple[oss2.Bucket, str]:
    from pai.session import get_default_session

    sess = get_default_session()
    if isinstance(oss_path, OssUriObj) or is_oss_uri(oss_path):
        # If the parameter oss_path is an OssUriObj object, we need to use the
        # corresponding bucket that OssUriObj instance belongs to for
        # uploading/downloading the data.
        if is_oss_uri(oss_path):
            oss_path = OssUriObj(oss_path)

        if sess.oss_bucket.bucket_name == oss_path.bucket_name:
            bucket = sess.oss_bucket
        else:
            bucket = sess.get_oss_bucket(
                oss_path.bucket_name, endpoint=oss_path.endpoint
            )
        oss_path = oss_path.object_key
    elif not bucket:
        bucket = sess.oss_bucket
    return bucket, oss_path


def upload(
    source_path: str,
    oss_path: Union[str, OssUriObj],
    bucket: Optional[oss2.Bucket] = None,
    is_tar: Optional[bool] = False,
) -> str:
    """Upload local source file/directory to OSS.

    Examples::

        # compress and upload local directory `./src/` to OSS
        >>> upload(source_path="./src/", oss_path="path/to/file",
        ... bucket=session.oss_bucket, is_tar=True)


    Args:
        source_path (str): Source file local path which needs to be uploaded, can be
            a single file or a directory.
        oss_path (Union[str, OssUriObj]): Destination OSS path.
        bucket (oss2.Bucket): OSS bucket used to store the upload data. If it is not
            provided, OSS bucket of the default session will be used.
        is_tar (bool): Whether to compress the file before uploading (default: False).

    Returns:
        str: A string in OSS URI format. If the source_path is directory, return the
            OSS URI representing the directory for uploaded data, else then
            returns the OSS URI points to the uploaded file.
    """

    bucket, oss_path = _get_bucket_and_path(bucket, oss_path)

    source_path_obj = pathlib.Path(source_path)
    if not source_path_obj.exists():
        raise RuntimeError("Source path is not exist: {}".format(source_path))

    if is_tar:
        # compress the local data and upload the compressed source data.
        with tempfile.TemporaryDirectory() as dir_name:
            temp_tar_path = _tar_file(
                source_path, os.path.join(dir_name, "source.tar.gz")
            )
            dest_path = (
                os.path.join(oss_path, os.path.basename(temp_tar_path))
                if oss_path.endswith("/")
                else oss_path
            )
            _upload_with_progress(
                filename=temp_tar_path, object_key=dest_path, oss_bucket=bucket
            )
            return "oss://{}/{}".format(bucket.bucket_name, dest_path)
    elif not source_path_obj.is_dir():
        # if source path is a file, just invoke bucket.put_object.

        # if the oss_path is endswith slash, the file will be uploaded to
        # "{oss_path}{filename}", else the file will be uploaded to "{oss_path}".
        dest_path = (
            os.path.join(oss_path, os.path.basename(source_path))
            if oss_path.endswith("/")
            else oss_path
        )
        _upload_with_progress(
            filename=source_path, object_key=dest_path, oss_bucket=bucket
        )
        return "oss://{}/{}".format(bucket.bucket_name, dest_path)
    else:
        # if the source path is a directory, upload all the file under the directory.
        source_files = glob.glob(
            pathname=str(source_path_obj / "**"),
            recursive=True,
        )
        if not oss_path.endswith("/"):
            oss_path += "/"

        files = [f for f in source_files if not os.path.isdir(f)]
        for file_path in files:
            file_path_obj = pathlib.Path(file_path)
            file_relative_path = file_path_obj.relative_to(source_path_obj).as_posix()
            object_key = oss_path + file_relative_path
            _upload_with_progress(
                filename=file_path, object_key=object_key, oss_bucket=bucket
            )
        return "oss://{}/{}".format(bucket.bucket_name, oss_path)


def download(
    oss_path: Union[str, OssUriObj],
    local_path: str,
    bucket: Optional[oss2.Bucket] = None,
    un_tar=False,
):
    """Download OSS objects to local path.

    Args:
        oss_path (str): Source OSS path, could be a single OSS object or a OSS
            directory.
        local_path (str): Local path used to store the data from OSS.
        bucket (oss2.Bucket, optional): OSS bucket used to store the upload data. If it
            is not provided, OSS bucket of the default session will be used.
        un_tar (bool, optional): Whether to decompress the downloaded data. It is only
            work for `oss_path` point to a single file that has a suffix "tar.gz".

    Returns:
        str: A local file path for the downloaded data.

    """

    bucket, oss_path = _get_bucket_and_path(bucket, oss_path)

    if not bucket.object_exists(oss_path) or oss_path.endswith("/"):
        # The `oss_path` represents a "directory" in the OSS bucket, download the
        # objects which object key is prefixed with `oss_path`.
        # Note: `un_tar` is not work while `oss_path` is a directory.

        oss_path += "/" if not oss_path.endswith("/") else ""
        iterator = oss2.ObjectIteratorV2(
            bucket=bucket,
            prefix=oss_path,
        )
        keys = [obj.key for obj in iterator if not obj.key.endswith("/")]
        for key in tqdm(keys, desc=f"Downloading: {oss_path}"):
            rel_path = os.path.relpath(key, oss_path)
            dest = os.path.join(local_path, rel_path)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            _download_with_progress(
                dest,
                object_key=key,
                oss_bucket=bucket,
            )
        return local_path
    else:
        # The `oss_path` represents a single file in OSS bucket.
        if oss_path.endswith(".tar.gz") and un_tar:
            # currently, only tar.gz format is supported for un_tar after downloading.
            with tempfile.TemporaryDirectory() as temp_dir:
                target_path = os.path.join(temp_dir, os.path.basename(oss_path))
                _download_with_progress(
                    target_path,
                    object_key=oss_path,
                    oss_bucket=bucket,
                )
                with tarfile.open(name=target_path, mode="r") as t:
                    t.extractall(path=local_path)

            return local_path
        else:
            os.makedirs(local_path, exist_ok=True)
            dest = os.path.join(local_path, os.path.basename(oss_path))
            _download_with_progress(
                dest,
                object_key=oss_path,
                oss_bucket=bucket,
            )

            return dest


class CredentialProviderWrapper(CredentialsProvider):
    """A wrapper class for the credential provider of OSS."""

    def __init__(self, config: Union[CredentialConfig] = None):
        self.client = CredentialClient(config)

    def get_credentials(self) -> Credentials:
        return Credentials(
            access_key_id=self.client.get_access_key_id(),
            access_key_secret=self.client.get_access_key_secret(),
            security_token=self.client.get_security_token(),
        )
