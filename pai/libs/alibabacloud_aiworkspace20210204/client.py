# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from typing import Dict
from Tea.core import TeaCore

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient
from pai.libs.alibabacloud_aiworkspace20210204 import models as aiwork_space_20210204_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient


class Client(OpenApiClient):
    """
    *\
    """
    def __init__(
        self, 
        config: open_api_models.Config,
    ):
        super().__init__(config)
        self._endpoint_rule = ''
        self.check_config(config)
        self._endpoint = self.get_endpoint('aiworkspace', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

    def get_endpoint(
        self,
        product_id: str,
        region_id: str,
        endpoint_rule: str,
        network: str,
        suffix: str,
        endpoint_map: Dict[str, str],
        endpoint: str,
    ) -> str:
        if not UtilClient.empty(endpoint):
            return endpoint
        if not UtilClient.is_unset(endpoint_map) and not UtilClient.empty(endpoint_map.get(region_id)):
            return endpoint_map.get(region_id)
        return EndpointUtilClient.get_endpoint_rules(product_id, region_id, endpoint_rule, network, suffix)

    def add_image_with_options(
        self,
        request: aiwork_space_20210204_models.AddImageRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.AddImageResponse:
        """
        @summary 增加 Image
        
        @param request: AddImageRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: AddImageResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.accessibility):
            body['Accessibility'] = request.accessibility
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.image_id):
            body['ImageId'] = request.image_id
        if not UtilClient.is_unset(request.image_uri):
            body['ImageUri'] = request.image_uri
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.size):
            body['Size'] = request.size
        if not UtilClient.is_unset(request.workspace_id):
            body['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='AddImage',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/images',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.AddImageResponse(),
            self.call_api(params, req, runtime)
        )

    async def add_image_with_options_async(
        self,
        request: aiwork_space_20210204_models.AddImageRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.AddImageResponse:
        """
        @summary 增加 Image
        
        @param request: AddImageRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: AddImageResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.accessibility):
            body['Accessibility'] = request.accessibility
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.image_id):
            body['ImageId'] = request.image_id
        if not UtilClient.is_unset(request.image_uri):
            body['ImageUri'] = request.image_uri
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.size):
            body['Size'] = request.size
        if not UtilClient.is_unset(request.workspace_id):
            body['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='AddImage',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/images',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.AddImageResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def add_image(
        self,
        request: aiwork_space_20210204_models.AddImageRequest,
    ) -> aiwork_space_20210204_models.AddImageResponse:
        """
        @summary 增加 Image
        
        @param request: AddImageRequest
        @return: AddImageResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.add_image_with_options(request, headers, runtime)

    async def add_image_async(
        self,
        request: aiwork_space_20210204_models.AddImageRequest,
    ) -> aiwork_space_20210204_models.AddImageResponse:
        """
        @summary 增加 Image
        
        @param request: AddImageRequest
        @return: AddImageResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.add_image_with_options_async(request, headers, runtime)

    def add_image_labels_with_options(
        self,
        image_id: str,
        request: aiwork_space_20210204_models.AddImageLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.AddImageLabelsResponse:
        """
        @summary 增加 Image 的标签
        
        @param request: AddImageLabelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: AddImageLabelsResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='AddImageLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/images/{OpenApiUtilClient.get_encode_param(image_id)}/labels',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.AddImageLabelsResponse(),
            self.call_api(params, req, runtime)
        )

    async def add_image_labels_with_options_async(
        self,
        image_id: str,
        request: aiwork_space_20210204_models.AddImageLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.AddImageLabelsResponse:
        """
        @summary 增加 Image 的标签
        
        @param request: AddImageLabelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: AddImageLabelsResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='AddImageLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/images/{OpenApiUtilClient.get_encode_param(image_id)}/labels',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.AddImageLabelsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def add_image_labels(
        self,
        image_id: str,
        request: aiwork_space_20210204_models.AddImageLabelsRequest,
    ) -> aiwork_space_20210204_models.AddImageLabelsResponse:
        """
        @summary 增加 Image 的标签
        
        @param request: AddImageLabelsRequest
        @return: AddImageLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.add_image_labels_with_options(image_id, request, headers, runtime)

    async def add_image_labels_async(
        self,
        image_id: str,
        request: aiwork_space_20210204_models.AddImageLabelsRequest,
    ) -> aiwork_space_20210204_models.AddImageLabelsResponse:
        """
        @summary 增加 Image 的标签
        
        @param request: AddImageLabelsRequest
        @return: AddImageLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.add_image_labels_with_options_async(image_id, request, headers, runtime)

    def add_member_role_with_options(
        self,
        workspace_id: str,
        member_id: str,
        role_name: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.AddMemberRoleResponse:
        """
        @summary 增加成员角色
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: AddMemberRoleResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='AddMemberRole',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/members/{OpenApiUtilClient.get_encode_param(member_id)}/roles/{OpenApiUtilClient.get_encode_param(role_name)}',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.AddMemberRoleResponse(),
            self.call_api(params, req, runtime)
        )

    async def add_member_role_with_options_async(
        self,
        workspace_id: str,
        member_id: str,
        role_name: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.AddMemberRoleResponse:
        """
        @summary 增加成员角色
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: AddMemberRoleResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='AddMemberRole',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/members/{OpenApiUtilClient.get_encode_param(member_id)}/roles/{OpenApiUtilClient.get_encode_param(role_name)}',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.AddMemberRoleResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def add_member_role(
        self,
        workspace_id: str,
        member_id: str,
        role_name: str,
    ) -> aiwork_space_20210204_models.AddMemberRoleResponse:
        """
        @summary 增加成员角色
        
        @return: AddMemberRoleResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.add_member_role_with_options(workspace_id, member_id, role_name, headers, runtime)

    async def add_member_role_async(
        self,
        workspace_id: str,
        member_id: str,
        role_name: str,
    ) -> aiwork_space_20210204_models.AddMemberRoleResponse:
        """
        @summary 增加成员角色
        
        @return: AddMemberRoleResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.add_member_role_with_options_async(workspace_id, member_id, role_name, headers, runtime)

    def add_workspace_quota_with_options(
        self,
        workspace_id: str,
        quota_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.AddWorkspaceQuotaResponse:
        """
        @summary 添加资源实例配额
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: AddWorkspaceQuotaResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='AddWorkspaceQuota',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/%5BWorkspaceId%5D/quotas/%5BQuotaId%5D',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.AddWorkspaceQuotaResponse(),
            self.call_api(params, req, runtime)
        )

    async def add_workspace_quota_with_options_async(
        self,
        workspace_id: str,
        quota_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.AddWorkspaceQuotaResponse:
        """
        @summary 添加资源实例配额
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: AddWorkspaceQuotaResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='AddWorkspaceQuota',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/%5BWorkspaceId%5D/quotas/%5BQuotaId%5D',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.AddWorkspaceQuotaResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def add_workspace_quota(
        self,
        workspace_id: str,
        quota_id: str,
    ) -> aiwork_space_20210204_models.AddWorkspaceQuotaResponse:
        """
        @summary 添加资源实例配额
        
        @return: AddWorkspaceQuotaResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.add_workspace_quota_with_options(workspace_id, quota_id, headers, runtime)

    async def add_workspace_quota_async(
        self,
        workspace_id: str,
        quota_id: str,
    ) -> aiwork_space_20210204_models.AddWorkspaceQuotaResponse:
        """
        @summary 添加资源实例配额
        
        @return: AddWorkspaceQuotaResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.add_workspace_quota_with_options_async(workspace_id, quota_id, headers, runtime)

    def assume_service_identity_role_with_options(
        self,
        role_name: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.AssumeServiceIdentityRoleResponse:
        """
        @summary 用PAI服务账户扮演角色
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: AssumeServiceIdentityRoleResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='AssumeServiceIdentityRole',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/serviceidentityroles/{OpenApiUtilClient.get_encode_param(role_name)}/assume',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.AssumeServiceIdentityRoleResponse(),
            self.call_api(params, req, runtime)
        )

    async def assume_service_identity_role_with_options_async(
        self,
        role_name: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.AssumeServiceIdentityRoleResponse:
        """
        @summary 用PAI服务账户扮演角色
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: AssumeServiceIdentityRoleResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='AssumeServiceIdentityRole',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/serviceidentityroles/{OpenApiUtilClient.get_encode_param(role_name)}/assume',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.AssumeServiceIdentityRoleResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def assume_service_identity_role(
        self,
        role_name: str,
    ) -> aiwork_space_20210204_models.AssumeServiceIdentityRoleResponse:
        """
        @summary 用PAI服务账户扮演角色
        
        @return: AssumeServiceIdentityRoleResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.assume_service_identity_role_with_options(role_name, headers, runtime)

    async def assume_service_identity_role_async(
        self,
        role_name: str,
    ) -> aiwork_space_20210204_models.AssumeServiceIdentityRoleResponse:
        """
        @summary 用PAI服务账户扮演角色
        
        @return: AssumeServiceIdentityRoleResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.assume_service_identity_role_with_options_async(role_name, headers, runtime)

    def change_dataset_owner_with_options(
        self,
        dataset_id: str,
        request: aiwork_space_20210204_models.ChangeDatasetOwnerRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ChangeDatasetOwnerResponse:
        """
        @summary 修改API的所有者
        
        @param request: ChangeDatasetOwnerRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ChangeDatasetOwnerResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.user_id):
            body['UserId'] = request.user_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ChangeDatasetOwner',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/datasets/change/{OpenApiUtilClient.get_encode_param(dataset_id)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ChangeDatasetOwnerResponse(),
            self.call_api(params, req, runtime)
        )

    async def change_dataset_owner_with_options_async(
        self,
        dataset_id: str,
        request: aiwork_space_20210204_models.ChangeDatasetOwnerRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ChangeDatasetOwnerResponse:
        """
        @summary 修改API的所有者
        
        @param request: ChangeDatasetOwnerRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ChangeDatasetOwnerResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.user_id):
            body['UserId'] = request.user_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ChangeDatasetOwner',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/datasets/change/{OpenApiUtilClient.get_encode_param(dataset_id)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ChangeDatasetOwnerResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def change_dataset_owner(
        self,
        dataset_id: str,
        request: aiwork_space_20210204_models.ChangeDatasetOwnerRequest,
    ) -> aiwork_space_20210204_models.ChangeDatasetOwnerResponse:
        """
        @summary 修改API的所有者
        
        @param request: ChangeDatasetOwnerRequest
        @return: ChangeDatasetOwnerResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.change_dataset_owner_with_options(dataset_id, request, headers, runtime)

    async def change_dataset_owner_async(
        self,
        dataset_id: str,
        request: aiwork_space_20210204_models.ChangeDatasetOwnerRequest,
    ) -> aiwork_space_20210204_models.ChangeDatasetOwnerResponse:
        """
        @summary 修改API的所有者
        
        @param request: ChangeDatasetOwnerRequest
        @return: ChangeDatasetOwnerResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.change_dataset_owner_with_options_async(dataset_id, request, headers, runtime)

    def create_code_source_with_options(
        self,
        request: aiwork_space_20210204_models.CreateCodeSourceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateCodeSourceResponse:
        """
        @summary 创建一个代码源配置
        
        @param request: CreateCodeSourceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateCodeSourceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.accessibility):
            body['Accessibility'] = request.accessibility
        if not UtilClient.is_unset(request.code_branch):
            body['CodeBranch'] = request.code_branch
        if not UtilClient.is_unset(request.code_repo):
            body['CodeRepo'] = request.code_repo
        if not UtilClient.is_unset(request.code_repo_access_token):
            body['CodeRepoAccessToken'] = request.code_repo_access_token
        if not UtilClient.is_unset(request.code_repo_user_name):
            body['CodeRepoUserName'] = request.code_repo_user_name
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.display_name):
            body['DisplayName'] = request.display_name
        if not UtilClient.is_unset(request.mount_path):
            body['MountPath'] = request.mount_path
        if not UtilClient.is_unset(request.workspace_id):
            body['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateCodeSource',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/codesources',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateCodeSourceResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_code_source_with_options_async(
        self,
        request: aiwork_space_20210204_models.CreateCodeSourceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateCodeSourceResponse:
        """
        @summary 创建一个代码源配置
        
        @param request: CreateCodeSourceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateCodeSourceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.accessibility):
            body['Accessibility'] = request.accessibility
        if not UtilClient.is_unset(request.code_branch):
            body['CodeBranch'] = request.code_branch
        if not UtilClient.is_unset(request.code_repo):
            body['CodeRepo'] = request.code_repo
        if not UtilClient.is_unset(request.code_repo_access_token):
            body['CodeRepoAccessToken'] = request.code_repo_access_token
        if not UtilClient.is_unset(request.code_repo_user_name):
            body['CodeRepoUserName'] = request.code_repo_user_name
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.display_name):
            body['DisplayName'] = request.display_name
        if not UtilClient.is_unset(request.mount_path):
            body['MountPath'] = request.mount_path
        if not UtilClient.is_unset(request.workspace_id):
            body['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateCodeSource',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/codesources',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateCodeSourceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_code_source(
        self,
        request: aiwork_space_20210204_models.CreateCodeSourceRequest,
    ) -> aiwork_space_20210204_models.CreateCodeSourceResponse:
        """
        @summary 创建一个代码源配置
        
        @param request: CreateCodeSourceRequest
        @return: CreateCodeSourceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_code_source_with_options(request, headers, runtime)

    async def create_code_source_async(
        self,
        request: aiwork_space_20210204_models.CreateCodeSourceRequest,
    ) -> aiwork_space_20210204_models.CreateCodeSourceResponse:
        """
        @summary 创建一个代码源配置
        
        @param request: CreateCodeSourceRequest
        @return: CreateCodeSourceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_code_source_with_options_async(request, headers, runtime)

    def create_collection_with_options(
        self,
        request: aiwork_space_20210204_models.CreateCollectionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateCollectionResponse:
        """
        @summary 创建Collection
        
        @param request: CreateCollectionRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateCollectionResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.collection_name):
            body['CollectionName'] = request.collection_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateCollection',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/collections',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateCollectionResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_collection_with_options_async(
        self,
        request: aiwork_space_20210204_models.CreateCollectionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateCollectionResponse:
        """
        @summary 创建Collection
        
        @param request: CreateCollectionRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateCollectionResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.collection_name):
            body['CollectionName'] = request.collection_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateCollection',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/collections',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateCollectionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_collection(
        self,
        request: aiwork_space_20210204_models.CreateCollectionRequest,
    ) -> aiwork_space_20210204_models.CreateCollectionResponse:
        """
        @summary 创建Collection
        
        @param request: CreateCollectionRequest
        @return: CreateCollectionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_collection_with_options(request, headers, runtime)

    async def create_collection_async(
        self,
        request: aiwork_space_20210204_models.CreateCollectionRequest,
    ) -> aiwork_space_20210204_models.CreateCollectionResponse:
        """
        @summary 创建Collection
        
        @param request: CreateCollectionRequest
        @return: CreateCollectionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_collection_with_options_async(request, headers, runtime)

    def create_dataset_with_options(
        self,
        request: aiwork_space_20210204_models.CreateDatasetRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateDatasetResponse:
        """
        @summary 创建数据集
        
        @param request: CreateDatasetRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateDatasetResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.accessibility):
            body['Accessibility'] = request.accessibility
        if not UtilClient.is_unset(request.data_source_type):
            body['DataSourceType'] = request.data_source_type
        if not UtilClient.is_unset(request.data_type):
            body['DataType'] = request.data_type
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.options):
            body['Options'] = request.options
        if not UtilClient.is_unset(request.property):
            body['Property'] = request.property
        if not UtilClient.is_unset(request.provider):
            body['Provider'] = request.provider
        if not UtilClient.is_unset(request.provider_type):
            body['ProviderType'] = request.provider_type
        if not UtilClient.is_unset(request.source_id):
            body['SourceId'] = request.source_id
        if not UtilClient.is_unset(request.source_type):
            body['SourceType'] = request.source_type
        if not UtilClient.is_unset(request.uri):
            body['Uri'] = request.uri
        if not UtilClient.is_unset(request.user_id):
            body['UserId'] = request.user_id
        if not UtilClient.is_unset(request.workspace_id):
            body['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateDataset',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/datasets',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateDatasetResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_dataset_with_options_async(
        self,
        request: aiwork_space_20210204_models.CreateDatasetRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateDatasetResponse:
        """
        @summary 创建数据集
        
        @param request: CreateDatasetRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateDatasetResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.accessibility):
            body['Accessibility'] = request.accessibility
        if not UtilClient.is_unset(request.data_source_type):
            body['DataSourceType'] = request.data_source_type
        if not UtilClient.is_unset(request.data_type):
            body['DataType'] = request.data_type
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.options):
            body['Options'] = request.options
        if not UtilClient.is_unset(request.property):
            body['Property'] = request.property
        if not UtilClient.is_unset(request.provider):
            body['Provider'] = request.provider
        if not UtilClient.is_unset(request.provider_type):
            body['ProviderType'] = request.provider_type
        if not UtilClient.is_unset(request.source_id):
            body['SourceId'] = request.source_id
        if not UtilClient.is_unset(request.source_type):
            body['SourceType'] = request.source_type
        if not UtilClient.is_unset(request.uri):
            body['Uri'] = request.uri
        if not UtilClient.is_unset(request.user_id):
            body['UserId'] = request.user_id
        if not UtilClient.is_unset(request.workspace_id):
            body['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateDataset',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/datasets',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateDatasetResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_dataset(
        self,
        request: aiwork_space_20210204_models.CreateDatasetRequest,
    ) -> aiwork_space_20210204_models.CreateDatasetResponse:
        """
        @summary 创建数据集
        
        @param request: CreateDatasetRequest
        @return: CreateDatasetResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_dataset_with_options(request, headers, runtime)

    async def create_dataset_async(
        self,
        request: aiwork_space_20210204_models.CreateDatasetRequest,
    ) -> aiwork_space_20210204_models.CreateDatasetResponse:
        """
        @summary 创建数据集
        
        @param request: CreateDatasetRequest
        @return: CreateDatasetResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_dataset_with_options_async(request, headers, runtime)

    def create_dataset_labels_with_options(
        self,
        dataset_id: str,
        request: aiwork_space_20210204_models.CreateDatasetLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateDatasetLabelsResponse:
        """
        @summary 创建或更新 Dataset 的标签
        
        @param request: CreateDatasetLabelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateDatasetLabelsResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateDatasetLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/datasets/{OpenApiUtilClient.get_encode_param(dataset_id)}/labels',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateDatasetLabelsResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_dataset_labels_with_options_async(
        self,
        dataset_id: str,
        request: aiwork_space_20210204_models.CreateDatasetLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateDatasetLabelsResponse:
        """
        @summary 创建或更新 Dataset 的标签
        
        @param request: CreateDatasetLabelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateDatasetLabelsResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateDatasetLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/datasets/{OpenApiUtilClient.get_encode_param(dataset_id)}/labels',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateDatasetLabelsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_dataset_labels(
        self,
        dataset_id: str,
        request: aiwork_space_20210204_models.CreateDatasetLabelsRequest,
    ) -> aiwork_space_20210204_models.CreateDatasetLabelsResponse:
        """
        @summary 创建或更新 Dataset 的标签
        
        @param request: CreateDatasetLabelsRequest
        @return: CreateDatasetLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_dataset_labels_with_options(dataset_id, request, headers, runtime)

    async def create_dataset_labels_async(
        self,
        dataset_id: str,
        request: aiwork_space_20210204_models.CreateDatasetLabelsRequest,
    ) -> aiwork_space_20210204_models.CreateDatasetLabelsResponse:
        """
        @summary 创建或更新 Dataset 的标签
        
        @param request: CreateDatasetLabelsRequest
        @return: CreateDatasetLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_dataset_labels_with_options_async(dataset_id, request, headers, runtime)

    def create_default_workspace_with_options(
        self,
        request: aiwork_space_20210204_models.CreateDefaultWorkspaceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateDefaultWorkspaceResponse:
        """
        @summary 创建默认工作空间
        
        @param request: CreateDefaultWorkspaceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateDefaultWorkspaceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.add_all_ram_users):
            body['AddAllRamUsers'] = request.add_all_ram_users
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.env_types):
            body['EnvTypes'] = request.env_types
        if not UtilClient.is_unset(request.resources):
            body['Resources'] = request.resources
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateDefaultWorkspace',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/defaultWorkspaces',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateDefaultWorkspaceResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_default_workspace_with_options_async(
        self,
        request: aiwork_space_20210204_models.CreateDefaultWorkspaceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateDefaultWorkspaceResponse:
        """
        @summary 创建默认工作空间
        
        @param request: CreateDefaultWorkspaceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateDefaultWorkspaceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.add_all_ram_users):
            body['AddAllRamUsers'] = request.add_all_ram_users
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.env_types):
            body['EnvTypes'] = request.env_types
        if not UtilClient.is_unset(request.resources):
            body['Resources'] = request.resources
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateDefaultWorkspace',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/defaultWorkspaces',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateDefaultWorkspaceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_default_workspace(
        self,
        request: aiwork_space_20210204_models.CreateDefaultWorkspaceRequest,
    ) -> aiwork_space_20210204_models.CreateDefaultWorkspaceResponse:
        """
        @summary 创建默认工作空间
        
        @param request: CreateDefaultWorkspaceRequest
        @return: CreateDefaultWorkspaceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_default_workspace_with_options(request, headers, runtime)

    async def create_default_workspace_async(
        self,
        request: aiwork_space_20210204_models.CreateDefaultWorkspaceRequest,
    ) -> aiwork_space_20210204_models.CreateDefaultWorkspaceResponse:
        """
        @summary 创建默认工作空间
        
        @param request: CreateDefaultWorkspaceRequest
        @return: CreateDefaultWorkspaceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_default_workspace_with_options_async(request, headers, runtime)

    def create_ding_talk_robot_message_with_options(
        self,
        request: aiwork_space_20210204_models.CreateDingTalkRobotMessageRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateDingTalkRobotMessageResponse:
        """
        @summary 发送特定格式的消息给钉钉机器人
        
        @param request: CreateDingTalkRobotMessageRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateDingTalkRobotMessageResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.access_token):
            body['AccessToken'] = request.access_token
        if not UtilClient.is_unset(request.message):
            body['Message'] = request.message
        if not UtilClient.is_unset(request.secret):
            body['Secret'] = request.secret
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateDingTalkRobotMessage',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/dingtalkrobotmessages',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateDingTalkRobotMessageResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_ding_talk_robot_message_with_options_async(
        self,
        request: aiwork_space_20210204_models.CreateDingTalkRobotMessageRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateDingTalkRobotMessageResponse:
        """
        @summary 发送特定格式的消息给钉钉机器人
        
        @param request: CreateDingTalkRobotMessageRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateDingTalkRobotMessageResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.access_token):
            body['AccessToken'] = request.access_token
        if not UtilClient.is_unset(request.message):
            body['Message'] = request.message
        if not UtilClient.is_unset(request.secret):
            body['Secret'] = request.secret
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateDingTalkRobotMessage',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/dingtalkrobotmessages',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateDingTalkRobotMessageResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_ding_talk_robot_message(
        self,
        request: aiwork_space_20210204_models.CreateDingTalkRobotMessageRequest,
    ) -> aiwork_space_20210204_models.CreateDingTalkRobotMessageResponse:
        """
        @summary 发送特定格式的消息给钉钉机器人
        
        @param request: CreateDingTalkRobotMessageRequest
        @return: CreateDingTalkRobotMessageResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_ding_talk_robot_message_with_options(request, headers, runtime)

    async def create_ding_talk_robot_message_async(
        self,
        request: aiwork_space_20210204_models.CreateDingTalkRobotMessageRequest,
    ) -> aiwork_space_20210204_models.CreateDingTalkRobotMessageResponse:
        """
        @summary 发送特定格式的消息给钉钉机器人
        
        @param request: CreateDingTalkRobotMessageRequest
        @return: CreateDingTalkRobotMessageResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_ding_talk_robot_message_with_options_async(request, headers, runtime)

    def create_experiment_with_options(
        self,
        request: aiwork_space_20210204_models.CreateExperimentRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateExperimentResponse:
        """
        @summary 创建实验
        
        @param request: CreateExperimentRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateExperimentResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.accessibility):
            body['Accessibility'] = request.accessibility
        if not UtilClient.is_unset(request.artifact_uri):
            body['ArtifactUri'] = request.artifact_uri
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.workspace_id):
            body['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateExperiment',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/experiments',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateExperimentResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_experiment_with_options_async(
        self,
        request: aiwork_space_20210204_models.CreateExperimentRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateExperimentResponse:
        """
        @summary 创建实验
        
        @param request: CreateExperimentRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateExperimentResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.accessibility):
            body['Accessibility'] = request.accessibility
        if not UtilClient.is_unset(request.artifact_uri):
            body['ArtifactUri'] = request.artifact_uri
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.workspace_id):
            body['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateExperiment',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/experiments',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateExperimentResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_experiment(
        self,
        request: aiwork_space_20210204_models.CreateExperimentRequest,
    ) -> aiwork_space_20210204_models.CreateExperimentResponse:
        """
        @summary 创建实验
        
        @param request: CreateExperimentRequest
        @return: CreateExperimentResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_experiment_with_options(request, headers, runtime)

    async def create_experiment_async(
        self,
        request: aiwork_space_20210204_models.CreateExperimentRequest,
    ) -> aiwork_space_20210204_models.CreateExperimentResponse:
        """
        @summary 创建实验
        
        @param request: CreateExperimentRequest
        @return: CreateExperimentResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_experiment_with_options_async(request, headers, runtime)

    def create_member_with_options(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.CreateMemberRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateMemberResponse:
        """
        @summary 创建成员
        
        @param request: CreateMemberRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateMemberResponse
        """
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
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/members',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateMemberResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_member_with_options_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.CreateMemberRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateMemberResponse:
        """
        @summary 创建成员
        
        @param request: CreateMemberRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateMemberResponse
        """
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
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/members',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateMemberResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_member(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.CreateMemberRequest,
    ) -> aiwork_space_20210204_models.CreateMemberResponse:
        """
        @summary 创建成员
        
        @param request: CreateMemberRequest
        @return: CreateMemberResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_member_with_options(workspace_id, request, headers, runtime)

    async def create_member_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.CreateMemberRequest,
    ) -> aiwork_space_20210204_models.CreateMemberResponse:
        """
        @summary 创建成员
        
        @param request: CreateMemberRequest
        @return: CreateMemberResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_member_with_options_async(workspace_id, request, headers, runtime)

    def create_model_with_options(
        self,
        request: aiwork_space_20210204_models.CreateModelRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateModelResponse:
        """
        @summary 创建模型
        
        @param request: CreateModelRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateModelResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.accessibility):
            body['Accessibility'] = request.accessibility
        if not UtilClient.is_unset(request.domain):
            body['Domain'] = request.domain
        if not UtilClient.is_unset(request.extra_info):
            body['ExtraInfo'] = request.extra_info
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        if not UtilClient.is_unset(request.model_description):
            body['ModelDescription'] = request.model_description
        if not UtilClient.is_unset(request.model_doc):
            body['ModelDoc'] = request.model_doc
        if not UtilClient.is_unset(request.model_name):
            body['ModelName'] = request.model_name
        if not UtilClient.is_unset(request.model_type):
            body['ModelType'] = request.model_type
        if not UtilClient.is_unset(request.order_number):
            body['OrderNumber'] = request.order_number
        if not UtilClient.is_unset(request.origin):
            body['Origin'] = request.origin
        if not UtilClient.is_unset(request.task):
            body['Task'] = request.task
        if not UtilClient.is_unset(request.workspace_id):
            body['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateModel',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateModelResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_model_with_options_async(
        self,
        request: aiwork_space_20210204_models.CreateModelRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateModelResponse:
        """
        @summary 创建模型
        
        @param request: CreateModelRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateModelResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.accessibility):
            body['Accessibility'] = request.accessibility
        if not UtilClient.is_unset(request.domain):
            body['Domain'] = request.domain
        if not UtilClient.is_unset(request.extra_info):
            body['ExtraInfo'] = request.extra_info
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        if not UtilClient.is_unset(request.model_description):
            body['ModelDescription'] = request.model_description
        if not UtilClient.is_unset(request.model_doc):
            body['ModelDoc'] = request.model_doc
        if not UtilClient.is_unset(request.model_name):
            body['ModelName'] = request.model_name
        if not UtilClient.is_unset(request.model_type):
            body['ModelType'] = request.model_type
        if not UtilClient.is_unset(request.order_number):
            body['OrderNumber'] = request.order_number
        if not UtilClient.is_unset(request.origin):
            body['Origin'] = request.origin
        if not UtilClient.is_unset(request.task):
            body['Task'] = request.task
        if not UtilClient.is_unset(request.workspace_id):
            body['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateModel',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateModelResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_model(
        self,
        request: aiwork_space_20210204_models.CreateModelRequest,
    ) -> aiwork_space_20210204_models.CreateModelResponse:
        """
        @summary 创建模型
        
        @param request: CreateModelRequest
        @return: CreateModelResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_model_with_options(request, headers, runtime)

    async def create_model_async(
        self,
        request: aiwork_space_20210204_models.CreateModelRequest,
    ) -> aiwork_space_20210204_models.CreateModelResponse:
        """
        @summary 创建模型
        
        @param request: CreateModelRequest
        @return: CreateModelResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_model_with_options_async(request, headers, runtime)

    def create_model_labels_with_options(
        self,
        model_id: str,
        request: aiwork_space_20210204_models.CreateModelLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateModelLabelsResponse:
        """
        @summary 创建或更新模型的标签
        
        @param request: CreateModelLabelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateModelLabelsResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateModelLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}/labels',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateModelLabelsResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_model_labels_with_options_async(
        self,
        model_id: str,
        request: aiwork_space_20210204_models.CreateModelLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateModelLabelsResponse:
        """
        @summary 创建或更新模型的标签
        
        @param request: CreateModelLabelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateModelLabelsResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateModelLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}/labels',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateModelLabelsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_model_labels(
        self,
        model_id: str,
        request: aiwork_space_20210204_models.CreateModelLabelsRequest,
    ) -> aiwork_space_20210204_models.CreateModelLabelsResponse:
        """
        @summary 创建或更新模型的标签
        
        @param request: CreateModelLabelsRequest
        @return: CreateModelLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_model_labels_with_options(model_id, request, headers, runtime)

    async def create_model_labels_async(
        self,
        model_id: str,
        request: aiwork_space_20210204_models.CreateModelLabelsRequest,
    ) -> aiwork_space_20210204_models.CreateModelLabelsResponse:
        """
        @summary 创建或更新模型的标签
        
        @param request: CreateModelLabelsRequest
        @return: CreateModelLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_model_labels_with_options_async(model_id, request, headers, runtime)

    def create_model_release_with_options(
        self,
        model_id: str,
        request: aiwork_space_20210204_models.CreateModelReleaseRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateModelReleaseResponse:
        """
        @summary 发布模型
        
        @param request: CreateModelReleaseRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateModelReleaseResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.collections):
            body['Collections'] = request.collections
        if not UtilClient.is_unset(request.target_model_origin):
            body['TargetModelOrigin'] = request.target_model_origin
        if not UtilClient.is_unset(request.target_model_provider):
            body['TargetModelProvider'] = request.target_model_provider
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateModelRelease',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}/release',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateModelReleaseResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_model_release_with_options_async(
        self,
        model_id: str,
        request: aiwork_space_20210204_models.CreateModelReleaseRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateModelReleaseResponse:
        """
        @summary 发布模型
        
        @param request: CreateModelReleaseRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateModelReleaseResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.collections):
            body['Collections'] = request.collections
        if not UtilClient.is_unset(request.target_model_origin):
            body['TargetModelOrigin'] = request.target_model_origin
        if not UtilClient.is_unset(request.target_model_provider):
            body['TargetModelProvider'] = request.target_model_provider
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateModelRelease',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}/release',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateModelReleaseResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_model_release(
        self,
        model_id: str,
        request: aiwork_space_20210204_models.CreateModelReleaseRequest,
    ) -> aiwork_space_20210204_models.CreateModelReleaseResponse:
        """
        @summary 发布模型
        
        @param request: CreateModelReleaseRequest
        @return: CreateModelReleaseResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_model_release_with_options(model_id, request, headers, runtime)

    async def create_model_release_async(
        self,
        model_id: str,
        request: aiwork_space_20210204_models.CreateModelReleaseRequest,
    ) -> aiwork_space_20210204_models.CreateModelReleaseResponse:
        """
        @summary 发布模型
        
        @param request: CreateModelReleaseRequest
        @return: CreateModelReleaseResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_model_release_with_options_async(model_id, request, headers, runtime)

    def create_model_version_with_options(
        self,
        model_id: str,
        request: aiwork_space_20210204_models.CreateModelVersionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateModelVersionResponse:
        """
        @summary 创建模型版本
        
        @param request: CreateModelVersionRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateModelVersionResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.approval_status):
            body['ApprovalStatus'] = request.approval_status
        if not UtilClient.is_unset(request.compression_spec):
            body['CompressionSpec'] = request.compression_spec
        if not UtilClient.is_unset(request.evaluation_spec):
            body['EvaluationSpec'] = request.evaluation_spec
        if not UtilClient.is_unset(request.extra_info):
            body['ExtraInfo'] = request.extra_info
        if not UtilClient.is_unset(request.format_type):
            body['FormatType'] = request.format_type
        if not UtilClient.is_unset(request.framework_type):
            body['FrameworkType'] = request.framework_type
        if not UtilClient.is_unset(request.inference_spec):
            body['InferenceSpec'] = request.inference_spec
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        if not UtilClient.is_unset(request.metrics):
            body['Metrics'] = request.metrics
        if not UtilClient.is_unset(request.options):
            body['Options'] = request.options
        if not UtilClient.is_unset(request.source_id):
            body['SourceId'] = request.source_id
        if not UtilClient.is_unset(request.source_type):
            body['SourceType'] = request.source_type
        if not UtilClient.is_unset(request.training_spec):
            body['TrainingSpec'] = request.training_spec
        if not UtilClient.is_unset(request.uri):
            body['Uri'] = request.uri
        if not UtilClient.is_unset(request.version_description):
            body['VersionDescription'] = request.version_description
        if not UtilClient.is_unset(request.version_name):
            body['VersionName'] = request.version_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateModelVersion',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}/versions',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateModelVersionResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_model_version_with_options_async(
        self,
        model_id: str,
        request: aiwork_space_20210204_models.CreateModelVersionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateModelVersionResponse:
        """
        @summary 创建模型版本
        
        @param request: CreateModelVersionRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateModelVersionResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.approval_status):
            body['ApprovalStatus'] = request.approval_status
        if not UtilClient.is_unset(request.compression_spec):
            body['CompressionSpec'] = request.compression_spec
        if not UtilClient.is_unset(request.evaluation_spec):
            body['EvaluationSpec'] = request.evaluation_spec
        if not UtilClient.is_unset(request.extra_info):
            body['ExtraInfo'] = request.extra_info
        if not UtilClient.is_unset(request.format_type):
            body['FormatType'] = request.format_type
        if not UtilClient.is_unset(request.framework_type):
            body['FrameworkType'] = request.framework_type
        if not UtilClient.is_unset(request.inference_spec):
            body['InferenceSpec'] = request.inference_spec
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        if not UtilClient.is_unset(request.metrics):
            body['Metrics'] = request.metrics
        if not UtilClient.is_unset(request.options):
            body['Options'] = request.options
        if not UtilClient.is_unset(request.source_id):
            body['SourceId'] = request.source_id
        if not UtilClient.is_unset(request.source_type):
            body['SourceType'] = request.source_type
        if not UtilClient.is_unset(request.training_spec):
            body['TrainingSpec'] = request.training_spec
        if not UtilClient.is_unset(request.uri):
            body['Uri'] = request.uri
        if not UtilClient.is_unset(request.version_description):
            body['VersionDescription'] = request.version_description
        if not UtilClient.is_unset(request.version_name):
            body['VersionName'] = request.version_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateModelVersion',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}/versions',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateModelVersionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_model_version(
        self,
        model_id: str,
        request: aiwork_space_20210204_models.CreateModelVersionRequest,
    ) -> aiwork_space_20210204_models.CreateModelVersionResponse:
        """
        @summary 创建模型版本
        
        @param request: CreateModelVersionRequest
        @return: CreateModelVersionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_model_version_with_options(model_id, request, headers, runtime)

    async def create_model_version_async(
        self,
        model_id: str,
        request: aiwork_space_20210204_models.CreateModelVersionRequest,
    ) -> aiwork_space_20210204_models.CreateModelVersionResponse:
        """
        @summary 创建模型版本
        
        @param request: CreateModelVersionRequest
        @return: CreateModelVersionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_model_version_with_options_async(model_id, request, headers, runtime)

    def create_model_version_labels_with_options(
        self,
        model_id: str,
        version_name: str,
        request: aiwork_space_20210204_models.CreateModelVersionLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateModelVersionLabelsResponse:
        """
        @summary 创建或更新模型版本的标签
        
        @param request: CreateModelVersionLabelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateModelVersionLabelsResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateModelVersionLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}/versions/{OpenApiUtilClient.get_encode_param(version_name)}/labels',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateModelVersionLabelsResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_model_version_labels_with_options_async(
        self,
        model_id: str,
        version_name: str,
        request: aiwork_space_20210204_models.CreateModelVersionLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateModelVersionLabelsResponse:
        """
        @summary 创建或更新模型版本的标签
        
        @param request: CreateModelVersionLabelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateModelVersionLabelsResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateModelVersionLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}/versions/{OpenApiUtilClient.get_encode_param(version_name)}/labels',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateModelVersionLabelsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_model_version_labels(
        self,
        model_id: str,
        version_name: str,
        request: aiwork_space_20210204_models.CreateModelVersionLabelsRequest,
    ) -> aiwork_space_20210204_models.CreateModelVersionLabelsResponse:
        """
        @summary 创建或更新模型版本的标签
        
        @param request: CreateModelVersionLabelsRequest
        @return: CreateModelVersionLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_model_version_labels_with_options(model_id, version_name, request, headers, runtime)

    async def create_model_version_labels_async(
        self,
        model_id: str,
        version_name: str,
        request: aiwork_space_20210204_models.CreateModelVersionLabelsRequest,
    ) -> aiwork_space_20210204_models.CreateModelVersionLabelsResponse:
        """
        @summary 创建或更新模型版本的标签
        
        @param request: CreateModelVersionLabelsRequest
        @return: CreateModelVersionLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_model_version_labels_with_options_async(model_id, version_name, request, headers, runtime)

    def create_model_version_release_with_options(
        self,
        model_id: str,
        version_name: str,
        request: aiwork_space_20210204_models.CreateModelVersionReleaseRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateModelVersionReleaseResponse:
        """
        @summary 发布模型版本
        
        @param request: CreateModelVersionReleaseRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateModelVersionReleaseResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.target_model_origin):
            body['TargetModelOrigin'] = request.target_model_origin
        if not UtilClient.is_unset(request.target_model_provider):
            body['TargetModelProvider'] = request.target_model_provider
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateModelVersionRelease',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}/versions/{OpenApiUtilClient.get_encode_param(version_name)}/release',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateModelVersionReleaseResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_model_version_release_with_options_async(
        self,
        model_id: str,
        version_name: str,
        request: aiwork_space_20210204_models.CreateModelVersionReleaseRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateModelVersionReleaseResponse:
        """
        @summary 发布模型版本
        
        @param request: CreateModelVersionReleaseRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateModelVersionReleaseResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.target_model_origin):
            body['TargetModelOrigin'] = request.target_model_origin
        if not UtilClient.is_unset(request.target_model_provider):
            body['TargetModelProvider'] = request.target_model_provider
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateModelVersionRelease',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}/versions/{OpenApiUtilClient.get_encode_param(version_name)}/release',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateModelVersionReleaseResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_model_version_release(
        self,
        model_id: str,
        version_name: str,
        request: aiwork_space_20210204_models.CreateModelVersionReleaseRequest,
    ) -> aiwork_space_20210204_models.CreateModelVersionReleaseResponse:
        """
        @summary 发布模型版本
        
        @param request: CreateModelVersionReleaseRequest
        @return: CreateModelVersionReleaseResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_model_version_release_with_options(model_id, version_name, request, headers, runtime)

    async def create_model_version_release_async(
        self,
        model_id: str,
        version_name: str,
        request: aiwork_space_20210204_models.CreateModelVersionReleaseRequest,
    ) -> aiwork_space_20210204_models.CreateModelVersionReleaseResponse:
        """
        @summary 发布模型版本
        
        @param request: CreateModelVersionReleaseRequest
        @return: CreateModelVersionReleaseResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_model_version_release_with_options_async(model_id, version_name, request, headers, runtime)

    def create_product_orders_with_options(
        self,
        request: aiwork_space_20210204_models.CreateProductOrdersRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateProductOrdersResponse:
        """
        @summary 创建产品订单
        
        @param request: CreateProductOrdersRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateProductOrdersResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.auto_pay):
            body['AutoPay'] = request.auto_pay
        if not UtilClient.is_unset(request.products):
            body['Products'] = request.products
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateProductOrders',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/productorders',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateProductOrdersResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_product_orders_with_options_async(
        self,
        request: aiwork_space_20210204_models.CreateProductOrdersRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateProductOrdersResponse:
        """
        @summary 创建产品订单
        
        @param request: CreateProductOrdersRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateProductOrdersResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.auto_pay):
            body['AutoPay'] = request.auto_pay
        if not UtilClient.is_unset(request.products):
            body['Products'] = request.products
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateProductOrders',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/productorders',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateProductOrdersResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_product_orders(
        self,
        request: aiwork_space_20210204_models.CreateProductOrdersRequest,
    ) -> aiwork_space_20210204_models.CreateProductOrdersResponse:
        """
        @summary 创建产品订单
        
        @param request: CreateProductOrdersRequest
        @return: CreateProductOrdersResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_product_orders_with_options(request, headers, runtime)

    async def create_product_orders_async(
        self,
        request: aiwork_space_20210204_models.CreateProductOrdersRequest,
    ) -> aiwork_space_20210204_models.CreateProductOrdersResponse:
        """
        @summary 创建产品订单
        
        @param request: CreateProductOrdersRequest
        @return: CreateProductOrdersResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_product_orders_with_options_async(request, headers, runtime)

    def create_service_identity_role_with_options(
        self,
        request: aiwork_space_20210204_models.CreateServiceIdentityRoleRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateServiceIdentityRoleResponse:
        """
        @summary 创建被PAI服务账户扮演的角色
        
        @param request: CreateServiceIdentityRoleRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateServiceIdentityRoleResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.role_name):
            body['RoleName'] = request.role_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateServiceIdentityRole',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/serviceidentityroles',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateServiceIdentityRoleResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_service_identity_role_with_options_async(
        self,
        request: aiwork_space_20210204_models.CreateServiceIdentityRoleRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateServiceIdentityRoleResponse:
        """
        @summary 创建被PAI服务账户扮演的角色
        
        @param request: CreateServiceIdentityRoleRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateServiceIdentityRoleResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.role_name):
            body['RoleName'] = request.role_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateServiceIdentityRole',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/serviceidentityroles',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateServiceIdentityRoleResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_service_identity_role(
        self,
        request: aiwork_space_20210204_models.CreateServiceIdentityRoleRequest,
    ) -> aiwork_space_20210204_models.CreateServiceIdentityRoleResponse:
        """
        @summary 创建被PAI服务账户扮演的角色
        
        @param request: CreateServiceIdentityRoleRequest
        @return: CreateServiceIdentityRoleResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_service_identity_role_with_options(request, headers, runtime)

    async def create_service_identity_role_async(
        self,
        request: aiwork_space_20210204_models.CreateServiceIdentityRoleRequest,
    ) -> aiwork_space_20210204_models.CreateServiceIdentityRoleResponse:
        """
        @summary 创建被PAI服务账户扮演的角色
        
        @param request: CreateServiceIdentityRoleRequest
        @return: CreateServiceIdentityRoleResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_service_identity_role_with_options_async(request, headers, runtime)

    def create_service_template_with_options(
        self,
        request: aiwork_space_20210204_models.CreateServiceTemplateRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateServiceTemplateResponse:
        """
        @summary 创建服务模版
        
        @param request: CreateServiceTemplateRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateServiceTemplateResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.inference_spec):
            body['InferenceSpec'] = request.inference_spec
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        if not UtilClient.is_unset(request.order_number):
            body['OrderNumber'] = request.order_number
        if not UtilClient.is_unset(request.provider):
            body['Provider'] = request.provider
        if not UtilClient.is_unset(request.service_template_description):
            body['ServiceTemplateDescription'] = request.service_template_description
        if not UtilClient.is_unset(request.service_template_doc):
            body['ServiceTemplateDoc'] = request.service_template_doc
        if not UtilClient.is_unset(request.service_template_name):
            body['ServiceTemplateName'] = request.service_template_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateServiceTemplate',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/servicetemplates',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateServiceTemplateResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_service_template_with_options_async(
        self,
        request: aiwork_space_20210204_models.CreateServiceTemplateRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateServiceTemplateResponse:
        """
        @summary 创建服务模版
        
        @param request: CreateServiceTemplateRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateServiceTemplateResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.inference_spec):
            body['InferenceSpec'] = request.inference_spec
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        if not UtilClient.is_unset(request.order_number):
            body['OrderNumber'] = request.order_number
        if not UtilClient.is_unset(request.provider):
            body['Provider'] = request.provider
        if not UtilClient.is_unset(request.service_template_description):
            body['ServiceTemplateDescription'] = request.service_template_description
        if not UtilClient.is_unset(request.service_template_doc):
            body['ServiceTemplateDoc'] = request.service_template_doc
        if not UtilClient.is_unset(request.service_template_name):
            body['ServiceTemplateName'] = request.service_template_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateServiceTemplate',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/servicetemplates',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateServiceTemplateResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_service_template(
        self,
        request: aiwork_space_20210204_models.CreateServiceTemplateRequest,
    ) -> aiwork_space_20210204_models.CreateServiceTemplateResponse:
        """
        @summary 创建服务模版
        
        @param request: CreateServiceTemplateRequest
        @return: CreateServiceTemplateResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_service_template_with_options(request, headers, runtime)

    async def create_service_template_async(
        self,
        request: aiwork_space_20210204_models.CreateServiceTemplateRequest,
    ) -> aiwork_space_20210204_models.CreateServiceTemplateResponse:
        """
        @summary 创建服务模版
        
        @param request: CreateServiceTemplateRequest
        @return: CreateServiceTemplateResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_service_template_with_options_async(request, headers, runtime)

    def create_service_template_labels_with_options(
        self,
        service_template_id: str,
        request: aiwork_space_20210204_models.CreateServiceTemplateLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateServiceTemplateLabelsResponse:
        """
        @summary 创建或更新服务模版的标签
        
        @param request: CreateServiceTemplateLabelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateServiceTemplateLabelsResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateServiceTemplateLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/servicetemplates/{OpenApiUtilClient.get_encode_param(service_template_id)}/labels',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateServiceTemplateLabelsResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_service_template_labels_with_options_async(
        self,
        service_template_id: str,
        request: aiwork_space_20210204_models.CreateServiceTemplateLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateServiceTemplateLabelsResponse:
        """
        @summary 创建或更新服务模版的标签
        
        @param request: CreateServiceTemplateLabelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateServiceTemplateLabelsResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateServiceTemplateLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/servicetemplates/{OpenApiUtilClient.get_encode_param(service_template_id)}/labels',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateServiceTemplateLabelsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_service_template_labels(
        self,
        service_template_id: str,
        request: aiwork_space_20210204_models.CreateServiceTemplateLabelsRequest,
    ) -> aiwork_space_20210204_models.CreateServiceTemplateLabelsResponse:
        """
        @summary 创建或更新服务模版的标签
        
        @param request: CreateServiceTemplateLabelsRequest
        @return: CreateServiceTemplateLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_service_template_labels_with_options(service_template_id, request, headers, runtime)

    async def create_service_template_labels_async(
        self,
        service_template_id: str,
        request: aiwork_space_20210204_models.CreateServiceTemplateLabelsRequest,
    ) -> aiwork_space_20210204_models.CreateServiceTemplateLabelsResponse:
        """
        @summary 创建或更新服务模版的标签
        
        @param request: CreateServiceTemplateLabelsRequest
        @return: CreateServiceTemplateLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_service_template_labels_with_options_async(service_template_id, request, headers, runtime)

    def create_trial_with_options(
        self,
        request: aiwork_space_20210204_models.CreateTrialRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateTrialResponse:
        """
        @summary 创建Trial
        
        @param request: CreateTrialRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateTrialResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.experiment_id):
            body['ExperimentId'] = request.experiment_id
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.source_id):
            body['SourceId'] = request.source_id
        if not UtilClient.is_unset(request.source_type):
            body['SourceType'] = request.source_type
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateTrial',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/trials',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateTrialResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_trial_with_options_async(
        self,
        request: aiwork_space_20210204_models.CreateTrialRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateTrialResponse:
        """
        @summary 创建Trial
        
        @param request: CreateTrialRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateTrialResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.experiment_id):
            body['ExperimentId'] = request.experiment_id
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.source_id):
            body['SourceId'] = request.source_id
        if not UtilClient.is_unset(request.source_type):
            body['SourceType'] = request.source_type
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateTrial',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/trials',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateTrialResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_trial(
        self,
        request: aiwork_space_20210204_models.CreateTrialRequest,
    ) -> aiwork_space_20210204_models.CreateTrialResponse:
        """
        @summary 创建Trial
        
        @param request: CreateTrialRequest
        @return: CreateTrialResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_trial_with_options(request, headers, runtime)

    async def create_trial_async(
        self,
        request: aiwork_space_20210204_models.CreateTrialRequest,
    ) -> aiwork_space_20210204_models.CreateTrialResponse:
        """
        @summary 创建Trial
        
        @param request: CreateTrialRequest
        @return: CreateTrialResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_trial_with_options_async(request, headers, runtime)

    def create_user_with_options(
        self,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateUserResponse:
        """
        @summary 创建用户
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateUserResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='CreateUser',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/users',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateUserResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_user_with_options_async(
        self,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateUserResponse:
        """
        @summary 创建用户
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateUserResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='CreateUser',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/users',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateUserResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_user(self) -> aiwork_space_20210204_models.CreateUserResponse:
        """
        @summary 创建用户
        
        @return: CreateUserResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_user_with_options(headers, runtime)

    async def create_user_async(self) -> aiwork_space_20210204_models.CreateUserResponse:
        """
        @summary 创建用户
        
        @return: CreateUserResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_user_with_options_async(headers, runtime)

    def create_workspace_with_options(
        self,
        request: aiwork_space_20210204_models.CreateWorkspaceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateWorkspaceResponse:
        """
        @summary 创建工作空间
        
        @param request: CreateWorkspaceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateWorkspaceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.display_name):
            body['DisplayName'] = request.display_name
        if not UtilClient.is_unset(request.env_types):
            body['EnvTypes'] = request.env_types
        if not UtilClient.is_unset(request.workspace_name):
            body['WorkspaceName'] = request.workspace_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateWorkspace',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateWorkspaceResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_workspace_with_options_async(
        self,
        request: aiwork_space_20210204_models.CreateWorkspaceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateWorkspaceResponse:
        """
        @summary 创建工作空间
        
        @param request: CreateWorkspaceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateWorkspaceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.display_name):
            body['DisplayName'] = request.display_name
        if not UtilClient.is_unset(request.env_types):
            body['EnvTypes'] = request.env_types
        if not UtilClient.is_unset(request.workspace_name):
            body['WorkspaceName'] = request.workspace_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateWorkspace',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateWorkspaceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_workspace(
        self,
        request: aiwork_space_20210204_models.CreateWorkspaceRequest,
    ) -> aiwork_space_20210204_models.CreateWorkspaceResponse:
        """
        @summary 创建工作空间
        
        @param request: CreateWorkspaceRequest
        @return: CreateWorkspaceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_workspace_with_options(request, headers, runtime)

    async def create_workspace_async(
        self,
        request: aiwork_space_20210204_models.CreateWorkspaceRequest,
    ) -> aiwork_space_20210204_models.CreateWorkspaceResponse:
        """
        @summary 创建工作空间
        
        @param request: CreateWorkspaceRequest
        @return: CreateWorkspaceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_workspace_with_options_async(request, headers, runtime)

    def create_workspace_resource_with_options(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.CreateWorkspaceResourceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateWorkspaceResourceResponse:
        """
        @summary 创建资源
        
        @param request: CreateWorkspaceResourceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateWorkspaceResourceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.option):
            body['Option'] = request.option
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
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/resources',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateWorkspaceResourceResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_workspace_resource_with_options_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.CreateWorkspaceResourceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.CreateWorkspaceResourceResponse:
        """
        @summary 创建资源
        
        @param request: CreateWorkspaceResourceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateWorkspaceResourceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.option):
            body['Option'] = request.option
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
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/resources',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.CreateWorkspaceResourceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_workspace_resource(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.CreateWorkspaceResourceRequest,
    ) -> aiwork_space_20210204_models.CreateWorkspaceResourceResponse:
        """
        @summary 创建资源
        
        @param request: CreateWorkspaceResourceRequest
        @return: CreateWorkspaceResourceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_workspace_resource_with_options(workspace_id, request, headers, runtime)

    async def create_workspace_resource_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.CreateWorkspaceResourceRequest,
    ) -> aiwork_space_20210204_models.CreateWorkspaceResourceResponse:
        """
        @summary 创建资源
        
        @param request: CreateWorkspaceResourceRequest
        @return: CreateWorkspaceResourceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_workspace_resource_with_options_async(workspace_id, request, headers, runtime)

    def delete_code_source_with_options(
        self,
        code_source_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteCodeSourceResponse:
        """
        @summary 删除一个代码源配置
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteCodeSourceResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteCodeSource',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/codesources/{OpenApiUtilClient.get_encode_param(code_source_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteCodeSourceResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_code_source_with_options_async(
        self,
        code_source_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteCodeSourceResponse:
        """
        @summary 删除一个代码源配置
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteCodeSourceResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteCodeSource',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/codesources/{OpenApiUtilClient.get_encode_param(code_source_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteCodeSourceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_code_source(
        self,
        code_source_id: str,
    ) -> aiwork_space_20210204_models.DeleteCodeSourceResponse:
        """
        @summary 删除一个代码源配置
        
        @return: DeleteCodeSourceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_code_source_with_options(code_source_id, headers, runtime)

    async def delete_code_source_async(
        self,
        code_source_id: str,
    ) -> aiwork_space_20210204_models.DeleteCodeSourceResponse:
        """
        @summary 删除一个代码源配置
        
        @return: DeleteCodeSourceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_code_source_with_options_async(code_source_id, headers, runtime)

    def delete_collection_with_options(
        self,
        collection_name: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteCollectionResponse:
        """
        @summary 删除Collection
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteCollectionResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteCollection',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/collections/{OpenApiUtilClient.get_encode_param(collection_name)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteCollectionResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_collection_with_options_async(
        self,
        collection_name: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteCollectionResponse:
        """
        @summary 删除Collection
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteCollectionResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteCollection',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/collections/{OpenApiUtilClient.get_encode_param(collection_name)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteCollectionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_collection(
        self,
        collection_name: str,
    ) -> aiwork_space_20210204_models.DeleteCollectionResponse:
        """
        @summary 删除Collection
        
        @return: DeleteCollectionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_collection_with_options(collection_name, headers, runtime)

    async def delete_collection_async(
        self,
        collection_name: str,
    ) -> aiwork_space_20210204_models.DeleteCollectionResponse:
        """
        @summary 删除Collection
        
        @return: DeleteCollectionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_collection_with_options_async(collection_name, headers, runtime)

    def delete_config_with_options(
        self,
        workspace_id: str,
        config_key: str,
        request: aiwork_space_20210204_models.DeleteConfigRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteConfigResponse:
        """
        @summary 删除配置
        
        @param request: DeleteConfigRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteConfigResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.labels):
            query['Labels'] = request.labels
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteConfig',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/configs/{OpenApiUtilClient.get_encode_param(config_key)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteConfigResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_config_with_options_async(
        self,
        workspace_id: str,
        config_key: str,
        request: aiwork_space_20210204_models.DeleteConfigRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteConfigResponse:
        """
        @summary 删除配置
        
        @param request: DeleteConfigRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteConfigResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.labels):
            query['Labels'] = request.labels
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteConfig',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/configs/{OpenApiUtilClient.get_encode_param(config_key)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteConfigResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_config(
        self,
        workspace_id: str,
        config_key: str,
        request: aiwork_space_20210204_models.DeleteConfigRequest,
    ) -> aiwork_space_20210204_models.DeleteConfigResponse:
        """
        @summary 删除配置
        
        @param request: DeleteConfigRequest
        @return: DeleteConfigResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_config_with_options(workspace_id, config_key, request, headers, runtime)

    async def delete_config_async(
        self,
        workspace_id: str,
        config_key: str,
        request: aiwork_space_20210204_models.DeleteConfigRequest,
    ) -> aiwork_space_20210204_models.DeleteConfigResponse:
        """
        @summary 删除配置
        
        @param request: DeleteConfigRequest
        @return: DeleteConfigResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_config_with_options_async(workspace_id, config_key, request, headers, runtime)

    def delete_dataset_with_options(
        self,
        dataset_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteDatasetResponse:
        """
        @summary 删除数据集
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteDatasetResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteDataset',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/datasets/{OpenApiUtilClient.get_encode_param(dataset_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteDatasetResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_dataset_with_options_async(
        self,
        dataset_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteDatasetResponse:
        """
        @summary 删除数据集
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteDatasetResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteDataset',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/datasets/{OpenApiUtilClient.get_encode_param(dataset_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteDatasetResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_dataset(
        self,
        dataset_id: str,
    ) -> aiwork_space_20210204_models.DeleteDatasetResponse:
        """
        @summary 删除数据集
        
        @return: DeleteDatasetResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_dataset_with_options(dataset_id, headers, runtime)

    async def delete_dataset_async(
        self,
        dataset_id: str,
    ) -> aiwork_space_20210204_models.DeleteDatasetResponse:
        """
        @summary 删除数据集
        
        @return: DeleteDatasetResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_dataset_with_options_async(dataset_id, headers, runtime)

    def delete_dataset_labels_with_options(
        self,
        dataset_id: str,
        request: aiwork_space_20210204_models.DeleteDatasetLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteDatasetLabelsResponse:
        """
        @summary 删除 Dataset 的标签
        
        @param request: DeleteDatasetLabelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteDatasetLabelsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keys):
            query['Keys'] = request.keys
        if not UtilClient.is_unset(request.label_keys):
            query['LabelKeys'] = request.label_keys
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteDatasetLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/datasets/{OpenApiUtilClient.get_encode_param(dataset_id)}/labels',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteDatasetLabelsResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_dataset_labels_with_options_async(
        self,
        dataset_id: str,
        request: aiwork_space_20210204_models.DeleteDatasetLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteDatasetLabelsResponse:
        """
        @summary 删除 Dataset 的标签
        
        @param request: DeleteDatasetLabelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteDatasetLabelsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keys):
            query['Keys'] = request.keys
        if not UtilClient.is_unset(request.label_keys):
            query['LabelKeys'] = request.label_keys
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteDatasetLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/datasets/{OpenApiUtilClient.get_encode_param(dataset_id)}/labels',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteDatasetLabelsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_dataset_labels(
        self,
        dataset_id: str,
        request: aiwork_space_20210204_models.DeleteDatasetLabelsRequest,
    ) -> aiwork_space_20210204_models.DeleteDatasetLabelsResponse:
        """
        @summary 删除 Dataset 的标签
        
        @param request: DeleteDatasetLabelsRequest
        @return: DeleteDatasetLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_dataset_labels_with_options(dataset_id, request, headers, runtime)

    async def delete_dataset_labels_async(
        self,
        dataset_id: str,
        request: aiwork_space_20210204_models.DeleteDatasetLabelsRequest,
    ) -> aiwork_space_20210204_models.DeleteDatasetLabelsResponse:
        """
        @summary 删除 Dataset 的标签
        
        @param request: DeleteDatasetLabelsRequest
        @return: DeleteDatasetLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_dataset_labels_with_options_async(dataset_id, request, headers, runtime)

    def delete_experiment_with_options(
        self,
        experiment_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteExperimentResponse:
        """
        @summary 删除实验
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteExperimentResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteExperiment',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/experiments/{OpenApiUtilClient.get_encode_param(experiment_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteExperimentResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_experiment_with_options_async(
        self,
        experiment_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteExperimentResponse:
        """
        @summary 删除实验
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteExperimentResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteExperiment',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/experiments/{OpenApiUtilClient.get_encode_param(experiment_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteExperimentResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_experiment(
        self,
        experiment_id: str,
    ) -> aiwork_space_20210204_models.DeleteExperimentResponse:
        """
        @summary 删除实验
        
        @return: DeleteExperimentResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_experiment_with_options(experiment_id, headers, runtime)

    async def delete_experiment_async(
        self,
        experiment_id: str,
    ) -> aiwork_space_20210204_models.DeleteExperimentResponse:
        """
        @summary 删除实验
        
        @return: DeleteExperimentResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_experiment_with_options_async(experiment_id, headers, runtime)

    def delete_experiment_label_with_options(
        self,
        experiment_id: str,
        key: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteExperimentLabelResponse:
        """
        @summary 删除实验标签
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteExperimentLabelResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteExperimentLabel',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/experiments/{OpenApiUtilClient.get_encode_param(experiment_id)}/labels/{OpenApiUtilClient.get_encode_param(key)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteExperimentLabelResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_experiment_label_with_options_async(
        self,
        experiment_id: str,
        key: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteExperimentLabelResponse:
        """
        @summary 删除实验标签
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteExperimentLabelResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteExperimentLabel',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/experiments/{OpenApiUtilClient.get_encode_param(experiment_id)}/labels/{OpenApiUtilClient.get_encode_param(key)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteExperimentLabelResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_experiment_label(
        self,
        experiment_id: str,
        key: str,
    ) -> aiwork_space_20210204_models.DeleteExperimentLabelResponse:
        """
        @summary 删除实验标签
        
        @return: DeleteExperimentLabelResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_experiment_label_with_options(experiment_id, key, headers, runtime)

    async def delete_experiment_label_async(
        self,
        experiment_id: str,
        key: str,
    ) -> aiwork_space_20210204_models.DeleteExperimentLabelResponse:
        """
        @summary 删除实验标签
        
        @return: DeleteExperimentLabelResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_experiment_label_with_options_async(experiment_id, key, headers, runtime)

    def delete_members_with_options(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.DeleteMembersRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteMembersResponse:
        """
        @summary 删除工作空间成员
        
        @param request: DeleteMembersRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteMembersResponse
        """
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
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/members',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteMembersResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_members_with_options_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.DeleteMembersRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteMembersResponse:
        """
        @summary 删除工作空间成员
        
        @param request: DeleteMembersRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteMembersResponse
        """
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
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/members',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteMembersResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_members(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.DeleteMembersRequest,
    ) -> aiwork_space_20210204_models.DeleteMembersResponse:
        """
        @summary 删除工作空间成员
        
        @param request: DeleteMembersRequest
        @return: DeleteMembersResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_members_with_options(workspace_id, request, headers, runtime)

    async def delete_members_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.DeleteMembersRequest,
    ) -> aiwork_space_20210204_models.DeleteMembersResponse:
        """
        @summary 删除工作空间成员
        
        @param request: DeleteMembersRequest
        @return: DeleteMembersResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_members_with_options_async(workspace_id, request, headers, runtime)

    def delete_model_with_options(
        self,
        model_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteModelResponse:
        """
        @summary 删除模型
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteModelResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteModel',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteModelResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_model_with_options_async(
        self,
        model_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteModelResponse:
        """
        @summary 删除模型
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteModelResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteModel',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteModelResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_model(
        self,
        model_id: str,
    ) -> aiwork_space_20210204_models.DeleteModelResponse:
        """
        @summary 删除模型
        
        @return: DeleteModelResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_model_with_options(model_id, headers, runtime)

    async def delete_model_async(
        self,
        model_id: str,
    ) -> aiwork_space_20210204_models.DeleteModelResponse:
        """
        @summary 删除模型
        
        @return: DeleteModelResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_model_with_options_async(model_id, headers, runtime)

    def delete_model_domain_with_options(
        self,
        model_domain_id: str,
        request: aiwork_space_20210204_models.DeleteModelDomainRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteModelDomainResponse:
        """
        @summary 删除模型领域
        
        @param request: DeleteModelDomainRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteModelDomainResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.model_task_ids):
            query['ModelTaskIds'] = request.model_task_ids
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteModelDomain',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/modeldomains/{OpenApiUtilClient.get_encode_param(model_domain_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteModelDomainResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_model_domain_with_options_async(
        self,
        model_domain_id: str,
        request: aiwork_space_20210204_models.DeleteModelDomainRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteModelDomainResponse:
        """
        @summary 删除模型领域
        
        @param request: DeleteModelDomainRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteModelDomainResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.model_task_ids):
            query['ModelTaskIds'] = request.model_task_ids
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteModelDomain',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/modeldomains/{OpenApiUtilClient.get_encode_param(model_domain_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteModelDomainResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_model_domain(
        self,
        model_domain_id: str,
        request: aiwork_space_20210204_models.DeleteModelDomainRequest,
    ) -> aiwork_space_20210204_models.DeleteModelDomainResponse:
        """
        @summary 删除模型领域
        
        @param request: DeleteModelDomainRequest
        @return: DeleteModelDomainResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_model_domain_with_options(model_domain_id, request, headers, runtime)

    async def delete_model_domain_async(
        self,
        model_domain_id: str,
        request: aiwork_space_20210204_models.DeleteModelDomainRequest,
    ) -> aiwork_space_20210204_models.DeleteModelDomainResponse:
        """
        @summary 删除模型领域
        
        @param request: DeleteModelDomainRequest
        @return: DeleteModelDomainResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_model_domain_with_options_async(model_domain_id, request, headers, runtime)

    def delete_model_labels_with_options(
        self,
        model_id: str,
        request: aiwork_space_20210204_models.DeleteModelLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteModelLabelsResponse:
        """
        @summary 删除模型的标签
        
        @param request: DeleteModelLabelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteModelLabelsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keys):
            query['Keys'] = request.keys
        if not UtilClient.is_unset(request.label_keys):
            query['LabelKeys'] = request.label_keys
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteModelLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}/labels',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteModelLabelsResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_model_labels_with_options_async(
        self,
        model_id: str,
        request: aiwork_space_20210204_models.DeleteModelLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteModelLabelsResponse:
        """
        @summary 删除模型的标签
        
        @param request: DeleteModelLabelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteModelLabelsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keys):
            query['Keys'] = request.keys
        if not UtilClient.is_unset(request.label_keys):
            query['LabelKeys'] = request.label_keys
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteModelLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}/labels',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteModelLabelsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_model_labels(
        self,
        model_id: str,
        request: aiwork_space_20210204_models.DeleteModelLabelsRequest,
    ) -> aiwork_space_20210204_models.DeleteModelLabelsResponse:
        """
        @summary 删除模型的标签
        
        @param request: DeleteModelLabelsRequest
        @return: DeleteModelLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_model_labels_with_options(model_id, request, headers, runtime)

    async def delete_model_labels_async(
        self,
        model_id: str,
        request: aiwork_space_20210204_models.DeleteModelLabelsRequest,
    ) -> aiwork_space_20210204_models.DeleteModelLabelsResponse:
        """
        @summary 删除模型的标签
        
        @param request: DeleteModelLabelsRequest
        @return: DeleteModelLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_model_labels_with_options_async(model_id, request, headers, runtime)

    def delete_model_version_with_options(
        self,
        model_id: str,
        version_name: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteModelVersionResponse:
        """
        @summary 删除模型版本
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteModelVersionResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteModelVersion',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}/versions/{OpenApiUtilClient.get_encode_param(version_name)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteModelVersionResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_model_version_with_options_async(
        self,
        model_id: str,
        version_name: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteModelVersionResponse:
        """
        @summary 删除模型版本
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteModelVersionResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteModelVersion',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}/versions/{OpenApiUtilClient.get_encode_param(version_name)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteModelVersionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_model_version(
        self,
        model_id: str,
        version_name: str,
    ) -> aiwork_space_20210204_models.DeleteModelVersionResponse:
        """
        @summary 删除模型版本
        
        @return: DeleteModelVersionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_model_version_with_options(model_id, version_name, headers, runtime)

    async def delete_model_version_async(
        self,
        model_id: str,
        version_name: str,
    ) -> aiwork_space_20210204_models.DeleteModelVersionResponse:
        """
        @summary 删除模型版本
        
        @return: DeleteModelVersionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_model_version_with_options_async(model_id, version_name, headers, runtime)

    def delete_model_version_labels_with_options(
        self,
        model_id: str,
        version_name: str,
        request: aiwork_space_20210204_models.DeleteModelVersionLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteModelVersionLabelsResponse:
        """
        @summary 删除模型版本的标签
        
        @param request: DeleteModelVersionLabelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteModelVersionLabelsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keys):
            query['Keys'] = request.keys
        if not UtilClient.is_unset(request.label_keys):
            query['LabelKeys'] = request.label_keys
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteModelVersionLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}/versions/{OpenApiUtilClient.get_encode_param(version_name)}/labels',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteModelVersionLabelsResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_model_version_labels_with_options_async(
        self,
        model_id: str,
        version_name: str,
        request: aiwork_space_20210204_models.DeleteModelVersionLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteModelVersionLabelsResponse:
        """
        @summary 删除模型版本的标签
        
        @param request: DeleteModelVersionLabelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteModelVersionLabelsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keys):
            query['Keys'] = request.keys
        if not UtilClient.is_unset(request.label_keys):
            query['LabelKeys'] = request.label_keys
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteModelVersionLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}/versions/{OpenApiUtilClient.get_encode_param(version_name)}/labels',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteModelVersionLabelsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_model_version_labels(
        self,
        model_id: str,
        version_name: str,
        request: aiwork_space_20210204_models.DeleteModelVersionLabelsRequest,
    ) -> aiwork_space_20210204_models.DeleteModelVersionLabelsResponse:
        """
        @summary 删除模型版本的标签
        
        @param request: DeleteModelVersionLabelsRequest
        @return: DeleteModelVersionLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_model_version_labels_with_options(model_id, version_name, request, headers, runtime)

    async def delete_model_version_labels_async(
        self,
        model_id: str,
        version_name: str,
        request: aiwork_space_20210204_models.DeleteModelVersionLabelsRequest,
    ) -> aiwork_space_20210204_models.DeleteModelVersionLabelsResponse:
        """
        @summary 删除模型版本的标签
        
        @param request: DeleteModelVersionLabelsRequest
        @return: DeleteModelVersionLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_model_version_labels_with_options_async(model_id, version_name, request, headers, runtime)

    def delete_service_template_with_options(
        self,
        service_template_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteServiceTemplateResponse:
        """
        @summary 删除服务模版
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteServiceTemplateResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteServiceTemplate',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/servicetemplates/{OpenApiUtilClient.get_encode_param(service_template_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteServiceTemplateResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_service_template_with_options_async(
        self,
        service_template_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteServiceTemplateResponse:
        """
        @summary 删除服务模版
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteServiceTemplateResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteServiceTemplate',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/servicetemplates/{OpenApiUtilClient.get_encode_param(service_template_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteServiceTemplateResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_service_template(
        self,
        service_template_id: str,
    ) -> aiwork_space_20210204_models.DeleteServiceTemplateResponse:
        """
        @summary 删除服务模版
        
        @return: DeleteServiceTemplateResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_service_template_with_options(service_template_id, headers, runtime)

    async def delete_service_template_async(
        self,
        service_template_id: str,
    ) -> aiwork_space_20210204_models.DeleteServiceTemplateResponse:
        """
        @summary 删除服务模版
        
        @return: DeleteServiceTemplateResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_service_template_with_options_async(service_template_id, headers, runtime)

    def delete_service_template_labels_with_options(
        self,
        service_template_id: str,
        request: aiwork_space_20210204_models.DeleteServiceTemplateLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteServiceTemplateLabelsResponse:
        """
        @summary 删除服务模版的标签
        
        @param request: DeleteServiceTemplateLabelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteServiceTemplateLabelsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.label_keys):
            query['LabelKeys'] = request.label_keys
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteServiceTemplateLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/servicetemplates/{OpenApiUtilClient.get_encode_param(service_template_id)}/labels',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteServiceTemplateLabelsResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_service_template_labels_with_options_async(
        self,
        service_template_id: str,
        request: aiwork_space_20210204_models.DeleteServiceTemplateLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteServiceTemplateLabelsResponse:
        """
        @summary 删除服务模版的标签
        
        @param request: DeleteServiceTemplateLabelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteServiceTemplateLabelsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.label_keys):
            query['LabelKeys'] = request.label_keys
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteServiceTemplateLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/servicetemplates/{OpenApiUtilClient.get_encode_param(service_template_id)}/labels',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteServiceTemplateLabelsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_service_template_labels(
        self,
        service_template_id: str,
        request: aiwork_space_20210204_models.DeleteServiceTemplateLabelsRequest,
    ) -> aiwork_space_20210204_models.DeleteServiceTemplateLabelsResponse:
        """
        @summary 删除服务模版的标签
        
        @param request: DeleteServiceTemplateLabelsRequest
        @return: DeleteServiceTemplateLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_service_template_labels_with_options(service_template_id, request, headers, runtime)

    async def delete_service_template_labels_async(
        self,
        service_template_id: str,
        request: aiwork_space_20210204_models.DeleteServiceTemplateLabelsRequest,
    ) -> aiwork_space_20210204_models.DeleteServiceTemplateLabelsResponse:
        """
        @summary 删除服务模版的标签
        
        @param request: DeleteServiceTemplateLabelsRequest
        @return: DeleteServiceTemplateLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_service_template_labels_with_options_async(service_template_id, request, headers, runtime)

    def delete_user_config_with_options(
        self,
        category_name: str,
        request: aiwork_space_20210204_models.DeleteUserConfigRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteUserConfigResponse:
        """
        @summary 删除用户配置
        
        @param request: DeleteUserConfigRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteUserConfigResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.config_key):
            query['ConfigKey'] = request.config_key
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteUserConfig',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/userconfigs/{OpenApiUtilClient.get_encode_param(category_name)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteUserConfigResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_user_config_with_options_async(
        self,
        category_name: str,
        request: aiwork_space_20210204_models.DeleteUserConfigRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteUserConfigResponse:
        """
        @summary 删除用户配置
        
        @param request: DeleteUserConfigRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteUserConfigResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.config_key):
            query['ConfigKey'] = request.config_key
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteUserConfig',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/userconfigs/{OpenApiUtilClient.get_encode_param(category_name)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteUserConfigResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_user_config(
        self,
        category_name: str,
        request: aiwork_space_20210204_models.DeleteUserConfigRequest,
    ) -> aiwork_space_20210204_models.DeleteUserConfigResponse:
        """
        @summary 删除用户配置
        
        @param request: DeleteUserConfigRequest
        @return: DeleteUserConfigResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_user_config_with_options(category_name, request, headers, runtime)

    async def delete_user_config_async(
        self,
        category_name: str,
        request: aiwork_space_20210204_models.DeleteUserConfigRequest,
    ) -> aiwork_space_20210204_models.DeleteUserConfigResponse:
        """
        @summary 删除用户配置
        
        @param request: DeleteUserConfigRequest
        @return: DeleteUserConfigResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_user_config_with_options_async(category_name, request, headers, runtime)

    def delete_workspace_with_options(
        self,
        workspace_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteWorkspaceResponse:
        """
        @summary 删除工作空间
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteWorkspaceResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteWorkspace',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteWorkspaceResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_workspace_with_options_async(
        self,
        workspace_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteWorkspaceResponse:
        """
        @summary 删除工作空间
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteWorkspaceResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteWorkspace',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteWorkspaceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_workspace(
        self,
        workspace_id: str,
    ) -> aiwork_space_20210204_models.DeleteWorkspaceResponse:
        """
        @summary 删除工作空间
        
        @return: DeleteWorkspaceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_workspace_with_options(workspace_id, headers, runtime)

    async def delete_workspace_async(
        self,
        workspace_id: str,
    ) -> aiwork_space_20210204_models.DeleteWorkspaceResponse:
        """
        @summary 删除工作空间
        
        @return: DeleteWorkspaceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_workspace_with_options_async(workspace_id, headers, runtime)

    def delete_workspace_resource_with_options(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.DeleteWorkspaceResourceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteWorkspaceResourceResponse:
        """
        @summary 删除工作空间资源
        
        @param request: DeleteWorkspaceResourceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteWorkspaceResourceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.group_name):
            query['GroupName'] = request.group_name
        if not UtilClient.is_unset(request.labels):
            query['Labels'] = request.labels
        if not UtilClient.is_unset(request.option):
            query['Option'] = request.option
        if not UtilClient.is_unset(request.product_type):
            query['ProductType'] = request.product_type
        if not UtilClient.is_unset(request.resource_ids):
            query['ResourceIds'] = request.resource_ids
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteWorkspaceResource',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/resources',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteWorkspaceResourceResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_workspace_resource_with_options_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.DeleteWorkspaceResourceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteWorkspaceResourceResponse:
        """
        @summary 删除工作空间资源
        
        @param request: DeleteWorkspaceResourceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteWorkspaceResourceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.group_name):
            query['GroupName'] = request.group_name
        if not UtilClient.is_unset(request.labels):
            query['Labels'] = request.labels
        if not UtilClient.is_unset(request.option):
            query['Option'] = request.option
        if not UtilClient.is_unset(request.product_type):
            query['ProductType'] = request.product_type
        if not UtilClient.is_unset(request.resource_ids):
            query['ResourceIds'] = request.resource_ids
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteWorkspaceResource',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/resources',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteWorkspaceResourceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_workspace_resource(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.DeleteWorkspaceResourceRequest,
    ) -> aiwork_space_20210204_models.DeleteWorkspaceResourceResponse:
        """
        @summary 删除工作空间资源
        
        @param request: DeleteWorkspaceResourceRequest
        @return: DeleteWorkspaceResourceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_workspace_resource_with_options(workspace_id, request, headers, runtime)

    async def delete_workspace_resource_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.DeleteWorkspaceResourceRequest,
    ) -> aiwork_space_20210204_models.DeleteWorkspaceResourceResponse:
        """
        @summary 删除工作空间资源
        
        @param request: DeleteWorkspaceResourceRequest
        @return: DeleteWorkspaceResourceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_workspace_resource_with_options_async(workspace_id, request, headers, runtime)

    def delete_workspace_roles_with_options(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.DeleteWorkspaceRolesRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteWorkspaceRolesResponse:
        """
        @summary 批量删除工作空间角色
        
        @param request: DeleteWorkspaceRolesRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteWorkspaceRolesResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.role_ids):
            body['RoleIds'] = request.role_ids
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteWorkspaceRoles',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/roles/action/delete',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteWorkspaceRolesResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_workspace_roles_with_options_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.DeleteWorkspaceRolesRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DeleteWorkspaceRolesResponse:
        """
        @summary 批量删除工作空间角色
        
        @param request: DeleteWorkspaceRolesRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteWorkspaceRolesResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.role_ids):
            body['RoleIds'] = request.role_ids
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteWorkspaceRoles',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/roles/action/delete',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DeleteWorkspaceRolesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_workspace_roles(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.DeleteWorkspaceRolesRequest,
    ) -> aiwork_space_20210204_models.DeleteWorkspaceRolesResponse:
        """
        @summary 批量删除工作空间角色
        
        @param request: DeleteWorkspaceRolesRequest
        @return: DeleteWorkspaceRolesResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_workspace_roles_with_options(workspace_id, request, headers, runtime)

    async def delete_workspace_roles_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.DeleteWorkspaceRolesRequest,
    ) -> aiwork_space_20210204_models.DeleteWorkspaceRolesResponse:
        """
        @summary 批量删除工作空间角色
        
        @param request: DeleteWorkspaceRolesRequest
        @return: DeleteWorkspaceRolesResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_workspace_roles_with_options_async(workspace_id, request, headers, runtime)

    def describe_pricing_module_with_options(
        self,
        request: aiwork_space_20210204_models.DescribePricingModuleRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DescribePricingModuleResponse:
        """
        @summary 查询阿里云商品对应模块信息
        
        @param request: DescribePricingModuleRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePricingModuleResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.product_code):
            query['ProductCode'] = request.product_code
        if not UtilClient.is_unset(request.product_type):
            query['ProductType'] = request.product_type
        if not UtilClient.is_unset(request.subscription_type):
            query['SubscriptionType'] = request.subscription_type
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePricingModule',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/proxy/describepricingmodule',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DescribePricingModuleResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_pricing_module_with_options_async(
        self,
        request: aiwork_space_20210204_models.DescribePricingModuleRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.DescribePricingModuleResponse:
        """
        @summary 查询阿里云商品对应模块信息
        
        @param request: DescribePricingModuleRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePricingModuleResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.product_code):
            query['ProductCode'] = request.product_code
        if not UtilClient.is_unset(request.product_type):
            query['ProductType'] = request.product_type
        if not UtilClient.is_unset(request.subscription_type):
            query['SubscriptionType'] = request.subscription_type
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePricingModule',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/proxy/describepricingmodule',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.DescribePricingModuleResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_pricing_module(
        self,
        request: aiwork_space_20210204_models.DescribePricingModuleRequest,
    ) -> aiwork_space_20210204_models.DescribePricingModuleResponse:
        """
        @summary 查询阿里云商品对应模块信息
        
        @param request: DescribePricingModuleRequest
        @return: DescribePricingModuleResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.describe_pricing_module_with_options(request, headers, runtime)

    async def describe_pricing_module_async(
        self,
        request: aiwork_space_20210204_models.DescribePricingModuleRequest,
    ) -> aiwork_space_20210204_models.DescribePricingModuleResponse:
        """
        @summary 查询阿里云商品对应模块信息
        
        @param request: DescribePricingModuleRequest
        @return: DescribePricingModuleResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.describe_pricing_module_with_options_async(request, headers, runtime)

    def get_code_source_with_options(
        self,
        code_source_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetCodeSourceResponse:
        """
        @summary 获取一个代码源配置
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetCodeSourceResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetCodeSource',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/codesources/{OpenApiUtilClient.get_encode_param(code_source_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetCodeSourceResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_code_source_with_options_async(
        self,
        code_source_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetCodeSourceResponse:
        """
        @summary 获取一个代码源配置
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetCodeSourceResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetCodeSource',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/codesources/{OpenApiUtilClient.get_encode_param(code_source_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetCodeSourceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_code_source(
        self,
        code_source_id: str,
    ) -> aiwork_space_20210204_models.GetCodeSourceResponse:
        """
        @summary 获取一个代码源配置
        
        @return: GetCodeSourceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_code_source_with_options(code_source_id, headers, runtime)

    async def get_code_source_async(
        self,
        code_source_id: str,
    ) -> aiwork_space_20210204_models.GetCodeSourceResponse:
        """
        @summary 获取一个代码源配置
        
        @return: GetCodeSourceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_code_source_with_options_async(code_source_id, headers, runtime)

    def get_code_sources_statistics_with_options(
        self,
        request: aiwork_space_20210204_models.GetCodeSourcesStatisticsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetCodeSourcesStatisticsResponse:
        """
        @summary 获取当前工作空间下的CodeSources的统计信息
        
        @param request: GetCodeSourcesStatisticsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetCodeSourcesStatisticsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetCodeSourcesStatistics',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/statistics/codesources',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetCodeSourcesStatisticsResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_code_sources_statistics_with_options_async(
        self,
        request: aiwork_space_20210204_models.GetCodeSourcesStatisticsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetCodeSourcesStatisticsResponse:
        """
        @summary 获取当前工作空间下的CodeSources的统计信息
        
        @param request: GetCodeSourcesStatisticsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetCodeSourcesStatisticsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetCodeSourcesStatistics',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/statistics/codesources',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetCodeSourcesStatisticsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_code_sources_statistics(
        self,
        request: aiwork_space_20210204_models.GetCodeSourcesStatisticsRequest,
    ) -> aiwork_space_20210204_models.GetCodeSourcesStatisticsResponse:
        """
        @summary 获取当前工作空间下的CodeSources的统计信息
        
        @param request: GetCodeSourcesStatisticsRequest
        @return: GetCodeSourcesStatisticsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_code_sources_statistics_with_options(request, headers, runtime)

    async def get_code_sources_statistics_async(
        self,
        request: aiwork_space_20210204_models.GetCodeSourcesStatisticsRequest,
    ) -> aiwork_space_20210204_models.GetCodeSourcesStatisticsResponse:
        """
        @summary 获取当前工作空间下的CodeSources的统计信息
        
        @param request: GetCodeSourcesStatisticsRequest
        @return: GetCodeSourcesStatisticsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_code_sources_statistics_with_options_async(request, headers, runtime)

    def get_collection_with_options(
        self,
        collection_name: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetCollectionResponse:
        """
        @summary 获取Collection
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetCollectionResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetCollection',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/collections/{OpenApiUtilClient.get_encode_param(collection_name)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetCollectionResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_collection_with_options_async(
        self,
        collection_name: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetCollectionResponse:
        """
        @summary 获取Collection
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetCollectionResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetCollection',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/collections/{OpenApiUtilClient.get_encode_param(collection_name)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetCollectionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_collection(
        self,
        collection_name: str,
    ) -> aiwork_space_20210204_models.GetCollectionResponse:
        """
        @summary 获取Collection
        
        @return: GetCollectionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_collection_with_options(collection_name, headers, runtime)

    async def get_collection_async(
        self,
        collection_name: str,
    ) -> aiwork_space_20210204_models.GetCollectionResponse:
        """
        @summary 获取Collection
        
        @return: GetCollectionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_collection_with_options_async(collection_name, headers, runtime)

    def get_dataset_with_options(
        self,
        dataset_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetDatasetResponse:
        """
        @summary 获取数据集
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetDatasetResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetDataset',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/datasets/{OpenApiUtilClient.get_encode_param(dataset_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetDatasetResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_dataset_with_options_async(
        self,
        dataset_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetDatasetResponse:
        """
        @summary 获取数据集
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetDatasetResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetDataset',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/datasets/{OpenApiUtilClient.get_encode_param(dataset_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetDatasetResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_dataset(
        self,
        dataset_id: str,
    ) -> aiwork_space_20210204_models.GetDatasetResponse:
        """
        @summary 获取数据集
        
        @return: GetDatasetResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_dataset_with_options(dataset_id, headers, runtime)

    async def get_dataset_async(
        self,
        dataset_id: str,
    ) -> aiwork_space_20210204_models.GetDatasetResponse:
        """
        @summary 获取数据集
        
        @return: GetDatasetResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_dataset_with_options_async(dataset_id, headers, runtime)

    def get_datasets_statistics_with_options(
        self,
        request: aiwork_space_20210204_models.GetDatasetsStatisticsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetDatasetsStatisticsResponse:
        """
        @summary 获取数据集总数
        
        @param request: GetDatasetsStatisticsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetDatasetsStatisticsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetDatasetsStatistics',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/statistics/datasets',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetDatasetsStatisticsResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_datasets_statistics_with_options_async(
        self,
        request: aiwork_space_20210204_models.GetDatasetsStatisticsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetDatasetsStatisticsResponse:
        """
        @summary 获取数据集总数
        
        @param request: GetDatasetsStatisticsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetDatasetsStatisticsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetDatasetsStatistics',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/statistics/datasets',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetDatasetsStatisticsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_datasets_statistics(
        self,
        request: aiwork_space_20210204_models.GetDatasetsStatisticsRequest,
    ) -> aiwork_space_20210204_models.GetDatasetsStatisticsResponse:
        """
        @summary 获取数据集总数
        
        @param request: GetDatasetsStatisticsRequest
        @return: GetDatasetsStatisticsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_datasets_statistics_with_options(request, headers, runtime)

    async def get_datasets_statistics_async(
        self,
        request: aiwork_space_20210204_models.GetDatasetsStatisticsRequest,
    ) -> aiwork_space_20210204_models.GetDatasetsStatisticsResponse:
        """
        @summary 获取数据集总数
        
        @param request: GetDatasetsStatisticsRequest
        @return: GetDatasetsStatisticsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_datasets_statistics_with_options_async(request, headers, runtime)

    def get_default_workspace_with_options(
        self,
        request: aiwork_space_20210204_models.GetDefaultWorkspaceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetDefaultWorkspaceResponse:
        """
        @summary 获取默认工作空间
        
        @param request: GetDefaultWorkspaceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetDefaultWorkspaceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.verbose):
            query['Verbose'] = request.verbose
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetDefaultWorkspace',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/defaultWorkspaces',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetDefaultWorkspaceResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_default_workspace_with_options_async(
        self,
        request: aiwork_space_20210204_models.GetDefaultWorkspaceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetDefaultWorkspaceResponse:
        """
        @summary 获取默认工作空间
        
        @param request: GetDefaultWorkspaceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetDefaultWorkspaceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.verbose):
            query['Verbose'] = request.verbose
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetDefaultWorkspace',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/defaultWorkspaces',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetDefaultWorkspaceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_default_workspace(
        self,
        request: aiwork_space_20210204_models.GetDefaultWorkspaceRequest,
    ) -> aiwork_space_20210204_models.GetDefaultWorkspaceResponse:
        """
        @summary 获取默认工作空间
        
        @param request: GetDefaultWorkspaceRequest
        @return: GetDefaultWorkspaceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_default_workspace_with_options(request, headers, runtime)

    async def get_default_workspace_async(
        self,
        request: aiwork_space_20210204_models.GetDefaultWorkspaceRequest,
    ) -> aiwork_space_20210204_models.GetDefaultWorkspaceResponse:
        """
        @summary 获取默认工作空间
        
        @param request: GetDefaultWorkspaceRequest
        @return: GetDefaultWorkspaceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_default_workspace_with_options_async(request, headers, runtime)

    def get_experiment_with_options(
        self,
        experiment_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetExperimentResponse:
        """
        @summary 获取实验
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetExperimentResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetExperiment',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/experiments/{OpenApiUtilClient.get_encode_param(experiment_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetExperimentResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_experiment_with_options_async(
        self,
        experiment_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetExperimentResponse:
        """
        @summary 获取实验
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetExperimentResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetExperiment',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/experiments/{OpenApiUtilClient.get_encode_param(experiment_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetExperimentResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_experiment(
        self,
        experiment_id: str,
    ) -> aiwork_space_20210204_models.GetExperimentResponse:
        """
        @summary 获取实验
        
        @return: GetExperimentResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_experiment_with_options(experiment_id, headers, runtime)

    async def get_experiment_async(
        self,
        experiment_id: str,
    ) -> aiwork_space_20210204_models.GetExperimentResponse:
        """
        @summary 获取实验
        
        @return: GetExperimentResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_experiment_with_options_async(experiment_id, headers, runtime)

    def get_image_with_options(
        self,
        image_id: str,
        request: aiwork_space_20210204_models.GetImageRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetImageResponse:
        """
        @summary 获取镜像
        
        @param request: GetImageRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetImageResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.verbose):
            query['Verbose'] = request.verbose
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetImage',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/images/{OpenApiUtilClient.get_encode_param(image_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetImageResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_image_with_options_async(
        self,
        image_id: str,
        request: aiwork_space_20210204_models.GetImageRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetImageResponse:
        """
        @summary 获取镜像
        
        @param request: GetImageRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetImageResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.verbose):
            query['Verbose'] = request.verbose
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetImage',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/images/{OpenApiUtilClient.get_encode_param(image_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetImageResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_image(
        self,
        image_id: str,
        request: aiwork_space_20210204_models.GetImageRequest,
    ) -> aiwork_space_20210204_models.GetImageResponse:
        """
        @summary 获取镜像
        
        @param request: GetImageRequest
        @return: GetImageResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_image_with_options(image_id, request, headers, runtime)

    async def get_image_async(
        self,
        image_id: str,
        request: aiwork_space_20210204_models.GetImageRequest,
    ) -> aiwork_space_20210204_models.GetImageResponse:
        """
        @summary 获取镜像
        
        @param request: GetImageRequest
        @return: GetImageResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_image_with_options_async(image_id, request, headers, runtime)

    def get_images_statistics_with_options(
        self,
        request: aiwork_space_20210204_models.GetImagesStatisticsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetImagesStatisticsResponse:
        """
        @summary 获取镜像统计
        
        @param request: GetImagesStatisticsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetImagesStatisticsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetImagesStatistics',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/statistics/images',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetImagesStatisticsResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_images_statistics_with_options_async(
        self,
        request: aiwork_space_20210204_models.GetImagesStatisticsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetImagesStatisticsResponse:
        """
        @summary 获取镜像统计
        
        @param request: GetImagesStatisticsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetImagesStatisticsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetImagesStatistics',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/statistics/images',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetImagesStatisticsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_images_statistics(
        self,
        request: aiwork_space_20210204_models.GetImagesStatisticsRequest,
    ) -> aiwork_space_20210204_models.GetImagesStatisticsResponse:
        """
        @summary 获取镜像统计
        
        @param request: GetImagesStatisticsRequest
        @return: GetImagesStatisticsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_images_statistics_with_options(request, headers, runtime)

    async def get_images_statistics_async(
        self,
        request: aiwork_space_20210204_models.GetImagesStatisticsRequest,
    ) -> aiwork_space_20210204_models.GetImagesStatisticsResponse:
        """
        @summary 获取镜像统计
        
        @param request: GetImagesStatisticsRequest
        @return: GetImagesStatisticsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_images_statistics_with_options_async(request, headers, runtime)

    def get_instance_job_with_options(
        self,
        instance_job_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetInstanceJobResponse:
        """
        @summary 获取任务
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetInstanceJobResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetInstanceJob',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/instancejobs/{OpenApiUtilClient.get_encode_param(instance_job_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetInstanceJobResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_instance_job_with_options_async(
        self,
        instance_job_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetInstanceJobResponse:
        """
        @summary 获取任务
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetInstanceJobResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetInstanceJob',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/instancejobs/{OpenApiUtilClient.get_encode_param(instance_job_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetInstanceJobResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_instance_job(
        self,
        instance_job_id: str,
    ) -> aiwork_space_20210204_models.GetInstanceJobResponse:
        """
        @summary 获取任务
        
        @return: GetInstanceJobResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_instance_job_with_options(instance_job_id, headers, runtime)

    async def get_instance_job_async(
        self,
        instance_job_id: str,
    ) -> aiwork_space_20210204_models.GetInstanceJobResponse:
        """
        @summary 获取任务
        
        @return: GetInstanceJobResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_instance_job_with_options_async(instance_job_id, headers, runtime)

    def get_instance_statistics_with_options(
        self,
        request: aiwork_space_20210204_models.GetInstanceStatisticsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetInstanceStatisticsResponse:
        """
        @summary 获得工作空间下实例统计数据
        
        @param request: GetInstanceStatisticsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetInstanceStatisticsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.option):
            query['Option'] = request.option
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetInstanceStatistics',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/statistics/instances',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetInstanceStatisticsResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_instance_statistics_with_options_async(
        self,
        request: aiwork_space_20210204_models.GetInstanceStatisticsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetInstanceStatisticsResponse:
        """
        @summary 获得工作空间下实例统计数据
        
        @param request: GetInstanceStatisticsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetInstanceStatisticsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.option):
            query['Option'] = request.option
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetInstanceStatistics',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/statistics/instances',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetInstanceStatisticsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_instance_statistics(
        self,
        request: aiwork_space_20210204_models.GetInstanceStatisticsRequest,
    ) -> aiwork_space_20210204_models.GetInstanceStatisticsResponse:
        """
        @summary 获得工作空间下实例统计数据
        
        @param request: GetInstanceStatisticsRequest
        @return: GetInstanceStatisticsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_instance_statistics_with_options(request, headers, runtime)

    async def get_instance_statistics_async(
        self,
        request: aiwork_space_20210204_models.GetInstanceStatisticsRequest,
    ) -> aiwork_space_20210204_models.GetInstanceStatisticsResponse:
        """
        @summary 获得工作空间下实例统计数据
        
        @param request: GetInstanceStatisticsRequest
        @return: GetInstanceStatisticsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_instance_statistics_with_options_async(request, headers, runtime)

    def get_member_with_options(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.GetMemberRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetMemberResponse:
        """
        @summary 获取成员
        
        @param request: GetMemberRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetMemberResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.member_id):
            query['MemberId'] = request.member_id
        if not UtilClient.is_unset(request.user_id):
            query['UserId'] = request.user_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetMember',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/member',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetMemberResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_member_with_options_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.GetMemberRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetMemberResponse:
        """
        @summary 获取成员
        
        @param request: GetMemberRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetMemberResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.member_id):
            query['MemberId'] = request.member_id
        if not UtilClient.is_unset(request.user_id):
            query['UserId'] = request.user_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetMember',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/member',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetMemberResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_member(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.GetMemberRequest,
    ) -> aiwork_space_20210204_models.GetMemberResponse:
        """
        @summary 获取成员
        
        @param request: GetMemberRequest
        @return: GetMemberResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_member_with_options(workspace_id, request, headers, runtime)

    async def get_member_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.GetMemberRequest,
    ) -> aiwork_space_20210204_models.GetMemberResponse:
        """
        @summary 获取成员
        
        @param request: GetMemberRequest
        @return: GetMemberResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_member_with_options_async(workspace_id, request, headers, runtime)

    def get_model_with_options(
        self,
        model_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetModelResponse:
        """
        @summary 获取模型
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetModelResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetModel',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetModelResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_model_with_options_async(
        self,
        model_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetModelResponse:
        """
        @summary 获取模型
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetModelResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetModel',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetModelResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_model(
        self,
        model_id: str,
    ) -> aiwork_space_20210204_models.GetModelResponse:
        """
        @summary 获取模型
        
        @return: GetModelResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_model_with_options(model_id, headers, runtime)

    async def get_model_async(
        self,
        model_id: str,
    ) -> aiwork_space_20210204_models.GetModelResponse:
        """
        @summary 获取模型
        
        @return: GetModelResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_model_with_options_async(model_id, headers, runtime)

    def get_model_version_with_options(
        self,
        model_id: str,
        version_name: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetModelVersionResponse:
        """
        @summary 获取模型版本
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetModelVersionResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetModelVersion',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}/versions/{OpenApiUtilClient.get_encode_param(version_name)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetModelVersionResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_model_version_with_options_async(
        self,
        model_id: str,
        version_name: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetModelVersionResponse:
        """
        @summary 获取模型版本
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetModelVersionResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetModelVersion',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}/versions/{OpenApiUtilClient.get_encode_param(version_name)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetModelVersionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_model_version(
        self,
        model_id: str,
        version_name: str,
    ) -> aiwork_space_20210204_models.GetModelVersionResponse:
        """
        @summary 获取模型版本
        
        @return: GetModelVersionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_model_version_with_options(model_id, version_name, headers, runtime)

    async def get_model_version_async(
        self,
        model_id: str,
        version_name: str,
    ) -> aiwork_space_20210204_models.GetModelVersionResponse:
        """
        @summary 获取模型版本
        
        @return: GetModelVersionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_model_version_with_options_async(model_id, version_name, headers, runtime)

    def get_pay_as_you_go_price_with_options(
        self,
        request: aiwork_space_20210204_models.GetPayAsYouGoPriceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetPayAsYouGoPriceResponse:
        """
        @summary 查询阿里云商品后付费价格
        
        @param request: GetPayAsYouGoPriceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetPayAsYouGoPriceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.module_list):
            body['ModuleList'] = request.module_list
        if not UtilClient.is_unset(request.product_code):
            body['ProductCode'] = request.product_code
        if not UtilClient.is_unset(request.product_type):
            body['ProductType'] = request.product_type
        if not UtilClient.is_unset(request.subscription_type):
            body['SubscriptionType'] = request.subscription_type
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='GetPayAsYouGoPrice',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/proxy/getpayasyougoprice',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetPayAsYouGoPriceResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_pay_as_you_go_price_with_options_async(
        self,
        request: aiwork_space_20210204_models.GetPayAsYouGoPriceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetPayAsYouGoPriceResponse:
        """
        @summary 查询阿里云商品后付费价格
        
        @param request: GetPayAsYouGoPriceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetPayAsYouGoPriceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.module_list):
            body['ModuleList'] = request.module_list
        if not UtilClient.is_unset(request.product_code):
            body['ProductCode'] = request.product_code
        if not UtilClient.is_unset(request.product_type):
            body['ProductType'] = request.product_type
        if not UtilClient.is_unset(request.subscription_type):
            body['SubscriptionType'] = request.subscription_type
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='GetPayAsYouGoPrice',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/proxy/getpayasyougoprice',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetPayAsYouGoPriceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_pay_as_you_go_price(
        self,
        request: aiwork_space_20210204_models.GetPayAsYouGoPriceRequest,
    ) -> aiwork_space_20210204_models.GetPayAsYouGoPriceResponse:
        """
        @summary 查询阿里云商品后付费价格
        
        @param request: GetPayAsYouGoPriceRequest
        @return: GetPayAsYouGoPriceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_pay_as_you_go_price_with_options(request, headers, runtime)

    async def get_pay_as_you_go_price_async(
        self,
        request: aiwork_space_20210204_models.GetPayAsYouGoPriceRequest,
    ) -> aiwork_space_20210204_models.GetPayAsYouGoPriceResponse:
        """
        @summary 查询阿里云商品后付费价格
        
        @param request: GetPayAsYouGoPriceRequest
        @return: GetPayAsYouGoPriceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_pay_as_you_go_price_with_options_async(request, headers, runtime)

    def get_permission_with_options(
        self,
        workspace_id: str,
        permission_code: str,
        request: aiwork_space_20210204_models.GetPermissionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetPermissionResponse:
        """
        @summary 获取权限，若无权限则返回错误
        
        @param request: GetPermissionRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetPermissionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.accessibility):
            query['Accessibility'] = request.accessibility
        if not UtilClient.is_unset(request.creator):
            query['Creator'] = request.creator
        if not UtilClient.is_unset(request.option):
            query['Option'] = request.option
        if not UtilClient.is_unset(request.resource):
            query['Resource'] = request.resource
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetPermission',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/permissions/{OpenApiUtilClient.get_encode_param(permission_code)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetPermissionResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_permission_with_options_async(
        self,
        workspace_id: str,
        permission_code: str,
        request: aiwork_space_20210204_models.GetPermissionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetPermissionResponse:
        """
        @summary 获取权限，若无权限则返回错误
        
        @param request: GetPermissionRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetPermissionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.accessibility):
            query['Accessibility'] = request.accessibility
        if not UtilClient.is_unset(request.creator):
            query['Creator'] = request.creator
        if not UtilClient.is_unset(request.option):
            query['Option'] = request.option
        if not UtilClient.is_unset(request.resource):
            query['Resource'] = request.resource
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetPermission',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/permissions/{OpenApiUtilClient.get_encode_param(permission_code)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetPermissionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_permission(
        self,
        workspace_id: str,
        permission_code: str,
        request: aiwork_space_20210204_models.GetPermissionRequest,
    ) -> aiwork_space_20210204_models.GetPermissionResponse:
        """
        @summary 获取权限，若无权限则返回错误
        
        @param request: GetPermissionRequest
        @return: GetPermissionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_permission_with_options(workspace_id, permission_code, request, headers, runtime)

    async def get_permission_async(
        self,
        workspace_id: str,
        permission_code: str,
        request: aiwork_space_20210204_models.GetPermissionRequest,
    ) -> aiwork_space_20210204_models.GetPermissionResponse:
        """
        @summary 获取权限，若无权限则返回错误
        
        @param request: GetPermissionRequest
        @return: GetPermissionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_permission_with_options_async(workspace_id, permission_code, request, headers, runtime)

    def get_resource_with_options(
        self,
        resource_id: str,
        workspace_id: str,
        request: aiwork_space_20210204_models.GetResourceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetResourceResponse:
        """
        @summary 获取工作空间资源
        
        @param request: GetResourceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetResourceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetResource',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/resources/{OpenApiUtilClient.get_encode_param(resource_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetResourceResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_resource_with_options_async(
        self,
        resource_id: str,
        workspace_id: str,
        request: aiwork_space_20210204_models.GetResourceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetResourceResponse:
        """
        @summary 获取工作空间资源
        
        @param request: GetResourceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetResourceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetResource',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/resources/{OpenApiUtilClient.get_encode_param(resource_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetResourceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_resource(
        self,
        resource_id: str,
        workspace_id: str,
        request: aiwork_space_20210204_models.GetResourceRequest,
    ) -> aiwork_space_20210204_models.GetResourceResponse:
        """
        @summary 获取工作空间资源
        
        @param request: GetResourceRequest
        @return: GetResourceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_resource_with_options(resource_id, workspace_id, request, headers, runtime)

    async def get_resource_async(
        self,
        resource_id: str,
        workspace_id: str,
        request: aiwork_space_20210204_models.GetResourceRequest,
    ) -> aiwork_space_20210204_models.GetResourceResponse:
        """
        @summary 获取工作空间资源
        
        @param request: GetResourceRequest
        @return: GetResourceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_resource_with_options_async(resource_id, workspace_id, request, headers, runtime)

    def get_role_statistics_with_options(
        self,
        request: aiwork_space_20210204_models.GetRoleStatisticsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetRoleStatisticsResponse:
        """
        @summary 获得角色统计
        
        @param request: GetRoleStatisticsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetRoleStatisticsResponse
        """
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
            pathname=f'/api/v1/statistics/roles',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetRoleStatisticsResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_role_statistics_with_options_async(
        self,
        request: aiwork_space_20210204_models.GetRoleStatisticsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetRoleStatisticsResponse:
        """
        @summary 获得角色统计
        
        @param request: GetRoleStatisticsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetRoleStatisticsResponse
        """
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
            pathname=f'/api/v1/statistics/roles',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetRoleStatisticsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_role_statistics(
        self,
        request: aiwork_space_20210204_models.GetRoleStatisticsRequest,
    ) -> aiwork_space_20210204_models.GetRoleStatisticsResponse:
        """
        @summary 获得角色统计
        
        @param request: GetRoleStatisticsRequest
        @return: GetRoleStatisticsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_role_statistics_with_options(request, headers, runtime)

    async def get_role_statistics_async(
        self,
        request: aiwork_space_20210204_models.GetRoleStatisticsRequest,
    ) -> aiwork_space_20210204_models.GetRoleStatisticsResponse:
        """
        @summary 获得角色统计
        
        @param request: GetRoleStatisticsRequest
        @return: GetRoleStatisticsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_role_statistics_with_options_async(request, headers, runtime)

    def get_service_template_with_options(
        self,
        service_template_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetServiceTemplateResponse:
        """
        @summary 获取服务模版
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetServiceTemplateResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetServiceTemplate',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/servicetemplates/{OpenApiUtilClient.get_encode_param(service_template_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetServiceTemplateResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_service_template_with_options_async(
        self,
        service_template_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetServiceTemplateResponse:
        """
        @summary 获取服务模版
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetServiceTemplateResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetServiceTemplate',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/servicetemplates/{OpenApiUtilClient.get_encode_param(service_template_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetServiceTemplateResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_service_template(
        self,
        service_template_id: str,
    ) -> aiwork_space_20210204_models.GetServiceTemplateResponse:
        """
        @summary 获取服务模版
        
        @return: GetServiceTemplateResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_service_template_with_options(service_template_id, headers, runtime)

    async def get_service_template_async(
        self,
        service_template_id: str,
    ) -> aiwork_space_20210204_models.GetServiceTemplateResponse:
        """
        @summary 获取服务模版
        
        @return: GetServiceTemplateResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_service_template_with_options_async(service_template_id, headers, runtime)

    def get_trial_with_options(
        self,
        trial_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetTrialResponse:
        """
        @summary Get trial
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetTrialResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetTrial',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/trials/{OpenApiUtilClient.get_encode_param(trial_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetTrialResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_trial_with_options_async(
        self,
        trial_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetTrialResponse:
        """
        @summary Get trial
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetTrialResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetTrial',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/trials/{OpenApiUtilClient.get_encode_param(trial_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetTrialResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_trial(
        self,
        trial_id: str,
    ) -> aiwork_space_20210204_models.GetTrialResponse:
        """
        @summary Get trial
        
        @return: GetTrialResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_trial_with_options(trial_id, headers, runtime)

    async def get_trial_async(
        self,
        trial_id: str,
    ) -> aiwork_space_20210204_models.GetTrialResponse:
        """
        @summary Get trial
        
        @return: GetTrialResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_trial_with_options_async(trial_id, headers, runtime)

    def get_workspace_with_options(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.GetWorkspaceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetWorkspaceResponse:
        """
        @summary 获取工作空间
        
        @param request: GetWorkspaceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetWorkspaceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.verbose):
            query['Verbose'] = request.verbose
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetWorkspace',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetWorkspaceResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_workspace_with_options_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.GetWorkspaceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetWorkspaceResponse:
        """
        @summary 获取工作空间
        
        @param request: GetWorkspaceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetWorkspaceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.verbose):
            query['Verbose'] = request.verbose
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetWorkspace',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetWorkspaceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_workspace(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.GetWorkspaceRequest,
    ) -> aiwork_space_20210204_models.GetWorkspaceResponse:
        """
        @summary 获取工作空间
        
        @param request: GetWorkspaceRequest
        @return: GetWorkspaceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_workspace_with_options(workspace_id, request, headers, runtime)

    async def get_workspace_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.GetWorkspaceRequest,
    ) -> aiwork_space_20210204_models.GetWorkspaceResponse:
        """
        @summary 获取工作空间
        
        @param request: GetWorkspaceRequest
        @return: GetWorkspaceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_workspace_with_options_async(workspace_id, request, headers, runtime)

    def get_workspace_role_with_options(
        self,
        workspace_id: str,
        role_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetWorkspaceRoleResponse:
        """
        @summary 获取工作空间角色
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetWorkspaceRoleResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetWorkspaceRole',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/roles/{OpenApiUtilClient.get_encode_param(role_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetWorkspaceRoleResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_workspace_role_with_options_async(
        self,
        workspace_id: str,
        role_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.GetWorkspaceRoleResponse:
        """
        @summary 获取工作空间角色
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetWorkspaceRoleResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetWorkspaceRole',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/roles/{OpenApiUtilClient.get_encode_param(role_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.GetWorkspaceRoleResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_workspace_role(
        self,
        workspace_id: str,
        role_id: str,
    ) -> aiwork_space_20210204_models.GetWorkspaceRoleResponse:
        """
        @summary 获取工作空间角色
        
        @return: GetWorkspaceRoleResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_workspace_role_with_options(workspace_id, role_id, headers, runtime)

    async def get_workspace_role_async(
        self,
        workspace_id: str,
        role_id: str,
    ) -> aiwork_space_20210204_models.GetWorkspaceRoleResponse:
        """
        @summary 获取工作空间角色
        
        @return: GetWorkspaceRoleResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_workspace_role_with_options_async(workspace_id, role_id, headers, runtime)

    def list_code_sources_with_options(
        self,
        request: aiwork_space_20210204_models.ListCodeSourcesRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListCodeSourcesResponse:
        """
        @summary 获取代码源配置列表
        
        @param request: ListCodeSourcesRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListCodeSourcesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.display_name):
            query['DisplayName'] = request.display_name
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListCodeSources',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/codesources',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListCodeSourcesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_code_sources_with_options_async(
        self,
        request: aiwork_space_20210204_models.ListCodeSourcesRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListCodeSourcesResponse:
        """
        @summary 获取代码源配置列表
        
        @param request: ListCodeSourcesRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListCodeSourcesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.display_name):
            query['DisplayName'] = request.display_name
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListCodeSources',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/codesources',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListCodeSourcesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_code_sources(
        self,
        request: aiwork_space_20210204_models.ListCodeSourcesRequest,
    ) -> aiwork_space_20210204_models.ListCodeSourcesResponse:
        """
        @summary 获取代码源配置列表
        
        @param request: ListCodeSourcesRequest
        @return: ListCodeSourcesResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_code_sources_with_options(request, headers, runtime)

    async def list_code_sources_async(
        self,
        request: aiwork_space_20210204_models.ListCodeSourcesRequest,
    ) -> aiwork_space_20210204_models.ListCodeSourcesResponse:
        """
        @summary 获取代码源配置列表
        
        @param request: ListCodeSourcesRequest
        @return: ListCodeSourcesResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_code_sources_with_options_async(request, headers, runtime)

    def list_collections_with_options(
        self,
        request: aiwork_space_20210204_models.ListCollectionsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListCollectionsResponse:
        """
        @summary 获取Collection列表
        
        @param request: ListCollectionsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListCollectionsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListCollections',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/collections',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListCollectionsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_collections_with_options_async(
        self,
        request: aiwork_space_20210204_models.ListCollectionsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListCollectionsResponse:
        """
        @summary 获取Collection列表
        
        @param request: ListCollectionsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListCollectionsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListCollections',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/collections',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListCollectionsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_collections(
        self,
        request: aiwork_space_20210204_models.ListCollectionsRequest,
    ) -> aiwork_space_20210204_models.ListCollectionsResponse:
        """
        @summary 获取Collection列表
        
        @param request: ListCollectionsRequest
        @return: ListCollectionsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_collections_with_options(request, headers, runtime)

    async def list_collections_async(
        self,
        request: aiwork_space_20210204_models.ListCollectionsRequest,
    ) -> aiwork_space_20210204_models.ListCollectionsResponse:
        """
        @summary 获取Collection列表
        
        @param request: ListCollectionsRequest
        @return: ListCollectionsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_collections_with_options_async(request, headers, runtime)

    def list_configs_with_options(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.ListConfigsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListConfigsResponse:
        """
        @summary 获取配置
        
        @param request: ListConfigsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListConfigsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.config_keys):
            query['ConfigKeys'] = request.config_keys
        if not UtilClient.is_unset(request.labels):
            query['Labels'] = request.labels
        if not UtilClient.is_unset(request.verbose):
            query['Verbose'] = request.verbose
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListConfigs',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/configs',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListConfigsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_configs_with_options_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.ListConfigsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListConfigsResponse:
        """
        @summary 获取配置
        
        @param request: ListConfigsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListConfigsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.config_keys):
            query['ConfigKeys'] = request.config_keys
        if not UtilClient.is_unset(request.labels):
            query['Labels'] = request.labels
        if not UtilClient.is_unset(request.verbose):
            query['Verbose'] = request.verbose
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListConfigs',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/configs',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListConfigsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_configs(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.ListConfigsRequest,
    ) -> aiwork_space_20210204_models.ListConfigsResponse:
        """
        @summary 获取配置
        
        @param request: ListConfigsRequest
        @return: ListConfigsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_configs_with_options(workspace_id, request, headers, runtime)

    async def list_configs_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.ListConfigsRequest,
    ) -> aiwork_space_20210204_models.ListConfigsResponse:
        """
        @summary 获取配置
        
        @param request: ListConfigsRequest
        @return: ListConfigsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_configs_with_options_async(workspace_id, request, headers, runtime)

    def list_datasets_with_options(
        self,
        request: aiwork_space_20210204_models.ListDatasetsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListDatasetsResponse:
        """
        @summary 获取数据集列表
        
        @param request: ListDatasetsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListDatasetsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.data_source_types):
            query['DataSourceTypes'] = request.data_source_types
        if not UtilClient.is_unset(request.data_types):
            query['DataTypes'] = request.data_types
        if not UtilClient.is_unset(request.label):
            query['Label'] = request.label
        if not UtilClient.is_unset(request.label_keys):
            query['LabelKeys'] = request.label_keys
        if not UtilClient.is_unset(request.label_values):
            query['LabelValues'] = request.label_values
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.properties):
            query['Properties'] = request.properties
        if not UtilClient.is_unset(request.provider):
            query['Provider'] = request.provider
        if not UtilClient.is_unset(request.source_id):
            query['SourceId'] = request.source_id
        if not UtilClient.is_unset(request.source_types):
            query['SourceTypes'] = request.source_types
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListDatasets',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/datasets',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListDatasetsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_datasets_with_options_async(
        self,
        request: aiwork_space_20210204_models.ListDatasetsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListDatasetsResponse:
        """
        @summary 获取数据集列表
        
        @param request: ListDatasetsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListDatasetsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.data_source_types):
            query['DataSourceTypes'] = request.data_source_types
        if not UtilClient.is_unset(request.data_types):
            query['DataTypes'] = request.data_types
        if not UtilClient.is_unset(request.label):
            query['Label'] = request.label
        if not UtilClient.is_unset(request.label_keys):
            query['LabelKeys'] = request.label_keys
        if not UtilClient.is_unset(request.label_values):
            query['LabelValues'] = request.label_values
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.properties):
            query['Properties'] = request.properties
        if not UtilClient.is_unset(request.provider):
            query['Provider'] = request.provider
        if not UtilClient.is_unset(request.source_id):
            query['SourceId'] = request.source_id
        if not UtilClient.is_unset(request.source_types):
            query['SourceTypes'] = request.source_types
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListDatasets',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/datasets',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListDatasetsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_datasets(
        self,
        request: aiwork_space_20210204_models.ListDatasetsRequest,
    ) -> aiwork_space_20210204_models.ListDatasetsResponse:
        """
        @summary 获取数据集列表
        
        @param request: ListDatasetsRequest
        @return: ListDatasetsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_datasets_with_options(request, headers, runtime)

    async def list_datasets_async(
        self,
        request: aiwork_space_20210204_models.ListDatasetsRequest,
    ) -> aiwork_space_20210204_models.ListDatasetsResponse:
        """
        @summary 获取数据集列表
        
        @param request: ListDatasetsRequest
        @return: ListDatasetsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_datasets_with_options_async(request, headers, runtime)

    def list_experiment_with_options(
        self,
        request: aiwork_space_20210204_models.ListExperimentRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListExperimentResponse:
        """
        @summary 获取实验列表
        
        @param request: ListExperimentRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListExperimentResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.labels):
            query['Labels'] = request.labels
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListExperiment',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/experiments',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListExperimentResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_experiment_with_options_async(
        self,
        request: aiwork_space_20210204_models.ListExperimentRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListExperimentResponse:
        """
        @summary 获取实验列表
        
        @param request: ListExperimentRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListExperimentResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.labels):
            query['Labels'] = request.labels
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListExperiment',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/experiments',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListExperimentResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_experiment(
        self,
        request: aiwork_space_20210204_models.ListExperimentRequest,
    ) -> aiwork_space_20210204_models.ListExperimentResponse:
        """
        @summary 获取实验列表
        
        @param request: ListExperimentRequest
        @return: ListExperimentResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_experiment_with_options(request, headers, runtime)

    async def list_experiment_async(
        self,
        request: aiwork_space_20210204_models.ListExperimentRequest,
    ) -> aiwork_space_20210204_models.ListExperimentResponse:
        """
        @summary 获取实验列表
        
        @param request: ListExperimentRequest
        @return: ListExperimentResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_experiment_with_options_async(request, headers, runtime)

    def list_features_with_options(
        self,
        request: aiwork_space_20210204_models.ListFeaturesRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListFeaturesResponse:
        """
        @summary 列举特性
        
        @param request: ListFeaturesRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListFeaturesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.names):
            query['Names'] = request.names
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFeatures',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/features',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListFeaturesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_features_with_options_async(
        self,
        request: aiwork_space_20210204_models.ListFeaturesRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListFeaturesResponse:
        """
        @summary 列举特性
        
        @param request: ListFeaturesRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListFeaturesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.names):
            query['Names'] = request.names
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFeatures',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/features',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListFeaturesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_features(
        self,
        request: aiwork_space_20210204_models.ListFeaturesRequest,
    ) -> aiwork_space_20210204_models.ListFeaturesResponse:
        """
        @summary 列举特性
        
        @param request: ListFeaturesRequest
        @return: ListFeaturesResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_features_with_options(request, headers, runtime)

    async def list_features_async(
        self,
        request: aiwork_space_20210204_models.ListFeaturesRequest,
    ) -> aiwork_space_20210204_models.ListFeaturesResponse:
        """
        @summary 列举特性
        
        @param request: ListFeaturesRequest
        @return: ListFeaturesResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_features_with_options_async(request, headers, runtime)

    def list_global_permissions_with_options(
        self,
        request: aiwork_space_20210204_models.ListGlobalPermissionsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListGlobalPermissionsResponse:
        """
        @summary 获取用户全局权限
        
        @param request: ListGlobalPermissionsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListGlobalPermissionsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.module_names):
            query['ModuleNames'] = request.module_names
        if not UtilClient.is_unset(request.operation_type):
            query['OperationType'] = request.operation_type
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.resource_types):
            query['ResourceTypes'] = request.resource_types
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListGlobalPermissions',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/permissions',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListGlobalPermissionsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_global_permissions_with_options_async(
        self,
        request: aiwork_space_20210204_models.ListGlobalPermissionsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListGlobalPermissionsResponse:
        """
        @summary 获取用户全局权限
        
        @param request: ListGlobalPermissionsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListGlobalPermissionsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.module_names):
            query['ModuleNames'] = request.module_names
        if not UtilClient.is_unset(request.operation_type):
            query['OperationType'] = request.operation_type
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.resource_types):
            query['ResourceTypes'] = request.resource_types
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListGlobalPermissions',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/permissions',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListGlobalPermissionsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_global_permissions(
        self,
        request: aiwork_space_20210204_models.ListGlobalPermissionsRequest,
    ) -> aiwork_space_20210204_models.ListGlobalPermissionsResponse:
        """
        @summary 获取用户全局权限
        
        @param request: ListGlobalPermissionsRequest
        @return: ListGlobalPermissionsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_global_permissions_with_options(request, headers, runtime)

    async def list_global_permissions_async(
        self,
        request: aiwork_space_20210204_models.ListGlobalPermissionsRequest,
    ) -> aiwork_space_20210204_models.ListGlobalPermissionsResponse:
        """
        @summary 获取用户全局权限
        
        @param request: ListGlobalPermissionsRequest
        @return: ListGlobalPermissionsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_global_permissions_with_options_async(request, headers, runtime)

    def list_image_label_keys_with_options(
        self,
        request: aiwork_space_20210204_models.ListImageLabelKeysRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListImageLabelKeysResponse:
        """
        @summary 列举匹配标签前缀的所有标签
        
        @param request: ListImageLabelKeysRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListImageLabelKeysResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.label_key_prefixes):
            query['LabelKeyPrefixes'] = request.label_key_prefixes
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListImageLabelKeys',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/image/labelkeys',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListImageLabelKeysResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_image_label_keys_with_options_async(
        self,
        request: aiwork_space_20210204_models.ListImageLabelKeysRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListImageLabelKeysResponse:
        """
        @summary 列举匹配标签前缀的所有标签
        
        @param request: ListImageLabelKeysRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListImageLabelKeysResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.label_key_prefixes):
            query['LabelKeyPrefixes'] = request.label_key_prefixes
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListImageLabelKeys',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/image/labelkeys',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListImageLabelKeysResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_image_label_keys(
        self,
        request: aiwork_space_20210204_models.ListImageLabelKeysRequest,
    ) -> aiwork_space_20210204_models.ListImageLabelKeysResponse:
        """
        @summary 列举匹配标签前缀的所有标签
        
        @param request: ListImageLabelKeysRequest
        @return: ListImageLabelKeysResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_image_label_keys_with_options(request, headers, runtime)

    async def list_image_label_keys_async(
        self,
        request: aiwork_space_20210204_models.ListImageLabelKeysRequest,
    ) -> aiwork_space_20210204_models.ListImageLabelKeysResponse:
        """
        @summary 列举匹配标签前缀的所有标签
        
        @param request: ListImageLabelKeysRequest
        @return: ListImageLabelKeysResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_image_label_keys_with_options_async(request, headers, runtime)

    def list_image_labels_with_options(
        self,
        request: aiwork_space_20210204_models.ListImageLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListImageLabelsResponse:
        """
        @summary 列举标签
        
        @param request: ListImageLabelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListImageLabelsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.image_id):
            query['ImageId'] = request.image_id
        if not UtilClient.is_unset(request.label_filter):
            query['LabelFilter'] = request.label_filter
        if not UtilClient.is_unset(request.label_keys):
            query['LabelKeys'] = request.label_keys
        if not UtilClient.is_unset(request.region):
            query['Region'] = request.region
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListImageLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/image/labels',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListImageLabelsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_image_labels_with_options_async(
        self,
        request: aiwork_space_20210204_models.ListImageLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListImageLabelsResponse:
        """
        @summary 列举标签
        
        @param request: ListImageLabelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListImageLabelsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.image_id):
            query['ImageId'] = request.image_id
        if not UtilClient.is_unset(request.label_filter):
            query['LabelFilter'] = request.label_filter
        if not UtilClient.is_unset(request.label_keys):
            query['LabelKeys'] = request.label_keys
        if not UtilClient.is_unset(request.region):
            query['Region'] = request.region
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListImageLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/image/labels',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListImageLabelsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_image_labels(
        self,
        request: aiwork_space_20210204_models.ListImageLabelsRequest,
    ) -> aiwork_space_20210204_models.ListImageLabelsResponse:
        """
        @summary 列举标签
        
        @param request: ListImageLabelsRequest
        @return: ListImageLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_image_labels_with_options(request, headers, runtime)

    async def list_image_labels_async(
        self,
        request: aiwork_space_20210204_models.ListImageLabelsRequest,
    ) -> aiwork_space_20210204_models.ListImageLabelsResponse:
        """
        @summary 列举标签
        
        @param request: ListImageLabelsRequest
        @return: ListImageLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_image_labels_with_options_async(request, headers, runtime)

    def list_images_with_options(
        self,
        request: aiwork_space_20210204_models.ListImagesRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListImagesResponse:
        """
        @summary 列举已注册镜像
        
        @param request: ListImagesRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListImagesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.accessibility):
            query['Accessibility'] = request.accessibility
        if not UtilClient.is_unset(request.labels):
            query['Labels'] = request.labels
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.parent_user_id):
            query['ParentUserId'] = request.parent_user_id
        if not UtilClient.is_unset(request.query):
            query['Query'] = request.query
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.user_id):
            query['UserId'] = request.user_id
        if not UtilClient.is_unset(request.verbose):
            query['Verbose'] = request.verbose
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListImages',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/images',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListImagesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_images_with_options_async(
        self,
        request: aiwork_space_20210204_models.ListImagesRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListImagesResponse:
        """
        @summary 列举已注册镜像
        
        @param request: ListImagesRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListImagesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.accessibility):
            query['Accessibility'] = request.accessibility
        if not UtilClient.is_unset(request.labels):
            query['Labels'] = request.labels
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.parent_user_id):
            query['ParentUserId'] = request.parent_user_id
        if not UtilClient.is_unset(request.query):
            query['Query'] = request.query
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.user_id):
            query['UserId'] = request.user_id
        if not UtilClient.is_unset(request.verbose):
            query['Verbose'] = request.verbose
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListImages',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/images',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListImagesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_images(
        self,
        request: aiwork_space_20210204_models.ListImagesRequest,
    ) -> aiwork_space_20210204_models.ListImagesResponse:
        """
        @summary 列举已注册镜像
        
        @param request: ListImagesRequest
        @return: ListImagesResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_images_with_options(request, headers, runtime)

    async def list_images_async(
        self,
        request: aiwork_space_20210204_models.ListImagesRequest,
    ) -> aiwork_space_20210204_models.ListImagesResponse:
        """
        @summary 列举已注册镜像
        
        @param request: ListImagesRequest
        @return: ListImagesResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_images_with_options_async(request, headers, runtime)

    def list_members_with_options(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.ListMembersRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListMembersResponse:
        """
        @summary 列举工作空间成员
        
        @param request: ListMembersRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListMembersResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.member_name):
            query['MemberName'] = request.member_name
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.roles):
            query['Roles'] = request.roles
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListMembers',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/members',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListMembersResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_members_with_options_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.ListMembersRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListMembersResponse:
        """
        @summary 列举工作空间成员
        
        @param request: ListMembersRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListMembersResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.member_name):
            query['MemberName'] = request.member_name
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.roles):
            query['Roles'] = request.roles
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListMembers',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/members',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListMembersResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_members(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.ListMembersRequest,
    ) -> aiwork_space_20210204_models.ListMembersResponse:
        """
        @summary 列举工作空间成员
        
        @param request: ListMembersRequest
        @return: ListMembersResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_members_with_options(workspace_id, request, headers, runtime)

    async def list_members_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.ListMembersRequest,
    ) -> aiwork_space_20210204_models.ListMembersResponse:
        """
        @summary 列举工作空间成员
        
        @param request: ListMembersRequest
        @return: ListMembersResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_members_with_options_async(workspace_id, request, headers, runtime)

    def list_model_domains_with_options(
        self,
        request: aiwork_space_20210204_models.ListModelDomainsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListModelDomainsResponse:
        """
        @summary 获取模型领域列表
        
        @param request: ListModelDomainsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListModelDomainsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.model_domain_ids):
            query['ModelDomainIds'] = request.model_domain_ids
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListModelDomains',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/modeldomains',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListModelDomainsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_model_domains_with_options_async(
        self,
        request: aiwork_space_20210204_models.ListModelDomainsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListModelDomainsResponse:
        """
        @summary 获取模型领域列表
        
        @param request: ListModelDomainsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListModelDomainsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.model_domain_ids):
            query['ModelDomainIds'] = request.model_domain_ids
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListModelDomains',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/modeldomains',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListModelDomainsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_model_domains(
        self,
        request: aiwork_space_20210204_models.ListModelDomainsRequest,
    ) -> aiwork_space_20210204_models.ListModelDomainsResponse:
        """
        @summary 获取模型领域列表
        
        @param request: ListModelDomainsRequest
        @return: ListModelDomainsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_model_domains_with_options(request, headers, runtime)

    async def list_model_domains_async(
        self,
        request: aiwork_space_20210204_models.ListModelDomainsRequest,
    ) -> aiwork_space_20210204_models.ListModelDomainsResponse:
        """
        @summary 获取模型领域列表
        
        @param request: ListModelDomainsRequest
        @return: ListModelDomainsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_model_domains_with_options_async(request, headers, runtime)

    def list_model_versions_with_options(
        self,
        model_id: str,
        request: aiwork_space_20210204_models.ListModelVersionsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListModelVersionsResponse:
        """
        @summary 获取模型版本列表
        
        @param request: ListModelVersionsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListModelVersionsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.approval_status):
            query['ApprovalStatus'] = request.approval_status
        if not UtilClient.is_unset(request.format_type):
            query['FormatType'] = request.format_type
        if not UtilClient.is_unset(request.framework_type):
            query['FrameworkType'] = request.framework_type
        if not UtilClient.is_unset(request.label):
            query['Label'] = request.label
        if not UtilClient.is_unset(request.label_string):
            query['LabelString'] = request.label_string
        if not UtilClient.is_unset(request.labels):
            query['Labels'] = request.labels
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.source_id):
            query['SourceId'] = request.source_id
        if not UtilClient.is_unset(request.source_type):
            query['SourceType'] = request.source_type
        if not UtilClient.is_unset(request.version_name):
            query['VersionName'] = request.version_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListModelVersions',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}/versions',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListModelVersionsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_model_versions_with_options_async(
        self,
        model_id: str,
        request: aiwork_space_20210204_models.ListModelVersionsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListModelVersionsResponse:
        """
        @summary 获取模型版本列表
        
        @param request: ListModelVersionsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListModelVersionsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.approval_status):
            query['ApprovalStatus'] = request.approval_status
        if not UtilClient.is_unset(request.format_type):
            query['FormatType'] = request.format_type
        if not UtilClient.is_unset(request.framework_type):
            query['FrameworkType'] = request.framework_type
        if not UtilClient.is_unset(request.label):
            query['Label'] = request.label
        if not UtilClient.is_unset(request.label_string):
            query['LabelString'] = request.label_string
        if not UtilClient.is_unset(request.labels):
            query['Labels'] = request.labels
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.source_id):
            query['SourceId'] = request.source_id
        if not UtilClient.is_unset(request.source_type):
            query['SourceType'] = request.source_type
        if not UtilClient.is_unset(request.version_name):
            query['VersionName'] = request.version_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListModelVersions',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}/versions',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListModelVersionsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_model_versions(
        self,
        model_id: str,
        request: aiwork_space_20210204_models.ListModelVersionsRequest,
    ) -> aiwork_space_20210204_models.ListModelVersionsResponse:
        """
        @summary 获取模型版本列表
        
        @param request: ListModelVersionsRequest
        @return: ListModelVersionsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_model_versions_with_options(model_id, request, headers, runtime)

    async def list_model_versions_async(
        self,
        model_id: str,
        request: aiwork_space_20210204_models.ListModelVersionsRequest,
    ) -> aiwork_space_20210204_models.ListModelVersionsResponse:
        """
        @summary 获取模型版本列表
        
        @param request: ListModelVersionsRequest
        @return: ListModelVersionsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_model_versions_with_options_async(model_id, request, headers, runtime)

    def list_models_with_options(
        self,
        request: aiwork_space_20210204_models.ListModelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListModelsResponse:
        """
        @summary 获取模型列表
        
        @param request: ListModelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListModelsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.collections):
            query['Collections'] = request.collections
        if not UtilClient.is_unset(request.domain):
            query['Domain'] = request.domain
        if not UtilClient.is_unset(request.label):
            query['Label'] = request.label
        if not UtilClient.is_unset(request.label_string):
            query['LabelString'] = request.label_string
        if not UtilClient.is_unset(request.labels):
            query['Labels'] = request.labels
        if not UtilClient.is_unset(request.model_name):
            query['ModelName'] = request.model_name
        if not UtilClient.is_unset(request.model_type):
            query['ModelType'] = request.model_type
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.origin):
            query['Origin'] = request.origin
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.provider):
            query['Provider'] = request.provider
        if not UtilClient.is_unset(request.query):
            query['Query'] = request.query
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.task):
            query['Task'] = request.task
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListModels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListModelsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_models_with_options_async(
        self,
        request: aiwork_space_20210204_models.ListModelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListModelsResponse:
        """
        @summary 获取模型列表
        
        @param request: ListModelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListModelsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.collections):
            query['Collections'] = request.collections
        if not UtilClient.is_unset(request.domain):
            query['Domain'] = request.domain
        if not UtilClient.is_unset(request.label):
            query['Label'] = request.label
        if not UtilClient.is_unset(request.label_string):
            query['LabelString'] = request.label_string
        if not UtilClient.is_unset(request.labels):
            query['Labels'] = request.labels
        if not UtilClient.is_unset(request.model_name):
            query['ModelName'] = request.model_name
        if not UtilClient.is_unset(request.model_type):
            query['ModelType'] = request.model_type
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.origin):
            query['Origin'] = request.origin
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.provider):
            query['Provider'] = request.provider
        if not UtilClient.is_unset(request.query):
            query['Query'] = request.query
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.task):
            query['Task'] = request.task
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListModels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListModelsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_models(
        self,
        request: aiwork_space_20210204_models.ListModelsRequest,
    ) -> aiwork_space_20210204_models.ListModelsResponse:
        """
        @summary 获取模型列表
        
        @param request: ListModelsRequest
        @return: ListModelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_models_with_options(request, headers, runtime)

    async def list_models_async(
        self,
        request: aiwork_space_20210204_models.ListModelsRequest,
    ) -> aiwork_space_20210204_models.ListModelsResponse:
        """
        @summary 获取模型列表
        
        @param request: ListModelsRequest
        @return: ListModelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_models_with_options_async(request, headers, runtime)

    def list_module_configs_with_options(
        self,
        request: aiwork_space_20210204_models.ListModuleConfigsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListModuleConfigsResponse:
        """
        @summary 列举PAI云产品的配置
        
        @param request: ListModuleConfigsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListModuleConfigsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.module_codes):
            query['ModuleCodes'] = request.module_codes
        if not UtilClient.is_unset(request.region):
            query['Region'] = request.region
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListModuleConfigs',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/moduleconfigs',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListModuleConfigsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_module_configs_with_options_async(
        self,
        request: aiwork_space_20210204_models.ListModuleConfigsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListModuleConfigsResponse:
        """
        @summary 列举PAI云产品的配置
        
        @param request: ListModuleConfigsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListModuleConfigsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.module_codes):
            query['ModuleCodes'] = request.module_codes
        if not UtilClient.is_unset(request.region):
            query['Region'] = request.region
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListModuleConfigs',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/moduleconfigs',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListModuleConfigsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_module_configs(
        self,
        request: aiwork_space_20210204_models.ListModuleConfigsRequest,
    ) -> aiwork_space_20210204_models.ListModuleConfigsResponse:
        """
        @summary 列举PAI云产品的配置
        
        @param request: ListModuleConfigsRequest
        @return: ListModuleConfigsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_module_configs_with_options(request, headers, runtime)

    async def list_module_configs_async(
        self,
        request: aiwork_space_20210204_models.ListModuleConfigsRequest,
    ) -> aiwork_space_20210204_models.ListModuleConfigsResponse:
        """
        @summary 列举PAI云产品的配置
        
        @param request: ListModuleConfigsRequest
        @return: ListModuleConfigsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_module_configs_with_options_async(request, headers, runtime)

    def list_operation_logs_with_options(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.ListOperationLogsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListOperationLogsResponse:
        """
        @summary 列出操作日志
        
        @param request: ListOperationLogsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListOperationLogsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.entity_status):
            query['EntityStatus'] = request.entity_status
        if not UtilClient.is_unset(request.entity_types):
            query['EntityTypes'] = request.entity_types
        if not UtilClient.is_unset(request.operations):
            query['Operations'] = request.operations
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListOperationLogs',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/logs',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListOperationLogsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_operation_logs_with_options_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.ListOperationLogsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListOperationLogsResponse:
        """
        @summary 列出操作日志
        
        @param request: ListOperationLogsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListOperationLogsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.entity_status):
            query['EntityStatus'] = request.entity_status
        if not UtilClient.is_unset(request.entity_types):
            query['EntityTypes'] = request.entity_types
        if not UtilClient.is_unset(request.operations):
            query['Operations'] = request.operations
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListOperationLogs',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/logs',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListOperationLogsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_operation_logs(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.ListOperationLogsRequest,
    ) -> aiwork_space_20210204_models.ListOperationLogsResponse:
        """
        @summary 列出操作日志
        
        @param request: ListOperationLogsRequest
        @return: ListOperationLogsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_operation_logs_with_options(workspace_id, request, headers, runtime)

    async def list_operation_logs_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.ListOperationLogsRequest,
    ) -> aiwork_space_20210204_models.ListOperationLogsResponse:
        """
        @summary 列出操作日志
        
        @param request: ListOperationLogsRequest
        @return: ListOperationLogsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_operation_logs_with_options_async(workspace_id, request, headers, runtime)

    def list_permissions_with_options(
        self,
        workspace_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListPermissionsResponse:
        """
        @summary 列举权限
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListPermissionsResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='ListPermissions',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/permissions',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListPermissionsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_permissions_with_options_async(
        self,
        workspace_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListPermissionsResponse:
        """
        @summary 列举权限
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListPermissionsResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='ListPermissions',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/permissions',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListPermissionsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_permissions(
        self,
        workspace_id: str,
    ) -> aiwork_space_20210204_models.ListPermissionsResponse:
        """
        @summary 列举权限
        
        @return: ListPermissionsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_permissions_with_options(workspace_id, headers, runtime)

    async def list_permissions_async(
        self,
        workspace_id: str,
    ) -> aiwork_space_20210204_models.ListPermissionsResponse:
        """
        @summary 列举权限
        
        @return: ListPermissionsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_permissions_with_options_async(workspace_id, headers, runtime)

    def list_product_authorizations_with_options(
        self,
        request: aiwork_space_20210204_models.ListProductAuthorizationsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListProductAuthorizationsResponse:
        """
        @summary 获取产品授权
        
        @param request: ListProductAuthorizationsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListProductAuthorizationsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.ram_role_names):
            query['RamRoleNames'] = request.ram_role_names
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListProductAuthorizations',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/productauthorizations',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListProductAuthorizationsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_product_authorizations_with_options_async(
        self,
        request: aiwork_space_20210204_models.ListProductAuthorizationsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListProductAuthorizationsResponse:
        """
        @summary 获取产品授权
        
        @param request: ListProductAuthorizationsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListProductAuthorizationsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.ram_role_names):
            query['RamRoleNames'] = request.ram_role_names
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListProductAuthorizations',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/productauthorizations',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListProductAuthorizationsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_product_authorizations(
        self,
        request: aiwork_space_20210204_models.ListProductAuthorizationsRequest,
    ) -> aiwork_space_20210204_models.ListProductAuthorizationsResponse:
        """
        @summary 获取产品授权
        
        @param request: ListProductAuthorizationsRequest
        @return: ListProductAuthorizationsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_product_authorizations_with_options(request, headers, runtime)

    async def list_product_authorizations_async(
        self,
        request: aiwork_space_20210204_models.ListProductAuthorizationsRequest,
    ) -> aiwork_space_20210204_models.ListProductAuthorizationsResponse:
        """
        @summary 获取产品授权
        
        @param request: ListProductAuthorizationsRequest
        @return: ListProductAuthorizationsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_product_authorizations_with_options_async(request, headers, runtime)

    def list_products_with_options(
        self,
        request: aiwork_space_20210204_models.ListProductsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListProductsResponse:
        """
        @summary 列举产品
        
        @param request: ListProductsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListProductsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.product_codes):
            query['ProductCodes'] = request.product_codes
        if not UtilClient.is_unset(request.service_codes):
            query['ServiceCodes'] = request.service_codes
        if not UtilClient.is_unset(request.verbose):
            query['Verbose'] = request.verbose
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListProducts',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/products',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListProductsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_products_with_options_async(
        self,
        request: aiwork_space_20210204_models.ListProductsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListProductsResponse:
        """
        @summary 列举产品
        
        @param request: ListProductsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListProductsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.product_codes):
            query['ProductCodes'] = request.product_codes
        if not UtilClient.is_unset(request.service_codes):
            query['ServiceCodes'] = request.service_codes
        if not UtilClient.is_unset(request.verbose):
            query['Verbose'] = request.verbose
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListProducts',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/products',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListProductsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_products(
        self,
        request: aiwork_space_20210204_models.ListProductsRequest,
    ) -> aiwork_space_20210204_models.ListProductsResponse:
        """
        @summary 列举产品
        
        @param request: ListProductsRequest
        @return: ListProductsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_products_with_options(request, headers, runtime)

    async def list_products_async(
        self,
        request: aiwork_space_20210204_models.ListProductsRequest,
    ) -> aiwork_space_20210204_models.ListProductsResponse:
        """
        @summary 列举产品
        
        @param request: ListProductsRequest
        @return: ListProductsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_products_with_options_async(request, headers, runtime)

    def list_quotas_with_options(
        self,
        request: aiwork_space_20210204_models.ListQuotasRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListQuotasResponse:
        """
        @summary 获取已有配额列表
        
        @param request: ListQuotasRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListQuotasResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListQuotas',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListQuotasResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_quotas_with_options_async(
        self,
        request: aiwork_space_20210204_models.ListQuotasRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListQuotasResponse:
        """
        @summary 获取已有配额列表
        
        @param request: ListQuotasRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListQuotasResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListQuotas',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListQuotasResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_quotas(
        self,
        request: aiwork_space_20210204_models.ListQuotasRequest,
    ) -> aiwork_space_20210204_models.ListQuotasResponse:
        """
        @summary 获取已有配额列表
        
        @param request: ListQuotasRequest
        @return: ListQuotasResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_quotas_with_options(request, headers, runtime)

    async def list_quotas_async(
        self,
        request: aiwork_space_20210204_models.ListQuotasRequest,
    ) -> aiwork_space_20210204_models.ListQuotasResponse:
        """
        @summary 获取已有配额列表
        
        @param request: ListQuotasRequest
        @return: ListQuotasResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_quotas_with_options_async(request, headers, runtime)

    def list_resources_with_options(
        self,
        request: aiwork_space_20210204_models.ListResourcesRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListResourcesResponse:
        """
        @summary 列举工作空间资源
        
        @param request: ListResourcesRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListResourcesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.group_name):
            query['GroupName'] = request.group_name
        if not UtilClient.is_unset(request.labels):
            query['Labels'] = request.labels
        if not UtilClient.is_unset(request.option):
            query['Option'] = request.option
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.product_types):
            query['ProductTypes'] = request.product_types
        if not UtilClient.is_unset(request.quota_ids):
            query['QuotaIds'] = request.quota_ids
        if not UtilClient.is_unset(request.resource_name):
            query['ResourceName'] = request.resource_name
        if not UtilClient.is_unset(request.resource_types):
            query['ResourceTypes'] = request.resource_types
        if not UtilClient.is_unset(request.verbose):
            query['Verbose'] = request.verbose
        if not UtilClient.is_unset(request.verbose_fields):
            query['VerboseFields'] = request.verbose_fields
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListResources',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/resources',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListResourcesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_resources_with_options_async(
        self,
        request: aiwork_space_20210204_models.ListResourcesRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListResourcesResponse:
        """
        @summary 列举工作空间资源
        
        @param request: ListResourcesRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListResourcesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.group_name):
            query['GroupName'] = request.group_name
        if not UtilClient.is_unset(request.labels):
            query['Labels'] = request.labels
        if not UtilClient.is_unset(request.option):
            query['Option'] = request.option
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.product_types):
            query['ProductTypes'] = request.product_types
        if not UtilClient.is_unset(request.quota_ids):
            query['QuotaIds'] = request.quota_ids
        if not UtilClient.is_unset(request.resource_name):
            query['ResourceName'] = request.resource_name
        if not UtilClient.is_unset(request.resource_types):
            query['ResourceTypes'] = request.resource_types
        if not UtilClient.is_unset(request.verbose):
            query['Verbose'] = request.verbose
        if not UtilClient.is_unset(request.verbose_fields):
            query['VerboseFields'] = request.verbose_fields
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListResources',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/resources',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListResourcesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_resources(
        self,
        request: aiwork_space_20210204_models.ListResourcesRequest,
    ) -> aiwork_space_20210204_models.ListResourcesResponse:
        """
        @summary 列举工作空间资源
        
        @param request: ListResourcesRequest
        @return: ListResourcesResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_resources_with_options(request, headers, runtime)

    async def list_resources_async(
        self,
        request: aiwork_space_20210204_models.ListResourcesRequest,
    ) -> aiwork_space_20210204_models.ListResourcesResponse:
        """
        @summary 列举工作空间资源
        
        @param request: ListResourcesRequest
        @return: ListResourcesResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_resources_with_options_async(request, headers, runtime)

    def list_service_templates_with_options(
        self,
        request: aiwork_space_20210204_models.ListServiceTemplatesRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListServiceTemplatesResponse:
        """
        @summary 获取服务模版列表
        
        @param request: ListServiceTemplatesRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListServiceTemplatesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.label):
            query['Label'] = request.label
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.provider):
            query['Provider'] = request.provider
        if not UtilClient.is_unset(request.query):
            query['Query'] = request.query
        if not UtilClient.is_unset(request.service_template_name):
            query['ServiceTemplateName'] = request.service_template_name
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListServiceTemplates',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/servicetemplates',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListServiceTemplatesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_service_templates_with_options_async(
        self,
        request: aiwork_space_20210204_models.ListServiceTemplatesRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListServiceTemplatesResponse:
        """
        @summary 获取服务模版列表
        
        @param request: ListServiceTemplatesRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListServiceTemplatesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.label):
            query['Label'] = request.label
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.provider):
            query['Provider'] = request.provider
        if not UtilClient.is_unset(request.query):
            query['Query'] = request.query
        if not UtilClient.is_unset(request.service_template_name):
            query['ServiceTemplateName'] = request.service_template_name
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListServiceTemplates',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/servicetemplates',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListServiceTemplatesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_service_templates(
        self,
        request: aiwork_space_20210204_models.ListServiceTemplatesRequest,
    ) -> aiwork_space_20210204_models.ListServiceTemplatesResponse:
        """
        @summary 获取服务模版列表
        
        @param request: ListServiceTemplatesRequest
        @return: ListServiceTemplatesResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_service_templates_with_options(request, headers, runtime)

    async def list_service_templates_async(
        self,
        request: aiwork_space_20210204_models.ListServiceTemplatesRequest,
    ) -> aiwork_space_20210204_models.ListServiceTemplatesResponse:
        """
        @summary 获取服务模版列表
        
        @param request: ListServiceTemplatesRequest
        @return: ListServiceTemplatesResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_service_templates_with_options_async(request, headers, runtime)

    def list_user_configs_with_options(
        self,
        request: aiwork_space_20210204_models.ListUserConfigsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListUserConfigsResponse:
        """
        @summary 获取用户配置
        
        @param request: ListUserConfigsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListUserConfigsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.category_names):
            query['CategoryNames'] = request.category_names
        if not UtilClient.is_unset(request.config_keys):
            query['ConfigKeys'] = request.config_keys
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListUserConfigs',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/userconfigs',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListUserConfigsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_user_configs_with_options_async(
        self,
        request: aiwork_space_20210204_models.ListUserConfigsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListUserConfigsResponse:
        """
        @summary 获取用户配置
        
        @param request: ListUserConfigsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListUserConfigsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.category_names):
            query['CategoryNames'] = request.category_names
        if not UtilClient.is_unset(request.config_keys):
            query['ConfigKeys'] = request.config_keys
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListUserConfigs',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/userconfigs',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListUserConfigsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_user_configs(
        self,
        request: aiwork_space_20210204_models.ListUserConfigsRequest,
    ) -> aiwork_space_20210204_models.ListUserConfigsResponse:
        """
        @summary 获取用户配置
        
        @param request: ListUserConfigsRequest
        @return: ListUserConfigsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_user_configs_with_options(request, headers, runtime)

    async def list_user_configs_async(
        self,
        request: aiwork_space_20210204_models.ListUserConfigsRequest,
    ) -> aiwork_space_20210204_models.ListUserConfigsResponse:
        """
        @summary 获取用户配置
        
        @param request: ListUserConfigsRequest
        @return: ListUserConfigsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_user_configs_with_options_async(request, headers, runtime)

    def list_users_with_options(
        self,
        request: aiwork_space_20210204_models.ListUsersRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListUsersResponse:
        """
        @summary 列出用户
        
        @param request: ListUsersRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListUsersResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.account_types):
            query['AccountTypes'] = request.account_types
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.user_ids):
            query['UserIds'] = request.user_ids
        if not UtilClient.is_unset(request.user_name):
            query['UserName'] = request.user_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListUsers',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/users',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListUsersResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_users_with_options_async(
        self,
        request: aiwork_space_20210204_models.ListUsersRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListUsersResponse:
        """
        @summary 列出用户
        
        @param request: ListUsersRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListUsersResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.account_types):
            query['AccountTypes'] = request.account_types
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.user_ids):
            query['UserIds'] = request.user_ids
        if not UtilClient.is_unset(request.user_name):
            query['UserName'] = request.user_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListUsers',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/users',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListUsersResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_users(
        self,
        request: aiwork_space_20210204_models.ListUsersRequest,
    ) -> aiwork_space_20210204_models.ListUsersResponse:
        """
        @summary 列出用户
        
        @param request: ListUsersRequest
        @return: ListUsersResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_users_with_options(request, headers, runtime)

    async def list_users_async(
        self,
        request: aiwork_space_20210204_models.ListUsersRequest,
    ) -> aiwork_space_20210204_models.ListUsersResponse:
        """
        @summary 列出用户
        
        @param request: ListUsersRequest
        @return: ListUsersResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_users_with_options_async(request, headers, runtime)

    def list_workspace_permissions_with_options(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.ListWorkspacePermissionsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListWorkspacePermissionsResponse:
        """
        @summary 批量获取权限
        
        @param request: ListWorkspacePermissionsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWorkspacePermissionsResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.options):
            body['Options'] = request.options
        if not UtilClient.is_unset(request.permissions):
            body['Permissions'] = request.permissions
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ListWorkspacePermissions',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/permissions/action/list',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListWorkspacePermissionsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_workspace_permissions_with_options_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.ListWorkspacePermissionsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListWorkspacePermissionsResponse:
        """
        @summary 批量获取权限
        
        @param request: ListWorkspacePermissionsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWorkspacePermissionsResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.options):
            body['Options'] = request.options
        if not UtilClient.is_unset(request.permissions):
            body['Permissions'] = request.permissions
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ListWorkspacePermissions',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/permissions/action/list',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListWorkspacePermissionsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_workspace_permissions(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.ListWorkspacePermissionsRequest,
    ) -> aiwork_space_20210204_models.ListWorkspacePermissionsResponse:
        """
        @summary 批量获取权限
        
        @param request: ListWorkspacePermissionsRequest
        @return: ListWorkspacePermissionsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_workspace_permissions_with_options(workspace_id, request, headers, runtime)

    async def list_workspace_permissions_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.ListWorkspacePermissionsRequest,
    ) -> aiwork_space_20210204_models.ListWorkspacePermissionsResponse:
        """
        @summary 批量获取权限
        
        @param request: ListWorkspacePermissionsRequest
        @return: ListWorkspacePermissionsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_workspace_permissions_with_options_async(workspace_id, request, headers, runtime)

    def list_workspace_roles_with_options(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.ListWorkspaceRolesRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListWorkspaceRolesResponse:
        """
        @summary 列举工作空间角色
        
        @param request: ListWorkspaceRolesRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWorkspaceRolesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.role_ids):
            query['RoleIds'] = request.role_ids
        if not UtilClient.is_unset(request.role_name):
            query['RoleName'] = request.role_name
        if not UtilClient.is_unset(request.role_type):
            query['RoleType'] = request.role_type
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        if not UtilClient.is_unset(request.verbose_fields):
            query['VerboseFields'] = request.verbose_fields
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWorkspaceRoles',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/roles',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListWorkspaceRolesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_workspace_roles_with_options_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.ListWorkspaceRolesRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListWorkspaceRolesResponse:
        """
        @summary 列举工作空间角色
        
        @param request: ListWorkspaceRolesRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWorkspaceRolesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.role_ids):
            query['RoleIds'] = request.role_ids
        if not UtilClient.is_unset(request.role_name):
            query['RoleName'] = request.role_name
        if not UtilClient.is_unset(request.role_type):
            query['RoleType'] = request.role_type
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        if not UtilClient.is_unset(request.verbose_fields):
            query['VerboseFields'] = request.verbose_fields
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWorkspaceRoles',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/roles',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListWorkspaceRolesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_workspace_roles(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.ListWorkspaceRolesRequest,
    ) -> aiwork_space_20210204_models.ListWorkspaceRolesResponse:
        """
        @summary 列举工作空间角色
        
        @param request: ListWorkspaceRolesRequest
        @return: ListWorkspaceRolesResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_workspace_roles_with_options(workspace_id, request, headers, runtime)

    async def list_workspace_roles_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.ListWorkspaceRolesRequest,
    ) -> aiwork_space_20210204_models.ListWorkspaceRolesResponse:
        """
        @summary 列举工作空间角色
        
        @param request: ListWorkspaceRolesRequest
        @return: ListWorkspaceRolesResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_workspace_roles_with_options_async(workspace_id, request, headers, runtime)

    def list_workspace_users_with_options(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.ListWorkspaceUsersRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListWorkspaceUsersResponse:
        """
        @summary 列出工作空间的可变为成员的用户
        
        @param request: ListWorkspaceUsersRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWorkspaceUsersResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.user_name):
            query['UserName'] = request.user_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWorkspaceUsers',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/users',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListWorkspaceUsersResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_workspace_users_with_options_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.ListWorkspaceUsersRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListWorkspaceUsersResponse:
        """
        @summary 列出工作空间的可变为成员的用户
        
        @param request: ListWorkspaceUsersRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWorkspaceUsersResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.user_name):
            query['UserName'] = request.user_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWorkspaceUsers',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/users',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListWorkspaceUsersResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_workspace_users(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.ListWorkspaceUsersRequest,
    ) -> aiwork_space_20210204_models.ListWorkspaceUsersResponse:
        """
        @summary 列出工作空间的可变为成员的用户
        
        @param request: ListWorkspaceUsersRequest
        @return: ListWorkspaceUsersResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_workspace_users_with_options(workspace_id, request, headers, runtime)

    async def list_workspace_users_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.ListWorkspaceUsersRequest,
    ) -> aiwork_space_20210204_models.ListWorkspaceUsersResponse:
        """
        @summary 列出工作空间的可变为成员的用户
        
        @param request: ListWorkspaceUsersRequest
        @return: ListWorkspaceUsersResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_workspace_users_with_options_async(workspace_id, request, headers, runtime)

    def list_workspaces_with_options(
        self,
        request: aiwork_space_20210204_models.ListWorkspacesRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListWorkspacesResponse:
        """
        @summary 获得工作空间列表
        
        @param request: ListWorkspacesRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWorkspacesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.fields):
            query['Fields'] = request.fields
        if not UtilClient.is_unset(request.module_list):
            query['ModuleList'] = request.module_list
        if not UtilClient.is_unset(request.option):
            query['Option'] = request.option
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        if not UtilClient.is_unset(request.verbose):
            query['Verbose'] = request.verbose
        if not UtilClient.is_unset(request.workspace_ids):
            query['WorkspaceIds'] = request.workspace_ids
        if not UtilClient.is_unset(request.workspace_name):
            query['WorkspaceName'] = request.workspace_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWorkspaces',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListWorkspacesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_workspaces_with_options_async(
        self,
        request: aiwork_space_20210204_models.ListWorkspacesRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.ListWorkspacesResponse:
        """
        @summary 获得工作空间列表
        
        @param request: ListWorkspacesRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWorkspacesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.fields):
            query['Fields'] = request.fields
        if not UtilClient.is_unset(request.module_list):
            query['ModuleList'] = request.module_list
        if not UtilClient.is_unset(request.option):
            query['Option'] = request.option
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        if not UtilClient.is_unset(request.verbose):
            query['Verbose'] = request.verbose
        if not UtilClient.is_unset(request.workspace_ids):
            query['WorkspaceIds'] = request.workspace_ids
        if not UtilClient.is_unset(request.workspace_name):
            query['WorkspaceName'] = request.workspace_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWorkspaces',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.ListWorkspacesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_workspaces(
        self,
        request: aiwork_space_20210204_models.ListWorkspacesRequest,
    ) -> aiwork_space_20210204_models.ListWorkspacesResponse:
        """
        @summary 获得工作空间列表
        
        @param request: ListWorkspacesRequest
        @return: ListWorkspacesResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_workspaces_with_options(request, headers, runtime)

    async def list_workspaces_async(
        self,
        request: aiwork_space_20210204_models.ListWorkspacesRequest,
    ) -> aiwork_space_20210204_models.ListWorkspacesResponse:
        """
        @summary 获得工作空间列表
        
        @param request: ListWorkspacesRequest
        @return: ListWorkspacesResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_workspaces_with_options_async(request, headers, runtime)

    def migrate_datasets_with_options(
        self,
        request: aiwork_space_20210204_models.MigrateDatasetsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.MigrateDatasetsResponse:
        """
        @summary 迁移数据集
        
        @param request: MigrateDatasetsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: MigrateDatasetsResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.count):
            body['Count'] = request.count
        if not UtilClient.is_unset(request.dataset_id):
            body['DatasetId'] = request.dataset_id
        if not UtilClient.is_unset(request.if_force):
            body['IfForce'] = request.if_force
        if not UtilClient.is_unset(request.owner_id):
            body['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.workspace_id):
            body['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='MigrateDatasets',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/datasets/migrate',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.MigrateDatasetsResponse(),
            self.call_api(params, req, runtime)
        )

    async def migrate_datasets_with_options_async(
        self,
        request: aiwork_space_20210204_models.MigrateDatasetsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.MigrateDatasetsResponse:
        """
        @summary 迁移数据集
        
        @param request: MigrateDatasetsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: MigrateDatasetsResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.count):
            body['Count'] = request.count
        if not UtilClient.is_unset(request.dataset_id):
            body['DatasetId'] = request.dataset_id
        if not UtilClient.is_unset(request.if_force):
            body['IfForce'] = request.if_force
        if not UtilClient.is_unset(request.owner_id):
            body['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.workspace_id):
            body['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='MigrateDatasets',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/datasets/migrate',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.MigrateDatasetsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def migrate_datasets(
        self,
        request: aiwork_space_20210204_models.MigrateDatasetsRequest,
    ) -> aiwork_space_20210204_models.MigrateDatasetsResponse:
        """
        @summary 迁移数据集
        
        @param request: MigrateDatasetsRequest
        @return: MigrateDatasetsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.migrate_datasets_with_options(request, headers, runtime)

    async def migrate_datasets_async(
        self,
        request: aiwork_space_20210204_models.MigrateDatasetsRequest,
    ) -> aiwork_space_20210204_models.MigrateDatasetsResponse:
        """
        @summary 迁移数据集
        
        @param request: MigrateDatasetsRequest
        @return: MigrateDatasetsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.migrate_datasets_with_options_async(request, headers, runtime)

    def publish_code_source_with_options(
        self,
        code_source_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.PublishCodeSourceResponse:
        """
        @summary 发布一个代码源配置为本工作空间下所有人可见
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: PublishCodeSourceResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='PublishCodeSource',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/codesources/{OpenApiUtilClient.get_encode_param(code_source_id)}/publish',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.PublishCodeSourceResponse(),
            self.call_api(params, req, runtime)
        )

    async def publish_code_source_with_options_async(
        self,
        code_source_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.PublishCodeSourceResponse:
        """
        @summary 发布一个代码源配置为本工作空间下所有人可见
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: PublishCodeSourceResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='PublishCodeSource',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/codesources/{OpenApiUtilClient.get_encode_param(code_source_id)}/publish',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.PublishCodeSourceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def publish_code_source(
        self,
        code_source_id: str,
    ) -> aiwork_space_20210204_models.PublishCodeSourceResponse:
        """
        @summary 发布一个代码源配置为本工作空间下所有人可见
        
        @return: PublishCodeSourceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.publish_code_source_with_options(code_source_id, headers, runtime)

    async def publish_code_source_async(
        self,
        code_source_id: str,
    ) -> aiwork_space_20210204_models.PublishCodeSourceResponse:
        """
        @summary 发布一个代码源配置为本工作空间下所有人可见
        
        @return: PublishCodeSourceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.publish_code_source_with_options_async(code_source_id, headers, runtime)

    def publish_dataset_with_options(
        self,
        dataset_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.PublishDatasetResponse:
        """
        @summary 更新数据集
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: PublishDatasetResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='PublishDataset',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/datasets/{OpenApiUtilClient.get_encode_param(dataset_id)}/publish',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.PublishDatasetResponse(),
            self.call_api(params, req, runtime)
        )

    async def publish_dataset_with_options_async(
        self,
        dataset_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.PublishDatasetResponse:
        """
        @summary 更新数据集
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: PublishDatasetResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='PublishDataset',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/datasets/{OpenApiUtilClient.get_encode_param(dataset_id)}/publish',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.PublishDatasetResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def publish_dataset(
        self,
        dataset_id: str,
    ) -> aiwork_space_20210204_models.PublishDatasetResponse:
        """
        @summary 更新数据集
        
        @return: PublishDatasetResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.publish_dataset_with_options(dataset_id, headers, runtime)

    async def publish_dataset_async(
        self,
        dataset_id: str,
    ) -> aiwork_space_20210204_models.PublishDatasetResponse:
        """
        @summary 更新数据集
        
        @return: PublishDatasetResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.publish_dataset_with_options_async(dataset_id, headers, runtime)

    def publish_image_with_options(
        self,
        image_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.PublishImageResponse:
        """
        @summary 发布 Image
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: PublishImageResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='PublishImage',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/images/{OpenApiUtilClient.get_encode_param(image_id)}/publish',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.PublishImageResponse(),
            self.call_api(params, req, runtime)
        )

    async def publish_image_with_options_async(
        self,
        image_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.PublishImageResponse:
        """
        @summary 发布 Image
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: PublishImageResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='PublishImage',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/images/{OpenApiUtilClient.get_encode_param(image_id)}/publish',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.PublishImageResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def publish_image(
        self,
        image_id: str,
    ) -> aiwork_space_20210204_models.PublishImageResponse:
        """
        @summary 发布 Image
        
        @return: PublishImageResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.publish_image_with_options(image_id, headers, runtime)

    async def publish_image_async(
        self,
        image_id: str,
    ) -> aiwork_space_20210204_models.PublishImageResponse:
        """
        @summary 发布 Image
        
        @return: PublishImageResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.publish_image_with_options_async(image_id, headers, runtime)

    def remove_image_with_options(
        self,
        image_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.RemoveImageResponse:
        """
        @summary 删除 Image
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: RemoveImageResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='RemoveImage',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/images/{OpenApiUtilClient.get_encode_param(image_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.RemoveImageResponse(),
            self.call_api(params, req, runtime)
        )

    async def remove_image_with_options_async(
        self,
        image_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.RemoveImageResponse:
        """
        @summary 删除 Image
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: RemoveImageResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='RemoveImage',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/images/{OpenApiUtilClient.get_encode_param(image_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.RemoveImageResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def remove_image(
        self,
        image_id: str,
    ) -> aiwork_space_20210204_models.RemoveImageResponse:
        """
        @summary 删除 Image
        
        @return: RemoveImageResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.remove_image_with_options(image_id, headers, runtime)

    async def remove_image_async(
        self,
        image_id: str,
    ) -> aiwork_space_20210204_models.RemoveImageResponse:
        """
        @summary 删除 Image
        
        @return: RemoveImageResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.remove_image_with_options_async(image_id, headers, runtime)

    def remove_image_labels_with_options(
        self,
        image_id: str,
        label_key: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.RemoveImageLabelsResponse:
        """
        @summary 删除 Image 的标签
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: RemoveImageLabelsResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='RemoveImageLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/images/{OpenApiUtilClient.get_encode_param(image_id)}/labels/{OpenApiUtilClient.get_encode_param(label_key)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.RemoveImageLabelsResponse(),
            self.call_api(params, req, runtime)
        )

    async def remove_image_labels_with_options_async(
        self,
        image_id: str,
        label_key: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.RemoveImageLabelsResponse:
        """
        @summary 删除 Image 的标签
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: RemoveImageLabelsResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='RemoveImageLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/images/{OpenApiUtilClient.get_encode_param(image_id)}/labels/{OpenApiUtilClient.get_encode_param(label_key)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.RemoveImageLabelsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def remove_image_labels(
        self,
        image_id: str,
        label_key: str,
    ) -> aiwork_space_20210204_models.RemoveImageLabelsResponse:
        """
        @summary 删除 Image 的标签
        
        @return: RemoveImageLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.remove_image_labels_with_options(image_id, label_key, headers, runtime)

    async def remove_image_labels_async(
        self,
        image_id: str,
        label_key: str,
    ) -> aiwork_space_20210204_models.RemoveImageLabelsResponse:
        """
        @summary 删除 Image 的标签
        
        @return: RemoveImageLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.remove_image_labels_with_options_async(image_id, label_key, headers, runtime)

    def remove_member_role_with_options(
        self,
        workspace_id: str,
        member_id: str,
        role_name: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.RemoveMemberRoleResponse:
        """
        @summary 删除成员角色
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: RemoveMemberRoleResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='RemoveMemberRole',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/members/{OpenApiUtilClient.get_encode_param(member_id)}/roles/{OpenApiUtilClient.get_encode_param(role_name)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.RemoveMemberRoleResponse(),
            self.call_api(params, req, runtime)
        )

    async def remove_member_role_with_options_async(
        self,
        workspace_id: str,
        member_id: str,
        role_name: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.RemoveMemberRoleResponse:
        """
        @summary 删除成员角色
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: RemoveMemberRoleResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='RemoveMemberRole',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/members/{OpenApiUtilClient.get_encode_param(member_id)}/roles/{OpenApiUtilClient.get_encode_param(role_name)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.RemoveMemberRoleResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def remove_member_role(
        self,
        workspace_id: str,
        member_id: str,
        role_name: str,
    ) -> aiwork_space_20210204_models.RemoveMemberRoleResponse:
        """
        @summary 删除成员角色
        
        @return: RemoveMemberRoleResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.remove_member_role_with_options(workspace_id, member_id, role_name, headers, runtime)

    async def remove_member_role_async(
        self,
        workspace_id: str,
        member_id: str,
        role_name: str,
    ) -> aiwork_space_20210204_models.RemoveMemberRoleResponse:
        """
        @summary 删除成员角色
        
        @return: RemoveMemberRoleResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.remove_member_role_with_options_async(workspace_id, member_id, role_name, headers, runtime)

    def remove_workspace_quota_with_options(
        self,
        workspace_id: str,
        quota_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.RemoveWorkspaceQuotaResponse:
        """
        @summary 移除资源实例配额
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: RemoveWorkspaceQuotaResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='RemoveWorkspaceQuota',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.RemoveWorkspaceQuotaResponse(),
            self.call_api(params, req, runtime)
        )

    async def remove_workspace_quota_with_options_async(
        self,
        workspace_id: str,
        quota_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.RemoveWorkspaceQuotaResponse:
        """
        @summary 移除资源实例配额
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: RemoveWorkspaceQuotaResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='RemoveWorkspaceQuota',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.RemoveWorkspaceQuotaResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def remove_workspace_quota(
        self,
        workspace_id: str,
        quota_id: str,
    ) -> aiwork_space_20210204_models.RemoveWorkspaceQuotaResponse:
        """
        @summary 移除资源实例配额
        
        @return: RemoveWorkspaceQuotaResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.remove_workspace_quota_with_options(workspace_id, quota_id, headers, runtime)

    async def remove_workspace_quota_async(
        self,
        workspace_id: str,
        quota_id: str,
    ) -> aiwork_space_20210204_models.RemoveWorkspaceQuotaResponse:
        """
        @summary 移除资源实例配额
        
        @return: RemoveWorkspaceQuotaResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.remove_workspace_quota_with_options_async(workspace_id, quota_id, headers, runtime)

    def set_experiment_labels_with_options(
        self,
        experiment_id: str,
        request: aiwork_space_20210204_models.SetExperimentLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.SetExperimentLabelsResponse:
        """
        @summary 更新实验标签
        
        @param request: SetExperimentLabelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: SetExperimentLabelsResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='SetExperimentLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/experiments/{OpenApiUtilClient.get_encode_param(experiment_id)}/labels',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.SetExperimentLabelsResponse(),
            self.call_api(params, req, runtime)
        )

    async def set_experiment_labels_with_options_async(
        self,
        experiment_id: str,
        request: aiwork_space_20210204_models.SetExperimentLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.SetExperimentLabelsResponse:
        """
        @summary 更新实验标签
        
        @param request: SetExperimentLabelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: SetExperimentLabelsResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='SetExperimentLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/experiments/{OpenApiUtilClient.get_encode_param(experiment_id)}/labels',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.SetExperimentLabelsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def set_experiment_labels(
        self,
        experiment_id: str,
        request: aiwork_space_20210204_models.SetExperimentLabelsRequest,
    ) -> aiwork_space_20210204_models.SetExperimentLabelsResponse:
        """
        @summary 更新实验标签
        
        @param request: SetExperimentLabelsRequest
        @return: SetExperimentLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.set_experiment_labels_with_options(experiment_id, request, headers, runtime)

    async def set_experiment_labels_async(
        self,
        experiment_id: str,
        request: aiwork_space_20210204_models.SetExperimentLabelsRequest,
    ) -> aiwork_space_20210204_models.SetExperimentLabelsResponse:
        """
        @summary 更新实验标签
        
        @param request: SetExperimentLabelsRequest
        @return: SetExperimentLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.set_experiment_labels_with_options_async(experiment_id, request, headers, runtime)

    def set_trial_labels_with_options(
        self,
        trial_id: str,
        request: aiwork_space_20210204_models.SetTrialLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.SetTrialLabelsResponse:
        """
        @summary 更新Trial标签
        
        @param request: SetTrialLabelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: SetTrialLabelsResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='SetTrialLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/trials/{OpenApiUtilClient.get_encode_param(trial_id)}/Labels',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.SetTrialLabelsResponse(),
            self.call_api(params, req, runtime)
        )

    async def set_trial_labels_with_options_async(
        self,
        trial_id: str,
        request: aiwork_space_20210204_models.SetTrialLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.SetTrialLabelsResponse:
        """
        @summary 更新Trial标签
        
        @param request: SetTrialLabelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: SetTrialLabelsResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='SetTrialLabels',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/trials/{OpenApiUtilClient.get_encode_param(trial_id)}/Labels',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.SetTrialLabelsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def set_trial_labels(
        self,
        trial_id: str,
        request: aiwork_space_20210204_models.SetTrialLabelsRequest,
    ) -> aiwork_space_20210204_models.SetTrialLabelsResponse:
        """
        @summary 更新Trial标签
        
        @param request: SetTrialLabelsRequest
        @return: SetTrialLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.set_trial_labels_with_options(trial_id, request, headers, runtime)

    async def set_trial_labels_async(
        self,
        trial_id: str,
        request: aiwork_space_20210204_models.SetTrialLabelsRequest,
    ) -> aiwork_space_20210204_models.SetTrialLabelsResponse:
        """
        @summary 更新Trial标签
        
        @param request: SetTrialLabelsRequest
        @return: SetTrialLabelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.set_trial_labels_with_options_async(trial_id, request, headers, runtime)

    def set_user_configs_with_options(
        self,
        request: aiwork_space_20210204_models.SetUserConfigsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.SetUserConfigsResponse:
        """
        @summary 更新用户配置
        
        @param request: SetUserConfigsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: SetUserConfigsResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.configs):
            body['Configs'] = request.configs
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='SetUserConfigs',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/userconfigs',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.SetUserConfigsResponse(),
            self.call_api(params, req, runtime)
        )

    async def set_user_configs_with_options_async(
        self,
        request: aiwork_space_20210204_models.SetUserConfigsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.SetUserConfigsResponse:
        """
        @summary 更新用户配置
        
        @param request: SetUserConfigsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: SetUserConfigsResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.configs):
            body['Configs'] = request.configs
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='SetUserConfigs',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/userconfigs',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.SetUserConfigsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def set_user_configs(
        self,
        request: aiwork_space_20210204_models.SetUserConfigsRequest,
    ) -> aiwork_space_20210204_models.SetUserConfigsResponse:
        """
        @summary 更新用户配置
        
        @param request: SetUserConfigsRequest
        @return: SetUserConfigsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.set_user_configs_with_options(request, headers, runtime)

    async def set_user_configs_async(
        self,
        request: aiwork_space_20210204_models.SetUserConfigsRequest,
    ) -> aiwork_space_20210204_models.SetUserConfigsResponse:
        """
        @summary 更新用户配置
        
        @param request: SetUserConfigsRequest
        @return: SetUserConfigsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.set_user_configs_with_options_async(request, headers, runtime)

    def sync_users_with_options(
        self,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.SyncUsersResponse:
        """
        @summary 同步用户信息
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: SyncUsersResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='SyncUsers',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/users/action/sync',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.SyncUsersResponse(),
            self.call_api(params, req, runtime)
        )

    async def sync_users_with_options_async(
        self,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.SyncUsersResponse:
        """
        @summary 同步用户信息
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: SyncUsersResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='SyncUsers',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/users/action/sync',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.SyncUsersResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def sync_users(self) -> aiwork_space_20210204_models.SyncUsersResponse:
        """
        @summary 同步用户信息
        
        @return: SyncUsersResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.sync_users_with_options(headers, runtime)

    async def sync_users_async(self) -> aiwork_space_20210204_models.SyncUsersResponse:
        """
        @summary 同步用户信息
        
        @return: SyncUsersResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.sync_users_with_options_async(headers, runtime)

    def update_configs_with_options(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.UpdateConfigsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.UpdateConfigsResponse:
        """
        @summary 更新配置
        
        @param request: UpdateConfigsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateConfigsResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.configs):
            body['Configs'] = request.configs
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateConfigs',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/configs',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.UpdateConfigsResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_configs_with_options_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.UpdateConfigsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.UpdateConfigsResponse:
        """
        @summary 更新配置
        
        @param request: UpdateConfigsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateConfigsResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.configs):
            body['Configs'] = request.configs
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateConfigs',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/configs',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.UpdateConfigsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_configs(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.UpdateConfigsRequest,
    ) -> aiwork_space_20210204_models.UpdateConfigsResponse:
        """
        @summary 更新配置
        
        @param request: UpdateConfigsRequest
        @return: UpdateConfigsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_configs_with_options(workspace_id, request, headers, runtime)

    async def update_configs_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.UpdateConfigsRequest,
    ) -> aiwork_space_20210204_models.UpdateConfigsResponse:
        """
        @summary 更新配置
        
        @param request: UpdateConfigsRequest
        @return: UpdateConfigsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.update_configs_with_options_async(workspace_id, request, headers, runtime)

    def update_dataset_with_options(
        self,
        dataset_id: str,
        request: aiwork_space_20210204_models.UpdateDatasetRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.UpdateDatasetResponse:
        """
        @summary 更新数据集
        
        @param request: UpdateDatasetRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateDatasetResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.options):
            body['Options'] = request.options
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateDataset',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/datasets/{OpenApiUtilClient.get_encode_param(dataset_id)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.UpdateDatasetResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_dataset_with_options_async(
        self,
        dataset_id: str,
        request: aiwork_space_20210204_models.UpdateDatasetRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.UpdateDatasetResponse:
        """
        @summary 更新数据集
        
        @param request: UpdateDatasetRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateDatasetResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.options):
            body['Options'] = request.options
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateDataset',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/datasets/{OpenApiUtilClient.get_encode_param(dataset_id)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.UpdateDatasetResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_dataset(
        self,
        dataset_id: str,
        request: aiwork_space_20210204_models.UpdateDatasetRequest,
    ) -> aiwork_space_20210204_models.UpdateDatasetResponse:
        """
        @summary 更新数据集
        
        @param request: UpdateDatasetRequest
        @return: UpdateDatasetResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_dataset_with_options(dataset_id, request, headers, runtime)

    async def update_dataset_async(
        self,
        dataset_id: str,
        request: aiwork_space_20210204_models.UpdateDatasetRequest,
    ) -> aiwork_space_20210204_models.UpdateDatasetResponse:
        """
        @summary 更新数据集
        
        @param request: UpdateDatasetRequest
        @return: UpdateDatasetResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.update_dataset_with_options_async(dataset_id, request, headers, runtime)

    def update_default_workspace_with_options(
        self,
        request: aiwork_space_20210204_models.UpdateDefaultWorkspaceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.UpdateDefaultWorkspaceResponse:
        """
        @summary 更新默认工作空间
        
        @param request: UpdateDefaultWorkspaceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateDefaultWorkspaceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.workspace_id):
            body['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateDefaultWorkspace',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/defaultWorkspaces',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.UpdateDefaultWorkspaceResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_default_workspace_with_options_async(
        self,
        request: aiwork_space_20210204_models.UpdateDefaultWorkspaceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.UpdateDefaultWorkspaceResponse:
        """
        @summary 更新默认工作空间
        
        @param request: UpdateDefaultWorkspaceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateDefaultWorkspaceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.workspace_id):
            body['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateDefaultWorkspace',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/defaultWorkspaces',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.UpdateDefaultWorkspaceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_default_workspace(
        self,
        request: aiwork_space_20210204_models.UpdateDefaultWorkspaceRequest,
    ) -> aiwork_space_20210204_models.UpdateDefaultWorkspaceResponse:
        """
        @summary 更新默认工作空间
        
        @param request: UpdateDefaultWorkspaceRequest
        @return: UpdateDefaultWorkspaceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_default_workspace_with_options(request, headers, runtime)

    async def update_default_workspace_async(
        self,
        request: aiwork_space_20210204_models.UpdateDefaultWorkspaceRequest,
    ) -> aiwork_space_20210204_models.UpdateDefaultWorkspaceResponse:
        """
        @summary 更新默认工作空间
        
        @param request: UpdateDefaultWorkspaceRequest
        @return: UpdateDefaultWorkspaceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.update_default_workspace_with_options_async(request, headers, runtime)

    def update_experiment_with_options(
        self,
        experiment_id: str,
        request: aiwork_space_20210204_models.UpdateExperimentRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.UpdateExperimentResponse:
        """
        @summary 更新实验
        
        @param request: UpdateExperimentRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateExperimentResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.accessibility):
            body['Accessibility'] = request.accessibility
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateExperiment',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/experiments/{OpenApiUtilClient.get_encode_param(experiment_id)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.UpdateExperimentResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_experiment_with_options_async(
        self,
        experiment_id: str,
        request: aiwork_space_20210204_models.UpdateExperimentRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.UpdateExperimentResponse:
        """
        @summary 更新实验
        
        @param request: UpdateExperimentRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateExperimentResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.accessibility):
            body['Accessibility'] = request.accessibility
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateExperiment',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/experiments/{OpenApiUtilClient.get_encode_param(experiment_id)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.UpdateExperimentResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_experiment(
        self,
        experiment_id: str,
        request: aiwork_space_20210204_models.UpdateExperimentRequest,
    ) -> aiwork_space_20210204_models.UpdateExperimentResponse:
        """
        @summary 更新实验
        
        @param request: UpdateExperimentRequest
        @return: UpdateExperimentResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_experiment_with_options(experiment_id, request, headers, runtime)

    async def update_experiment_async(
        self,
        experiment_id: str,
        request: aiwork_space_20210204_models.UpdateExperimentRequest,
    ) -> aiwork_space_20210204_models.UpdateExperimentResponse:
        """
        @summary 更新实验
        
        @param request: UpdateExperimentRequest
        @return: UpdateExperimentResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.update_experiment_with_options_async(experiment_id, request, headers, runtime)

    def update_model_with_options(
        self,
        model_id: str,
        request: aiwork_space_20210204_models.UpdateModelRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.UpdateModelResponse:
        """
        @summary 更新模型
        
        @param request: UpdateModelRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateModelResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.accessibility):
            body['Accessibility'] = request.accessibility
        if not UtilClient.is_unset(request.domain):
            body['Domain'] = request.domain
        if not UtilClient.is_unset(request.extra_info):
            body['ExtraInfo'] = request.extra_info
        if not UtilClient.is_unset(request.model_description):
            body['ModelDescription'] = request.model_description
        if not UtilClient.is_unset(request.model_doc):
            body['ModelDoc'] = request.model_doc
        if not UtilClient.is_unset(request.model_name):
            body['ModelName'] = request.model_name
        if not UtilClient.is_unset(request.model_type):
            body['ModelType'] = request.model_type
        if not UtilClient.is_unset(request.order_number):
            body['OrderNumber'] = request.order_number
        if not UtilClient.is_unset(request.origin):
            body['Origin'] = request.origin
        if not UtilClient.is_unset(request.task):
            body['Task'] = request.task
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateModel',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.UpdateModelResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_model_with_options_async(
        self,
        model_id: str,
        request: aiwork_space_20210204_models.UpdateModelRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.UpdateModelResponse:
        """
        @summary 更新模型
        
        @param request: UpdateModelRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateModelResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.accessibility):
            body['Accessibility'] = request.accessibility
        if not UtilClient.is_unset(request.domain):
            body['Domain'] = request.domain
        if not UtilClient.is_unset(request.extra_info):
            body['ExtraInfo'] = request.extra_info
        if not UtilClient.is_unset(request.model_description):
            body['ModelDescription'] = request.model_description
        if not UtilClient.is_unset(request.model_doc):
            body['ModelDoc'] = request.model_doc
        if not UtilClient.is_unset(request.model_name):
            body['ModelName'] = request.model_name
        if not UtilClient.is_unset(request.model_type):
            body['ModelType'] = request.model_type
        if not UtilClient.is_unset(request.order_number):
            body['OrderNumber'] = request.order_number
        if not UtilClient.is_unset(request.origin):
            body['Origin'] = request.origin
        if not UtilClient.is_unset(request.task):
            body['Task'] = request.task
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateModel',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.UpdateModelResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_model(
        self,
        model_id: str,
        request: aiwork_space_20210204_models.UpdateModelRequest,
    ) -> aiwork_space_20210204_models.UpdateModelResponse:
        """
        @summary 更新模型
        
        @param request: UpdateModelRequest
        @return: UpdateModelResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_model_with_options(model_id, request, headers, runtime)

    async def update_model_async(
        self,
        model_id: str,
        request: aiwork_space_20210204_models.UpdateModelRequest,
    ) -> aiwork_space_20210204_models.UpdateModelResponse:
        """
        @summary 更新模型
        
        @param request: UpdateModelRequest
        @return: UpdateModelResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.update_model_with_options_async(model_id, request, headers, runtime)

    def update_model_domains_with_options(
        self,
        request: aiwork_space_20210204_models.UpdateModelDomainsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.UpdateModelDomainsResponse:
        """
        @summary 更新模型领域
        
        @param request: UpdateModelDomainsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateModelDomainsResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.model_domains):
            body['ModelDomains'] = request.model_domains
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateModelDomains',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/modeldomains',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.UpdateModelDomainsResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_model_domains_with_options_async(
        self,
        request: aiwork_space_20210204_models.UpdateModelDomainsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.UpdateModelDomainsResponse:
        """
        @summary 更新模型领域
        
        @param request: UpdateModelDomainsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateModelDomainsResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.model_domains):
            body['ModelDomains'] = request.model_domains
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateModelDomains',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/modeldomains',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.UpdateModelDomainsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_model_domains(
        self,
        request: aiwork_space_20210204_models.UpdateModelDomainsRequest,
    ) -> aiwork_space_20210204_models.UpdateModelDomainsResponse:
        """
        @summary 更新模型领域
        
        @param request: UpdateModelDomainsRequest
        @return: UpdateModelDomainsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_model_domains_with_options(request, headers, runtime)

    async def update_model_domains_async(
        self,
        request: aiwork_space_20210204_models.UpdateModelDomainsRequest,
    ) -> aiwork_space_20210204_models.UpdateModelDomainsResponse:
        """
        @summary 更新模型领域
        
        @param request: UpdateModelDomainsRequest
        @return: UpdateModelDomainsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.update_model_domains_with_options_async(request, headers, runtime)

    def update_model_version_with_options(
        self,
        model_id: str,
        version_name: str,
        request: aiwork_space_20210204_models.UpdateModelVersionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.UpdateModelVersionResponse:
        """
        @summary 更新模型版本
        
        @param request: UpdateModelVersionRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateModelVersionResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.approval_status):
            body['ApprovalStatus'] = request.approval_status
        if not UtilClient.is_unset(request.compression_spec):
            body['CompressionSpec'] = request.compression_spec
        if not UtilClient.is_unset(request.evaluation_spec):
            body['EvaluationSpec'] = request.evaluation_spec
        if not UtilClient.is_unset(request.extra_info):
            body['ExtraInfo'] = request.extra_info
        if not UtilClient.is_unset(request.inference_spec):
            body['InferenceSpec'] = request.inference_spec
        if not UtilClient.is_unset(request.metrics):
            body['Metrics'] = request.metrics
        if not UtilClient.is_unset(request.options):
            body['Options'] = request.options
        if not UtilClient.is_unset(request.source_id):
            body['SourceId'] = request.source_id
        if not UtilClient.is_unset(request.source_type):
            body['SourceType'] = request.source_type
        if not UtilClient.is_unset(request.training_spec):
            body['TrainingSpec'] = request.training_spec
        if not UtilClient.is_unset(request.version_description):
            body['VersionDescription'] = request.version_description
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateModelVersion',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}/versions/{OpenApiUtilClient.get_encode_param(version_name)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.UpdateModelVersionResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_model_version_with_options_async(
        self,
        model_id: str,
        version_name: str,
        request: aiwork_space_20210204_models.UpdateModelVersionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.UpdateModelVersionResponse:
        """
        @summary 更新模型版本
        
        @param request: UpdateModelVersionRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateModelVersionResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.approval_status):
            body['ApprovalStatus'] = request.approval_status
        if not UtilClient.is_unset(request.compression_spec):
            body['CompressionSpec'] = request.compression_spec
        if not UtilClient.is_unset(request.evaluation_spec):
            body['EvaluationSpec'] = request.evaluation_spec
        if not UtilClient.is_unset(request.extra_info):
            body['ExtraInfo'] = request.extra_info
        if not UtilClient.is_unset(request.inference_spec):
            body['InferenceSpec'] = request.inference_spec
        if not UtilClient.is_unset(request.metrics):
            body['Metrics'] = request.metrics
        if not UtilClient.is_unset(request.options):
            body['Options'] = request.options
        if not UtilClient.is_unset(request.source_id):
            body['SourceId'] = request.source_id
        if not UtilClient.is_unset(request.source_type):
            body['SourceType'] = request.source_type
        if not UtilClient.is_unset(request.training_spec):
            body['TrainingSpec'] = request.training_spec
        if not UtilClient.is_unset(request.version_description):
            body['VersionDescription'] = request.version_description
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateModelVersion',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/models/{OpenApiUtilClient.get_encode_param(model_id)}/versions/{OpenApiUtilClient.get_encode_param(version_name)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.UpdateModelVersionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_model_version(
        self,
        model_id: str,
        version_name: str,
        request: aiwork_space_20210204_models.UpdateModelVersionRequest,
    ) -> aiwork_space_20210204_models.UpdateModelVersionResponse:
        """
        @summary 更新模型版本
        
        @param request: UpdateModelVersionRequest
        @return: UpdateModelVersionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_model_version_with_options(model_id, version_name, request, headers, runtime)

    async def update_model_version_async(
        self,
        model_id: str,
        version_name: str,
        request: aiwork_space_20210204_models.UpdateModelVersionRequest,
    ) -> aiwork_space_20210204_models.UpdateModelVersionResponse:
        """
        @summary 更新模型版本
        
        @param request: UpdateModelVersionRequest
        @return: UpdateModelVersionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.update_model_version_with_options_async(model_id, version_name, request, headers, runtime)

    def update_service_template_with_options(
        self,
        service_template_id: str,
        request: aiwork_space_20210204_models.UpdateServiceTemplateRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.UpdateServiceTemplateResponse:
        """
        @summary 更新服务模版
        
        @param request: UpdateServiceTemplateRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateServiceTemplateResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.inference_spec):
            body['InferenceSpec'] = request.inference_spec
        if not UtilClient.is_unset(request.order_number):
            body['OrderNumber'] = request.order_number
        if not UtilClient.is_unset(request.service_template_description):
            body['ServiceTemplateDescription'] = request.service_template_description
        if not UtilClient.is_unset(request.service_template_doc):
            body['ServiceTemplateDoc'] = request.service_template_doc
        if not UtilClient.is_unset(request.service_template_name):
            body['ServiceTemplateName'] = request.service_template_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateServiceTemplate',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/servicetemplates/{OpenApiUtilClient.get_encode_param(service_template_id)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.UpdateServiceTemplateResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_service_template_with_options_async(
        self,
        service_template_id: str,
        request: aiwork_space_20210204_models.UpdateServiceTemplateRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.UpdateServiceTemplateResponse:
        """
        @summary 更新服务模版
        
        @param request: UpdateServiceTemplateRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateServiceTemplateResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.inference_spec):
            body['InferenceSpec'] = request.inference_spec
        if not UtilClient.is_unset(request.order_number):
            body['OrderNumber'] = request.order_number
        if not UtilClient.is_unset(request.service_template_description):
            body['ServiceTemplateDescription'] = request.service_template_description
        if not UtilClient.is_unset(request.service_template_doc):
            body['ServiceTemplateDoc'] = request.service_template_doc
        if not UtilClient.is_unset(request.service_template_name):
            body['ServiceTemplateName'] = request.service_template_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateServiceTemplate',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/servicetemplates/{OpenApiUtilClient.get_encode_param(service_template_id)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.UpdateServiceTemplateResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_service_template(
        self,
        service_template_id: str,
        request: aiwork_space_20210204_models.UpdateServiceTemplateRequest,
    ) -> aiwork_space_20210204_models.UpdateServiceTemplateResponse:
        """
        @summary 更新服务模版
        
        @param request: UpdateServiceTemplateRequest
        @return: UpdateServiceTemplateResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_service_template_with_options(service_template_id, request, headers, runtime)

    async def update_service_template_async(
        self,
        service_template_id: str,
        request: aiwork_space_20210204_models.UpdateServiceTemplateRequest,
    ) -> aiwork_space_20210204_models.UpdateServiceTemplateResponse:
        """
        @summary 更新服务模版
        
        @param request: UpdateServiceTemplateRequest
        @return: UpdateServiceTemplateResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.update_service_template_with_options_async(service_template_id, request, headers, runtime)

    def update_workspace_with_options(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.UpdateWorkspaceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.UpdateWorkspaceResponse:
        """
        @summary 更新工作空间
        
        @param request: UpdateWorkspaceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateWorkspaceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
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
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.UpdateWorkspaceResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_workspace_with_options_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.UpdateWorkspaceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.UpdateWorkspaceResponse:
        """
        @summary 更新工作空间
        
        @param request: UpdateWorkspaceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateWorkspaceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
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
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.UpdateWorkspaceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_workspace(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.UpdateWorkspaceRequest,
    ) -> aiwork_space_20210204_models.UpdateWorkspaceResponse:
        """
        @summary 更新工作空间
        
        @param request: UpdateWorkspaceRequest
        @return: UpdateWorkspaceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_workspace_with_options(workspace_id, request, headers, runtime)

    async def update_workspace_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.UpdateWorkspaceRequest,
    ) -> aiwork_space_20210204_models.UpdateWorkspaceResponse:
        """
        @summary 更新工作空间
        
        @param request: UpdateWorkspaceRequest
        @return: UpdateWorkspaceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.update_workspace_with_options_async(workspace_id, request, headers, runtime)

    def update_workspace_resource_with_options(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.UpdateWorkspaceResourceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.UpdateWorkspaceResourceResponse:
        """
        @summary 更新工作空间资源
        
        @param request: UpdateWorkspaceResourceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateWorkspaceResourceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.group_name):
            body['GroupName'] = request.group_name
        if not UtilClient.is_unset(request.is_default):
            body['IsDefault'] = request.is_default
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        if not UtilClient.is_unset(request.product_type):
            body['ProductType'] = request.product_type
        if not UtilClient.is_unset(request.resource_ids):
            body['ResourceIds'] = request.resource_ids
        if not UtilClient.is_unset(request.resource_type):
            body['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.spec):
            body['Spec'] = request.spec
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateWorkspaceResource',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/resources',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.UpdateWorkspaceResourceResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_workspace_resource_with_options_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.UpdateWorkspaceResourceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.UpdateWorkspaceResourceResponse:
        """
        @summary 更新工作空间资源
        
        @param request: UpdateWorkspaceResourceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateWorkspaceResourceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.group_name):
            body['GroupName'] = request.group_name
        if not UtilClient.is_unset(request.is_default):
            body['IsDefault'] = request.is_default
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        if not UtilClient.is_unset(request.product_type):
            body['ProductType'] = request.product_type
        if not UtilClient.is_unset(request.resource_ids):
            body['ResourceIds'] = request.resource_ids
        if not UtilClient.is_unset(request.resource_type):
            body['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.spec):
            body['Spec'] = request.spec
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateWorkspaceResource',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/resources',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.UpdateWorkspaceResourceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_workspace_resource(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.UpdateWorkspaceResourceRequest,
    ) -> aiwork_space_20210204_models.UpdateWorkspaceResourceResponse:
        """
        @summary 更新工作空间资源
        
        @param request: UpdateWorkspaceResourceRequest
        @return: UpdateWorkspaceResourceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_workspace_resource_with_options(workspace_id, request, headers, runtime)

    async def update_workspace_resource_async(
        self,
        workspace_id: str,
        request: aiwork_space_20210204_models.UpdateWorkspaceResourceRequest,
    ) -> aiwork_space_20210204_models.UpdateWorkspaceResourceResponse:
        """
        @summary 更新工作空间资源
        
        @param request: UpdateWorkspaceResourceRequest
        @return: UpdateWorkspaceResourceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.update_workspace_resource_with_options_async(workspace_id, request, headers, runtime)

    def update_workspace_role_with_options(
        self,
        workspace_id: str,
        role_id: str,
        request: aiwork_space_20210204_models.UpdateWorkspaceRoleRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.UpdateWorkspaceRoleResponse:
        """
        @summary 更新工作空间角色
        
        @param request: UpdateWorkspaceRoleRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateWorkspaceRoleResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.module_permissions):
            body['ModulePermissions'] = request.module_permissions
        if not UtilClient.is_unset(request.role_name):
            body['RoleName'] = request.role_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateWorkspaceRole',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/roles/{OpenApiUtilClient.get_encode_param(role_id)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.UpdateWorkspaceRoleResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_workspace_role_with_options_async(
        self,
        workspace_id: str,
        role_id: str,
        request: aiwork_space_20210204_models.UpdateWorkspaceRoleRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> aiwork_space_20210204_models.UpdateWorkspaceRoleResponse:
        """
        @summary 更新工作空间角色
        
        @param request: UpdateWorkspaceRoleRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateWorkspaceRoleResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.module_permissions):
            body['ModulePermissions'] = request.module_permissions
        if not UtilClient.is_unset(request.role_name):
            body['RoleName'] = request.role_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateWorkspaceRole',
            version='2021-02-04',
            protocol='HTTPS',
            pathname=f'/api/v1/workspaces/{OpenApiUtilClient.get_encode_param(workspace_id)}/roles/{OpenApiUtilClient.get_encode_param(role_id)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            aiwork_space_20210204_models.UpdateWorkspaceRoleResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_workspace_role(
        self,
        workspace_id: str,
        role_id: str,
        request: aiwork_space_20210204_models.UpdateWorkspaceRoleRequest,
    ) -> aiwork_space_20210204_models.UpdateWorkspaceRoleResponse:
        """
        @summary 更新工作空间角色
        
        @param request: UpdateWorkspaceRoleRequest
        @return: UpdateWorkspaceRoleResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_workspace_role_with_options(workspace_id, role_id, request, headers, runtime)

    async def update_workspace_role_async(
        self,
        workspace_id: str,
        role_id: str,
        request: aiwork_space_20210204_models.UpdateWorkspaceRoleRequest,
    ) -> aiwork_space_20210204_models.UpdateWorkspaceRoleResponse:
        """
        @summary 更新工作空间角色
        
        @param request: UpdateWorkspaceRoleRequest
        @return: UpdateWorkspaceRoleResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.update_workspace_role_with_options_async(workspace_id, role_id, request, headers, runtime)
