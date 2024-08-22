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

import locale
import os
import re
from typing import Any, Dict, List, Optional, Tuple

import oss2
from alibabacloud_credentials.client import Client as CredentialClient
from alibabacloud_credentials.models import Config as CredentialConfig
from alibabacloud_sts20150401.client import Client
from alibabacloud_sts20150401.models import (
    GetCallerIdentityResponseBody as CallerIdentity,
)
from alibabacloud_tea_openapi import models as open_api_models
from oss2.models import BucketInfo, SimplifiedBucketInfo
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.layout import HSplit, Layout
from prompt_toolkit.shortcuts import confirm as prompt_confirm
from prompt_toolkit.widgets import Label, RadioList

from ...api.base import ServiceName
from ...api.client_factory import ClientFactory
from ...api.workspace import WorkspaceAPI, WorkspaceConfigKeys
from ...common.consts import DEFAULT_NETWORK_TYPE, PAI_VPC_ENDPOINT, Network
from ...common.logging import get_logger
from ...common.oss_utils import CredentialProviderWrapper, OssUriObj
from ...common.utils import is_domain_connectable, make_list_resource_iterator
from ...libs.alibabacloud_pai_dsw20220101.client import Client as DswClient
from ...session import Session

logger = get_logger(__name__)

locale_code, _ = locale.getdefaultlocale()

OSS_NAME_PATTERN = re.compile(pattern="^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$")
ZH_CN_LOCAL = "zh_CN"

# RoleARN pattern for AssumedRole CallerIdentity
ASSUMED_ROLE_ARN_PATTERN = re.compile(r"acs:ram::\d+:assumed-role/([^/]+)/.*")

# DSW Notebook Default Role Name:
PAI_DSW_DEFAULT_ROLE_NAME = "aliyunpaidswdefaultrole"


DEFAULT_PRODUCT_RAM_ROLE_NAMES = [
    "AliyunODPSPAIDefaultRole",
    "AliyunPAIAccessingOSSRole",
    "AliyunPAIDLCAccessingOSSRole",
    "AliyunPAIDLCDefaultRole",
]


class WorkspaceRoles(object):
    """Workspace roles."""

    AlgoDeveloper = "PAI.AlgoDeveloper"
    WorkspaceAdmin = "PAI.WorkspaceAdmin"
    WorkspaceOwner = "PAI.WorkspaceOwner"
    LabelManager = "PAI.LabelManager"

    @classmethod
    def recommend_roles(cls):
        """Recommend roles for user to use."""
        return [
            cls.AlgoDeveloper,
            cls.WorkspaceAdmin,
            cls.WorkspaceOwner,
        ]


class CallerIdentityType(object):

    # Document: https://help.aliyun.com/document_detail/371868.html

    # - Account: an Alibaba Cloud account
    Account = "Account"
    # - RamUser: a RAM user
    RamUser = "RAMUser"
    # - AssumedRoleUser: a RAM role
    AssumedRoleUser = "AssumedRoleUser"


class UserProfile(object):

    _credential_client = None

    def __init__(
        self,
        credential_config: CredentialConfig,
        region_id: str,
    ):
        self.region_id = region_id
        self.credential_config = credential_config

        if DEFAULT_NETWORK_TYPE:
            self.network = Network.from_string(DEFAULT_NETWORK_TYPE)
        else:
            self.network = (
                Network.VPC
                if is_domain_connectable(PAI_VPC_ENDPOINT.format(self.region_id))
                else Network.PUBLIC
            )
        self._caller_identify = self._get_caller_identity()

    def _get_credential_client(self):
        if self._credential_client:
            return self._credential_client
        self._credential_client = CredentialClient(self.credential_config)
        return self._credential_client

    def get_access_key_id(self):
        return self._get_credential_client().get_access_key_id()

    def get_access_key_secret(self):
        return self._get_credential_client().get_access_key_secret()

    def get_security_token(self):
        return self._get_credential_client().get_security_token()

    def _get_caller_identity(self) -> CallerIdentity:
        return (
            Client(
                config=open_api_models.Config(
                    credential=self._get_credential_client(),
                    region_id=self.region_id,
                    network=(
                        None
                        if self.network == Network.PUBLIC
                        else self.network.value.lower()
                    ),
                )
            )
            .get_caller_identity()
            .body
        )

    def is_dsw_default_role(self) -> bool:
        if self._caller_identify.identity_type != CallerIdentityType.AssumedRoleUser:
            return False
        m = ASSUMED_ROLE_ARN_PATTERN.match(self._caller_identify.arn)
        return m and m.group(1).lower() == PAI_DSW_DEFAULT_ROLE_NAME

    def get_acs_dsw_client(self) -> DswClient:
        return ClientFactory.create_client(
            service_name=ServiceName.PAI_DSW,
            credential_client=self._get_credential_client(),
            region_id=self.region_id,
            network=self.network,
        )

    def get_instance_info(self, instance_id: str) -> Dict[str, Any]:
        dsw_client = self.get_acs_dsw_client()
        return dsw_client.get_instance(instance_id).body.to_map()

    def get_credential(self):
        return self._credential_client.get_access_key_id()

    @property
    def is_ram_user(self) -> bool:
        return self._caller_identify.identity_type == CallerIdentityType.RamUser

    @property
    def is_account(self) -> bool:
        return self._caller_identify.identity_type == CallerIdentityType.Account

    @property
    def account_id(self):
        """Return Alibaba Cloud account ID of the current user profile"""
        return self._caller_identify.account_id

    @property
    def user_id(self):
        """Return the Alibaba Cloud user ID of the current user profile"""
        return self._caller_identify.user_id

    @property
    def identify_type(self):
        return self._caller_identify.identity_type

    def get_default_oss_endpoint(self):
        return "https://oss-{}.aliyuncs.com".format(self.region_id)

    def list_oss_buckets(self, prefix: str = "") -> List[SimplifiedBucketInfo]:
        buckets: List[SimplifiedBucketInfo] = []
        service = oss2.Service(
            auth=oss2.ProviderAuth(
                credentials_provider=CredentialProviderWrapper(
                    config=self.credential_config,
                ),
            ),
            endpoint=self.get_default_oss_endpoint(),
        )

        marker = ""
        while True:
            res: oss2.models.ListBucketsResult = service.list_buckets(
                prefix=prefix, marker=marker
            )
            buckets.extend(
                [b for b in res.buckets if self.region_id in b.location] or []
            )
            if not res.is_truncated:
                break
            else:
                marker = res.next_marker

        return buckets

    def get_bucket_info(self, bucket_name) -> BucketInfo:
        auth = oss2.ProviderAuth(
            credentials_provider=CredentialProviderWrapper(
                config=self.credential_config,
            ),
        )
        bucket = oss2.Bucket(
            auth, self.get_default_oss_endpoint(), bucket_name=bucket_name
        )
        bucket_info = bucket.get_bucket_info()
        return bucket_info

    def create_oss_bucket(self, bucket_name):
        bucket = oss2.Bucket(
            bucket_name=bucket_name,
            auth=oss2.ProviderAuth(
                credentials_provider=CredentialProviderWrapper(
                    config=self.credential_config,
                ),
            ),
            endpoint=self.get_default_oss_endpoint(),
        )
        bucket.create_bucket()

    def get_production_authorizations(self):
        workspace_api = self.get_workspace_api()
        res = workspace_api.list_product_authorizations(
            ram_role_names=DEFAULT_PRODUCT_RAM_ROLE_NAMES
        )
        return res["AuthorizationDetails"]

    def get_workspace_api(self) -> WorkspaceAPI:
        acs_ws_client = ClientFactory.create_client(
            service_name=ServiceName.PAI_WORKSPACE,
            credential_client=self._get_credential_client(),
            region_id=self.region_id,
            network=self.network,
        )

        return WorkspaceAPI(
            acs_client=acs_ws_client,
        )

    def get_default_oss_storage_uri(
        self, workspace_id: str
    ) -> Tuple[Optional[str], Optional[str]]:
        return Session._get_default_oss_storage(
            workspace_id=workspace_id,
            cred=self._get_credential_client(),
            region_id=self.region_id,
            network=self.network,
        )

    def set_default_oss_storage(
        self, workspace_id, bucket_name: str, intranet_endpoint: str
    ):
        workspace_api = self.get_workspace_api()
        oss_uri = "oss://{}.{}/".format(bucket_name, intranet_endpoint)
        configs = {WorkspaceConfigKeys.DEFAULT_OSS_STORAGE_URI: oss_uri}
        workspace_api.update_configs(workspace_id, configs=configs)

    def get_roles_in_workspace(
        self, workspace_id, user_id: Optional[str] = None
    ) -> List[str]:
        workspace_api = self.get_workspace_api()
        user_id = user_id or self.user_id
        member_info = next(
            (
                mem
                for mem in make_list_resource_iterator(
                    workspace_api.list_members,
                    workspace_id=workspace_id,
                )
                if mem["UserId"] == user_id
            ),
            None,
        )

        # If user has PAIFullAccess policy, 'member_info' may be None.
        return member_info["Roles"] if member_info else []

    def has_permission_edit_config(self, workspace_id: str) -> bool:
        """Return True if the current user has permission to edit workspace config.

        Only members with the role of WorkspaceAdmin or WorkspaceOwner can edit
        workspace config.

        """
        roles = self.get_roles_in_workspace(workspace_id)
        return any(
            (
                r in roles
                for r in [WorkspaceRoles.WorkspaceAdmin, WorkspaceRoles.WorkspaceOwner]
            )
        )


def localized_text(en_text: str, cn_text: str = None):
    if locale_code == ZH_CN_LOCAL:
        return cn_text or en_text
    else:
        return en_text


def mask_secret(secret, mask_count=4):
    masked = (
        secret[:mask_count]
        + (len(secret) - mask_count * 2) * "*"
        + secret[-mask_count:]
    )
    return masked


def mask_and_trim(secret, max_size=20):
    masked = mask_secret(secret, mask_count=8)
    if len(masked) > max_size:
        masked = masked[:max_size] + "..."
    return masked


def radio_list_prompt(
    title: str = "",
    values=None,
    cancel_value=None,
    style=None,
    async_: bool = False,
    **kwargs,
):
    # Create the radio list
    radio_list = RadioList(values)
    # Remove the enter key binding so that we can augment it
    radio_list.control.key_bindings.remove("enter")

    bindings = KeyBindings()

    # Replace the enter key binding to select the value and also submit it
    @bindings.add("enter")
    def exit_with_value(event):
        """
        Pressing Enter will exit the user interface, returning the highlighted value.
        """
        radio_list._handle_enter()
        event.app.exit(result=radio_list.current_value)

    @bindings.add("c-c")
    def backup_exit_with_value(event):
        """
        Pressing Ctrl-C will exit the user interface with the cancel_value.
        """
        event.app.exit(result=cancel_value)

    # Create and run the mini inline application
    application = Application(
        layout=Layout(HSplit([Label(title), radio_list])),
        key_bindings=merge_key_bindings([load_key_bindings(), bindings]),
        mouse_support=True,
        style=style,
        **kwargs,
    )
    if async_:
        return application.run_async()
    else:
        return application.run()


def confirm(message: str = "Confirm?", suffix: str = " (y/n, default: y)"):
    # Input enter key returns an empty string, we assume enter is 'YES'.
    res = prompt_confirm(message, suffix)
    yes = True if isinstance(res, str) and res.strip() == "" else res
    return yes


def not_empty(text: str) -> bool:
    return bool(text.strip())


def print_highlight(msg: str):
    print(ColorEscape.green(msg))


def print_warning(msg: str):
    print(ColorEscape.red(msg))


def validate_bucket_name(name: str) -> bool:
    return bool(OSS_NAME_PATTERN.match(name))


class ColorEscape(object):
    """
    A utility class to wrap a string with color escape code.
    """

    _black = "\u001b[30m"
    _red = "\u001b[31m"
    _green = "\u001b[32m"
    _yellow = "\u001b[33m"
    _blue = "\u001b[34m"
    _magenta = "\u001b[35m"
    _cyan = "\u001b[36m"
    _white = "\u001b[37m"
    _default = "\u001b[39m"

    _reset = "\u001b[0m"

    @classmethod
    def green(cls, msg: str) -> str:
        return cls._format(msg, cls._green)

    @classmethod
    def red(cls, msg: str) -> str:
        return cls._format(msg, cls._red)

    @classmethod
    def _format(cls, msg: str, code: str) -> str:
        if os.environ.get("NO_COLOR"):
            # See https://no-color.org/
            return msg
        return code + msg + cls._reset
