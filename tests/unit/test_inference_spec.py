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

        with self.assertRaises(ValueError):
            infer_spec.mount(
                "oss://pai-sdk-example/path/to/model/", mount_path="/ml/model/"
            )

    def test_inference_spec_creating(self):
        infer_spec = InferenceSpec.from_serving_container(
            image_uri="python:3",
            command="python serving.py",
            environment_variables={
                "PYTHONPATH": "1",
                "Foo": "Bar",
            },
            port=8001,
        )

        infer_spec.metadata.rpc.keepalive = 1000
        self.assertEqual(infer_spec.containers[0].image, "python:3")
        self.assertListEqual(
            infer_spec.containers[0].env,
            [
                {
                    "name": "PYTHONPATH",
                    "value": "1",
                },
                {
                    "name": "Foo",
                    "value": "Bar",
                },
            ],
        )
        self.assertDictEqual(
            infer_spec.to_dict(),
            {
                "containers": [
                    {
                        "image": "python:3",
                        "script": "python serving.py",
                        "env": [
                            {
                                "name": "PYTHONPATH",
                                "value": "1",
                            },
                            {
                                "name": "Foo",
                                "value": "Bar",
                            },
                        ],
                        "port": 8001,
                    }
                ],
                "metadata": {
                    "rpc": {
                        "keepalive": 1000,
                    }
                },
            },
        )
