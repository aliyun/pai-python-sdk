# coding: utf-8
import yaml

from pai.operator import ContainerOperator

from pai.operator.types import (
    PipelineArtifact,
    LocationArtifactMetadata,
    DataType,
    LocationType,
)
from pai.operator.types import (
    PipelineParameter,
)
from tests.integration import BaseIntegTestCase


class TestContainerOperator(BaseIntegTestCase):
    def test_component_base(self):
        inputs = [
            PipelineParameter(name="xflow_name", typ=str),
            PipelineArtifact(
                name="inputs1",
                metadata=LocationArtifactMetadata(
                    data_type=DataType.DataSet, location_type=LocationType.OSS
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
        ]

        container_templ = ContainerOperator(
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

        container_templ.run(
            job_name="hello-world",
            arguments={
                "xflow_name": "abcd",
            },
        )

    def test_from_scripts(self):
        # op = ContainerOperator.from_scripts(
        #     source_dir="/Users/liangquan/code/pypai/tests/test_data/script_dir",
        #     entry_file="main.py",
        #     inputs=[],
        #     outputs=[],
        #     image_uri="test_image",
        #     install_packages=["requests"],
        # )

        print(PipelineParameter("x").fullname)

        # op.as_step()