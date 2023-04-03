import logging
from abc import ABCMeta
from typing import Any, Dict, List, Optional, Union

import six
from alibabacloud_tea_openapi.client import Client
from alibabacloud_tea_util.models import RuntimeOptions
from six import with_metaclass
from Tea.model import TeaModel

logger = logging.getLogger(__name__)


class PAIServiceName(object):
    PAI_DLC = "PAI_DLC"
    PAI_EAS = "PAI_EAS"
    AIWORKSPACE = "AIWORKSPACE"
    PAIFLOW = "PAIFLOW"
    TRAINING_SERVICE = "TRAINING"


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


class ResourceAPI(with_metaclass(ABCMeta, object)):
    """Class that provide APIs to operate the resource."""

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

    def _do_request(self, method_, *args, **kwargs):
        headers, runtime = self._make_extra_request_options()
        if "headers" not in kwargs:
            kwargs["headers"] = headers
        if "runtime" not in kwargs:
            kwargs["runtime"] = runtime
        resp = getattr(self.acs_client, method_)(*args, **kwargs)
        return resp.body

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

    def __init__(self, workspace_id, acs_client, **kwargs):
        super(WorkspaceScopedResourceAPI, self).__init__(
            acs_client=acs_client, **kwargs
        )
        self.workspace_id = workspace_id

    def _do_request(self, method_, **kwargs):
        headers, runtime = self._make_extra_request_options()
        if "headers" not in kwargs:
            kwargs["headers"] = headers
        if "runtime" not in kwargs:
            kwargs["runtime"] = runtime
        request = kwargs.get("request")

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

        resp = getattr(self.acs_client, method_)(**kwargs)
        return resp.body


class PaginatedResult(object):
    """A class represent response of a pagination call to PAI service."""

    items: List[Union[Dict[str, Any], str]] = None
    total_count: int = None

    def __init__(self, items: List[Union[Dict[str, Any], str]], total_count: int):
        self.items = items
        self.total_count = total_count
