from __future__ import absolute_import

from pai.xflow.transformer import XFlowOfflineModelTransformer
from test import BaseTestCase


class TestTransformer(BaseTestCase):

    # Train offline model
    def setUpClass(cls):
        super(TestTransformer, cls).setUpClass()

    # remove useless offline model
    def tearDownClass(cls):
        super(TestTransformer, cls).tearDownClass()

    def testXFlowOfflineModel(self):
        offline_model = XFlowOfflineModelTransformer(
            session=self.session,
            model=self.model
        )
        offline_model.transform()
