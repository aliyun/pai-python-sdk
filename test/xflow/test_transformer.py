from __future__ import absolute_import

from pai.xflow.transformer import XFlowOfflineModelTransformer
from pai.xflow.classifier import LogisticRegression

from test import BaseTestCase


class TestTransformer(BaseTestCase):

    # Train offline model
    @classmethod
    def setUpClass(cls):
        super(TestTransformer, cls).setUpClass()

    # TODO: wait for artifact value format
    @classmethod
    def prepare_offline_model(cls):
        pass

    # remove useless offline model
    @classmethod
    def tearDownClass(cls):
        super(TestTransformer, cls).tearDownClass()

    def testXFlowOfflineModel(self):
        offline_model = XFlowOfflineModelTransformer(
            session=self.session,
            model=self.model
        )
        offline_model.transform()
