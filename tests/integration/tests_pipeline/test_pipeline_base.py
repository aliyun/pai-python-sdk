from __future__ import absolute_import

import os

from pai.common import ProviderAlibabaPAI
from pai.pipeline.template import PipelineTemplate
from tests.integration import BaseIntegTestCase

_current_dir = os.path.dirname(os.path.abspath(__file__))


class TestPipelineBase(BaseIntegTestCase):
    @classmethod
    def init_prediction_pipeline(
        cls,
        identifier="prediction-xflow-maxCompute",
        version="v1",
        provider=ProviderAlibabaPAI,
    ):
        p = PipelineTemplate.get_by_identifier(
            identifier=identifier, provider=provider, version=version
        )
        return p

    def test_args_translate(self):
        p = self.init_prediction_pipeline()

        table_name = self.TestDataSetTables["iris_data"]
        arguments = {
            "execution": {
                "k1": "value",
                "k2": "value",
            },
            "outputTableName": "pai_output_test_table",
            "inputDataSetArtifact": self.odps_client.get_table(table_name),
            "inputModelArtifact": "odps://%s/offlinemodels/test_iris_model"
            % self.odps_client.project,
        }

        parameters, artifacts = p.translate_arguments(arguments)

        expected_parameters = [
            {
                "name": "execution",
                "value": {
                    "k1": "value",
                    "k2": "value",
                },
            },
            {
                "name": "outputTableName",
                "value": "pai_output_test_table",
            },
        ]

        def sort_item_by_name(args):
            return sorted(args, key=lambda x: x["name"])

        self.assertEqual(
            sort_item_by_name(expected_parameters), sort_item_by_name(parameters)
        )

        expected_artifacts = [
            {
                "name": "inputDataSetArtifact",
                "value": '{"location": {"project": "%s", "table": "%s"}}'
                % (self.odps_client.project, table_name),
            },
            {
                "name": "inputModelArtifact",
                "value": '{"location": {"name": "test_iris_model", "project":'
                ' "%s"}, "name": "test_iris_model"}' % self.odps_client.project,
            },
        ]

        self.assertEqual(
            sort_item_by_name(expected_artifacts), sort_item_by_name(artifacts)
        )
