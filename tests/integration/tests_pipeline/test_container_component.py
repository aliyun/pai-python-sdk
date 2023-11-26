# coding: utf-8

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

import time
from unittest import skip

from pai.pipeline import Pipeline
from pai.pipeline.component import ContainerComponent, RegisteredComponent
from pai.pipeline.types import (
    DataType,
    LocationArtifactMetadata,
    LocationType,
    PipelineArtifact,
    PipelineParameter,
)
from tests.integration import BaseIntegTestCase


class TestContainerOperator(BaseIntegTestCase):
    @skip("Skip for now")
    def test_component_base(self):
        inputs = [
            PipelineParameter(name="xflow_name", typ=str, desc="ExampleParam"),
            PipelineArtifact(
                name="inputs1",
                metadata=LocationArtifactMetadata(
                    data_type=DataType.DataSet, location_type=LocationType.OSS
                ),
                desc="ExampleInputArtifact",
            ),
        ]
        outputs = [
            PipelineArtifact(
                name="output1",
                metadata=LocationArtifactMetadata(
                    data_type=DataType.DataSet, location_type=LocationType.OSS
                ),
                desc="ExampleOutputArtifact",
            ),
        ]

        container_templ = ContainerComponent(
            image_uri=self.get_python_image(),
            inputs=inputs,
            outputs=outputs,
            command=[
                "python",
                "-c",
                "import os; print('\\n'.join(['%s=%s' % (k, v) for k, v in os.environ.items()]));",
            ],
            env={"HelloWorld": '"{{inputs.parameters}}"'},
        )

        version = "v-%s" % int(time.time())
        registered_op = container_templ.save(identifier="ExampleOp", version=version)
        self.assertEqual(registered_op.inputs["xflow_name"].desc, "ExampleParam")
        self.assertEqual(registered_op.inputs["inputs1"].desc, "ExampleInputArtifact")
        self.assertEqual(registered_op.outputs["output1"].desc, "ExampleOutputArtifact")
        container_templ.run(
            job_name="hello-world",
            arguments={
                "xflow_name": "abcd",
            },
        )
        registered_op.delete()

    def test_container_op_crud(self):
        op1 = ContainerComponent(
            image_uri=self.get_python_image(),
            inputs=[],
            outputs=[],
            command=[
                "python",
                "-c",
                "import os; print('\\n'.join(['%s=%s' % (k, v) for k, v in os.environ.items()]));",
            ],
        )

        op_version = "v-%s" % int(time.time())
        op_identifier = "containerOpExample"

        # test register and get component
        reg_op = op1.save(identifier=op_identifier, version=op_version)
        remote_op = RegisteredComponent.get_by_identifier(
            identifier=op_identifier, version=op_version
        )

        assert reg_op == remote_op

        # test update component manifest
        op2 = ContainerComponent(
            image_uri=self.get_python_image(),
            inputs=[],
            outputs=[],
            command=[
                "echo",
                "HelloWorld",
            ],
        )
        op2_manifest = op2.to_manifest(identifier=op_identifier, version=op_version)
        reg_op.update(op2_manifest)

        # test delete component
        reg_op.delete()
        with self.assertRaises(ValueError):
            _ = RegisteredComponent.get_by_identifier(
                identifier=op_identifier, version=op_version
            )

    def test_pipeline_update(self):

        op1 = ContainerComponent(
            image_uri=self.get_python_image(),
            inputs=[PipelineParameter("x", default="10")],
            outputs=[],
            command=[
                "python",
                "-c",
                "import os; print('\\n'.join(['%s=%s' % (k, v) for k, v in os.environ.items()]));",
            ],
        )

        def create_pipeline(x):
            step1 = op1.as_step("step1", inputs={"x": x})
            step2 = op1.as_step("step2", inputs={"x": x})
            return Pipeline(steps=[step1, step2])

        p = create_pipeline(10)

        version = "v-%s" % int(time.time())
        identifier = "examplePipeline"

        reg_pipeline = p.save(identifier=identifier, version=version)

        p2 = create_pipeline(100)

        p2_manifest = p2.to_manifest(identifier=identifier, version=version)
        reg_pipeline.update(component=p2_manifest)
        reg_pipeline.delete()
