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

import contextlib
import io
import json
from unittest import skip

from pai.pipeline import Pipeline
from pai.pipeline.component import ContainerComponent
from pai.pipeline.types import PipelineParameter
from pai.pipeline.types.parameter import LoopItemPlaceholder
from tests.integration import BaseIntegTestCase


@skip("Backend is not stable.")
class TestLoopPipeline(BaseIntegTestCase):
    def test_loop_with_sequence(self):
        op = ContainerComponent(
            inputs=[
                PipelineParameter("foo", default="valueFoo"),
                PipelineParameter("bar", default="valueBar"),
            ],
            image_uri="python:3",
            env={
                "PYTHONUNBUFFERED": "1",
            },
            command=[
                "bash",
                "-c",
                "echo foo={{inputs.parameters.foo}} bar=={{inputs.parameters.bar}}",
            ],
        )
        step1 = op.as_loop_step(
            name="loop-range",
            items=range(0, 10),
            parallelism=10,
            inputs={
                "foo": LoopItemPlaceholder(),
            },
        )
        p = Pipeline(steps=[step1])
        print(p.to_manifest(identifier="example", version="v1"))
        run_output = io.StringIO()
        with contextlib.redirect_stdout(run_output):
            p.run(job_name="test_loop_with_sequence")
        print(run_output)
        self.assertTrue("foo=1" in run_output.getvalue())

    def test_loop_with_param(self):
        output_param_name = "outputparam"
        output_params = json.dumps(["hello", "world"])
        op = ContainerComponent(
            inputs=[
                PipelineParameter("foo", default="valueFoo"),
                PipelineParameter("bar", default="valueBar"),
            ],
            outputs=[
                PipelineParameter(output_param_name),
            ],
            image_uri="python:3",
            env={
                "PYTHONUNBUFFERED": "1",
            },
            command=[
                "bash",
                "-c",
                "echo foo={{inputs.parameters.foo}} bar=={{inputs.parameters.bar}}"
                " && mkdir -p  /pai/outputs/parameters/ "
                " && echo '%s' > /pai/outputs/parameters/%s"
                " && cat  /pai/outputs/parameters/%s"
                % (output_params, output_param_name, output_param_name),
            ],
        )

        step1 = op.as_step(name="step1")
        step_loop = op.as_loop_step(
            name="loop-with-param",
            items=step1.outputs[0],
            inputs={"foo": "{{item}}"},
            parallelism=5,
        )
        step_valid = op.as_step(
            name="step-print-param",
            inputs={
                "foo": step1.outputs[0],
            },
        )
        p = Pipeline(steps=[step1, step_loop, step_valid])
        print(p.to_manifest(identifier="example", version="v1"))

        run_output = io.StringIO()
        with contextlib.redirect_stdout(run_output):
            p.run(job_name="test_loop_with_param")
        print(run_output.getvalue())
        self.assertTrue("foo=hello" in run_output.getvalue())
        self.assertTrue("foo=world" in run_output.getvalue())

    def test_loop_with_items(self):
        op = ContainerComponent(
            inputs=[
                PipelineParameter("foo", default="valueFoo"),
                PipelineParameter("bar", default="valueBar"),
            ],
            image_uri="python:3",
            env={
                "PYTHONUNBUFFERED": "1",
            },
            command=[
                "bash",
                "-c",
                "echo foo={{inputs.parameters.foo}} bar=={{inputs.parameters.bar}}",
            ],
        )

        step1 = op.as_loop_step(
            name="loop-with-items",
            items=["hello", "world"],
            inputs={"foo": LoopItemPlaceholder()},
        )
        p = Pipeline(steps=[step1])
        print(p.to_manifest(identifier="example", version="v1"))
        run_output = io.StringIO()
        with contextlib.redirect_stdout(run_output):
            p.run(job_name="test_loop_with_items")
        print(run_output.getvalue())
        self.assertTrue("foo=hello" in run_output.getvalue())
