from __future__ import absolute_import

import json

from aliyunsdkcore.acs_exception.exceptions import ClientException, ServerException

from pai.api.exception import ServiceCallException


class BaseClient(object):

    def __init__(self, acs_client):
        self._acs_client = acs_client

    def _call_service_with_exception(self, request):
        try:
            raw_resp = self._acs_client.do_action_with_exception(request)
            resp = self._response_to_dict(raw_resp)
        except (ClientException, ServerException) as e:
            raise ServiceCallException(e.__str__())

        # if int(resp["Code"]) != 200:
        #     message = "Service response error, code:%s, message:%s" % (
        #         resp["Code"], resp["Message"])
        #     raise ServiceCallException(message)
        return resp

    def _get_endpoint(self):
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
        req.set_protocol_type("https")
        return req
