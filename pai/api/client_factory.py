from .paiflow import PAIFlowClient
from .sts import StsClient


class ClientFactory(object):
    @staticmethod
    def create_paiflow_client(acs_client):
        return PAIFlowClient(acs_client)

    @staticmethod
    def create_sts_client(acs_client):
        return StsClient(acs_client)
