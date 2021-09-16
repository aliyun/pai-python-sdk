from __future__ import absolute_import

import six


def is_oss_url(url):
    return bool(url and isinstance(url, six.string_types) and url.startswith("oss://"))
