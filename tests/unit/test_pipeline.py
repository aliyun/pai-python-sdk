from pai.common import ProviderAlibabaPAI
from pai.pipeline import Pipeline
from pai.pipeline.step import PipelineStep
from pai.pipeline.types import (
    PipelineArtifact,
    LocationArtifactMetadata,
    LocationType,
    DataType,
)
from tests.unit import BaseUnitTestCase


class TestPipelineBuild(BaseUnitTestCase):

    RepeatedArtifactExampleIdentifier = "repeated_artifact_example"

    def test_repeated_artifact_case_1(self):

        input_table = PipelineArtifact(
            "input_table",
            metadata=LocationArtifactMetadata(
                data_type=DataType.DataSet, location_type=LocationType.MaxComputeTable
            ),
        )

        step1 = PipelineStep(
            identifier="split",
            provider=ProviderAlibabaPAI,
            version="v1",
            inputs={"inputTable": input_table},
        )

        step2 = PipelineStep(
            identifier=self.RepeatedArtifactExampleIdentifier,
            provider=ProviderAlibabaPAI,
            version="v1",
            inputs={
                "input1": [
                    step1.outputs.artifacts[0],
                    step1.outputs.artifacts[1],
                    "odps://pai_online_project/tables/wumai_data",
                ],
            },
        )

        step3 = PipelineStep(
            identifier=self.RepeatedArtifactExampleIdentifier,
            provider=ProviderAlibabaPAI,
            version="v1",
            inputs={
                "input1": [
                    step2.outputs.artifacts[0][10],
                    step1.outputs.artifacts[1],
                    "odps://pai_online_project/tables/wumai_data",
                ],
            },
        )

        _ = Pipeline(steps=[step3], outputs=[step3.outputs[0], step1.outputs[0]])
