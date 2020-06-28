import os
import unittest
from tests import BaseTestCase
from tests.test_paiflow import load_local_yaml


class TestPaiFlowAPI(BaseTestCase):

    def setUp(self):
        super(TestPaiFlowAPI, self).setUp()

    def test_pipeline_crud(self):
        resp = self.session.list_pipeline()
        print(resp)


if __name__ == '__main__':
    unittest.main()
