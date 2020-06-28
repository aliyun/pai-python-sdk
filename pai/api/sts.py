from pai.api import BaseClient

from libs.aliyunsdksts.request.v20150401 import GetCallerIdentityRequest


class StsClient(BaseClient):

    def __init__(self, acs_client=None):
        super(StsClient, self).__init__(acs_client=acs_client)

    def get_caller_identity(self):
        request = self._construct_request(GetCallerIdentityRequest.GetCallerIdentityRequest)
        return self._call_service_with_exception(request)
