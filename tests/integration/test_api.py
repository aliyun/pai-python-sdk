from __future__ import absolute_import

from pprint import pprint

import os
import unittest

import yaml

from pai.common import ProviderAlibabaPAI
from pai.pipeline import PipelineRun
from pai.operator import SavedOperator
from pai.core.session import get_default_session
from pai.common.utils import iter_with_limit
from tests.integration import BaseIntegTestCase, _test_root


class TestPaiFlowAPI(BaseIntegTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestPaiFlowAPI, cls).setUpClass()

        from pai.api.client_factory import ClientFactory

        cls.client = ClientFactory.create_paiflow_client(
            access_key_id=cls.pai_service_config.access_key_id,
            access_key_secret=cls.pai_service_config.access_key_secret,
            region_id=cls.pai_service_config.region_id,
        )

    @classmethod
    def tearDownClass(cls):
        super(TestPaiFlowAPI, cls).tearDownClass()
        if hasattr(cls, "paiflowclient"):
            del cls.paiflowclient

    def test_get_pipeline_schema(self):
        identifier = "evaluate_1"
        pipeline_info = self.session.get_pipeline(
            identifier=identifier, provider=ProviderAlibabaPAI, version="v1"
        )
        self.assertIsNotNone(pipeline_info["PipelineId"])
        manifest = yaml.load(pipeline_info["Manifest"], yaml.FullLoader)
        self.assertEqual(identifier, manifest["metadata"]["identifier"])

    def test_list_pipeline(self):
        pipelines, count = self.client.list_pipeline(
            identifier="evaluate_1", provider=ProviderAlibabaPAI, version="v1"
        )
        self.assertEqual(count, 1)
        self.assertEqual(len(pipelines), 1)
        self.assertEqual(pipelines[0]["Identifier"], "evaluate_1")
        self.assertEqual(pipelines[0]["Provider"], ProviderAlibabaPAI)

    def test_list_pipeline_generator(self):
        for pipeline in self.client.list_pipeline_generator(provider=ProviderAlibabaPAI):
            print(pipeline)

    def test_list_pipelines(self):
        count = 0
        for pl in self.session.list_pipeline(provider=ProviderAlibabaPAI):
            count += 1

        self.assertTrue(count > 0)

    def test_list_run_generator(self):
        run_info = next(self.client.list_run_generator(status="Succeeded"))
        run = self.client.get_run(run_info["RunId"])
        pprint(run)
        rs = self.client.get_node(run_id=run_info["RunId"], node_id=run["NodeId"])
        pprint(rs)




        # for info in self.client.list_run_generator(status="Succeeded"):
        #     run = self.client.get_run(info["RunId"])
        #     self.client.list_run_node()
        #     print(run)

    def test_get_node(self):
        pass

    def test_list_template(self):
        templates = list(
            iter_with_limit(SavedOperator.list(provider=ProviderAlibabaPAI), 10)
        )

        for template in templates:
            print(template)
            print(template.inputs)
            print(template.outputs)

    def test_list_run(self):
        runs = list(iter_with_limit(PipelineRun.list(), 10))
        self.assertTrue(len(runs) <= 10)

    def test_load_pipeline(self):
        # sess = get_default_session()
        #
        # identitifers = ["sql", "split"]
        #
        # manifest_dir = os.path.join(_test_root, "..", "test_data", "manifests")
        #
        # for id in identitifers:
        #     op = SavedOperator.get_by_identifier(identifier=id, provider=ProviderAlibabaPAI, version="v1")
        #     manifest = sess.describe_pipeline(op.pipeline_id)["Manifest"]
        #     file = os.path.join(manifest_dir, id + ".yaml")
        #     with open(file, "w") as f:
        #         f.write(manifest)
        pass


if __name__ == "__main__":
    unittest.main()
