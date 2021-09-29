import contextlib
import os
from unittest import skipUnless, skipIf

from pai.common.utils import gen_temp_table
from pai.core.session import EnvType
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
from tests.integration.utils import t_context
from tests.test_data import (
    SCRIPT_DIR_PATH,
    MAXC_SQL_TEMPLATE_SCRIPT_PATH,
    SHELL_SCRIPT_DIR_PATH,
    RAW_ARTIFACT_RW_DIR_PATH,
)


@contextlib.contextmanager
def cwd_context(target_dir):
    previous_dir = os.getcwd()
    os.chdir(target_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)


@skipUnless(
    t_context.env_type == EnvType.PublicCloud and not t_context.is_inner,
    "Group inner do not support code snapshot with OSS.",
)
class TestScriptOperatorOssSnapshot(BaseIntegTestCase):
    def test_local_source_files(self):
        templ = ScriptOperator.create_with_oss_snapshot(
            entry_file="main.py",
            source_dir=SCRIPT_DIR_PATH,
            inputs=[
                PipelineParameter(name="foo", typ=str, default="Hello"),
                PipelineParameter(name="bar", typ=int, default=200),
            ],
            image_uri=self.get_python_image(),
        )
        manifest = templ.to_dict()
        env_vars = manifest["spec"]["container"]["envs"]
        self.assertTrue(PAI_SOURCE_CODE_ENV_KEY in env_vars)
        self.assertEqual(env_vars[PAI_PROGRAM_ENTRY_POINT_ENV_KEY], "main.py")
        templ.run(
            job_name="HelloWorld",
            arguments={
                "foo": "Hello",
                "bar": "World",
            },
        )

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

    # @skipIf(not t_context.has_docker, "Do not found docker cli tool.")
    # def test_local_run(self):
    #     templ = ScriptOperator.create_with_oss_snapshot(
    #         entry_file="main.py",
    #         source_dir=MAXC_SQL_TEMPLATE_SCRIPT_PATH,
    #         inputs=[
    #             PipelineParameter("sql"),
    #             PipelineParameter("execution", typ=dict),
    #             PipelineParameter("outputTable"),
    #             PipelineParameter("lifeCycle", typ=int, default=7),
    #             PipelineArtifact(
    #                 "t1",
    #                 metadata=MetadataBuilder.maxc_table(),
    #             ),
    #             PipelineArtifact(
    #                 "t2",
    #                 metadata=MetadataBuilder.maxc_table(),
    #             ),
    #             PipelineArtifact(
    #                 "t3",
    #                 metadata=MetadataBuilder.maxc_table(),
    #             ),
    #             PipelineArtifact(
    #                 "t4",
    #                 metadata=MetadataBuilder.maxc_table(),
    #             ),
    #         ],
    #         outputs=[
    #             PipelineArtifact(
    #                 "outputTable",
    #                 metadata=MetadataBuilder.maxc_table(),
    #                 value=MaxComputeTableArtifact.value_from_param("outputTable"),
    #             )
    #         ],
    #     )
    #
    #     maxc_config = t_context.maxc_config
    #     local_run_container = templ.run(
    #         job_name="helloWorld",
    #         local_mode=True,
    #         arguments={
    #             "sql": """
    #             -- SQL Example
    #             select * from ${t2};
    #             """,
    #             "t2": "odps://pai_online_project/tables/breast_cancer_data",
    #             "outputTable": gen_temp_table(),
    #             "execution": {
    #                 "endpoint": maxc_config.endpoint,
    #                 "odpsProject": maxc_config.project,
    #                 "accessKeyId": maxc_config.access_key_id,
    #                 "accessKeySecret": maxc_config.access_key_secret,
    #             },
    #         },
    #     )
    #     self.assertEqual(local_run_container.attrs["State"]["ExitCode"], 0)


@skipUnless(
    t_context.has_docker and t_context.has_docker, "Do not found docker cli tool"
)
class TestScriptOperatorImageSnapshot(BaseIntegTestCase):
    def test_image_snapshot(self):
        op = ScriptOperator.create_with_image_snapshot(
            entry_file="main.py",
            source_dir=SCRIPT_DIR_PATH,
            inputs=[PipelineParameter("foo")],
            outputs=[],
            base_image=self.get_python_image(),
            image_uri="master0:5000/paiflow/example",
        )

        op.to_dict()
        op.run(
            "test_image_snapshot",
            arguments={
                "foo": "ArgumentsFoo",
            },
        )

    def test_pip_install(self):
        pass
        # op = ScriptOperator.create_with_image_snapshot(
        # )


class TestScriptOperatorSourceSnapshot(BaseIntegTestCase):
    def test_literal_snapshot(self):
        script_file = os.path.join(SHELL_SCRIPT_DIR_PATH, "job.sh")
        op = ScriptOperator.create_with_source_snapshot(
            script_file=script_file,
            inputs=[PipelineParameter("foo")],
            image_uri=self.get_python_image(),
        )

        op.run(
            "test_literal_snapshot",
            arguments={
                "foo": "FooFromLiteralSnapshot",
            },
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

    def test_read_raw_artifact(self):
        script_file = os.path.join(RAW_ARTIFACT_RW_DIR_PATH, "main.py")
        op = ScriptOperator.create_with_source_snapshot(
            script_file=script_file,
            inputs=[
                PipelineArtifact(
                    name="input1",
                    metadata=MetadataBuilder.raw(),
                ),
            ],
            outputs=[
                PipelineArtifact(
                    name="output1",
                    metadata=MetadataBuilder.raw(),
                )
            ],
            image_uri=self.get_python_image(),
        )

        run = op.run("rawArtifactAppend", arguments={"input1": "helloWorld"})
        self.assertEqual(run.get_outputs()[0].value, "helloWorld:End")

    def test_list_logs(self):
        pass

        # def create_pipeline():
        #     step1 = op.as_step(name="step1", inputs={"input1": "helloWorld"})
        #
        #     step2 = op.as_step(
        #         name="step2",
        #         inputs={
        #             "input1": step1.outputs["output1"],
        #         },
        #     )
        #
        #     return Pipeline(steps=[step1, step2], outputs=step2.outputs[:])
        #
        # p = create_pipeline()
        # pipeline_run = p.run("rawArtifactPassing")
        #
        # self.assertEqual(pipeline_run.get_outputs()[0].value, "helloWorld:End:End")

    def test_rw_raw_artifact(self):
        script_file = os.path.join(RAW_ARTIFACT_RW_DIR_PATH, "pai_running_example.py")

        op = ScriptOperator.create_with_source_snapshot(
            script_file=script_file,
            inputs=[
                PipelineArtifact(
                    name="input1",
                    metadata=MetadataBuilder.raw(),
                ),
            ],
            outputs=[
                PipelineArtifact(
                    name="output1",
                    metadata=MetadataBuilder.raw(),
                )
            ],
            install_packages=[
                "https://pai-sdk.oss-cn-shanghai.aliyuncs.com/pai_running_utils/dist/pai_running_utils-0.2.5.post2-py2.py3-none-any.whl"
            ],
            image_uri=self.get_python_image(),
        )

        op.run("rawArtifactExample", arguments={"input1": "helloWorld"})
