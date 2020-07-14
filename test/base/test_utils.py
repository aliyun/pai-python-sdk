# coding=utf-8
from __future__ import absolute_import, unicode_literals

from __future__ import print_function
from pai import ProviderAlibabaPAI
from test import BaseTestCase
from pai.pipeline import Pipeline
from pai.utils import extract_odps_table_info, ensure_unicode


class TestUtils(BaseTestCase):

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


    def test_ensure_unicode(self):
        i1 = "Hello中国"
        i2 = "Hell World"
        print((ensure_unicode(i1), type(ensure_unicode(i1))))
        print((ensure_unicode(i2), type(ensure_unicode(i2))))


