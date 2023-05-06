# coding=utf-8
from __future__ import absolute_import, print_function

import os

from pai.common.oss_utils import is_oss_uri
from tests.test_data import SCRIPT_DIR_PATH
from tests.unit import BaseUnitTestCase
from tests.unit.utils import extract_odps_table_info, file_checksum


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

    def test_file_checksum(self):
        checksum = file_checksum(os.path.join(SCRIPT_DIR_PATH, "main.py"))
        self.assertTrue(len(checksum), 32)

    def test_is_oss_url(self):
        cases = [
            {
                "name": "case1",
                "input": None,
                "expected": False,
            },
            {
                "name": "case2",
                "input": "/hello",
                "expected": False,
            },
            {
                "name": "case3",
                "input": "oss://bucket_name/path/to/file",
                "expected": True,
            },
            {
                "name": "case4",
                "input": "file://bucket_name/path/to/file",
                "expected": False,
            },
        ]

        for case in cases:
            result = is_oss_uri(case["input"])
            self.assertEqual(result, case["expected"], "case:%s failed" % case["name"])
