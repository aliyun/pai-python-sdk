from __future__ import absolute_import

from pai.xflow.classifier import LogisticRegression
from test import BaseTestCase


class TestXFlowEstimator(BaseTestCase):

    def test_algo_init(self):
        lr = LogisticRegression(
            session=self.session,
            regularized_level=1.0,
            regularized_type="l2",
            max_iter=200,
            epsilon=1e-6
        )
        expected_parameters = {
            "regularized_level": 1.0,
            "regularized_type": "l2",
            "max_iter": 200,
            "epsilon": 1e-6,
        }
        self.assertEqual(lr.parameters, expected_parameters)

    def test_estimator_build(self):
        lr = LogisticRegression(
            session=self.session
        )

        args = {
            "regularized_level": 1.0,
            "regularized_type": "l2",
            "max_iter": 200,
            "epsilon": 1e-6,
            "feature_cols": ["pm2", "co2"],
            "label_col": "_c2",
            "model_name": "ut_lr_model",
            "enable_sparse": True,
            "sparse_delimiter": (",", ":")
        }

        expected = {
            "regularizedLevel": 1.0,
            "maxIter": 200,
            "epsilon": 1e-6,
            "featureColNames": "pm2,co2",
            "labelColName": "_c2",
            "modelName": "ut_lr_model",
            "enableSparse": True,
            "itemDelimiter": ",",
            "kvDelimiter": ":",
            "__xflowProject": lr.get_xflow_project(),
            "__execution": lr.get_xflow_execution(),
        }

        compiled_args = lr.rebuild_args(
            **args
        )

        self.assertEqual(expected, compiled_args)

    def test_multiple_call_fit(self):
        pass
