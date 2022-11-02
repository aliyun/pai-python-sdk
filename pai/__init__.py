from __future__ import absolute_import

import os


def read_version():
    version_file = os.path.join(os.path.dirname(__file__), "VERSION")

    if os.path.exists(version_file):
        with open(version_file, "r") as f:
            return f.read().strip()


__version__ = read_version()
