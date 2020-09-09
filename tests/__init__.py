from __future__ import absolute_import

import logging
import os
import unittest
from collections import namedtuple

import oss2
from odps import ODPS
from six.moves import configparser
from six.moves.configparser import DEFAULTSECT

from pai.session import setup_default_pai_session
from pai.workspace import Workspace

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

    TestDataSetTables = {
        "heart_disease_prediction": "heart_disease_prediction",
        "wumai_data": "wumai_data",
        "iris_data": "iris_data",
        "processed_wumai_data_1": "sdk_test_wumai_dataset_1",
        "processed_wumai_data_2": "sdk_test_wumai_dataset_2",
    }

    TestModels = {
        "wumai_model": "wumai_model"
    }

    @classmethod
    def setUpClass(cls):
        super(BaseTestCase, cls).setUpClass()
        cls._log_config()

        cls._set_test_session()
        cls.odps_client = cls._get_odps_client()
        cls.oss_info, cls.oss_bucket = cls._get_oss_info()

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
        client_config = cls.get_test_config()["client"]
        workspace_name = client_config.pop("workspace_name")

        default_session = setup_default_pai_session(**client_config)

        if not workspace_name:
            return default_session
        ws = Workspace.get_by_name(workspace_name)
        if not ws:
            ws = Workspace.create(name=workspace_name)
        default_session.set_workspace(ws)
        return default_session

    @classmethod
    def _get_odps_client(cls):
        configs = cls.get_test_config()
        access_key_id = configs["odps"]["access_key_id"]
        access_key_secret = configs["odps"]["access_key_secret"]
        project = configs["odps"]["project"]
        endpoint = configs["odps"]["endpoint"]
        logview_host = configs["odps"]["logview_host"]
        return ODPS(
            access_id=access_key_id,
            secret_access_key=access_key_secret,
            project=project,
            endpoint=endpoint,
            logview_host=logview_host,
        )

    @classmethod
    def _get_oss_info(cls):
        configs = cls.get_test_config()
        oss_info = OSSInfo(**configs["oss"])
        oss_auth = oss2.Auth(
            access_key_id=configs["client"]["access_key_id"],
            access_key_secret=configs["client"]["access_key_secret"],
        )
        oss_bucket = oss2.Bucket(oss_auth, endpoint=oss_info.endpoint, bucket_name=oss_info.bucket)
        return oss_info, oss_bucket

    @classmethod
    def get_test_config(cls):
        cfg_parser = configparser.ConfigParser()

        cfg_parser.set(section=DEFAULTSECT, option="workspace_name", value="")
        cfg_parser.read(os.path.join(_test_root, "test.ini"))
        access_key_id = cfg_parser.get("client", "access_key_id")
        access_key_secret = cfg_parser.get("client", "access_key_secret")
        workspace_name = cfg_parser.get("client", "workspace_name")
        region_id = cfg_parser.get("client", "region_id")
        odps_project = cfg_parser.get("odps", "project")
        odps_endpoint = cfg_parser.get("odps", "endpoint")
        odps_logview_host = cfg_parser.get("odps", "logview_host")

        return {
            "client": {
                "region_id": region_id,
                "access_key_id": access_key_id,
                "access_key_secret": access_key_secret,
                "workspace_name": workspace_name,
            },
            "odps": {
                "project": odps_project,
                "access_key_id": access_key_id,
                "access_key_secret": access_key_secret,
                "endpoint": odps_endpoint,
                "logview_host": odps_logview_host,
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
