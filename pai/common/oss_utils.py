from __future__ import absolute_import

import glob
import logging
import os.path
import pathlib
from collections import namedtuple
from typing import Optional

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

ParsedDatasetPath = namedtuple(
    "ParsedDatasetPath", field_names=["is_dir", "dir_path", "file_name"]
)


def parse_oss_url(oss_url: str) -> "ParsedOssUrl":
    """Parse the given OSS schema URL and returns an namedtuple including bucket_name, object_key, endpoint, role_arn.
    Args:
        oss_url: URL in OSS schema ( oss://<bucket.endpoint>/<object_key>?endpoint=<endpoint>&host=<endpoint>&role_arn=<role_arn>)
    Returns:
        ParsedOssUrl: Returns a namedtuple including bucket_name, object_key, endpoint and role_arn.
    """
    parsed_result = parse.urlparse(oss_url)
    if parsed_result.scheme != "oss":
        raise ValueError("require OSS url but given '{}'".format(oss_url))
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
    return ParsedOssUrl(
        bucket_name=bucket_name,
        object_key=object_key,
        endpoint=endpoint,
        role_arn=role_arn,
    )


def compose_oss_url(bucket, path, endpoint=None):
    """Build OSS uri from given bucket, object path, and service endpoint."""
    host = bucket if not endpoint else "{0}.{1}".format(bucket, endpoint)
    path = path.lstrip("/")
    url = "oss://{0}/{1}".format(host, path.lstrip("/"))
    return url


def parse_dataset_path(path):
    """Parse given path, returns a namedtuple.

    Args:
        path: OSS object key or NAS file path.

    Returns:
        namedtuple: An namedtuple including is_dir, dir_path, file_name.
    """
    path = path.strip()
    if path.endswith("/"):
        is_dir, dir_path, file_name = True, os.path.join("/", path), None
    else:
        idx = path.rfind("/")
        if idx < 0:
            is_dir, dir_path, file_name = False, "/", path
        else:
            is_dir, dir_path, file_name = (
                False,
                os.path.join("/", path[: idx + 1]),
                path[idx + 1 :],
            )

    return ParsedDatasetPath(
        is_dir=is_dir,
        dir_path=dir_path,
        file_name=file_name,
    )


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
    parsed = parse_oss_url(url)

    return "oss://{bucket_name}.{endpoint}/{key}".format(
        bucket_name=parsed.bucket_name, endpoint=endpoint, key=parsed.object_key
    )


def tar_and_upload(source_path, destination, oss_bucket):
    pass
