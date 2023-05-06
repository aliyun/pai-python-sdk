from __future__ import absolute_import

import functools
import json
import logging
import os.path
import typing
from datetime import datetime
from typing import Callable, Optional

import oss2

from .api.api_container import ResourceAPIsContainerMixin
from .common.oss_utils import OssUriObj

logger = logging.getLogger(__name__)

# Environment variable that indicates where the config path is located.
# If it is not provided, "$HOME/.pai/config.json" is used as the default config path.
ENV_PAI_CONFIG_PATH = "PAI_CONFIG_PATH"

INNER_REGION_IDS = ["center"]


# Global default session used by the program.
_default_session = None


def config_default_session(f: Callable) -> Callable:
    """Decorator to config default session for the function."""

    @functools.wraps(f)
    def _(*args, **kwargs):
        if not kwargs.get("session"):
            kwargs["session"] = get_default_session()

        return f(*args, **kwargs)

    return _


def setup_default_session(
    access_key_id: str,
    access_key_secret: str,
    region_id: str,
    oss_bucket_name: Optional[str] = None,
    oss_endpoint: Optional[str] = None,
    workspace_id: Optional[typing.Union[str, int]] = None,
    **kwargs,
) -> "Session":
    """Set up the default session used in the program.

    The function construct a session that used for communicating with PAI service,
    and set it as the global default instance.

    Args:
        access_key_id (str): The access key ID for the Alibaba Cloud account.
        access_key_secret (str): The access key secret for the Alibaba Cloud
            account.
        region_id (str): The ID of the Alibaba Cloud region where the service
            is located.
        workspace_id (str, optional): ID of the workspace used in the default
            session.
        oss_bucket_name (str, optional): The name of the OSS bucket used in the
            session.
        oss_endpoint (str, optional): The endpoint for the OSS bucket.
        **kwargs:

    Returns:
        :class:`pai.session.Session`: Initialized default session.

    """
    session = Session(
        access_key_id,
        access_key_secret,
        region_id,
        oss_bucket_name=oss_bucket_name,
        oss_endpoint=oss_endpoint,
        workspace_id=workspace_id,
        **kwargs,
    )

    global _default_session
    _default_session = session
    return session


def get_default_session() -> "Session":
    """Get the default session used by the program.

    If the global default session is set, the function will try to initialize
    a session from config file.

    Returns:
        :class:`pai.session.Session`: The default session.

    """
    global _default_session
    if not _default_session:
        _default_session = Session.from_config()
    return _default_session


class Session(ResourceAPIsContainerMixin):
    """A class responsible for communicating with PAI services."""

    def __init__(
        self,
        access_key_id: str,
        access_key_secret: str,
        region_id: str,
        workspace_id: Optional[str] = None,
        security_token: Optional[str] = None,
        oss_bucket_name: Optional[str] = None,
        oss_endpoint: Optional[str] = None,
        **kwargs,
    ):
        """PAI Session Initializer.

        Args:
            access_key_id (str): The access key ID for the Alibaba Cloud account.
            access_key_secret (str): The access key secret for the Alibaba Cloud
                account.
            region_id (str): The ID of the Alibaba Cloud region where the service
                is located.
            workspace_id (str, optional): ID of the workspace used in the default
                session.
            oss_bucket_name (str, optional): The name of the OSS bucket used in the
                session.
            oss_endpoint (str, optional): The endpoint for the OSS bucket.
        """

        if not access_key_id or not access_key_secret or not region_id:
            raise ValueError("Please provide access_key, access_secret and region")

        self._region_id = region_id
        self._access_key_id = access_key_id
        self._access_key_secret = access_key_secret
        self._security_token = security_token
        self._workspace_id = workspace_id
        self._oss_bucket_name = oss_bucket_name
        self._oss_endpoint = oss_endpoint

        self._oss_access_key_id = kwargs.pop("oss_access_key_id", None)
        self._oss_access_key_secret = kwargs.pop("oss_access_key_secret", None)
        self._oss_security_token = kwargs.pop("oss_security_token", None)

        header = kwargs.pop("header", None)
        super(Session, self).__init__(header=header)

    @property
    def region_id(self) -> str:
        return self._region_id

    @property
    def is_inner(self) -> bool:
        return self._region_id in INNER_REGION_IDS

    @property
    def workspace_name(self):
        if hasattr(self, "_workspace_name") and self._workspace_name:
            return self._workspace_name

        workspace_id = self.workspace_id
        if not workspace_id:
            raise ValueError("Workspace id is not set.")
        workspace_api_obj = self.workspace_api.get(workspace_id=self.workspace_id)
        self._workspace_name = workspace_api_obj["WorkspaceName"]

        return self._workspace_name

    @property
    def provider(self) -> str:
        return self.pipeline_api.get_caller_provider()

    @property
    def workspace_id(self) -> str:
        """ID of the workspace used by the session.

        Returns the workspace used in the session, if workspace_id is not specified
        for the session, returns the default workspace id for the account.

        """
        if self._workspace_id:
            return self._workspace_id

        resp = self.workspace_api.get_default_workspace()
        self._workspace_id = resp["WorkspaceId"]
        return self._workspace_id

    @property
    def console_uri(self) -> str:
        """The web console URI for PAI service."""
        if self.is_inner:
            return "https://pai-next.alibaba-inc.com"
        else:
            return "https://pai.console.aliyun.com/console"

    def _init_oss_config(
        self,
    ):
        """Initialize a OssConfig instance."""
        if not self._oss_bucket_name:
            # If OSS bucket name is not provided, use the default OSS storage URI
            # that is configured for the workspace.
            default_oss_uri = self.workspace_api.get_default_storage_uri(
                self.workspace_id
            )
            if not default_oss_uri:
                raise RuntimeError(
                    "No default OSS URI is configured for the workspace."
                )
            oss_uri_obj = OssUriObj(default_oss_uri)
            self._oss_bucket_name = oss_uri_obj.bucket_name

        if not self._oss_endpoint:
            self._oss_endpoint = self._get_default_oss_endpoint()

    @property
    def oss_bucket(self):
        """A OSS2 bucket instance used by the session."""
        if not self._oss_bucket_name or not self._oss_endpoint:
            self._init_oss_config()

        if self._security_token:
            auth = oss2.StsAuth(
                access_key_id=self._access_key_id,
                access_key_secret=self._access_key_secret,
                security_token=self._security_token,
            )
        else:
            auth = oss2.Auth(
                access_key_id=self._access_key_id,
                access_key_secret=self._access_key_secret,
            )

        oss_bucket = oss2.Bucket(
            auth=auth,
            endpoint=self._oss_endpoint,
            bucket_name=self._oss_bucket_name,
        )
        return oss_bucket

    @classmethod
    def from_config(cls, config_path: Optional[str] = None):
        """Initialize a session instance from the config file.

        Args:
            config_path (str): The path to the config, if it is not provided,
             "$HOME/.pai/config" is used.

        Returns:
            :class:`pai.session.Session`: A PAI session instance.

        """
        return cls._init_from_file_config(config_path=config_path)

    def save_config(self, config_path=None):
        """Save the configuration of the session to a local file."""
        # Save attributes that startswith an underline.
        config = {
            key.lstrip("_"): value
            for key, value in vars(self).items()
            if key.startswith("_") and value is not None
        }

        if not config_path:
            default_config_path = os.path.join(
                os.path.expanduser("~"), ".pai", "config.json"
            )
            config_path = os.environ.get(ENV_PAI_CONFIG_PATH, default_config_path)

        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w") as f:
            f.write(json.dumps(config, indent=4))
        logger.info("Write PAI config succeed: config_path=%s" % config_path)

    @classmethod
    def _init_from_file_config(cls, config_path=None):
        """Read config file and construct a session instance.

        Returns:
            :class:`pai.session.Session`: Session instance init from config file.
        """
        if not config_path:
            default_config_path = os.path.join(
                os.path.expanduser("~"), ".pai", "config.json"
            )
            config_path = os.environ.get(ENV_PAI_CONFIG_PATH, default_config_path)
        if not os.path.exists(config_path):
            logger.warning("Not found config file: %s", config_path)
            return

        with open(config_path, "r") as f:
            config = json.load(f)

        sess = Session(**config)

        return sess

    def patch_oss_endpoint(self, oss_uri: str):
        oss_uri_obj = OssUriObj(oss_uri)
        if oss_uri_obj.endpoint:
            return oss_uri

        # patch endpoint using current OSS bucket endpoint.
        endpoint = self.oss_bucket.endpoint
        if endpoint.startswith("http://"):
            endpoint = endpoint.lstrip("http://")
        elif endpoint.startswith("https://"):
            endpoint = endpoint.lstrip("https://")
        return "oss://{bucket_name}.{endpoint}/{key}".format(
            bucket_name=oss_uri_obj.bucket_name,
            endpoint=endpoint,
            key=oss_uri_obj.object_key,
        )

    def _get_default_oss_endpoint(self):
        """Returns a default OSS endpoint."""
        if self._oss_endpoint:
            return self._oss_endpoint

        # OSS Endpoint document:
        # https://help.aliyun.com/document_detail/31837.html
        internet_endpoint = "oss-{}.aliyuncs.com".format(self.region_id)

        # TODO: support using internal endpoint if inspect the program
        #  is running in cloud.
        # internal_endpoint="oss-{}-internal.aliyuncs.com"

        return internet_endpoint

    def get_oss_bucket(self, bucket_name) -> oss2.Bucket:
        """Get a OSS bucket using the credentials of the session.

        Args:
            bucket_name (str): The name of the bucket.

        Returns:
            :class:`oss2.Bucket`: A OSS bucket instance.

        """
        endpoint = self._oss_endpoint or self._get_default_oss_endpoint()
        if self._security_token:
            auth = oss2.StsAuth(
                access_key_id=self._access_key_id,
                access_key_secret=self._access_key_secret,
                security_token=self._security_token,
            )
        else:
            auth = oss2.Auth(
                access_key_id=self._access_key_id,
                access_key_secret=self._access_key_secret,
            )
        oss_bucket = oss2.Bucket(
            auth=auth,
            endpoint=endpoint,
            bucket_name=bucket_name,
        )
        return oss_bucket

    @classmethod
    def get_storage_path_by_category(
        cls, category: str, dir_name: Optional[str] = None
    ) -> str:
        """Get an OSS storage path for the resource.

        Args:
            category (str): The category of the resource.
            dir_name (str, optional): The directory name of the resource.

        Returns:
            str: A OSS storage path.

        """
        dir_name = dir_name or datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        storage_path = os.path.join("pai", category, dir_name).strip()

        if not storage_path.endswith("/"):
            storage_path += "/"
        return storage_path
