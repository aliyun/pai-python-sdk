# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from typing import Dict
from Tea.core import TeaCore

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient
# from alibabacloud_paistudio20220112 import models as pai_studio_20220112_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient

from pai.libs.alibabacloud_paistudio20220112 import models as pai_studio_20220112_models


class Client(OpenApiClient):
    """
    *\
    """
    def __init__(
        self, 
        config: open_api_models.Config,
    ):
        super().__init__(config)
        self._endpoint_rule = 'regional'
        self._endpoint_map = {
            'cn-beijing': 'pai.cn-beijing.aliyuncs.com',
            'cn-hangzhou': 'pai.cn-hangzhou.aliyuncs.com',
            'cn-shanghai': 'pai.cn-shanghai.aliyuncs.com',
            'cn-shenzhen': 'pai.cn-shenzhen.aliyuncs.com',
            'cn-hongkong': 'pai.cn-hongkong.aliyuncs.com',
            'ap-southeast-1': 'pai.ap-southeast-1.aliyuncs.com',
            'ap-southeast-2': 'pai.ap-southeast-2.aliyuncs.com',
            'ap-southeast-3': 'pai.ap-southeast-3.aliyuncs.com',
            'ap-southeast-5': 'pai.ap-southeast-5.aliyuncs.com',
            'us-west-1': 'pai.us-west-1.aliyuncs.com',
            'us-east-1': 'pai.us-east-1.aliyuncs.com',
            'eu-central-1': 'pai.eu-central-1.aliyuncs.com',
            'me-east-1': 'pai.me-east-1.aliyuncs.com',
            'ap-south-1': 'pai.ap-south-1.aliyuncs.com',
            'cn-qingdao': 'pai.cn-qingdao.aliyuncs.com',
            'cn-zhangjiakou': 'pai.cn-zhangjiakou.aliyuncs.com'
        }
        self.check_config(config)
        self._endpoint = self.get_endpoint('paistudio', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

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

    def create_ai4ddefault_bucket_with_options(
        self,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.CreateAI4DDefaultBucketResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='CreateAI4DDefaultBucket',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/ai4d/defaultbucket',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.CreateAI4DDefaultBucketResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_ai4ddefault_bucket_with_options_async(
        self,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.CreateAI4DDefaultBucketResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='CreateAI4DDefaultBucket',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/ai4d/defaultbucket',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.CreateAI4DDefaultBucketResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_ai4ddefault_bucket(self) -> pai_studio_20220112_models.CreateAI4DDefaultBucketResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_ai4ddefault_bucket_with_options(headers, runtime)

    async def create_ai4ddefault_bucket_async(self) -> pai_studio_20220112_models.CreateAI4DDefaultBucketResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_ai4ddefault_bucket_with_options_async(headers, runtime)

    def create_ai4dserivce_with_options(
        self,
        request: pai_studio_20220112_models.CreateAI4DSerivceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.CreateAI4DSerivceResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.inference_spec):
            body['InferenceSpec'] = request.inference_spec
        if not UtilClient.is_unset(request.service_type):
            body['ServiceType'] = request.service_type
        if not UtilClient.is_unset(request.workspace_id):
            body['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateAI4DSerivce',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/ai4d/services',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.CreateAI4DSerivceResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_ai4dserivce_with_options_async(
        self,
        request: pai_studio_20220112_models.CreateAI4DSerivceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.CreateAI4DSerivceResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.inference_spec):
            body['InferenceSpec'] = request.inference_spec
        if not UtilClient.is_unset(request.service_type):
            body['ServiceType'] = request.service_type
        if not UtilClient.is_unset(request.workspace_id):
            body['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateAI4DSerivce',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/ai4d/services',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.CreateAI4DSerivceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_ai4dserivce(
        self,
        request: pai_studio_20220112_models.CreateAI4DSerivceRequest,
    ) -> pai_studio_20220112_models.CreateAI4DSerivceResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_ai4dserivce_with_options(request, headers, runtime)

    async def create_ai4dserivce_async(
        self,
        request: pai_studio_20220112_models.CreateAI4DSerivceRequest,
    ) -> pai_studio_20220112_models.CreateAI4DSerivceResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_ai4dserivce_with_options_async(request, headers, runtime)

    def create_algorithm_with_options(
        self,
        request: pai_studio_20220112_models.CreateAlgorithmRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.CreateAlgorithmResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.algorithm_description):
            body['AlgorithmDescription'] = request.algorithm_description
        if not UtilClient.is_unset(request.algorithm_name):
            body['AlgorithmName'] = request.algorithm_name
        if not UtilClient.is_unset(request.display_name):
            body['DisplayName'] = request.display_name
        if not UtilClient.is_unset(request.workspace_id):
            body['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateAlgorithm',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/algorithms',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.CreateAlgorithmResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_algorithm_with_options_async(
        self,
        request: pai_studio_20220112_models.CreateAlgorithmRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.CreateAlgorithmResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.algorithm_description):
            body['AlgorithmDescription'] = request.algorithm_description
        if not UtilClient.is_unset(request.algorithm_name):
            body['AlgorithmName'] = request.algorithm_name
        if not UtilClient.is_unset(request.display_name):
            body['DisplayName'] = request.display_name
        if not UtilClient.is_unset(request.workspace_id):
            body['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateAlgorithm',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/algorithms',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.CreateAlgorithmResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_algorithm(
        self,
        request: pai_studio_20220112_models.CreateAlgorithmRequest,
    ) -> pai_studio_20220112_models.CreateAlgorithmResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_algorithm_with_options(request, headers, runtime)

    async def create_algorithm_async(
        self,
        request: pai_studio_20220112_models.CreateAlgorithmRequest,
    ) -> pai_studio_20220112_models.CreateAlgorithmResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_algorithm_with_options_async(request, headers, runtime)

    def create_algorithm_version_with_options(
        self,
        algorithm_id: str,
        algorithm_version: str,
        tmp_req: pai_studio_20220112_models.CreateAlgorithmVersionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.CreateAlgorithmVersionResponse:
        UtilClient.validate_model(tmp_req)
        request = pai_studio_20220112_models.CreateAlgorithmVersionShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.algorithm_spec):
            request.algorithm_spec_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.algorithm_spec, 'AlgorithmSpec', 'json')
        body = {}
        if not UtilClient.is_unset(request.algorithm_spec_shrink):
            body['AlgorithmSpec'] = request.algorithm_spec_shrink
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateAlgorithmVersion',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/algorithms/{OpenApiUtilClient.get_encode_param(algorithm_id)}/versions/{OpenApiUtilClient.get_encode_param(algorithm_version)}',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.CreateAlgorithmVersionResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_algorithm_version_with_options_async(
        self,
        algorithm_id: str,
        algorithm_version: str,
        tmp_req: pai_studio_20220112_models.CreateAlgorithmVersionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.CreateAlgorithmVersionResponse:
        UtilClient.validate_model(tmp_req)
        request = pai_studio_20220112_models.CreateAlgorithmVersionShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.algorithm_spec):
            request.algorithm_spec_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.algorithm_spec, 'AlgorithmSpec', 'json')
        body = {}
        if not UtilClient.is_unset(request.algorithm_spec_shrink):
            body['AlgorithmSpec'] = request.algorithm_spec_shrink
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateAlgorithmVersion',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/algorithms/{OpenApiUtilClient.get_encode_param(algorithm_id)}/versions/{OpenApiUtilClient.get_encode_param(algorithm_version)}',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.CreateAlgorithmVersionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_algorithm_version(
        self,
        algorithm_id: str,
        algorithm_version: str,
        request: pai_studio_20220112_models.CreateAlgorithmVersionRequest,
    ) -> pai_studio_20220112_models.CreateAlgorithmVersionResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_algorithm_version_with_options(algorithm_id, algorithm_version, request, headers, runtime)

    async def create_algorithm_version_async(
        self,
        algorithm_id: str,
        algorithm_version: str,
        request: pai_studio_20220112_models.CreateAlgorithmVersionRequest,
    ) -> pai_studio_20220112_models.CreateAlgorithmVersionResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_algorithm_version_with_options_async(algorithm_id, algorithm_version, request, headers, runtime)

    def create_component_with_options(
        self,
        request: pai_studio_20220112_models.CreateComponentRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.CreateComponentResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.display_name):
            body['DisplayName'] = request.display_name
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
            action='CreateComponent',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/components',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.CreateComponentResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_component_with_options_async(
        self,
        request: pai_studio_20220112_models.CreateComponentRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.CreateComponentResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.display_name):
            body['DisplayName'] = request.display_name
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
            action='CreateComponent',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/components',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.CreateComponentResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_component(
        self,
        request: pai_studio_20220112_models.CreateComponentRequest,
    ) -> pai_studio_20220112_models.CreateComponentResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_component_with_options(request, headers, runtime)

    async def create_component_async(
        self,
        request: pai_studio_20220112_models.CreateComponentRequest,
    ) -> pai_studio_20220112_models.CreateComponentResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_component_with_options_async(request, headers, runtime)

    def create_component_version_with_options(
        self,
        component_id: str,
        request: pai_studio_20220112_models.CreateComponentVersionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.CreateComponentVersionResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.config_dir):
            body['ConfigDir'] = request.config_dir
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        if not UtilClient.is_unset(request.spec):
            body['Spec'] = request.spec
        if not UtilClient.is_unset(request.version):
            body['Version'] = request.version
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateComponentVersion',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/components/{OpenApiUtilClient.get_encode_param(component_id)}/versions',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.CreateComponentVersionResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_component_version_with_options_async(
        self,
        component_id: str,
        request: pai_studio_20220112_models.CreateComponentVersionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.CreateComponentVersionResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.config_dir):
            body['ConfigDir'] = request.config_dir
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        if not UtilClient.is_unset(request.spec):
            body['Spec'] = request.spec
        if not UtilClient.is_unset(request.version):
            body['Version'] = request.version
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateComponentVersion',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/components/{OpenApiUtilClient.get_encode_param(component_id)}/versions',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.CreateComponentVersionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_component_version(
        self,
        component_id: str,
        request: pai_studio_20220112_models.CreateComponentVersionRequest,
    ) -> pai_studio_20220112_models.CreateComponentVersionResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_component_version_with_options(component_id, request, headers, runtime)

    async def create_component_version_async(
        self,
        component_id: str,
        request: pai_studio_20220112_models.CreateComponentVersionRequest,
    ) -> pai_studio_20220112_models.CreateComponentVersionResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_component_version_with_options_async(component_id, request, headers, runtime)

    def create_quota_with_options(
        self,
        request: pai_studio_20220112_models.CreateQuotaRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.CreateQuotaResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.allocate_strategy):
            body['AllocateStrategy'] = request.allocate_strategy
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        if not UtilClient.is_unset(request.min):
            body['Min'] = request.min
        if not UtilClient.is_unset(request.parent_quota_id):
            body['ParentQuotaId'] = request.parent_quota_id
        if not UtilClient.is_unset(request.quota_name):
            body['QuotaName'] = request.quota_name
        if not UtilClient.is_unset(request.resource_group_ids):
            body['ResourceGroupIds'] = request.resource_group_ids
        if not UtilClient.is_unset(request.resource_type):
            body['ResourceType'] = request.resource_type
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateQuota',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.CreateQuotaResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_quota_with_options_async(
        self,
        request: pai_studio_20220112_models.CreateQuotaRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.CreateQuotaResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.allocate_strategy):
            body['AllocateStrategy'] = request.allocate_strategy
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        if not UtilClient.is_unset(request.min):
            body['Min'] = request.min
        if not UtilClient.is_unset(request.parent_quota_id):
            body['ParentQuotaId'] = request.parent_quota_id
        if not UtilClient.is_unset(request.quota_name):
            body['QuotaName'] = request.quota_name
        if not UtilClient.is_unset(request.resource_group_ids):
            body['ResourceGroupIds'] = request.resource_group_ids
        if not UtilClient.is_unset(request.resource_type):
            body['ResourceType'] = request.resource_type
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateQuota',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.CreateQuotaResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_quota(
        self,
        request: pai_studio_20220112_models.CreateQuotaRequest,
    ) -> pai_studio_20220112_models.CreateQuotaResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_quota_with_options(request, headers, runtime)

    async def create_quota_async(
        self,
        request: pai_studio_20220112_models.CreateQuotaRequest,
    ) -> pai_studio_20220112_models.CreateQuotaResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_quota_with_options_async(request, headers, runtime)

    def create_resource_group_with_options(
        self,
        request: pai_studio_20220112_models.CreateResourceGroupRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.CreateResourceGroupResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.computing_resource_provider):
            body['ComputingResourceProvider'] = request.computing_resource_provider
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.resource_type):
            body['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.user_vpc):
            body['UserVpc'] = request.user_vpc
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateResourceGroup',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.CreateResourceGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_resource_group_with_options_async(
        self,
        request: pai_studio_20220112_models.CreateResourceGroupRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.CreateResourceGroupResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.computing_resource_provider):
            body['ComputingResourceProvider'] = request.computing_resource_provider
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.resource_type):
            body['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.user_vpc):
            body['UserVpc'] = request.user_vpc
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateResourceGroup',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.CreateResourceGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_resource_group(
        self,
        request: pai_studio_20220112_models.CreateResourceGroupRequest,
    ) -> pai_studio_20220112_models.CreateResourceGroupResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_resource_group_with_options(request, headers, runtime)

    async def create_resource_group_async(
        self,
        request: pai_studio_20220112_models.CreateResourceGroupRequest,
    ) -> pai_studio_20220112_models.CreateResourceGroupResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_resource_group_with_options_async(request, headers, runtime)

    def create_service_identity_role_with_options(
        self,
        request: pai_studio_20220112_models.CreateServiceIdentityRoleRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.CreateServiceIdentityRoleResponse:
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
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/ai4d/serviceidentityroles',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.CreateServiceIdentityRoleResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_service_identity_role_with_options_async(
        self,
        request: pai_studio_20220112_models.CreateServiceIdentityRoleRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.CreateServiceIdentityRoleResponse:
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
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/ai4d/serviceidentityroles',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.CreateServiceIdentityRoleResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_service_identity_role(
        self,
        request: pai_studio_20220112_models.CreateServiceIdentityRoleRequest,
    ) -> pai_studio_20220112_models.CreateServiceIdentityRoleResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_service_identity_role_with_options(request, headers, runtime)

    async def create_service_identity_role_async(
        self,
        request: pai_studio_20220112_models.CreateServiceIdentityRoleRequest,
    ) -> pai_studio_20220112_models.CreateServiceIdentityRoleResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_service_identity_role_with_options_async(request, headers, runtime)

    def create_training_job_with_options(
        self,
        request: pai_studio_20220112_models.CreateTrainingJobRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.CreateTrainingJobResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.algorithm_name):
            body['AlgorithmName'] = request.algorithm_name
        if not UtilClient.is_unset(request.algorithm_provider):
            body['AlgorithmProvider'] = request.algorithm_provider
        if not UtilClient.is_unset(request.algorithm_spec):
            body['AlgorithmSpec'] = request.algorithm_spec
        if not UtilClient.is_unset(request.algorithm_version):
            body['AlgorithmVersion'] = request.algorithm_version
        if not UtilClient.is_unset(request.code_dir):
            body['CodeDir'] = request.code_dir
        if not UtilClient.is_unset(request.compute_resource):
            body['ComputeResource'] = request.compute_resource
        if not UtilClient.is_unset(request.hyper_parameters):
            body['HyperParameters'] = request.hyper_parameters
        if not UtilClient.is_unset(request.input_channels):
            body['InputChannels'] = request.input_channels
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        if not UtilClient.is_unset(request.output_channels):
            body['OutputChannels'] = request.output_channels
        if not UtilClient.is_unset(request.role_arn):
            body['RoleArn'] = request.role_arn
        if not UtilClient.is_unset(request.scheduler):
            body['Scheduler'] = request.scheduler
        if not UtilClient.is_unset(request.training_job_description):
            body['TrainingJobDescription'] = request.training_job_description
        if not UtilClient.is_unset(request.training_job_name):
            body['TrainingJobName'] = request.training_job_name
        if not UtilClient.is_unset(request.user_vpc):
            body['UserVpc'] = request.user_vpc
        if not UtilClient.is_unset(request.workspace_id):
            body['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateTrainingJob',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.CreateTrainingJobResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_training_job_with_options_async(
        self,
        request: pai_studio_20220112_models.CreateTrainingJobRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.CreateTrainingJobResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.algorithm_name):
            body['AlgorithmName'] = request.algorithm_name
        if not UtilClient.is_unset(request.algorithm_provider):
            body['AlgorithmProvider'] = request.algorithm_provider
        if not UtilClient.is_unset(request.algorithm_spec):
            body['AlgorithmSpec'] = request.algorithm_spec
        if not UtilClient.is_unset(request.algorithm_version):
            body['AlgorithmVersion'] = request.algorithm_version
        if not UtilClient.is_unset(request.code_dir):
            body['CodeDir'] = request.code_dir
        if not UtilClient.is_unset(request.compute_resource):
            body['ComputeResource'] = request.compute_resource
        if not UtilClient.is_unset(request.hyper_parameters):
            body['HyperParameters'] = request.hyper_parameters
        if not UtilClient.is_unset(request.input_channels):
            body['InputChannels'] = request.input_channels
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        if not UtilClient.is_unset(request.output_channels):
            body['OutputChannels'] = request.output_channels
        if not UtilClient.is_unset(request.role_arn):
            body['RoleArn'] = request.role_arn
        if not UtilClient.is_unset(request.scheduler):
            body['Scheduler'] = request.scheduler
        if not UtilClient.is_unset(request.training_job_description):
            body['TrainingJobDescription'] = request.training_job_description
        if not UtilClient.is_unset(request.training_job_name):
            body['TrainingJobName'] = request.training_job_name
        if not UtilClient.is_unset(request.user_vpc):
            body['UserVpc'] = request.user_vpc
        if not UtilClient.is_unset(request.workspace_id):
            body['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateTrainingJob',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.CreateTrainingJobResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_training_job(
        self,
        request: pai_studio_20220112_models.CreateTrainingJobRequest,
    ) -> pai_studio_20220112_models.CreateTrainingJobResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_training_job_with_options(request, headers, runtime)

    async def create_training_job_async(
        self,
        request: pai_studio_20220112_models.CreateTrainingJobRequest,
    ) -> pai_studio_20220112_models.CreateTrainingJobResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_training_job_with_options_async(request, headers, runtime)

    def delete_algorithm_with_options(
        self,
        algorithm_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.DeleteAlgorithmResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteAlgorithm',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/algorithms/{OpenApiUtilClient.get_encode_param(algorithm_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.DeleteAlgorithmResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_algorithm_with_options_async(
        self,
        algorithm_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.DeleteAlgorithmResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteAlgorithm',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/algorithms/{OpenApiUtilClient.get_encode_param(algorithm_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.DeleteAlgorithmResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_algorithm(
        self,
        algorithm_id: str,
    ) -> pai_studio_20220112_models.DeleteAlgorithmResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_algorithm_with_options(algorithm_id, headers, runtime)

    async def delete_algorithm_async(
        self,
        algorithm_id: str,
    ) -> pai_studio_20220112_models.DeleteAlgorithmResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_algorithm_with_options_async(algorithm_id, headers, runtime)

    def delete_algorithm_version_with_options(
        self,
        algorithm_id: str,
        algorithm_version: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.DeleteAlgorithmVersionResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteAlgorithmVersion',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/algorithms/{OpenApiUtilClient.get_encode_param(algorithm_id)}/versions/{OpenApiUtilClient.get_encode_param(algorithm_version)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.DeleteAlgorithmVersionResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_algorithm_version_with_options_async(
        self,
        algorithm_id: str,
        algorithm_version: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.DeleteAlgorithmVersionResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteAlgorithmVersion',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/algorithms/{OpenApiUtilClient.get_encode_param(algorithm_id)}/versions/{OpenApiUtilClient.get_encode_param(algorithm_version)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.DeleteAlgorithmVersionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_algorithm_version(
        self,
        algorithm_id: str,
        algorithm_version: str,
    ) -> pai_studio_20220112_models.DeleteAlgorithmVersionResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_algorithm_version_with_options(algorithm_id, algorithm_version, headers, runtime)

    async def delete_algorithm_version_async(
        self,
        algorithm_id: str,
        algorithm_version: str,
    ) -> pai_studio_20220112_models.DeleteAlgorithmVersionResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_algorithm_version_with_options_async(algorithm_id, algorithm_version, headers, runtime)

    def delete_component_with_options(
        self,
        component_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.DeleteComponentResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteComponent',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/components/{OpenApiUtilClient.get_encode_param(component_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.DeleteComponentResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_component_with_options_async(
        self,
        component_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.DeleteComponentResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteComponent',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/components/{OpenApiUtilClient.get_encode_param(component_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.DeleteComponentResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_component(
        self,
        component_id: str,
    ) -> pai_studio_20220112_models.DeleteComponentResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_component_with_options(component_id, headers, runtime)

    async def delete_component_async(
        self,
        component_id: str,
    ) -> pai_studio_20220112_models.DeleteComponentResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_component_with_options_async(component_id, headers, runtime)

    def delete_component_version_with_options(
        self,
        component_id: str,
        version: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.DeleteComponentVersionResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteComponentVersion',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/components/{OpenApiUtilClient.get_encode_param(component_id)}/versions/{OpenApiUtilClient.get_encode_param(version)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.DeleteComponentVersionResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_component_version_with_options_async(
        self,
        component_id: str,
        version: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.DeleteComponentVersionResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteComponentVersion',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/components/{OpenApiUtilClient.get_encode_param(component_id)}/versions/{OpenApiUtilClient.get_encode_param(version)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.DeleteComponentVersionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_component_version(
        self,
        component_id: str,
        version: str,
    ) -> pai_studio_20220112_models.DeleteComponentVersionResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_component_version_with_options(component_id, version, headers, runtime)

    async def delete_component_version_async(
        self,
        component_id: str,
        version: str,
    ) -> pai_studio_20220112_models.DeleteComponentVersionResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_component_version_with_options_async(component_id, version, headers, runtime)

    def delete_component_version_snapshot_with_options(
        self,
        snapshot_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.DeleteComponentVersionSnapshotResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteComponentVersionSnapshot',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/componentversionsnapshots/{OpenApiUtilClient.get_encode_param(snapshot_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.DeleteComponentVersionSnapshotResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_component_version_snapshot_with_options_async(
        self,
        snapshot_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.DeleteComponentVersionSnapshotResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteComponentVersionSnapshot',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/componentversionsnapshots/{OpenApiUtilClient.get_encode_param(snapshot_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.DeleteComponentVersionSnapshotResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_component_version_snapshot(
        self,
        snapshot_id: str,
    ) -> pai_studio_20220112_models.DeleteComponentVersionSnapshotResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_component_version_snapshot_with_options(snapshot_id, headers, runtime)

    async def delete_component_version_snapshot_async(
        self,
        snapshot_id: str,
    ) -> pai_studio_20220112_models.DeleteComponentVersionSnapshotResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_component_version_snapshot_with_options_async(snapshot_id, headers, runtime)

    def delete_machine_group_with_options(
        self,
        machine_group_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.DeleteMachineGroupResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteMachineGroup',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/machinegroups/{OpenApiUtilClient.get_encode_param(machine_group_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.DeleteMachineGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_machine_group_with_options_async(
        self,
        machine_group_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.DeleteMachineGroupResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteMachineGroup',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/machinegroups/{OpenApiUtilClient.get_encode_param(machine_group_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.DeleteMachineGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_machine_group(
        self,
        machine_group_id: str,
    ) -> pai_studio_20220112_models.DeleteMachineGroupResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_machine_group_with_options(machine_group_id, headers, runtime)

    async def delete_machine_group_async(
        self,
        machine_group_id: str,
    ) -> pai_studio_20220112_models.DeleteMachineGroupResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_machine_group_with_options_async(machine_group_id, headers, runtime)

    def delete_quota_with_options(
        self,
        quota_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.DeleteQuotaResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteQuota',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.DeleteQuotaResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_quota_with_options_async(
        self,
        quota_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.DeleteQuotaResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteQuota',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.DeleteQuotaResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_quota(
        self,
        quota_id: str,
    ) -> pai_studio_20220112_models.DeleteQuotaResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_quota_with_options(quota_id, headers, runtime)

    async def delete_quota_async(
        self,
        quota_id: str,
    ) -> pai_studio_20220112_models.DeleteQuotaResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_quota_with_options_async(quota_id, headers, runtime)

    def delete_quota_labels_with_options(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.DeleteQuotaLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.DeleteQuotaLabelsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keys):
            query['Keys'] = request.keys
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteQuotaLabels',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}/labels',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.DeleteQuotaLabelsResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_quota_labels_with_options_async(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.DeleteQuotaLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.DeleteQuotaLabelsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keys):
            query['Keys'] = request.keys
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteQuotaLabels',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}/labels',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.DeleteQuotaLabelsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_quota_labels(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.DeleteQuotaLabelsRequest,
    ) -> pai_studio_20220112_models.DeleteQuotaLabelsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_quota_labels_with_options(quota_id, request, headers, runtime)

    async def delete_quota_labels_async(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.DeleteQuotaLabelsRequest,
    ) -> pai_studio_20220112_models.DeleteQuotaLabelsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_quota_labels_with_options_async(quota_id, request, headers, runtime)

    def delete_resource_group_with_options(
        self,
        resource_group_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.DeleteResourceGroupResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteResourceGroup',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.DeleteResourceGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_resource_group_with_options_async(
        self,
        resource_group_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.DeleteResourceGroupResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteResourceGroup',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.DeleteResourceGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_resource_group(
        self,
        resource_group_id: str,
    ) -> pai_studio_20220112_models.DeleteResourceGroupResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_resource_group_with_options(resource_group_id, headers, runtime)

    async def delete_resource_group_async(
        self,
        resource_group_id: str,
    ) -> pai_studio_20220112_models.DeleteResourceGroupResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_resource_group_with_options_async(resource_group_id, headers, runtime)

    def delete_resource_group_machine_group_with_options(
        self,
        machine_group_id: str,
        resource_group_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.DeleteResourceGroupMachineGroupResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteResourceGroupMachineGroup',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}/machinegroups/{OpenApiUtilClient.get_encode_param(machine_group_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.DeleteResourceGroupMachineGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_resource_group_machine_group_with_options_async(
        self,
        machine_group_id: str,
        resource_group_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.DeleteResourceGroupMachineGroupResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteResourceGroupMachineGroup',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}/machinegroups/{OpenApiUtilClient.get_encode_param(machine_group_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.DeleteResourceGroupMachineGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_resource_group_machine_group(
        self,
        machine_group_id: str,
        resource_group_id: str,
    ) -> pai_studio_20220112_models.DeleteResourceGroupMachineGroupResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_resource_group_machine_group_with_options(machine_group_id, resource_group_id, headers, runtime)

    async def delete_resource_group_machine_group_async(
        self,
        machine_group_id: str,
        resource_group_id: str,
    ) -> pai_studio_20220112_models.DeleteResourceGroupMachineGroupResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_resource_group_machine_group_with_options_async(machine_group_id, resource_group_id, headers, runtime)

    def delete_training_job_with_options(
        self,
        training_job_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.DeleteTrainingJobResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteTrainingJob',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs/{OpenApiUtilClient.get_encode_param(training_job_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.DeleteTrainingJobResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_training_job_with_options_async(
        self,
        training_job_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.DeleteTrainingJobResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteTrainingJob',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs/{OpenApiUtilClient.get_encode_param(training_job_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.DeleteTrainingJobResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_training_job(
        self,
        training_job_id: str,
    ) -> pai_studio_20220112_models.DeleteTrainingJobResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_training_job_with_options(training_job_id, headers, runtime)

    async def delete_training_job_async(
        self,
        training_job_id: str,
    ) -> pai_studio_20220112_models.DeleteTrainingJobResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_training_job_with_options_async(training_job_id, headers, runtime)

    def delete_training_job_labels_with_options(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.DeleteTrainingJobLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.DeleteTrainingJobLabelsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keys):
            query['Keys'] = request.keys
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteTrainingJobLabels',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs/{OpenApiUtilClient.get_encode_param(training_job_id)}/labels',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.DeleteTrainingJobLabelsResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_training_job_labels_with_options_async(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.DeleteTrainingJobLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.DeleteTrainingJobLabelsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keys):
            query['Keys'] = request.keys
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteTrainingJobLabels',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs/{OpenApiUtilClient.get_encode_param(training_job_id)}/labels',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.DeleteTrainingJobLabelsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_training_job_labels(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.DeleteTrainingJobLabelsRequest,
    ) -> pai_studio_20220112_models.DeleteTrainingJobLabelsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_training_job_labels_with_options(training_job_id, request, headers, runtime)

    async def delete_training_job_labels_async(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.DeleteTrainingJobLabelsRequest,
    ) -> pai_studio_20220112_models.DeleteTrainingJobLabelsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_training_job_labels_with_options_async(training_job_id, request, headers, runtime)

    def get_ai4ddefault_bucket_with_options(
        self,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetAI4DDefaultBucketResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetAI4DDefaultBucket',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/ai4d/defaultbucket',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetAI4DDefaultBucketResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_ai4ddefault_bucket_with_options_async(
        self,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetAI4DDefaultBucketResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetAI4DDefaultBucket',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/ai4d/defaultbucket',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetAI4DDefaultBucketResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_ai4ddefault_bucket(self) -> pai_studio_20220112_models.GetAI4DDefaultBucketResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_ai4ddefault_bucket_with_options(headers, runtime)

    async def get_ai4ddefault_bucket_async(self) -> pai_studio_20220112_models.GetAI4DDefaultBucketResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_ai4ddefault_bucket_with_options_async(headers, runtime)

    def get_algorithm_with_options(
        self,
        algorithm_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetAlgorithmResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetAlgorithm',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/algorithms/{OpenApiUtilClient.get_encode_param(algorithm_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetAlgorithmResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_algorithm_with_options_async(
        self,
        algorithm_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetAlgorithmResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetAlgorithm',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/algorithms/{OpenApiUtilClient.get_encode_param(algorithm_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetAlgorithmResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_algorithm(
        self,
        algorithm_id: str,
    ) -> pai_studio_20220112_models.GetAlgorithmResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_algorithm_with_options(algorithm_id, headers, runtime)

    async def get_algorithm_async(
        self,
        algorithm_id: str,
    ) -> pai_studio_20220112_models.GetAlgorithmResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_algorithm_with_options_async(algorithm_id, headers, runtime)

    def get_algorithm_version_with_options(
        self,
        algorithm_id: str,
        algorithm_version: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetAlgorithmVersionResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetAlgorithmVersion',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/algorithms/{OpenApiUtilClient.get_encode_param(algorithm_id)}/versions/{OpenApiUtilClient.get_encode_param(algorithm_version)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetAlgorithmVersionResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_algorithm_version_with_options_async(
        self,
        algorithm_id: str,
        algorithm_version: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetAlgorithmVersionResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetAlgorithmVersion',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/algorithms/{OpenApiUtilClient.get_encode_param(algorithm_id)}/versions/{OpenApiUtilClient.get_encode_param(algorithm_version)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetAlgorithmVersionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_algorithm_version(
        self,
        algorithm_id: str,
        algorithm_version: str,
    ) -> pai_studio_20220112_models.GetAlgorithmVersionResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_algorithm_version_with_options(algorithm_id, algorithm_version, headers, runtime)

    async def get_algorithm_version_async(
        self,
        algorithm_id: str,
        algorithm_version: str,
    ) -> pai_studio_20220112_models.GetAlgorithmVersionResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_algorithm_version_with_options_async(algorithm_id, algorithm_version, headers, runtime)

    def get_component_with_options(
        self,
        component_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetComponentResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetComponent',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/components/{OpenApiUtilClient.get_encode_param(component_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetComponentResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_component_with_options_async(
        self,
        component_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetComponentResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetComponent',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/components/{OpenApiUtilClient.get_encode_param(component_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetComponentResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_component(
        self,
        component_id: str,
    ) -> pai_studio_20220112_models.GetComponentResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_component_with_options(component_id, headers, runtime)

    async def get_component_async(
        self,
        component_id: str,
    ) -> pai_studio_20220112_models.GetComponentResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_component_with_options_async(component_id, headers, runtime)

    def get_component_version_with_options(
        self,
        component_id: str,
        version: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetComponentVersionResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetComponentVersion',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/components/{OpenApiUtilClient.get_encode_param(component_id)}/versions/{OpenApiUtilClient.get_encode_param(version)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetComponentVersionResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_component_version_with_options_async(
        self,
        component_id: str,
        version: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetComponentVersionResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetComponentVersion',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/components/{OpenApiUtilClient.get_encode_param(component_id)}/versions/{OpenApiUtilClient.get_encode_param(version)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetComponentVersionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_component_version(
        self,
        component_id: str,
        version: str,
    ) -> pai_studio_20220112_models.GetComponentVersionResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_component_version_with_options(component_id, version, headers, runtime)

    async def get_component_version_async(
        self,
        component_id: str,
        version: str,
    ) -> pai_studio_20220112_models.GetComponentVersionResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_component_version_with_options_async(component_id, version, headers, runtime)

    def get_component_version_snapshot_with_options(
        self,
        snapshot_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetComponentVersionSnapshotResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetComponentVersionSnapshot',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/componentversionsnapshots/{OpenApiUtilClient.get_encode_param(snapshot_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetComponentVersionSnapshotResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_component_version_snapshot_with_options_async(
        self,
        snapshot_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetComponentVersionSnapshotResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetComponentVersionSnapshot',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/componentversionsnapshots/{OpenApiUtilClient.get_encode_param(snapshot_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetComponentVersionSnapshotResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_component_version_snapshot(
        self,
        snapshot_id: str,
    ) -> pai_studio_20220112_models.GetComponentVersionSnapshotResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_component_version_snapshot_with_options(snapshot_id, headers, runtime)

    async def get_component_version_snapshot_async(
        self,
        snapshot_id: str,
    ) -> pai_studio_20220112_models.GetComponentVersionSnapshotResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_component_version_snapshot_with_options_async(snapshot_id, headers, runtime)

    def get_instance_job_with_options(
        self,
        instance_job_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetInstanceJobResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetInstanceJob',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/instancejobs/{OpenApiUtilClient.get_encode_param(instance_job_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetInstanceJobResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_instance_job_with_options_async(
        self,
        instance_job_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetInstanceJobResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetInstanceJob',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/instancejobs/{OpenApiUtilClient.get_encode_param(instance_job_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetInstanceJobResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_instance_job(
        self,
        instance_job_id: str,
    ) -> pai_studio_20220112_models.GetInstanceJobResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_instance_job_with_options(instance_job_id, headers, runtime)

    async def get_instance_job_async(
        self,
        instance_job_id: str,
    ) -> pai_studio_20220112_models.GetInstanceJobResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_instance_job_with_options_async(instance_job_id, headers, runtime)

    def get_job_view_metrics_with_options(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.GetJobViewMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetJobViewMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.time_step):
            query['TimeStep'] = request.time_step
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetJobViewMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}/jobmetrics',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetJobViewMetricsResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_job_view_metrics_with_options_async(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.GetJobViewMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetJobViewMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.time_step):
            query['TimeStep'] = request.time_step
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetJobViewMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}/jobmetrics',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetJobViewMetricsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_job_view_metrics(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.GetJobViewMetricsRequest,
    ) -> pai_studio_20220112_models.GetJobViewMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_job_view_metrics_with_options(resource_group_id, request, headers, runtime)

    async def get_job_view_metrics_async(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.GetJobViewMetricsRequest,
    ) -> pai_studio_20220112_models.GetJobViewMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_job_view_metrics_with_options_async(resource_group_id, request, headers, runtime)

    def get_jobs_statistics_by_quota_with_options(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.GetJobsStatisticsByQuotaRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetJobsStatisticsByQuotaResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetJobsStatisticsByQuota',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}/statistics/jobs',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetJobsStatisticsByQuotaResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_jobs_statistics_by_quota_with_options_async(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.GetJobsStatisticsByQuotaRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetJobsStatisticsByQuotaResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetJobsStatisticsByQuota',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}/statistics/jobs',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetJobsStatisticsByQuotaResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_jobs_statistics_by_quota(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.GetJobsStatisticsByQuotaRequest,
    ) -> pai_studio_20220112_models.GetJobsStatisticsByQuotaResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_jobs_statistics_by_quota_with_options(quota_id, request, headers, runtime)

    async def get_jobs_statistics_by_quota_async(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.GetJobsStatisticsByQuotaRequest,
    ) -> pai_studio_20220112_models.GetJobsStatisticsByQuotaResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_jobs_statistics_by_quota_with_options_async(quota_id, request, headers, runtime)

    def get_jobs_statistics_by_resource_group_with_options(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.GetJobsStatisticsByResourceGroupRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetJobsStatisticsByResourceGroupResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceID'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetJobsStatisticsByResourceGroup',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}/statistics/jobs',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetJobsStatisticsByResourceGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_jobs_statistics_by_resource_group_with_options_async(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.GetJobsStatisticsByResourceGroupRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetJobsStatisticsByResourceGroupResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceID'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetJobsStatisticsByResourceGroup',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}/statistics/jobs',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetJobsStatisticsByResourceGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_jobs_statistics_by_resource_group(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.GetJobsStatisticsByResourceGroupRequest,
    ) -> pai_studio_20220112_models.GetJobsStatisticsByResourceGroupResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_jobs_statistics_by_resource_group_with_options(resource_group_id, request, headers, runtime)

    async def get_jobs_statistics_by_resource_group_async(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.GetJobsStatisticsByResourceGroupRequest,
    ) -> pai_studio_20220112_models.GetJobsStatisticsByResourceGroupResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_jobs_statistics_by_resource_group_with_options_async(resource_group_id, request, headers, runtime)

    def get_machine_group_with_options(
        self,
        machine_group_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetMachineGroupResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetMachineGroup',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/machinegroups/{OpenApiUtilClient.get_encode_param(machine_group_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetMachineGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_machine_group_with_options_async(
        self,
        machine_group_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetMachineGroupResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetMachineGroup',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/machinegroups/{OpenApiUtilClient.get_encode_param(machine_group_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetMachineGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_machine_group(
        self,
        machine_group_id: str,
    ) -> pai_studio_20220112_models.GetMachineGroupResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_machine_group_with_options(machine_group_id, headers, runtime)

    async def get_machine_group_async(
        self,
        machine_group_id: str,
    ) -> pai_studio_20220112_models.GetMachineGroupResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_machine_group_with_options_async(machine_group_id, headers, runtime)

    def get_node_metrics_with_options(
        self,
        resource_group_id: str,
        metric_type: str,
        request: pai_studio_20220112_models.GetNodeMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetNodeMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.gputype):
            query['GPUType'] = request.gputype
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.time_step):
            query['TimeStep'] = request.time_step
        if not UtilClient.is_unset(request.verbose):
            query['Verbose'] = request.verbose
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetNodeMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}/nodemetrics/{OpenApiUtilClient.get_encode_param(metric_type)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetNodeMetricsResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_node_metrics_with_options_async(
        self,
        resource_group_id: str,
        metric_type: str,
        request: pai_studio_20220112_models.GetNodeMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetNodeMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.gputype):
            query['GPUType'] = request.gputype
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.time_step):
            query['TimeStep'] = request.time_step
        if not UtilClient.is_unset(request.verbose):
            query['Verbose'] = request.verbose
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetNodeMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}/nodemetrics/{OpenApiUtilClient.get_encode_param(metric_type)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetNodeMetricsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_node_metrics(
        self,
        resource_group_id: str,
        metric_type: str,
        request: pai_studio_20220112_models.GetNodeMetricsRequest,
    ) -> pai_studio_20220112_models.GetNodeMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_node_metrics_with_options(resource_group_id, metric_type, request, headers, runtime)

    async def get_node_metrics_async(
        self,
        resource_group_id: str,
        metric_type: str,
        request: pai_studio_20220112_models.GetNodeMetricsRequest,
    ) -> pai_studio_20220112_models.GetNodeMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_node_metrics_with_options_async(resource_group_id, metric_type, request, headers, runtime)

    def get_node_view_metrics_with_options(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.GetNodeViewMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetNodeViewMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.node_id):
            query['NodeId'] = request.node_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.time_step):
            query['TimeStep'] = request.time_step
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetNodeViewMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}/nodeviewmetrics',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetNodeViewMetricsResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_node_view_metrics_with_options_async(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.GetNodeViewMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetNodeViewMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.node_id):
            query['NodeId'] = request.node_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.time_step):
            query['TimeStep'] = request.time_step
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetNodeViewMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}/nodeviewmetrics',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetNodeViewMetricsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_node_view_metrics(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.GetNodeViewMetricsRequest,
    ) -> pai_studio_20220112_models.GetNodeViewMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_node_view_metrics_with_options(resource_group_id, request, headers, runtime)

    async def get_node_view_metrics_async(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.GetNodeViewMetricsRequest,
    ) -> pai_studio_20220112_models.GetNodeViewMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_node_view_metrics_with_options_async(resource_group_id, request, headers, runtime)

    def get_operation_with_options(
        self,
        operation_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetOperationResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetOperation',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/operations/{OpenApiUtilClient.get_encode_param(operation_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetOperationResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_operation_with_options_async(
        self,
        operation_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetOperationResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetOperation',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/operations/{OpenApiUtilClient.get_encode_param(operation_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetOperationResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_operation(
        self,
        operation_id: str,
    ) -> pai_studio_20220112_models.GetOperationResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_operation_with_options(operation_id, headers, runtime)

    async def get_operation_async(
        self,
        operation_id: str,
    ) -> pai_studio_20220112_models.GetOperationResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_operation_with_options_async(operation_id, headers, runtime)

    def get_quota_with_options(
        self,
        quota_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetQuotaResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetQuota',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetQuotaResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_quota_with_options_async(
        self,
        quota_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetQuotaResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetQuota',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetQuotaResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_quota(
        self,
        quota_id: str,
    ) -> pai_studio_20220112_models.GetQuotaResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_quota_with_options(quota_id, headers, runtime)

    async def get_quota_async(
        self,
        quota_id: str,
    ) -> pai_studio_20220112_models.GetQuotaResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_quota_with_options_async(quota_id, headers, runtime)

    def get_quota_job_view_metrics_with_options(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.GetQuotaJobViewMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetQuotaJobViewMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.time_step):
            query['TimeStep'] = request.time_step
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetQuotaJobViewMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}/jobmetrics',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetQuotaJobViewMetricsResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_quota_job_view_metrics_with_options_async(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.GetQuotaJobViewMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetQuotaJobViewMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.time_step):
            query['TimeStep'] = request.time_step
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetQuotaJobViewMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}/jobmetrics',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetQuotaJobViewMetricsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_quota_job_view_metrics(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.GetQuotaJobViewMetricsRequest,
    ) -> pai_studio_20220112_models.GetQuotaJobViewMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_quota_job_view_metrics_with_options(quota_id, request, headers, runtime)

    async def get_quota_job_view_metrics_async(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.GetQuotaJobViewMetricsRequest,
    ) -> pai_studio_20220112_models.GetQuotaJobViewMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_quota_job_view_metrics_with_options_async(quota_id, request, headers, runtime)

    def get_quota_metrics_with_options(
        self,
        quota_id: str,
        metric_type: str,
        request: pai_studio_20220112_models.GetQuotaMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetQuotaMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.gputype):
            query['GPUType'] = request.gputype
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.time_step):
            query['TimeStep'] = request.time_step
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetQuotaMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}/metrics/{OpenApiUtilClient.get_encode_param(metric_type)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetQuotaMetricsResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_quota_metrics_with_options_async(
        self,
        quota_id: str,
        metric_type: str,
        request: pai_studio_20220112_models.GetQuotaMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetQuotaMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.gputype):
            query['GPUType'] = request.gputype
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.time_step):
            query['TimeStep'] = request.time_step
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetQuotaMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}/metrics/{OpenApiUtilClient.get_encode_param(metric_type)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetQuotaMetricsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_quota_metrics(
        self,
        quota_id: str,
        metric_type: str,
        request: pai_studio_20220112_models.GetQuotaMetricsRequest,
    ) -> pai_studio_20220112_models.GetQuotaMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_quota_metrics_with_options(quota_id, metric_type, request, headers, runtime)

    async def get_quota_metrics_async(
        self,
        quota_id: str,
        metric_type: str,
        request: pai_studio_20220112_models.GetQuotaMetricsRequest,
    ) -> pai_studio_20220112_models.GetQuotaMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_quota_metrics_with_options_async(quota_id, metric_type, request, headers, runtime)

    def get_quota_node_metrics_with_options(
        self,
        quota_id: str,
        metric_type: str,
        request: pai_studio_20220112_models.GetQuotaNodeMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetQuotaNodeMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.gputype):
            query['GPUType'] = request.gputype
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.time_step):
            query['TimeStep'] = request.time_step
        if not UtilClient.is_unset(request.verbose):
            query['Verbose'] = request.verbose
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetQuotaNodeMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}/nodemetrics/{OpenApiUtilClient.get_encode_param(metric_type)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetQuotaNodeMetricsResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_quota_node_metrics_with_options_async(
        self,
        quota_id: str,
        metric_type: str,
        request: pai_studio_20220112_models.GetQuotaNodeMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetQuotaNodeMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.gputype):
            query['GPUType'] = request.gputype
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.time_step):
            query['TimeStep'] = request.time_step
        if not UtilClient.is_unset(request.verbose):
            query['Verbose'] = request.verbose
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetQuotaNodeMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}/nodemetrics/{OpenApiUtilClient.get_encode_param(metric_type)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetQuotaNodeMetricsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_quota_node_metrics(
        self,
        quota_id: str,
        metric_type: str,
        request: pai_studio_20220112_models.GetQuotaNodeMetricsRequest,
    ) -> pai_studio_20220112_models.GetQuotaNodeMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_quota_node_metrics_with_options(quota_id, metric_type, request, headers, runtime)

    async def get_quota_node_metrics_async(
        self,
        quota_id: str,
        metric_type: str,
        request: pai_studio_20220112_models.GetQuotaNodeMetricsRequest,
    ) -> pai_studio_20220112_models.GetQuotaNodeMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_quota_node_metrics_with_options_async(quota_id, metric_type, request, headers, runtime)

    def get_quota_node_view_metrics_with_options(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.GetQuotaNodeViewMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetQuotaNodeViewMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.node_id):
            query['NodeId'] = request.node_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.time_step):
            query['TimeStep'] = request.time_step
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetQuotaNodeViewMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}/nodeviewmetrics',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetQuotaNodeViewMetricsResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_quota_node_view_metrics_with_options_async(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.GetQuotaNodeViewMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetQuotaNodeViewMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.node_id):
            query['NodeId'] = request.node_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.time_step):
            query['TimeStep'] = request.time_step
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetQuotaNodeViewMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}/nodeviewmetrics',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetQuotaNodeViewMetricsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_quota_node_view_metrics(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.GetQuotaNodeViewMetricsRequest,
    ) -> pai_studio_20220112_models.GetQuotaNodeViewMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_quota_node_view_metrics_with_options(quota_id, request, headers, runtime)

    async def get_quota_node_view_metrics_async(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.GetQuotaNodeViewMetricsRequest,
    ) -> pai_studio_20220112_models.GetQuotaNodeViewMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_quota_node_view_metrics_with_options_async(quota_id, request, headers, runtime)

    def get_quota_range_user_view_metrics_with_options(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.GetQuotaRangeUserViewMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetQuotaRangeUserViewMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.user_id):
            query['UserId'] = request.user_id
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetQuotaRangeUserViewMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}/rangeusermetrics',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetQuotaRangeUserViewMetricsResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_quota_range_user_view_metrics_with_options_async(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.GetQuotaRangeUserViewMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetQuotaRangeUserViewMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.user_id):
            query['UserId'] = request.user_id
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetQuotaRangeUserViewMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}/rangeusermetrics',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetQuotaRangeUserViewMetricsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_quota_range_user_view_metrics(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.GetQuotaRangeUserViewMetricsRequest,
    ) -> pai_studio_20220112_models.GetQuotaRangeUserViewMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_quota_range_user_view_metrics_with_options(quota_id, request, headers, runtime)

    async def get_quota_range_user_view_metrics_async(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.GetQuotaRangeUserViewMetricsRequest,
    ) -> pai_studio_20220112_models.GetQuotaRangeUserViewMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_quota_range_user_view_metrics_with_options_async(quota_id, request, headers, runtime)

    def get_quota_user_view_metrics_with_options(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.GetQuotaUserViewMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetQuotaUserViewMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.time_step):
            query['TimeStep'] = request.time_step
        if not UtilClient.is_unset(request.user_id):
            query['UserId'] = request.user_id
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetQuotaUserViewMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}/usermetrics',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetQuotaUserViewMetricsResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_quota_user_view_metrics_with_options_async(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.GetQuotaUserViewMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetQuotaUserViewMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.time_step):
            query['TimeStep'] = request.time_step
        if not UtilClient.is_unset(request.user_id):
            query['UserId'] = request.user_id
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetQuotaUserViewMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}/usermetrics',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetQuotaUserViewMetricsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_quota_user_view_metrics(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.GetQuotaUserViewMetricsRequest,
    ) -> pai_studio_20220112_models.GetQuotaUserViewMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_quota_user_view_metrics_with_options(quota_id, request, headers, runtime)

    async def get_quota_user_view_metrics_async(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.GetQuotaUserViewMetricsRequest,
    ) -> pai_studio_20220112_models.GetQuotaUserViewMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_quota_user_view_metrics_with_options_async(quota_id, request, headers, runtime)

    def get_range_user_view_metrics_with_options(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.GetRangeUserViewMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetRangeUserViewMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.user_id):
            query['UserId'] = request.user_id
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetRangeUserViewMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}/rangeusermetrics',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetRangeUserViewMetricsResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_range_user_view_metrics_with_options_async(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.GetRangeUserViewMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetRangeUserViewMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.user_id):
            query['UserId'] = request.user_id
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetRangeUserViewMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}/rangeusermetrics',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetRangeUserViewMetricsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_range_user_view_metrics(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.GetRangeUserViewMetricsRequest,
    ) -> pai_studio_20220112_models.GetRangeUserViewMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_range_user_view_metrics_with_options(resource_group_id, request, headers, runtime)

    async def get_range_user_view_metrics_async(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.GetRangeUserViewMetricsRequest,
    ) -> pai_studio_20220112_models.GetRangeUserViewMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_range_user_view_metrics_with_options_async(resource_group_id, request, headers, runtime)

    def get_resource_group_with_options(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.GetResourceGroupRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetResourceGroupResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.is_aiworkspace_data_enabled):
            query['IsAIWorkspaceDataEnabled'] = request.is_aiworkspace_data_enabled
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetResourceGroup',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetResourceGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_resource_group_with_options_async(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.GetResourceGroupRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetResourceGroupResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.is_aiworkspace_data_enabled):
            query['IsAIWorkspaceDataEnabled'] = request.is_aiworkspace_data_enabled
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetResourceGroup',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetResourceGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_resource_group(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.GetResourceGroupRequest,
    ) -> pai_studio_20220112_models.GetResourceGroupResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_resource_group_with_options(resource_group_id, request, headers, runtime)

    async def get_resource_group_async(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.GetResourceGroupRequest,
    ) -> pai_studio_20220112_models.GetResourceGroupResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_resource_group_with_options_async(resource_group_id, request, headers, runtime)

    def get_resource_group_machine_group_with_options(
        self,
        machine_group_id: str,
        resource_group_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetResourceGroupMachineGroupResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetResourceGroupMachineGroup',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}/machinegroups/{OpenApiUtilClient.get_encode_param(machine_group_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetResourceGroupMachineGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_resource_group_machine_group_with_options_async(
        self,
        machine_group_id: str,
        resource_group_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetResourceGroupMachineGroupResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetResourceGroupMachineGroup',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}/machinegroups/{OpenApiUtilClient.get_encode_param(machine_group_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetResourceGroupMachineGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_resource_group_machine_group(
        self,
        machine_group_id: str,
        resource_group_id: str,
    ) -> pai_studio_20220112_models.GetResourceGroupMachineGroupResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_resource_group_machine_group_with_options(machine_group_id, resource_group_id, headers, runtime)

    async def get_resource_group_machine_group_async(
        self,
        machine_group_id: str,
        resource_group_id: str,
    ) -> pai_studio_20220112_models.GetResourceGroupMachineGroupResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_resource_group_machine_group_with_options_async(machine_group_id, resource_group_id, headers, runtime)

    def get_resource_group_metrics_with_options(
        self,
        resource_group_id: str,
        metric_type: str,
        request: pai_studio_20220112_models.GetResourceGroupMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetResourceGroupMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.gputype):
            query['GPUType'] = request.gputype
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.time_step):
            query['TimeStep'] = request.time_step
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetResourceGroupMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}/metrics/{OpenApiUtilClient.get_encode_param(metric_type)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetResourceGroupMetricsResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_resource_group_metrics_with_options_async(
        self,
        resource_group_id: str,
        metric_type: str,
        request: pai_studio_20220112_models.GetResourceGroupMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetResourceGroupMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.gputype):
            query['GPUType'] = request.gputype
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.time_step):
            query['TimeStep'] = request.time_step
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetResourceGroupMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}/metrics/{OpenApiUtilClient.get_encode_param(metric_type)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetResourceGroupMetricsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_resource_group_metrics(
        self,
        resource_group_id: str,
        metric_type: str,
        request: pai_studio_20220112_models.GetResourceGroupMetricsRequest,
    ) -> pai_studio_20220112_models.GetResourceGroupMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_resource_group_metrics_with_options(resource_group_id, metric_type, request, headers, runtime)

    async def get_resource_group_metrics_async(
        self,
        resource_group_id: str,
        metric_type: str,
        request: pai_studio_20220112_models.GetResourceGroupMetricsRequest,
    ) -> pai_studio_20220112_models.GetResourceGroupMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_resource_group_metrics_with_options_async(resource_group_id, metric_type, request, headers, runtime)

    def get_resource_group_request_with_options(
        self,
        request: pai_studio_20220112_models.GetResourceGroupRequestRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetResourceGroupRequestResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.pod_status):
            query['PodStatus'] = request.pod_status
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupID'] = request.resource_group_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetResourceGroupRequest',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/data/request',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetResourceGroupRequestResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_resource_group_request_with_options_async(
        self,
        request: pai_studio_20220112_models.GetResourceGroupRequestRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetResourceGroupRequestResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.pod_status):
            query['PodStatus'] = request.pod_status
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupID'] = request.resource_group_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetResourceGroupRequest',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/data/request',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetResourceGroupRequestResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_resource_group_request(
        self,
        request: pai_studio_20220112_models.GetResourceGroupRequestRequest,
    ) -> pai_studio_20220112_models.GetResourceGroupRequestResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_resource_group_request_with_options(request, headers, runtime)

    async def get_resource_group_request_async(
        self,
        request: pai_studio_20220112_models.GetResourceGroupRequestRequest,
    ) -> pai_studio_20220112_models.GetResourceGroupRequestResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_resource_group_request_with_options_async(request, headers, runtime)

    def get_resource_group_total_with_options(
        self,
        request: pai_studio_20220112_models.GetResourceGroupTotalRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetResourceGroupTotalResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupID'] = request.resource_group_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetResourceGroupTotal',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/data/total',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetResourceGroupTotalResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_resource_group_total_with_options_async(
        self,
        request: pai_studio_20220112_models.GetResourceGroupTotalRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetResourceGroupTotalResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupID'] = request.resource_group_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetResourceGroupTotal',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/data/total',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetResourceGroupTotalResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_resource_group_total(
        self,
        request: pai_studio_20220112_models.GetResourceGroupTotalRequest,
    ) -> pai_studio_20220112_models.GetResourceGroupTotalResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_resource_group_total_with_options(request, headers, runtime)

    async def get_resource_group_total_async(
        self,
        request: pai_studio_20220112_models.GetResourceGroupTotalRequest,
    ) -> pai_studio_20220112_models.GetResourceGroupTotalResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_resource_group_total_with_options_async(request, headers, runtime)

    def get_service_identity_role_with_options(
        self,
        role_name: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetServiceIdentityRoleResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetServiceIdentityRole',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/ai4d/serviceidentityroles/{OpenApiUtilClient.get_encode_param(role_name)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetServiceIdentityRoleResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_service_identity_role_with_options_async(
        self,
        role_name: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetServiceIdentityRoleResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetServiceIdentityRole',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/ai4d/serviceidentityroles/{OpenApiUtilClient.get_encode_param(role_name)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetServiceIdentityRoleResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_service_identity_role(
        self,
        role_name: str,
    ) -> pai_studio_20220112_models.GetServiceIdentityRoleResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_service_identity_role_with_options(role_name, headers, runtime)

    async def get_service_identity_role_async(
        self,
        role_name: str,
    ) -> pai_studio_20220112_models.GetServiceIdentityRoleResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_service_identity_role_with_options_async(role_name, headers, runtime)

    def get_token_with_options(
        self,
        request: pai_studio_20220112_models.GetTokenRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetTokenResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.expire_time):
            query['ExpireTime'] = request.expire_time
        if not UtilClient.is_unset(request.training_job_id):
            query['TrainingJobId'] = request.training_job_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetToken',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/tokens',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetTokenResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_token_with_options_async(
        self,
        request: pai_studio_20220112_models.GetTokenRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetTokenResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.expire_time):
            query['ExpireTime'] = request.expire_time
        if not UtilClient.is_unset(request.training_job_id):
            query['TrainingJobId'] = request.training_job_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetToken',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/tokens',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetTokenResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_token(
        self,
        request: pai_studio_20220112_models.GetTokenRequest,
    ) -> pai_studio_20220112_models.GetTokenResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_token_with_options(request, headers, runtime)

    async def get_token_async(
        self,
        request: pai_studio_20220112_models.GetTokenRequest,
    ) -> pai_studio_20220112_models.GetTokenResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_token_with_options_async(request, headers, runtime)

    def get_training_job_with_options(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.GetTrainingJobRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetTrainingJobResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.token):
            query['Token'] = request.token
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetTrainingJob',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs/{OpenApiUtilClient.get_encode_param(training_job_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetTrainingJobResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_training_job_with_options_async(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.GetTrainingJobRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetTrainingJobResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.token):
            query['Token'] = request.token
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetTrainingJob',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs/{OpenApiUtilClient.get_encode_param(training_job_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetTrainingJobResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_training_job(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.GetTrainingJobRequest,
    ) -> pai_studio_20220112_models.GetTrainingJobResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_training_job_with_options(training_job_id, request, headers, runtime)

    async def get_training_job_async(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.GetTrainingJobRequest,
    ) -> pai_studio_20220112_models.GetTrainingJobResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_training_job_with_options_async(training_job_id, request, headers, runtime)

    def get_training_job_latest_metrics_with_options(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.GetTrainingJobLatestMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetTrainingJobLatestMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.names):
            query['Names'] = request.names
        if not UtilClient.is_unset(request.token):
            query['Token'] = request.token
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetTrainingJobLatestMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs/{OpenApiUtilClient.get_encode_param(training_job_id)}/latestmetrics',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetTrainingJobLatestMetricsResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_training_job_latest_metrics_with_options_async(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.GetTrainingJobLatestMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetTrainingJobLatestMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.names):
            query['Names'] = request.names
        if not UtilClient.is_unset(request.token):
            query['Token'] = request.token
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetTrainingJobLatestMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs/{OpenApiUtilClient.get_encode_param(training_job_id)}/latestmetrics',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetTrainingJobLatestMetricsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_training_job_latest_metrics(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.GetTrainingJobLatestMetricsRequest,
    ) -> pai_studio_20220112_models.GetTrainingJobLatestMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_training_job_latest_metrics_with_options(training_job_id, request, headers, runtime)

    async def get_training_job_latest_metrics_async(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.GetTrainingJobLatestMetricsRequest,
    ) -> pai_studio_20220112_models.GetTrainingJobLatestMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_training_job_latest_metrics_with_options_async(training_job_id, request, headers, runtime)

    def get_user_view_metrics_with_options(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.GetUserViewMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetUserViewMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.time_step):
            query['TimeStep'] = request.time_step
        if not UtilClient.is_unset(request.user_id):
            query['UserId'] = request.user_id
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetUserViewMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}/usermetrics',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetUserViewMetricsResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_user_view_metrics_with_options_async(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.GetUserViewMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.GetUserViewMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.time_step):
            query['TimeStep'] = request.time_step
        if not UtilClient.is_unset(request.user_id):
            query['UserId'] = request.user_id
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetUserViewMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}/usermetrics',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.GetUserViewMetricsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_user_view_metrics(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.GetUserViewMetricsRequest,
    ) -> pai_studio_20220112_models.GetUserViewMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_user_view_metrics_with_options(resource_group_id, request, headers, runtime)

    async def get_user_view_metrics_async(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.GetUserViewMetricsRequest,
    ) -> pai_studio_20220112_models.GetUserViewMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_user_view_metrics_with_options_async(resource_group_id, request, headers, runtime)

    def list_ai4dserivces_with_options(
        self,
        request: pai_studio_20220112_models.ListAI4DSerivcesRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListAI4DSerivcesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.service_type):
            query['ServiceType'] = request.service_type
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListAI4DSerivces',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/ai4d/services',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListAI4DSerivcesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_ai4dserivces_with_options_async(
        self,
        request: pai_studio_20220112_models.ListAI4DSerivcesRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListAI4DSerivcesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.service_type):
            query['ServiceType'] = request.service_type
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListAI4DSerivces',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/ai4d/services',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListAI4DSerivcesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_ai4dserivces(
        self,
        request: pai_studio_20220112_models.ListAI4DSerivcesRequest,
    ) -> pai_studio_20220112_models.ListAI4DSerivcesResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_ai4dserivces_with_options(request, headers, runtime)

    async def list_ai4dserivces_async(
        self,
        request: pai_studio_20220112_models.ListAI4DSerivcesRequest,
    ) -> pai_studio_20220112_models.ListAI4DSerivcesResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_ai4dserivces_with_options_async(request, headers, runtime)

    def list_algorithm_versions_with_options(
        self,
        algorithm_id: str,
        request: pai_studio_20220112_models.ListAlgorithmVersionsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListAlgorithmVersionsResponse:
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
            action='ListAlgorithmVersions',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/algorithms/{OpenApiUtilClient.get_encode_param(algorithm_id)}/versions',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListAlgorithmVersionsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_algorithm_versions_with_options_async(
        self,
        algorithm_id: str,
        request: pai_studio_20220112_models.ListAlgorithmVersionsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListAlgorithmVersionsResponse:
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
            action='ListAlgorithmVersions',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/algorithms/{OpenApiUtilClient.get_encode_param(algorithm_id)}/versions',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListAlgorithmVersionsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_algorithm_versions(
        self,
        algorithm_id: str,
        request: pai_studio_20220112_models.ListAlgorithmVersionsRequest,
    ) -> pai_studio_20220112_models.ListAlgorithmVersionsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_algorithm_versions_with_options(algorithm_id, request, headers, runtime)

    async def list_algorithm_versions_async(
        self,
        algorithm_id: str,
        request: pai_studio_20220112_models.ListAlgorithmVersionsRequest,
    ) -> pai_studio_20220112_models.ListAlgorithmVersionsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_algorithm_versions_with_options_async(algorithm_id, request, headers, runtime)

    def list_algorithms_with_options(
        self,
        request: pai_studio_20220112_models.ListAlgorithmsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListAlgorithmsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.algorithm_id):
            query['AlgorithmId'] = request.algorithm_id
        if not UtilClient.is_unset(request.algorithm_name):
            query['AlgorithmName'] = request.algorithm_name
        if not UtilClient.is_unset(request.algorithm_provider):
            query['AlgorithmProvider'] = request.algorithm_provider
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListAlgorithms',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/algorithms',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListAlgorithmsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_algorithms_with_options_async(
        self,
        request: pai_studio_20220112_models.ListAlgorithmsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListAlgorithmsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.algorithm_id):
            query['AlgorithmId'] = request.algorithm_id
        if not UtilClient.is_unset(request.algorithm_name):
            query['AlgorithmName'] = request.algorithm_name
        if not UtilClient.is_unset(request.algorithm_provider):
            query['AlgorithmProvider'] = request.algorithm_provider
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListAlgorithms',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/algorithms',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListAlgorithmsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_algorithms(
        self,
        request: pai_studio_20220112_models.ListAlgorithmsRequest,
    ) -> pai_studio_20220112_models.ListAlgorithmsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_algorithms_with_options(request, headers, runtime)

    async def list_algorithms_async(
        self,
        request: pai_studio_20220112_models.ListAlgorithmsRequest,
    ) -> pai_studio_20220112_models.ListAlgorithmsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_algorithms_with_options_async(request, headers, runtime)

    def list_component_version_snapshots_with_options(
        self,
        request: pai_studio_20220112_models.ListComponentVersionSnapshotsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListComponentVersionSnapshotsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.component_id):
            query['ComponentId'] = request.component_id
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.snapshot_id):
            query['SnapshotId'] = request.snapshot_id
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.version):
            query['Version'] = request.version
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListComponentVersionSnapshots',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/componentversionsnapshots',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListComponentVersionSnapshotsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_component_version_snapshots_with_options_async(
        self,
        request: pai_studio_20220112_models.ListComponentVersionSnapshotsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListComponentVersionSnapshotsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.component_id):
            query['ComponentId'] = request.component_id
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.snapshot_id):
            query['SnapshotId'] = request.snapshot_id
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.version):
            query['Version'] = request.version
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListComponentVersionSnapshots',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/componentversionsnapshots',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListComponentVersionSnapshotsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_component_version_snapshots(
        self,
        request: pai_studio_20220112_models.ListComponentVersionSnapshotsRequest,
    ) -> pai_studio_20220112_models.ListComponentVersionSnapshotsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_component_version_snapshots_with_options(request, headers, runtime)

    async def list_component_version_snapshots_async(
        self,
        request: pai_studio_20220112_models.ListComponentVersionSnapshotsRequest,
    ) -> pai_studio_20220112_models.ListComponentVersionSnapshotsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_component_version_snapshots_with_options_async(request, headers, runtime)

    def list_component_versions_with_options(
        self,
        component_id: str,
        tmp_req: pai_studio_20220112_models.ListComponentVersionsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListComponentVersionsResponse:
        UtilClient.validate_model(tmp_req)
        request = pai_studio_20220112_models.ListComponentVersionsShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.labels):
            request.labels_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.labels, 'Labels', 'json')
        query = {}
        if not UtilClient.is_unset(request.labels_shrink):
            query['Labels'] = request.labels_shrink
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.version):
            query['Version'] = request.version
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListComponentVersions',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/components/{OpenApiUtilClient.get_encode_param(component_id)}/versions',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListComponentVersionsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_component_versions_with_options_async(
        self,
        component_id: str,
        tmp_req: pai_studio_20220112_models.ListComponentVersionsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListComponentVersionsResponse:
        UtilClient.validate_model(tmp_req)
        request = pai_studio_20220112_models.ListComponentVersionsShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.labels):
            request.labels_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.labels, 'Labels', 'json')
        query = {}
        if not UtilClient.is_unset(request.labels_shrink):
            query['Labels'] = request.labels_shrink
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.version):
            query['Version'] = request.version
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListComponentVersions',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/components/{OpenApiUtilClient.get_encode_param(component_id)}/versions',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListComponentVersionsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_component_versions(
        self,
        component_id: str,
        request: pai_studio_20220112_models.ListComponentVersionsRequest,
    ) -> pai_studio_20220112_models.ListComponentVersionsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_component_versions_with_options(component_id, request, headers, runtime)

    async def list_component_versions_async(
        self,
        component_id: str,
        request: pai_studio_20220112_models.ListComponentVersionsRequest,
    ) -> pai_studio_20220112_models.ListComponentVersionsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_component_versions_with_options_async(component_id, request, headers, runtime)

    def list_components_with_options(
        self,
        tmp_req: pai_studio_20220112_models.ListComponentsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListComponentsResponse:
        UtilClient.validate_model(tmp_req)
        request = pai_studio_20220112_models.ListComponentsShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.labels):
            request.labels_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.labels, 'Labels', 'json')
        query = {}
        if not UtilClient.is_unset(request.component_id):
            query['ComponentId'] = request.component_id
        if not UtilClient.is_unset(request.component_ids):
            query['ComponentIds'] = request.component_ids
        if not UtilClient.is_unset(request.labels_shrink):
            query['Labels'] = request.labels_shrink
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.provider):
            query['Provider'] = request.provider
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListComponents',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/components',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListComponentsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_components_with_options_async(
        self,
        tmp_req: pai_studio_20220112_models.ListComponentsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListComponentsResponse:
        UtilClient.validate_model(tmp_req)
        request = pai_studio_20220112_models.ListComponentsShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.labels):
            request.labels_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.labels, 'Labels', 'json')
        query = {}
        if not UtilClient.is_unset(request.component_id):
            query['ComponentId'] = request.component_id
        if not UtilClient.is_unset(request.component_ids):
            query['ComponentIds'] = request.component_ids
        if not UtilClient.is_unset(request.labels_shrink):
            query['Labels'] = request.labels_shrink
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.provider):
            query['Provider'] = request.provider
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListComponents',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/components',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListComponentsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_components(
        self,
        request: pai_studio_20220112_models.ListComponentsRequest,
    ) -> pai_studio_20220112_models.ListComponentsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_components_with_options(request, headers, runtime)

    async def list_components_async(
        self,
        request: pai_studio_20220112_models.ListComponentsRequest,
    ) -> pai_studio_20220112_models.ListComponentsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_components_with_options_async(request, headers, runtime)

    def list_instance_jobs_with_options(
        self,
        request: pai_studio_20220112_models.ListInstanceJobsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListInstanceJobsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.instance_job_type):
            query['InstanceJobType'] = request.instance_job_type
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
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListInstanceJobs',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/instancejobs',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListInstanceJobsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_instance_jobs_with_options_async(
        self,
        request: pai_studio_20220112_models.ListInstanceJobsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListInstanceJobsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.instance_job_type):
            query['InstanceJobType'] = request.instance_job_type
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
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListInstanceJobs',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/instancejobs',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListInstanceJobsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_instance_jobs(
        self,
        request: pai_studio_20220112_models.ListInstanceJobsRequest,
    ) -> pai_studio_20220112_models.ListInstanceJobsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_instance_jobs_with_options(request, headers, runtime)

    async def list_instance_jobs_async(
        self,
        request: pai_studio_20220112_models.ListInstanceJobsRequest,
    ) -> pai_studio_20220112_models.ListInstanceJobsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_instance_jobs_with_options_async(request, headers, runtime)

    def list_node_types_with_options(
        self,
        request: pai_studio_20220112_models.ListNodeTypesRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListNodeTypesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.accelerator_type):
            query['AcceleratorType'] = request.accelerator_type
        if not UtilClient.is_unset(request.gputype):
            query['GPUType'] = request.gputype
        if not UtilClient.is_unset(request.node_types):
            query['NodeTypes'] = request.node_types
        if not UtilClient.is_unset(request.quota_id):
            query['QuotaId'] = request.quota_id
        if not UtilClient.is_unset(request.resource_group_ids):
            query['ResourceGroupIds'] = request.resource_group_ids
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListNodeTypes',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/nodetypes',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListNodeTypesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_node_types_with_options_async(
        self,
        request: pai_studio_20220112_models.ListNodeTypesRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListNodeTypesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.accelerator_type):
            query['AcceleratorType'] = request.accelerator_type
        if not UtilClient.is_unset(request.gputype):
            query['GPUType'] = request.gputype
        if not UtilClient.is_unset(request.node_types):
            query['NodeTypes'] = request.node_types
        if not UtilClient.is_unset(request.quota_id):
            query['QuotaId'] = request.quota_id
        if not UtilClient.is_unset(request.resource_group_ids):
            query['ResourceGroupIds'] = request.resource_group_ids
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListNodeTypes',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/nodetypes',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListNodeTypesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_node_types(
        self,
        request: pai_studio_20220112_models.ListNodeTypesRequest,
    ) -> pai_studio_20220112_models.ListNodeTypesResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_node_types_with_options(request, headers, runtime)

    async def list_node_types_async(
        self,
        request: pai_studio_20220112_models.ListNodeTypesRequest,
    ) -> pai_studio_20220112_models.ListNodeTypesResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_node_types_with_options_async(request, headers, runtime)

    def list_nodes_with_options(
        self,
        request: pai_studio_20220112_models.ListNodesRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListNodesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.accelerator_type):
            query['AcceleratorType'] = request.accelerator_type
        if not UtilClient.is_unset(request.gputype):
            query['GPUType'] = request.gputype
        if not UtilClient.is_unset(request.node_statuses):
            query['NodeStatuses'] = request.node_statuses
        if not UtilClient.is_unset(request.node_types):
            query['NodeTypes'] = request.node_types
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.order_statuses):
            query['OrderStatuses'] = request.order_statuses
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.quota_id):
            query['QuotaId'] = request.quota_id
        if not UtilClient.is_unset(request.resource_group_ids):
            query['ResourceGroupIds'] = request.resource_group_ids
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListNodes',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/nodes',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListNodesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_nodes_with_options_async(
        self,
        request: pai_studio_20220112_models.ListNodesRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListNodesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.accelerator_type):
            query['AcceleratorType'] = request.accelerator_type
        if not UtilClient.is_unset(request.gputype):
            query['GPUType'] = request.gputype
        if not UtilClient.is_unset(request.node_statuses):
            query['NodeStatuses'] = request.node_statuses
        if not UtilClient.is_unset(request.node_types):
            query['NodeTypes'] = request.node_types
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.order_statuses):
            query['OrderStatuses'] = request.order_statuses
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.quota_id):
            query['QuotaId'] = request.quota_id
        if not UtilClient.is_unset(request.resource_group_ids):
            query['ResourceGroupIds'] = request.resource_group_ids
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListNodes',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/nodes',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListNodesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_nodes(
        self,
        request: pai_studio_20220112_models.ListNodesRequest,
    ) -> pai_studio_20220112_models.ListNodesResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_nodes_with_options(request, headers, runtime)

    async def list_nodes_async(
        self,
        request: pai_studio_20220112_models.ListNodesRequest,
    ) -> pai_studio_20220112_models.ListNodesResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_nodes_with_options_async(request, headers, runtime)

    def list_operations_with_options(
        self,
        request: pai_studio_20220112_models.ListOperationsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListOperationsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.object_id):
            query['ObjectId'] = request.object_id
        if not UtilClient.is_unset(request.object_type):
            query['ObjectType'] = request.object_type
        if not UtilClient.is_unset(request.operation_id):
            query['OperationId'] = request.operation_id
        if not UtilClient.is_unset(request.operation_type):
            query['OperationType'] = request.operation_type
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
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListOperations',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/operations',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListOperationsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_operations_with_options_async(
        self,
        request: pai_studio_20220112_models.ListOperationsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListOperationsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.object_id):
            query['ObjectId'] = request.object_id
        if not UtilClient.is_unset(request.object_type):
            query['ObjectType'] = request.object_type
        if not UtilClient.is_unset(request.operation_id):
            query['OperationId'] = request.operation_id
        if not UtilClient.is_unset(request.operation_type):
            query['OperationType'] = request.operation_type
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
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListOperations',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/operations',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListOperationsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_operations(
        self,
        request: pai_studio_20220112_models.ListOperationsRequest,
    ) -> pai_studio_20220112_models.ListOperationsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_operations_with_options(request, headers, runtime)

    async def list_operations_async(
        self,
        request: pai_studio_20220112_models.ListOperationsRequest,
    ) -> pai_studio_20220112_models.ListOperationsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_operations_with_options_async(request, headers, runtime)

    def list_permissions_with_options(
        self,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListPermissionsResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='ListPermissions',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/permissions',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListPermissionsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_permissions_with_options_async(
        self,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListPermissionsResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='ListPermissions',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/permissions',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListPermissionsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_permissions(self) -> pai_studio_20220112_models.ListPermissionsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_permissions_with_options(headers, runtime)

    async def list_permissions_async(self) -> pai_studio_20220112_models.ListPermissionsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_permissions_with_options_async(headers, runtime)

    def list_quotas_with_options(
        self,
        request: pai_studio_20220112_models.ListQuotasRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListQuotasResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.parent_quota_id):
            query['ParentQuotaId'] = request.parent_quota_id
        if not UtilClient.is_unset(request.quota_ids):
            query['QuotaIds'] = request.quota_ids
        if not UtilClient.is_unset(request.quota_name):
            query['QuotaName'] = request.quota_name
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.statuses):
            query['Statuses'] = request.statuses
        if not UtilClient.is_unset(request.workspace_ids):
            query['WorkspaceIds'] = request.workspace_ids
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListQuotas',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListQuotasResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_quotas_with_options_async(
        self,
        request: pai_studio_20220112_models.ListQuotasRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListQuotasResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.parent_quota_id):
            query['ParentQuotaId'] = request.parent_quota_id
        if not UtilClient.is_unset(request.quota_ids):
            query['QuotaIds'] = request.quota_ids
        if not UtilClient.is_unset(request.quota_name):
            query['QuotaName'] = request.quota_name
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.statuses):
            query['Statuses'] = request.statuses
        if not UtilClient.is_unset(request.workspace_ids):
            query['WorkspaceIds'] = request.workspace_ids
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListQuotas',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListQuotasResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_quotas(
        self,
        request: pai_studio_20220112_models.ListQuotasRequest,
    ) -> pai_studio_20220112_models.ListQuotasResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_quotas_with_options(request, headers, runtime)

    async def list_quotas_async(
        self,
        request: pai_studio_20220112_models.ListQuotasRequest,
    ) -> pai_studio_20220112_models.ListQuotasResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_quotas_with_options_async(request, headers, runtime)

    def list_resource_group_machine_groups_with_options(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.ListResourceGroupMachineGroupsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListResourceGroupMachineGroupsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.creator_id):
            query['CreatorID'] = request.creator_id
        if not UtilClient.is_unset(request.ecs_spec):
            query['EcsSpec'] = request.ecs_spec
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.payment_duration):
            query['PaymentDuration'] = request.payment_duration
        if not UtilClient.is_unset(request.payment_duration_unit):
            query['PaymentDurationUnit'] = request.payment_duration_unit
        if not UtilClient.is_unset(request.payment_type):
            query['PaymentType'] = request.payment_type
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListResourceGroupMachineGroups',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}/machinegroups',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListResourceGroupMachineGroupsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_resource_group_machine_groups_with_options_async(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.ListResourceGroupMachineGroupsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListResourceGroupMachineGroupsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.creator_id):
            query['CreatorID'] = request.creator_id
        if not UtilClient.is_unset(request.ecs_spec):
            query['EcsSpec'] = request.ecs_spec
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.payment_duration):
            query['PaymentDuration'] = request.payment_duration
        if not UtilClient.is_unset(request.payment_duration_unit):
            query['PaymentDurationUnit'] = request.payment_duration_unit
        if not UtilClient.is_unset(request.payment_type):
            query['PaymentType'] = request.payment_type
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListResourceGroupMachineGroups',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}/machinegroups',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListResourceGroupMachineGroupsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_resource_group_machine_groups(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.ListResourceGroupMachineGroupsRequest,
    ) -> pai_studio_20220112_models.ListResourceGroupMachineGroupsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_resource_group_machine_groups_with_options(resource_group_id, request, headers, runtime)

    async def list_resource_group_machine_groups_async(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.ListResourceGroupMachineGroupsRequest,
    ) -> pai_studio_20220112_models.ListResourceGroupMachineGroupsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_resource_group_machine_groups_with_options_async(resource_group_id, request, headers, runtime)

    def list_resource_groups_with_options(
        self,
        request: pai_studio_20220112_models.ListResourceGroupsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListResourceGroupsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.computing_resource_provider):
            query['ComputingResourceProvider'] = request.computing_resource_provider
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.show_all):
            query['ShowAll'] = request.show_all
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListResourceGroups',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListResourceGroupsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_resource_groups_with_options_async(
        self,
        request: pai_studio_20220112_models.ListResourceGroupsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListResourceGroupsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.computing_resource_provider):
            query['ComputingResourceProvider'] = request.computing_resource_provider
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.show_all):
            query['ShowAll'] = request.show_all
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListResourceGroups',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListResourceGroupsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_resource_groups(
        self,
        request: pai_studio_20220112_models.ListResourceGroupsRequest,
    ) -> pai_studio_20220112_models.ListResourceGroupsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_resource_groups_with_options(request, headers, runtime)

    async def list_resource_groups_async(
        self,
        request: pai_studio_20220112_models.ListResourceGroupsRequest,
    ) -> pai_studio_20220112_models.ListResourceGroupsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_resource_groups_with_options_async(request, headers, runtime)

    def list_training_job_events_with_options(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.ListTrainingJobEventsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListTrainingJobEventsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.token):
            query['Token'] = request.token
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListTrainingJobEvents',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs/{OpenApiUtilClient.get_encode_param(training_job_id)}/events',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListTrainingJobEventsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_training_job_events_with_options_async(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.ListTrainingJobEventsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListTrainingJobEventsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.token):
            query['Token'] = request.token
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListTrainingJobEvents',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs/{OpenApiUtilClient.get_encode_param(training_job_id)}/events',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListTrainingJobEventsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_training_job_events(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.ListTrainingJobEventsRequest,
    ) -> pai_studio_20220112_models.ListTrainingJobEventsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_training_job_events_with_options(training_job_id, request, headers, runtime)

    async def list_training_job_events_async(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.ListTrainingJobEventsRequest,
    ) -> pai_studio_20220112_models.ListTrainingJobEventsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_training_job_events_with_options_async(training_job_id, request, headers, runtime)

    def list_training_job_instance_events_with_options(
        self,
        training_job_id: str,
        instance_id: str,
        request: pai_studio_20220112_models.ListTrainingJobInstanceEventsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListTrainingJobInstanceEventsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.token):
            query['Token'] = request.token
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListTrainingJobInstanceEvents',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs/{OpenApiUtilClient.get_encode_param(training_job_id)}/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/events',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListTrainingJobInstanceEventsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_training_job_instance_events_with_options_async(
        self,
        training_job_id: str,
        instance_id: str,
        request: pai_studio_20220112_models.ListTrainingJobInstanceEventsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListTrainingJobInstanceEventsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.token):
            query['Token'] = request.token
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListTrainingJobInstanceEvents',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs/{OpenApiUtilClient.get_encode_param(training_job_id)}/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/events',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListTrainingJobInstanceEventsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_training_job_instance_events(
        self,
        training_job_id: str,
        instance_id: str,
        request: pai_studio_20220112_models.ListTrainingJobInstanceEventsRequest,
    ) -> pai_studio_20220112_models.ListTrainingJobInstanceEventsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_training_job_instance_events_with_options(training_job_id, instance_id, request, headers, runtime)

    async def list_training_job_instance_events_async(
        self,
        training_job_id: str,
        instance_id: str,
        request: pai_studio_20220112_models.ListTrainingJobInstanceEventsRequest,
    ) -> pai_studio_20220112_models.ListTrainingJobInstanceEventsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_training_job_instance_events_with_options_async(training_job_id, instance_id, request, headers, runtime)

    def list_training_job_instance_metrics_with_options(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.ListTrainingJobInstanceMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListTrainingJobInstanceMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.metric_type):
            query['MetricType'] = request.metric_type
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.time_step):
            query['TimeStep'] = request.time_step
        if not UtilClient.is_unset(request.token):
            query['Token'] = request.token
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListTrainingJobInstanceMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs/{OpenApiUtilClient.get_encode_param(training_job_id)}/instancemetrics',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListTrainingJobInstanceMetricsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_training_job_instance_metrics_with_options_async(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.ListTrainingJobInstanceMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListTrainingJobInstanceMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.metric_type):
            query['MetricType'] = request.metric_type
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.time_step):
            query['TimeStep'] = request.time_step
        if not UtilClient.is_unset(request.token):
            query['Token'] = request.token
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListTrainingJobInstanceMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs/{OpenApiUtilClient.get_encode_param(training_job_id)}/instancemetrics',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListTrainingJobInstanceMetricsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_training_job_instance_metrics(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.ListTrainingJobInstanceMetricsRequest,
    ) -> pai_studio_20220112_models.ListTrainingJobInstanceMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_training_job_instance_metrics_with_options(training_job_id, request, headers, runtime)

    async def list_training_job_instance_metrics_async(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.ListTrainingJobInstanceMetricsRequest,
    ) -> pai_studio_20220112_models.ListTrainingJobInstanceMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_training_job_instance_metrics_with_options_async(training_job_id, request, headers, runtime)

    def list_training_job_logs_with_options(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.ListTrainingJobLogsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListTrainingJobLogsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.token):
            query['Token'] = request.token
        if not UtilClient.is_unset(request.worker_id):
            query['WorkerId'] = request.worker_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListTrainingJobLogs',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs/{OpenApiUtilClient.get_encode_param(training_job_id)}/logs',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListTrainingJobLogsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_training_job_logs_with_options_async(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.ListTrainingJobLogsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListTrainingJobLogsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.token):
            query['Token'] = request.token
        if not UtilClient.is_unset(request.worker_id):
            query['WorkerId'] = request.worker_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListTrainingJobLogs',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs/{OpenApiUtilClient.get_encode_param(training_job_id)}/logs',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListTrainingJobLogsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_training_job_logs(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.ListTrainingJobLogsRequest,
    ) -> pai_studio_20220112_models.ListTrainingJobLogsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_training_job_logs_with_options(training_job_id, request, headers, runtime)

    async def list_training_job_logs_async(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.ListTrainingJobLogsRequest,
    ) -> pai_studio_20220112_models.ListTrainingJobLogsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_training_job_logs_with_options_async(training_job_id, request, headers, runtime)

    def list_training_job_metrics_with_options(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.ListTrainingJobMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListTrainingJobMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.token):
            query['Token'] = request.token
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListTrainingJobMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs/{OpenApiUtilClient.get_encode_param(training_job_id)}/metrics',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListTrainingJobMetricsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_training_job_metrics_with_options_async(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.ListTrainingJobMetricsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListTrainingJobMetricsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.token):
            query['Token'] = request.token
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListTrainingJobMetrics',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs/{OpenApiUtilClient.get_encode_param(training_job_id)}/metrics',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListTrainingJobMetricsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_training_job_metrics(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.ListTrainingJobMetricsRequest,
    ) -> pai_studio_20220112_models.ListTrainingJobMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_training_job_metrics_with_options(training_job_id, request, headers, runtime)

    async def list_training_job_metrics_async(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.ListTrainingJobMetricsRequest,
    ) -> pai_studio_20220112_models.ListTrainingJobMetricsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_training_job_metrics_with_options_async(training_job_id, request, headers, runtime)

    def list_training_jobs_with_options(
        self,
        tmp_req: pai_studio_20220112_models.ListTrainingJobsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListTrainingJobsResponse:
        UtilClient.validate_model(tmp_req)
        request = pai_studio_20220112_models.ListTrainingJobsShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.labels):
            request.labels_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.labels, 'Labels', 'json')
        query = {}
        if not UtilClient.is_unset(request.algorithm_name):
            query['AlgorithmName'] = request.algorithm_name
        if not UtilClient.is_unset(request.algorithm_provider):
            query['AlgorithmProvider'] = request.algorithm_provider
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.is_temp_algo):
            query['IsTempAlgo'] = request.is_temp_algo
        if not UtilClient.is_unset(request.labels_shrink):
            query['Labels'] = request.labels_shrink
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        if not UtilClient.is_unset(request.training_job_id):
            query['TrainingJobId'] = request.training_job_id
        if not UtilClient.is_unset(request.training_job_name):
            query['TrainingJobName'] = request.training_job_name
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListTrainingJobs',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListTrainingJobsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_training_jobs_with_options_async(
        self,
        tmp_req: pai_studio_20220112_models.ListTrainingJobsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ListTrainingJobsResponse:
        UtilClient.validate_model(tmp_req)
        request = pai_studio_20220112_models.ListTrainingJobsShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.labels):
            request.labels_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.labels, 'Labels', 'json')
        query = {}
        if not UtilClient.is_unset(request.algorithm_name):
            query['AlgorithmName'] = request.algorithm_name
        if not UtilClient.is_unset(request.algorithm_provider):
            query['AlgorithmProvider'] = request.algorithm_provider
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.is_temp_algo):
            query['IsTempAlgo'] = request.is_temp_algo
        if not UtilClient.is_unset(request.labels_shrink):
            query['Labels'] = request.labels_shrink
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        if not UtilClient.is_unset(request.training_job_id):
            query['TrainingJobId'] = request.training_job_id
        if not UtilClient.is_unset(request.training_job_name):
            query['TrainingJobName'] = request.training_job_name
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListTrainingJobs',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ListTrainingJobsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_training_jobs(
        self,
        request: pai_studio_20220112_models.ListTrainingJobsRequest,
    ) -> pai_studio_20220112_models.ListTrainingJobsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_training_jobs_with_options(request, headers, runtime)

    async def list_training_jobs_async(
        self,
        request: pai_studio_20220112_models.ListTrainingJobsRequest,
    ) -> pai_studio_20220112_models.ListTrainingJobsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_training_jobs_with_options_async(request, headers, runtime)

    def release_algorithm_with_options(
        self,
        algorithm_id: str,
        request: pai_studio_20220112_models.ReleaseAlgorithmRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ReleaseAlgorithmResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.target_algorithm_name):
            query['TargetAlgorithmName'] = request.target_algorithm_name
        if not UtilClient.is_unset(request.update_if_exists):
            query['UpdateIfExists'] = request.update_if_exists
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ReleaseAlgorithm',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/algorithms/{OpenApiUtilClient.get_encode_param(algorithm_id)}/release',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ReleaseAlgorithmResponse(),
            self.call_api(params, req, runtime)
        )

    async def release_algorithm_with_options_async(
        self,
        algorithm_id: str,
        request: pai_studio_20220112_models.ReleaseAlgorithmRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ReleaseAlgorithmResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.target_algorithm_name):
            query['TargetAlgorithmName'] = request.target_algorithm_name
        if not UtilClient.is_unset(request.update_if_exists):
            query['UpdateIfExists'] = request.update_if_exists
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ReleaseAlgorithm',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/algorithms/{OpenApiUtilClient.get_encode_param(algorithm_id)}/release',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ReleaseAlgorithmResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def release_algorithm(
        self,
        algorithm_id: str,
        request: pai_studio_20220112_models.ReleaseAlgorithmRequest,
    ) -> pai_studio_20220112_models.ReleaseAlgorithmResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.release_algorithm_with_options(algorithm_id, request, headers, runtime)

    async def release_algorithm_async(
        self,
        algorithm_id: str,
        request: pai_studio_20220112_models.ReleaseAlgorithmRequest,
    ) -> pai_studio_20220112_models.ReleaseAlgorithmResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.release_algorithm_with_options_async(algorithm_id, request, headers, runtime)

    def release_algorithm_version_with_options(
        self,
        algorithm_id: str,
        algorithm_version: str,
        request: pai_studio_20220112_models.ReleaseAlgorithmVersionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ReleaseAlgorithmVersionResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.target_algorithm_name):
            query['TargetAlgorithmName'] = request.target_algorithm_name
        if not UtilClient.is_unset(request.target_algorithm_version):
            query['TargetAlgorithmVersion'] = request.target_algorithm_version
        if not UtilClient.is_unset(request.update_if_exists):
            query['UpdateIfExists'] = request.update_if_exists
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ReleaseAlgorithmVersion',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/algorithms/{OpenApiUtilClient.get_encode_param(algorithm_id)}/versions/{OpenApiUtilClient.get_encode_param(algorithm_version)}/release',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ReleaseAlgorithmVersionResponse(),
            self.call_api(params, req, runtime)
        )

    async def release_algorithm_version_with_options_async(
        self,
        algorithm_id: str,
        algorithm_version: str,
        request: pai_studio_20220112_models.ReleaseAlgorithmVersionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ReleaseAlgorithmVersionResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.target_algorithm_name):
            query['TargetAlgorithmName'] = request.target_algorithm_name
        if not UtilClient.is_unset(request.target_algorithm_version):
            query['TargetAlgorithmVersion'] = request.target_algorithm_version
        if not UtilClient.is_unset(request.update_if_exists):
            query['UpdateIfExists'] = request.update_if_exists
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ReleaseAlgorithmVersion',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/algorithms/{OpenApiUtilClient.get_encode_param(algorithm_id)}/versions/{OpenApiUtilClient.get_encode_param(algorithm_version)}/release',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ReleaseAlgorithmVersionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def release_algorithm_version(
        self,
        algorithm_id: str,
        algorithm_version: str,
        request: pai_studio_20220112_models.ReleaseAlgorithmVersionRequest,
    ) -> pai_studio_20220112_models.ReleaseAlgorithmVersionResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.release_algorithm_version_with_options(algorithm_id, algorithm_version, request, headers, runtime)

    async def release_algorithm_version_async(
        self,
        algorithm_id: str,
        algorithm_version: str,
        request: pai_studio_20220112_models.ReleaseAlgorithmVersionRequest,
    ) -> pai_studio_20220112_models.ReleaseAlgorithmVersionResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.release_algorithm_version_with_options_async(algorithm_id, algorithm_version, request, headers, runtime)

    def scale_quota_with_options(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.ScaleQuotaRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ScaleQuotaResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.min):
            body['Min'] = request.min
        if not UtilClient.is_unset(request.resource_group_ids):
            body['ResourceGroupIds'] = request.resource_group_ids
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ScaleQuota',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}/action/scale',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ScaleQuotaResponse(),
            self.call_api(params, req, runtime)
        )

    async def scale_quota_with_options_async(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.ScaleQuotaRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.ScaleQuotaResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.min):
            body['Min'] = request.min
        if not UtilClient.is_unset(request.resource_group_ids):
            body['ResourceGroupIds'] = request.resource_group_ids
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ScaleQuota',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}/action/scale',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.ScaleQuotaResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def scale_quota(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.ScaleQuotaRequest,
    ) -> pai_studio_20220112_models.ScaleQuotaResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.scale_quota_with_options(quota_id, request, headers, runtime)

    async def scale_quota_async(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.ScaleQuotaRequest,
    ) -> pai_studio_20220112_models.ScaleQuotaResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.scale_quota_with_options_async(quota_id, request, headers, runtime)

    def stop_arrears_training_job_with_options(
        self,
        training_job_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.StopArrearsTrainingJobResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='StopArrearsTrainingJob',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs/{OpenApiUtilClient.get_encode_param(training_job_id)}/arrearage/stop',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.StopArrearsTrainingJobResponse(),
            self.call_api(params, req, runtime)
        )

    async def stop_arrears_training_job_with_options_async(
        self,
        training_job_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.StopArrearsTrainingJobResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='StopArrearsTrainingJob',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs/{OpenApiUtilClient.get_encode_param(training_job_id)}/arrearage/stop',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.StopArrearsTrainingJobResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def stop_arrears_training_job(
        self,
        training_job_id: str,
    ) -> pai_studio_20220112_models.StopArrearsTrainingJobResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.stop_arrears_training_job_with_options(training_job_id, headers, runtime)

    async def stop_arrears_training_job_async(
        self,
        training_job_id: str,
    ) -> pai_studio_20220112_models.StopArrearsTrainingJobResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.stop_arrears_training_job_with_options_async(training_job_id, headers, runtime)

    def stop_training_job_with_options(
        self,
        training_job_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.StopTrainingJobResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='StopTrainingJob',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs/{OpenApiUtilClient.get_encode_param(training_job_id)}/stop',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.StopTrainingJobResponse(),
            self.call_api(params, req, runtime)
        )

    async def stop_training_job_with_options_async(
        self,
        training_job_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.StopTrainingJobResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='StopTrainingJob',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs/{OpenApiUtilClient.get_encode_param(training_job_id)}/stop',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.StopTrainingJobResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def stop_training_job(
        self,
        training_job_id: str,
    ) -> pai_studio_20220112_models.StopTrainingJobResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.stop_training_job_with_options(training_job_id, headers, runtime)

    async def stop_training_job_async(
        self,
        training_job_id: str,
    ) -> pai_studio_20220112_models.StopTrainingJobResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.stop_training_job_with_options_async(training_job_id, headers, runtime)

    def update_algorithm_with_options(
        self,
        algorithm_id: str,
        request: pai_studio_20220112_models.UpdateAlgorithmRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.UpdateAlgorithmResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.algorithm_description):
            body['AlgorithmDescription'] = request.algorithm_description
        if not UtilClient.is_unset(request.display_name):
            body['DisplayName'] = request.display_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateAlgorithm',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/algorithms/{OpenApiUtilClient.get_encode_param(algorithm_id)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.UpdateAlgorithmResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_algorithm_with_options_async(
        self,
        algorithm_id: str,
        request: pai_studio_20220112_models.UpdateAlgorithmRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.UpdateAlgorithmResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.algorithm_description):
            body['AlgorithmDescription'] = request.algorithm_description
        if not UtilClient.is_unset(request.display_name):
            body['DisplayName'] = request.display_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateAlgorithm',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/algorithms/{OpenApiUtilClient.get_encode_param(algorithm_id)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.UpdateAlgorithmResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_algorithm(
        self,
        algorithm_id: str,
        request: pai_studio_20220112_models.UpdateAlgorithmRequest,
    ) -> pai_studio_20220112_models.UpdateAlgorithmResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_algorithm_with_options(algorithm_id, request, headers, runtime)

    async def update_algorithm_async(
        self,
        algorithm_id: str,
        request: pai_studio_20220112_models.UpdateAlgorithmRequest,
    ) -> pai_studio_20220112_models.UpdateAlgorithmResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.update_algorithm_with_options_async(algorithm_id, request, headers, runtime)

    def update_algorithm_version_with_options(
        self,
        algorithm_id: str,
        algorithm_version: str,
        tmp_req: pai_studio_20220112_models.UpdateAlgorithmVersionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.UpdateAlgorithmVersionResponse:
        UtilClient.validate_model(tmp_req)
        request = pai_studio_20220112_models.UpdateAlgorithmVersionShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.algorithm_spec):
            request.algorithm_spec_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.algorithm_spec, 'AlgorithmSpec', 'json')
        body = {}
        if not UtilClient.is_unset(request.algorithm_spec_shrink):
            body['AlgorithmSpec'] = request.algorithm_spec_shrink
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateAlgorithmVersion',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/algorithms/{OpenApiUtilClient.get_encode_param(algorithm_id)}/versions/{OpenApiUtilClient.get_encode_param(algorithm_version)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.UpdateAlgorithmVersionResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_algorithm_version_with_options_async(
        self,
        algorithm_id: str,
        algorithm_version: str,
        tmp_req: pai_studio_20220112_models.UpdateAlgorithmVersionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.UpdateAlgorithmVersionResponse:
        UtilClient.validate_model(tmp_req)
        request = pai_studio_20220112_models.UpdateAlgorithmVersionShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.algorithm_spec):
            request.algorithm_spec_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.algorithm_spec, 'AlgorithmSpec', 'json')
        body = {}
        if not UtilClient.is_unset(request.algorithm_spec_shrink):
            body['AlgorithmSpec'] = request.algorithm_spec_shrink
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateAlgorithmVersion',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/algorithms/{OpenApiUtilClient.get_encode_param(algorithm_id)}/versions/{OpenApiUtilClient.get_encode_param(algorithm_version)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.UpdateAlgorithmVersionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_algorithm_version(
        self,
        algorithm_id: str,
        algorithm_version: str,
        request: pai_studio_20220112_models.UpdateAlgorithmVersionRequest,
    ) -> pai_studio_20220112_models.UpdateAlgorithmVersionResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_algorithm_version_with_options(algorithm_id, algorithm_version, request, headers, runtime)

    async def update_algorithm_version_async(
        self,
        algorithm_id: str,
        algorithm_version: str,
        request: pai_studio_20220112_models.UpdateAlgorithmVersionRequest,
    ) -> pai_studio_20220112_models.UpdateAlgorithmVersionResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.update_algorithm_version_with_options_async(algorithm_id, algorithm_version, request, headers, runtime)

    def update_component_with_options(
        self,
        component_id: str,
        request: pai_studio_20220112_models.UpdateComponentRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.UpdateComponentResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.display_name):
            body['DisplayName'] = request.display_name
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateComponent',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/components/{OpenApiUtilClient.get_encode_param(component_id)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.UpdateComponentResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_component_with_options_async(
        self,
        component_id: str,
        request: pai_studio_20220112_models.UpdateComponentRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.UpdateComponentResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.display_name):
            body['DisplayName'] = request.display_name
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateComponent',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/components/{OpenApiUtilClient.get_encode_param(component_id)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.UpdateComponentResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_component(
        self,
        component_id: str,
        request: pai_studio_20220112_models.UpdateComponentRequest,
    ) -> pai_studio_20220112_models.UpdateComponentResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_component_with_options(component_id, request, headers, runtime)

    async def update_component_async(
        self,
        component_id: str,
        request: pai_studio_20220112_models.UpdateComponentRequest,
    ) -> pai_studio_20220112_models.UpdateComponentResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.update_component_with_options_async(component_id, request, headers, runtime)

    def update_component_version_with_options(
        self,
        component_id: str,
        version: str,
        request: pai_studio_20220112_models.UpdateComponentVersionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.UpdateComponentVersionResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.labels):
            query['Labels'] = request.labels
        if not UtilClient.is_unset(request.spec):
            query['Spec'] = request.spec
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateComponentVersion',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/components/{OpenApiUtilClient.get_encode_param(component_id)}/versions/{OpenApiUtilClient.get_encode_param(version)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.UpdateComponentVersionResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_component_version_with_options_async(
        self,
        component_id: str,
        version: str,
        request: pai_studio_20220112_models.UpdateComponentVersionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.UpdateComponentVersionResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.labels):
            query['Labels'] = request.labels
        if not UtilClient.is_unset(request.spec):
            query['Spec'] = request.spec
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateComponentVersion',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/components/{OpenApiUtilClient.get_encode_param(component_id)}/versions/{OpenApiUtilClient.get_encode_param(version)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.UpdateComponentVersionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_component_version(
        self,
        component_id: str,
        version: str,
        request: pai_studio_20220112_models.UpdateComponentVersionRequest,
    ) -> pai_studio_20220112_models.UpdateComponentVersionResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_component_version_with_options(component_id, version, request, headers, runtime)

    async def update_component_version_async(
        self,
        component_id: str,
        version: str,
        request: pai_studio_20220112_models.UpdateComponentVersionRequest,
    ) -> pai_studio_20220112_models.UpdateComponentVersionResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.update_component_version_with_options_async(component_id, version, request, headers, runtime)

    def update_component_version_snapshot_with_options(
        self,
        snapshot_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.UpdateComponentVersionSnapshotResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='UpdateComponentVersionSnapshot',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/componentversionsnapshots/{OpenApiUtilClient.get_encode_param(snapshot_id)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.UpdateComponentVersionSnapshotResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_component_version_snapshot_with_options_async(
        self,
        snapshot_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.UpdateComponentVersionSnapshotResponse:
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='UpdateComponentVersionSnapshot',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/componentversionsnapshots/{OpenApiUtilClient.get_encode_param(snapshot_id)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.UpdateComponentVersionSnapshotResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_component_version_snapshot(
        self,
        snapshot_id: str,
    ) -> pai_studio_20220112_models.UpdateComponentVersionSnapshotResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_component_version_snapshot_with_options(snapshot_id, headers, runtime)

    async def update_component_version_snapshot_async(
        self,
        snapshot_id: str,
    ) -> pai_studio_20220112_models.UpdateComponentVersionSnapshotResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.update_component_version_snapshot_with_options_async(snapshot_id, headers, runtime)

    def update_quota_with_options(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.UpdateQuotaRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.UpdateQuotaResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateQuota',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.UpdateQuotaResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_quota_with_options_async(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.UpdateQuotaRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.UpdateQuotaResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateQuota',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.UpdateQuotaResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_quota(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.UpdateQuotaRequest,
    ) -> pai_studio_20220112_models.UpdateQuotaResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_quota_with_options(quota_id, request, headers, runtime)

    async def update_quota_async(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.UpdateQuotaRequest,
    ) -> pai_studio_20220112_models.UpdateQuotaResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.update_quota_with_options_async(quota_id, request, headers, runtime)

    def update_quota_labels_with_options(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.UpdateQuotaLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.UpdateQuotaLabelsResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateQuotaLabels',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}/labels',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.UpdateQuotaLabelsResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_quota_labels_with_options_async(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.UpdateQuotaLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.UpdateQuotaLabelsResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateQuotaLabels',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/quotas/{OpenApiUtilClient.get_encode_param(quota_id)}/labels',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.UpdateQuotaLabelsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_quota_labels(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.UpdateQuotaLabelsRequest,
    ) -> pai_studio_20220112_models.UpdateQuotaLabelsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_quota_labels_with_options(quota_id, request, headers, runtime)

    async def update_quota_labels_async(
        self,
        quota_id: str,
        request: pai_studio_20220112_models.UpdateQuotaLabelsRequest,
    ) -> pai_studio_20220112_models.UpdateQuotaLabelsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.update_quota_labels_with_options_async(quota_id, request, headers, runtime)

    def update_resource_group_with_options(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.UpdateResourceGroupRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.UpdateResourceGroupResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.unbind):
            body['Unbind'] = request.unbind
        if not UtilClient.is_unset(request.user_vpc):
            body['UserVpc'] = request.user_vpc
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateResourceGroup',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.UpdateResourceGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_resource_group_with_options_async(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.UpdateResourceGroupRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.UpdateResourceGroupResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.unbind):
            body['Unbind'] = request.unbind
        if not UtilClient.is_unset(request.user_vpc):
            body['UserVpc'] = request.user_vpc
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateResourceGroup',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/resources/{OpenApiUtilClient.get_encode_param(resource_group_id)}',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.UpdateResourceGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_resource_group(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.UpdateResourceGroupRequest,
    ) -> pai_studio_20220112_models.UpdateResourceGroupResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_resource_group_with_options(resource_group_id, request, headers, runtime)

    async def update_resource_group_async(
        self,
        resource_group_id: str,
        request: pai_studio_20220112_models.UpdateResourceGroupRequest,
    ) -> pai_studio_20220112_models.UpdateResourceGroupResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.update_resource_group_with_options_async(resource_group_id, request, headers, runtime)

    def update_training_job_labels_with_options(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.UpdateTrainingJobLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.UpdateTrainingJobLabelsResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateTrainingJobLabels',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs/{OpenApiUtilClient.get_encode_param(training_job_id)}/labels',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.UpdateTrainingJobLabelsResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_training_job_labels_with_options_async(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.UpdateTrainingJobLabelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> pai_studio_20220112_models.UpdateTrainingJobLabelsResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.labels):
            body['Labels'] = request.labels
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateTrainingJobLabels',
            version='2022-01-12',
            protocol='HTTPS',
            pathname=f'/api/v1/trainingjobs/{OpenApiUtilClient.get_encode_param(training_job_id)}/labels',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_studio_20220112_models.UpdateTrainingJobLabelsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_training_job_labels(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.UpdateTrainingJobLabelsRequest,
    ) -> pai_studio_20220112_models.UpdateTrainingJobLabelsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_training_job_labels_with_options(training_job_id, request, headers, runtime)

    async def update_training_job_labels_async(
        self,
        training_job_id: str,
        request: pai_studio_20220112_models.UpdateTrainingJobLabelsRequest,
    ) -> pai_studio_20220112_models.UpdateTrainingJobLabelsResponse:
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.update_training_job_labels_with_options_async(training_job_id, request, headers, runtime)
