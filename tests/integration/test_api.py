from __future__ import absolute_import

import unittest
from pprint import pprint

import yaml

from pai.common import ProviderAlibabaPAI
from tests.integration import BaseIntegTestCase


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

    def test_list_pipeline(self):
        pipelines, count = self.client.list_pipeline(
            identifier="evaluate_1", provider=ProviderAlibabaPAI, version="v1"
        )
        self.assertEqual(count, 1)
        self.assertEqual(len(pipelines), 1)
        self.assertEqual(pipelines[0]["Identifier"], "evaluate_1")
        self.assertEqual(pipelines[0]["Provider"], ProviderAlibabaPAI)

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
        run_info = next(self.client.list_run_generator(status="Succeeded"))
        print(run_info)
        run_id = run_info["RunId"]

        run_info = self.client.get_run(run_id=run_id)
        print(run_info)

        self.assertIsNotNone(run_id)
        rs = self.client.get_node(run_id=run_id, node_id=run_info["NodeId"])
        pprint(rs)
        self.assertIsNotNone(rs)

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
