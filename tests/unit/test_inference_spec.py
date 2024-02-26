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

from pai.exception import DuplicatedMountException, MountPathIsOccupiedException
from pai.model import InferenceSpec
from tests.unit import BaseUnitTestCase


class TestInferenceSpec(BaseUnitTestCase):
    def test_inference_spec(self):
        infer_spec = InferenceSpec(
            processor="pmml",
        )
        self.assertEqual(infer_spec.processor, "pmml")
        infer_spec.merge_options(
            {
                "metadata.instance": 2,
                "metadata.rpc.keepalive": 10000,
                "name": "example",
            }
        )
        self.assertEqual(infer_spec.metadata.instance, 2)
        self.assertEqual(infer_spec.metadata.rpc.keepalive, 10000)
        self.assertDictEqual(infer_spec.metadata.rpc, {"keepalive": 10000})
        self.assertEqual(infer_spec.name, "example")
        infer_spec.add_option("metadata.rpc.batching", True)
        self.assertEqual(infer_spec.metadata.rpc.batching, True)

        infer_spec.storage = [
            {
                "mount_path": "/ml/model/",
                "oss": {
                    "endpoint": "oss-cn-beijing-internal.aliyuncs.com",
                    "path": "oss://pai-sdk-example/path/to/model/",
                },
            },
        ]
        infer_spec.mount("oss://pai-sdk-example/path/to/code/", mount_path="/ml/code/")

        self.assertEqual(infer_spec.storage[0].mount_path, "/ml/model/")
        d = infer_spec.to_dict()
        self.assertEqual(
            d,
            {
                "processor": "pmml",
                "metadata": {
                    "instance": 2,
                    "rpc": {
                        "keepalive": 10000,
                        "batching": True,
                    },
                },
                "name": "example",
                "storage": [
                    {
                        "mount_path": "/ml/model/",
                        "oss": {
                            "endpoint": "oss-cn-beijing-internal.aliyuncs.com",
                            "path": "oss://pai-sdk-example/path/to/model/",
                        },
                    },
                    {
                        "mount_path": "/ml/code/",
                        "oss": {
                            "path": "oss://pai-sdk-example/path/to/code/",
                        },
                    },
                ],
            },
        )

        with self.assertRaises(DuplicatedMountException):
            infer_spec.mount(
                "oss://pai-sdk-example/path/to/model/", mount_path="/ml/hello/"
            )

        with self.assertRaises(DuplicatedMountException):
            infer_spec.mount(
                "oss://pai-sdk-example/path/to/model/", mount_path="/ml/world/"
            )

        infer_spec.mount(
            "oss://pai-sdk-example/path/to/abc/edfg", mount_path="/ml/code/"
        )
