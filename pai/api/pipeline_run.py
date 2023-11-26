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

from ..common.yaml_utils import dump as yaml_dump
from ..libs.alibabacloud_paiflow20210202.models import (
    CreateRunRequest,
    GetNodeRequest,
    GetNodeResponseBody,
    GetRunRequest,
    GetRunResponseBody,
    ListNodeLogsRequest,
    ListNodeLogsResponseBody,
    ListNodeOutputsRequest,
    ListNodeOutputsResponseBody,
    ListRunsRequest,
    ListRunsResponseBody,
    UpdateRunRequest,
)
from .base import ServiceName, WorkspaceScopedResourceAPI


class PipelineRunAPI(WorkspaceScopedResourceAPI):

    BACKEND_SERVICE_NAME = ServiceName.PAIFLOW

    _list_method = "list_runs_with_options"
    _get_method = "get_run_with_options"
    _create_method = "create_run_with_options"
    _start_method = "start_run_with_options"
    _terminate_method = "terminate_run_with_options"
    _update_method = "update_run_with_options"

    _get_node_method = "get_node_with_options"
    _list_node_logs_method = "list_node_logs_with_options"
    _list_node_outputs_method = "list_node_outputs_with_options"

    def list(
        self,
        name=None,
        run_id=None,
        pipeline_id=None,
        status=None,
        sort_by=None,
        order=None,
        page_number=None,
        page_size=None,
        experiment_id=None,
        source=None,
        **kwargs,
    ):
        request = ListRunsRequest(
            page_number=page_number,
            page_size=page_size,
            experiment_id=experiment_id,
            name=name,
            pipeline_id=pipeline_id,
            run_id=run_id,
            sort_by=sort_by,
            order=order,
            source=source,
            status=status,
            **kwargs,
        )
        resp: ListRunsResponseBody = self._do_request(
            method_=self._list_method, request=request
        )
        return self.make_paginated_result(resp.to_map())

    def get(self, run_id):
        request = GetRunRequest()
        resp: GetRunResponseBody = self._do_request(
            method_=self._get_method, run_id=run_id, request=request
        )
        return resp.to_map()

    def create(
        self,
        name,
        pipeline_id=None,
        manifest=None,
        arguments=None,
        env=None,
        no_confirm_required=False,
        source="SDK",
    ):
        run_args = {"arguments": arguments, "env": env}

        if not pipeline_id and not manifest:
            raise ValueError(
                "Create pipeline run require either pipeline_id or manifest."
            )
        if pipeline_id and manifest:
            raise ValueError(
                "Both pipeline_id and manifest are provide, create_run need only one."
            )
        if not name:
            raise ValueError("Pipeline run instance need a name.")

        run_args = yaml_dump(run_args)
        if manifest and isinstance(manifest, dict):
            manifest = yaml_dump(manifest)

        request = CreateRunRequest(
            pipeline_id=pipeline_id,
            name=name,
            pipeline_manifest=manifest,
            arguments=run_args,
            no_confirm_required=no_confirm_required,
            source=source,
        )
        resp = self._do_request(self._create_method, request=request)
        return resp.run_id

    def start(self, run_id):
        self._do_request(self._start_method, run_id=run_id)

    def terminate_run(self, run_id):
        self._do_request(self._terminate_method, run_id=run_id)

    def update(self, run_id, name):
        request = UpdateRunRequest(name=name)
        self._do_request(self._update_method, run_id=run_id, request=request)

    def get_node(self, run_id, node_id, depth=2):
        request = GetNodeRequest(depth=depth)
        resp: GetNodeResponseBody = self._do_request(
            method_=self._get_node_method,
            run_id=run_id,
            node_id=node_id,
            request=request,
        )
        return resp.to_map()

    def list_node_logs(
        self,
        run_id,
        node_id,
        from_time=None,
        to_time=None,
        keyword=None,
        reverse=False,
        page_offset=0,
        page_size=100,
    ):
        request = ListNodeLogsRequest(
            offset=page_offset,
            page_size=page_size,
            from_time_in_seconds=from_time,
            to_time_in_seconds=to_time,
            keyword=keyword,
            reverse=reverse,
        )
        resp: ListNodeLogsResponseBody = self._do_request(
            self._list_node_logs_method,
            run_id=run_id,
            node_id=node_id,
            request=request,
        )
        return self.make_paginated_result(resp.to_map())

    def list_node_outputs(
        self,
        run_id,
        node_id,
        depth=2,
        name=None,
        sort_by=None,
        order=None,
        type=None,
        page_number=1,
        page_size=50,
    ):

        request = ListNodeOutputsRequest(
            name=name,
            depth=depth,
            page_number=page_number,
            page_size=page_size,
            sort_by=sort_by,
            order=order,
            type=type,
        )

        resp: ListNodeOutputsResponseBody = self._do_request(
            self._list_node_outputs_method,
            run_id=run_id,
            node_id=node_id,
            request=request,
        )
        return self.make_paginated_result(resp.to_map())
