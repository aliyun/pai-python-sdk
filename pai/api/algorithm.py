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

from typing import Any, Dict, Tuple

from ..libs.alibabacloud_paistudio20220112.models import (
    AlgorithmSpec,
    CreateAlgorithmRequest,
    CreateAlgorithmResponseBody,
    CreateAlgorithmVersionRequest,
    CreateAlgorithmVersionResponseBody,
    GetAlgorithmVersionResponseBody,
    ListAlgorithmsRequest,
    ListAlgorithmsResponseBody,
    ListAlgorithmVersionsRequest,
)
from .base import PaginatedResult, ServiceName, WorkspaceScopedResourceAPI


class AlgorithmAPI(WorkspaceScopedResourceAPI):

    BACKEND_SERVICE_NAME = ServiceName.PAI_STUDIO

    _get_method = "get_algorithm_with_options"
    _list_method = "list_algorithms_with_options"
    _create_method = "create_algorithm_with_options"

    _get_version_method = "get_algorithm_version_with_options"
    _list_versions_method = "list_algorithm_versions_with_options"
    _create_version_method = "create_algorithm_version_with_options"

    # _delete_algorithm_version_method = "delete_algorithm_version_with_options"

    def get(self, algorithm_id):
        resp = self._do_request(method_=self._get_method, algorithm_id=algorithm_id)
        return resp.to_map()

    def list(
        self,
        algorithm_id=None,
        algorithm_provider=None,
        algorithm_name=None,
        page_number=1,
        page_size=10,
    ) -> PaginatedResult:

        if algorithm_provider:
            workspace_id = self.workspace_id_none_placeholder
        else:
            # Use default workspace configured in Session if provider is not configured.
            workspace_id = None

        request = ListAlgorithmsRequest(
            algorithm_id=algorithm_id,
            algorithm_name=algorithm_name,
            algorithm_provider=algorithm_provider,
            page_number=page_number,
            page_size=page_size,
            workspace_id=workspace_id,
        )

        resp: ListAlgorithmsResponseBody = self._do_request(
            method_=self._list_method, request=request
        )
        return self.make_paginated_result(resp)

    def create(self, name, description):
        request = CreateAlgorithmRequest(
            algorithm_description=description,
            algorithm_name=name,
        )

        res: CreateAlgorithmResponseBody = self._do_request(
            method_=self._create_method,
            request=request,
        )
        return res.algorithm_id

    def get_version(self, algorithm_id, algorithm_version) -> Dict[str, Any]:
        resp: GetAlgorithmVersionResponseBody = self._do_request(
            method_=self._get_version_method,
            algorithm_id=algorithm_id,
            algorithm_version=algorithm_version,
        )
        return resp.to_map()

    def list_versions(
        self, algorithm_id, page_size=50, page_number=1
    ) -> PaginatedResult:
        request = ListAlgorithmVersionsRequest(
            page_number=page_number, page_size=page_size
        )

        res = self._do_request(
            method_=self._list_versions_method,
            algorithm_id=algorithm_id,
            request=request,
        )
        return self.make_paginated_result(res)

    def create_version(
        self, algorithm_id, version, algorithm_spec: Dict[str, Any]
    ) -> Tuple[str, str]:
        request = CreateAlgorithmVersionRequest(
            algorithm_spec=AlgorithmSpec().from_map(algorithm_spec),
        )

        res: CreateAlgorithmVersionResponseBody = self._do_request(
            method_=self._create_version_method,
            algorithm_id=algorithm_id,
            algorithm_version=version,
            request=request,
        )

        return res.algorithm_id, res.algorithm_version

    def get_by_name(self, algorithm_name, algorithm_provider=None):
        page_size, page_number = 50, 1

        while True:
            result = self.list(
                algorithm_name=algorithm_name,
                algorithm_provider=algorithm_provider,
                page_size=page_size,
                page_number=page_number,
            )

            if result.total_count == 0:
                return

            for item in result.items:
                if item["AlgorithmName"] == algorithm_name:
                    return item

            page_number += 1
