from pai.predictor.service import (
    BuildInProcessor,
    ComputeConfig,
    ContainerProcessor,
    CustomProcessor,
    ServiceConfig,
    ServiceRpcConfig,
)
from tests.unit import BaseUnitTestCase


class TestServiceConfig(BaseUnitTestCase):
    def test_config(self):
        data = {
            "cloud": {
                "computing": {"instance_type": "ecs.c6.large"},
            },
            "metadata": {
                "cpu": 2,
                "instance": 1,
                "memory": 4000,
                "name": "lq_test_ecs_spec",
                "resource": "example_resource",
            },
            "model_path": "oss://test-sdk/test-model-deploy/model_flow_vhndmr3oa1x4kvvs9w_node_ksqe5z1g3je376zt2m_model.xml",
            "oss_endpoint": "oss-cn-shanghai.aliyuncs.com",
            "processor": "pmml",
            "source": "region=cn-shanghai,worksapceId=264097,kind=Model,id=model-xqb38zx588izhqa1kt/1.0.0",
        }

        config = ServiceConfig.from_api_object(data)
        self.assertIsInstance(config.processor, str)
        self.assertEqual(config.oss_endpoint, "oss-cn-shanghai.aliyuncs.com")
        self.assertEqual(
            config.model_path,
            "oss://test-sdk/test-model-deploy/model_flow_vhndmr3oa1x4kvvs9w_node_ksqe5z1g3je376zt2m_model.xml",
        )
        self.assertEqual(config.name, "lq_test_ecs_spec")
        self.assertEqual(config.compute_config.instance_type, "ecs.c6.large")
        self.assertEqual(config.compute_config.resource_id, "example_resource")

    def test_container_processor(self):
        data = {
            "containers": [{"command": "sleep 100", "image": "python:3", "port": 8002}],
            "dockerAuth": "aGVsbG86d29ybGQ=",
            "metadata": {
                "cpu": 1,
                "gpu": 0,
                "instance": 2,
                "memory": 2000,
            },
            "name": "lq_test_container",
        }
        config = ServiceConfig.from_api_object(data)

        self.assertIsInstance(config.processor, ContainerProcessor)
        self.assertTrue(bool(config.processor.docker_username))
        self.assertTrue(bool(config.processor.docker_password))
        self.assertEqual(config.name, "lq_test_container")
        self.assertEqual(config.compute_config.cpu, 1)
        self.assertEqual(config.compute_config.gpu, 0)
        self.assertEqual(config.compute_config.memory, 2000)
        self.assertEqual(config.instance_count, 2)
        result = config.to_api_object()
        self.assertEqual(result["name"], "lq_test_container")

    def test_custom_processor(self):
        data = {
            "metadata": {
                "cpu": 1,
                "gpu": 0,
                "instance": 2,
                "memory": 2000,
                "name": "lq_test_custom_process",
            },
            "model_path": "oss://lq-pai-test-1-sh/test-model-deploy/model_flow_vhndmr3oa1x4kvvs9w_node_ksqe5z1g3je376zt2m_model.xml",
            "oss_endpoint": "oss-cn-shanghai.aliyuncs.com",
            "processor_entry": "main.py",
            "processor_path": "oss://alink-test-2/model.ak.zip",
            "processor_type": "python",
        }

        config = ServiceConfig.from_api_object(data)
        self.assertEqual(config.model_path, data["model_path"])
        self.assertIsInstance(config.processor, CustomProcessor)
        self.assertEqual(config.processor.processor_type, "python")

        self.assertEqual(config.compute_config.memory, 2000)
        self.assertEqual(config.compute_config.cpu, 1)
        self.assertEqual(config.instance_count, 2)

    def test_build_in_processor(self):
        data = {
            "cloud": {
                "computing": {"instance_type": "ecs.c6.large"},
                "networking": {
                    "default_route": "eth0",
                    "destination_cidrs": "192.168.0.1/8",
                    "security_group_id": "sg-uf68sxd8cxajzc5mzjne",
                    "vpc_id": "vpc-uf6t31q3xii741wfpru3d",
                    "vswitch_id": "vsw-uf6kv5tuc5dgdmdw67ah2",
                },
            },
            "metadata": {
                "cpu": 2,
                "instance": 1,
                "memory": 4000,
                "name": "lq_test_ecs_spec",
            },
            "model_path": "oss://lq-pai-test-1-sh/test-model-deploy/model_flow_vhndmr3oa1x4kvvs9w_node_ksqe5z1g3je376zt2m_model.xml",
            "oss_endpoint": "oss-cn-shanghai.aliyuncs.com",
            "processor": "pmml",
            "source": "region=cn-shanghai,worksapceId=264097,kind=Model,id=model-xqb38zx588izhqa1kt/1.0.0",
        }
        config = ServiceConfig.from_api_object(data)
        self.assertTrue(not config.blue_green_release)
        self.assertTrue(not config.service_group_name)
        self.assertEqual(config.processor, "pmml")
        self.assertEqual(config.compute_config.instance_type, "ecs.c6.large")
        self.assertEqual(config.compute_config.cpu, 2)
        self.assertEqual(config.compute_config.memory, 4000)
        result = config.to_api_object()

        self.assertEqual(
            result["cloud"]["computing"]["instance_type"],
            config.compute_config.instance_type,
        )
        self.assertEqual(result["metadata"]["instance"], config.instance_count)

    def test_make_config(self):
        config = ServiceConfig(
            name="test_service_make_config",
            instance_count=2,
            service_group_name="test_service_group",
            compute_config=ComputeConfig(
                cpu=1,
                memory=2000,
            ),
            processor=BuildInProcessor.PMML,
            model_path="oss://unit-test-bucket.oss-cn-shanghai.aliyuncs.com/path/to/model",
            token="exampleToken",
        )
        data = config.to_api_object()

        self.assertDictEqual(
            data,
            {
                "name": "test_service_make_config",
                "metadata": {
                    "cpu": 1,
                    "memory": 2000,
                    "gpu": 0,
                    "instance": 2,
                    "group": "test_service_group",
                },
                "model_path": "oss://unit-test-bucket/path/to/model",
                "processor": "pmml",
                "token": "exampleToken",
            },
        )

    def test_blue_green_release(self):
        config = ServiceConfig(
            name="test_service_make_config",
            instance_count=2,
            compute_config=ComputeConfig(
                cpu=1,
                memory=2000,
            ),
            processor=BuildInProcessor.PMML,
            model_path="oss://unit-test-bucket.oss-cn-shanghai.aliyuncs.com/path/to/model",
            blue_green_release=True,
            service_group_name="test_service_group",
        )
        data = config.to_api_object()
        self.assertEqual(data["metadata"]["release"], True)
        self.assertEqual(data["metadata"]["group"], "test_service_group")

        c = ServiceConfig.from_api_object(data)

        self.assertTrue(c.blue_green_release)
        self.assertTrue(c.service_group_name == "test_service_group")

    def test_rpc_config_1(self):
        config = ServiceConfig(
            name="test_service_rpc_config",
            instance_count=2,
            rpc_config=ServiceRpcConfig(
                keepalive=1000,
                io_threads=2,
                # batching=None,
                max_batch_size=2,
                worker_threads=5,
                max_queue_size=10,
                max_batch_timeout=100,
            ),
        )

        self.assertEqual(
            config.to_api_object(),
            {
                "metadata": {"instance": 2, "rpc.io_threads": 2, "rpc.keepalive": 1000},
                "name": "test_service_rpc_config",
            },
        )

        c = ServiceConfig.from_api_object(config.to_api_object())
        self.assertFalse(bool(c.rpc_config.batching))
        self.assertEqual(c.rpc_config.keepalive, 1000)
        self.assertEqual(c.rpc_config.io_threads, 2)
        self.assertIsNone(c.rpc_config.max_batch_size)

    def test_rpc_config_enable_batching(self):
        config = ServiceConfig(
            name="test_service_rpc_config",
            instance_count=2,
            rpc_config=ServiceRpcConfig(
                keepalive=1000,
                # io_threads=2,
                batching=True,
                max_batch_size=2,
                worker_threads=5,
                max_queue_size=10,
                max_batch_timeout=100,
            ),
        )

        self.assertEqual(
            config.to_api_object(),
            {
                "metadata": {
                    "instance": 2,
                    "rpc.keepalive": 1000,
                    "rpc.batching": True,
                    "rpc.max_batch_size": 2,
                    "rpc.max_batch_timeout": 100,
                    "rpc.max_queue_size": 10,
                    "rpc.worker_threads": 5,
                },
                "name": "test_service_rpc_config",
            },
        )

        c = ServiceConfig.from_api_object(config.to_api_object())
        self.assertTrue(c.rpc_config.keepalive, 1000)
        self.assertTrue(c.rpc_config.batching)
        self.assertEqual(c.rpc_config.max_batch_size, 2)
        self.assertEqual(c.rpc_config.max_queue_size, 10)
        self.assertEqual(c.rpc_config.worker_threads, 5)
        self.assertEqual(c.rpc_config.max_batch_timeout, 100)
