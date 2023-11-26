# coding=utf-8

#  Copyright 2023 Alibaba, Inc. or its affiliates.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from __future__ import absolute_import, print_function

import os

from pai.common.oss_utils import is_oss_uri
from pai.common.utils import generate_repr, is_filesystem_uri, is_odps_table_uri
from tests.test_data import SCRIPT_DIR_PATH
from tests.unit import BaseUnitTestCase
from tests.unit.utils import extract_odps_table_info, file_checksum


class DummyClass(object):
    def __init__(self, foo: str, bar: str):
        self.foo = foo
        self.bar = bar


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
            with self.subTest(case=case):
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
            with self.subTest(case=case):
                result = is_oss_uri(case["input"])
                self.assertEqual(
                    result, case["expected"], "case:%s failed" % case["name"]
                )

    def test_generate_repr(self):
        test_cases = [
            {
                "arguments": {
                    "repr_obj": DummyClass("hello", "world"),
                    "attrs": ["foo"],
                    "extra": {},
                },
                "expected": "DummyClass(foo=hello)",
            },
            {
                "arguments": {
                    "repr_obj": DummyClass("hello", "world"),
                    "attrs": ["foo", "bar"],
                    "extra": {},
                },
                "expected": "DummyClass(foo=hello, bar=world)",
            },
            {
                "arguments": {
                    "repr_obj": DummyClass("hello", "world"),
                    "attrs": ["foo", "bar"],
                    "extra": {"alice": "bob"},
                },
                "expected": "DummyClass(foo=hello, bar=world, alice=bob)",
            },
        ]
        for tc in test_cases:
            with self.subTest(tc=tc):
                result = generate_repr(
                    tc["arguments"]["repr_obj"],
                    *tc["arguments"]["attrs"],
                    **tc["arguments"]["extra"],
                )
                self.assertEqual(result, tc["expected"])

    def test_is_odps_table(self):
        test_cases = [
            {
                "arguments": {
                    "uri": "odps://test_project/tables/test_table",
                },
                "expected": True,
            },
            {
                "arguments": {
                    "uri": "odps://test_project/table/test_table",
                },
                "expected": False,
            },
            {
                "arguments": {
                    "uri": "odps://test_project/table",
                },
                "expected": False,
            },
            {
                "arguments": {
                    "uri": "oss://tables/test_table",
                },
                "expected": False,
            },
        ]

        for tc in test_cases:
            with self.subTest(tc=tc):
                result = is_odps_table_uri(tc["arguments"]["uri"])
                self.assertEqual(result, tc["expected"])

    def test_is_filesystem_uri(self):
        test_cases = [
            {
                "arguments": {
                    "uri": "nas://dummy_file_system_id.cn-hangzhou/path/to/dir",
                },
                "expected": True,
            },
            {
                "arguments": {
                    "uri": "cpfs://dummy_file_system_id/path/to/dir",
                },
                "expected": True,
            },
            {
                "arguments": {
                    "uri": "odps://test_project/table/test_table",
                },
                "expected": False,
            },
            {
                "arguments": {
                    "uri": "oss://test_project/table",
                },
                "expected": False,
            },
        ]

        for tc in test_cases:
            with self.subTest(tc=tc):
                result = is_filesystem_uri(tc["arguments"]["uri"])
                self.assertEqual(result, tc["expected"])
