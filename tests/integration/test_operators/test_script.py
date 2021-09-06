import os
from unittest import skip

import contextlib

from pai.common.utils import gen_temp_table
from pai.operator import (
    ScriptOperator,
    PAI_SOURCE_CODE_ENV_KEY,
    PAI_PROGRAM_ENTRY_POINT_ENV_KEY,
)
from pai.operator.types import PipelineArtifact, MetadataBuilder
from pai.operator.types import (
    PipelineParameter,
)
from pai.operator.types.artifact import MaxComputeTableArtifact
from pai.pipeline import Pipeline
from tests.integration import BaseIntegTestCase
from tests.test_data import (
    SCRIPT_DIR_PATH,
    MAXC_SQL_TEMPLATE_SCRIPT_PATH,
    SHELL_SCRIPT_DIR_PATH,
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
        templ = ScriptOperator.create_with_oss_snapshot(
            entry_file="main.py",
            source_dir=SCRIPT_DIR_PATH,
            inputs=[
                PipelineParameter(name="foo", typ=str, default="Hello"),
                PipelineParameter(name="bar", typ=int, default=200),
            ],
        )
        manifest = templ.to_dict()
        env_vars = manifest["spec"]["container"]["envs"]
        self.assertTrue(PAI_SOURCE_CODE_ENV_KEY in env_vars)
        self.assertEqual(env_vars[PAI_PROGRAM_ENTRY_POINT_ENV_KEY], "main.py")
        templ.run(job_name="HelloWorld")

    def test_single_local_file(self):
        templ = ScriptOperator.create_with_oss_snapshot(
            entry_file=os.path.join(SCRIPT_DIR_PATH, "main.py"),
            inputs=[
                PipelineParameter(name="foo", typ=int, default=10),
                PipelineParameter(name="bar", typ=int, default=200),
            ],
        )
        # templ.prepare()
        manifest = templ.to_dict()
        env_vars = manifest["spec"]["container"]["envs"]
        self.assertTrue(PAI_SOURCE_CODE_ENV_KEY in env_vars)
        self.assertEqual(env_vars[PAI_PROGRAM_ENTRY_POINT_ENV_KEY], "main.py")

    def test_oss_source_files(self):
        templ = ScriptOperator.create_with_oss_snapshot(
            entry_file="main.py",
            source_dir="oss://oss_bucket.oss-cn-hangzhou.aliyuncs.com/path/to_files/source.tar.gz",
        )
        manifest = templ.to_dict()
        env_vars = manifest["spec"]["container"]["envs"]
        self.assertTrue(
            env_vars[PAI_SOURCE_CODE_ENV_KEY],
            "oss://oss_bucket.oss-cn-hangzhou.aliyuncs.com/path/to_files/source.tar.gz",
        )
        self.assertEqual(env_vars[PAI_PROGRAM_ENTRY_POINT_ENV_KEY], "main.py")

    def test_oss_single_file(self):
        templ = ScriptOperator.create_with_oss_snapshot(
            entry_file="oss://oss_bucket.oss-cn-hangzhou.aliyuncs.com/path/to/main.py",
        )
        manifest = templ.to_dict()
        env_vars = manifest["spec"]["container"]["envs"]
        self.assertTrue(
            env_vars[PAI_SOURCE_CODE_ENV_KEY],
            "oss://oss_bucket.oss-cn-hangzhou.aliyuncs.com/path/to/main.py",
        )
        self.assertEqual(env_vars[PAI_PROGRAM_ENTRY_POINT_ENV_KEY], "main.py")

    @skip("Aone dynamic container environment do not support docker in docker.")
    def test_local_run(self):
        templ = ScriptOperator.create_with_oss_snapshot(
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

    def test_image_snapshot(self):
        op = ScriptOperator.create_with_image_snapshot(
            entry_file="main.py",
            source_dir=SCRIPT_DIR_PATH,
            inputs=[PipelineParameter("foo")],
            outputs=[],
            image_uri="reg.docker.alibaba-inc.com/lq_test/test_image",
        )

        op.to_dict()
        op.run(
            "test_image_snapshot",
            arguments={
                "foo": "ArgumentsFoo",
            },
        )

    def test_literal_snapshot(self):
        script_file = os.path.join(SHELL_SCRIPT_DIR_PATH, "job.sh")
        op = ScriptOperator.create_with_literal_snapshot(
            script_file=script_file, inputs=[PipelineParameter("foo")]
        )

        op.run(
            "test_literal_snapshot",
            arguments={
                "foo": "FooFromLiteralSnapshot",
            },
            local_mode=True,
        )

        def create_pipeline():
            x = PipelineParameter("x")
            step1 = op.as_step(
                name="step1",
                inputs={
                    "foo": x,
                },
            )

            step2 = op.as_step(
                name="step2",
                inputs={
                    "foo": "HardCodeParam",
                },
            )

            step2.after(step1)

            return Pipeline(steps=[step2])

        p = create_pipeline()

        p.run("literal_pipeline_job", arguments={"x": "ParameterX"})
