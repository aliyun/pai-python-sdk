# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import unicode_literals

from Tea.converter import TeaConverter

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient

from pai.libs.alibabacloud_aiworkspace20210204 import models as aiwork_space_20210204_models


class Client(OpenApiClient):
    """
    *\
    """
    def __init__(self, config):
        super(Client, self).__init__(config)
        self._endpoint_rule = ''
        self.check_config(config)
        self._endpoint = self.get_endpoint('aiworkspace', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

    def get_endpoint(self, product_id, region_id, endpoint_rule, network, suffix, endpoint_map, endpoint):
        if not UtilClient.empty(endpoint):
            return endpoint
        if not UtilClient.is_unset(endpoint_map) and not UtilClient.empty(endpoint_map.get(region_id)):
            return endpoint_map.get(region_id)
        return EndpointUtilClient.get_endpoint_rules(product_id, region_id, endpoint_rule, network, suffix)

    def add_member_role(self, workspace_id, member_id, role_name):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.add_member_role_with_options(workspace_id, member_id, role_name, headers, runtime)

    def add_member_role_with_options(self, workspace_id, member_id, role_name, headers, runtime):
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='AddMemberRole',
            version='2021-02-04',
            protocol='HTTPS',
            pathname='/api/v1/workspaces/%s/members/{MemberId}/roles/{RoleName}' % TeaConverter.to_unicode(workspace_id),
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return aiwork_space_20210204_models.AddMemberRoleResponse().from_map(
            self.call_api(params, req, runtime)
        )

    def add_workspace_quota(self, workspace_id, quota_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.add_workspace_quota_with_options(workspace_id, quota_id, request, headers, runtime)

    def add_workspace_quota_with_options(self, workspace_id, quota_id, request, headers, runtime):
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.quota_type):
            body['QuotaType'] = request.quota_type
        if not UtilClient.is_unset(request.mode):
            body['Mode'] = request.mode
        if not UtilClient.is_unset(request.product_code):
            body['ProductCode'] = request.product_code
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='AddWorkspaceQuota',
            version='2021-02-04',
            protocol='HTTPS',
            pathname='/api/v1/workspaces/[WorkspaceId]/quotas/[QuotaId]',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return aiwork_space_20210204_models.AddWorkspaceQuotaResponse().from_map(
            self.call_api(params, req, runtime)
        )

    def create_member(self, workspace_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_member_with_options(workspace_id, request, headers, runtime)

    def create_member_with_options(self, workspace_id, request, headers, runtime):
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.members):
            body['Members'] = request.members
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateMember',
            version='2021-02-04',
            protocol='HTTPS',
            pathname='/api/v1/workspaces/%s/members' % TeaConverter.to_unicode(workspace_id),
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return aiwork_space_20210204_models.CreateMemberResponse().from_map(
            self.call_api(params, req, runtime)
        )

    def create_workspace(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_workspace_with_options(request, headers, runtime)

    def create_workspace_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.workspace_name):
            body['WorkspaceName'] = request.workspace_name
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.display_name):
            body['DisplayName'] = request.display_name
        if not UtilClient.is_unset(request.env_types):
            body['EnvTypes'] = request.env_types
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateWorkspace',
            version='2021-02-04',
            protocol='HTTPS',
            pathname='/api/v1/workspaces',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return aiwork_space_20210204_models.CreateWorkspaceResponse().from_map(
            self.call_api(params, req, runtime)
        )

    def create_workspace_resource(self, workspace_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_workspace_resource_with_options(workspace_id, request, headers, runtime)

    def create_workspace_resource_with_options(self, workspace_id, request, headers, runtime):
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.resources):
            body['Resources'] = request.resources
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateWorkspaceResource',
            version='2021-02-04',
            protocol='HTTPS',
            pathname='/api/v1/workspaces/%s/resources' % TeaConverter.to_unicode(workspace_id),
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return aiwork_space_20210204_models.CreateWorkspaceResourceResponse().from_map(
            self.call_api(params, req, runtime)
        )

    def delete_members(self, workspace_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_members_with_options(workspace_id, request, headers, runtime)

    def delete_members_with_options(self, workspace_id, request, headers, runtime):
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.member_ids):
            query['MemberIds'] = request.member_ids
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteMembers',
            version='2021-02-04',
            protocol='HTTPS',
            pathname='/api/v1/workspaces/%s/members' % TeaConverter.to_unicode(workspace_id),
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return aiwork_space_20210204_models.DeleteMembersResponse().from_map(
            self.call_api(params, req, runtime)
        )

    def get_permission(self, workspace_id, permission_code):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_permission_with_options(workspace_id, permission_code, headers, runtime)

    def get_permission_with_options(self, workspace_id, permission_code, headers, runtime):
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetPermission',
            version='2021-02-04',
            protocol='HTTPS',
            pathname='/api/v1/workspaces/%s/permissions/{PermissionCode}' % TeaConverter.to_unicode(workspace_id),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return aiwork_space_20210204_models.GetPermissionResponse().from_map(
            self.call_api(params, req, runtime)
        )

    def get_role_statistics(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_role_statistics_with_options(request, headers, runtime)

    def get_role_statistics_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetRoleStatistics',
            version='2021-02-04',
            protocol='HTTPS',
            pathname='/api/v1/statistics/roles',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return aiwork_space_20210204_models.GetRoleStatisticsResponse().from_map(
            self.call_api(params, req, runtime)
        )

    def get_workspace(self, workspace_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_workspace_with_options(workspace_id, headers, runtime)

    def get_workspace_with_options(self, workspace_id, headers, runtime):
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetWorkspace',
            version='2021-02-04',
            protocol='HTTPS',
            pathname='/api/v1/workspaces/%s' % TeaConverter.to_unicode(workspace_id),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return aiwork_space_20210204_models.GetWorkspaceResponse().from_map(
            self.call_api(params, req, runtime)
        )

    def list_members(self, workspace_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_members_with_options(workspace_id, request, headers, runtime)

    def list_members_with_options(self, workspace_id, request, headers, runtime):
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.roles):
            query['Roles'] = request.roles
        if not UtilClient.is_unset(request.member_name):
            query['MemberName'] = request.member_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListMembers',
            version='2021-02-04',
            protocol='HTTPS',
            pathname='/api/v1/workspaces/%s/members' % TeaConverter.to_unicode(workspace_id),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return aiwork_space_20210204_models.ListMembersResponse().from_map(
            self.call_api(params, req, runtime)
        )

    def list_operation_logs(self, workspace_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_operation_logs_with_options(workspace_id, request, headers, runtime)

    def list_operation_logs_with_options(self, workspace_id, request, headers, runtime):
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.entity_types):
            query['EntityTypes'] = request.entity_types
        if not UtilClient.is_unset(request.operations):
            query['Operations'] = request.operations
        if not UtilClient.is_unset(request.operation_status):
            query['OperationStatus'] = request.operation_status
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.entity_status):
            query['EntityStatus'] = request.entity_status
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListOperationLogs',
            version='2021-02-04',
            protocol='HTTPS',
            pathname='/api/v1/workspaces/%s/logs' % TeaConverter.to_unicode(workspace_id),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return aiwork_space_20210204_models.ListOperationLogsResponse().from_map(
            self.call_api(params, req, runtime)
        )

    def list_permissions(self, workspace_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_permissions_with_options(workspace_id, headers, runtime)

    def list_permissions_with_options(self, workspace_id, headers, runtime):
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='ListPermissions',
            version='2021-02-04',
            protocol='HTTPS',
            pathname='/api/v1/workspaces/%s/permissions' % TeaConverter.to_unicode(workspace_id),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return aiwork_space_20210204_models.ListPermissionsResponse().from_map(
            self.call_api(params, req, runtime)
        )

    def list_products(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_products_with_options(request, headers, runtime)

    def list_products_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.product_codes):
            query['ProductCodes'] = request.product_codes
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListProducts',
            version='2021-02-04',
            protocol='HTTPS',
            pathname='/api/v1/products',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return aiwork_space_20210204_models.ListProductsResponse().from_map(
            self.call_api(params, req, runtime)
        )

    def list_quotas(self):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_quotas_with_options(headers, runtime)

    def list_quotas_with_options(self, headers, runtime):
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='ListQuotas',
            version='2021-02-04',
            protocol='HTTPS',
            pathname='/api/v1/quotas',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return aiwork_space_20210204_models.ListQuotasResponse().from_map(
            self.call_api(params, req, runtime)
        )

    def list_resources(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_resources_with_options(request, headers, runtime)

    def list_resources_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.product_types):
            query['ProductTypes'] = request.product_types
        if not UtilClient.is_unset(request.resource_group_name):
            query['ResourceGroupName'] = request.resource_group_name
        if not UtilClient.is_unset(request.resource_name):
            query['ResourceName'] = request.resource_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListResources',
            version='2021-02-04',
            protocol='HTTPS',
            pathname='/api/v1/resources',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return aiwork_space_20210204_models.ListResourcesResponse().from_map(
            self.call_api(params, req, runtime)
        )

    def list_workspaces(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_workspaces_with_options(request, headers, runtime)

    def list_workspaces_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.workspace_name):
            query['WorkspaceName'] = request.workspace_name
        if not UtilClient.is_unset(request.module_list):
            query['ModuleList'] = request.module_list
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        if not UtilClient.is_unset(request.option):
            query['Option'] = request.option
        if not UtilClient.is_unset(request.verbose):
            query['Verbose'] = request.verbose
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWorkspaces',
            version='2021-02-04',
            protocol='HTTPS',
            pathname='/api/v1/workspaces',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return aiwork_space_20210204_models.ListWorkspacesResponse().from_map(
            self.call_api(params, req, runtime)
        )

    def list_workspace_users(self, workspace_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_workspace_users_with_options(workspace_id, headers, runtime)

    def list_workspace_users_with_options(self, workspace_id, headers, runtime):
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='ListWorkspaceUsers',
            version='2021-02-04',
            protocol='HTTPS',
            pathname='/api/v1/workspaces/%s/users' % TeaConverter.to_unicode(workspace_id),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return aiwork_space_20210204_models.ListWorkspaceUsersResponse().from_map(
            self.call_api(params, req, runtime)
        )

    def remove_member_role(self, workspace_id, member_id, role_name):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.remove_member_role_with_options(workspace_id, member_id, role_name, headers, runtime)

    def remove_member_role_with_options(self, workspace_id, member_id, role_name, headers, runtime):
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='RemoveMemberRole',
            version='2021-02-04',
            protocol='HTTPS',
            pathname='/api/v1/workspaces/%s/members/{MemberId}/roles/{RoleName}' % TeaConverter.to_unicode(workspace_id),
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return aiwork_space_20210204_models.RemoveMemberRoleResponse().from_map(
            self.call_api(params, req, runtime)
        )

    def remove_workspace_quota(self, workspace_id, quota_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.remove_workspace_quota_with_options(workspace_id, quota_id, headers, runtime)

    def remove_workspace_quota_with_options(self, workspace_id, quota_id, headers, runtime):
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='RemoveWorkspaceQuota',
            version='2021-02-04',
            protocol='HTTPS',
            pathname='/api/v1/workspaces/%s/quotas/{QuotaId}' % TeaConverter.to_unicode(workspace_id),
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return aiwork_space_20210204_models.RemoveWorkspaceQuotaResponse().from_map(
            self.call_api(params, req, runtime)
        )

    def update_workspace(self, workspace_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_workspace_with_options(workspace_id, request, headers, runtime)

    def update_workspace_with_options(self, workspace_id, request, headers, runtime):
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.display_name):
            body['DisplayName'] = request.display_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateWorkspace',
            version='2021-02-04',
            protocol='HTTPS',
            pathname='/api/v1/workspaces/%s' % TeaConverter.to_unicode(workspace_id),
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return aiwork_space_20210204_models.UpdateWorkspaceResponse().from_map(
            self.call_api(params, req, runtime)
        )

    def update_workspace_resource(self, workspace_id, resource_group_name, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_workspace_resource_with_options(workspace_id, resource_group_name, request, headers, runtime)

    def update_workspace_resource_with_options(self, workspace_id, resource_group_name, request, headers, runtime):
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.is_default):
            body['IsDefault'] = request.is_default
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateWorkspaceResource',
            version='2021-02-04',
            protocol='HTTPS',
            pathname='/api/v1/workspaces/%s/resources/{ResourceGroupName}' % TeaConverter.to_unicode(workspace_id),
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return aiwork_space_20210204_models.UpdateWorkspaceResourceResponse().from_map(
            self.call_api(params, req, runtime)
        )
