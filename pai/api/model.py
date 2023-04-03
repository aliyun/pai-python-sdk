import typing

from pai.api.base import PaginatedResult, WorkspaceScopedResourceAPI
from pai.libs.alibabacloud_aiworkspace20210204.models import (
    CreateModelRequest,
    CreateModelVersionRequest,
    Label,
    ListModelsRequest,
    ListModelsResponseBody,
    ListModelVersionsRequest,
    ListModelVersionsResponseBody,
    UpdateModelVersionRequest,
)

if typing.TYPE_CHECKING:
    pass


class ModelAPI(WorkspaceScopedResourceAPI):

    _create_model_method = "create_model_with_options"
    _list_model_method = "list_models_with_options"
    _get_model_method = "get_model_with_options"
    _delete_model_method = "delete_model_with_options"

    _create_model_version_method = "create_model_version_with_options"
    _get_model_version_method = "get_model_version_with_options"
    _update_model_version_method = "update_model_version_with_options"
    _list_model_version_method = "list_model_versions_with_options"
    _delete_model_version_method = "delete_model_version_with_options"

    def get_api_object_by_resource_id(self, model_id):
        resp = self._do_request(self._get_model_method, model_id=model_id)
        return resp.to_map()

    def get_version_api_object(self, model_id, version):
        resp = self._do_request(
            self._get_model_version_method, model_id=model_id, version_name=version
        )
        return resp.to_map()

    def create_from_api_object(self, api_object):
        request = CreateModelRequest().from_map(api_object)

        resp = self._do_request(self._create_model_method, request=request)
        return resp.model_id

    def create(self, name, accessibility=None, labels=None, description=None):

        labels = [Label(key=k, value=v) for k, v in labels.items()] if labels else []

        request = CreateModelRequest(
            model_name=name,
            accessibility=accessibility,
            labels=labels,
            model_description=description,
        )

        resp = self._do_request(self._create_model_method, request=request)
        return resp.model_id

    def get(self, model_id):
        resp = self._do_request(method_=self._get_model_method, model_id=model_id)
        return resp.to_map()

    def delete(self, model_id):
        self._do_request(method_=self._delete_model_method, model_id=model_id)

    def create_version(
        self,
        model_id,
        uri,
        version=None,
        model_format=None,
        framework=None,
        labels=None,
        inference_spec=None,
        description=None,
    ):
        """Create a ModeVersion resource."""

        labels = [Label(key=k, value=v) for k, v in labels.items()] if labels else []

        request = CreateModelVersionRequest(
            version_name=version,
            format_type=model_format,
            framework_type=framework,
            inference_spec=inference_spec,
            labels=labels,
            uri=uri,
            version_description=description,
            # options=None,
            # source_id=None,
            # source_type=None,
        )

        response = self._do_request(
            self._create_model_version_method, model_id=model_id, request=request
        )

        version_name = response.to_map()["VersionName"]
        return version_name

    def get_model_version_api_object(self, model_id, version):
        resp = self._do_request(
            self._get_model_version_method, model_id=model_id, version_name=version
        )
        obj = resp.to_map()
        obj.update({"ModelId": model_id})
        return obj

    def get_version(self, model_id, version):
        return self.get_model_version_api_object(model_id=model_id, version=version)

    def refresh_version(self, model_version):
        api_obj = self.get_model_version_api_object(
            model_id=model_version.model_id, version=model_version.version
        )
        model_version.patch_from_api_object(api_obj)

    def list(
        self, name=None, order=None, page_number=None, page_size=None, sort_by=None
    ) -> PaginatedResult:

        request = ListModelsRequest(
            model_name=name,
            order=order,
            page_number=page_number,
            page_size=page_size,
            sort_by=sort_by,
            # labels=None,
            # label_string=None,
        )

        resp: ListModelsResponseBody = self._do_request(
            self._list_model_method, request=request
        )
        return self.make_paginated_result(resp)

    def list_versions(
        self,
        model_id,
        framework=None,
        model_format=None,
        page_number=None,
        page_size=None,
        order=None,
        sort_by=None,
    ) -> PaginatedResult:

        request = ListModelVersionsRequest(
            format_type=model_format,
            framework_type=framework,
            # label_string=None,
            # labels=None,
            order=order,
            sort_by=sort_by,
            # version_name=None,
            # source_id=None,
            # source_type=None,
            page_number=page_number,
            page_size=page_size,
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

    def update_version(self, model_id, version, inference_spec=None, description=None):
        request = UpdateModelVersionRequest(
            inference_spec=inference_spec, version_description=description
        )
        self._do_request(
            self._update_model_version_method,
            model_id=model_id,
            version_name=version,
            request=request,
        )

    def delete_version(self, model_id, version):
        self._do_request(
            self._delete_model_version_method,
            model_id=model_id,
            version_name=version,
        )
