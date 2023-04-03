import json
from typing import Any, Dict, List, Optional, Union

from pai.api.base import PaginatedResult, PAIServiceName, WorkspaceScopedResourceAPI
from pai.common.consts import (
    DatasetSourceType,
    DataType,
    FileProperty,
    ResourceAccessibility,
)
from pai.libs.alibabacloud_aiworkspace20210204.models import (
    CreateDatasetRequest,
    DatasetLabel,
    ListDatasetsRequest,
    ListDatasetsResponseBody,
)


class DatasetAPI(WorkspaceScopedResourceAPI):
    """Class which provide API to operate Dataset resource."""

    BACKEND_SERVICE_NAME = PAIServiceName.AIWORKSPACE

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
    ) -> PaginatedResult:
        """Returns Dataset in paging.

        Args:
            data_source_type: Data source type of the dataset using, support OSS and NAS.
            name: Name of the Dataset.
            page_number: Page number.
            page_size: Page size.

        Returns:
            int: A list of datasets match the conditions.
        """

        request = ListDatasetsRequest(
            data_source_types=data_source_type,
            name=name,
            page_size=page_size,
            page_number=page_number,
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
