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
from pai.pipeline.types.artifact import MaxComputeTableArtifact
from pai.pipeline.types.parameter import (
    PipelineParameter,
)
from tests.integration import BaseIntegTestCase
from tests.test_data import SCRIPT_DIR_PATH, MAXC_SQL_TEMPLATE_SCRIPT_PATH


class TestScriptTemplate(BaseIntegTestCase):
    @classmethod
    def get_odps_config(cls):
        odps_config = cls.get_test_config()["odps"]
        return odps_config

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
        print(env_vars)

        self.assertTrue(PAI_SOURCE_CODE_ENV_KEY in env_vars)
        self.assertEqual(env_vars[PAI_PROGRAM_ENTRY_POINT_ENV_KEY], "main.py")
        run = templ.run(job_name="HelloWorld", wait=True)
        self.assertEqual(run.get_status(), PipelineRunStatus.Succeeded)

    def test_local_run(self):
        templ = ScriptTemplate(
            entry_point="main.py",
            source_dir=MAXC_SQL_TEMPLATE_SCRIPT_PATH,
            inputs=[
                PipelineParameter("sql"),
                PipelineParameter("execution", typ=dict),
                PipelineParameter("outputTable"),
                PipelineParameter("lifeCycle", typ=int, default=7),
                PipelineArtifact(
                    "t1",
                    ArtifactMetadata(
                        data_type=ArtifactDataType.DataSet,
                        location_type=ArtifactLocationType.MaxComputeTable,
                    ),
                ),
                PipelineArtifact(
                    "t2",
                    ArtifactMetadata(
                        data_type=ArtifactDataType.DataSet,
                        location_type=ArtifactLocationType.MaxComputeTable,
                    ),
                ),
                PipelineArtifact(
                    "t3",
                    ArtifactMetadata(
                        data_type=ArtifactDataType.DataSet,
                        location_type=ArtifactLocationType.MaxComputeTable,
                    ),
                ),
                PipelineArtifact(
                    "t4",
                    ArtifactMetadata(
                        data_type=ArtifactDataType.DataSet,
                        location_type=ArtifactLocationType.MaxComputeTable,
                    ),
                ),
            ],
            outputs=[
                PipelineArtifact(
                    "outputTable",
                    metadata=ArtifactMetadata(
                        data_type=ArtifactDataType.DataSet,
                        location_type=ArtifactLocationType.MaxComputeTable,
                    ),
                    value=MaxComputeTableArtifact.value_from_param("outputTable"),
                )
            ],
        )

        container = templ.run(
            job_name="helloWorld",
            local_mode=True,
            arguments={
                "sql": """
                -- SQL Example
                describe ${t1};
                select * from ${t2};
                """,
                "t1": "odps://pai_sdk_test/tables/sample",
                "t2": "odps://pai_sdk_test/tables/iris_data",
                "outputTable": "pai_temp_table",
                "execution": {
                    "endpoint": self.get_odps_config()["endpoint"],
                    "odpsProject": self.get_odps_config()["project"],
                    "accessKeyId": self.get_odps_config()["access_key_id"],
                    "accessKeySecret": self.get_odps_config()["access_key_secret"],
                },
            },
        )
        self.assertEqual(container.attrs["State"]["ExitCode"], 0)
