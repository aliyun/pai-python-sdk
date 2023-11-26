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

from unittest import skip

from pai.pipeline import Pipeline
from pai.pipeline.component import ContainerComponent
from pai.pipeline.types import PipelineParameter
from tests.integration import BaseIntegTestCase


class TestUnRegisteredComponent(BaseIntegTestCase):
    @skip("Skip for now")
    def test_pipeline(self):
        python_image = self.get_python_image()

        op1 = ContainerComponent(
            inputs=[PipelineParameter("foo"), PipelineParameter("bar")],
            outputs=[],
            image_uri=python_image,
            command=[
                "python",
                "-u",
                "-c",
                "print('{{inputs.parameters.foo}} {{inputs.parameters.bar}}')",
            ],
        )

        def build_pipeline():
            x = PipelineParameter("foo")
            y = PipelineParameter("bar")
            step1 = op1.as_step(
                inputs={
                    "foo": x,
                    "bar": y,
                },
                name="step1",
            )

            step2 = op1.as_step(
                inputs={
                    "foo": "hello",
                    "bar": "world",
                }
            )

            step2.after(step1)

            return Pipeline(steps=[step1, step2])

        p = build_pipeline()
        p.run(
            job_name="test_container_op_pipeline",
            arguments={
                "foo": "Hello",
                "bar": "World",
            },
        )
