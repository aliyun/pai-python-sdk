from __future__ import absolute_import

import logging
import os
import unittest
from collections import namedtuple
from odps import ODPS
from six.moves import configparser
import oss2

from pai.session import Session, set_default_pai_session

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

    odps_client = None
    default_xflow_project = 'algo_public'

    PUBLIC_DATASET_TABLE_HEART_DISEASE_PREDICTION = "odps://pai_online_project/tables/heart_disease_prediction"
    PUBLIC_DATASET_WUMAI_TABLE_NAME = 'pai_online_project.wumai_data'

    @classmethod
    def setUpClass(cls):
        super(BaseTestCase, cls).setUpClass()
        cls._set_test_session()
        cls.odps_client = cls._get_odps_client()
        cls.oss_info = cls._get_oss_info()
        cls._log_config()

    @classmethod
    def tearDownClass(cls):
        super(BaseTestCase, cls).tearDownClass()

    @classmethod
    def get_default_xflow_execution(cls, odps_client=None):
        if not odps_client:
            odps_client = cls.odps_client

        return {
            "odpsInfoFile": "/share/base/odpsInfo.ini",
            "endpoint": odps_client.endpoint,
            "logViewHost": odps_client.logview_host,
            "odpsProject": odps_client.project,
        }

    @classmethod
    def _set_test_session(cls):
        configs = cls.get_test_config()
        set_default_pai_session(**configs["client"])

    @classmethod
    def _get_odps_client(cls):
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
    def _get_oss_info(cls):
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
    def _log_config():
        logging.basicConfig(level=logging.INFO,
                            format='[%(asctime)s] %(pathname)s:%(lineno)d %(levelname)s '
                                   '- %(message)s',
                            datefmt='%Y/%m/%d %H:%M:%S')
