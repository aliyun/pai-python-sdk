from pai.estimator import CpfsFileSystemInput, FileSystemInput
from tests.unit import BaseUnitTestCase


class TestFileSystemInput(BaseUnitTestCase):
    def test_to_input_uri(self):
        cases = [
            {
                "name": "normal",
                "arguments": {
                    "file_system_id": "dummy_file_system_id",
                    "directory_path": "path/to/data",
                },
                "expected": "nas://dummy_file_system_id.cn-hangzhou/path/to/data",
            },
            {
                "name": "without_directory_path",
                "arguments": {
                    "file_system_id": "dummy_file_system_id",
                },
                "expected": "nas://dummy_file_system_id.cn-hangzhou/",
            },
            {
                "name": "with_prefix_slash",
                "arguments": {
                    "file_system_id": "dummy_file_system_id",
                    "directory_path": "/path/to/data",
                },
                "expected": "nas://dummy_file_system_id.cn-hangzhou/path/to/data",
            },
        ]

        for case in cases:
            with self.subTest(case=case):
                input = FileSystemInput(**case["arguments"])

                self.assertEqual(input.to_input_uri(), case["expected"])


class TestCpfsFileSystemInput(BaseUnitTestCase):
    def test_to_input_uri(self):
        cases = [
            {
                "name": "normal",
                "arguments": {
                    "file_system_id": "dummy_file_system_id",
                    "protocol_service_id": "dummy_protocol_service_id",
                    "export_id": "dummy_export_id",
                },
                "expected": "cpfs://dummy_file_system_id.cn-hangzhou/"
                "dummy_protocol_service_id/dummy_export_id/",
            },
        ]

        for case in cases:
            with self.subTest(case=case):
                input = CpfsFileSystemInput(**case["arguments"])

                self.assertEqual(input.to_input_uri(), case["expected"])
