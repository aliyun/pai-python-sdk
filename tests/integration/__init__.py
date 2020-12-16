from __future__ import absolute_import

from collections import namedtuple

import logging
import os
import oss2
import unittest
from odps import ODPS
from six.moves import configparser

from pai.core import setup_default_session

_test_root = os.path.dirname(os.path.abspath(__file__))


PaiServiceConfig = namedtuple(
    "AlibabaCloudServiceConfig",
    [
        "access_key_id",
        "access_key_secret",
        "region_id",
        "workspace_id",
    ],
)


MaxcConfig = namedtuple(
    "MaxcConfig",
    [
        "access_key_id",
        "access_key_secret",
        "endpoint",
        "project",
    ],
)

OssConfig = namedtuple(
    "OssConfig",
    [
        "access_key_id",
        "access_key_secret",
        "bucket_name",
        "endpoint",
        "role_arn",
    ],
)


class BaseIntegTestCase(unittest.TestCase):
    """
    Base class for unittest, any test case class should inherit this.
    """

    oss_info = None
    oss_bucket = None

    odps_client = None
    default_xflow_project = "algo_public"

    TestDataSetTables = {
        "heart_disease_prediction": "heart_disease_prediction",
        "wumai_data": "wumai_data",
        "iris_data": "iris_data",
        "processed_wumai_data_1": "sdk_test_wumai_dataset_1",
        "processed_wumai_data_2": "sdk_test_wumai_dataset_2",
    }

    TestModels = {"wumai_model": "wumai_model"}

    @classmethod
    def setUpClass(cls):
        super(BaseIntegTestCase, cls).setUpClass()
        cls._log_config()

        pai_service_config, oss_config, maxc_config = cls.load_test_config()

        cls.oss_info, cls.oss_bucket = cls._get_oss_bucket(oss_config)
        cls._setup_test_session(pai_service_config, oss_config)
        cls.odps_client = cls._get_odps_client(maxc_config)

    @classmethod
    def tearDownClass(cls):
        super(BaseIntegTestCase, cls).tearDownClass()

    @classmethod
    def get_default_maxc_execution(cls, odps_client=None):
        if not odps_client:
            odps_client = cls.odps_client

        return {
            "odpsInfoFile": "/share/base/odpsInfo.ini",
            "endpoint": odps_client.endpoint,
            "logViewHost": odps_client.logview_host,
            "odpsProject": odps_client.project,
        }

    @classmethod
    def _setup_test_session(cls, pai_service_config, oss_config):
        return setup_default_session(
            access_key_id=pai_service_config.access_key_id,
            access_key_secret=pai_service_config.access_key_secret,
            region_id=pai_service_config.region_id,
            workspace_id=pai_service_config.workspace_id,
            oss_bucket_name=oss_config.bucket_name,
            oss_endpoint=oss_config.endpoint,
        )

    @classmethod
    def _get_odps_client(cls, maxc_config):
        return ODPS(
            access_id=maxc_config.access_key_id,
            secret_access_key=maxc_config.access_key_secret,
            project=maxc_config.project,
            endpoint=maxc_config.endpoint,
        )

    @classmethod
    def _get_oss_bucket(cls, oss_config):
        oss_auth = oss2.Auth(
            access_key_id=oss_config.access_key_id,
            access_key_secret=oss_config.access_key_secret,
        )
        oss_bucket = oss2.Bucket(
            oss_auth,
            endpoint=oss_config.endpoint,
            bucket_name=oss_config.bucket_name,
        )
        return oss_config, oss_bucket

    @classmethod
    def load_test_config(cls):
        test_config = os.environ.get("PAI_TEST_CONFIG", "test.ini")
        cfg_parser = configparser.ConfigParser()
        cfg_parser.read(os.path.join(_test_root, test_config))

        access_key_id = cfg_parser.get("client", "access_key_id")
        access_key_secret = cfg_parser.get("client", "access_key_secret")
        region_id = cfg_parser.get("client", "region_id")

        pai_service_config = PaiServiceConfig(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            region_id=region_id,
            workspace_id=cfg_parser.get("client", "workspace_id"),
        )

        oss_config = OssConfig(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            bucket_name=cfg_parser.get("oss", "bucket"),
            endpoint=cfg_parser.get("oss", "endpoint"),
            role_arn=cfg_parser.get("oss", "rolearn"),
        )

        maxc_config = MaxcConfig(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            endpoint=cfg_parser.get("odps", "endpoint"),
            project=cfg_parser.get("odps", "project"),
        )
        return pai_service_config, oss_config, maxc_config

    @staticmethod
    def _log_config():
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] %(pathname)s:%(lineno)d %(levelname)s "
            "- %(message)s",
            datefmt="%Y/%m/%d %H:%M:%S",
        )
