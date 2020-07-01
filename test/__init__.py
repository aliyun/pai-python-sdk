from __future__ import absolute_import

import os
import unittest

from six.moves import configparser

from pai.session import Session

_test_root = os.path.dirname(os.path.abspath(__file__))


class BaseTestCase(unittest.TestCase):
    """
    Base class for unittest, any test case class should inherit this.
    """

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.session = self.get_test_session()

    def tearDown(self):
        super(BaseTestCase, self).tearDown()

    @classmethod
    def get_test_session(cls):
        configs = cls.get_test_config()
        return Session(**configs["client"])

    @classmethod
    def get_test_config(cls):
        cfg_parser = configparser.ConfigParser()
        cfg_parser.read(os.path.join(_test_root, "test.conf"))
        access_key = cfg_parser.get("client", "access_key")
        access_secret = cfg_parser.get("client", "access_secret")
        region = cfg_parser.get("client", "region")

        return {
            "client": {
                "region_id": region,
                "access_key": access_key,
                "access_secret": access_secret
            }
        }
