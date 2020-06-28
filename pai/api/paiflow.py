import six
import yaml

from libs.aliyunsdkpaiflow.request.v20200328 import (
    CreatePipelineRequest, DeletePipelineRequest, GetPipelineRequest,
    ListPipelinesRequest, UpdatePipelineRequest, DescribePipelineRequest,
)
from libs.aliyunsdkpaiflow.request.v20200328 import (
    CreateRunRequest, GetRunRequest, TerminateRunRequest, SuspendRunRequest, ResumeRunRequest, RetryRunRequest,
    StartRunRequest
)
from pai.api import BaseClient


def ensure_str(val):
    if isinstance(val, six.string_types):
        return val
    elif isinstance(val, six.integer_types):
        return str(val)
    else:
        raise ValueError("ensure_str: not support type:%s" % type(val))


class PAIFlowClient(BaseClient):

    def __init__(self, acs_client=None):
        """Class to wrap APIs provided by PaiFlow pipeline service.

        Args:
            acs_client: Alibaba Cloud Service client.
        """
        super(PAIFlowClient, self).__init__(acs_client=acs_client)

    def _get_endpoint(self):
        return "pre-paiflow.data.aliyun.com"  # pre-release env

    def get_pipeline(self, pipeline_id):
        request = self._construct_request(GetPipelineRequest.GetPipelineRequest)
        request.set_PipelineId(pipeline_id)
        return self._call_service_with_exception(request)

    def list_pipeline(self, identifier=None, provider=None, query=None, source_type="private",
                      version="", page_num=1, page_size=50):
        assert source_type in ("private", "public")

        request = self._construct_request(ListPipelinesRequest.ListPipelinesRequest)
        request.set_PageNumber(page_num)
        request.set_PageSize(page_size)
        request.set_SourceType(source_type)

        if provider is not None:
            request.set_PipelineProvider(provider)
        if identifier is not None:
            request.set_PipelineIdentifier(identifier)
        if query is not None:
            request.set_FuzzyMatching(query)
        if version is not None:
            request.set_PipelineVersion(version)

        return self._call_service_with_exception(request)

    def create_pipeline(self, manifest):
        request = self._construct_request(CreatePipelineRequest.CreatePipelineRequest)
        request.set_manifest(manifest)
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

    def create_run(self, name, arguments, pipeline_id=None, manifest=None, no_confirm_required=False):
        if not pipeline_id and not manifest:
            raise ValueError("Create pipeline run need either pipeline_id or manifest.")
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
        request.set_Arguments(arguments)

        request.set_Name(name)
        request.set_NoConfirmRequired(no_confirm_required)
        return self._call_service_with_exception(request)

    def list_run(self, sorted_by, page_resize):
        pass

    def get_run(self, run_id):
        request = self._construct_request(GetRunRequest.GetRunRequest)
        request.set_RunId(ensure_str(run_id))
        return self._call_service_with_exception(request)

    def terminate_run(self, run_id):
        request = self._construct_request(TerminateRunRequest.TerminateRunRequest)
        request.set_RunId(ensure_str(run_id))
        return self._call_service_with_exception(request)

    def suspend_run(self, run_id):
        request = self._construct_request(SuspendRunRequest.SuspendRunRequest)
        request.set_RunId(ensure_str(run_id))
        return self._call_service_with_exception(request)

    def resume_run(self, run_id):
        request = self._construct_request(ResumeRunRequest.ResumeRunRequest)
        request.set_RunId(ensure_str(run_id))
        return self._call_service_with_exception(request)

    def retry_run(self, run_id):
        request = self._construct_request(RetryRunRequest.RetryRunRequest)
        request.set_RunId(ensure_str(run_id))
        return self._call_service_with_exception(request)

    def start_run(self, run_id):
        request = self._construct_request(StartRunRequest.StartRunRequest)
        request.set_RunId(ensure_str(run_id))
        return self._call_service_with_exception(request)
