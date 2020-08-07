from __future__ import absolute_import

import time

from pai.job import JobStatus
from pai.xflow.transformer import OfflineModelTransformer, MaxComputeDataSource, ModelTransferToOSS, \
    FeatureNormalize
from tests import BaseTestCase


class TestOfflineModelPredictionTransformer(BaseTestCase):

    def test_XFlowOfflineModel(self):
        project = self.odps_client.project
        model_name = "pai_sdk_test_lr_offlinemodel"
        tf = OfflineModelTransformer(
            session=self.session,
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
            wait=False, job_name="pysdk-test-om-algo",
            feature_cols=["pm10", "so2", "co", "no2"],
            label_col="_c2",
            result_col="prediction_result",
            score_col="prediction_score",
            detail_col="prediction_detail",
            append_cols="time,hour,_c2,pm10,so2,co,no2",
        )

        job.attach(log_outputs=False, timeout=None)

        self.assertEqual(JobStatus.Succeeded, job.get_status())

        # outputs = job.get_outputs()
        # time.sleep(20)
        # self.assertTrue(len(job.get_outputs()) > 0)
        # self.assertTrue("outputArtifact" in outputs)


class TestODPSDataSource(BaseTestCase):

    def test_data_source(self):
        tf = MaxComputeDataSource(session=self.session,
                                  xflow_execution={
                                      "odpsInfoFile": "/share/base/odpsInfo.ini",
                                      "endpoint": "http://service.cn-shanghai.maxcompute.aliyun.com/api",
                                      "logViewHost": "http://logview.odps.aliyun.com",
                                      "odpsProject": self.odps_client.project,
                                  })
        job_name = "pysdk-test-data-source"
        run_job = tf.transform(table_name="pai_online_project.wumai_data", wait=False,
                               job_name=job_name)
        self.assertEqual(run_job.get_status(), JobStatus.Running)
        self.assertEqual(run_job.name, job_name)
        run_job.attach(log_outputs=False)
        self.assertEqual(run_job.get_status(), JobStatus.Succeeded)
        # TODO: Pipeline outputs is not ready even enter Succeed status.
        time.sleep(10)
        self.assertTrue(len(run_job.get_outputs()) > 0)


class TestModelTransferToOSS(BaseTestCase):

    def test_model_transfer(self):
        tf = ModelTransferToOSS(
            session=self.session, bucket=self.oss_info.bucket,
            endpoint=self.oss_info.endpoint,
            rolearn=self.oss_info.rolearn,
            xflow_execution={
                "odpsInfoFile": "/share/base/odpsInfo.ini",
                "endpoint": "http://service.cn-shanghai.maxcompute.aliyun.com/api",
                "logViewHost": "http://logview.odps.aliyun.com",
                "odpsProject": self.odps_client.project,
            })

        model_name = "pai_sdk_test_lr_offlinemodel"
        offlinemodel = 'odps://{0}/offlinemodels/{1}'.format(self.odps_client.project, model_name)
        job = tf.transform(offlinemodel, path="/paiflow/test/noprefix/",
                           job_name="pysdk-test-modeltransfer2oss",
                           wait=False)
        job.attach(log_outputs=False)
        self.assertEqual(JobStatus.Succeeded, job.get_status())
