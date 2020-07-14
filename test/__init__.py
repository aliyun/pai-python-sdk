from __future__ import absolute_import

import os
import logging
import unittest

from six.moves import configparser
from odps import ODPS

from pai.session import Session

_test_root = os.path.dirname(os.path.abspath(__file__))


class BaseTestCase(unittest.TestCase):
    """
    Base class for unittest, any test case class should inherit this.
    """

    session = None
    odps_client = None

    @classmethod
    def setUpClass(cls):
        super(BaseTestCase, cls).setUpClass()

        cls.session = cls.get_test_session()
        cls.odps_client = cls.get_odps_client()
        cls.log_config()

    @classmethod
    def tearDownClass(cls):
        super(BaseTestCase, cls).tearDownClass()

    @classmethod
    def get_test_session(cls):
        configs = cls.get_test_config()
        odps_project = configs["odps"]["project"]
        return Session(odps_project=odps_project, **configs["client"])

    @classmethod
    def get_odps_client(cls):
        configs = cls.get_test_config()
        access_key = configs["odps"]["access_key"]
        access_secret = configs["odps"]["access_secret"]
        project = configs["odps"]["project"]
        return ODPS(
            access_id=access_key,
            secret_access_key=access_secret,
            project=project,
        )

    @classmethod
    def get_test_config(cls):
        cfg_parser = configparser.ConfigParser()
        cfg_parser.read(os.path.join(_test_root, "test.conf"))
        access_key = cfg_parser.get("client", "access_key")
        access_secret = cfg_parser.get("client", "access_secret")
        region = cfg_parser.get("client", "region")
        odps_project = cfg_parser.get("odps", "odps_project")

        return {
            "client": {
                "region_id": region,
                "access_key": access_key,
                "access_secret": access_secret
            },
            "odps": {
                "project": odps_project,
                "access_key": access_key,
                "access_secret": access_secret,
            }
        }

    @staticmethod
    def log_config():
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s [%(levelname)s] %(message)s',
                            datefmt='%Y/%m/%d %H:%M:%S')
