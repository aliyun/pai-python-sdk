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
from typing import List

from ..libs.alibabacloud_aiworkspace20210204.models import (
    CreateExperimentRequest,
    CreateExperimentResponseBody,
    Experiment,
    LabelInfo,
    ListExperimentRequest,
    ListExperimentResponseBody,
    SetExperimentLabelsRequest,
    UpdateExperimentRequest,
)
from .base import PaginatedResult, ServiceName, WorkspaceScopedResourceAPI


class ExperimentAPI(WorkspaceScopedResourceAPI):
    BACKEND_SERVICE_NAME = ServiceName.PAI_WORKSPACE

    _get_method = "get_experiment_with_options"
    _create_method = "create_experiment_with_options"
    _list_method = "list_experiment_with_options"
    _update_method = "update_experiment_with_options"
    _delete_method = "delete_experiment_with_options"
    _set_labels_method = "set_experiment_labels_with_options"
    _delete_label_method = "delete_experiment_label_with_options"

    def get(self, experiment_id: str):
        resp: Experiment = self._do_request(
            method_=self._get_method, experiment_id=experiment_id
        )
        return resp.to_map()

    def create(
        self,
        name,
        artifact_uri,
        workspace_id,
        **kwargs,
    ):
        request = CreateExperimentRequest(
            name=name,
            artifact_uri=artifact_uri,
            workspace_id=workspace_id,
            **kwargs,
        )
        resp: CreateExperimentResponseBody = self._do_request(
            method_=self._create_method, request=request
        )
        return resp.experiment_id

    def list(
        self,
        name: str = None,
        page_size: int = 50,
        page_number: int = 1,
        order: str = "DESC",
        **kwargs,
    ) -> PaginatedResult:
        workspace_id = kwargs.pop("workspace_id", None)
        request = ListExperimentRequest(
            name=name,
            page_size=page_size,
            page_number=page_number,
            order=order,
            workspace_id=workspace_id,
            **kwargs,
        )
        resp: ListExperimentResponseBody = self._do_request(
            method_=self._list_method, request=request
        )
        return self.make_paginated_result(resp)

    def update(
        self,
        experiment_id: str,
        name: str,
        **kwargs,
    ):
        request = UpdateExperimentRequest(
            name=name,
            **kwargs,
        )
        self._do_request(
            method_=self._update_method, experiment_id=experiment_id, request=request
        )
        return

    def delete(self, experiment_id: str):
        self._do_request(method_=self._delete_method, experiment_id=experiment_id)
        return

    def set_experiment_labels(self, experiment_id: str, labels: List[LabelInfo]):
        request = SetExperimentLabelsRequest(
            labels=labels,
        )
        self._do_request(
            method_=self._set_labels_method,
            experiment_id=experiment_id,
            request=request,
        )
        return

    def delete_experiment_label(self, experiment_id: str, key: str):
        self._do_request(
            method_=self._delete_label_method, experiment_id=experiment_id, key=key
        )
        return
