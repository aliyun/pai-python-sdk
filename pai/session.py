#  Copyright 2023 Alibaba, Inc. or its affiliates.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from __future__ import absolute_import

import json
import logging
import os.path
import posixpath
from datetime import datetime
from typing import Any, Dict, Optional, Union

import oss2
from alibabacloud_credentials.models import Config as CredentialConfig
from alibabacloud_credentials.utils import auth_constant

from .api.api_container import ResourceAPIsContainerMixin
from .common.consts import DEFAULT_CONFIG_PATH
from .common.oss_utils import CredentialProviderWrapper, OssUriObj
from .common.utils import is_domain_connectable, make_list_resource_iterator

logger = logging.getLogger(__name__)

# Environment variable that indicates where the config path is located.
# If it is not provided, "$HOME/.pai/config.json" is used as the default config path.
ENV_PAI_CONFIG_PATH = "PAI_CONFIG_PATH"

INNER_REGION_IDS = ["center"]


# Global default session used by the program.
_default_session = None

# Default config keys.
_DEFAULT_CONFIG_KEYS = [
    "region_id",
    "oss_bucket_name",
    "workspace_id",
    "oss_endpoint",
]


def setup_default_session(
    access_key_id: Optional[str] = None,
    access_key_secret: Optional[str] = None,
    security_token: Optional[str] = None,
    region_id: Optional[str] = None,
    credential_config: Optional[CredentialConfig] = None,
    oss_bucket_name: Optional[str] = None,
    oss_endpoint: Optional[str] = None,
    workspace_id: Optional[Union[str, int]] = None,
    **kwargs,
) -> "Session":
    """Set up the default session used in the program.

    The function construct a session that used for communicating with PAI service,
    and set it as the global default instance.

    Args:
        access_key_id (str): The access key ID used to access the Alibaba Cloud.
        access_key_secret (str): The access key secret used to access the Alibaba Cloud.
        security_token (str, optional): The security token used to access the Alibaba
            Cloud.
        credential_config (:class:`alibabacloud_credentials.models.Config`, optional):
            The credential config used to access the Alibaba Cloud.
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

    if (access_key_id and access_key_secret) and credential_config:
        raise ValueError("Please provide either access_key or credential_config.")
    elif not credential_config and (access_key_id and access_key_secret):
        # use explicit credential
        if security_token:
            credential_config = CredentialConfig(
                access_key_id=access_key_id,
                access_key_secret=access_key_secret,
                security_token=security_token,
                type=auth_constant.STS,
            )
        else:
            credential_config = CredentialConfig(
                access_key_id=access_key_id,
                access_key_secret=access_key_secret,
                type=auth_constant.ACCESS_KEY,
            )

    # override the config from default session
    default_session = get_default_session()

    region_id = region_id or default_session.region_id
    workspace_id = workspace_id or default_session.workspace_id
    oss_bucket_name = oss_bucket_name or default_session.oss_bucket_name
    oss_endpoint = oss_endpoint or default_session.oss_endpoint
    credential_config = credential_config or default_session.credential_config

    session = Session(
        region_id=region_id,
        credential_config=credential_config,
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
        config = load_default_config_file()
        if not config:
            return
        _default_session = Session(**config)
    return _default_session


def load_default_config_file() -> Optional[Dict[str, Any]]:
    """Read config file"""

    config_path = DEFAULT_CONFIG_PATH
    if not os.path.exists(config_path):
        return

    with open(config_path, "r") as f:
        config = json.load(f)
        config = {
            key: value for key, value in config.items() if key in _DEFAULT_CONFIG_KEYS
        }

    # for backward compatibility, try to read credential from config file.
    if "access_key_id" in config and "access_key_secret" in config:
        config["credential_config"] = CredentialConfig(
            access_key_id=config["access_key_id"],
            access_key_secret=config["access_key_secret"],
            type=auth_constant.ACCESS_KEY,
        )

    return config


class Session(ResourceAPIsContainerMixin):
    """A class responsible for communicating with PAI services."""

    def __init__(
        self,
        region_id: str,
        workspace_id: Optional[str] = None,
        credential_config: Optional[CredentialConfig] = None,
        oss_bucket_name: Optional[str] = None,
        oss_endpoint: Optional[str] = None,
        **kwargs,
    ):
        """PAI Session Initializer.

        Args:
            credential_config (:class:`alibabacloud_credentials.models.Config`, optional):
                The credential config used to access the Alibaba Cloud.
            region_id (str): The ID of the Alibaba Cloud region where the service
                is located.
            workspace_id (str, optional): ID of the workspace used in the default
                session.
            oss_bucket_name (str, optional): The name of the OSS bucket used in the
                session.
            oss_endpoint (str, optional): The endpoint for the OSS bucket.
        """

        if not region_id:
            raise ValueError("Region ID must be provided.")

        self._credential_config = credential_config
        self._region_id = region_id
        self._workspace_id = workspace_id
        self._oss_bucket_name = oss_bucket_name
        self._oss_endpoint = oss_endpoint

        header = kwargs.pop("header", None)
        super(Session, self).__init__(header=header)

    @property
    def region_id(self) -> str:
        return self._region_id

    @property
    def is_inner(self) -> bool:
        return self._region_id in INNER_REGION_IDS

    @property
    def oss_bucket_name(self) -> str:
        return self._oss_bucket_name

    @property
    def oss_endpoint(self) -> str:
        return self._oss_endpoint

    @property
    def credential_config(self) -> CredentialConfig:
        return self._credential_config

    @property
    def workspace_name(self):
        if hasattr(self, "_workspace_name") and self._workspace_name:
            return self._workspace_name

        if not self._workspace_id:
            raise ValueError("Workspace id is not set.")
        workspace_api_obj = self.workspace_api.get(workspace_id=self._workspace_id)
        self._workspace_name = workspace_api_obj["WorkspaceName"]
        return self._workspace_name

    @property
    def provider(self) -> str:
        caller_identity = self._acs_sts_client.get_caller_identity().body
        return caller_identity.account_id

    @property
    def workspace_id(self) -> str:
        """ID of the workspace used by the session."""
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

    def _get_oss_auth(self):
        auth = oss2.ProviderAuth(
            credentials_provider=CredentialProviderWrapper(
                config=self._credential_config,
            )
        )
        return auth

    @property
    def oss_bucket(self):
        """A OSS2 bucket instance used by the session."""
        if not self._oss_bucket_name or not self._oss_endpoint:
            self._init_oss_config()
        oss_bucket = oss2.Bucket(
            auth=self._get_oss_auth(),
            endpoint=self._oss_endpoint,
            bucket_name=self._oss_bucket_name,
        )
        return oss_bucket

    def save_config(self, config_path=None):
        """Save the configuration of the session to a local file."""
        attrs = {key.lstrip("_"): value for key, value in vars(self).items()}
        config = {
            key: value
            for key, value in attrs.items()
            if key in _DEFAULT_CONFIG_KEYS and value is not None
        }

        config_path = config_path or DEFAULT_CONFIG_PATH
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w") as f:
            f.write(json.dumps(config, indent=4))
        logger.info("Write PAI config succeed: config_path=%s" % config_path)

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

    def _get_default_oss_endpoint(self) -> str:
        """Returns a default OSS endpoint."""

        # OSS Endpoint document:
        # https://help.aliyun.com/document_detail/31837.html
        internet_endpoint = "oss-{}.aliyuncs.com".format(self.region_id)
        internal_endpoint = "oss-{}-internal.aliyuncs.com".format(self.region_id)

        return (
            internet_endpoint
            if is_domain_connectable(internal_endpoint)
            else internet_endpoint
        )

    def get_oss_bucket(self, bucket_name: str, endpoint: str = None) -> oss2.Bucket:
        """Get a OSS bucket using the credentials of the session.

        Args:
            bucket_name (str): The name of the bucket.
            endpoint (str): Endpoint of the bucket.

        Returns:
            :class:`oss2.Bucket`: A OSS bucket instance.

        """
        endpoint = endpoint or self._oss_endpoint or self._get_default_oss_endpoint()
        oss_bucket = oss2.Bucket(
            auth=self._get_oss_auth(),
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
        storage_path = posixpath.join("pai", category, dir_name).strip()

        if not storage_path.endswith("/"):
            storage_path += "/"
        return storage_path

    def is_supported_training_instance(self, instance_type: str) -> bool:
        """Check if the instance type is supported for training."""
        instance_generator = make_list_resource_iterator(self.job_api.list_ecs_specs)
        machine_spec = next(
            (
                item
                for item in instance_generator
                if item["InstanceType"] == instance_type
            ),
            None,
        )
        return bool(machine_spec)

    def is_gpu_training_instance(self, instance_type: str) -> bool:
        """Check if the instance type is GPU instance for training."""
        instance_generator = make_list_resource_iterator(self.job_api.list_ecs_specs)
        machine_spec = next(
            (
                item
                for item in instance_generator
                if item["InstanceType"] == instance_type
            ),
            None,
        )
        if not machine_spec:
            raise ValueError(
                f"Instance type {instance_type} is not supported for training job. "
                "Please provide a supported instance type."
            )
        return machine_spec["AcceleratorType"] == "GPU"

    def is_supported_inference_instance(self, instance_type: str) -> bool:
        """Check if the instance type is supported for inference."""
        res = self.service_api.describe_machine()["InstanceMetas"]
        spec = next(
            (item for item in res if item["InstanceType"] == instance_type), None
        )
        return bool(spec)

    def is_gpu_inference_instance(self, instance_type: str) -> bool:
        """Check if the instance type is GPU instance for inference."""
        res = self.service_api.describe_machine()["InstanceMetas"]
        spec = next(
            (item for item in res if item["InstanceType"] == instance_type), None
        )

        if not spec:
            raise ValueError(
                f"Instance type {instance_type} is not supported for deploying. "
                "Please provide a supported instance type."
            )
        return bool(spec["GPU"])
