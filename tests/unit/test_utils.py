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
from pai.common.utils import generate_repr, is_filesystem_uri, is_odps_table_uri, parse_region_id_from_endpoint, \
    parse_oss_uri, parse_nas_uri, parse_cpfs_uri, parse_local_file_uri, parse_pai_dataset_uri, parse_odps_uri, \
    parse_bmcpfs_uri
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

    def test_parse_region_id_from_valid_endpoint(self):
        self.assertEqual(parse_region_id_from_endpoint("cn-shanghai"), 'cn-shanghai')
        self.assertEqual(parse_region_id_from_endpoint("cn-shanghai-internal"), 'cn-shanghai')
        self.assertEqual(parse_region_id_from_endpoint("cn-shanghai-internal.aliyuncs.com"), 'cn-shanghai')

    def test_parse_region_id_from_invalid_endpoint(self):
        self.assertIsNone(parse_region_id_from_endpoint("http://someotherendpoint.com"))
        self.assertIsNone(parse_region_id_from_endpoint(""))
        self.assertIsNone(parse_region_id_from_endpoint(None))

    def test_parse_valid_oss_uri(self):
        self.assertEqual(parse_oss_uri('oss://test-bucket.oss-cn-hangzhou.aliyuncs.com/models/ALBERTv2-Chinese'
                                       '-NewsBase.pth'),
                         ('test-bucket', 'cn-hangzhou', 'models/ALBERTv2-Chinese-NewsBase.pth'))
        self.assertEqual(
            parse_oss_uri(
                'oss://test-bucket.oss-cn-hangzhou-internal.aliyuncs.com/models/ALBERTv2-Chinese-NewsBase.pth'),
            ('test-bucket', 'cn-hangzhou', 'models/ALBERTv2-Chinese-NewsBase.pth'))
        self.assertEqual(parse_oss_uri('oss://test-bucket.oss-cn-hangzhou.aliyuncs.com/'),
                         ('test-bucket', 'cn-hangzhou', '/'))
        self.assertEqual(parse_oss_uri('oss://test-bucket.oss-cn-hangzhou.aliyuncs.com'),
                         ('test-bucket', 'cn-hangzhou', '/'))

    def test_parse_invalid_oss_uri(self):
        self.assertIsNone(parse_oss_uri('oss://test-bucket/models/ALBERTv2-Chinese'
                                        '-NewsBase.pth'))
        self.assertIsNone(parse_oss_uri('oss://'))
        self.assertIsNone(parse_oss_uri(''))

    def test_parse_valid_nas_uri(self):
        self.assertEqual(parse_nas_uri('nas://007636fd-gfyy.cn-hangzhou.extreme.nas.aliyuncs.com/mnt/foo/'),
                         ('nas://007636fd-gfyy.cn-hangzhou.extreme.nas.aliyuncs.com/mnt/foo/', 'cn-hangzhou'))
        self.assertEqual(parse_nas_uri('nas://007636fd-gfyy.cn-hangzhou.extreme.nas.aliyuncs.com/'),
                         ('nas://007636fd-gfyy.cn-hangzhou.extreme.nas.aliyuncs.com/', 'cn-hangzhou'))
        self.assertEqual(parse_nas_uri('nas://007636fd-gfyy.cn-hangzhou.extreme.nas.aliyuncs.com'),
                         ('nas://007636fd-gfyy.cn-hangzhou.extreme.nas.aliyuncs.com', 'cn-hangzhou'))
        self.assertEqual(parse_nas_uri('nas://066e54a580.cn-hangzhou/'),
                         ('nas://066e54a580.cn-hangzhou/', 'cn-hangzhou'))

    def test_parse_invalid_nas_uri(self):
        self.assertIsNone(parse_nas_uri('nas://007636fd-gfyy.extreme.nas.aliyuncs.com/mnt/foo/'))
        self.assertIsNone(parse_nas_uri('nas://'))
        self.assertIsNone(parse_nas_uri(''))

    def test_parse_valid_cpfs_uri(self):
        self.assertEqual(
            parse_cpfs_uri('cpfs://cpfs-00f4b992044a71be.cn-hangzhou/ptc-008727a69e07d3cf/exp-00d695a1b9f6c926/'),
            ('cpfs://cpfs-00f4b992044a71be.cn-hangzhou/ptc-008727a69e07d3cf/exp-00d695a1b9f6c926/', 'cn-hangzhou'))
        self.assertEqual(parse_cpfs_uri('cpfs://cpfs-00f4b992044a71be.cn-hangzhou/'),
                         ('cpfs://cpfs-00f4b992044a71be.cn-hangzhou/', 'cn-hangzhou'))
        self.assertEqual(parse_cpfs_uri('cpfs://cpfs-00f4b992044a71be.cn-hangzhou'),
                         ('cpfs://cpfs-00f4b992044a71be.cn-hangzhou', 'cn-hangzhou'))

    def test_parse_invalid_cpfs_uri(self):
        self.assertIsNone(parse_cpfs_uri('cpfs://cpfs-00f4b992044a71be/mnt/foo/'))
        self.assertIsNone(parse_cpfs_uri('cpfs://'))
        self.assertIsNone(parse_cpfs_uri(''))

    def test_parse_valid_bmcpfs_uri(self):
        self.assertEqual(
            parse_bmcpfs_uri('bmcpfs://cpfs-291070fd9529c747-000001.cn-wulanchabu.cpfs.aliyuncs.com/sub/dir'),
            ('bmcpfs://cpfs-291070fd9529c747-000001.cn-wulanchabu.cpfs.aliyuncs.com/sub/dir', 'cn-wulanchabu'))
        self.assertEqual(parse_bmcpfs_uri('bmcpfs://cpfs-291070fd9529c747-000001.cn-wulanchabu.cpfs.aliyuncs.com/'),
                         ('bmcpfs://cpfs-291070fd9529c747-000001.cn-wulanchabu.cpfs.aliyuncs.com/', 'cn-wulanchabu'))
        self.assertEqual(parse_bmcpfs_uri('bmcpfs://cpfs-291070fd9529c747-000001.cn-wulanchabu.cpfs.aliyuncs.com'),
                         ('bmcpfs://cpfs-291070fd9529c747-000001.cn-wulanchabu.cpfs.aliyuncs.com', 'cn-wulanchabu'))

    def test_parse_invalid_bmcpfs_uri(self):
        self.assertIsNone(parse_bmcpfs_uri('bmcpfs://cpfs-291070fd9529c747-000001.cpfs.aliyuncs.com/'))
        self.assertIsNone(parse_bmcpfs_uri('bmcpfs://'))
        self.assertIsNone(parse_bmcpfs_uri(''))

    def test_parse_valid_local_file_uri(self):
        self.assertEqual(parse_local_file_uri('file:///mnt/dataset_123-456+789'),
                         '/mnt/dataset_123-456+789')
        self.assertEqual(parse_local_file_uri('file:///mnt/dataset 123'),
                         '/mnt/dataset 123')
        self.assertEqual(parse_local_file_uri('file:///'),
                         '/')

    def test_parse_invalid_local_file_uri(self):
        self.assertIsNone(parse_local_file_uri('file://mnt/dataset'))
        self.assertIsNone(parse_local_file_uri('file://'))
        self.assertIsNone(parse_local_file_uri(''))

    def test_parse_valid_pai_dataset_uri(self):
        self.assertEqual(parse_pai_dataset_uri('pai://datasets/d-123456'),
                         ('d-123456', '1'))
        self.assertEqual(parse_pai_dataset_uri('pai://datasets/d-123456/2'),
                         ('d-123456', '2'))
        self.assertEqual(parse_pai_dataset_uri('pai://datasets/d-123456/2/3'),
                         ('d-123456', '2'))

    def test_parse_invalid_pai_dataset_uri(self):
        self.assertIsNone(parse_pai_dataset_uri('pai://datasets/'))
        self.assertIsNone(parse_pai_dataset_uri('pai://'))
        self.assertIsNone(parse_pai_dataset_uri(''))

    def test_parse_valid_odps_uri(self):
        self.assertEqual(parse_odps_uri('odps://project_mc/schema1/tables/flow_model_label_table_v1'),
                         ('project_mc', 'schema1', 'flow_model_label_table_v1'))
        self.assertEqual(parse_odps_uri('odps://project_mc/tables/flow_model_label_table_v1'),
                         ('project_mc', None, 'flow_model_label_table_v1'))

    def test_parse_invalid_odps_uri(self):
        self.assertIsNone(parse_odps_uri('odps://project_mc/tables/'))
        self.assertIsNone(parse_odps_uri('odps://project_mc/'))
        self.assertIsNone(parse_odps_uri('odps://'))
        self.assertIsNone(parse_odps_uri(''))
