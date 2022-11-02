import logging
from abc import ABCMeta
from typing import Any, Dict, List, Union

import six
from alibabacloud_tea_util import models as util_models
from six import with_metaclass
from Tea.model import TeaModel

from pai.common.consts import PAIServiceName

logger = logging.getLogger(__name__)


class ResourceAPI(with_metaclass(ABCMeta, object)):
    """Class that provide APIs to operate the resource."""

    BACKEND_SERVICE_NAME = PAIServiceName.PAI_DLC

    def __init__(self, acs_client):
        self.acs_client = acs_client

    @classmethod
    def _make_extra_request_options(cls):
        """Returns headers and runtime for client."""
        return dict(), util_models.RuntimeOptions()

    def _do_request(self, method_, **kwargs):
        headers, runtime = self._make_extra_request_options()
        if "headers" not in kwargs:
            kwargs["headers"] = headers
        if "runtime" not in kwargs:
            kwargs["runtime"] = runtime
        resp = getattr(self.acs_client, method_)(**kwargs)
        # logger.debug(
        #     "DoRequest {} Response: status_code={} header={} body={}".format(
        #         type(self).__name__,
        #         resp.status_code,
        #         resp.headers,
        #         resp.body.to_map(),
        #     )
        # )
        self._check_response(resp)
        return resp.body

    def _check_response(self, resp):
        pass
        # if resp.status_code != 200:
        #     raise RuntimeError("Unexpected response: {} {}", type(self), resp.to_map())

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


class ScopeResourceAPI(ResourceAPI):
    """Scoped Resource API."""

    def __init__(self, workspace_id, acs_client):
        super(ScopeResourceAPI, self).__init__(acs_client=acs_client)
        self.workspace_id = workspace_id


class PaginatedResult(object):
    items: List[Dict[str, Any]] = None
    total_count: int = None

    def __init__(self, items: List[Dict[str, Any]], total_count: int):
        self.items = items
        self.total_count = total_count
