from __future__ import absolute_import
from __future__ import print_function

import random
import time

import odps
import pandas as pd
from six.moves import zip
from sklearn.datasets import load_iris

from pai.job import JobStatus
from pai.xflow.classifier import LogisticRegression
from tests import BaseTestCase


class TestLogisticsRegression(BaseTestCase):
    temp_tables = []

    @classmethod
    def setUpClass(cls):
        super(TestLogisticsRegression, cls).setUpClass()
        # prepare DataSet table
        iris_data = load_iris()
        columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'category']
        pddf = pd.DataFrame(dict(
            list(zip(columns, list(iris_data.data.T) + [iris_data.target]))), columns=columns)

        cls.iris_table_name = 'test_iris_table_%d' % random.randint(0, 999999)
        cls.temp_tables.append(cls.iris_table_name)
        cls.iris_df = odps.DataFrame(pddf).persist(
            cls.iris_table_name, odps=cls.odps_client, lifecycle=1)

    @classmethod
    def tearDownClass(cls):
        # clear temp tables
        super(TestLogisticsRegression, cls).tearDownClass()
        for name in cls.temp_tables:
            cls.odps_client.delete_table(name, if_exists=True, async_=True)

    def test_sync_train(self):
        project = self.odps_client.project
        model_name = 'test_iris_model_%d' % random.randint(0, 999999)
        lr = LogisticRegression(
            session=self.session,
            regularized_type="l2",
            xflow_execution={
                "odpsInfoFile": "/share/base/odpsInfo.ini",
                "endpoint": "http://service.cn-shanghai.maxcompute.aliyun.com/api",
                "logViewHost": "http://logview.odps.aliyun.com",
                "odpsProject": project,
            }
        )

        iris_dataset_table = 'odps://pai_online_project/tables/iris_data'

        run_job = lr.fit(wait=True, log_outputs=False, input_data=iris_dataset_table,
                         job_name="pysdk-test-lr-sync-fit",
                         model_name=model_name, good_value=1, label_col="type",
                         feature_cols=['f1', 'f2', 'f3', 'f4'])

        self.assertEqual(JobStatus.Succeeded, run_job.get_status())
        # PipelineOutput is not ready while status switch to succeed.
        time.sleep(10)
        offline_model = run_job.create_model(output_name="outputArtifact")
        self.assertIsNotNone(offline_model)

    def test_async_train(self):
        model_name = 'test_iris_model_%d' % random.randint(0, 999999)
        lr = LogisticRegression(
            session=self.session,
            regularized_type="l2",
            xflow_execution={
                "odpsInfoFile": "/share/base/odpsInfo.ini",
                "endpoint": "http://service.cn-shanghai.maxcompute.aliyun.com/api",
                "logViewHost": "http://logview.odps.aliyun.com",
                "odpsProject": self.odps_client.project,
            }
        )
        run_job = lr.fit(wait=False, input_data=self.iris_df, label_col="category",
                         job_name="pysdk-test-lr-async-fit", model_name=model_name,
                         good_value=1,
                         feature_cols=['sepal_length', 'sepal_width', 'petal_length',
                                       'petal_width'])

        self.assertEqual(JobStatus.Running, run_job.get_status())
        run_job.attach()
        self.assertEqual(JobStatus.Succeeded, run_job.get_status())
        time.sleep(20)
        offline_model = run_job.create_model(output_name="outputArtifact")
        self.assertIsNotNone(offline_model)

        self.assertTrue(self.odps_client.exist_offline_model(
            model_name, project=self.odps_client.project))

    def test_lr_multiple_call_fit(self):
        model_name = 'test_iris_model_%d' % random.randint(0, 999999)
        lr = LogisticRegression(
            session=self.session,
            regularized_level=1.0,
            xflow_execution={
                "odpsInfoFile": "/share/base/odpsInfo.ini",
                "endpoint": "http://service.cn-shanghai.maxcompute.aliyun.com/api",
                "logViewHost": "http://logview.odps.aliyun.com",
                "odpsProject": self.odps_client.project,
            }
        )
        job1 = lr.fit(wait=False, input_data=self.iris_df, job_name="pysdk-test-lr-multi-fit-1",
                      label_col="category", model_name=model_name, good_value=1,
                      feature_cols=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'], )

        self.assertEqual(lr.last_job, job1)

        job2 = lr.fit(wait=False, input_data=self.iris_df, label_col="category",
                      job_name="pysdk-test-lr-multi-fit-2", good_value=1,
                      feature_cols=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'],
                      model_name=model_name)
        self.assertEqual(lr.last_job, job2)
        self.assertNotEqual(job1.run_id, job2.run_id)

    def test_enable_spare(self):
        pass


class TestRandomForestClassifier(BaseTestCase):
    pass
