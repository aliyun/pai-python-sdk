from __future__ import absolute_import

from functools import wraps

import six
import yaml

from pai.api.base import paginate_service_call, BaseClient
from pai.core.exception import ServiceCallException
from pai.libs.aliyunsdkpaiflow.request.v20200328 import (
    CreatePipelineRequest, DeletePipelineRequest, GetPipelineRequest, ListPipelinesRequest,
    UpdatePipelineRequest, DescribePipelineRequest, UpdatePipelinePrivilegeRequest,
    TerminateRunRequest, SuspendRunRequest, RetryRunRequest, StartRunRequest, ListRunsRequest,
    ListNodeLogsRequest, ResumeRunRequest, GetRunRequest, GetNodeDetailRequest, CreateRunRequest,
    ListNodeOutputsRequest, GetMyProviderRequest
)
from pai.libs.aliyunsdkpaiflow.request.v20200328 import GetPipelinePrivilegeRequest
from pai.common.utils import ensure_str, ensure_unix_time


def require_workspace(f):
    @wraps(f)
    def _(self, *args, **kwargs):
        if not kwargs.get("workspace_id", None) and self.is_workspace_required:
            raise ValueError("Please provide WorkspaceId")

        return f(self, *args, **kwargs)

    return _


class PAIFlowClient(BaseClient):

    _ENV_SERVICE_ENDPOINT_KEY = 'ALIPAI_PAIFLOW_ENDPOINT'

    def __init__(self, acs_client, _is_inner=False):
        """Class to wrap APIs provided by PaiFlow pipeline service.

        Args:
            acs_client: Alibaba Cloud Service client.
        """
        super(PAIFlowClient, self).__init__(acs_client=acs_client)
        self._inner = _is_inner

    def _call_service_with_exception(self, request):
        resp = super(PAIFlowClient, self)._call_service_with_exception(request)
        if resp["Code"] is not None:
            message = "Service response error, request:%s code:%s, message:%s" % (
                request, resp["Code"], resp["Message"])
            raise ServiceCallException(message)
        return resp

    def _get_endpoint(self):
        if self._endpoint:
            return self._endpoint
        if self._inner:
            return "paiflowinner-inner.aliyuncs.com"
        else:
            return "paiflow.{region_id}.aliyuncs.com".format(region_id=self.region_id)

    def _get_product(self):
        if self._inner:
            return 'PAIFlowInner'
        else:
            return 'PAIFlow'

    @property
    def is_workspace_required(self):
        if not self._inner:
            return True
        return False

    def get_pipeline(self, pipeline_id=None, identifier=None, version=None, provider=None):
        request = self._construct_request(GetPipelineRequest.GetPipelineRequest)
        if pipeline_id is not None:
            request.set_PipelineId(pipeline_id)
        elif identifier and provider and version:
            request.set_PipelineIdentifier(identifier)
            request.set_PipelineVersion(version)
            request.set_PipelineProvider(provider)
        else:
            raise ValueError("Please provider pipeline_id or identifier-provider-version to fetch"
                             " the specific Pipeline")
        return self._call_service_with_exception(request)

    @paginate_service_call
    def list_pipeline(self, identifier=None, provider=None, fuzzy=None, workspace_id=None,
                      version=""):
        request = self._construct_request(ListPipelinesRequest.ListPipelinesRequest)

        if workspace_id is not None:
            request.set_WorkspaceId(workspace_id)
        if provider is not None:
            request.set_PipelineProvider(provider)
        if identifier is not None:
            request.set_PipelineIdentifier(identifier)
        if fuzzy is not None:
            request.set_FuzzyMatching(fuzzy)
        if version is not None:
            request.set_PipelineVersion(version)

        return request

    @require_workspace
    def create_pipeline(self, manifest, workspace_id=None):
        request = self._construct_request(CreatePipelineRequest.CreatePipelineRequest)
        request.set_Manifest(manifest)
        if workspace_id:
            request.set_WorkspaceId(workspace_id)

        response = self._call_service_with_exception(request)
        return response

    def delete_pipeline(self, pipeline_id):
        request = self._construct_request(DeletePipelineRequest.DeletePipelineRequest)
        request.set_PipelineId(pipeline_id)
        return self._call_service_with_exception(request)

    def update_pipeline(self, pipeline_id, manifest):
        request = self._construct_request(UpdatePipelineRequest.UpdatePipelineRequest)
        request.set_PipelineId(pipeline_id)
        request.set_Manifest(manifest)
        return self._call_service_with_exception(request)

    def describe_pipeline(self, pipeline_id):
        request = self._construct_request(DescribePipelineRequest.DescribePipelineRequest)
        request.set_PipelineId(ensure_str(pipeline_id))
        return self._call_service_with_exception(request)

    def update_pipeline_privilege(self, pipeline_id, user_ids):
        request = self._construct_request(
            UpdatePipelinePrivilegeRequest.UpdatePipelinePrivilegeRequest)
        request.set_PipelineId(pipeline_id)
        if not user_ids:
            raise ValueError("Argument 'users' should not be empty.")
        if isinstance(user_ids, six.string_types):
            user_ids = [user_ids]
        request.add_body_params("users", user_ids)
        return self._call_service_with_exception(request)

    def list_pipeline_privilege(self, pipeline_id):
        request = self._construct_request(GetPipelinePrivilegeRequest.GetPipelinePrivilegeRequest)
        request.set_PipelineId(pipeline_id)
        return self._call_service_with_exception(request)

    @require_workspace
    def create_run(self, name, arguments, pipeline_id=None, manifest=None,
                   no_confirm_required=False, workspace_id=None):
        if not pipeline_id and not manifest:
            raise ValueError("Create pipeline run require either pipeline_id or manifest.")
        if pipeline_id and manifest:
            raise ValueError("Both pipeline_id and manifest are provide, create_run need only one.")
        if not name:
            raise ValueError("Pipeline run instance need a name.")

        request = self._construct_request(CreateRunRequest.CreateRunRequest)

        if manifest:
            if isinstance(manifest, dict):
                manifest = yaml.dump(manifest)
            request.set_PipelineManifest(manifest)
        if pipeline_id:
            request.set_PipelineId(pipeline_id)

        if isinstance(arguments, dict):
            arguments = yaml.dump(arguments)

        if workspace_id is not None:
            request.set_WorkspaceId(workspace_id)

        request.set_Arguments(arguments)
        request.set_Name(name)
        request.set_NoConfirmRequired(no_confirm_required)
        return self._call_service_with_exception(request)

    @paginate_service_call
    def list_run(self, name=None, run_id=None, pipeline_id=None, status=None, sorted_by=None,
                 sorted_sequence=None, workspace_id=None):
        request = self._construct_request(ListRunsRequest.ListRunsRequest)
        if name is not None:
            request.set_Name(name)

        if run_id is not None:
            request.set_RunId(run_id)

        if pipeline_id is not None:
            request.set_PipelineId(run_id)

        if status is not None:
            request.set_Status(status)

        if sorted_by is not None:
            request.set_SortedBy(sorted_by)

        if sorted_sequence is not None:
            request.set_sortedSequence(sorted_sequence)

        if workspace_id is not None:
            request.set_WorkspaceId(workspace_id)

        return request

    def get_run(self, run_id):
        request = self._construct_request(GetRunRequest.GetRunRequest)
        request.set_RunId(run_id)
        return self._call_service_with_exception(request)

    def terminate_run(self, run_id):
        request = self._construct_request(TerminateRunRequest.TerminateRunRequest)
        request.set_RunId(run_id)
        return self._call_service_with_exception(request)

    def suspend_run(self, run_id):
        request = self._construct_request(SuspendRunRequest.SuspendRunRequest)
        request.set_RunId(run_id)
        return self._call_service_with_exception(request)

    def resume_run(self, run_id):
        request = self._construct_request(ResumeRunRequest.ResumeRunRequest)
        request.set_RunId(run_id)
        return self._call_service_with_exception(request)

    def retry_run(self, run_id):
        request = self._construct_request(RetryRunRequest.RetryRunRequest)
        request.set_RunId(run_id)
        return self._call_service_with_exception(request)

    def start_run(self, run_id):
        request = self._construct_request(StartRunRequest.StartRunRequest)
        request.set_RunId(run_id)
        return self._call_service_with_exception(request)

    def get_run_detail(self, run_id, node_id, depth=2):
        request = self._construct_request(GetNodeDetailRequest.GetNodeDetailRequest)
        request.set_RunId(run_id)
        request.set_NodeId(node_id)
        request.set_Depth(depth)
        return self._call_service_with_exception(request)

    def list_node_log(self, run_id, node_id, from_time=None, to_time=None, keyword=None,
                      reverse=False, page_offset=0, page_size=100):
        request = self._construct_request(ListNodeLogsRequest.ListNodeLogsRequest)
        request.set_RunId(run_id)
        request.set_NodeId(node_id)

        if from_time is not None:
            request.set_FromTimeInSeconds(ensure_unix_time(from_time))

        if to_time is not None:
            request.set_ToTimeInSeconds(ensure_unix_time(to_time))

        if keyword is not None:
            request.set_Keyword(keyword)
        if reverse is not None:
            request.set_Reverse(reverse)

        request.set_PageOffset(page_offset)
        request.set_PageSize(page_size)
        return self._call_service_with_exception(request)

    def list_run_outputs(self, run_id, node_id, depth=2, name=None, sorted_by=None,
                         sorted_sequence=None, typ=None, page_number=1, page_size=50):
        request = self._construct_request(ListNodeOutputsRequest.ListNodeOutputsRequest)

        request.set_Depth(depth)
        request.set_NodeId(node_id)
        request.set_RunId(run_id)
        request.set_PageNumber(page_number)
        request.set_PageSize(page_size)

        if name is not None:
            request.set_Name(name)
        if sorted_by is not None:
            request.set_SortedBy(sorted_by)
        if sorted_sequence is not None:
            request.set_sortedSequence(sorted_sequence)
        if typ is not None:
            request.set_Type(typ)
        return self._call_service_with_exception(request)

    def get_my_provider(self):
        request = self._construct_request(GetMyProviderRequest.GetMyProviderRequest)
        return self._call_service_with_exception(request)
