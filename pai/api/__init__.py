from __future__ import absolute_import

import json
import logging

from aliyunsdkcore.acs_exception.exceptions import ClientException, ServerException

from pai.api.exception import ServiceCallException

logger = logging.getLogger(__name__)


class BaseClient(object):

    def __init__(self, acs_client):
        self._acs_client = acs_client

    def _call_service_with_exception(self, request):
        logger.debug("Request:%s, path_params:%s, uri_params:%s, query_params:%s, body_params:%s",
                     type(request), request.get_path_params(), request.get_uri_params(),
                     request.get_query_params(), request.get_body_params())
        try:
            raw_resp = self._acs_client.do_action_with_exception(request)
            resp = self._response_to_dict(raw_resp)
        except (ClientException, ServerException) as e:
            raise ServiceCallException(e.__str__())
        return resp

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
