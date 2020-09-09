from __future__ import absolute_import
from __future__ import print_function

import random
import time

import odps

from pai.core.job import JobStatus
from pai.xflow.classifier import LogisticRegression
from tests import BaseTestCase


class TestLogisticsRegression(BaseTestCase):
    temp_tables = []
    temp_models = []

    @classmethod
    def setUpClass(cls):
        super(TestLogisticsRegression, cls).setUpClass()
        # prepare DataSet table
        table_name = cls.TestDataSetTables["processed_wumai_data_1"]
        cls.iris_df = odps.DataFrame(cls.odps_client.get_table(table_name))

    @classmethod
    def tearDownClass(cls):
        # clear temp tables
        super(TestLogisticsRegression, cls).tearDownClass()
        for name in cls.temp_tables:
            cls.odps_client.delete_table(name, if_exists=True, async_=True)
        for model_name in cls.temp_models:
            cls.odps_client.delete_offline_model(model_name, if_exists=True)

    def test_sync_train(self):
        model_name = 'test_iris_model_%d' % random.randint(0, 999999)
        lr = LogisticRegression(
            regularized_type="l2",
            xflow_execution=self.get_default_xflow_execution(),
        )

        iris_dataset_table = self.odps_client.get_table(
            self.TestDataSetTables["processed_wumai_data_1"])

        run_job = lr.fit(wait=True, log_outputs=False, input_data=iris_dataset_table,
                         job_name="pysdk-test-lr-sync-fit",
                         model_name=model_name, good_value=1, label_col="_c2",
                         feature_cols=["pm10", "so2", "co", "no2"])

        self.assertEqual(JobStatus.Succeeded, run_job.get_status())
        # PipelineOutput is not ready while status switch to succeed.
        time.sleep(10)
        offline_model = run_job.create_model(output_name="outputArtifact")
        self.assertIsNotNone(offline_model)

    def test_async_train(self):
        model_name = 'test_wumai_model_%d' % random.randint(0, 999999)
        self.temp_models.append(model_name)

        lr = LogisticRegression(
            regularized_type="l2",
            xflow_execution=self.get_default_xflow_execution(),
        )
        run_job = lr.fit(wait=False, input_data=self.iris_df, label_col="_c2", good_value=1,
                         job_name="pysdk-test-lr-async-fit", model_name=model_name,
                         feature_cols=["pm10", "so2", "co", "no2"])

        self.assertEqual(JobStatus.Running, run_job.get_status())
        run_job.attach()
        self.assertEqual(JobStatus.Succeeded, run_job.get_status())
        time.sleep(20)
        offline_model = run_job.create_model(output_name="outputArtifact")
        self.assertIsNotNone(offline_model)

        self.assertTrue(self.odps_client.exist_offline_model(
            model_name, project=self.odps_client.project))

    def test_lr_multiple_call_fit(self):
        model_name1 = 'test_iris_model_%d' % random.randint(0, 999999)
        model_name2 = 'test_iris_model_%d' % random.randint(0, 999999)
        self.temp_models.append(model_name1)
        self.temp_models.append(model_name2)

        lr = LogisticRegression(
            regularized_level=1.0,
            xflow_execution=self.get_default_xflow_execution(),
        )
        job1 = lr.fit(wait=False, input_data=self.iris_df, job_name="pysdk-test-lr-multi-fit-1",
                      label_col="_c2", model_name=model_name1, good_value=1,
                      feature_cols=["pm10", "so2", "co", "no2"])

        self.assertEqual(lr.last_job, job1)

        job2 = lr.fit(wait=False, input_data=self.iris_df, label_col="_c2",
                      job_name="pysdk-test-lr-multi-fit-2", good_value=1,
                      feature_cols=["pm10", "so2", "co", "no2"],
                      model_name=model_name2)
        self.assertEqual(lr.last_job, job2)
        self.assertNotEqual(job1.run_id, job2.run_id)
        job1.attach()
        job2.attach()
