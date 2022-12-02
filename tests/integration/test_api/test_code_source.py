from pai.code_source import CodeSource
from tests.integration import BaseIntegTestCase
from tests.integration.utils import make_resource_name


class TestCodeSource(BaseIntegTestCase):
    def test_code_source(self):
        display_name = make_resource_name("CodeSource", "Create")
        code_source = CodeSource(
            code_repo="https://code.aliyun.com/pai-test-1/dlc-example.git",
            display_name=display_name,
            mount_path="/ml/code/",
        )

        self.assertIsNone(code_source.id)
        self.assertIsNone(code_source.create_time)
        self.assertIsNone(code_source.modified_time)
        code_source.register()
        self.assertIsNotNone(code_source.id)
        self.assertIsNotNone(code_source.create_time)
        self.assertIsNotNone(code_source.modified_time)
        self.assertTrue(len(code_source.list()) > 0)
        # self.assertIsNone(code_source.delete())
