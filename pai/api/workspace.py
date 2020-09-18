from __future__ import absolute_import

import six

from pai.api.base import paginate_service_call, BaseClient
from pai.libs.aliyunsdkaiworkspace.request.v20200814 import ListWorkspacesRequest, \
    GetWorkspaceRequest, UpdateWorkspaceRequest, \
    ListSubUsersRequest, ListMembersRequest, CreateMemberRequest, ListPermissionsRequest, \
    GetPermissionRequest, GetDefaultWorkspaceRequest


class WorkspaceClient(BaseClient):

    _ENV_SERVICE_ENDPOINT_KEY = 'ALIPAI_AIWORKSPACE_ENDPOINT'

    def __init__(self, acs_client):
        super(WorkspaceClient, self).__init__(acs_client=acs_client)

    def _get_endpoint(self):
        if self._endpoint:
            return self._endpoint
        return "aiworkspace.cn-shanghai.aliyuncs.com"

    def _get_product(self):
        return "AIWorkSpace"

    @paginate_service_call
    def list(self, name=None, sorted_by=None, sorted_sequence=None, page_size=None):
        request = self._construct_request(ListWorkspacesRequest.ListWorkspacesRequest)
        if name is not None:
            request.set_WorkspaceName(name)
        if sorted_by is not None:
            request.set_SortedField(sorted_by)
        if sorted_sequence is not None:
            request.set_SortedSequence(sorted_sequence)
        return request

    def get(self, workspace_id):
        request = self._construct_request(GetWorkspaceRequest.GetWorkspaceRequest)
        request.set_WorkspaceId(workspace_id)
        return self._call_service_with_exception(request)

    def update(self, workspace_id, name):
        request = self._construct_request(UpdateWorkspaceRequest.UpdateWorkspaceRequest)
        request.set_WorkspaceId(workspace_id)
        request.set_WorkspaceName(name)
        return self._call_service_with_exception(request)

    def delete_member(self, workspace_id, delete_member_ids):
        if not delete_member_ids:
            raise ValueError("Please given non-empty delete_member_ids")

        request = self._construct_request(UpdateWorkspaceRequest.UpdateWorkspaceRequest)
        if not isinstance(delete_member_ids, (list, tuple)):
            delete_member_ids = [delete_member_ids]

        request.set_WorkspaceId(workspace_id)
        request.add_body_params("DeletedMemberIds", delete_member_ids)
        return self._call_service_with_exception(request)

    def add_member(self, workspace_id, member):
        request = self._construct_request(CreateMemberRequest.CreateMemberRequest)
        if not isinstance(member, (list, tuple)):
            member = [member]

        request.set_WorkspaceId(workspace_id)
        request.add_body_params("Members", member)

        return self._call_service_with_exception(request)

    @paginate_service_call
    def list_member(self, workspace_id, name=None, role=None):
        request = self._construct_request(ListMembersRequest.ListMembersRequest)
        request.set_WorkspaceId(workspace_id)
        if name is not None:
            request.set_UserName(name)

        if role is not None and role:
            if isinstance(role, (list, tuple)):
                role = ','.join(role)
            elif not isinstance(role, six.string_types):
                raise ValueError("Required comma split roles list")
            request.set_Roles(role)
        return request

    @paginate_service_call
    def list_sub_users(self, exclude_workspace_id=None):
        request = self._construct_request(ListSubUsersRequest.ListSubUsersRequest)
        if exclude_workspace_id:
            request.set_ExcludeWorkspaceId(exclude_workspace_id)
        return request

    def list_permissions(self, workspace_id):
        request = self._construct_request(ListPermissionsRequest.ListPermissionsRequest)
        request.set_WorkspaceId(workspace_id)
        return self._call_service_with_exception(request)

    def get_permission(self, workspace_id, permission_code):
        request = self._construct_request(GetPermissionRequest.GetPermissionRequest)
        request.set_WorkspaceId(workspace_id)
        request.set_PermissionCode(permission_code)
        return self._call_service_with_exception(request)

    def get_default_workspace(self):
        request = self._construct_request(GetDefaultWorkspaceRequest.GetDefaultWorkspaceRequest)
        return self._call_service_with_exception(request)
