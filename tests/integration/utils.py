import configparser
import os
import shutil
from collections import namedtuple


from pai.core.session import EnvType

_test_root = os.path.dirname(os.path.abspath(__file__))


PaiServiceConfig = namedtuple(
    "AlibabaCloudServiceConfig",
    [
        "access_key_id",
        "access_key_secret",
        "region_id",
        "workspace_id",
        "endpoint",
        "env_type",
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


class TestContext(object):
    def __init__(self, pai_service_config, oss_config, maxc_config):
        self.pai_service_config = pai_service_config
        self.oss_config = oss_config
        self.maxc_config = maxc_config

    @property
    def has_docker(self):
        return shutil.which("docker") is not None

    @property
    def is_inner(self):
        return self.pai_service_config.region_id == "center"

    @property
    def env_type(self):
        if self.pai_service_config.env_type:
            return self.pai_service_config.env_type
        return EnvType.PublicCloud

    @classmethod
    def _load_test_config(cls):
        test_config = os.environ.get("PAI_TEST_CONFIG", "test.ini")
        cfg_parser = configparser.ConfigParser()
        cfg_parser.read(os.path.join(_test_root, test_config))

        access_key_id = cfg_parser.get("client", "access_key_id")
        access_key_secret = cfg_parser.get("client", "access_key_secret")
        region_id = cfg_parser.get("client", "region_id", fallback=None)
        endpoint = cfg_parser.get("client", "endpoint", fallback=None)
        _env_type_name = cfg_parser.get("client", "env_type", fallback=None)
        workspace_id = cfg_parser.get("client", "workspace_id", fallback=None)

        pai_service_config = PaiServiceConfig(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            region_id=region_id,
            env_type=EnvType.PublicCloud
            if not _env_type_name
            else EnvType[_env_type_name],
            workspace_id=workspace_id,
            endpoint=endpoint,
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

    @classmethod
    def load_test_config(cls):
        pai_service_config, oss_config, maxc_config = cls._load_test_config()
        return cls(
            pai_service_config,
            oss_config,
            maxc_config,
        )

    @classmethod
    def get_context(cls):
        return t_context


t_context = TestContext.load_test_config()
