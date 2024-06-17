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

from pai.pipeline import Pipeline
from pai.pipeline.component import ContainerComponent
from pai.pipeline.types import (
    ArtifactMetadataUtils,
    PipelineArtifact,
    PipelineParameter,
)
from tests.unit import BaseUnitTestCase


class TestPipelineBuild(BaseUnitTestCase):
    def test_io_name_conflict(self):
        input_params = [
            PipelineParameter(name="input1", default="hello"),
            PipelineParameter(name="input2", default="world"),
        ]
        output_artifacts = [
            PipelineArtifact(name="output1", metadata=ArtifactMetadataUtils.raw()),
            PipelineArtifact(name="output2", metadata=ArtifactMetadataUtils.raw()),
        ]

        op = ContainerComponent(
            image_uri="python:3",
            inputs=input_params,
            outputs=output_artifacts,
            command="echo hello",
        )
        step1 = op.as_step(name="step1")
        step2 = op.as_step(name="step2")

        _ = Pipeline(
            steps=[step1, step2],
            outputs={
                "step1_output1": step1.outputs["output1"],
                "step1_output2": step2.outputs["output1"],
            },
        )

        with self.assertRaisesRegex(ValueError, ".*conflict.*") as _:
            step1 = op.as_step(name="step1")
            step2 = op.as_step(name="step2")
            _ = Pipeline(
                steps=[step1, step2],
                outputs=[step1.outputs["output1"], step2.outputs["output1"]],
            )

    def test_condition_step(self):

        inputs = [
            PipelineParameter(name="foo", default="hello"),
            PipelineParameter(name="bar", default="world"),
        ]
        outputs = [
            PipelineParameter(name="outputParam"),
        ]

        op = ContainerComponent(
            image_uri="python:3",
            inputs=inputs,
            outputs=outputs,
            command="echo hello",
        )

        step1 = op.as_step(
            name="step1",
        )

        eq_case = op.as_condition_step(
            condition=step1.outputs[0] == "true", name="step1", inputs={}
        ).to_dict()

        self.assertEqual(
            eq_case["spec"]["when"],
            "{{pipelines.step1.outputs.parameters.outputParam}} == true",
        )

        neq_case = op.as_condition_step(
            condition=step1.outputs[0] != "true", name="step1", inputs={}
        ).to_dict()

        self.assertEqual(
            neq_case["spec"]["when"],
            "{{pipelines.step1.outputs.parameters.outputParam}} != true",
        )

        lt_case = op.as_condition_step(
            condition=step1.outputs[0] < "true", name="step1", inputs={}
        ).to_dict()

        self.assertEqual(
            lt_case["spec"]["when"],
            "{{pipelines.step1.outputs.parameters.outputParam}} < true",
        )

        gt_case = op.as_condition_step(
            condition=step1.outputs[0] > "true", name="step1", inputs={}
        ).to_dict()

        self.assertEqual(
            gt_case["spec"]["when"],
            "{{pipelines.step1.outputs.parameters.outputParam}} > true",
        )
        geq_case = op.as_condition_step(
            condition=step1.outputs[0] >= "true", name="step1", inputs={}
        ).to_dict()
        self.assertEqual(
            geq_case["spec"]["when"],
            "{{pipelines.step1.outputs.parameters.outputParam}} >= true",
        )

        leq_case = op.as_condition_step(
            condition=step1.outputs[0] <= "true", name="step1", inputs={}
        ).to_dict()
        self.assertEqual(
            leq_case["spec"]["when"],
            "{{pipelines.step1.outputs.parameters.outputParam}} <= true",
        )

    def test_loop_step(self):
        inputs = [
            PipelineParameter(name="foo", default="hello"),
            PipelineParameter(name="bar", default="world"),
        ]
        outputs = [
            PipelineParameter(name="outputParam"),
        ]

        op = ContainerComponent(
            image_uri="python:3",
            inputs=inputs,
            outputs=outputs,
            command="echo hello",
        )

        range_case = op.as_loop_step(items=range(0, 10), name="step1").to_dict()

        self.assertEqual(
            range_case["spec"]["withSequence"],
            {
                "start": 0,
                "end": 10,
            },
        )

        item_list_case = op.as_loop_step(
            items=[
                {
                    "foo": "bar",
                },
                {
                    "hello": "world",
                },
            ],
            name="step1",
        ).to_dict()

        self.assertEqual(
            item_list_case["spec"]["withItems"],
            [
                {
                    "foo": "bar",
                },
                {
                    "hello": "world",
                },
            ],
        )

        output_step1 = op.as_step(name="stepOutput")
        output_param_case = op.as_loop_step(
            items=output_step1.outputs[0], name="step1"
        ).to_dict()

        self.assertEqual(
            output_param_case["spec"]["withParam"],
            "{{pipelines.stepOutput.outputs.parameters.outputParam}}",
        )
