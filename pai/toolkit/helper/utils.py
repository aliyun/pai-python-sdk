import locale
import logging
import os
import re
from typing import List

import oss2
from alibabacloud_sts20150401.client import Client
from alibabacloud_sts20150401.models import (
    GetCallerIdentityResponseBody as CallerIdentity,
)
from alibabacloud_tea_openapi import models as open_api_models
from oss2.models import SimplifiedBucketInfo
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.layout import HSplit, Layout
from prompt_toolkit.shortcuts import confirm as prompt_confirm
from prompt_toolkit.widgets import Label, RadioList

from pai.api.base import PAIServiceName
from pai.api.client_factory import ClientFactory
from pai.api.workspace import WorkspaceAPI, WorkspaceConfigKeys
from pai.common.oss_utils import OssUriObj
from pai.common.utils import make_list_resource_iterator

logger = logging.getLogger(__name__)

locale_code, _ = locale.getdefaultlocale()

OSS_NAME_PATTERN = re.compile(pattern="^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$")
ZH_CN_LOCAL = "zh_CN"

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
    def __init__(
        self,
        access_key_id: str,
        access_key_secret: str,
        region_id: str,
    ):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.region_id = region_id
        self._caller_identify = self._get_caller_identity()

    def _get_caller_identity(self) -> CallerIdentity:
        return (
            Client(
                config=open_api_models.Config(
                    access_key_id=self.access_key_id,
                    access_key_secret=self.access_key_secret,
                    region_id=self.region_id,
                )
            )
            .get_caller_identity()
            .body
        )

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

    def list_oss_buckets(self):
        buckets: List[SimplifiedBucketInfo] = []
        service = oss2.Service(
            auth=oss2.Auth(
                access_key_id=self.access_key_id,
                access_key_secret=self.access_key_secret,
            ),
            endpoint=self.get_default_oss_endpoint(),
        )

        marker = ""
        while True:
            res: oss2.models.ListBucketsResult = service.list_buckets(marker=marker)
            buckets.extend(
                [b for b in res.buckets if self.region_id in b.location] or []
            )
            if not res.is_truncated:
                break
            else:
                marker = res.next_marker

        return buckets

    def get_bucket_info(self, bucket_name):
        service = oss2.Service(
            auth=oss2.Auth(
                access_key_id=self.access_key_id,
                access_key_secret=self.access_key_secret,
            ),
            endpoint=self.get_default_oss_endpoint(),
        )
        res: oss2.models.ListBucketsResult = service.list_buckets(prefix=bucket_name)
        bucket_info = next((b for b in res.buckets if b.name == bucket_name), None)
        if not bucket_info:
            raise ValueError(
                f"Not found bucket with the specific name: bucket_name={bucket_name}"
            )

        return bucket_info

    def create_oss_bucket(self, bucket_name):
        bucket = oss2.Bucket(
            bucket_name=bucket_name,
            auth=oss2.Auth(
                access_key_id=self.access_key_id,
                access_key_secret=self.access_key_secret,
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
            service_name=PAIServiceName.AIWORKSPACE,
            access_key_id=self.access_key_id,
            access_key_secret=self.access_key_secret,
            region_id=self.region_id,
        )

        return WorkspaceAPI(
            acs_client=acs_ws_client,
        )

    def get_default_oss_storage_uri(self, workspace_id: str):
        workspace_api = self.get_workspace_api()
        resp = workspace_api.list_configs(
            workspace_id=workspace_id,
            config_keys=WorkspaceConfigKeys.DEFAULT_OSS_STORAGE_URI,
        )

        oss_storage_uri = next(
            (
                item["ConfigValue"]
                for item in resp["Configs"]
                if item["ConfigKey"] == WorkspaceConfigKeys.DEFAULT_OSS_STORAGE_URI
            ),
            None,
        )
        if not oss_storage_uri:
            return

        uri_obj = OssUriObj(oss_storage_uri)
        return "oss://{}".format(uri_obj.bucket_name)

    def set_default_oss_storage(self, workspace_id, bucket_info: SimplifiedBucketInfo):
        workspace_api = self.get_workspace_api()
        oss_uri = "oss://{}.{}/".format(bucket_info.name, bucket_info.intranet_endpoint)
        configs = {WorkspaceConfigKeys.DEFAULT_OSS_STORAGE_URI: oss_uri}
        workspace_api.update_configs(workspace_id, configs=configs)

    def get_roles_in_workspace(self, workspace_id) -> List[str]:
        workspace_api = self.get_workspace_api()
        member_info = next(
            (
                mem
                for mem in make_list_resource_iterator(
                    workspace_api.list_members,
                    workspace_id=workspace_id,
                )
                if mem["UserId"] == self.user_id
            ),
            None,
        )

        return member_info["Roles"]

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


def mask_secret(secret):
    masked = secret[:4] + (len(secret) - 8) * "*" + secret[-4:]
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
