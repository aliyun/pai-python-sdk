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

import typing
from typing import Any, Dict

from ..libs.alibabacloud_aiworkspace20210204.models import (
    CreateModelRequest,
    CreateModelVersionRequest,
    Label,
    ListModelsRequest,
    ListModelsResponseBody,
    ListModelVersionsRequest,
    ListModelVersionsResponseBody,
    UpdateModelVersionRequest,
)
from .base import PaginatedResult, ServiceName, WorkspaceScopedResourceAPI

if typing.TYPE_CHECKING:
    pass


class ModelAPI(WorkspaceScopedResourceAPI):

    BACKEND_SERVICE_NAME = ServiceName.PAI_WORKSPACE

    _create_model_method = "create_model_with_options"
    _list_model_method = "list_models_with_options"
    _get_model_method = "get_model_with_options"
    _delete_model_method = "delete_model_with_options"

    _create_model_version_method = "create_model_version_with_options"
    _list_model_version_method = "list_model_versions_with_options"
    _get_model_version_method = "get_model_version_with_options"
    _update_model_version_method = "update_model_version_with_options"
    _delete_model_version_method = "delete_model_version_with_options"

    def create(
        self,
        accessibility: str = None,
        domain: str = None,
        labels: Dict[str, str] = None,
        model_description: str = None,
        model_doc: str = None,
        model_name: str = None,
        origin: str = None,
        task: str = None,
        workspace_id: str = None,
    ) -> str:
        labels = [Label(key=k, value=v) for k, v in labels.items()] if labels else []

        request = CreateModelRequest(
            accessibility=accessibility,
            domain=domain,
            labels=labels,
            model_description=model_description,
            model_doc=model_doc,
            model_name=model_name,
            origin=origin,
            task=task,
            workspace_id=workspace_id,
        )

        resp = self._do_request(self._create_model_method, request=request)
        return resp.model_id

    def list(
        self,
        collections: str = None,
        domain: str = None,
        label: str = None,
        label_string: str = None,
        labels: str = None,
        model_name: str = None,
        order: str = None,
        origin: str = None,
        page_number: int = None,
        page_size: int = None,
        provider: str = None,
        query: str = None,
        sort_by: str = None,
        task: str = None,
        workspace_id: str = None,
    ) -> PaginatedResult:
        request = ListModelsRequest(
            collections=collections,
            domain=domain,
            label=label,
            label_string=label_string,
            labels=labels,
            model_name=model_name,
            order=order,
            origin=origin,
            page_number=page_number,
            page_size=page_size,
            provider=provider,
            query=query,
            sort_by=sort_by,
            task=task,
            workspace_id=workspace_id,
        )

        resp: ListModelsResponseBody = self._do_request(
            self._list_model_method, request=request
        )
        return self.make_paginated_result(resp)

    def get(self, model_id: str):
        resp = self._do_request(method_=self._get_model_method, model_id=model_id)
        return resp.to_map()

    def delete(self, model_id: str):
        self._do_request(method_=self._delete_model_method, model_id=model_id)

    def create_version(
        self,
        model_id: str,
        approval_status: str = None,
        evaluation_spec: Dict[str, Any] = None,
        format_type: str = None,
        framework_type: str = None,
        inference_spec: Dict[str, Any] = None,
        labels: Dict[str, str] = None,
        metrics: Dict[str, Any] = None,
        options: str = None,
        source_id: str = None,
        source_type: str = None,
        training_spec: Dict[str, Any] = None,
        uri: str = None,
        version_description: str = None,
        version_name: str = None,
    ):
        """Create a ModeVersion resource."""
        labels = [Label(key=k, value=v) for k, v in labels.items()] if labels else []

        request = CreateModelVersionRequest(
            approval_status=approval_status,
            evaluation_spec=evaluation_spec,
            format_type=format_type,
            framework_type=framework_type,
            inference_spec=inference_spec,
            labels=labels,
            metrics=metrics,
            options=options,
            source_id=source_id,
            source_type=source_type,
            training_spec=training_spec,
            uri=uri,
            version_description=version_description,
            version_name=version_name,
        )

        response = self._do_request(
            self._create_model_version_method, model_id=model_id, request=request
        )

        version_name = response.to_map()["VersionName"]
        return version_name

    def list_versions(
        self,
        model_id,
        approval_status: str = None,
        format_type: str = None,
        framework_type: str = None,
        label: str = None,
        label_string: str = None,
        labels: str = None,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        sort_by: str = None,
        source_id: str = None,
        source_type: str = None,
        version_name: str = None,
    ) -> PaginatedResult:
        request = ListModelVersionsRequest(
            approval_status=approval_status,
            format_type=format_type,
            framework_type=framework_type,
            label=label,
            label_string=label_string,
            labels=labels,
            order=order,
            page_number=page_number,
            page_size=page_size,
            sort_by=sort_by,
            source_id=source_id,
            source_type=source_type,
            version_name=version_name,
        )

        resp: ListModelVersionsResponseBody = self._do_request(
            self._list_model_version_method, model_id=model_id, request=request
        )

        data = resp.to_map()
        for v in data["Versions"]:
            v.update(
                {
                    "ModelId": model_id,
                }
            )
        return self.make_paginated_result(data)

    def get_version(self, model_id: str, version: str):
        resp = self._do_request(
            self._get_model_version_method, model_id=model_id, version_name=version
        )
        obj = resp.to_map()
        obj.update({"ModelId": model_id})
        return obj

    def update_version(
        self,
        model_id: str,
        version: str,
        approval_status: str = None,
        evaluation_spec: Dict[str, Any] = None,
        inference_spec: Dict[str, Any] = None,
        metrics: Dict[str, Any] = None,
        options: str = None,
        source_id: str = None,
        source_type: str = None,
        training_spec: Dict[str, Any] = None,
        version_description: str = None,
    ):
        request = UpdateModelVersionRequest(
            approval_status=approval_status,
            evaluation_spec=evaluation_spec,
            inference_spec=inference_spec,
            metrics=metrics,
            options=options,
            source_id=source_id,
            source_type=source_type,
            training_spec=training_spec,
            version_description=version_description,
        )
        self._do_request(
            self._update_model_version_method,
            model_id=model_id,
            version_name=version,
            request=request,
        )

    def delete_version(self, model_id: str, version: str):
        self._do_request(
            self._delete_model_version_method,
            model_id=model_id,
            version_name=version,
        )
