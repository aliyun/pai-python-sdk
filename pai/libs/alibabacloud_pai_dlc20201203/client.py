# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import unicode_literals

from Tea.core import TeaCore
from Tea.converter import TeaConverter

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient
# from alibabacloud_pai_dlc20201203 import models as pai_dlc_20201203_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient


from pai.libs.alibabacloud_pai_dlc20201203 import models as pai_dlc_20201203_models


class Client(OpenApiClient):
    """
    *\
    """
    def __init__(self, config):
        super(Client, self).__init__(config)
        self._endpoint_rule = ''
        self.check_config(config)
        self._endpoint = self.get_endpoint('pai-dlc', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

    def get_endpoint(self, product_id, region_id, endpoint_rule, network, suffix, endpoint_map, endpoint):
        if not UtilClient.empty(endpoint):
            return endpoint
        if not UtilClient.is_unset(endpoint_map) and not UtilClient.empty(endpoint_map.get(region_id)):
            return endpoint_map.get(region_id)
        return EndpointUtilClient.get_endpoint_rules(product_id, region_id, endpoint_rule, network, suffix)

    def batch_get_jobs_statistics(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.batch_get_jobs_statistics_with_options(request, headers, runtime)

    def batch_get_jobs_statistics_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.workspace_ids):
            query['WorkspaceIds'] = request.workspace_ids
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='BatchGetJobsStatistics',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/batch/statistics/jobs',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.BatchGetJobsStatisticsResponse(),
            self.call_api(params, req, runtime)
        )

    def create_code_source(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_code_source_with_options(request, headers, runtime)

    def create_code_source_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        body = {}
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
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateCodeSource',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/codesources',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.CreateCodeSourceResponse(),
            self.call_api(params, req, runtime)
        )

    def create_data_source(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_data_source_with_options(request, headers, runtime)

    def create_data_source_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.data_source_type):
            body['DataSourceType'] = request.data_source_type
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.display_name):
            body['DisplayName'] = request.display_name
        if not UtilClient.is_unset(request.endpoint):
            body['Endpoint'] = request.endpoint
        if not UtilClient.is_unset(request.file_system_id):
            body['FileSystemId'] = request.file_system_id
        if not UtilClient.is_unset(request.is_proxy):
            body['IsProxy'] = request.is_proxy
        if not UtilClient.is_unset(request.mount_path):
            body['MountPath'] = request.mount_path
        if not UtilClient.is_unset(request.options):
            body['Options'] = request.options
        if not UtilClient.is_unset(request.path):
            body['Path'] = request.path
        if not UtilClient.is_unset(request.proxy_content):
            body['ProxyContent'] = request.proxy_content
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateDataSource',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/datasources',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.CreateDataSourceResponse(),
            self.call_api(params, req, runtime)
        )

    def create_debugger_config(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_debugger_config_with_options(request, headers, runtime)

    def create_debugger_config_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.content):
            body['Content'] = request.content
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.display_name):
            body['DisplayName'] = request.display_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateDebuggerConfig',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/debuggerconfigs',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.CreateDebuggerConfigResponse(),
            self.call_api(params, req, runtime)
        )

    def create_debugger_job_issue(self, job_id, debugger_job_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_debugger_job_issue_with_options(job_id, debugger_job_id, request, headers, runtime)

    def create_debugger_job_issue_with_options(self, job_id, debugger_job_id, request, headers, runtime):
        UtilClient.validate_model(request)
        job_id = OpenApiUtilClient.get_encode_param(job_id)
        debugger_job_id = OpenApiUtilClient.get_encode_param(debugger_job_id)
        body = {}
        if not UtilClient.is_unset(request.debugger_job_issue):
            body['DebuggerJobIssue'] = request.debugger_job_issue
        if not UtilClient.is_unset(request.debugger_rule_name):
            body['DebuggerRuleName'] = request.debugger_rule_name
        if not UtilClient.is_unset(request.token):
            body['Token'] = request.token
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateDebuggerJobIssue',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/jobs/%s/debuggerjobs/%s/issues' % (TeaConverter.to_unicode(job_id), TeaConverter.to_unicode(debugger_job_id)),
            method='POST',
            auth_type='Anonymous',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.CreateDebuggerJobIssueResponse(),
            self.call_api(params, req, runtime)
        )

    def create_job(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_job_with_options(request, headers, runtime)

    def create_job_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.code_source):
            body['CodeSource'] = request.code_source
        if not UtilClient.is_unset(request.data_sources):
            body['DataSources'] = request.data_sources
        if not UtilClient.is_unset(request.debugger_config_content):
            body['DebuggerConfigContent'] = request.debugger_config_content
        if not UtilClient.is_unset(request.display_name):
            body['DisplayName'] = request.display_name
        if not UtilClient.is_unset(request.elastic_spec):
            body['ElasticSpec'] = request.elastic_spec
        if not UtilClient.is_unset(request.envs):
            body['Envs'] = request.envs
        if not UtilClient.is_unset(request.job_max_running_time_minutes):
            body['JobMaxRunningTimeMinutes'] = request.job_max_running_time_minutes
        if not UtilClient.is_unset(request.job_specs):
            body['JobSpecs'] = request.job_specs
        if not UtilClient.is_unset(request.job_type):
            body['JobType'] = request.job_type
        if not UtilClient.is_unset(request.priority):
            body['Priority'] = request.priority
        if not UtilClient.is_unset(request.resource_id):
            body['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.settings):
            body['Settings'] = request.settings
        if not UtilClient.is_unset(request.thirdparty_lib_dir):
            body['ThirdpartyLibDir'] = request.thirdparty_lib_dir
        if not UtilClient.is_unset(request.thirdparty_libs):
            body['ThirdpartyLibs'] = request.thirdparty_libs
        if not UtilClient.is_unset(request.user_command):
            body['UserCommand'] = request.user_command
        if not UtilClient.is_unset(request.user_vpc):
            body['UserVpc'] = request.user_vpc
        if not UtilClient.is_unset(request.workspace_id):
            body['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateJob',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/jobs',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.CreateJobResponse(),
            self.call_api(params, req, runtime)
        )

    def create_quota(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_quota_with_options(request, headers, runtime)

    def create_quota_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.quota_detail):
            body['QuotaDetail'] = request.quota_detail
        if not UtilClient.is_unset(request.quota_name):
            body['QuotaName'] = request.quota_name
        if not UtilClient.is_unset(request.quota_type):
            body['QuotaType'] = request.quota_type
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateQuota',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/quotas',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.CreateQuotaResponse(),
            self.call_api(params, req, runtime)
        )

    def create_tensorboard(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_tensorboard_with_options(request, headers, runtime)

    def create_tensorboard_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.data_source_id):
            body['DataSourceId'] = request.data_source_id
        if not UtilClient.is_unset(request.data_source_type):
            body['DataSourceType'] = request.data_source_type
        if not UtilClient.is_unset(request.data_sources):
            body['DataSources'] = request.data_sources
        if not UtilClient.is_unset(request.display_name):
            body['DisplayName'] = request.display_name
        if not UtilClient.is_unset(request.job_id):
            body['JobId'] = request.job_id
        if not UtilClient.is_unset(request.max_running_time_minutes):
            body['MaxRunningTimeMinutes'] = request.max_running_time_minutes
        if not UtilClient.is_unset(request.options):
            body['Options'] = request.options
        if not UtilClient.is_unset(request.source_id):
            body['SourceId'] = request.source_id
        if not UtilClient.is_unset(request.source_type):
            body['SourceType'] = request.source_type
        if not UtilClient.is_unset(request.summary_path):
            body['SummaryPath'] = request.summary_path
        if not UtilClient.is_unset(request.summary_relative_path):
            body['SummaryRelativePath'] = request.summary_relative_path
        if not UtilClient.is_unset(request.uri):
            body['Uri'] = request.uri
        if not UtilClient.is_unset(request.workspace_id):
            body['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateTensorboard',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/tensorboards',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.CreateTensorboardResponse(),
            self.call_api(params, req, runtime)
        )

    def delete_code_source(self, code_source_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_code_source_with_options(code_source_id, headers, runtime)

    def delete_code_source_with_options(self, code_source_id, headers, runtime):
        code_source_id = OpenApiUtilClient.get_encode_param(code_source_id)
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteCodeSource',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/codesources/%s' % TeaConverter.to_unicode(code_source_id),
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.DeleteCodeSourceResponse(),
            self.call_api(params, req, runtime)
        )

    def delete_data_source(self, data_source_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_data_source_with_options(data_source_id, headers, runtime)

    def delete_data_source_with_options(self, data_source_id, headers, runtime):
        data_source_id = OpenApiUtilClient.get_encode_param(data_source_id)
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteDataSource',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/datasources/%s' % TeaConverter.to_unicode(data_source_id),
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.DeleteDataSourceResponse(),
            self.call_api(params, req, runtime)
        )

    def delete_debugger_config(self, debugger_config_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_debugger_config_with_options(debugger_config_id, headers, runtime)

    def delete_debugger_config_with_options(self, debugger_config_id, headers, runtime):
        debugger_config_id = OpenApiUtilClient.get_encode_param(debugger_config_id)
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteDebuggerConfig',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/debuggerconfigs/%s' % TeaConverter.to_unicode(debugger_config_id),
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.DeleteDebuggerConfigResponse(),
            self.call_api(params, req, runtime)
        )

    def delete_job(self, job_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_job_with_options(job_id, headers, runtime)

    def delete_job_with_options(self, job_id, headers, runtime):
        job_id = OpenApiUtilClient.get_encode_param(job_id)
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteJob',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/jobs/%s' % TeaConverter.to_unicode(job_id),
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.DeleteJobResponse(),
            self.call_api(params, req, runtime)
        )

    def delete_job_by_batch(self, job_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_job_by_batch_with_options(job_id, headers, runtime)

    def delete_job_by_batch_with_options(self, job_id, headers, runtime):
        job_id = OpenApiUtilClient.get_encode_param(job_id)
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteJobByBatch',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/jobs/%s/batch' % TeaConverter.to_unicode(job_id),
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.DeleteJobByBatchResponse(),
            self.call_api(params, req, runtime)
        )

    def delete_jobs(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_jobs_with_options(request, headers, runtime)

    def delete_jobs_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.job_ids):
            body['JobIds'] = request.job_ids
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteJobs',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/batch/jobs/delete',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.DeleteJobsResponse(),
            self.call_api(params, req, runtime)
        )

    def delete_quota(self, quota_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_quota_with_options(quota_id, headers, runtime)

    def delete_quota_with_options(self, quota_id, headers, runtime):
        quota_id = OpenApiUtilClient.get_encode_param(quota_id)
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteQuota',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/quotas/%s' % TeaConverter.to_unicode(quota_id),
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.DeleteQuotaResponse(),
            self.call_api(params, req, runtime)
        )

    def delete_tensorboard(self, tensorboard_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_tensorboard_with_options(tensorboard_id, request, headers, runtime)

    def delete_tensorboard_with_options(self, tensorboard_id, request, headers, runtime):
        UtilClient.validate_model(request)
        tensorboard_id = OpenApiUtilClient.get_encode_param(tensorboard_id)
        query = {}
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteTensorboard',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/tensorboards/%s' % TeaConverter.to_unicode(tensorboard_id),
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.DeleteTensorboardResponse(),
            self.call_api(params, req, runtime)
        )

    def get_authorization(self):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_authorization_with_options(headers, runtime)

    def get_authorization_with_options(self, headers, runtime):
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetAuthorization',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/authorization',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.GetAuthorizationResponse(),
            self.call_api(params, req, runtime)
        )

    def get_code_source(self, code_source_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_code_source_with_options(code_source_id, headers, runtime)

    def get_code_source_with_options(self, code_source_id, headers, runtime):
        code_source_id = OpenApiUtilClient.get_encode_param(code_source_id)
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetCodeSource',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/codesources/%s' % TeaConverter.to_unicode(code_source_id),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.GetCodeSourceResponse(),
            self.call_api(params, req, runtime)
        )

    def get_data_source(self, data_source_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_data_source_with_options(data_source_id, headers, runtime)

    def get_data_source_with_options(self, data_source_id, headers, runtime):
        data_source_id = OpenApiUtilClient.get_encode_param(data_source_id)
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetDataSource',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/datasources/%s' % TeaConverter.to_unicode(data_source_id),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.GetDataSourceResponse(),
            self.call_api(params, req, runtime)
        )

    def get_debugger_config(self, debugger_config_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_debugger_config_with_options(debugger_config_id, headers, runtime)

    def get_debugger_config_with_options(self, debugger_config_id, headers, runtime):
        debugger_config_id = OpenApiUtilClient.get_encode_param(debugger_config_id)
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetDebuggerConfig',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/debuggerconfigs/%s' % TeaConverter.to_unicode(debugger_config_id),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.GetDebuggerConfigResponse(),
            self.call_api(params, req, runtime)
        )

    def get_debugger_job(self, job_id, debugger_job_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_debugger_job_with_options(job_id, debugger_job_id, headers, runtime)

    def get_debugger_job_with_options(self, job_id, debugger_job_id, headers, runtime):
        job_id = OpenApiUtilClient.get_encode_param(job_id)
        debugger_job_id = OpenApiUtilClient.get_encode_param(debugger_job_id)
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetDebuggerJob',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/jobs/%s/debuggerjobs/%s' % (TeaConverter.to_unicode(job_id), TeaConverter.to_unicode(debugger_job_id)),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.GetDebuggerJobResponse(),
            self.call_api(params, req, runtime)
        )

    def get_debugger_result(self, job_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_debugger_result_with_options(job_id, headers, runtime)

    def get_debugger_result_with_options(self, job_id, headers, runtime):
        job_id = OpenApiUtilClient.get_encode_param(job_id)
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetDebuggerResult',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/jobs/%s/debuggerresult' % TeaConverter.to_unicode(job_id),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.GetDebuggerResultResponse(),
            self.call_api(params, req, runtime)
        )

    def get_job(self, job_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_job_with_options(job_id, headers, runtime)

    def get_job_with_options(self, job_id, headers, runtime):
        job_id = OpenApiUtilClient.get_encode_param(job_id)
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetJob',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/jobs/%s' % TeaConverter.to_unicode(job_id),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.GetJobResponse(),
            self.call_api(params, req, runtime)
        )

    def get_job_debugger_config(self, job_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_job_debugger_config_with_options(job_id, headers, runtime)

    def get_job_debugger_config_with_options(self, job_id, headers, runtime):
        job_id = OpenApiUtilClient.get_encode_param(job_id)
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetJobDebuggerConfig',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/jobs/%s/debuggerconfig' % TeaConverter.to_unicode(job_id),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.GetJobDebuggerConfigResponse(),
            self.call_api(params, req, runtime)
        )

    def get_job_events(self, job_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_job_events_with_options(job_id, request, headers, runtime)

    def get_job_events_with_options(self, job_id, request, headers, runtime):
        UtilClient.validate_model(request)
        job_id = OpenApiUtilClient.get_encode_param(job_id)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.max_events_num):
            query['MaxEventsNum'] = request.max_events_num
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetJobEvents',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/jobs/%s/events' % TeaConverter.to_unicode(job_id),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.GetJobEventsResponse(),
            self.call_api(params, req, runtime)
        )

    def get_job_metrics(self, job_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_job_metrics_with_options(job_id, request, headers, runtime)

    def get_job_metrics_with_options(self, job_id, request, headers, runtime):
        UtilClient.validate_model(request)
        job_id = OpenApiUtilClient.get_encode_param(job_id)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
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
            action='GetJobMetrics',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/jobs/%s/metrics' % TeaConverter.to_unicode(job_id),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.GetJobMetricsResponse(),
            self.call_api(params, req, runtime)
        )

    def get_job_workflow(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_job_workflow_with_options(request, headers, runtime)

    def get_job_workflow_with_options(self, tmp_req, headers, runtime):
        UtilClient.validate_model(tmp_req)
        request = pai_dlc_20201203_models.GetJobWorkflowShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.properties):
            request.properties_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.properties, 'Properties', 'json')
        query = {}
        if not UtilClient.is_unset(request.algo_name):
            query['AlgoName'] = request.algo_name
        if not UtilClient.is_unset(request.project_name):
            query['ProjectName'] = request.project_name
        if not UtilClient.is_unset(request.properties_shrink):
            query['Properties'] = request.properties_shrink
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetJobWorkflow',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/jobdispatch/workflow',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.GetJobWorkflowResponse(),
            self.call_api(params, req, runtime)
        )

    def get_jobs_statistics(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_jobs_statistics_with_options(request, headers, runtime)

    def get_jobs_statistics_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetJobsStatistics',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/statistics/jobs',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.GetJobsStatisticsResponse(),
            self.call_api(params, req, runtime)
        )

    def get_pod_events(self, job_id, pod_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_pod_events_with_options(job_id, pod_id, request, headers, runtime)

    def get_pod_events_with_options(self, job_id, pod_id, request, headers, runtime):
        UtilClient.validate_model(request)
        job_id = OpenApiUtilClient.get_encode_param(job_id)
        pod_id = OpenApiUtilClient.get_encode_param(pod_id)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.max_events_num):
            query['MaxEventsNum'] = request.max_events_num
        if not UtilClient.is_unset(request.pod_uid):
            query['PodUid'] = request.pod_uid
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetPodEvents',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/jobs/%s/pods/%s/events' % (TeaConverter.to_unicode(job_id), TeaConverter.to_unicode(pod_id)),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.GetPodEventsResponse(),
            self.call_api(params, req, runtime)
        )

    def get_pod_logs(self, job_id, pod_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_pod_logs_with_options(job_id, pod_id, request, headers, runtime)

    def get_pod_logs_with_options(self, job_id, pod_id, request, headers, runtime):
        UtilClient.validate_model(request)
        job_id = OpenApiUtilClient.get_encode_param(job_id)
        pod_id = OpenApiUtilClient.get_encode_param(pod_id)
        query = {}
        if not UtilClient.is_unset(request.download_to_file):
            query['DownloadToFile'] = request.download_to_file
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.max_lines):
            query['MaxLines'] = request.max_lines
        if not UtilClient.is_unset(request.pod_uid):
            query['PodUid'] = request.pod_uid
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetPodLogs',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/jobs/%s/pods/%s/logs' % (TeaConverter.to_unicode(job_id), TeaConverter.to_unicode(pod_id)),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.GetPodLogsResponse(),
            self.call_api(params, req, runtime)
        )

    def get_quota(self, quota_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_quota_with_options(quota_id, headers, runtime)

    def get_quota_with_options(self, quota_id, headers, runtime):
        quota_id = OpenApiUtilClient.get_encode_param(quota_id)
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetQuota',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/quotas/%s' % TeaConverter.to_unicode(quota_id),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.GetQuotaResponse(),
            self.call_api(params, req, runtime)
        )

    def get_security_group(self, security_group_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_security_group_with_options(security_group_id, headers, runtime)

    def get_security_group_with_options(self, security_group_id, headers, runtime):
        security_group_id = OpenApiUtilClient.get_encode_param(security_group_id)
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetSecurityGroup',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/securitygroups/%s' % TeaConverter.to_unicode(security_group_id),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.GetSecurityGroupResponse(),
            self.call_api(params, req, runtime)
        )

    def get_switch(self, switch_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_switch_with_options(switch_id, headers, runtime)

    def get_switch_with_options(self, switch_id, headers, runtime):
        switch_id = OpenApiUtilClient.get_encode_param(switch_id)
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetSwitch',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/switches/%s' % TeaConverter.to_unicode(switch_id),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.GetSwitchResponse(),
            self.call_api(params, req, runtime)
        )

    def get_tensorboard(self, tensorboard_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_tensorboard_with_options(tensorboard_id, request, headers, runtime)

    def get_tensorboard_with_options(self, tensorboard_id, request, headers, runtime):
        UtilClient.validate_model(request)
        tensorboard_id = OpenApiUtilClient.get_encode_param(tensorboard_id)
        query = {}
        if not UtilClient.is_unset(request.jod_id):
            query['JodId'] = request.jod_id
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetTensorboard',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/tensorboards/%s' % TeaConverter.to_unicode(tensorboard_id),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.GetTensorboardResponse(),
            self.call_api(params, req, runtime)
        )

    def get_token(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_token_with_options(request, headers, runtime)

    def get_token_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.expire_time):
            query['ExpireTime'] = request.expire_time
        if not UtilClient.is_unset(request.target_id):
            query['TargetId'] = request.target_id
        if not UtilClient.is_unset(request.target_type):
            query['TargetType'] = request.target_type
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetToken',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/tokens',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.GetTokenResponse(),
            self.call_api(params, req, runtime)
        )

    def get_user_authorization(self, user_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_user_authorization_with_options(user_id, headers, runtime)

    def get_user_authorization_with_options(self, user_id, headers, runtime):
        user_id = OpenApiUtilClient.get_encode_param(user_id)
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetUserAuthorization',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/users/%s/authorization' % TeaConverter.to_unicode(user_id),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.GetUserAuthorizationResponse(),
            self.call_api(params, req, runtime)
        )

    def get_vpc(self, vpc_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_vpc_with_options(vpc_id, headers, runtime)

    def get_vpc_with_options(self, vpc_id, headers, runtime):
        vpc_id = OpenApiUtilClient.get_encode_param(vpc_id)
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetVpc',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/vpcs/%s' % TeaConverter.to_unicode(vpc_id),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.GetVpcResponse(),
            self.call_api(params, req, runtime)
        )

    def get_workspace(self, workspace_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_workspace_with_options(workspace_id, headers, runtime)

    def get_workspace_with_options(self, workspace_id, headers, runtime):
        workspace_id = OpenApiUtilClient.get_encode_param(workspace_id)
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetWorkspace',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/workspaces/%s' % TeaConverter.to_unicode(workspace_id),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.GetWorkspaceResponse(),
            self.call_api(params, req, runtime)
        )

    def job_dispatch_query(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.job_dispatch_query_with_options(request, headers, runtime)

    def job_dispatch_query_with_options(self, tmp_req, headers, runtime):
        UtilClient.validate_model(tmp_req)
        request = pai_dlc_20201203_models.JobDispatchQueryShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.properties):
            request.properties_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.properties, 'Properties', 'json')
        if not UtilClient.is_unset(tmp_req.settings):
            request.settings_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.settings, 'Settings', 'json')
        query = {}
        if not UtilClient.is_unset(request.algo_name):
            query['AlgoName'] = request.algo_name
        if not UtilClient.is_unset(request.project_name):
            query['ProjectName'] = request.project_name
        if not UtilClient.is_unset(request.properties_shrink):
            query['Properties'] = request.properties_shrink
        if not UtilClient.is_unset(request.settings_shrink):
            query['Settings'] = request.settings_shrink
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='JobDispatchQuery',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/jobdispatch',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.JobDispatchQueryResponse(),
            self.call_api(params, req, runtime)
        )

    def job_dispatch_submit(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.job_dispatch_submit_with_options(request, headers, runtime)

    def job_dispatch_submit_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.algo_name):
            body['AlgoName'] = request.algo_name
        if not UtilClient.is_unset(request.project_name):
            body['ProjectName'] = request.project_name
        if not UtilClient.is_unset(request.properties):
            body['Properties'] = request.properties
        if not UtilClient.is_unset(request.settings):
            body['Settings'] = request.settings
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='JobDispatchSubmit',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/jobdispatch',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.JobDispatchSubmitResponse(),
            self.call_api(params, req, runtime)
        )

    def list_code_sources(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_code_sources_with_options(request, headers, runtime)

    def list_code_sources_with_options(self, request, headers, runtime):
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
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListCodeSources',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/codesources',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.ListCodeSourcesResponse(),
            self.call_api(params, req, runtime)
        )

    def list_data_sources(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_data_sources_with_options(request, headers, runtime)

    def list_data_sources_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.data_source_type):
            query['DataSourceType'] = request.data_source_type
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
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListDataSources',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/datasources',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.ListDataSourcesResponse(),
            self.call_api(params, req, runtime)
        )

    def list_debugger_config_templates(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_debugger_config_templates_with_options(request, headers, runtime)

    def list_debugger_config_templates_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.display_name):
            query['DisplayName'] = request.display_name
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListDebuggerConfigTemplates',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/debuggerconfigtemplates',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.ListDebuggerConfigTemplatesResponse(),
            self.call_api(params, req, runtime)
        )

    def list_debugger_configs(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_debugger_configs_with_options(request, headers, runtime)

    def list_debugger_configs_with_options(self, request, headers, runtime):
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
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListDebuggerConfigs',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/debuggerconfigs',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.ListDebuggerConfigsResponse(),
            self.call_api(params, req, runtime)
        )

    def list_debugger_job_pods(self, job_id, debugger_job_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_debugger_job_pods_with_options(job_id, debugger_job_id, request, headers, runtime)

    def list_debugger_job_pods_with_options(self, job_id, debugger_job_id, request, headers, runtime):
        UtilClient.validate_model(request)
        job_id = OpenApiUtilClient.get_encode_param(job_id)
        debugger_job_id = OpenApiUtilClient.get_encode_param(debugger_job_id)
        query = {}
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
            action='ListDebuggerJobPods',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/jobs/%s/debuggerjobs/%s/pods' % (TeaConverter.to_unicode(job_id), TeaConverter.to_unicode(debugger_job_id)),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.ListDebuggerJobPodsResponse(),
            self.call_api(params, req, runtime)
        )

    def list_debugger_jobs(self, job_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_debugger_jobs_with_options(job_id, request, headers, runtime)

    def list_debugger_jobs_with_options(self, job_id, request, headers, runtime):
        UtilClient.validate_model(request)
        job_id = OpenApiUtilClient.get_encode_param(job_id)
        query = {}
        if not UtilClient.is_unset(request.debugger_job_status):
            query['DebuggerJobStatus'] = request.debugger_job_status
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
            action='ListDebuggerJobs',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/jobs/%s/debuggerjobs' % TeaConverter.to_unicode(job_id),
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.ListDebuggerJobsResponse(),
            self.call_api(params, req, runtime)
        )

    def list_ecs_specs(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_ecs_specs_with_options(request, headers, runtime)

    def list_ecs_specs_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.accelerator_type):
            query['AcceleratorType'] = request.accelerator_type
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
            action='ListEcsSpecs',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/ecsspecs',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.ListEcsSpecsResponse(),
            self.call_api(params, req, runtime)
        )

    def list_images(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_images_with_options(request, headers, runtime)

    def list_images_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.accelerator_type):
            query['AcceleratorType'] = request.accelerator_type
        if not UtilClient.is_unset(request.framework):
            query['Framework'] = request.framework
        if not UtilClient.is_unset(request.image_provider_type):
            query['ImageProviderType'] = request.image_provider_type
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListImages',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/images',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.ListImagesResponse(),
            self.call_api(params, req, runtime)
        )

    def list_jobs(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_jobs_with_options(request, headers, runtime)

    def list_jobs_with_options(self, tmp_req, headers, runtime):
        UtilClient.validate_model(tmp_req)
        request = pai_dlc_20201203_models.ListJobsShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.tags):
            request.tags_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.tags, 'Tags', 'json')
        query = {}
        if not UtilClient.is_unset(request.business_user_id):
            query['BusinessUserId'] = request.business_user_id
        if not UtilClient.is_unset(request.caller):
            query['Caller'] = request.caller
        if not UtilClient.is_unset(request.display_name):
            query['DisplayName'] = request.display_name
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.job_type):
            query['JobType'] = request.job_type
        if not UtilClient.is_unset(request.order):
            query['Order'] = request.order
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.pipeline_id):
            query['PipelineId'] = request.pipeline_id
        if not UtilClient.is_unset(request.resource_id):
            query['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.show_own):
            query['ShowOwn'] = request.show_own
        if not UtilClient.is_unset(request.sort_by):
            query['SortBy'] = request.sort_by
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        if not UtilClient.is_unset(request.tags_shrink):
            query['Tags'] = request.tags_shrink
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListJobs',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/jobs',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.ListJobsResponse(),
            self.call_api(params, req, runtime)
        )

    def list_quotas(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_quotas_with_options(request, headers, runtime)

    def list_quotas_with_options(self, request, headers, runtime):
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
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListQuotas',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/quotas',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.ListQuotasResponse(),
            self.call_api(params, req, runtime)
        )

    def list_security_groups(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_security_groups_with_options(request, headers, runtime)

    def list_security_groups_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.vpc_id):
            query['VpcId'] = request.vpc_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListSecurityGroups',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/securitygroups',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.ListSecurityGroupsResponse(),
            self.call_api(params, req, runtime)
        )

    def list_switches(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_switches_with_options(request, headers, runtime)

    def list_switches_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.vpc_id):
            query['VpcId'] = request.vpc_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListSwitches',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/switches',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.ListSwitchesResponse(),
            self.call_api(params, req, runtime)
        )

    def list_tensorboards(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_tensorboards_with_options(request, headers, runtime)

    def list_tensorboards_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.display_name):
            query['DisplayName'] = request.display_name
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.job_id):
            query['JobId'] = request.job_id
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
        if not UtilClient.is_unset(request.tensorboard_id):
            query['TensorboardId'] = request.tensorboard_id
        if not UtilClient.is_unset(request.verbose):
            query['Verbose'] = request.verbose
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListTensorboards',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/tensorboards',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.ListTensorboardsResponse(),
            self.call_api(params, req, runtime)
        )

    def list_vpcs(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_vpcs_with_options(request, headers, runtime)

    def list_vpcs_with_options(self, request, headers, runtime):
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
            action='ListVpcs',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/vpcs',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.ListVpcsResponse(),
            self.call_api(params, req, runtime)
        )

    def list_workspaces(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_workspaces_with_options(request, headers, runtime)

    def list_workspaces_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.need_detail):
            query['NeedDetail'] = request.need_detail
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
            action='ListWorkspaces',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/workspaces',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.ListWorkspacesResponse(),
            self.call_api(params, req, runtime)
        )

    def start_tensorboard(self, tensorboard_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.start_tensorboard_with_options(tensorboard_id, request, headers, runtime)

    def start_tensorboard_with_options(self, tensorboard_id, request, headers, runtime):
        UtilClient.validate_model(request)
        tensorboard_id = OpenApiUtilClient.get_encode_param(tensorboard_id)
        query = {}
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='StartTensorboard',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/tensorboards/%s/start' % TeaConverter.to_unicode(tensorboard_id),
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.StartTensorboardResponse(),
            self.call_api(params, req, runtime)
        )

    def stop_debugger_jobs(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.stop_debugger_jobs_with_options(request, headers, runtime)

    def stop_debugger_jobs_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.job_id):
            body['JobId'] = request.job_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='StopDebuggerJobs',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/batch/jobs/debuggerjobs/stop',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.StopDebuggerJobsResponse(),
            self.call_api(params, req, runtime)
        )

    def stop_job(self, job_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.stop_job_with_options(job_id, headers, runtime)

    def stop_job_with_options(self, job_id, headers, runtime):
        job_id = OpenApiUtilClient.get_encode_param(job_id)
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='StopJob',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/jobs/%s/stop' % TeaConverter.to_unicode(job_id),
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.StopJobResponse(),
            self.call_api(params, req, runtime)
        )

    def stop_job_by_batch(self, job_id):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.stop_job_by_batch_with_options(job_id, headers, runtime)

    def stop_job_by_batch_with_options(self, job_id, headers, runtime):
        job_id = OpenApiUtilClient.get_encode_param(job_id)
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='StopJobByBatch',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/jobs/stop/batch',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.StopJobByBatchResponse(),
            self.call_api(params, req, runtime)
        )

    def stop_jobs(self, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.stop_jobs_with_options(request, headers, runtime)

    def stop_jobs_with_options(self, request, headers, runtime):
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.job_ids):
            body['JobIds'] = request.job_ids
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='StopJobs',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/batch/jobs/stop',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.StopJobsResponse(),
            self.call_api(params, req, runtime)
        )

    def stop_tensorboard(self, tensorboard_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.stop_tensorboard_with_options(tensorboard_id, request, headers, runtime)

    def stop_tensorboard_with_options(self, tensorboard_id, request, headers, runtime):
        UtilClient.validate_model(request)
        tensorboard_id = OpenApiUtilClient.get_encode_param(tensorboard_id)
        query = {}
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='StopTensorboard',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/tensorboards/%s/stop' % TeaConverter.to_unicode(tensorboard_id),
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.StopTensorboardResponse(),
            self.call_api(params, req, runtime)
        )

    def update_debugger_config(self, debugger_config_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_debugger_config_with_options(debugger_config_id, request, headers, runtime)

    def update_debugger_config_with_options(self, debugger_config_id, request, headers, runtime):
        UtilClient.validate_model(request)
        debugger_config_id = OpenApiUtilClient.get_encode_param(debugger_config_id)
        body = {}
        if not UtilClient.is_unset(request.content):
            body['Content'] = request.content
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.display_name):
            body['DisplayName'] = request.display_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateDebuggerConfig',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/debuggerconfigs/%s' % TeaConverter.to_unicode(debugger_config_id),
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.UpdateDebuggerConfigResponse(),
            self.call_api(params, req, runtime)
        )

    def update_job(self, job_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_job_with_options(job_id, request, headers, runtime)

    def update_job_with_options(self, job_id, request, headers, runtime):
        UtilClient.validate_model(request)
        job_id = OpenApiUtilClient.get_encode_param(job_id)
        body = {}
        if not UtilClient.is_unset(request.priority):
            body['Priority'] = request.priority
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateJob',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/jobs/%s' % TeaConverter.to_unicode(job_id),
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.UpdateJobResponse(),
            self.call_api(params, req, runtime)
        )

    def update_quota(self, quota_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_quota_with_options(quota_id, request, headers, runtime)

    def update_quota_with_options(self, quota_id, request, headers, runtime):
        UtilClient.validate_model(request)
        quota_id = OpenApiUtilClient.get_encode_param(quota_id)
        body = {}
        if not UtilClient.is_unset(request.quota_detail):
            body['QuotaDetail'] = request.quota_detail
        if not UtilClient.is_unset(request.quota_name):
            body['QuotaName'] = request.quota_name
        if not UtilClient.is_unset(request.quota_type):
            body['QuotaType'] = request.quota_type
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateQuota',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/quotas/%s' % TeaConverter.to_unicode(quota_id),
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.UpdateQuotaResponse(),
            self.call_api(params, req, runtime)
        )

    def update_tensorboard(self, tensorboard_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_tensorboard_with_options(tensorboard_id, request, headers, runtime)

    def update_tensorboard_with_options(self, tensorboard_id, request, headers, runtime):
        UtilClient.validate_model(request)
        tensorboard_id = OpenApiUtilClient.get_encode_param(tensorboard_id)
        query = {}
        if not UtilClient.is_unset(request.max_running_time_minutes):
            query['MaxRunningTimeMinutes'] = request.max_running_time_minutes
        if not UtilClient.is_unset(request.workspace_id):
            query['WorkspaceId'] = request.workspace_id
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateTensorboard',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/tensorboards/%s' % TeaConverter.to_unicode(tensorboard_id),
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.UpdateTensorboardResponse(),
            self.call_api(params, req, runtime)
        )

    def update_workspace_quota(self, workspace_id, quota_id, request):
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_workspace_quota_with_options(workspace_id, quota_id, request, headers, runtime)

    def update_workspace_quota_with_options(self, workspace_id, quota_id, request, headers, runtime):
        UtilClient.validate_model(request)
        workspace_id = OpenApiUtilClient.get_encode_param(workspace_id)
        quota_id = OpenApiUtilClient.get_encode_param(quota_id)
        body = {}
        if not UtilClient.is_unset(request.enable_tide_resource):
            body['EnableTideResource'] = request.enable_tide_resource
        if not UtilClient.is_unset(request.resource_level):
            body['ResourceLevel'] = request.resource_level
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateWorkspaceQuota',
            version='2020-12-03',
            protocol='HTTPS',
            pathname='/api/v1/workspaces/%s/quotas/%s' % (TeaConverter.to_unicode(workspace_id), TeaConverter.to_unicode(quota_id)),
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            pai_dlc_20201203_models.UpdateWorkspaceQuotaResponse(),
            self.call_api(params, req, runtime)
        )
