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


class PublicMaxComputeTableDataSet(object):
    default_dataset_project = "pai_online_project"

    def __init__(self, table_name, feature_cols, label_col):
        self.table_name = table_name
        self.feature_cols = feature_cols
        self.label_col = label_col

    @property
    def columns(self):
        return self.feature_cols + [self.label_col]

    def get_table(self):
        return "%s.%s" % (self.default_dataset_project, self.table_name)

    def to_url(self):
        return "odps://{0}/tables/{1}".format(
            type(self).default_dataset_project, self.table_name
        )

    @classmethod
    def set_dataset_project(cls, dataset_project):
        cls.default_dataset_project = dataset_project


class BaseIntegTestCase(unittest.TestCase):
    """
    Base class for unittest, any test case class should inherit this.
    """

    maxc_config = None
    pai_service_config = None
    oss_config = None

    default_session = None
    odps_client = None
    default_xflow_project = "algo_public"

    wumai_dataset = PublicMaxComputeTableDataSet(
        table_name="wumai_data",
        feature_cols=[
            "hour",
            "time",
            "pm10",
            "so2",
            "co",
            "no2",
        ],
        label_col="pm2",
    )

    breast_cancer_dataset = PublicMaxComputeTableDataSet(
        table_name="breast_cancer_data",
        feature_cols=[
            "age",
            "menopause",
            "tumor_size",
            "inv_nodes",
            "node_caps",
            "deg_malig",
            "breast",
            "breast_quad",
            "irradiat",
        ],
        label_col="class",
    )

    heart_disease_prediction_dataset = PublicMaxComputeTableDataSet(
        table_name="heart_disease_prediction",
        feature_cols=[
            "sex",
            "cp",
            "fbs",
            "restecg",
            "exang",
            "slop",
            "thal",
            "age",
            "trestbps",
            "chol",
            "thalach",
            "oldpeak",
            "ca",
        ],
        label_col="ifhealth",
    )

    @classmethod
    def setUpClass(cls):
        super(BaseIntegTestCase, cls).setUpClass()
        cls._log_config()

        cls.pai_service_config, cls.oss_config, cls.maxc_config = cls.load_test_config()

        cls.oss_bucket = cls._init_oss_bucket()
        cls.default_session = cls._setup_test_session()
        if cls.default_session._is_inner:
            PublicMaxComputeTableDataSet.set_dataset_project("pai_inner_project")

        cls.odps_client = cls._init_maxc_client()

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
            "odpsProject": odps_client.project,
        }

    @classmethod
    def _setup_test_session(cls):
        return setup_default_session(
            access_key_id=cls.pai_service_config.access_key_id,
            access_key_secret=cls.pai_service_config.access_key_secret,
            region_id=cls.pai_service_config.region_id,
            workspace_id=cls.pai_service_config.workspace_id,
            oss_bucket_name=cls.oss_config.bucket_name,
            oss_endpoint=cls.oss_config.endpoint,
        )

    @classmethod
    def _init_maxc_client(cls):
        return ODPS(
            access_id=cls.maxc_config.access_key_id,
            secret_access_key=cls.maxc_config.access_key_secret,
            project=cls.maxc_config.project,
            endpoint=cls.maxc_config.endpoint,
        )

    @classmethod
    def _init_oss_bucket(cls):
        oss_auth = oss2.Auth(
            access_key_id=cls.oss_config.access_key_id,
            access_key_secret=cls.oss_config.access_key_secret,
        )
        oss_bucket = oss2.Bucket(
            oss_auth,
            endpoint=cls.oss_config.endpoint,
            bucket_name=cls.oss_config.bucket_name,
        )
        return oss_bucket

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
