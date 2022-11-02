from __future__ import absolute_import

import hashlib
import os
import random
import re
import string
import tarfile
import tempfile
import time
import uuid
from datetime import datetime

import six
from odps import DataFrame as ODPSDataFrame
from odps.models import Table
from odps.models.partition import Partition

odps_table_re = (
    r"odps://(?P<project>[^/]+)/tables/(?P<table_name>[^/]+)(?P<partition>.*)"
)


PAI_PIPELINE_RUN_ID_PLACEHOLDER = "${pai_system_run_id}"
PAI_PIPELINE_NODE_ID_PLACEHOLDER = "${pai_system_node_id}"


def md5_digest(raw_data):
    return hashlib.md5(raw_data).hexdigest()


def ensure_str(val):
    if isinstance(val, six.string_types):
        return val
    elif isinstance(val, six.integer_types):
        return str(val)
    else:
        raise ValueError("ensure_str: not support type:%s" % type(val))


def ensure_unix_time(t):
    if isinstance(t, datetime):
        return time.mktime(t.timetuple())
    elif isinstance(t, six.integer_types):
        return t
    else:
        raise ValueError(
            "not support format, unable to convert to unix timestamp(%s:%s)"
            % (type(t), t)
        )


def extract_odps_table_info(data):
    if isinstance(data, ODPSDataFrame):
        data = data.data

    if isinstance(data, Table):
        return "%s.%s" % (data.project.name, data.name), None
    elif isinstance(data, Partition):
        return "%s.%s" % (data.table.project.name, data.table.name), data.spec
    elif isinstance(data, six.string_types):
        return _extract_odps_table_info_from_url(data)
    else:
        raise ValueError("Not support ODPSTable input(type:%s)" % type(data))


def _extract_odps_table_info_from_url(resource):
    matches = re.match(odps_table_re, resource)
    if not matches:
        raise ValueError("Not support ODPSTable resource schema.")

    project, table, partition = (
        matches.group("project"),
        matches.group("table_name"),
        matches.group("partition").strip("/"),
    )
    return project, table, partition


def ensure_unicode(t):
    return six.ensure_text(t)


def gen_temp_table(prefix="pai_temp_"):
    return "{prefix}{identifier}".format(
        prefix=prefix,
        identifier=uuid.uuid4().hex,
    )


def gen_run_node_scoped_placeholder(suffix=None):
    if suffix:
        return "{0}_{1}_{2}".format(
            PAI_PIPELINE_NODE_ID_PLACEHOLDER, PAI_PIPELINE_RUN_ID_PLACEHOLDER, suffix
        )
    else:
        return "{0}_{1}".format(
            PAI_PIPELINE_NODE_ID_PLACEHOLDER, PAI_PIPELINE_RUN_ID_PLACEHOLDER
        )


def iter_with_limit(iterator, limit):
    if not isinstance(limit, six.integer_types) or limit <= 0:
        raise ValueError("'limit' should be positive integer")
    idx = 0
    for item in iterator:
        yield item
        idx += 1
        if idx >= limit:
            return


def tar_source_files(source_files, target=None):
    if isinstance(source_files, six.string_types):
        source_files = [source_files]
    if target is None:
        target = tempfile.mktemp()

    with tarfile.open(target, "w:gz") as tar:
        for name in source_files:
            tar.add(name, arcname=os.path.basename(name))
    return target


def tar_file(source_file, target=None):
    source_file = to_abs_path(source_file)
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


def file_checksum(file_name, hash_type="md5"):
    if hash_type.lower() != "md5":
        raise ValueError("not support hash type")

    hash_md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(256 * 1024), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def to_abs_path(path):
    if os.path.isabs(path):
        return path
    else:
        return os.path.abspath(path)


def extract_file_name(file_or_path):
    _, tail = os.path.split(file_or_path)
    return tail.strip()


def makedirs(path_dir, mode=0o777):
    if not os.path.exists(path_dir):
        # argument `exist_ok` not support in Python2
        os.makedirs(path_dir, mode=mode)


def is_iterable(arg):
    try:
        _ = iter(arg)
        return True
    except TypeError:
        return False


def random_str(n):
    """Random string generation with lower case letters and digits.

    Args:
        n: Size of generated random string.

    Returns:
        str: generated random string.

    """
    return "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(n)
    )


def camel_to_snake(name):
    """Convert a name from camel case to snake case."""
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def snake_to_camel(name):
    """Convert a name from snake case to camel case."""
    return "".join([w.title() for w in name.split("_")])


def print_msg(msg: str, *args, **kwargs):
    print(msg.format(*args, **kwargs))
