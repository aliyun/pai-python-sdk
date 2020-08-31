from __future__ import absolute_import

from pai.api.paiflow import PAIFlowClient
from pai.api.sts import StsClient


class ClientFactory(object):

    @staticmethod
    def _is_inner_client(acs_client):
        if acs_client.get_region_id() == "center":
            return True
        return False

    @classmethod
    def create_paiflow_client(cls, acs_client):
        return PAIFlowClient(acs_client, cls._is_inner_client(acs_client))

    @classmethod
    def create_sts_client(cls, acs_client):
        return StsClient(acs_client)
