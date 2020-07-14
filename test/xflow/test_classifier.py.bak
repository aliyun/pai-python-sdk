from __future__ import absolute_import

import random
import time

import odps
import pandas as pd
from sklearn.datasets import load_iris

from pai.xflow.classifier import LogisticRegression
from test import BaseTestCase


class TestLogisticsRegression(BaseTestCase):
    temp_tables = []

    @classmethod
    def setUpClass(cls):
        super(TestLogisticsRegression, cls).setUpClass()
        # prepare DataSet table
        iris_data = load_iris()
        columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'category']
        pddf = pd.DataFrame(dict(
            zip(columns, list(iris_data.data.T) + [iris_data.target])), columns=columns)

        cls.iris_table_name = 'test_iris_table_%d' % random.randint(0, 999999)
        print(cls.iris_table_name)
        cls.temp_tables.append(cls.iris_table_name)
        cls.iris_df = odps.DataFrame(pddf).persist(
            cls.iris_table_name, odps=cls.odps_client, lifecycle=1)

    # @classmethod
    # def tearDownClass(cls):
    #     # clear temp tables
    #     super(TestLogisticsRegression, cls).tearDownClass()
    #     for name in cls.temp_tables:
    #         cls.odps_client.delete_table(name, if_exists=True, async_=True)

    def testLogisticsRegressionSyncTrain(self):
        model_name = 'test_iris_model_%d' % random.randint(0, 999999)
        lr = LogisticRegression(
            session=self.session,
            regularized_type="l2",
        )
        run_job = lr.fit(wait=True, input_data=self.iris_df, label_col="category",
                         model_name=model_name)

        offline_model = run_job.create_model(name="ut_lr_%d" % (int(time.time())), artifact="outputArtifact")
        self.assertIsNotNone(offline_model)

    def testLogisticsRegressionAsyncTrain(self):
        model_name = 'test_iris_model_%d' % random.randint(0, 999999)
        lr = LogisticRegression(
            session=self.session,
            regularized_type="l2",
        )
        run_job = lr.fit(wait=False, input_data=self.iris_df, feature_cols=self.iris_df, label_col="category",
                         model_name=model_name)
        run_job.attach()
        offline_model = run_job.create_model(name="ut_lr_%d" % (int(time.time())), artifact="outputArtifact")
        self.assertIsNotNone(offline_model)

    def testLogisticsRegressionFitMultiCall(self):
        model_name = 'test_iris_model_%d' % random.randint(0, 999999)
        lr = LogisticRegression(
            session=self.session,
            regularized_level="l2"
        )
        run_job = lr.fit(wait=False, input_data=self.iris_df, feature_cols=self.iris_df, label_col="category",
                         model_name=model_name)

    def testArgumentsNotSatisfy(self):
        lr = LogisticRegression(
            session=self.session,
            regularized_type="l2",
        )
        with self.assertRaises(ValueError):
            # miss required arguments model_name
            lr.fit(wait=True, input_data=self.iris_df, feature_cols=self.iris_df, label_col="category")


class TestRandomForestClassifier(BaseTestCase):
    pass
