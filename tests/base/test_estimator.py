from __future__ import absolute_import

import unittest

from pai import ProviderAlibabaPAI
from pai.pipeline import Pipeline
from tests import BaseTestCase


class TestEstimatorBase(BaseTestCase):

    def init_base_lr_estimator(self):
        identifier = "logisticregression-binary-xflow-maxCompute"
        version = "v1"
        provider = ProviderAlibabaPAI
        p = Pipeline.get_by_identifier(session=self.session, identifier=identifier,
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
        self.assertEqual(est.get_identifier(), p.identifier)
        self.assertEqual(est.get_version(), p.version)
        self.assertEqual(est.get_provider(), p.provider)
        self.assertEqual(est.get_pipeline_id(), p.pipeline_id)

    def test_estimator_from_pipeline(self):
        p, est = self.init_base_lr_estimator()
        model_name = "ut_estimator_from_pipeline"
        project = "pai_sdk_test"
        run_args = {
            "inputArtifact": "odps://{project_name}/tables/{table_name}".format(
                project_name=project, table_name="pai_sdk_test.lr_data_set"),
            "labelColName": "_c2",
            "featureColNames": "pm10,so2,co,no2",
            "modelName": model_name,
            "goodValue": 1,
            "project": "algo_public",
            "execution": {
                "odpsInfoFile": "/share/base/odpsInfo.ini",
                "endpoint": "http://service.cn-shanghai.maxcompute.aliyun.com/api",
                "logViewHost": "http://logview.odps.aliyun.com",
                "odpsProject": "pai_sdk_test",
            },
        }

        job = est.fit(wait=True, job_name="pysdk-test-estimator-pipeline", arguments=run_args)

        print(job.get_outputs())

        # assert odps offlineModel exists
        self.assertTrue(
            self.session.odps_client.exist_offline_model(name=model_name, project=project))

        # model = job.create_model(artifact="outputArtifact")
        # model.deploy()

    def test_new_composite_pipeline_to_estimator(self):
        pass
