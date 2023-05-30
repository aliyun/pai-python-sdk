from typing import Any, Dict, List, Union

from pai.api.base import PaginatedResult, PAIServiceName, WorkspaceScopedResourceAPI
from pai.libs.alibabacloud_aiworkspace20210204.models import (
    ListImagesRequest,
    ListImagesResponseBody,
)


class ImageLabel(object):
    # Unofficial Image Label
    UNOFFICIAL_LABEL = "system.official=false"
    # Official Image Label
    OFFICIAL_LABEL = "system.official=true"

    # PAI Image Label
    PROVIDER_PAI_LABEL = "system.origin=PAI"
    # Community Image Label
    PROVIDER_COMMUNITY_LABEL = "system.origin=Community"

    # DLC Image Label: for training
    DLC_LABEL = "system.supported.dlc=true"
    # EAS Image Label: for inference
    EAS_LABEL = "system.supported.eas=true"
    # DSW Image Label: for develop
    DSW_LABEL = "system.supported.dsw=true"

    # Accelerator: Use GPU
    DEVICE_TYPE_GPU = "system.chipType=GPU"
    DEVICE_TYPE_CPU = "system.chipType=CPU"

    # Python Version
    PYTHON_VERSION = "system.pythonVersion"


class ImageAPI(WorkspaceScopedResourceAPI):
    """Class which provide API to operate CodeSource resource."""

    BACKEND_SERVICE_NAME = PAIServiceName.AIWORKSPACE

    _list_method = "list_images_with_options"
    _create_method = "create_image_with_options"
    _delete_method = "add_image_with_options"

    def list(
        self,
        labels: Union[Dict[str, Any], List[str]] = ImageLabel.UNOFFICIAL_LABEL,
        name: str = None,
        order: str = "DESC",
        page_number: int = 1,
        page_size: int = 50,
        parent_user_id: str = None,
        query: str = None,
        sort_by: str = None,
        user_id: str = None,
        verbose: bool = False,
        **kwargs,
    ) -> PaginatedResult:
        """List image resources."""
        workspace_id = kwargs.pop("workspace_id", None)
        if isinstance(labels, dict):
            labels = ",".join(["{}={}".format(k, v) for k, v in labels.items()])
        elif isinstance(labels, list):
            labels = ",".join([item for item in labels])

        req = ListImagesRequest(
            labels=labels,
            name=name,
            order=order,
            page_number=page_number,
            page_size=page_size,
            parent_user_id=parent_user_id,
            query=query,
            sort_by=sort_by,
            user_id=user_id,
            verbose=verbose,
            workspace_id=workspace_id,
        )

        return self._list(request=req)

    def _list(self, request) -> PaginatedResult:
        resp: ListImagesResponseBody = self._do_request(
            self._list_method, request=request
        )

        return self.make_paginated_result(resp)
