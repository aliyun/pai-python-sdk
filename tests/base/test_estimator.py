from __future__ import absolute_import

import time

from pai.common import ProviderAlibabaPAI
from pai.pipeline.template import PipelineTemplate
from tests import BaseTestCase


class TestEstimatorBase(BaseTestCase):

    def init_base_lr_estimator(self):
        identifier = "logisticregression-binary-xflow-maxCompute"
        version = "v1"
        provider = ProviderAlibabaPAI
        p = PipelineTemplate.get_by_identifier(identifier=identifier,
                                               provider=provider, version=version)
        parameters = {
            "project": "algo_public",
            "epsilon": 1e-06,
            "maxIter": 100,
            # "regularizedType": "l1",
            "regularizedLevel": 1.0,
        }
        est = p.to_estimator(parameters=parameters)
        return p, est

    def test_init_base_lr_estimator(self):
        p, est = self.init_base_lr_estimator()
        self.assertEqual(est.identifier, p.identifier)
        self.assertEqual(est.provider, p.provider)
        self.assertEqual(est.pipeline_id, p.pipeline_id)

    def test_estimator_from_pipeline(self):
        p, est = self.init_base_lr_estimator()
        model_name = "ut_estimator_from_pipeline"
        project = self.odps_client.project
        run_args = {
            "inputArtifact": "odps://{project_name}/tables/{table_name}".format(
                project_name=project, table_name="lr_data_set"),
            "labelColName": "_c2",
            "featureColNames": "pm10,so2,co,no2",
            "modelName": model_name,
            "goodValue": 1,
            "project": self.default_xflow_project,
            "execution": self.get_default_xflow_execution(),
        }

        _ = est.fit(wait=False, job_name="pysdk-test-estimator-pipeline", arguments=run_args)
        # assert odps offlineModel exists
        self.assertTrue(
            self.odps_client.exist_offline_model(name=model_name, project=project))

    def test_new_composite_pipeline_to_estimator(self):
        pass
