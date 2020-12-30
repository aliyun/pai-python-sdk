from __future__ import absolute_import
import os

version_file = os.path.join(os.path.dirname(__file__), "VERSION")
if os.path.exists(version_file):
    with open(version_file, "r") as f:
        __version__ = f.read().strip()
else:
    __version__ = None
