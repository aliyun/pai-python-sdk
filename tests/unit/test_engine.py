from __future__ import absolute_import

from pai.core.engine import (
    EngineEnvType,
    ComputeEngineType,
    ComputeEngine,
    MaxComputeEngine,
)
from tests.unit import BaseUnitTestCase


class TestComputeEngine(BaseUnitTestCase):
    def test_compute_engine_load(self):
        cases = [
            {
                "name": "max_compute_engine",
                "input": {
                    "IsDefault": False,
                    "Name": "xianzhitest225",
                    "ResourceInstances": [
                        {
                            "CreateTime": 1608032817000,
                            "EnvType": "prod",
                            "Id": "141409",
                            "IsDefault": False,
                            "Name": "xianzhitest225",
                            "ProductType": "MaxCompute",
                            "ResourceGroups": [
                                {
                                    "CardType": None,
                                    "CommodityCode": "post-odps",
                                    "Mode": "share",
                                    "Name": "aliyun_group_ay20",
                                    "ProductType": "MaxCompute",
                                    "Quotas": [
                                        {
                                            "Name": "aliyun",
                                            "Spec": '{"cu":"11500","minCu":"2300","parentId":"0"}',
                                        }
                                    ],
                                },
                                {
                                    "CardType": None,
                                    "CommodityCode": "pai",
                                    "Mode": "share",
                                    "Name": "aliyun_pai_public",
                                    "ProductType": "PAI",
                                    "Quotas": [{"Name": None, "Spec": "{}"}],
                                },
                            ],
                            "Spec": '{"Endpoint":"http://service.odps.aliyun.com/api","ProjectName":"xianzhitest225"}',
                            "WorkspaceId": "46296",
                        }
                    ],
                },
                "expected": {
                    "cls": MaxComputeEngine,
                    "attributes": {
                        "is_default": False,
                        "name": "xianzhitest225",
                        "EngineType": ComputeEngineType.MaxCompute,
                        "workspace_id": "46296",
                    },
                    "project_instances": [
                        {
                            "id": "141409",
                            "env_type": EngineEnvType.Production,
                            "name": "xianzhitest225",
                            "workspace_id": "46296",
                            "project_name": "xianzhitest225",
                            "endpoint": "http://service.odps.aliyun.com/api",
                        },
                    ],
                    "to_execution_config": [
                        {
                            "args": {
                                "env_type": None,
                            },
                            "result": {
                                "endpoint": "http://service.odps.aliyun.com/api",
                                "project": "xianzhitest225",
                            },
                        },
                        {
                            "args": {
                                "env_type": "prod",
                            },
                            "result": {
                                "endpoint": "http://service.odps.aliyun.com/api",
                                "project": "xianzhitest225",
                            },
                        },
                    ],
                },
            },
            {
                "name": "max_compute_v2",
                "input": {
                    "IsDefault": True,
                    "Name": "lq_test",
                    "ResourceInstances": [
                        {
                            "CreateTime": 1608546150000,
                            "EnvType": "dev",
                            "Id": "144521",
                            "IsDefault": True,
                            "Name": "lq_test_v2_dev",
                            "ProductType": "MaxCompute",
                            "ResourceGroups": [
                                {
                                    "CardType": None,
                                    "CommodityCode": "post-odps",
                                    "Mode": "share",
                                    "Name": "aliyun_group_ay20",
                                    "ProductType": "MaxCompute",
                                    "Quotas": [
                                        {
                                            "Name": "aliyun",
                                            "Spec": '{"cu":"11500","minCu":"2300"}',
                                        }
                                    ],
                                }
                            ],
                            "Spec": '{"Endpoint":"http://service.odps.aliyun.com/api","ProjectName":"lq_test_v2_dev"}',
                            "WorkspaceId": "152770",
                        },
                        {
                            "CreateTime": 1608546140000,
                            "EnvType": "prod",
                            "Id": "144520",
                            "IsDefault": True,
                            "Name": "lq_test_v2",
                            "ProductType": "MaxCompute",
                            "ResourceGroups": [
                                {
                                    "CardType": None,
                                    "CommodityCode": "post-odps",
                                    "Mode": "share",
                                    "Name": "aliyun_group_ay20",
                                    "ProductType": "MaxCompute",
                                    "Quotas": [
                                        {
                                            "Name": "aliyun",
                                            "Spec": '{"cu":"11500","minCu":"2300"}',
                                        }
                                    ],
                                }
                            ],
                            "Spec": '{"Endpoint":"http://service.odps.aliyun.com/api","ProjectName":"lq_test_v2"}',
                            "WorkspaceId": "152770",
                        },
                    ],
                },
                "expected": {
                    "cls": MaxComputeEngine,
                    "attributes": {
                        "is_default": True,
                        "name": "lq_test",
                        "EngineType": ComputeEngineType.MaxCompute,
                        "workspace_id": "152770",
                    },
                    "project_instances": [
                        {
                            "id": "144521",
                            "env_type": EngineEnvType.Develop,
                            "name": "lq_test_v2_dev",
                            "workspace_id": "152770",
                            "project_name": "lq_test_v2_dev",
                            "endpoint": "http://service.odps.aliyun.com/api",
                        },
                        {
                            "id": "144520",
                            "env_type": EngineEnvType.Production,
                            "name": "lq_test_v2",
                            "workspace_id": "152770",
                            "project_name": "lq_test_v2",
                            "endpoint": "http://service.odps.aliyun.com/api",
                        },
                    ],
                    "to_execution_config": [
                        {
                            "args": {
                                "env_type": None,
                            },
                            "result": {
                                "endpoint": "http://service.odps.aliyun.com/api",
                                "project": "lq_test_v2_dev",
                            },
                        },
                        {
                            "args": {
                                "env_type": EngineEnvType.Develop,
                            },
                            "result": {
                                "endpoint": "http://service.odps.aliyun.com/api",
                                "project": "lq_test_v2_dev",
                            },
                        },
                        {
                            "args": {
                                "env_type": EngineEnvType.Production,
                            },
                            "result": {
                                "endpoint": "http://service.odps.aliyun.com/api",
                                "project": "lq_test_v2",
                            },
                        },
                    ],
                },
            },
        ]

        for case in cases:
            compute_engine = ComputeEngine.load_from_dict(case["input"])
            self.assertIsInstance(
                compute_engine,
                case["expected"]["cls"],
                "case: %s failure" % case["name"],
            )

            for attr_name, attr_value in case["expected"]["attributes"].items():
                self.assertEqual(
                    getattr(compute_engine, attr_name),
                    attr_value,
                    "case: %s failure" % case["name"],
                )
            for idx, instance_attributes in enumerate(
                case["expected"].get("project_instances", [])
            ):
                project_instance = compute_engine.project_instances[idx]
                for attr_name, attr_value in instance_attributes.items():
                    self.assertEqual(
                        getattr(project_instance, attr_name),
                        attr_value,
                        "case: %s, project_instance attribute: %s test failed"
                        % (case["name"], attr_name),
                    )

            for idx, item in enumerate(case["expected"]["to_execution_config"]):
                args = item["args"]
                self.assertEqual(
                    item["result"],
                    compute_engine.to_execution_config(**args),
                    "case:%s, to_execution_config:%s, test failed"
                    % (case["name"], idx),
                )
