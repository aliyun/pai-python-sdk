from __future__ import absolute_import

import os
import time
import unittest
from pprint import pprint

from pai.pipeline import Pipeline, PipelineStep
from pai.pipeline.parameter import ParameterType
from pai.common import ProviderAlibabaPAI
from pai.pipeline.artifact import ArtifactDataType, ArtifactLocationType
from pai.pipeline.run import RunInstance, RunStatus
from pai.xflow.classifier import LogisticRegression
from test import BaseTestCase
from test.pipeline import load_local_yaml

_current_dir = os.path.dirname(os.path.abspath(__file__))


class TestPipelineBase(BaseTestCase):

    def init_prediction_pipeline(self, identifier="prediction-xflow-maxCompute",
                                 version="v1", provider=ProviderAlibabaPAI):
        p = Pipeline.get_by_identifier(identifier=identifier,
                                       provider=ProviderAlibabaPAI,
                                       version=version,
                                       session=self.session)
        return p

    def test_pipeline_init(self):
        identifier ="prediction-xflow-maxCompute"
        provider = ProviderAlibabaPAI
        version = "v1"
        p = self.init_prediction_pipeline(identifier, version, provider)
        self.assertEqual(p.identifier, identifier)
        self.assertEqual(p.version, version)
        self.assertEqual(p.provider, provider)

        expected_param_specs = {'__XFlow_execution': {'name': '__XFlow_execution',
                                                      'required': True,
                                                      'type': 'Map'},
                                '__XFlow_project': {'name': '__XFlow_project',
                                                    'required': True,
                                                    'type': 'String',
                                                    'value': 'algo_public'},
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
            "__XFlow_execution":  {
                "k1": "value",
                "k2": "value",
            },
            "__XFlow_project": "algo_Public",
            "outputTableName": "pai_output_test_table",
        }

        parameters, artifacts = p.translate_arguments(arguments)
