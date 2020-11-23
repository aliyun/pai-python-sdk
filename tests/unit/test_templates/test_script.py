import os
from pprint import pprint

from pai.pipeline.templates.script import (
    ScriptTemplate,
    PAI_PROGRAM_ENTRY_POINT_ENV_KEY,
    PAI_SOURCE_CODE_ENV_KEY,
    PAI_SCRIPT_TEMPLATE_DEFAULT_COMMAND,
)
from tests.unit import BaseUnitTestCase, test_root
from tests.test_data import SCRIPT_DIR_PATH


class TestPythonScriptTemplate(BaseUnitTestCase):
    def test_script(self):
        entry_point = "main.py"
        script_templ = ScriptTemplate(
            source_dir=SCRIPT_DIR_PATH,
            entry_point="main.py",
            inputs=[],
            env={
                "hello": "world",
            },
        )
        script_templ.prepare()
        manifest = script_templ.to_dict()
        manifest_env = manifest["spec"]["execution"]["env"]

        self.assertTrue(manifest_env.get(PAI_SOURCE_CODE_ENV_KEY).startswith("oss://"))
        self.assertEqual(
            manifest_env.get(PAI_PROGRAM_ENTRY_POINT_ENV_KEY, ""), entry_point
        )
        self.assertEqual(manifest_env.get("hello", ""), "world")

        self.assertEqual(
            manifest["spec"]["execution"]["command"],
            [PAI_SCRIPT_TEMPLATE_DEFAULT_COMMAND],
        )
