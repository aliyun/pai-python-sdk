import os

import pai
from tests.unit import BaseUnitTestCase


class TestPkgMetadata(BaseUnitTestCase):
    def read_version(self, version_file):
        with open(version_file, "r") as f:
            return f.read().strip()

    def test_version(self):
        version_file = os.path.join(os.path.dirname(pai.__file__), "VERSION")
        file_exists = os.path.exists(version_file)
        self.assertTrue(file_exists)
        self.assertTrue(pai.__version__ is not None)
        self.assertEqual(self.read_version(version_file), pai.__version__)
