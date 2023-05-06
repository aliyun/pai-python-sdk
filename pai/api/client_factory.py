from __future__ import absolute_import

import logging
import os

from alibabacloud_tea_openapi.models import Config

import pai
from pai.api.base import PAIServiceName
from pai.common.utils import default_user_agent
from pai.libs.alibabacloud_aiworkspace20210204.client import Client as WorkspaceClient
from pai.libs.alibabacloud_eas20210701.client import Client as EasClient
from pai.libs.alibabacloud_pai_dlc20201203.client import Client as DlcClient
from pai.libs.alibabacloud_paiflow20210202.client import Client as FlowClient
from pai.libs.alibabacloud_paistudio20220112.client import Client as TrainingClient

_logger = logging.getLogger(__name__)

PAI_SERVICE_ENDPOINT_ENV_KEY_PATTERN = "{}_SERVICE_ENDPOINT"

PAI_SERVICE_ENDPOINT_BY_REGION_ID_PATTERN = "{}.{}.aliyuncs.com"

PAI_SERVICE_NAME_POP_PRODUCT_NAME_MAPPING = {
    PAIServiceName.PAI_DLC: "pai-dlc",
    PAIServiceName.PAI_EAS: "pai-eas",
    PAIServiceName.AIWORKSPACE: "aiworkspace",
    PAIServiceName.PAIFLOW: "paiflow",
    PAIServiceName.TRAINING_SERVICE: "pai",
}


class ClientFactory(object):
    ClientClsByServiceName = {
        PAIServiceName.PAI_DLC: DlcClient,
        PAIServiceName.PAI_EAS: EasClient,
        PAIServiceName.AIWORKSPACE: WorkspaceClient,
        PAIServiceName.PAIFLOW: FlowClient,
        PAIServiceName.TRAINING_SERVICE: TrainingClient,
    }

    @staticmethod
    def _is_inner_client(acs_client):
        return acs_client.get_region_id() == "center"

    @classmethod
    def create_client(
        cls,
        service_name,
        access_key_id: str,
        access_key_secret: str,
        region_id: str,
        security_token: str = None,
        endpoint: str = None,
        **kwargs,
    ):
        """Create an OpenAPI client which is responsible to interacted with the PAI service.

        Args:
            service_name:  PAI Service name.
            access_key_id:
            access_key_secret:
            region_id:
            security_token:
            endpoint:
            **kwargs:

        Returns:

        """
        config = Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            region_id=region_id,
            security_token=security_token,
            endpoint=cls.get_endpoint(
                service_name=service_name,
                region_id=region_id,
                endpoint=endpoint,
            ),
            signature_algorithm="v2",
            user_agent=default_user_agent(),
            **kwargs,
        )
        client = cls.ClientClsByServiceName.get(service_name)(config)
        return client

    @classmethod
    def get_endpoint(cls, service_name: str, region_id: str, endpoint: str = None):
        """Get the endpoint for the service client.

        Args:
            service_name:
            region_id:
            endpoint:

        Returns:
            str: Endpoint for the service.
        """
        # 1. Use specific endpoint.
        if endpoint:
            return endpoint

        # 2. Use endpoint configured in environment variable.
        key = PAI_SERVICE_ENDPOINT_ENV_KEY_PATTERN.format(
            service_name.upper().replace("-", "_")
        )
        if os.environ.get(key):
            endpoint = os.environ.get(key)
            logging.info(
                f"Using PAI service endpoint from environment: "
                f"service_name={service_name} "
                f"endpoint={endpoint}"
            )
            return endpoint

        # 3. Get endpoint using product_name and region_id.
        pop_product_name = PAI_SERVICE_NAME_POP_PRODUCT_NAME_MAPPING.get(service_name)
        if not pop_product_name:
            raise ValueError(
                "Unknown service endpoint: Service Name={}".format(service_name)
            )

        if not region_id:
            raise ValueError("Please provide region_id to get the endpoint.")
        return PAI_SERVICE_ENDPOINT_BY_REGION_ID_PATTERN.format(
            pop_product_name, region_id
        )
