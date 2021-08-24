from unittest import skip

import contextlib
import os

from pai.common.utils import gen_temp_table
from pai.operator import (
    ScriptOperator,
    PAI_SOURCE_CODE_ENV_KEY,
    PAI_PROGRAM_ENTRY_POINT_ENV_KEY,
)
from pai.operator.types import PipelineArtifact, MetadataBuilder
from pai.operator.types.artifact import MaxComputeTableArtifact
from pai.operator.types import (
    PipelineParameter,
)
from tests.integration import BaseIntegTestCase
from tests.test_data import (
    SCRIPT_DIR_PATH,
    MAXC_SQL_TEMPLATE_SCRIPT_PATH,
)


@contextlib.contextmanager
def cwd_context(target_dir):
    previous_dir = os.getcwd()
    os.chdir(target_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)


class TestScriptOperator(BaseIntegTestCase):
    @classmethod
    def get_maxc_config(cls):
        _, _, maxc_config = cls.load_test_config()
        return maxc_config

    def test_local_source_files(self):
        templ = ScriptOperator(
            entry_file="main.py",
            source_dir=SCRIPT_DIR_PATH,
            inputs=[
                PipelineParameter(name="foo", typ=str, default="Hello"),
                PipelineParameter(name="bar", typ=int, default=200),
            ],
        )
        templ.prepare()
        manifest = templ.to_dict()
        env_vars = manifest["spec"]["container"]["envs"]
        self.assertTrue(PAI_SOURCE_CODE_ENV_KEY in env_vars)
        self.assertEqual(env_vars[PAI_PROGRAM_ENTRY_POINT_ENV_KEY], "main.py")
        templ.run(job_name="HelloWorld")

    def test_single_local_file(self):
        templ = ScriptOperator(
            entry_file=os.path.join(SCRIPT_DIR_PATH, "main.py"),
            inputs=[
                PipelineParameter(name="foo", typ=int, default=10),
                PipelineParameter(name="bar", typ=int, default=200),
            ],
        )
        templ.prepare()
        manifest = templ.to_dict()
        env_vars = manifest["spec"]["container"]["envs"]
        self.assertTrue(PAI_SOURCE_CODE_ENV_KEY in env_vars)
        self.assertEqual(env_vars[PAI_PROGRAM_ENTRY_POINT_ENV_KEY], "main.py")

    def test_oss_source_files(self):
        templ = ScriptOperator(
            entry_file="main.py",
            source_dir="oss://oss_bucket.oss-cn-hangzhou.aliyuncs.com/path/to_files/source.tar.gz",
        )
        templ.prepare()
        manifest = templ.to_dict()
        env_vars = manifest["spec"]["container"]["envs"]
        self.assertTrue(
            env_vars[PAI_SOURCE_CODE_ENV_KEY],
            "oss://oss_bucket.oss-cn-hangzhou.aliyuncs.com/path/to_files/source.tar.gz",
        )
        self.assertEqual(env_vars[PAI_PROGRAM_ENTRY_POINT_ENV_KEY], "main.py")

    def test_oss_single_file(self):
        templ = ScriptOperator(
            entry_file="oss://oss_bucket.oss-cn-hangzhou.aliyuncs.com/path/to/main.py",
        )
        templ.prepare()
        manifest = templ.to_dict()
        env_vars = manifest["spec"]["container"]["envs"]
        self.assertTrue(
            env_vars[PAI_SOURCE_CODE_ENV_KEY],
            "oss://oss_bucket.oss-cn-hangzhou.aliyuncs.com/path/to/main.py",
        )
        self.assertEqual(env_vars[PAI_PROGRAM_ENTRY_POINT_ENV_KEY], "main.py")

    @skip("Aone dynamic container environment do not support docker in docker.")
    def test_local_run(self):
        templ = ScriptOperator(
            entry_file="main.py",
            source_dir=MAXC_SQL_TEMPLATE_SCRIPT_PATH,
            inputs=[
                PipelineParameter("sql"),
                PipelineParameter("execution", typ=dict),
                PipelineParameter("outputTable"),
                PipelineParameter("lifeCycle", typ=int, default=7),
                PipelineArtifact(
                    "t1",
                    metadata=MetadataBuilder.maxc_table(),
                ),
                PipelineArtifact(
                    "t2",
                    metadata=MetadataBuilder.maxc_table(),
                ),
                PipelineArtifact(
                    "t3",
                    metadata=MetadataBuilder.maxc_table(),
                ),
                PipelineArtifact(
                    "t4",
                    metadata=MetadataBuilder.maxc_table(),
                ),
            ],
            outputs=[
                PipelineArtifact(
                    "outputTable",
                    metadata=MetadataBuilder.maxc_table(),
                    value=MaxComputeTableArtifact.value_from_param("outputTable"),
                )
            ],
        )

        maxc_config = self.get_maxc_config()
        local_run_container = templ.run(
            job_name="helloWorld",
            local_mode=True,
            arguments={
                "sql": """
                -- SQL Example
                select * from ${t2};
                """,
                "t2": "odps://pai_online_project/tables/breast_cancer_data",
                "outputTable": gen_temp_table(),
                "execution": {
                    "endpoint": maxc_config.endpoint,
                    "odpsProject": maxc_config.project,
                    "accessKeyId": maxc_config.access_key_id,
                    "accessKeySecret": maxc_config.access_key_secret,
                },
            },
        )
        self.assertEqual(local_run_container.attrs["State"]["ExitCode"], 0)
