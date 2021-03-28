from __future__ import absolute_import

import six

from pai.api.base import paginate_service_call, BaseClient, BaseTeaClient
from pai.libs.alibabacloud_aiworkspace20210204.models import (
    ListWorkspacesRequest,
    ListResourcesRequest,
    ListMembersRequest,
    ListProductsRequest,
    ListOperationLogsRequest,
    CreateWorkspaceRequest,
    CreateWorkspaceResourceRequest,
    CreateMemberRequest,
    DeleteMembersRequest,
)


class WorkspaceClient(BaseTeaClient):

    _ENV_SERVICE_ENDPOINT_KEY = "ALIPAI_AIWORKSPACE_ENDPOINT"

    def __init__(self, base_client):
        super(WorkspaceClient, self).__init__(base_client=base_client)

    def list_workspace(
        self,
        page_number=None,
        page_size=None,
        sort_by=None,
        order=None,
        workspace_name=None,
        module_list=None,
        status=None,
        option=None,
        verbose=None,
    ):
        request = ListWorkspacesRequest(
            page_number=page_number,
            page_size=page_size,
            sort_by=sort_by,
            order=order,
            workspace_name=workspace_name,
            module_list=module_list,
            status=status,
            option=option,
            verbose=verbose,
        )

        resp = self._call_service_with_exception(
            self.base_client.list_workspaces, request=request
        ).to_map()

        workspaces, total_count = resp["Workspaces"], resp["TotalCount"]
        return workspaces, total_count

    def list_workspace_generator(
        self,
        page_number=None,
        page_size=None,
        sort_by=None,
        order=None,
        workspace_name=None,
        module_list=None,
        status=None,
        option=None,
        verbose=None,
    ):
        return type(self).to_generator(self.list_workspace)(
            page_number=page_number,
            page_size=page_size,
            sort_by=sort_by,
            order=order,
            workspace_name=workspace_name,
            module_list=module_list,
            status=status,
            option=option,
            verbose=verbose,
        )

    def _get_endpoint(self):
        if self._endpoint:
            return self._endpoint
        elif self._inner:
            return "aiworkspaceinner-inner.aliyuncs.com"
        else:
            return "aiworkspace.{region_id}.aliyuncs.com".format(
                region_id=self.region_id
            )

    def _get_product(self):
        return "AIWorkSpace"

    def create(self, name, display_name=None, description=None, env_types=None):
        request = CreateWorkspaceRequest(
            workspace_name=name,
            description=description,
            display_name=display_name,
            env_types=None,
        )

        resp = self._call_service_with_exception(
            self.base_client.create_workspace, request=request
        )
        return resp.to_map()

    def get_workspace(self, workspace_id):
        resp = self.base_client.get_workspace(workspace_id)
        return resp.body.to_map()

    def update(self, workspace_id, name):
        raise NotImplementedError

    def delete_member(self, workspace_id, delete_member_ids):
        raise NotImplementedError

    def add_member(self, workspace_id, member):
        raise NotImplementedError

    def list_member(self, workspace_id, name=None, role=None):
        raise NotImplementedError

    def list_sub_users(self, exclude_workspace_id=None):
        raise NotImplementedError

    def list_permissions(self, workspace_id):
        raise NotImplementedError

    def get_permission(self, workspace_id, permission_code):
        raise NotImplementedError

    def create_tenant(self):
        raise NotImplementedError

    def get_tenant(self):
        raise NotImplementedError

    def add_compute_engine(self, workspace_id):
        raise NotImplementedError

    def list_compute_engines(self, name, workspace_id, engine_type="PAI", **kwargs):
        raise NotImplementedError

    def list_resource_groups(self, tenant_id):
        raise NotImplementedError

    def list_commodities(self):
        raise NotImplementedError
