import json
import logging
import typing
from typing import Any, Dict, Union

from pai.api.base import PaginatedResult, PAIServiceName, ResourceAPI
from pai.libs.alibabacloud_eas20210701.models import (
    CreateServiceRequest,
    CreateServiceResponseBody,
    ListServicesRequest,
    ListServicesResponseBody,
    ReleaseServiceRequest,
    UpdateServiceRequest,
    UpdateServiceVersionRequest,
)

logger = logging.getLogger(__name__)


class ServiceAPI(ResourceAPI):
    BACKEND_SERVICE_NAME = PAIServiceName.PAI_EAS

    _create_method = "create_service_with_options"
    _update_method = "update_service_with_options"
    _update_version_method = "update_service_version_with_options"
    _list_method = "list_services_with_options"
    _get_method = "describe_service_with_options"
    _start_method = "start_service_with_options"
    _stop_method = "stop_service_with_options"
    _delete_method = "delete_service_with_options"
    _release_method = "release_service_with_options"

    _get_group_method = "describe_group_with_options"
    _list_groups_method = "list_group_with_options"

    def __init__(self, region_id, acs_client, **kwargs):
        super(ServiceAPI, self).__init__(acs_client=acs_client, **kwargs)
        self.region_id = region_id

    def list(
        self, filter=None, order=None, page_number=None, page_size=None, sort=None
    ) -> PaginatedResult:
        """

        Returns:

        """
        request = ListServicesRequest(
            filter=filter,
            order=order,
            page_number=page_number,
            page_size=page_size,
            sort=sort,
        )
        resp: ListServicesResponseBody = self._do_request(self._list_method, request)
        return self.make_paginated_result(resp)

    def get_api_object_by_resource_id(self, resource_id):
        resp = self._do_request(
            self._get_method,
            cluster_id=self.region_id,
            service_name=resource_id,
        )
        return resp.to_map()

    def get(self, name: str) -> Dict[str, Any]:
        return self.get_api_object_by_resource_id(resource_id=name)

    def create(self, config: Union[str, typing.Dict]) -> str:
        """Create a PAI EAS Service resource, returns the service name."""

        if isinstance(config, str):
            config_obj = json.loads(config)
        else:
            config_obj = config

        request = CreateServiceRequest(body=config_obj)
        resp: CreateServiceResponseBody = self._do_request(self._create_method, request)
        return resp.service_name

    def release(self, name, weight):
        request = ReleaseServiceRequest(weight=weight)
        self._do_request(
            self._release_method,
            cluster_id=self.region_id,
            service_name=name,
            request=request,
        )

    def start(self, name):
        self._do_request(
            self._start_method, cluster_id=self.region_id, service_name=name
        )

    def stop(self, name):
        self._do_request(
            self._stop_method, cluster_id=self.region_id, service_name=name
        )

    def delete(self, name):
        self._do_request(
            self._delete_method, cluster_id=self.region_id, service_name=name
        )

    def update(self, name, config: Union[str, typing.Dict]):

        if isinstance(config, str):
            config_obj = json.loads(config)
        else:
            config_obj = config

        request: UpdateServiceRequest = UpdateServiceRequest(
            body=config_obj,
        )

        self._do_request(
            self._update_method,
            cluster_id=self.region_id,
            service_name=name,
            request=request,
        )

    def update_version(self, name, version):
        request = UpdateServiceVersionRequest(version=version)
        self._do_request(
            self._update_version_method,
            cluster_id=self.region_id,
            service_name=name,
            request=request,
        )

    def get_group(self, group_name) -> Dict[str, Any]:
        resp = self._do_request(
            self._get_group_method,
            cluster_id=self.region_id,
            group_name=group_name,
        )
        return resp.to_map()
