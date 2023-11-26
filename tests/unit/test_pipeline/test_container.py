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

import yaml

from pai.pipeline.component import ContainerComponent
from pai.pipeline.types import (
    DataType,
    LocationArtifactMetadata,
    LocationType,
    PipelineArtifact,
    PipelineParameter,
)
from tests.unit import BaseUnitTestCase


class TestContainerOperator(BaseUnitTestCase):
    def test_manifest(self):
        inputs = [
            PipelineParameter(name="epoch", typ=int),
            PipelineParameter(
                name="regularizedType",
                typ=str,
                default="l1",
            ),
            PipelineArtifact(
                name="dataset",
                metadata=LocationArtifactMetadata(
                    data_type=DataType.DataSet, location_type=LocationType.OSS
                ),
            ),
            PipelineArtifact(
                name="model",
                metadata=LocationArtifactMetadata(
                    data_type=DataType.Model, location_type=LocationType.OSS
                ),
            ),
        ]

        outputs = [
            PipelineArtifact(
                name="output1",
                metadata=LocationArtifactMetadata(
                    data_type=DataType.DataSet, location_type=LocationType.OSS
                ),
            ),
            PipelineArtifact(
                name="output2",
                metadata=LocationArtifactMetadata(
                    data_type=DataType.Model, location_type=LocationType.OSS
                ),
            ),
        ]

        image_registry_config = {
            "userName": "testUserName",
            "password": "testPassword",
        }
        env_vars = {
            "PAI_SOURCE_CODE": "oss://hello/world/source-code.gz.tar",
            "PAI_ENTRY_POINT": "run.py",
        }
        image_uri = "registry.cn-shanghai.aliyuncs.com/paiflow-core/xflow_base:v1.1"
        command = ["train"]

        templ = ContainerComponent(
            image_uri=image_uri,
            command=command,
            image_registry_config=image_registry_config,
            inputs=inputs,
            outputs=outputs,
            env=env_vars,
        )
        manifest = templ.to_dict()
        print(yaml.dump(manifest))

        input_params_spec = manifest["spec"]["inputs"]["parameters"]
        input_artifacts_spec = manifest["spec"]["inputs"]["artifacts"]
        output_artifacts_spec = manifest["spec"]["outputs"]["artifacts"]
        env_spec = manifest["spec"]["container"]["envs"]

        self.assertEqual(
            input_params_spec,
            [
                {"name": "epoch", "type": "Int"},
                {"name": "regularizedType", "type": "String", "value": "l1"},
            ],
        )

        self.assertEqual(
            input_artifacts_spec,
            [
                {
                    "metadata": {"type": {"DataSet": {"locationType": "OSS"}}},
                    "name": "dataset",
                    "required": False,
                },
                {
                    "metadata": {"type": {"Model": {"locationType": "OSS"}}},
                    "name": "model",
                    "required": False,
                },
            ],
        )

        self.assertEqual(
            output_artifacts_spec,
            [
                {
                    "metadata": {"type": {"DataSet": {"locationType": "OSS"}}},
                    "name": "output1",
                    "required": False,
                },
                {
                    "metadata": {"type": {"Model": {"locationType": "OSS"}}},
                    "name": "output2",
                    "required": False,
                },
            ],
        )

        self.assertEqual(env_spec, env_vars)
        self.assertEqual(manifest["spec"]["container"]["command"], command)
        self.assertEqual(manifest["spec"]["container"]["image"], image_uri)
        self.assertEqual(
            manifest["spec"]["container"]["imageRegistryConfig"], image_registry_config
        )
