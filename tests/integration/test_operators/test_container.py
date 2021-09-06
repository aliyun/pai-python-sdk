# coding: utf-8
from pprint import pprint

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

    def test_from_source_files(self):
        script_dir = "../../test_data/script_dir"
        op = ContainerOperator.from_scripts(
            source_dir=script_dir,
            entry_file="main.py",
            inputs=[PipelineParameter("foo")],
            outputs=[],
            image_uri="registry.cn-shanghai.aliyuncs.com/paiflow_custom_image/mlflow-serve-test:v1.0",
            install_packages=["requests"],
        )

        print(op.to_dict())

        op.run("hello", arguments={"foo": "Hello"})

    def test_from_script(self):
        op = ContainerOperator.from_script(
            script_file="../../test_data/script_dir/main.py",
            inputs=[PipelineParameter("foo")],
            outputs=[],
            image_uri="registry.cn-shanghai.aliyuncs.com/paiflow_custom_image/mlflow-serve-test:v1.0",
            install_packages=["requests"],
        )

        pprint(op.to_dict())
        op.run("hello", arguments={"foo": "Hello"})

    def test_from_script(self):
        op = ContainerOperator.from_script(
            script_file="../../test_data/shell_scripts/job.sh",
            inputs=[PipelineParameter("foo")],
            outputs=[],
            image_uri="python3",
            install_packages=["requests"],
        )

        print(yaml.dump(op.to_dict()))

        step1 = op.as_step(
            inputs={
                "foo": "alice",
            }
        )

        step2 = op.as_step(
            inputs={
                "foo": "bob",
            }
        )

        step2.after(step1)

        p = Pipeline(steps=[step1, step2])

        p.save(job_name="test")
