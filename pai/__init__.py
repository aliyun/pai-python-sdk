from __future__ import absolute_import

# noinspection PyCompatibility
from importlib.metadata import PackageNotFoundError, version

PACKAGE_NAME = "alipai"

try:
    __version__ = version(PACKAGE_NAME)
except PackageNotFoundError:
    # package is not installed
    __version__ = None
