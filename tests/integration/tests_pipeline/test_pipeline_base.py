#  Copyright 2023 Alibaba, Inc. or its affiliates.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from __future__ import absolute_import

import os

from pai.common import ProviderAlibabaPAI
from pai.pipeline.component import RegisteredComponent
from tests.integration import BaseIntegTestCase

_current_dir = os.path.dirname(os.path.abspath(__file__))


class TestPipelineWithSavedOp(BaseIntegTestCase):
    @classmethod
    def init_prediction_pipeline(
        cls,
        identifier="Prediction_1",
        version="v1",
        provider=ProviderAlibabaPAI,
    ):
        p = RegisteredComponent.get_by_identifier(
            identifier=identifier, provider=provider, version=version
        )
        return p

    def test_args_translate(self):
        p = self.init_prediction_pipeline()

        arguments = {
            "execution": {
                "k1": "value",
                "k2": "value",
            },
            "outputTableName": "pai_output_test_table",
            "inputTable": self.breast_cancer_dataset.to_url(),
            "model": "odps://%s/offlinemodels/test_iris_model"
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

        self.assertListEqual(
            sorted(expected_parameters, key=lambda x: x["name"]),
            sorted(parameters, key=lambda x: x["name"]),
        )

        expected_artifacts = [
            {
                "name": "inputTable",
                "metadata": {"type": {"DataSet": {"locationType": "MaxComputeTable"}}},
                "value": '{"location": {"project": "%s", "table": "%s"}}'
                % (
                    self.breast_cancer_dataset.default_dataset_project,
                    self.breast_cancer_dataset.table_name,
                ),
            },
            {
                "name": "model",
                "metadata": {
                    "type": {
                        "Model": {
                            "locationType": "MaxComputeOfflineModel",
                            "modelType": "OfflineModel",
                        }
                    }
                },
                "value": '{"location": {"name": "test_iris_model", "project":'
                ' "%s"}, "name": "test_iris_model"}' % self.odps_client.project,
            },
        ]

        self.assertEqual(
            sorted(expected_artifacts, key=lambda x: x["name"]),
            sorted(artifacts, key=lambda x: x["name"]),
        )
