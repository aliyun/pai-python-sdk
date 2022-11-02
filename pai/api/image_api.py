from pai.api.base import PaginatedResult, ScopeResourceAPI
from pai.common.consts import DEFAULT_PAGE_NUMBER, DEFAULT_PAGE_SIZE, PAIServiceName
from pai.libs.alibabacloud_aiworkspace20210204.client import Client
from pai.libs.alibabacloud_aiworkspace20210204.models import (
    ListImagesRequest,
    ListImagesResponseBody,
)


class ImageAPI(ScopeResourceAPI):
    """Class which provide API to operate CodeSource resource."""

    BACKEND_SERVICE_NAME = PAIServiceName.AIWORKSPACE

    # Default List image label filter.
    _LIST_IMAGE_DEFAULT_LABEL_FILTER = "system.official=false"
    _LIST_IMAGE_PAI_LABEL_FILTER = (
        "system.origin=PAI,system.official=true,system.supported.dlc=true"
    )
    _LIST_IMAGE_COMMUNITY_LABEL_FILTER = "system.origin=Community,system.official=true"

    _LIST_DEFAULT_SORT_BY_FIELD = "GmtCreateTime"
    _LIST_DEFAULT_ORDER = "ASC"

    _list_method = "list_images_with_options"
    _create_method = "create_image_with_options"
    _delete_method = "add_image_with_options"

    def __init__(self, workspace_id: str, acs_client: Client) -> None:
        super(ImageAPI, self).__init__(workspace_id=workspace_id, acs_client=acs_client)

    def list(
        self,
        name=None,
        creator_id=None,
        verbose=False,
        labels=_LIST_IMAGE_DEFAULT_LABEL_FILTER,
        workspace_id=None,
        sort_by=None,
        order=_LIST_DEFAULT_ORDER,
        page_number=DEFAULT_PAGE_NUMBER,
        page_size=DEFAULT_PAGE_SIZE,
    ):
        """List image resources."""

        if workspace_id is None:
            workspace_id = self.workspace_id

        if isinstance(labels, dict):
            labels = ["{}={}".format(k, v) for k, v in labels.items()]

        req = ListImagesRequest(
            labels=labels,
            name=name,
            operator_create=creator_id,
            sort_by=sort_by,
            order=order,
            verbose=verbose,
            page_size=page_size,
            page_number=page_number,
            workspace_id=workspace_id,
        )

        return self._list(request=req)

    def _list(self, request) -> PaginatedResult:
        resp: ListImagesResponseBody = self._do_request(
            self._list_method, request=request
        )

        return self.make_paginated_result(resp)

    def list_community_images(
        self, name=None, page_size=DEFAULT_PAGE_SIZE, page_number=DEFAULT_PAGE_NUMBER
    ) -> PaginatedResult:
        """List image_api provided by community.

        Args:
            name: Name of the image, support fuzzy matching.
            page_size: Page size
            page_number: Page Number
        """
        req = ListImagesRequest(
            name=name,
            labels=self._LIST_IMAGE_COMMUNITY_LABEL_FILTER,
            sort_by=self._LIST_DEFAULT_SORT_BY_FIELD,
            order=self._LIST_DEFAULT_ORDER,
            verbose=True,
            page_size=page_size,
            page_number=page_number,
        )
        return self._list(request=req)

    def list_pai_images(
        self, name=None, page_size=DEFAULT_PAGE_SIZE, page_number=DEFAULT_PAGE_NUMBER
    ) -> PaginatedResult:
        """List image_api provided by PAI."""
        req = ListImagesRequest(
            name=name,
            labels=self._LIST_IMAGE_PAI_LABEL_FILTER,
            sort_by=self._LIST_DEFAULT_SORT_BY_FIELD,
            order=self._LIST_DEFAULT_ORDER,
            verbose=True,
            page_size=page_size,
            page_number=page_number,
        )
        return self._list(request=req)
