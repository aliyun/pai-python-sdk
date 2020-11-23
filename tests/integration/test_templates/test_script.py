from pai.pipeline import PipelineRunStatus
from pai.pipeline.templates import (
    ScriptTemplate,
    PAI_SOURCE_CODE_ENV_KEY,
    PAI_PROGRAM_ENTRY_POINT_ENV_KEY,
)

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
from tests.test_data import SCRIPT_DIR_PATH


class TestScriptTemplate(BaseIntegTestCase):
    def test_script(self):
        templ = ScriptTemplate(
            entry_point="main.py",
            source_dir=SCRIPT_DIR_PATH,
            inputs=[
                PipelineParameter(name="foo", typ=int, default=10),
                PipelineParameter(name="bar", typ=int, default=200),
                PipelineArtifact(
                    name="dataSet",
                    metadata=ArtifactMetadata(
                        data_type=ArtifactDataType.DataSet,
                        location_type=ArtifactLocationType.OSS,
                    ),
                ),
            ],
            outputs=[
                PipelineParameter(name="result", typ=int, default=100),
                PipelineArtifact(
                    name="handled",
                    metadata=ArtifactMetadata(
                        data_type=ArtifactDataType.DataSet,
                        location_type=ArtifactLocationType.OSS,
                    ),
                ),
            ],
            image_uri="registry.cn-shanghai.aliyuncs.com/paiflow-core/base:0.1.0",
        )
        templ.prepare()
        manifest = templ.to_dict()
        env_vars = manifest["spec"]["execution"]["env"]

        self.assertTrue(PAI_SOURCE_CODE_ENV_KEY in env_vars)
        self.assertEqual(env_vars[PAI_PROGRAM_ENTRY_POINT_ENV_KEY], "main.py")
        run = templ.run(job_name="HelloWorld", wait=True)
        self.assertEqual(run.get_status(), PipelineRunStatus.Succeeded)
