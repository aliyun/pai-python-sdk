import locale
import logging
import os.path
from typing import Any, Dict, List

import oss2
from oss2.models import SimplifiedBucketInfo
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator

from pai.common.oss_utils import OssUriObj
from pai.common.utils import make_list_resource_iterator, random_str
from pai.session import Session
from pai.toolkit.helper.consts import REGION_INFOS, SUPPORTED_REGION_IDS
from pai.toolkit.helper.utils import (
    UserProfile,
    WorkspaceRoles,
    confirm,
    localized_text,
    mask_secret,
    not_empty,
    print_highlight,
    print_warning,
    radio_list_prompt,
    validate_bucket_name,
)

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".pai", "config.json")
local, _ = locale.getdefaultlocale()


def prompt_for_credential():

    # Prompt for Access Key ID
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

    # Prompt for Access Key Secret
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

    region_name_map = {r["regionId"]: r["regionName"] for r in REGION_INFOS}

    region_row_format = "{:<30}{}"

    region_list = [
        (
            region_id,
            region_row_format.format(
                region_id, localized_text(*region_name_map[region_id])
            ),
        )
        for region_id in SUPPORTED_REGION_IDS
    ]

    region_id = radio_list_prompt(
        title=localized_text(
            "Please select the region where the service will be used: ",
            "请选择使用服务的地域: ",
        ),
        values=region_list,
        erase_when_done=True,
    )

    print_highlight(
        localized_text(
            "Input credential and region:",
            "当前配置的访问密钥和地域:",
        )
    )
    print_highlight(f"AccessKeyId: {access_key_id}")
    print_highlight(f"AccessKeySecret: { mask_secret(access_key_secret)}")
    print_highlight(f"RegionId: {region_id}")

    user_profile = UserProfile(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        region_id=region_id,
    )
    print_highlight(f"IdentityType: {user_profile.identify_type}")

    check_product_authorization(user_profile)
    return user_profile


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
    default_storage_uri = user_profile.get_default_oss_storage_uri(
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
            buckets: List[SimplifiedBucketInfo] = user_profile.list_oss_buckets()
            index = radio_list_prompt(
                localized_text(
                    "Please select the OSS Bucket you want to use:",
                    "请选择您需要使用的OSS Bucket：",
                ),
                values=[(idx, b.name) for idx, b in enumerate(buckets)],
                erase_when_done=True,
            )
            bucket_name = buckets[index].name

    bucket_info = user_profile.get_bucket_info(bucket_name)

    # If Workspace has no default OSS storage URI and user has permission to edit,
    # prompt to set the default OSS storage URI.
    if not default_storage_uri and user_profile.has_permission_edit_config(
        workspace_id=workspace_id
    ):
        prompt_for_set_default_oss_storage(user_profile, workspace_id, bucket_info)

    row_format = "{:<60}{}"
    endpoint = radio_list_prompt(
        localized_text(
            "Please select the Endpoint to access OSS:",
            "请选择访问OSS使用的Endpoint：",
        ),
        values=[
            (
                bucket_info.intranet_endpoint,
                row_format.format(
                    bucket_info.intranet_endpoint,
                    localized_text(
                        "Intranet endpoint,use in the PAI Notebook and ECS in the same "
                        "region. ",
                        "内网域名(请在同地域的PAI Notebook, ECS等内网环境中使用)",
                    ),
                ),
            ),
            (
                bucket_info.extranet_endpoint,
                row_format.format(
                    bucket_info.extranet_endpoint,
                    localized_text(
                        "Public endpoint",
                        "外网域名",
                    ),
                ),
            ),
        ],
        erase_when_done=True,
    )
    return bucket_name, endpoint


def prompt_for_set_default_oss_storage(
    user_profile: UserProfile, workspace_id: str, bucket_info
):
    yes_no = confirm(
        localized_text(
            "Whether config the bucket as the default storage for the Workspace?",
            "是否将当前的OSS Bucket作为工作空间的默认存储？",
        )
    )
    if yes_no:
        user_profile.set_default_oss_storage(workspace_id, bucket_info)


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
    print_highlight(f"AccessKeyId: {user_profile.access_key_id}")
    print_highlight(f"AccessKeySecret: { mask_secret(user_profile.access_key_secret)}")
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
        access_key_id=user_profile.access_key_id,
        access_key_secret=user_profile.access_key_secret,
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
