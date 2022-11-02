import logging
from datetime import datetime
from typing import Any, Dict

from pai.api.base import PaginatedResult, ScopeResourceAPI
from pai.common.consts import (
    DEFAULT_PAGE_NUMBER,
    DEFAULT_PAGE_SIZE,
    PagingOrder,
    PAIServiceName,
)
from pai.libs.alibabacloud_pai_dlc20201203.client import Client
from pai.libs.alibabacloud_pai_dlc20201203.models import (
    CreateJobRequest,
    CreateJobResponseBody,
    GetJobEventsRequest,
    GetJobEventsResponseBody,
    GetPodLogsRequest,
    ListEcsSpecsRequest,
    ListJobsRequest,
    ListJobsResponseBody,
)

logger = logging.getLogger(__name__)


class JobAPI(ScopeResourceAPI):
    """Class which provide API to operate job resource."""

    BACKEND_SERVICE_NAME = PAIServiceName.PAI_DLC

    _list_method = "list_jobs_with_options"
    _get_method = "get_job_with_options"
    _delete_method = "delete_job_with_options"
    _create_method = "create_job_with_options"
    _stop_method = "stop_job_with_options"
    _list_ecs_spec_method = "list_ecs_specs_with_options"
    _get_job_events_method = "get_job_events_with_options"
    _get_pod_logs_method = "get_pod_logs_with_options"

    _DEFAULT_PAGE_SIZE = 50
    _DEFAULT_PAGE_NUMBER = 1

    def __init__(self, workspace_id: str, acs_client: Client) -> None:
        super(JobAPI, self).__init__(workspace_id=workspace_id, acs_client=acs_client)

    @classmethod
    def _generate_display_name(cls, job):
        return "{}-{}".format(
            type(job).__name__, datetime.now().isoformat(sep="-", timespec="seconds")
        )

    def create(
        self,
        display_name,
        job_specs,
        job_type="TFJob",
        code_source_config=None,
        data_source_configs=None,
        environment_variables=None,
        max_running_time_minutes=None,
        # options=None,
        resource_id=None,
        priority=None,
        thirdparty_lib_dir=None,
        thirdparty_libs=None,
        user_command=None,
        user_vpc=None,
        **kwargs,
    ) -> str:
        """Create a DlcJob resource.

        Returns:
            str: Job id of the created job.

        """
        request = self._make_create_job_request(
            display_name=display_name,
            job_specs=job_specs,
            job_type=job_type,
            code_source_config=code_source_config,
            data_source_configs=data_source_configs,
            environment_variables=environment_variables,
            max_running_time_minutes=max_running_time_minutes,
            resource_id=resource_id,
            priority=priority,
            thirdparty_lib_dir=thirdparty_lib_dir,
            thirdparty_libs=thirdparty_libs,
            user_command=user_command,
            user_vpc=user_vpc,
        )
        resp: CreateJobResponseBody = self._do_request(
            method_=self._create_method, request=request
        )

        return resp.job_id

    def _make_create_job_request(
        self,
        display_name,
        job_specs,
        job_type="TFJob",
        code_source_config=None,
        data_source_configs=None,
        environment_variables=None,
        max_running_time_minutes=None,
        resource_id=None,
        priority=None,
        thirdparty_lib_dir=None,
        thirdparty_libs=None,
        user_command=None,
        user_vpc=None,
    ) -> CreateJobRequest:
        from pai.entity.job import Job

        api_object = Job(
            display_name=display_name,
            job_specs=job_specs,
            job_type=job_type,
            code_source=code_source_config,
            data_sources=data_source_configs,
            envs=environment_variables,
            max_running_time_minutes=max_running_time_minutes,
            resource_id=resource_id,
            priority=priority,
            third_party_libs=thirdparty_libs,
            third_party_lib_dir=thirdparty_lib_dir,
            user_command=user_command,
            user_vpc=user_vpc,
        ).to_api_object()
        request = CreateJobRequest().from_map(api_object)
        request.workspace_id = self.workspace_id

        return request

    def list(
        self,
        display_name=None,
        start_time=None,
        end_time=None,
        resource_id=None,
        sort_by=None,
        order=None,
        status=None,
        tags=None,
        workspace_id=None,
        page_number=DEFAULT_PAGE_NUMBER,
        page_size=DEFAULT_PAGE_SIZE,
    ) -> PaginatedResult:
        """List the DlcJob resource which match given condition.

        Args:
            display_name: Display name of the job, support fuzz matching.
            start_time: Start time of the job
            end_time:
            resource_id:
            status:
            sort_by:
            order:
            tags:
            page_number:
            page_size:
            workspace_id:

        Returns:

        """

        if not workspace_id:
            workspace_id = self.workspace_id

        request = ListJobsRequest(
            display_name=display_name,
            start_time=start_time,
            end_time=end_time,
            page_size=page_size,
            page_number=page_number,
            resource_id=resource_id,
            sort_by=sort_by,
            order=order,
            status=status,
            tags=tags,
            workspace_id=workspace_id,
        )

        resp: ListJobsResponseBody = self._do_request(
            method_=self._list_method, tmp_req=request
        )
        return self.make_paginated_result(resp)

    def get_api_object_by_resource_id(self, resource_id):
        resp = self._do_request(method_=self._get_method, job_id=resource_id)
        return resp.to_map()

    def get(self, id: str) -> Dict[str, Any]:
        """Get the DlcJob resource by job_id.

        Args:
            id: Id of the Job.

        Returns:
            DlcJob:

        """
        return self.get_api_object_by_resource_id(resource_id=id)

    def delete(self, id: str) -> None:
        """Delete the job."""
        self._do_request(method_=self._delete_method, job_id=id)

    def stop(self, id: str) -> None:
        """Stop the job."""
        self._do_request(method_=self._stop_method, job_id=id)

    def list_events(self, id, start_time=None, end_time=None, max_events_num=2000):
        """Get Events of the DLC Job.

        Args:
            id (str):  Job Id
            start_time: Start time of job events range.
            end_time: End time of job events range.
            max_events_num: Max event number return from the response.

        Returns:
            List[str]: List of job events.

        """
        # TODO(LiangQuan): start_time/end_time support type datatime.
        request = GetJobEventsRequest(
            start_time=start_time, end_time=end_time, max_events_num=max_events_num
        )
        result: GetJobEventsResponseBody = self._do_request(
            method_=self._get_job_events_method, job_id=id, request=request
        )

        return result.events

    def list_pod_events(self, id, pod_id):
        pass

    def list_pod_logs(
        self,
        job_id,
        pod_id,
        end_time=None,
        max_lines=None,
        pod_uid=None,
        start_time=None,
    ):
        """List logs of a specific pod.

        Args:
            job_id:  Job Id
            pod_id:
            end_time:
            max_lines:
            pod_uid:
            start_time:

        Returns:

        """
        request = GetPodLogsRequest(
            end_time=end_time,
            max_lines=max_lines,
            pod_uid=pod_uid,
            start_time=start_time,
        )

        result = self._do_request(
            method_=self._get_pod_logs_method,
            job_id=job_id,
            pod_id=pod_id,
            request=request,
        )

        return result.logs

    def list_ecs_specs(
        self,
        accelerator_type=None,
        order=PagingOrder.ASCENT,
        page_number=DEFAULT_PAGE_NUMBER,
        page_size=DEFAULT_PAGE_SIZE,
        sort_by="Gpu",
    ) -> PaginatedResult:

        """List EcsSpecs that DLC service provided."""

        request = ListEcsSpecsRequest(
            accelerator_type=accelerator_type,
            order=order,
            page_number=page_number,
            page_size=page_size,
            sort_by=sort_by,
        )

        result = self._do_request(method_=self._list_ecs_spec_method, request=request)

        return self.make_paginated_result(result, item_key="EcsSpecs")
