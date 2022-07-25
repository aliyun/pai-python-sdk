from __future__ import absolute_import

import os

from unittest import skipIf

from pai.common import ProviderAlibabaPAI
from pai.operator import SavedOperator
from tests.integration import BaseIntegTestCase, EnvType
from tests.integration.utils import t_context

_current_dir = os.path.dirname(os.path.abspath(__file__))


@skipIf(
    t_context.env_type == EnvType.Light,
    "Light Environment do not hold PAI provide SavedOperator.",
)
class TestPipelineWithSavedOp(BaseIntegTestCase):
    @classmethod
    def init_prediction_pipeline(
        cls,
        identifier="Prediction_1",
        version="v1",
        provider=ProviderAlibabaPAI,
    ):
        p = SavedOperator.get_by_identifier(
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

    def test_alink_op(self):
        op = SavedOperator.get_by_identifier(
            identifier="alink_pyalink", provider=ProviderAlibabaPAI, version="v1"
        )

        compute_resource = {
            "endpoint": "http://service.cn-hangzhou.maxcompute.aliyun.com/api",
            "odpsProject": "abk_test_1",
        }

        mc_compute = compute_resource.copy()
        pyalink_script = """
        import itertools
        from pyalink.alink import *

        def main(sources, sinks, parameter):
            raw_data = sources[0]
            # split the raw dataset
            spliter = SplitBatchOp().setFraction(0.8).linkFrom(raw_data)
            train_data = spliter
            valid_data = spliter.getSideOutput(0)

            train_data.link(sinks[0])
            valid_data.link(sinks[1])
            BatchOperator.execute()
        """

        op.run(
            job_name="pyalink-demo",
            arguments={
                "execution": compute_resource,
                "execution_maxcompute": mc_compute,
                "input-0": "odps://pai_online_project/tables/heart_disease_prediction",
                "computeTarget": "MaxCompute",
                "literalPythonScript": pyalink_script,
            },
        )
