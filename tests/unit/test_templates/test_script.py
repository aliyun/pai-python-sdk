import os
from pprint import pprint

import re
from pai.pipeline import PipelineParameter
from pai.pipeline.template import (
    ScriptTemplate,
    PAI_PROGRAM_ENTRY_POINT_ENV_KEY,
    PAI_SOURCE_CODE_ENV_KEY,
    PAI_SCRIPT_TEMPLATE_DEFAULT_COMMAND,
)
from pai.pipeline.types import (
    PipelineArtifact,
    ArtifactMetadata,
    ArtifactDataType,
    ArtifactLocationType,
)

from pai.pipeline.types.artifact import MaxComputeTableArtifact
from tests.unit import BaseUnitTestCase
from tests.test_data import SCRIPT_DIR_PATH


class TestScriptTemplate(BaseUnitTestCase):
    def test_script(self):
        entry_point = "main.py"
        script_templ = ScriptTemplate(
            source_dir=SCRIPT_DIR_PATH,
            entry_file="main.py",
            inputs=[],
            env={
                "hello": "world",
            },
        )
        script_templ.prepare()
        manifest = script_templ.to_dict()
        manifest_env = manifest["spec"]["container"]["envs"]

        self.assertTrue(manifest_env.get(PAI_SOURCE_CODE_ENV_KEY).startswith("oss://"))
        self.assertEqual(
            manifest_env.get(PAI_PROGRAM_ENTRY_POINT_ENV_KEY, ""), entry_point
        )
        self.assertEqual(manifest_env.get("hello", ""), "world")

        self.assertEqual(
            manifest["spec"]["container"]["command"],
            [PAI_SCRIPT_TEMPLATE_DEFAULT_COMMAND],
        )

    def test_check_script_source_files(self):
        cases = [
            {
                "name": "oss_source_case1",
                "input": {
                    "entry_file": "oss://test_bucket/main.py",
                    "source_dir": "oss://test_bucket/hello/world",
                },
                "expectedErrorMsg": "OSS",
            },
            {
                "name": "oss_source_case2",
                "input": {
                    "entry_file": "oss://test_bucket/main.py",
                    "source_dir": "/test_bucket/hello/world",
                },
                "expectedErrorMsg": "OSS",
            },
            {
                "name": "entry_file_is_dir",
                "input": {
                    "entry_file": "oss://test_bucket/source_path/dir/",
                    "source_dir": "/test_bucket/hello/world",
                },
                "expectedErrorMsg": r"directory path",
            },
            {
                "name": "source",
                "input": {
                    "entry_file": "test_bucket/source_path/dir/main.py",
                    "source_dir": "/test_bucket/hello/world",
                },
                "expectedErrorMsg": "top-level directory",
            },
        ]

        for case in cases:
            with self.assertRaisesRegexp(ValueError, case["expectedErrorMsg"]):
                ScriptTemplate.check_source_file(
                    entry_file=case["input"]["entry_file"],
                    source_dir=case["input"]["source_dir"],
                )

    def test_table_ref(self):
        templ = ScriptTemplate(
            source_dir="./scripts",
            entry_file="main.py",
            inputs=[
                PipelineParameter(
                    "tableName",
                ),
                PipelineParameter("partition", default=""),
            ],
            outputs=[
                PipelineArtifact(
                    "outputTable",
                    ArtifactMetadata(
                        data_type=ArtifactDataType.DataSet,
                        location_type=ArtifactLocationType.MaxComputeTable,
                    ),
                    value=MaxComputeTableArtifact.value_from_param(
                        "tableName", "partition"
                    ),
                )
            ],
        )
        pprint(templ.to_dict())
