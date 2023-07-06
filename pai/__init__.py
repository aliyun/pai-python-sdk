import sys

if sys.version_info >= (3, 8):
    # noinspection PyCompatibility
    from importlib.metadata import PackageNotFoundError, version
else:
    from importlib_metadata import PackageNotFoundError, version

PACKAGE_NAME = "alipai"

try:
    __version__ = version(PACKAGE_NAME)
except PackageNotFoundError:
    # package is not installed
    __version__ = None
