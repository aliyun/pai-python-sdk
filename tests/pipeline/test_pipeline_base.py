from __future__ import absolute_import

import os

from pai.common import ProviderAlibabaPAI
from pai.pipeline import Pipeline
from tests import BaseTestCase

_current_dir = os.path.dirname(os.path.abspath(__file__))


class TestPipelineBase(BaseTestCase):

    def init_prediction_pipeline(self, identifier="prediction-xflow-maxCompute",
                                 version="v1", provider=ProviderAlibabaPAI):
        p = Pipeline.get_by_identifier(identifier=identifier,
                                       provider=provider,
                                       version=version,
                                       session=self.session)
        return p

    def test_pipeline_init(self):
        identifier = "prediction-xflow-maxCompute"
        provider = ProviderAlibabaPAI
        version = "v1"
        p = self.init_prediction_pipeline(identifier, version, provider)
        self.assertEqual(p.identifier, identifier)
        self.assertEqual(p.version, version)
        self.assertEqual(p.provider, provider)

        expected_param_specs = {'execution': {'name': 'execution',
                                              'required': True,
                                              'type': 'Map'},
                                'appendColNames': {'name': 'appendColNames', 'type': 'String',
                                                   'value': ''},
                                'coreNum': {'feasible': {'range': '[1, INF['},
                                            'name': 'coreNum',
                                            'type': 'Int',
                                            'value': ''},
                                'detailColName': {'name': 'detailColName', 'type': 'String',
                                                  'value': ''},
                                'enableSparse': {'name': 'enableSparse', 'type': 'Bool',
                                                 'value': False},
                                'featureColNames': {'name': 'featureColNames', 'type': 'String',
                                                    'value': ''},
                                'itemDelimiter': {'name': 'itemDelimiter', 'type': 'String',
                                                  'value': ' '},
                                'kvDelimiter': {'name': 'kvDelimiter', 'type': 'String',
                                                'value': ':'},
                                'lifecycle': {'feasible': {'range': '[1, INF['},
                                              'name': 'lifecycle',
                                              'type': 'Int',
                                              'value': ''},
                                'memSizePerCore': {'feasible': {'range': '[1, INF['},
                                                   'name': 'memSizePerCore',
                                                   'type': 'Int',
                                                   'value': ''},
                                'outputTableName': {'name': 'outputTableName',
                                                    'required': True,
                                                    'type': 'String'},
                                'outputTablePartition': {'name': 'outputTablePartition',
                                                         'type': 'String',
                                                         'value': ''},
                                'resultColName': {'name': 'resultColName', 'type': 'String',
                                                  'value': ''},
                                'scoreColName': {'name': 'scoreColName', 'type': 'String',
                                                 'value': ''}}

        expected_af_specs = {
            'inputDataSetArtifact': {
                'metadata': {'type': {'DataSet': {'locationType': 'MaxComputeTable'}}},
                'name': 'inputDataSetArtifact',
                'required': True},
            'inputModelArtifact': {'metadata': {
                'type': {'Model': {'locationType': 'MaxComputeOfflineModel',
                                   'modelType': 'OfflineModel'}}},
                'name': 'inputModelArtifact',
                'required': True}
        }

        self.assertEqual(p.input_parameters_spec, expected_param_specs)
        self.assertEqual(p.input_artifacts_spec, expected_af_specs)

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
