from __future__ import absolute_import

from pai.api.paiflow import PAIFlowClient
from pai.api.sts import StsClient
from pai.api.workspace import WorkspaceClient
from alibabacloud_tea_openapi.models import Config


class ClientConfig(object):
    def __init__(
        self,
        access_key_id,
        access_key_secret,
        region_id=None,
        endpoint=None,
        security_token=None,
        **kwargs
    ):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.security_token = security_token
        self.region_id = region_id
        self.endpoint = endpoint
        self.kwargs = kwargs

    def to_tea_config(self):
        config = Config(
            access_key_id=self.access_key_id,
            access_key_secret=self.access_key_secret,
            region_id=self.region_id,
            endpoint=self.endpoint,
            security_token=self.security_token,
            **self.kwargs
        )
        return config


class ClientFactory(object):
    @staticmethod
    def _is_inner_client(acs_client):
        return acs_client.get_region_id() == "center"

    @classmethod
    def create_paiflow_client(
        cls, access_key_id, access_key_secret, region_id, endpoint=None
    ):

        return PAIFlowClient(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            region_id=region_id,
            endpoint=endpoint,
        )

    @classmethod
    def create_sts_client(cls, acs_client):
        return StsClient(acs_client)

    @classmethod
    def create_workspace_client(
        cls, access_key_id, access_key_secret, region_id, endpoint=None
    ):
        return WorkspaceClient(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            region_id=region_id,
            endpoint=endpoint,
        )

    @classmethod
    def build_workspace_endpoint(cls, region_id):
        return "aiworkspace.{}.aliyuncs.com".format(region_id)

    @classmethod
    def build_paiflow_endpoint(cls, region_id):
        return "paiflow.{}.aliyuncs.com".format(region_id)
