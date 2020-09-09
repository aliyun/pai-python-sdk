from __future__ import absolute_import

from pai.api.base import BaseClient

from aliyunsdksts.request.v20150401 import GetCallerIdentityRequest


class StsClient(BaseClient):

    def __init__(self, acs_client=None):
        super(StsClient, self).__init__(acs_client=acs_client)

    def _get_endpoint(self):
        return "sts.aliyuncs.com"

    def get_caller_identity(self):
        request = self._construct_request(GetCallerIdentityRequest.GetCallerIdentityRequest)
        return self._call_service_with_exception(request)
