from __future__ import absolute_import


import os
import unittest

import yaml

from pai.common import ProviderAlibabaPAI
from pai.pipeline import PipelineRun, PipelineTemplate
from pai.core.session import get_default_session
from pai.common.utils import iter_with_limit
from tests.integration import BaseIntegTestCase

_test_root = os.path.dirname(os.path.abspath(__file__))


class TestPaiFlowAPI(BaseIntegTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestPaiFlowAPI, cls).setUpClass()
        session = get_default_session()
        cls.session = session

    @classmethod
    def tearDownClass(cls):
        super(TestPaiFlowAPI, cls).tearDownClass()
        if cls.session:
            del cls.session

    def test_get_pipeline(self):
        identifier = "evaluate-xflow-maxCompute"
        pipeline_info = self.session.get_pipeline(identifier=identifier,
                                                  provider=ProviderAlibabaPAI,
                                                  version="v1")
        self.assertIsNotNone(pipeline_info["PipelineId"])
        manifest = yaml.load(pipeline_info["Manifest"], yaml.FullLoader)
        self.assertEqual(identifier, manifest["metadata"]["identifier"])

    def test_list_pipeline(self):
        pipeline_infos = list(iter_with_limit(self.session.list_pipeline(
            provider=ProviderAlibabaPAI), 10))
        self.assertTrue(len(pipeline_infos) == 10)

    def test_provider(self):
        assert self.session.provider is not None

    def test_pipeline_create(self):
        pass

    def test_pipeline_update_privilege(self):
        pass

    def test_run_wait(self):
        pass

    def test_get_run_detail(self):
        pass

    def test_get_log(self):
        pass

    def test_manifest_run(self):
        pass

    def test_composite_pipeline_run(self):
        pass

    def test_run_status_manager(self):
        pass

    def test_run_outputs(self):
        pass

    def test_list_pipelines(self):
        count = 0
        for pl in self.session.list_pipeline(provider=ProviderAlibabaPAI):
            count += 1

        self.assertTrue(count > 0)

    def test_list_template(self):
        templates = list(iter_with_limit(PipelineTemplate.list(provider=ProviderAlibabaPAI), 10))
        self.assertTrue(len(templates) <= 10)

    def test_list_run(self):
        runs = list(iter_with_limit(PipelineRun.list(), 10))
        self.assertTrue(len(runs) <= 10)


if __name__ == "__main__":
    unittest.main()
