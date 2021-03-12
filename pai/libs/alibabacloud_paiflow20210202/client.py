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

from pai.libs.alibabacloud_paiflow20210202 import models as paiflow_20210202_models


class Client(OpenApiClient):
    """
    *\
    """
    def __init__(self, config):
        super(Client, self).__init__(config)
        self._endpoint_rule = 'central'
        self._endpoint_map = {
            'cn-beijing': 'pai.cn-beijing.aliyuncs.com',
            'cn-hangzhou': 'pai.cn-hangzhou.data.aliyun.com',
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
            'ap-south-1': 'pai.ap-south-1.aliyuncs.com'
        }
        self.check_config(config)
        self._endpoint = self.get_endpoint('paiflow', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

    def get_endpoint(self, product_id, region_id, endpoint_rule, network, suffix, endpoint_map, endpoint):
        if not UtilClient.empty(endpoint):
            return endpoint
        if not UtilClient.is_unset(endpoint_map) and not UtilClient.empty(endpoint_map.get(region_id)):
            return endpoint_map.get(region_id)
        return EndpointUtilClient.get_endpoint_rules(product_id, region_id, endpoint_rule, network, suffix)

    def create_pipeline(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_pipeline_with_options(request, headers, runtime)

    def create_pipeline_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.workspace_id):
            body['WorkspaceId'] = request.workspace_id
        if not UtilClient.is_unset(request.manifest):
            body['Manifest'] = request.manifest
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return paiflow_20210202_models.CreatePipelineResponse().from_map(
            self.do_roarequest('CreatePipeline', '2021-02-02', 'HTTPS', 'POST', 'AK', '/api/v1/pipelines', 'json', req, runtime)
        )

    def create_pipeline_release(self, pipeline_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_pipeline_release_with_options(pipeline_id, request, headers, runtime)

    def create_pipeline_release_with_options(self, pipeline_id, request, headers, runtime):
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.target_pipeline_provider):
            body['TargetPipelineProvider'] = request.target_pipeline_provider
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return paiflow_20210202_models.CreatePipelineReleaseResponse().from_map(
            self.do_roarequest('CreatePipelineRelease', '2021-02-02', 'HTTPS', 'PUT', 'AK', '/api/v1/pipelines/%s/releases' % TeaConverter.to_unicode(pipeline_id), 'json', req, runtime)
        )

    def create_run(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_run_with_options(request, headers, runtime)

    def create_run_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.pipeline_id):
            body['PipelineId'] = request.pipeline_id
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.pipeline_manifest):
            body['PipelineManifest'] = request.pipeline_manifest
        if not UtilClient.is_unset(request.arguments):
            body['Arguments'] = request.arguments
        if not UtilClient.is_unset(request.no_confirm_required):
            body['NoConfirmRequired'] = request.no_confirm_required
        if not UtilClient.is_unset(request.workspace_id):
            body['WorkspaceId'] = request.workspace_id
        if not UtilClient.is_unset(request.source):
            body['Source'] = request.source
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return paiflow_20210202_models.CreateRunResponse().from_map(
            self.do_roarequest('CreateRun', '2021-02-02', 'HTTPS', 'POST', 'AK', '/api/v1/runs', 'json', req, runtime)
        )

    def delete_pipeline(self, pipeline_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_pipeline_with_options(pipeline_id, headers, runtime)

    def delete_pipeline_with_options(self, pipeline_id, headers, runtime):
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        return paiflow_20210202_models.DeletePipelineResponse().from_map(
            self.do_roarequest('DeletePipeline', '2021-02-02', 'HTTPS', 'DELETE', 'AK', '/api/v1/pipelines/%s' % TeaConverter.to_unicode(pipeline_id), 'json', req, runtime)
        )

    def get_caller_provider(self):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_caller_provider_with_options(headers, runtime)

    def get_caller_provider_with_options(self, headers, runtime):
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        return paiflow_20210202_models.GetCallerProviderResponse().from_map(
            self.do_roarequest('GetCallerProvider', '2021-02-02', 'HTTPS', 'GET', 'AK', '/api/v1/provider', 'json', req, runtime)
        )

    def get_node(self, run_id, node_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_node_with_options(run_id, node_id, request, headers, runtime)

    def get_node_with_options(self, run_id, node_id, request, headers, runtime):
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.depth):
            query['Depth'] = request.depth
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        return paiflow_20210202_models.GetNodeResponse().from_map(
            self.do_roarequest('GetNode', '2021-02-02', 'HTTPS', 'GET', 'AK', '/api/v1/runs/%s/nodes/%s' % (TeaConverter.to_unicode(run_id), TeaConverter.to_unicode(node_id)), 'json', req, runtime)
        )

    def get_pipeline(self, pipeline_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_pipeline_with_options(pipeline_id, headers, runtime)

    def get_pipeline_with_options(self, pipeline_id, headers, runtime):
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        return paiflow_20210202_models.GetPipelineResponse().from_map(
            self.do_roarequest('GetPipeline', '2021-02-02', 'HTTPS', 'GET', 'AK', '/api/v1/pipelines/%s' % TeaConverter.to_unicode(pipeline_id), 'json', req, runtime)
        )

    def get_pipeline_schema(self, pipeline_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_pipeline_schema_with_options(pipeline_id, headers, runtime)

    def get_pipeline_schema_with_options(self, pipeline_id, headers, runtime):
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        return paiflow_20210202_models.GetPipelineSchemaResponse().from_map(
            self.do_roarequest('GetPipelineSchema', '2021-02-02', 'HTTPS', 'GET', 'AK', '/api/v1/pipelines/%s/schema' % TeaConverter.to_unicode(pipeline_id), 'json', req, runtime)
        )

    def get_run(self, run_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_run_with_options(run_id, headers, runtime)

    def get_run_with_options(self, run_id, headers, runtime):
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        return paiflow_20210202_models.GetRunResponse().from_map(
            self.do_roarequest('GetRun', '2021-02-02', 'HTTPS', 'GET', 'AK', '/api/v1/runs/%s' % TeaConverter.to_unicode(run_id), 'json', req, runtime)
        )

    def list_node_logs(self, run_id, node_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_node_logs_with_options(run_id, node_id, request, headers, runtime)

    def list_node_logs_with_options(self, run_id, node_id, request, headers, runtime):
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.offset):
            query['Offset'] = request.offset
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.from_time_in_seconds):
            query['FromTimeInSeconds'] = request.from_time_in_seconds
        if not UtilClient.is_unset(request.keyword):
            query['Keyword'] = request.keyword
        if not UtilClient.is_unset(request.reverse):
            query['Reverse'] = request.reverse
        if not UtilClient.is_unset(request.to_time_in_seconds):
            query['ToTimeInSeconds'] = request.to_time_in_seconds
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        return paiflow_20210202_models.ListNodeLogsResponse().from_map(
            self.do_roarequest('ListNodeLogs', '2021-02-02', 'HTTPS', 'GET', 'AK', '/api/v1/runs/%s/nodes/%s/logs' % (TeaConverter.to_unicode(run_id), TeaConverter.to_unicode(node_id)), 'json', req, runtime)
        )

    def list_node_outputs(self, run_id, node_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_node_outputs_with_options(run_id, node_id, request, headers, runtime)

    def list_node_outputs_with_options(self, run_id, node_id, request, headers, runtime):
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.depth):
            query['Depth'] = request.depth
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.type):
            query['Type'] = request.type
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        return paiflow_20210202_models.ListNodeOutputsResponse().from_map(
            self.do_roarequest('ListNodeOutputs', '2021-02-02', 'HTTPS', 'GET', 'AK', '/api/v1/runs/%s/nodes/%s/outputs' % (TeaConverter.to_unicode(run_id), TeaConverter.to_unicode(node_id)), 'json', req, runtime)
        )

    def list_pipeline_privileges(self, pipeline_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_pipeline_privileges_with_options(pipeline_id, headers, runtime)

    def list_pipeline_privileges_with_options(self, pipeline_id, headers, runtime):
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        return paiflow_20210202_models.ListPipelinePrivilegesResponse().from_map(
            self.do_roarequest('ListPipelinePrivileges', '2021-02-02', 'HTTPS', 'GET', 'AK', '/api/v1/pipelines/%s/privileges' % TeaConverter.to_unicode(pipeline_id), 'json', req, runtime)
        )

    def list_pipelines(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_pipelines_with_options(request, headers, runtime)

    def list_pipelines_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.pipeline_identifier):
            query['PipelineIdentifier'] = request.pipeline_identifier
        if not UtilClient.is_unset(request.pipeline_provider):
            query['PipelineProvider'] = request.pipeline_provider
        if not UtilClient.is_unset(request.pipeline_version):
            query['PipelineVersion'] = request.pipeline_version
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        return paiflow_20210202_models.ListPipelinesResponse().from_map(
            self.do_roarequest('ListPipelines', '2021-02-02', 'HTTPS', 'GET', 'AK', '/api/v1/pipelines', 'json', req, runtime)
        )

    def list_runs(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_runs_with_options(request, headers, runtime)

    def list_runs_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.experiment_id):
            query['ExperimentId'] = request.experiment_id
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.pipeline_id):
            query['PipelineId'] = request.pipeline_id
        if not UtilClient.is_unset(request.run_id):
            query['RunId'] = request.run_id
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.source):
            query['Source'] = request.source
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        return paiflow_20210202_models.ListRunsResponse().from_map(
            self.do_roarequest('ListRuns', '2021-02-02', 'HTTPS', 'GET', 'AK', '/api/v1/runs', 'json', req, runtime)
        )

    def list_runs_status(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_runs_status_with_options(request, headers, runtime)

    def list_runs_status_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.run_ids):
            body['RunIds'] = request.run_ids
        if not UtilClient.is_unset(request.node_infos):
            body['NodeInfos'] = request.node_infos
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return paiflow_20210202_models.ListRunsStatusResponse().from_map(
            self.do_roarequest('ListRunsStatus', '2021-02-02', 'HTTPS', 'PUT', 'AK', '/api/v1/runs', 'json', req, runtime)
        )

    def start_run(self, run_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.start_run_with_options(run_id, headers, runtime)

    def start_run_with_options(self, run_id, headers, runtime):
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        return paiflow_20210202_models.StartRunResponse().from_map(
            self.do_roarequest('StartRun', '2021-02-02', 'HTTPS', 'PUT', 'AK', '/api/v1/runs/%s/start' % TeaConverter.to_unicode(run_id), 'json', req, runtime)
        )

    def terminate_run(self, run_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.terminate_run_with_options(run_id, headers, runtime)

    def terminate_run_with_options(self, run_id, headers, runtime):
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        return paiflow_20210202_models.TerminateRunResponse().from_map(
            self.do_roarequest('TerminateRun', '2021-02-02', 'HTTPS', 'PUT', 'AK', '/api/v1/runs/%s/termination' % TeaConverter.to_unicode(run_id), 'json', req, runtime)
        )

    def update_pipeline(self, pipeline_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_pipeline_with_options(pipeline_id, request, headers, runtime)

    def update_pipeline_with_options(self, pipeline_id, request, headers, runtime):
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.manifest):
            body['Manifest'] = request.manifest
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return paiflow_20210202_models.UpdatePipelineResponse().from_map(
            self.do_roarequest('UpdatePipeline', '2021-02-02', 'HTTPS', 'PUT', 'AK', '/api/v1/pipelines/%s' % TeaConverter.to_unicode(pipeline_id), 'json', req, runtime)
        )

    def update_pipeline_privileges(self, pipeline_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_pipeline_privileges_with_options(pipeline_id, request, headers, runtime)

    def update_pipeline_privileges_with_options(self, pipeline_id, request, headers, runtime):
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.users):
            body['Users'] = request.users
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return paiflow_20210202_models.UpdatePipelinePrivilegesResponse().from_map(
            self.do_roarequest('UpdatePipelinePrivileges', '2021-02-02', 'HTTPS', 'PUT', 'AK', '/api/v1/pipelines/%s/privileges' % TeaConverter.to_unicode(pipeline_id), 'json', req, runtime)
        )

    def update_run(self, run_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_run_with_options(run_id, request, headers, runtime)

    def update_run_with_options(self, run_id, request, headers, runtime):
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return paiflow_20210202_models.UpdateRunResponse().from_map(
            self.do_roarequest('UpdateRun', '2021-02-02', 'HTTPS', 'PUT', 'AK', '/api/v1/runs/%s' % TeaConverter.to_unicode(run_id), 'json', req, runtime)
        )
