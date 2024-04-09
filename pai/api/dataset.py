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

import json
from typing import Any, Dict, List, Optional, Union

from ..common.consts import (
    DatasetSourceType,
    DataType,
    FileProperty,
    ResourceAccessibility,
)
from ..libs.alibabacloud_aiworkspace20210204.models import (
    CreateDatasetRequest,
    DatasetLabel,
    ListDatasetsRequest,
    ListDatasetsResponseBody,
)
from .base import PaginatedResult, ServiceName, WorkspaceScopedResourceAPI


class DatasetAPI(WorkspaceScopedResourceAPI):
    """Class which provide API to operate Dataset resource."""

    BACKEND_SERVICE_NAME = ServiceName.PAI_WORKSPACE

    _list_method = "list_datasets_with_options"
    _get_method = "get_dataset_with_options"
    _delete_method = "delete_dataset_with_options"
    _create_method = "create_dataset_with_options"

    def list(
        self,
        data_source_type: str = None,
        name: str = None,
        page_size: int = 20,
        page_number: int = 1,
        order: str = "DESC",
        **kwargs,
    ) -> PaginatedResult:
        """Returns Dataset in paging.

        Args:
            data_source_type: Data source type of the dataset using, support OSS and NAS.
            name: Name of the Dataset.
            page_number: Page number.
            page_size: Page size.
            order: Return list order.

        Returns:
            int: A list of datasets match the conditions.
        """

        request = ListDatasetsRequest(
            data_source_types=data_source_type,
            name=name,
            page_size=page_size,
            page_number=page_number,
            order=order,
            **kwargs,
        )

        resp: ListDatasetsResponseBody = self._do_request(
            self._list_method, request=request
        )

        return self.make_paginated_result(resp)

    def get_api_object_by_resource_id(
        self, resource_id: str
    ) -> Dict[str, Union[List[Dict[str, str]], str]]:
        result = self._do_request(self._get_method, dataset_id=resource_id)
        return result.to_map()

    def get(self, id: str) -> Dict[str, Any]:
        """Get Dataset by Id.

        Returns:
            dict:
        """

        return self.get_api_object_by_resource_id(resource_id=id)

    def delete(self, id):
        """Delete the Dataset."""
        self._do_request(self._delete_method, dataset_id=id)

    def create(
        self,
        uri: str,
        name: Optional[str] = None,
        data_source_type: str = None,
        options: Union[str, Dict[str, Any]] = None,
        description: str = None,
        labels: Optional[Dict[str, str]] = None,
        mount_path: str = "/mnt/data/",
        data_type: str = DataType.COMMON,
        accessibility: str = ResourceAccessibility.PUBLIC,
        property: str = FileProperty.DIRECTORY,
        source_type: str = DatasetSourceType.USER,
    ) -> str:
        """Create a Dataset resource."""

        labels = labels or dict()
        request = CreateDatasetRequest(
            accessibility=accessibility,
            data_source_type=data_source_type,
            data_type=data_type,
            description=description,
            labels=[
                DatasetLabel(key=key, value=value) for key, value in labels.items()
            ],
            name=name,
            options=self._patch_mount_path(options, mount_path=mount_path),
            property=property,
            source_type=source_type,
            uri=uri,
        )
        result = self._do_request(self._create_method, request=request)
        return result.dataset_id

    @classmethod
    def _patch_mount_path(cls, options: Union[str, Dict[str, Any]], mount_path: str):
        if isinstance(options, str):
            options = json.loads(options)
        options = options or dict()
        if mount_path:
            options.update({"mountPath": mount_path})

        return json.dumps(options)
