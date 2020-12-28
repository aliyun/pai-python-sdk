from __future__ import absolute_import

import random

from pai.algo.classifier import LogisticRegression
from pai.core.job import JobStatus
from pai.algo.transformer import OfflineModelTransformer, ModelTransferToOSS
from tests.integration import BaseIntegTestCase


class TestOfflineModelTransformer(BaseIntegTestCase):

    model_name = None
    train_dataset = BaseIntegTestCase.breast_cancer_dataset

    @classmethod
    def prepare_offline_model(cls):
        cls.model_name = "test_model_%d" % random.randint(0, 999999999)
        lr = LogisticRegression(
            regularized_type="l2",
            execution=cls.get_default_maxc_execution(),
        )
        dataset = cls.train_dataset
        _ = lr.fit(
            wait=True,
            show_outputs=False,
            input_data=dataset.to_url(),
            job_name="prepare-offlinemodel-job",
            model_name=cls.model_name,
            good_value=1,
            label_col=dataset.label_col,
            feature_cols=dataset.feature_cols,
        )

    @classmethod
    def setUpClass(cls):
        super(TestOfflineModelTransformer, cls).setUpClass()
        cls.prepare_offline_model()

    @classmethod
    def tearDownClass(cls):
        super(TestOfflineModelTransformer, cls).tearDownClass()
        cls.odps_client.delete_offline_model(cls.model_name, if_exists=True)

    def test_offlinemodel_transformer(self):
        project = self.maxc_config.project
        model_name = self.model_name
        tf = OfflineModelTransformer(
            model="odps://{0}/offlinemodels/{1}".format(project, model_name),
            execution=self.get_default_maxc_execution(),
        )
        job = tf.transform(
            self.train_dataset.to_url(),
            wait=False,
            job_name="pysdk-test-om-algo",
            feature_cols=",".join(self.train_dataset.feature_cols),
            label_col=self.train_dataset.label_col,
            result_col="prediction_result",
            score_col="prediction_score",
            detail_col="prediction_detail",
            append_cols=",".join(self.train_dataset.feature_cols),
        )

        job.wait_for_completion(show_outputs=True)

        self.assertEqual(JobStatus.Succeeded, job.get_status())

    def test_model_transfer(self):
        tf = ModelTransferToOSS(
            bucket=self.oss_config.bucket_name,
            endpoint=self.oss_config.endpoint,
            rolearn=self.oss_config.role_arn,
            execution=self.get_default_maxc_execution(),
        )

        model_name = self.model_name
        offlinemodel = "odps://{0}/offlinemodels/{1}".format(
            self.maxc_config.project, model_name
        )
        job = tf.transform(
            offlinemodel,
            path="/test/pai/offlinemodel_transfer/",
            job_name="pysdk-test-modeltransfer2oss",
            wait=False,
        )
        job.wait_for_completion(show_outputs=False)
        self.assertEqual(JobStatus.Succeeded, job.get_status())
