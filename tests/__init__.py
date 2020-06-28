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
        self.session = self.get_test_session()

    def tearDown(self):
        pass

    @classmethod
    def get_test_session(cls):
        configs = cls.get_test_config()
        return Session(**configs)

    @classmethod
    def get_test_config(cls):
        cfg_parser = configparser.ConfigParser()
        cfg_parser.read(os.path.join(_test_root, 'test.conf'))
        access_key = cfg_parser.get('test', 'access_key')
        access_secret = cfg_parser.get('test', 'access_secret')
        region = cfg_parser.get('test', 'region')

        return {
            'region_id': region,
            'access_key': access_key,
            'access_secret': access_secret
        }
