from __future__ import absolute_import

import unittest
from pprint import pprint

from pai.job import JobStatus
from pai.xflow.transformer import OfflineModelTransformer, MaxComputeDataSource
from test import BaseTestCase


class TestOfflineModelPredictionTransformer(BaseTestCase):

    def testXFlowOfflineModel(self):
        project = "pai_sdk_test"
        model_name = "pai_sdk_test_lr_offlinemodel"
        tf = OfflineModelTransformer(session=self.session,
                                     model="odps://{0}/offlinemodels/{1}".format(project,
                                                                                 model_name),
                                     xflow_execution={
                                         "odpsInfoFile": "/share/base/odpsInfo.ini",
                                         "endpoint": "http://service.cn-shanghai.maxcompute.aliyun.com/api",
                                         "logViewHost": "http://logview.odps.aliyun.com",
                                         "odpsProject": project,
                                     })
        job = tf.transform(
            "odps://{}/tables/offline_model_test_data_set".format(project),
            wait=True, job_name=None,
            feature_cols=["pm10", "so2", "co", "no2"],
            label_col="_c2",
            result_col="prediction_result",
            score_col="prediction_score",
            detail_col="prediction_detail",
            append_cols="time,hour,_c2,pm10,so2,co,no2",
        )

        self.assertEqual(JobStatus.Succeeded, job.get_status())


class TestODPSDataSource(BaseTestCase):

    # @unittest.skip("Backend artifact support not ready")
    def test_data_source(self):
        tf = MaxComputeDataSource(session=self.session)
        job_name = "test_data_source"
        run_job = tf.transform(table_name="pai_online_project.wumai_data", wait=False,
                               job_name=job_name)
        self.assertEqual(run_job.get_status(), JobStatus.Running)
        self.assertEqual(run_job.name, job_name)
        run_job.attach()
        self.assertEqual(run_job.get_status(), JobStatus.Succeeded)

        run_job.get_outputs()
