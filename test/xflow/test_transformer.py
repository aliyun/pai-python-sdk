from __future__ import absolute_import

from pai import RunInstance
from pai.job import JobStatus
from pai.xflow.transformer import OfflineModelTransformer, MaxComputeDataSource, ModelTransferToOSS
from test import BaseTestCase


class TestOfflineModelPredictionTransformer(BaseTestCase):

    def testXFlowOfflineModel(self):
        project = "pai_sdk_test"
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
            wait=True, job_name=None,
            feature_cols=["pm10", "so2", "co", "no2"],
            label_col="_c2",
            result_col="prediction_result",
            score_col="prediction_score",
            detail_col="prediction_detail",
            append_cols="time,hour,_c2,pm10,so2,co,no2",
        )

        self.assertEqual(JobStatus.Succeeded, job.get_status())
        outputs = job.get_outputs()

    def test_outputs(self):
        run_id = "flow-ec67rsug8kyly4049z"
        run_instance = RunInstance(run_id=run_id, session=self.session)
        print(run_instance.get_outputs())
        [{u'Info': {
            u'value': u'{"location": {"table": "pai_temp_77c08aeb2e514c9d8649feba4a88ee77"}}',
            u'metadata': {u'path': u'/tmp/outputs/artifacts/outputArtifact/data',
                          u'type': {u'DataSet': {u'locationType': u'MaxComputeTable'}}}},
          u'Name': u'outputArtifact', u'Producer': u'flow-ec67rsug8kyly4049z',
          u'CreateTime': 1595214018000, u'Type': u'DataSet', u'Id': u'artifact-e0xdqhsfhqctxkpyli'}]


class TestODPSDataSource(BaseTestCase):

    def test_data_source(self):
        tf = MaxComputeDataSource(session=self.session)
        job_name = "pysdk-test-data-source"
        run_job = tf.transform(table_name="pai_online_project.wumai_data", wait=False,
                               job_name=job_name)
        self.assertEqual(run_job.get_status(), JobStatus.Running)
        self.assertEqual(run_job.name, job_name)
        run_job.attach()
        self.assertEqual(run_job.get_status(), JobStatus.Succeeded)

        run_job.get_outputs()


class TestModelTransferToOSS(BaseTestCase):

    def setUp(self):
        super(TestModelTransferToOSS, self).setUp()

    def tearDown(self):
        super(TestModelTransferToOSS, self).tearDown()

    def test_model_transfer(self):
        tf = ModelTransferToOSS(
            session=self.session, bucket="dataplus-pai-test",
            endpoint="oss-cn-shanghai.aliyuncs.com",
            rolearn="acs:ram::1557702098194904:role/aliyunodpspaidefaultrole",
        )

        project = "pai_sdk_test"
        model_name = "pai_sdk_test_lr_offlinemodel"
        offlinemodel = 'odps://{0}/offlinemodels/{1}'.format(project, model_name)
        job = tf.transform(offlinemodel, path="/paiflow/test/noprefix/",
                           job_name="pysdk-test-modeltransfer2oss",
                           wait=True)
        self.assertEqual(JobStatus.Succeeded, job.get_status())


