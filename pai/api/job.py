#  Copyright 2023 Alibaba, Inc. or its affiliates.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from datetime import datetime
from typing import Any, Dict, List

from ..common.logging import get_logger
from ..libs.alibabacloud_pai_dlc20201203.models import (
    GetJobEventsRequest,
    GetJobEventsResponseBody,
    GetPodLogsRequest,
    GetPodLogsResponseBody,
    ListEcsSpecsRequest,
    ListJobsRequest,
    ListJobsResponseBody,
)
from .base import PaginatedResult, ServiceName, WorkspaceScopedResourceAPI

logger = get_logger(__name__)


class JobAPI(WorkspaceScopedResourceAPI):
    """Class which provide API to operate job resource."""

    BACKEND_SERVICE_NAME = ServiceName.PAI_DLC

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

    @classmethod
    def _generate_display_name(cls, job):
        return "{}-{}".format(
            type(job).__name__, datetime.now().isoformat(sep="-", timespec="seconds")
        )

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
        page_number=1,
        page_size=50,
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

        Returns:

        """

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
            id: ID of the Job.

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

    def list_logs(
        self,
        job_id,
        pod_id,
        end_time: datetime = None,
        start_time: datetime = None,
        max_lines: int = None,
        pod_uid: str = None,
    ) -> List[str]:
        """List logs of a specific job pod."""
        request = GetPodLogsRequest(
            end_time=end_time,
            max_lines=max_lines,
            pod_uid=pod_uid,
            start_time=start_time,
        )

        result: GetPodLogsResponseBody = self._do_request(
            method_=self._get_pod_logs_method,
            job_id=job_id,
            pod_id=pod_id,
            request=request,
        )

        return result.logs

    def list_ecs_specs(
        self,
        accelerator_type=None,
        order="asc",
        page_number=1,
        page_size=10,
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
