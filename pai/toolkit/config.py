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
import os.path
from enum import Enum
from typing import Any, Dict, List, Optional

import oss2
from alibabacloud_credentials.client import Client as CredentialClient
from alibabacloud_credentials.exceptions import CredentialException
from alibabacloud_credentials.models import Config as CredentialConfig
from alibabacloud_credentials.providers import (
    CredentialsUriProvider,
    EcsRamRoleCredentialProvider,
    EnvironmentVariableCredentialsProvider,
    OIDCRoleArnCredentialProvider,
    ProfileCredentialsProvider,
    RamRoleArnCredentialProvider,
    RsaKeyPairCredentialProvider,
)
from alibabacloud_credentials.utils import auth_constant
from oss2.models import SimplifiedBucketInfo
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator

from ..common.logging import get_logger
from ..common.oss_utils import OssUriObj
from ..common.utils import (
    is_domain_connectable,
    make_list_resource_iterator,
    random_str,
)
from ..session import Session
from .helper.consts import REGION_INFOS
from .helper.utils import (
    UserProfile,
    WorkspaceRoles,
    confirm,
    localized_text,
    mask_and_trim,
    mask_secret,
    not_empty,
    print_highlight,
    print_warning,
    radio_list_prompt,
    validate_bucket_name,
)

logger = get_logger(__name__)

DEFAULT_CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".pai", "config.json")
DEFAULT_CREDENTIAL_INI_PATH = os.path.join(
    os.path.expanduser("~"), ".alibabacloud", "credentials.ini"
)

REGION_ID_ENV_KEYS = [
    "ALIBABACLOUD_REGION_ID",
    "ALICLOUD_REGION_ID",
    "REGION",
    "dsw_region",
    "DSW_REGION",
]

local, _ = locale.getdefaultlocale()


CREDENTIAL_INI_TEMPLATE = """[default]
enable = true
type = access_key
access_key_id = {access_key_id}
access_key_secret = {access_key_secret}
"""


def _get_default_credential_client() -> Optional[CredentialClient]:
    try:
        return CredentialClient()
    except CredentialException:
        logger.debug("Not found credential from default credential provider chain.")


class CredentialProviderType(Enum):
    EnvironmentVariable = EnvironmentVariableCredentialsProvider
    OIDCRoleArn = OIDCRoleArnCredentialProvider
    EcsRamRole = EcsRamRoleCredentialProvider
    RamRoleArn = RamRoleArnCredentialProvider
    RsaKeyPair = RsaKeyPairCredentialProvider
    Profile = ProfileCredentialsProvider
    CredentialUri = CredentialsUriProvider

    @classmethod
    def get_current_provider(cls) -> Optional["CredentialProviderType"]:
        from alibabacloud_credentials.providers import DefaultCredentialsProvider

        d = {t.value: t for t in cls}
        provider = DefaultCredentialsProvider()
        for p in provider.user_configuration_providers:
            if p.get_credentials():
                return d.get(p.__class__)

    @classmethod
    def credential_hint(cls, cred_type: Optional["CredentialProviderType"]) -> str:
        provider_hints = {
            CredentialProviderType.EnvironmentVariable: localized_text(
                "The credential source is: Environment Variable",
                "凭证来源: 环境变量(ALIBABACLOUD_ACCESS_KEY_ID, ALIBABACLOUD_ACCESS_KEY_SECRET)",
            ),
            CredentialProviderType.OIDCRoleArn: localized_text(
                "The credential source is: OIDC Role Arn",
                "凭证来源: OIDC Role Arn",
            ),
            CredentialProviderType.EcsRamRole: localized_text(
                "The credential source is: ECS Ram Role",
                "凭证来源: ECS Ram Role",
            ),
            CredentialProviderType.RamRoleArn: localized_text(
                "The credential source is: Ram Role Arn",
                "凭证来源: Ram Role Arn",
            ),
            CredentialProviderType.RsaKeyPair: localized_text(
                "The credential source is: RSA Key Pair",
                "凭证来源: RSA Key Pair",
            ),
            CredentialProviderType.Profile: localized_text(
                "The credential source is: Profile",
                "凭证来源: Profile(~/.alibabacloud/credentials.ini)",
            ),
            CredentialProviderType.CredentialUri: localized_text(
                "The credential source is: CredentialUri (EnvironmentVairbale ALIBABA_CLOUD_CREDENTIALS_URI)",
                "凭证来源: CredentialUri (环境变量 ALIBABA_CLOUD_CREDENTIALS_URI)",
            ),
        }

        return provider_hints.get(
            cred_type,
            localized_text(
                "The credential source is: Unknown",
                "凭证来源: 未知",
            ),
        )


def prompt_for_credential():
    default_credential_client = _get_default_credential_client()
    if not default_credential_client:
        # Prompt for Access Key ID and Access Key Secret
        access_key_id = prompt(
            localized_text(
                "Please enter your Alibaba Cloud account AccessKeyId: ",
                "请输入您的阿里云账号AccessKeyId: ",
            ),
            validator=Validator.from_callable(
                validate_func=not_empty,
                error_message=localized_text(
                    "AccessKeyId can not be empty string.",
                    "AccessKeyId 不能为空",
                ),
                move_cursor_to_end=True,
            ),
        ).strip()
        access_key_secret = prompt(
            localized_text(
                "Please enter your Alibaba Cloud account AccessKeySecret: ",
                "请输入您的阿里云账号AccessKeySecret: ",
            ),
            is_password=True,
            validator=Validator.from_callable(
                validate_func=not_empty,
                error_message=localized_text(
                    "AccessKeySecret can not be empty string.",
                    "AccessKeySecret 不能为空",
                ),
                move_cursor_to_end=True,
            ),
        ).strip()
        credential_config = CredentialConfig(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type=auth_constant.ACCESS_KEY,
        )
        credential_client = CredentialClient(config=credential_config)
    else:
        # Credential chain documentation:
        # https://help.aliyun.com/zh/sdk/developer-reference/v2-manage-python-access-credentials
        print(
            localized_text(
                "Use credential from default credential provider chain:",
                "使用默认的凭证链获取访问密钥:",
            )
        )

        credential_source_hint = CredentialProviderType.credential_hint(
            CredentialProviderType.get_current_provider()
        )
        print(credential_source_hint)
        credential_client = default_credential_client
        credential_config = None

    region_id = prompt_for_region()
    print_highlight(
        localized_text(
            "The current configuration of Credential and RegionId:",
            "当前配置的访问密钥和地域:",
        )
    )

    access_key_id = credential_client.get_access_key_id()
    access_key_secret = credential_client.get_access_key_secret()
    security_token = credential_client.get_security_token()

    print_highlight(f"AccessKeyId: {access_key_id}")
    print_highlight(f"AccessKeySecret: { mask_secret(access_key_secret)}")
    if security_token:
        print_highlight(f"SecurityToken: {mask_and_trim(security_token)}")
    print_highlight(f"RegionId: {region_id}")
    user_profile = UserProfile(
        credential_config=credential_config,
        region_id=region_id,
    )
    print_highlight(f"IdentityType: {user_profile.identify_type}")

    # Write input credential to default credential config file.
    if credential_config:
        raw_config = CREDENTIAL_INI_TEMPLATE.format(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
        )
        os.makedirs(os.path.dirname(DEFAULT_CREDENTIAL_INI_PATH), exist_ok=True)
        with open(DEFAULT_CREDENTIAL_INI_PATH, "w") as f:
            f.write(raw_config)
        print(
            localized_text("Credential saved to: ", "密钥已保存至: ")
            + DEFAULT_CREDENTIAL_INI_PATH
        )

    check_product_authorization(user_profile)
    return user_profile


def prompt_for_region():
    for key in REGION_ID_ENV_KEYS:
        region_id = os.environ.get(key)
        if region_id:
            print(
                localized_text(
                    f"Config RegionId from environment variable({key}): {region_id} ",
                    f"从环境变量({key})中获取RegionId: {region_id}",
                )
            )
            return region_id

    region_name_map = {r["regionId"]: r["regionName"] for r in REGION_INFOS}
    region_row_format = "{:<30}{}"
    supported_region_ids = list(region_name_map.keys())

    region_list = [
        (
            region_id,
            region_row_format.format(
                region_id, localized_text(*region_name_map[region_id])
            ),
        )
        for region_id in supported_region_ids
    ]

    region_id = radio_list_prompt(
        title=localized_text(
            "Please select the region where the service will be used: ",
            "请选择使用服务的地域: ",
        ),
        values=region_list,
        erase_when_done=True,
    )
    return region_id


def check_product_authorization(user_profile: UserProfile):
    print(localized_text("Check Dependent Service Authorization：", "云产品依赖检查: "))
    auths = {
        auth["RamRoleName"]: auth["IsAuthorized"]
        for auth in user_profile.get_production_authorizations()
    }
    for role_name, authorized in auths.items():
        print(
            "{:<40}{}".format(
                role_name, "Authorized" if authorized else "NotAuthorized"
            )
        )


def prompt_for_workspace(user_profile: UserProfile):
    """Ask for workspace configurations."""
    workspace_api = user_profile.get_workspace_api()

    row_format = "{:<50}{}"

    def workspace_choice_name(workspace: Dict[str, Any]):
        if workspace.get("IsDefault"):
            return row_format.format(
                workspace["WorkspaceName"],
                str(workspace["WorkspaceId"]) + "  (*default)",
            )
        return row_format.format(
            workspace["WorkspaceName"],
            str(workspace["WorkspaceId"]),
        )

    items = sorted(
        [
            (item, workspace_choice_name(workspace=item))
            for item in make_list_resource_iterator(
                workspace_api.list,
                page_number=1,
                page_size=50,
            )
        ],
        key=lambda x: (x[0].get("IsDefault", False), x[0]["WorkspaceName"]),
        reverse=True,
    )
    if not items:
        if user_profile.is_account:
            raise RuntimeError(
                localized_text(
                    f"You do not have any available Workspace in the selected region ("
                    f"{user_profile.region_id}). Please create one in the region."
                    f" through the PAI console (https://pai.console.aliyun.com/).",
                    f"您在选择的Region ({user_profile.region_id}）下没有可用的工作空间，"
                    f"请通过PAI的控制台（ https://pai.console.aliyun.com/ ）创建一个工作空间。",
                )
            )
        else:
            raise RuntimeError(
                localized_text(
                    f"You do not have any available Workspace in the selected region ("
                    f"{user_profile.region_id}). Please create a new workspace or "
                    f"contact an administrator to be added to an existing workspace.",
                    f"您在选择的Region ({user_profile.region_id}) 下没有可用的工作空间，"
                    f"请创建一个新的工作空间，或是联系管理员将您添加到已有的工作空间。",
                )
            )
    else:
        header = row_format.format("WorkspaceName", "WorkspaceId")
        workspace_item = radio_list_prompt(
            localized_text(
                f"Please select the workspace you need to access:\n    {header}",
                f"请选择您需要访问的工作空间\n    {header})",
            ),
            values=items,
            erase_when_done=True,
        )

        workspace_id = workspace_item["WorkspaceId"]

    roles = user_profile.get_roles_in_workspace(workspace_id)
    role_info = ", ".join(roles)
    if not any(r for r in roles if r in WorkspaceRoles.recommend_roles()):
        print_warning(
            localized_text(
                f"We recommend using a workspace with at least developer permission. "
                f"Role in the workspace: {role_info}",
                f"建议使用至少有开发者权限的工作空间，当前工作空间角色：{role_info}",
            )
        )

    print_highlight(
        localized_text(
            "Current workspace configuration selected:",
            "当前选择的工作空间信息:",
        )
    )
    print_highlight(
        "WorkspaceName: {}\nWorkspaceId: {}\nRoles: {}".format(
            workspace_item["WorkspaceName"],
            workspace_item["WorkspaceId"],
            role_info,
        )
    )

    return workspace_id


def prompt_for_oss_bucket(user_profile: UserProfile, workspace_id: str):
    default_storage_uri, endpoint = user_profile.get_default_oss_storage_uri(
        workspace_id=workspace_id
    )
    print(
        localized_text(
            "Please configure the OSS Bucket to be used.", "请配置使用的OSS Bucket"
        )
    )
    if user_profile.is_ram_user:
        print_warning(
            localized_text(
                "Please confirm that current RAM user has been granted permission to"
                " list buckets and access the OSS Bucket that is needed.",
                "请确认当前的RAM账号 ListBuckets 权限以及 需要使用的OSS Bucket的读写权限。",
            )
        )

    bucket_name = None
    # use the default OSS storage URI configured in the Workspace.
    if default_storage_uri and confirm(
        localized_text(
            f"Do you want to use the default OSS Bucket of the current workspace"
            f" ({default_storage_uri})?",
            f"是否使用当前工作空间的默认OSS Bucket ({default_storage_uri}) ?",
        )
    ):
        bucket_name = OssUriObj(default_storage_uri).bucket_name

    if not bucket_name:
        buckets: List[SimplifiedBucketInfo] = user_profile.list_oss_buckets()
        if not buckets:
            print(
                localized_text(
                    f"You do not have any available OSS Bucket in the region"
                    f" ({user_profile.region_id}).",
                    f"您在当前Region （{user_profile.region_id}） 下没有可用的OSS Bucket。",
                )
            )
            bucket_name = prompt_for_create_oss_bucket(user_profile, workspace_id)
        else:
            index = radio_list_prompt(
                localized_text(
                    "Please select the OSS Bucket you want to use:",
                    "请选择您需要使用的OSS Bucket：",
                ),
                values=[(idx, b.name) for idx, b in enumerate(buckets)],
                erase_when_done=True,
            )
            bucket_name = buckets[index].name

    try:
        bucket_info = user_profile.get_bucket_info(bucket_name=bucket_name)
    except oss2.exceptions.AccessDenied:
        # try to get bucket info with ListBuckets API if the user has no permission to
        # GetBucketInfo API.
        buckets = user_profile.list_oss_buckets(prefix=bucket_name)
        bucket_info = next((b for b in buckets if b.name == bucket_name), None)

    if not bucket_info:
        print_warning(
            localized_text(
                "Failed to get bucket info, use default endpoint.",
                "获取 Bucket 信息失败，使用默认 Endpoint。",
            )
        )
        region_id = user_profile.region_id
        extranet_endpoint, intranet_endpoint = (
            f"oss-{region_id}.aliyuncs.com",
            f"oss-{region_id}-internal.aliyuncs.com",
        )
    else:
        extranet_endpoint, intranet_endpoint = (
            bucket_info.extranet_endpoint,
            bucket_info.intranet_endpoint,
        )

    # If Workspace has no default OSS storage URI and user has permission to edit,
    # prompt to set the default OSS storage URI.
    if not default_storage_uri and user_profile.has_permission_edit_config(
        workspace_id=workspace_id
    ):
        prompt_for_set_default_oss_storage(
            user_profile, workspace_id, bucket_name, intranet_endpoint=intranet_endpoint
        )

    row_format = "{:<60}{}"
    intra_endpoint_connectable = is_domain_connectable(intranet_endpoint, timeout=1)
    candidates = [
        (
            intranet_endpoint,
            row_format.format(
                intranet_endpoint,
                localized_text(
                    "Internal endpoint (Please use in PAI-DSW Notebook, ECS and other "
                    "intranet environment)",
                    "内网Endpoint(请在PAI-DSW Notebook, ECS等内网环境中使用)",
                ),
            ),
        ),
        (
            extranet_endpoint,
            row_format.format(
                extranet_endpoint,
                localized_text(
                    "Public endpoint",
                    "外网Endpoint",
                ),
            ),
        ),
    ]

    if not intra_endpoint_connectable:
        candidates = candidates[::-1]

    endpoint = radio_list_prompt(
        localized_text(
            "Please select the Endpoint to access OSS:",
            "请选择访问OSS使用的Endpoint：",
        ),
        values=candidates,
        erase_when_done=True,
    )
    return bucket_name, endpoint


def prompt_for_set_default_oss_storage(
    user_profile: UserProfile,
    workspace_id: str,
    bucket_name: str,
    intranet_endpoint: str,
):
    yes_no = confirm(
        localized_text(
            "Whether config the bucket as the default storage for the Workspace?",
            "是否将当前的OSS Bucket作为工作空间的默认存储？",
        )
    )
    if yes_no:
        user_profile.set_default_oss_storage(
            workspace_id, bucket_name, intranet_endpoint=intranet_endpoint
        )


def prompt_for_create_oss_bucket(user_profile: UserProfile, workspace_id):
    gen_bucket_name = f"pai-{user_profile.account_id}-{workspace_id}"

    while True:
        bucket_name = prompt(
            localized_text(
                "Please confirm the OSS Bucket name：\n",
                "请确认新建的 OSS 的 Bucket名称：\n",
            ),
            default=gen_bucket_name,
            validator=Validator.from_callable(
                validate_func=validate_bucket_name,
                error_message=localized_text(
                    "Invalid bucket name.",
                    "错误的Bucket名称.",
                ),
                move_cursor_to_end=True,
            ),
        )

        res = confirm(
            localized_text(
                f"Confirm to create the OSS Bucket. BucketName:{bucket_name}",
                f"是否使用该名称创建新的OSS Bucket。 BucketName:{bucket_name}",
            )
        )
        if not res:
            continue

        try:
            user_profile.create_oss_bucket(bucket_name)
            print_highlight(
                localized_text(
                    f"Create bucket succeeded. {bucket_name}",
                    f"Bucket创建成功. {bucket_name}",
                )
            )
            break
        except oss2.exceptions.ServerError as e:
            if e.code == "BucketAlreadyExists":
                # if bucket already exists.
                print_warning(
                    localized_text(
                        f"Bucket already exists: {bucket_name}",
                        f"当前Bucket已经被占用: {bucket_name}",
                    )
                )
                if bucket_name == gen_bucket_name:
                    gen_bucket_name = (
                        f"pai-{user_profile.account_id}-{workspace_id}-{random_str(6)}"
                    )
                continue
            raise e

    return bucket_name


def prompt_for_config_writing(
    user_profile: UserProfile,
    workspace_id,
    bucket_name,
    bucket_endpoint,
):
    # Print configuration summary.
    print_highlight(localized_text("Current configuration options:", "当前配置项:"))
    print_highlight(f"WorkspaceId: { workspace_id}")
    print_highlight(f"RegionId: {user_profile.region_id}")
    print_highlight(f"OSS Bucket Name: {bucket_name}")
    print_highlight(f"OSS Bucket Endpoint: {bucket_endpoint}")

    if os.path.exists(DEFAULT_CONFIG_PATH):
        overwrite = confirm(
            localized_text(
                f"The configuration file already exists. Do you want to overwrite the"
                f" original configuration? ({DEFAULT_CONFIG_PATH})",
                f"配置文件已经存在，是否覆盖原先配置 ({DEFAULT_CONFIG_PATH})？",
            )
        )
        if not overwrite:
            print_highlight(
                localized_text("Discard current configuration.", "放弃保存当前配置。")
            )
            return

    sess = Session(
        region_id=user_profile.region_id,
        workspace_id=workspace_id,
        oss_bucket_name=bucket_name,
        oss_endpoint=bucket_endpoint,
    )
    sess.save_config()
    print(
        localized_text(
            f"Configuration saved successfully: {DEFAULT_CONFIG_PATH}",
            f"配置保存成功: {DEFAULT_CONFIG_PATH}",
        )
    )


def prompt_config_with_default_dsw_role(user_profile: UserProfile):
    print(
        localized_text(
            "The current DSW instance is bound to the default PAI DSW role,"
            " automatically utilizes the instance's workspace and OSS Bucket configurations.",
            "当前DSW实例绑定PAI DSW默认角色，自动使用实例的工作空间和OSS Bucket配置",
        )
    )
    instance_id = os.environ.get("DSW_INSTANCE_ID")
    if not instance_id:
        raise RuntimeError(
            "Not found PAI DSW instance id from environment variable: DSW_INSTANCE_ID"
        )
    instance_info = user_profile.get_instance_info(instance_id=instance_id)
    workspace_id = instance_info["WorkspaceId"]
    workspace_name = instance_info["WorkspaceName"]
    user_id = instance_info["UserId"]
    roles = user_profile.get_roles_in_workspace(workspace_id, user_id)
    role_info = ", ".join(roles)
    print_highlight(
        localized_text(
            "Current workspace configuration:",
            "当前实例的工作空间信息:",
        )
    )
    print_highlight(
        "WorkspaceName: {}\nWorkspaceId: {}\nRoles: {}".format(
            workspace_name,
            workspace_id,
            role_info,
        )
    )

    default_storage_uri, endpoint = user_profile.get_default_oss_storage_uri(
        workspace_id=workspace_id,
    )

    if not default_storage_uri:
        print_warning(
            localized_text(
                "WARNING: The STS credential generated by the default ROLE only support accessing "
                "the default OSS Bucket storage of the workspace.\n"
                "It is not configured for the current workspace, please "
                "reference the document to configure the default OSS Bucket storage: \n"
                "https://help.aliyun.com/zh/pai/user-guide/manage-workspaces#section-afd-ntr-nwh",
                '警告：默认角色产生的STS凭证仅支持访问"工作空间默认存储"的OSS Bucket。\n'
                "当前工作空间没有配置默认OSS Bucket存储，请参考帮助文档进行配置：\n"
                "https://help.aliyun.com/zh/pai/user-guide/manage-workspaces#section-afd-ntr-nwh",
            )
        )
        bucket_name, endpoint = None, None
    else:
        bucket_name = OssUriObj(default_storage_uri).bucket_name
    return workspace_id, bucket_name, endpoint


def run():
    """
    The flow of pai config.

    1. Prompt for the basic user profile, including the AccessKey and region.
    2. Prompt for the workspace.
        2.1. If no workspace exists, raise a RuntimeError.
        2.2. List workspaces for the user to select.
    3. Prompt for the OSS Bucket.
        3.1. If the workspace has a default OSS storage, prompt whether to use the
            default one. If yes, use the default OSS Bucket, and go to 3.3.
        3.2. List Buckets for the user to select. If there are no OSS Buckets, prompt
            to create an OSS Bucket; otherwise, return the Bucket selected by the user.
        3.3. Prompt for the OSS endpoint for the Bucket.
    4. Prompt for configuration writing.

    """
    # Ask for Account profile
    user_profile = prompt_for_credential()

    if user_profile.is_dsw_default_role():
        (
            workspace_id,
            bucket_name,
            bucket_endpoint,
        ) = prompt_config_with_default_dsw_role(user_profile=user_profile)
    else:
        # Ask for workspace
        workspace_id = prompt_for_workspace(user_profile=user_profile)
        # Ask for OSS Bucket
        bucket_name, bucket_endpoint = prompt_for_oss_bucket(
            user_profile=user_profile, workspace_id=workspace_id
        )

    # Ask for config writing
    prompt_for_config_writing(
        user_profile,
        workspace_id,
        bucket_name,
        bucket_endpoint,
    )


if __name__ == "__main__":
    run()
