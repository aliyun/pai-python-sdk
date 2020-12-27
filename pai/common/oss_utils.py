from __future__ import absolute_import

import six
from oss2.exceptions import NotFound as OssNotFoundException


def is_oss_url(url):
    return bool(url and isinstance(url, six.string_types) and url.startswith("oss://"))
