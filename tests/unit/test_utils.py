# coding=utf-8
from __future__ import absolute_import
from __future__ import print_function

import tarfile
import tempfile
import os

from pai.common.utils import extract_odps_table_info, tar_source_files, file_checksum
from tests.unit import BaseUnitTestCase
from tests.test_data import SCRIPT_DIR_PATH


class TestUtils(BaseUnitTestCase):
    def test_extract_odps_table_from_url(self):
        cases = [
            {
                "name": "case_table",
                "input": "odps://test_project/tables/test_table",
                "expected": ["test_project", "test_table", ""],
            },
            {
                "name": "case_table_with_slash",
                "input": "odps://test_project/tables/test_table/",
                "expected": ["test_project", "test_table", ""],
            },
            {
                "name": "case_partition",
                "input": "odps://test_project/tables/test_table/p1=hello",
                "expected": ["test_project", "test_table", "p1=hello"],
            },
            {
                "name": "case_multi_key_partition",
                "input": "odps://test_project/tables/test_table/p1=Hello/p2=World/",
                "expected": ["test_project", "test_table", "p1=Hello/p2=World"],
            },
        ]

        for case in cases:
            result = extract_odps_table_info(case["input"])
            self.assertListEqual(list(result), case["expected"])

    def test_tar_source_files(self):
        source_files = [
            os.path.join(SCRIPT_DIR_PATH, f) for f in os.listdir(SCRIPT_DIR_PATH)
        ]

        temp = tempfile.mktemp()

        try:
            tar_result = tar_source_files(source_files, temp)
            self.assertTrue(tarfile.is_tarfile(tar_result))

            expected = ["main.py", "utils.py", "requirements.txt"]

            with tarfile.open(tar_result, "r") as result:
                self.assertEqual(sorted(result.getnames()), sorted(expected))
        finally:
            os.remove(temp)

    def test_file_checksum(self):
        checksum = file_checksum(os.path.join(SCRIPT_DIR_PATH, "main.py"))
        self.assertTrue(len(checksum), 32)
