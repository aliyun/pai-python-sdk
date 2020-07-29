from __future__ import absolute_import

import logging
import os
import unittest
from collections import namedtuple
from odps import ODPS
from six.moves import configparser
import oss2

from pai.session import Session

_test_root = os.path.dirname(os.path.abspath(__file__))

OSSInfo = namedtuple(
    "OSSInfo", [
        "bucket",
        "endpoint",
        "rolearn",
    ]
)


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
        cls.oss_info = cls.get_oss_info()
        cls.log_config()

    @classmethod
    def tearDownClass(cls):
        super(BaseTestCase, cls).tearDownClass()

    @classmethod
    def get_test_session(cls):
        configs = cls.get_test_config()
        return Session(**configs["client"])

    @classmethod
    def get_odps_client(cls):
        configs = cls.get_test_config()
        access_key_id = configs["odps"]["access_key_id"]
        access_key_secret = configs["odps"]["access_key_secret"]
        project = configs["odps"]["project"]
        return ODPS(
            access_id=access_key_id,
            secret_access_key=access_key_secret,
            project=project,
        )

    @classmethod
    def get_oss_info(cls):
        configs = cls.get_test_config()
        oss_info = OSSInfo(**configs["oss"])
        return oss_info

    @classmethod
    def get_test_config(cls):
        cfg_parser = configparser.ConfigParser()
        cfg_parser.read(os.path.join(_test_root, "test.ini"))
        access_key_id = cfg_parser.get("client", "access_key_id")
        access_key_secret = cfg_parser.get("client", "access_key_secret")
        region_id = cfg_parser.get("client", "region_id")
        odps_project = cfg_parser.get("odps", "project")

        return {
            "client": {
                "region_id": region_id,
                "access_key_id": access_key_id,
                "access_key_secret": access_key_secret
            },
            "odps": {
                "project": odps_project,
                "access_key_id": access_key_id,
                "access_key_secret": access_key_secret,
            },
            "oss": {
                "bucket": cfg_parser.get("oss", "bucket"),
                "endpoint": cfg_parser.get("oss", "endpoint"),
                "rolearn": cfg_parser.get("oss", "rolearn"),
            }
        }

    @staticmethod
    def log_config():
        logging.basicConfig(level=logging.INFO,
                            format='[%(asctime)s] %(pathname)s:%(lineno)d %(levelname)s '
                                   '- %(message)s',
                            datefmt='%Y/%m/%d %H:%M:%S')
