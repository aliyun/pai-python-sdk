from __future__ import absolute_import

import glob
import logging
import os.path
import pathlib
from collections import namedtuple
from typing import Optional, Tuple

import six
from oss2.api import Bucket
from six.moves.urllib import parse

_logger = logging.getLogger(__name__)


def is_oss_url(url: Optional[str]) -> bool:
    """Return if url is in OSS URL schema."""
    return bool(url and isinstance(url, six.string_types) and url.startswith("oss://"))


ParsedOssUrl = namedtuple(
    "ParsedOssUrl", field_names=["bucket_name", "object_key", "endpoint", "role_arn"]
)


def parse_oss_url(oss_url: str) -> "ParsedOssUrl":
    """Parse the given OSS schema URL and returns an namedtuple including bucket_name, object_key, endpoint, role_arn.
    Args:
        oss_url: URL in OSS schema ( oss://<bucket.endpoint>/<object_key>?endpoint=<endpoint>&host=<endpoint>&role_arn=<role_arn>)
    Returns:
        ParsedOssUrl: Returns a namedtuple including bucket_name, object_key, endpoint and role_arn.
    """

    uri = OssUri(oss_url)
    return ParsedOssUrl(
        bucket_name=uri.bucket_name,
        object_key=uri.object_key,
        endpoint=uri.endpoint,
        role_arn=uri.role_arn,
    )


def compose_oss_url(bucket, path, endpoint=None):
    """Build OSS uri from given bucket, object path, and service endpoint."""
    return OssUri.from_bucket_key_endpoint(
        bucket_name=bucket, object_key=path, endpoint=endpoint
    ).uri


def upload_to_oss(source_path: str, oss_path: str, oss_bucket: Bucket) -> str:
    """Upload local source file/directory to OSS.

    Args:
        source_path (str): Source path which needs to be uploaded.
        oss_path (str): Destination OSS path.
        oss_bucket (oss2.Bucket): OSS bucket used for upload.
    """
    source_path_obj = pathlib.Path(source_path)

    if not source_path_obj.exists():
        raise RuntimeError("Source path not exist: {}".format(source_path))
    if source_path_obj.is_dir():
        source_files = glob.glob(
            pathname=str(source_path_obj / "**"),
            recursive=True,
        )
        is_empty_dir = True

        if not oss_path.endswith("/"):
            oss_path += "/"
        for file_path in source_files:
            file_path_obj = pathlib.Path(file_path)
            if file_path_obj.is_dir():
                continue
            is_empty_dir = False
            file_relative_path = file_path_obj.relative_to(source_path_obj).as_posix()
            object_key = oss_path + file_relative_path
            oss_bucket.put_object_from_file(key=object_key, filename=file_path)
        if is_empty_dir:
            raise RuntimeError("Source path is empty dir: {}".format(source_path))
    else:
        oss_bucket.put_object_from_file(key=oss_path, filename=source_path)
    return "oss://{}/{}".format(oss_bucket.bucket_name, oss_path)


def truncate_endpoint(url):
    """Remove endpoint if it is present as host in OSS URL.

    Args:
        url (str): OSS URL.

    Returns:
        str: Endpoint removed OSS URL.
    """

    parsed = parse_oss_url(url)

    return "oss://{bucket_name}/{key}".format(
        bucket_name=parsed.bucket_name, key=parsed.object_key
    )


def join_endpoint(url, endpoint):
    oss_uri = OssUri(url)
    if endpoint:
        if endpoint.startswith("http://"):
            endpoint = endpoint.lstrip("http://")
        elif endpoint.startswith("https://"):
            endpoint = endpoint.lstrip("https://")

    return "oss://{bucket_name}.{endpoint}/{key}".format(
        bucket_name=oss_uri.bucket_name, endpoint=endpoint, key=oss_uri.object_key
    )


class OssUri(object):
    """A class that represent an OSS URI and provide some convenient method."""

    def __init__(self, uri):
        """Constructor for class OssUri.

        Args:
            uri (str): A string in OSS schema: oss://{bucket_name}.{endpoint}/{object_key}, endpoint in url is optional.
        """
        if not uri.startswith("oss://"):
            raise ValueError(
                "Invalid OSS uri schema, please provide a string starts with 'oss://'"
            )
        bucket_name, object_key, endpoint, role_arn = self.parse(uri)
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.endpoint = endpoint
        self.role_arn = role_arn

    @classmethod
    def from_bucket_key_endpoint(
        cls, bucket_name: str, object_key: str, endpoint: Optional[str] = None
    ) -> "OssUri":
        """Initialize an OSSUri object from bucket_name, object_key and endpoint.

        Args:
            bucket_name (str): The name of the OSS bucket.
            object_key (str): OSS object key/path.
            endpoint (str): Endpoint for the OSS bucket.

        Returns:
            OssUri:

        """

        # OSS object key could not contain leading slashes.
        # Document: https://help.aliyun.com/document_detail/273129.html
        object_key = object_key.lstrip("/")
        if endpoint:
            if endpoint.startswith("http://"):
                endpoint = endpoint.lstrip("http://")
            elif endpoint.startswith("https://"):
                endpoint = endpoint.lstrip("https://")

            uri = f"oss://{bucket_name}.{endpoint}/{object_key}"
        else:
            uri = f"oss://{bucket_name}/{object_key}"
        return OssUri(uri=uri)

    @classmethod
    def parse(cls, oss_uri: str) -> Tuple[str, str, str, str]:
        """Parse OSS uri string and returns a tuple of [bucket_name, object_key, endpoint, role_arn].

        Args:
            oss_uri (str): A string in OSS Uri schema: oss://{bucket_name}.{endpoint}/{object_key}.

        Returns:
            Tuple: An tuple of [bucket_name, object_key, endpoint, role_arn].

        """
        parsed_result = parse.urlparse(oss_uri)
        if parsed_result.scheme != "oss":
            raise ValueError(
                "require OSS url('oss://[bucket_name]/[object_key]') but given '{}'".format(
                    oss_uri
                )
            )
        object_key = parsed_result.path
        if object_key.startswith("/"):
            object_key = object_key[1:]

        query = parse.parse_qs(parsed_result.query)
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
