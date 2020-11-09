from __future__ import absolute_import

from pai.core.job import JobStatus
from pai.xflow.transformer import OfflineModelTransformer, ModelTransferToOSS
from tests.integration import BaseIntegTestCase


class TestOfflineModelTransformer(BaseIntegTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestOfflineModelTransformer, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(TestOfflineModelTransformer, cls).tearDownClass()

    def test_XFlowOfflineModel(self):
        project = self.odps_client.project
        model_name = self.TestModels["wumai_model"]
        tf = OfflineModelTransformer(
            model="odps://{0}/offlinemodels/{1}".format(project, model_name),
            xflow_execution=self.get_default_xflow_execution(),
        )
        job = tf.transform(
            "odps://{}/tables/{}".format(
                project, self.TestDataSetTables["processed_wumai_data_2"]
            ),
            wait=False,
            job_name="pysdk-test-om-algo",
            feature_cols=["pm10", "so2", "co", "no2"],
            label_col="_c2",
            result_col="prediction_result",
            score_col="prediction_score",
            detail_col="prediction_detail",
            append_cols="time,hour,_c2,pm10,so2,co,no2",
        )

        job.wait_for_completion(show_outputs=False, timeout=None)

        self.assertEqual(JobStatus.Succeeded, job.get_status())

    def test_model_transfer(self):
        tf = ModelTransferToOSS(
            bucket=self.oss_info.bucket,
            endpoint=self.oss_info.endpoint,
            rolearn=self.oss_info.rolearn,
            xflow_execution=self.get_default_xflow_execution(),
        )

        model_name = self.TestModels["wumai_model"]
        offlinemodel = "odps://{0}/offlinemodels/{1}".format(
            self.odps_client.project, model_name
        )
        job = tf.transform(
            offlinemodel,
            path="/paiflow/test/noprefix/",
            job_name="pysdk-test-modeltransfer2oss",
            wait=False,
        )
        job.wait_for_completion(show_outputs=False)
        self.assertEqual(JobStatus.Succeeded, job.get_status())
