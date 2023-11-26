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

import typing
from typing import Any, Dict, List, Union

from ..libs.alibabacloud_aiworkspace20210204.models import (
    CreateMemberRequest,
    CreateMemberRequestMembers,
    CreateMemberResponseBody,
    CreateWorkspaceRequest,
    CreateWorkspaceResponseBody,
    DeleteMembersRequest,
    GetDefaultWorkspaceRequest,
    GetDefaultWorkspaceResponseBody,
    GetMemberRequest,
    GetMemberResponseBody,
    GetWorkspaceRequest,
    GetWorkspaceResponseBody,
    ListConfigsRequest,
    ListConfigsResponseBody,
    ListMembersRequest,
    ListMembersResponseBody,
    ListProductAuthorizationsRequest,
    ListProductAuthorizationsResponseBody,
    ListWorkspacesRequest,
    ListWorkspacesResponseBody,
    UpdateConfigsRequest,
    UpdateConfigsRequestConfigs,
)
from .base import ResourceAPI, ServiceName

if typing.TYPE_CHECKING:
    pass


class WorkspaceConfigKeys(object):

    DEFAULT_OSS_STORAGE_URI = "modelExportPath"
    MAXCOMPUTE_TEMP_TABLE_LIFECYCLE = "tempTableLifecycle"


class WorkspaceAPI(ResourceAPI):

    BACKEND_SERVICE_NAME = ServiceName.PAI_WORKSPACE

    _list_method = "list_workspaces_with_options"
    _get_method = "get_workspace_with_options"
    _create_method = "create_workspace_with_options"
    _get_default_workspace_method = "get_default_workspace_with_options"
    _list_configs_method = "list_configs_with_options"
    _update_configs_method = "update_configs_with_options"

    _list_member_method = "list_members_with_options"
    _create_member_method = "create_member_with_options"
    _get_member_method = "get_member_with_options"
    _delete_members_method = "delete_members_with_options"
    _add_member_role_method = "add_member_role_with_options"
    _remove_member_role_method = "remove_member_role_with_options"
    _list_product_authorizations_method = "list_product_authorizations_with_options"

    def list(
        self,
        page_number=None,
        page_size=None,
        sort_by=None,
        order=None,
        name=None,
        module_list=None,
        status=None,
        option=None,
        verbose=None,
    ) -> List[Dict[str, Any]]:
        request = ListWorkspacesRequest(
            page_number=page_number,
            page_size=page_size,
            sort_by=sort_by,
            order=order,
            workspace_name=name,
            module_list=module_list,
            status=status,
            option=option,
            verbose=verbose,
        )
        res: ListWorkspacesResponseBody = self._do_request(
            method_=self._list_method, request=request
        )

        return [item.to_map() for item in res.workspaces]

    def get(self, workspace_id: str, verbose: bool = True) -> Dict[str, Any]:
        request = GetWorkspaceRequest(verbose=verbose)

        res: GetWorkspaceResponseBody = self._do_request(
            method_=self._get_method,
            workspace_id=workspace_id,
            request=request,
        )
        return res.to_map()

    def create(
        self,
        name: str,
        display_name: str = None,
        description: str = None,
        env_types: List[str] = None,
    ) -> str:
        request = CreateWorkspaceRequest(
            description=description,
            display_name=display_name,
            workspace_name=name,
            env_types=env_types,
        )

        res: CreateWorkspaceResponseBody = self._do_request(
            method_=self._create_method, request=request
        )
        return res.workspace_id

    def list_members(
        self,
        workspace_id: str,
        member_name: str = None,
        roles: List[str] = None,
        page_number: int = None,
        page_size: int = None,
    ) -> List[Dict[str, Any]]:
        request = ListMembersRequest(
            member_name=member_name,
            page_number=page_number,
            page_size=page_size,
            roles=roles,
        )

        res: ListMembersResponseBody = self._do_request(
            method_=self._list_member_method,
            workspace_id=workspace_id,
            request=request,
        )
        return [item.to_map() for item in res.members]

    def add_member(self, workspace_id: str, user_id: str, roles: List[str]) -> str:
        request = CreateMemberRequest(
            members=[
                CreateMemberRequestMembers(
                    user_id=user_id,
                    roles=roles,
                )
            ],
        )

        res: CreateMemberResponseBody = self._do_request(
            method_=self._create_member_method,
            workspace_id=workspace_id,
            request=request,
        )
        return res.members[0].member_id

    def get_member(self, workspace_id: str, user_id: str) -> Dict[str, Any]:
        request = GetMemberRequest(user_id=user_id)

        res: GetMemberResponseBody = self._do_request(
            method_=self._get_member_method, workspace_id=workspace_id, request=request
        )
        return res.to_map()

    def delete_members(self, workspace_id: str, member_ids: List[str]) -> None:
        request = DeleteMembersRequest(
            member_ids=member_ids,
        )
        self._do_request(
            method_=self._delete_members_method,
            workspace_id=workspace_id,
            request=request,
        )

    def add_member_role(
        self, workspace_id: str, member_id: str, role_name: str
    ) -> None:
        self._do_request(
            method_=self._add_member_role_method,
            workspace_id=workspace_id,
            member_id=member_id,
            role_name=role_name,
        )

    def remove_member_role(
        self, workspace_id: str, member_id: str, role_name: str
    ) -> None:
        self._do_request(
            method_=self._remove_member_role_method,
            workspace_id=workspace_id,
            member_id=member_id,
            role_name=role_name,
        )

    def get_default_workspace(self) -> Dict[str, Any]:
        """Get the default workspace for the account."""
        request = GetDefaultWorkspaceRequest()
        resp: GetDefaultWorkspaceResponseBody = self._do_request(
            method_=self._get_default_workspace_method, request=request
        )
        return resp.to_map()

    def list_configs(self, workspace_id, config_keys: Union[List[str], str]) -> Dict:
        """List configs used in the Workspace."""
        request = ListConfigsRequest(
            config_keys=",".join(config_keys)
            if isinstance(config_keys, (tuple, list))
            else config_keys,
        )

        resp: ListConfigsResponseBody = self._do_request(
            method_=self._list_configs_method,
            workspace_id=workspace_id,
            request=request,
        )
        return resp.to_map()

    def get_default_storage_uri(self, workspace_id):
        resp = self.list_configs(
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
        return oss_storage_uri

    def update_configs(self, workspace_id: str, configs: Union[Dict, List]):
        """Update configs used in the Workspace."""
        if isinstance(configs, Dict):
            configs = [
                UpdateConfigsRequestConfigs(
                    config_key=key,
                    config_value=value,
                )
                for key, value in configs.items()
            ]
        else:
            configs = [UpdateConfigsRequestConfigs.from_map(item) for item in configs]
        request = UpdateConfigsRequest(configs=configs)

        self._do_request(
            method_=self._update_configs_method,
            workspace_id=workspace_id,
            request=request,
        )

    def list_product_authorizations(self, ram_role_names: List[str]) -> Dict[str, Any]:
        request = ListProductAuthorizationsRequest(
            ram_role_names=",".join(ram_role_names)
        )

        res: ListProductAuthorizationsResponseBody = self._do_request(
            self._list_product_authorizations_method, request
        )

        return res.to_map()
