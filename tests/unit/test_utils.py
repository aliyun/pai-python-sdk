# coding=utf-8
from __future__ import absolute_import
from __future__ import print_function

from pai.common.utils import extract_odps_table_info
from tests.unit import BaseUnitTestCase


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
