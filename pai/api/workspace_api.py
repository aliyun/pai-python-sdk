import typing
from typing import Any, Dict, List

from pai.api.base import ResourceAPI
from pai.common.consts import PAIServiceName
from pai.libs.alibabacloud_aiworkspace20210204.models import (
    CreateMemberRequest,
    CreateMemberRequestMembers,
    CreateMemberResponseBody,
    CreateWorkspaceRequest,
    CreateWorkspaceResponseBody,
    DeleteMembersRequest,
    GetMemberRequest,
    GetMemberResponseBody,
    GetWorkspaceRequest,
    GetWorkspaceResponseBody,
    ListMembersRequest,
    ListMembersResponseBody,
    ListWorkspacesRequest,
    ListWorkspacesResponseBody,
)

if typing.TYPE_CHECKING:
    pass


class WorkspaceAPI(ResourceAPI):

    BACKEND_SERVICE_NAME = PAIServiceName.AIWORKSPACE

    _list_method = "list_workspaces_with_options"
    _get_method = "get_workspace_with_options"
    _create_method = "create_workspace_with_options"

    _list_member_method = "list_members_with_options"
    _create_member_method = "create_member_with_options"
    _get_member_method = "get_member_with_options"
    _delete_members_method = "delete_members_with_options"
    _add_member_role_method = "add_member_role_with_options"
    _remove_member_role_method = "remove_member_role_with_options"

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
