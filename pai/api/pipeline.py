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

from typing import Any, Dict

from ..common.logging import get_logger
from ..libs.alibabacloud_paiflow20210202.models import (
    CreatePipelineRequest,
    CreatePipelineResponseBody,
    GetPipelineResponseBody,
    GetPipelineSchemaResponseBody,
    ListPipelinesRequest,
    ListPipelinesResponseBody,
    UpdatePipelineRequest,
)
from .base import PaginatedResult, ServiceName, WorkspaceScopedResourceAPI

logger = get_logger(__name__)


class PipelineAPI(WorkspaceScopedResourceAPI):

    BACKEND_SERVICE_NAME = ServiceName.PAIFLOW

    _get_method = "get_pipeline_with_options"
    _get_schema_method = "get_pipeline_schema_with_options"
    _list_method = "list_pipelines_with_options"
    _create_method = "create_pipeline_with_options"
    _delete_method = "delete_pipeline_with_options"
    _update_method = "update_pipeline_with_options"
    _get_caller_provider_method = "get_caller_provider_with_options"

    def get(self, pipeline_id) -> Dict[str, Any]:
        resp: GetPipelineResponseBody = self._do_request(
            method_=self._get_method, pipeline_id=pipeline_id
        )
        return resp.to_map()

    def get_by_identifier(self, identifier, provider, version="v1"):
        res = self.list(identifier=identifier, provider=provider, version=version)
        if not res.items:
            return
        if len(res.items) > 1:
            logger.warning(
                f"Get pipeline by identifier returns more one pipeline: "
                f"identifier={identifier} provider={provider} version={version}"
            )
        return res.items[0]

    def get_schema(self, pipeline_id):
        resp: GetPipelineSchemaResponseBody = self._do_request(
            method_=self._get_schema_method, pipeline_id=pipeline_id
        )

        return resp.to_map()

    def list(
        self,
        identifier=None,
        provider=None,
        version=None,
        page_number=None,
        page_size=None,
    ) -> PaginatedResult:
        if provider:
            workspace_id = self.workspace_id_none_placeholder
        else:
            workspace_id = None

        request = ListPipelinesRequest(
            page_number=page_number,
            page_size=page_size,
            pipeline_provider=provider,
            pipeline_version=version,
            pipeline_identifier=identifier,
            workspace_id=workspace_id,
        )

        resp: ListPipelinesResponseBody = self._do_request(
            method_=self._list_method, request=request
        )
        return self.make_paginated_result(resp)

    def create(self, manifest):
        request = CreatePipelineRequest(manifest=manifest)
        resp: CreatePipelineResponseBody = self._do_request(
            method_=self._create_method, request=request
        )
        return resp.pipeline_id

    def delete(self, pipeline_id):
        self._do_request(
            method_=self._delete_method,
            pipeline_id=pipeline_id,
        )

    def update(self, pipeline_id, manifest):
        request = UpdatePipelineRequest(
            manifest=manifest,
        )
        self._do_request(
            method_=self._update_method, pipeline_id=pipeline_id, request=request
        )
