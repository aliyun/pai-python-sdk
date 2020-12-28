from __future__ import absolute_import
from __future__ import print_function

import random
import time

from pai.algo.classifier import LogisticRegression
from pai.core.job import JobStatus
from tests.integration import BaseIntegTestCase


class TestLogisticsRegression(BaseIntegTestCase):
    temp_models = []

    @classmethod
    def tearDownClass(cls):
        super(TestLogisticsRegression, cls).tearDownClass()
        for model_name in cls.temp_models:
            cls.odps_client.delete_offline_model(model_name, if_exists=True)

    @classmethod
    def gen_temp_model_name(cls):
        model_name = "test_model_%d" % random.randint(0, 999999999)
        cls.temp_models.append(model_name)
        return model_name

    def test_sync_train(self):
        model_name = self.gen_temp_model_name()
        lr = LogisticRegression(
            regularized_type="l2",
            execution=self.get_default_maxc_execution(),
        )

        dataset = self.breast_cancer_dataset
        run_job = lr.fit(
            wait=True,
            show_outputs=False,
            input_data=dataset.to_url(),
            job_name="pysdk-test-lr-sync-fit",
            model_name=model_name,
            good_value=1,
            label_col=dataset.label_col,
            feature_cols=dataset.feature_cols,
        )

        self.assertEqual(JobStatus.Succeeded, run_job.get_status())
        # PipelineOutput is not ready while status switch to succeed.
        time.sleep(10)
        offline_model = run_job.create_model(output_name="outputArtifact")
        self.assertIsNotNone(offline_model)

    def test_async_train(self):
        model_name = self.gen_temp_model_name()

        lr = LogisticRegression(
            regularized_type="l2",
            execution=self.get_default_maxc_execution(),
        )
        data_set = self.breast_cancer_dataset

        run_job = lr.fit(
            wait=False,
            input_data=data_set.to_url(),
            label_col=data_set.label_col,
            good_value=1,
            job_name="pysdk-test-lr-async-fit",
            model_name=model_name,
            feature_cols=data_set.feature_cols,
        )

        run_job.wait_for_completion()
        self.assertEqual(JobStatus.Succeeded, run_job.get_status())
        offline_model = run_job.create_model(output_name="outputArtifact")
        self.assertIsNotNone(offline_model)

        self.assertTrue(
            self.odps_client.exist_offline_model(
                model_name, project=self.odps_client.project
            )
        )
