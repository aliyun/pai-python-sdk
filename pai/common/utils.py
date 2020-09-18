from __future__ import absolute_import

import hashlib
import re
from datetime import datetime

import six
import uuid
from odps import DataFrame as ODPSDataFrame
from odps.models import Table
from odps.models.partition import Partition

odps_table_re = r'odps://(?P<project>[^/]+)/tables/(?P<table_name>[^/]+)(?P<partition>.*)'


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
        return (t - datetime(1970, 1, 1)).total_seconds()
    elif isinstance(t, six.integer_types):
        return t
    else:
        raise ValueError(
            "not support format, unable to convert to unix timestamp(%s:%s)" % (type(t), t))


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

    project, table, partition = matches.group("project"), matches.group(
        "table_name"), matches.group("partition").strip(
        "/")
    return project, table, partition


def ensure_unicode(t):
    return six.ensure_text(t)


def gen_temp_table(prefix="pai_temp_"):
    return '{prefix}{identifier}'.format(
        prefix=prefix,
        identifier=uuid.uuid4().hex,
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
