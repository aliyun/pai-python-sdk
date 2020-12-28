# coding: utf-8

from pai.pipeline.templates.container import ContainerTemplate

from pai.pipeline.types import (
    PipelineArtifact,
    ArtifactMetadata,
    ArtifactDataType,
    ArtifactLocationType,
)
from pai.pipeline.types.parameter import (
    PipelineParameter,
)
from tests.integration import BaseIntegTestCase


class TestContainerTemplate(BaseIntegTestCase):
    def test_component_base(self):
        inputs = [
            PipelineParameter(name="xflow_name", typ=str),
            PipelineArtifact(
                name="inputs1",
                metadata=ArtifactMetadata(
                    data_type=ArtifactDataType.DataSet,
                    location_type=ArtifactLocationType.OSS,
                ),
            ),
        ]
        outputs = [
            PipelineArtifact(
                name="output1",
                metadata=ArtifactMetadata(
                    data_type=ArtifactDataType.DataSet,
                    location_type=ArtifactLocationType.OSS,
                ),
            ),
        ]

        container_templ = ContainerTemplate(
            image_uri="python:3",
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
