# coding=utf-8
from __future__ import absolute_import
from __future__ import print_function

import tarfile
import tempfile
import os
from mock import patch

from pai.common.oss_utils import is_oss_url

from pai.common.utils import (
    extract_odps_table_info,
    tar_source_files,
    file_checksum,
    to_abs_path,
    extract_file_name,
)
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

    def test_to_abs_path(self):
        cwd = os.getcwd()
        cases = [
            {
                "name": "case1",
                "input": "example",
                "expected": os.path.join(cwd, "example"),
            },
            {
                "name": "case2",
                "input": "/home/admin/logs",
                "expected": "/home/admin/logs",
            },
        ]
        for case in cases:
            result = to_abs_path(case["input"])

            self.assertEqual(case["expected"], result, "case:%s failed" % case["name"])

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
            result = is_oss_url(case["input"])
            self.assertEqual(result, case["expected"], "case:%s failed" % case["name"])

    @patch("os.path.sep", "/")
    def test_extract_file_name(self):
        cases = [
            {
                "name": "case1",
                "input": "/home/root/main.py",
                "expected": "main.py",
            },
            {
                "name": "case2",
                "input": "main.py",
                "expected": "main.py",
            },
            {
                "name": "case3",
                "input": "relative/path/to/main.py",
                "expected": "main.py",
            },
            {
                "name": "case4",
                "input": "oss://bucket_name/path_to_file/main.py",
                "expected": "main.py",
            },
        ]

        for case in cases:
            result = extract_file_name(case["input"])
            self.assertEqual(case["expected"], result, "case:%s failed" % case["name"])
