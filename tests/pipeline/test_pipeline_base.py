from __future__ import absolute_import

import os

from pai.common import ProviderAlibabaPAI
from pai.pipeline.template import PipelineTemplate
from tests import BaseTestCase

_current_dir = os.path.dirname(os.path.abspath(__file__))


class TestPipelineBase(BaseTestCase):

    @classmethod
    def init_prediction_pipeline(cls, identifier="prediction-xflow-maxCompute",
                                 version="v1", provider=ProviderAlibabaPAI):
        p = PipelineTemplate.get_by_identifier(identifier=identifier,
                                               provider=provider,
                                               version=version)
        return p

    def test_args_translate(self):
        p = self.init_prediction_pipeline()

        arguments = {
            "execution": {
                "k1": "value",
                "k2": "value",
            },
            "outputTableName": "pai_output_test_table",
            "inputDataSetArtifact": "odps://pai_online_project/tables/iris_data",
            "inputModelArtifact": "odps://pai_online_project/offlinemodels/test_iris_model",
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
            }
        ]

        def sort_arg_by_name(args):
            return sorted(args, key=lambda x: x["name"])

        self.assertEqual(sort_arg_by_name(expected_parameters), sort_arg_by_name(parameters))

        expected_artifacts = [
            {
                'name': 'inputDataSetArtifact',
                'value': '{"location": {"project": "pai_online_project", "table": "iris_data"}}'
            },
            {
                'name': 'inputModelArtifact',
                'value': '{"location": {"name": "test_iris_model", "project": "pai_online_project"}, "name": "test_iris_model"}',
            }
        ]

        self.assertEqual(expected_artifacts, artifacts)
