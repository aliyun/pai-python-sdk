from __future__ import absolute_import

import json
import os
from functools import wraps
import logging

from aliyunsdkcore.acs_exception.exceptions import ClientException, ServerException

from pai.core.exception import ServiceCallException

DefaultPageSize = 50

logger = logging.getLogger(__name__)


def paginate_service_call(f):
    @wraps(f)
    def _(self, *args, **kwargs):
        request = f(self, *args, **kwargs)
        return self._call_paginate_service_with_exception(request)

    return _


class BaseClient(object):
    _ENV_SERVICE_ENDPOINT_KEY = None

    def __init__(self, acs_client, endpoint=None):
        self._acs_client = acs_client

        if endpoint:
            self._endpoint = endpoint
        elif self._ENV_SERVICE_ENDPOINT_KEY is not None and \
                self._ENV_SERVICE_ENDPOINT_KEY in os.environ:
            self._endpoint = os.environ[self._ENV_SERVICE_ENDPOINT_KEY]
        else:
            self._endpoint = None

    def _call_service_with_exception(self, request):
        logger.debug("Request:%s, path_params:%s, uri_params:%s, query_params:%s, body_params:%s",
                     type(request), request.get_path_params(), request.get_uri_params(),
                     request.get_query_params(), request.get_body_params())
        try:
            raw_resp = self._acs_client.do_action_with_exception(request)
            logger.debug("Response:%s", raw_resp)
            resp = self._response_to_dict(raw_resp)
        except (ClientException, ServerException) as e:
            raise ServiceCallException(e.__str__())
        return resp

    def _call_paginate_service_with_exception(self, request, page_size=DefaultPageSize):
        page_num = 1
        is_end = False
        while not is_end:
            request.set_PageNumber(page_num)
            request.set_PageSize(page_size)
            logger.debug("Paginate Request:%s:page_size:%s, page_number:%s", type(self).__name__,
                         page_size, page_num)
            resp = self._call_service_with_exception(request)
            total_count = resp["TotalCount"]
            for resource in resp["Data"]:
                yield resource
            if page_num * page_size >= total_count:
                is_end = True
            page_num += 1

    @property
    def region_id(self):
        return self._acs_client.get_region_id()

    def _get_endpoint(self):
        pass

    def _get_product(self):
        pass

    @classmethod
    def _response_to_dict(cls, response):
        if not response:
            return dict()

        return json.loads(response, encoding="utf-8")

    def _construct_request(self, request_cls):
        req = request_cls()
        req.set_accept_format("json")

        if req.get_method() in ["POST", "PUT"]:
            req.set_content_type("application/json")

        if self._get_endpoint():
            req.set_endpoint(self._get_endpoint())

        if self._get_product():
            req.set_product(self._get_product())

        req.set_protocol_type("https")
        return req
