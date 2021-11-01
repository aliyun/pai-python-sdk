from __future__ import absolute_import

import unittest

import yaml

from pai.common import ProviderAlibabaPAI
from pai.core.session import Session, EnvType
from tests.integration import BaseIntegTestCase
from tests.integration.utils import t_context


class TestPaiFlowAPI(BaseIntegTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestPaiFlowAPI, cls).setUpClass()
        session = Session.current()
        cls.client = session.paiflow_client

    @classmethod
    def tearDownClass(cls):
        super(TestPaiFlowAPI, cls).tearDownClass()
        if hasattr(cls, "paiflowclient"):
            del cls.paiflowclient

    @unittest.skipIf(
        t_context.env_type == EnvType.Light,
        "Light Env do not contain operator provide by PAI",
    )
    def test_get_pipeline_schema(self):
        identifier = "evaluate_1"
        pipeline_info = next(
            self.client.list_pipeline_generator(
                identifier=identifier, provider=ProviderAlibabaPAI, version="v1"
            ),
            None,
        )
        self.assertIsNotNone(pipeline_info["PipelineId"])
        rs = self.client.get_pipeline_schema(pipeline_info["PipelineId"])
        manifest = yaml.load(rs["Manifest"], yaml.FullLoader)
        self.assertEqual(identifier, manifest["metadata"]["identifier"])
        self.assertEqual(ProviderAlibabaPAI, manifest["metadata"]["provider"])
        self.assertEqual("v1", manifest["metadata"]["version"])

    @unittest.skipIf(
        t_context.env_type == EnvType.Light,
        "Light Env do not contain operator provide by PAI",
    )
    def test_list_pipeline(self):
        pipelines, count = self.client.list_pipeline(
            identifier="evaluate_1", provider=ProviderAlibabaPAI, version="v1"
        )
        self.assertEqual(count, 1)
        self.assertEqual(len(pipelines), 1)
        self.assertEqual(pipelines[0]["Identifier"], "evaluate_1")
        self.assertEqual(pipelines[0]["Provider"], ProviderAlibabaPAI)

    @unittest.skipIf(
        t_context.env_type == EnvType.Light,
        "Light Env do not contain operator provide by PAI",
    )
    def test_list_pipeline_generator(self):
        pipeline = next(
            (
                pipeline
                for pipeline in self.client.list_pipeline_generator(
                    provider=ProviderAlibabaPAI
                )
            ),
            None,
        )
        self.assertIsNotNone(pipeline)

    def test_list_run_generator(self):
        run_info = next(self.client.list_run_generator(status="Succeeded"), None)
        if run_info is not None:
            self.assertIsNotNone(run_info["RunId"])


if __name__ == "__main__":
    unittest.main()
