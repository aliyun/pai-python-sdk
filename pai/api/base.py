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

from abc import ABCMeta
from typing import Any, Dict, List, Optional, Union

import six
from alibabacloud_tea_openapi.client import Client
from alibabacloud_tea_util.models import RuntimeOptions
from six import with_metaclass
from Tea.model import TeaModel

from ..common.logging import get_logger

logger = get_logger(__name__)


class ServiceName(object):
    # Service provided by PAI.
    PAI_DLC = "pai-dlc"
    PAI_EAS = "pai-eas"
    PAI_WORKSPACE = "aiworkspace"
    PAI_STUDIO = "pai"
    PAIFLOW = "paiflow"
    # Other services provided by Alibaba Cloud.
    STS = "sts"
    PAI_DSW = "pai-dsw"


class PAIRestResourceTypes(object):
    """Resource types provided by PAI REST API."""

    Dataset = "Dataset"
    DlcJob = "DlcJob"
    CodeSource = "CodeSource"
    Image = "Image"
    Service = "Service"
    Model = "Model"
    Workspace = "Workspace"
    Algorithm = "Algorithm"
    TrainingJob = "TrainingJob"
    Pipeline = "Pipeline"
    PipelineRun = "PipelineRun"
    TensorBoard = "TensorBoard"
    Experiment = "Experiment"


class ResourceAPI(with_metaclass(ABCMeta, object)):
    """Class that provide APIs to operate the resource."""

    BACKEND_SERVICE_NAME = None

    def __init__(
        self,
        acs_client: Client,
        header: Optional[Dict[str, str]] = None,
        runtime: Optional[RuntimeOptions] = None,
    ):
        """Initialize a ResourceAPI object.

        Args:
            acs_client (Client): A basic client used to communicate with a specific PAI
                service.
            header (Dict[str, str], optional): Header set in the HTTP request. Defaults
                to None.
            runtime (RuntimeOptions, optional): Options configured for the client
                runtime behavior, such as read_timeout, connection_timeout, etc.
                Defaults to None.
        """
        self.acs_client = acs_client
        self.header = header
        self.runtime = runtime

    def _make_extra_request_options(self):
        """Returns headers and runtime for client."""
        return self.header or dict(), self.runtime or RuntimeOptions()

    def _do_request(self, method_: str, *args, **kwargs):
        headers, runtime = self._make_extra_request_options()
        if "headers" not in kwargs:
            kwargs["headers"] = headers
        if "runtime" not in kwargs:
            kwargs["runtime"] = runtime
        request_method = getattr(self.acs_client, method_)

        return request_method(*args, **kwargs).body

    def get_api_object_by_resource_id(self, resource_id):
        raise NotImplementedError

    def refresh_entity(self, id_, entity):
        """Refresh entity using API object from service."""
        if not isinstance(id_, six.string_types) and not isinstance(
            id_, six.integer_types
        ):
            raise ValueError(
                "Expected integer type or string type for id, but given type %s"
                % type(id_)
            )
        api_obj = self.get_api_object_by_resource_id(resource_id=id_)
        return entity.patch_from_api_object(api_obj)

    @classmethod
    def make_paginated_result(
        cls,
        data: Union[Dict[str, Any], TeaModel],
        item_key=None,
    ) -> "PaginatedResult":
        """Make a paginated result from response.

        Args:
            data: Response data.
            item_key:

        Returns:

        """
        if isinstance(data, TeaModel):
            data = data.to_map()
        total_count = data.pop("TotalCount")

        if item_key:
            items = data[item_key]
        else:
            values = list([val for val in data.values() if isinstance(val, list)])
            if len(values) != 1:
                raise ValueError("Requires item key to make paginated result.")
            items = values[0]
        return PaginatedResult(items=items, total_count=total_count)


class WorkspaceScopedResourceAPI(with_metaclass(ABCMeta, ResourceAPI)):
    """Workspace Scoped Resource API."""

    # A workspace_id placeholder indicate the workspace_id field of
    # the request should not be replaced.
    workspace_id_none_placeholder = "WORKSPACE_ID_NONE_PLACEHOLDER"

    # Default parameter name for request object.
    default_param_name_for_request = "request"

    def __init__(self, workspace_id, acs_client, **kwargs):
        super(WorkspaceScopedResourceAPI, self).__init__(
            acs_client=acs_client, **kwargs
        )
        self.workspace_id = workspace_id

    def _do_request(self, method_, **kwargs):
        request = kwargs.get(self.default_param_name_for_request)

        if not request:
            # Sometimes, request object is not named as "request", we need to find it.
            for param_name, param_value in kwargs.items():
                if isinstance(param_value, TeaModel) and type(
                    param_value
                ).__name__.endswith("Request"):
                    request = param_value
                    break

        # Automatically configure the workspace ID for the request
        if request and hasattr(request, "workspace_id"):
            if request.workspace_id is None:
                request.workspace_id = self.workspace_id
            elif (
                request.workspace_id == self.workspace_id_none_placeholder
                or not request.workspace_id
            ):
                # request.workspace_id is 0 or request.workspace_id is empty string,
                # we do not inject workspace_id of the scope.
                request.workspace_id = None
        return super(WorkspaceScopedResourceAPI, self)._do_request(method_, **kwargs)


class PaginatedResult(object):
    """A class represent response of a pagination call to PAI service."""

    items: List[Union[Dict[str, Any], str]] = None
    total_count: int = None

    def __init__(self, items: List[Union[Dict[str, Any], str]], total_count: int):
        self.items = items
        self.total_count = total_count
