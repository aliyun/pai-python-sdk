import hashlib
from datetime import datetime

import six


def md5_digest(raw_data):
    return hashlib.md5(raw_data).hexdigest()


def run_detail_url(run_id, region_id):
    return "https://pai.data.aliyun.com/console?regionId={region_id}#/task-list/detail/{run_id}".format(
        region_id=region_id, run_id=run_id,
    )


def ensure_str(val):
    if isinstance(val, six.string_types):
        return val
    elif isinstance(val, six.integer_types):
        return str(val)
    else:
        raise ValueError("ensure_str: not support type:%s" % type(val))


def ensure_unix_time(t):
    if isinstance(t, datetime):
        return datetime.fromtimestamp(t)
    elif isinstance(t, (int, long)):
        return t
    else:
        raise ValueError("not support format for unix timestamp:%s", t)
