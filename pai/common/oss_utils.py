from __future__ import absolute_import

from collections import namedtuple
from six.moves.urllib import parse


import six


def is_oss_url(url):
    return bool(url and isinstance(url, six.string_types) and url.startswith("oss://"))


ParsedOssUrl = namedtuple(
    "ParsedOssUrl", field_names=["bucket_name", "object_key", "endpoint", "role_arn"]
)
ParsedDatasetPath = namedtuple(
    "ParsedDatasetPath", field_names=["is_dir", "dir_path", "file_name"]
)


def parse_oss_url(oss_url):
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
