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

from pai.exception import DuplicatedMountException
from pai.model import (
    InferenceSpec,
    NfsStorageConfig,
    NodeStorageConfig,
    OssStorageConfig,
    RawStorageConfig,
    SharedMemoryConfig,
    container_serving_spec,
)
from tests.unit import BaseUnitTestCase


class TestInferenceSpec(BaseUnitTestCase):
    def test_add_options(self):
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

    def test_mount_storage(self):
        infer_spec = InferenceSpec(
            processor="pmml",
        )
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

    def test_set_model(self):
        infer_spec = container_serving_spec(
            command="python3 /ml/code/model.py",
            image_uri="python:3",
        )
        infer_spec.storage = [
            {
                "mount_path": "/ml/code/",
                "oss": {
                    "path": "oss://pai-sdk-example/path/to/code/",
                },
            },
        ]
        model_path_v1 = "oss://pai-sdk-example/path/to/model/v1/"
        infer_spec.set_model_data(model_path_v1)
        self.assertEqual(model_path_v1, infer_spec.storage[1].oss.path)

        model_path_v2 = "oss://pai-sdk-example/path/to/model/v2/"
        infer_spec.set_model_data(model_path_v2)
        self.assertEqual(model_path_v2, infer_spec.storage[1].oss.path)

    def test_storage(self):
        infer_spec = container_serving_spec(
            command="python3 /ml/code/model.py",
            image_uri="python:3",
            storage_configs=[
                OssStorageConfig(
                    mount_path="/ml/model/",
                    oss_path="oss://pai-sdk-example/path/to/model/",
                ),
                NfsStorageConfig(
                    mount_path="/ml/shared/",
                    nfs_server="nfs://abc",
                    nfs_path="/path/to/shared/",
                ),
                SharedMemoryConfig(size_limit=64),
                NodeStorageConfig(mount_path="/ml/disk/"),
                RawStorageConfig(
                    config={
                        "image": {
                            "image": "MyImageUri",
                            "path": "/path/to/mount/",
                        },
                        "mount_path": "/data_image",
                    }
                ),
            ],
        )

        truth = [
            {
                "mount_path": "/ml/model/",
                "oss": {"path": "oss://pai-sdk-example/path/to/model/"},
            },
            {
                "mount_path": "/ml/shared/",
                "nfs": {
                    "path": "/path/to/shared/",
                    "readOnly": False,
                    "server": "nfs://abc",
                },
            },
            {
                "empty_dir": {"medium": "memory", "size_limit": 64},
                "mount_path": "/dev/shm",
            },
            {"empty_dir": {}, "mount_path": "/ml/disk/"},
            {
                "image": {
                    "image": "MyImageUri",
                    "path": "/path/to/mount/",
                },
                "mount_path": "/data_image",
            },
        ]
        self.assertListEqual(truth, infer_spec.storage)
