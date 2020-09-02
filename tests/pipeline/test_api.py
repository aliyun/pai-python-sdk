from __future__ import absolute_import

import os
import unittest

import yaml

from pai.common import ProviderAlibabaPAI
from pai.pipeline.template import PipelineTemplate
from pai.session import Session
from tests import BaseTestCase

_test_root = os.path.dirname(os.path.abspath(__file__))


class TestPaiFlowAPI(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestPaiFlowAPI, cls).setUpClass()
        session = Session.get_current_session()
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
        pipeline_infos, total_count = self.session.list_pipeline(
            provider=ProviderAlibabaPAI, page_size=50, page_num=1)

        self.assertTrue(len(pipeline_infos) > 0)
        self.assertTrue(total_count > 0)

    def test_provider(self):
        assert self.session.provider is not None

    def test_pipeline_create(self):
        pass

    def test_pipeline_update_privilege(self):
        pass

    def test_run_wait(self):
        pass

    def test_list_run(self):
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
        pipelines, count = self.session.list_pipeline(provider=ProviderAlibabaPAI)
        self.assertTrue(len(pipelines) > 0)
        self.assertTrue(count > 0)


if __name__ == "__main__":
    unittest.main()
