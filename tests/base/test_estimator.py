from __future__ import absolute_import

from pai.common import ProviderAlibabaPAI
from pai.pipeline.template import PipelineTemplate
from tests import BaseTestCase


class TestEstimatorBase(BaseTestCase):

    def init_base_lr_estimator(self):
        identifier = "logisticregression-binary-xflow-maxCompute"
        version = "v1"
        provider = ProviderAlibabaPAI
        p = PipelineTemplate.get_by_identifier(identifier=identifier,
                                               provider=provider, version=version)
        parameters = {
            "project": "algo_public",
            "epsilon": 1e-06,
            "maxIter": 100,
            # "regularizedType": "l1",
            "regularizedLevel": 1.0,
        }
        est = p.to_estimator(parameters=parameters)
        return p, est

    def test_init_base_lr_estimator(self):
        p, est = self.init_base_lr_estimator()
        self.assertEqual(est.identifier, p.identifier)
        self.assertEqual(est.provider, p.provider)
        self.assertEqual(est.pipeline_id, p.pipeline_id)
