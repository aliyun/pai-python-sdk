#  Copyright 2023 Alibaba, Inc. or its affiliates.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from __future__ import absolute_import

from typing import Optional

from alibabacloud_credentials.client import Client as CredentialClient
from alibabacloud_sts20150401.client import Client as StsClient
from alibabacloud_tea_openapi.models import Config

from ..common.consts import Network
from ..common.logging import get_logger
from ..common.utils import http_user_agent
from ..libs.alibabacloud_aiworkspace20210204.client import Client as WorkspaceClient
from ..libs.alibabacloud_eas20210701.client import Client as EasClient
from ..libs.alibabacloud_pai_dlc20201203.client import Client as DlcClient
from ..libs.alibabacloud_pai_dsw20220101.client import Client as DswClient
from ..libs.alibabacloud_paiflow20210202.client import Client as FlowClient
from ..libs.alibabacloud_paistudio20220112.client import Client as PaiClient
from .base import ServiceName

_logger = get_logger(__name__)

DEFAULT_SERVICE_ENDPOINT_PATTERN = "{}.{}.aliyuncs.com"


class ClientFactory(object):
    ClientByServiceName = {
        ServiceName.PAI_DLC: DlcClient,
        ServiceName.PAI_EAS: EasClient,
        ServiceName.PAI_WORKSPACE: WorkspaceClient,
        ServiceName.PAIFLOW: FlowClient,
        ServiceName.PAI_STUDIO: PaiClient,
        ServiceName.STS: StsClient,
        ServiceName.PAI_DSW: DswClient,
    }

    @staticmethod
    def _is_inner_client(acs_client):
        return acs_client.get_region_id() == "center"

    @classmethod
    def create_client(
        cls,
        service_name,
        region_id: str,
        credential_client: CredentialClient,
        network: Optional[Network] = None,
        **kwargs,
    ):
        """Create an API client which is responsible to interacted with the Alibaba
        Cloud service."""

        config = Config(
            region_id=region_id,
            credential=credential_client,
            endpoint=cls.get_endpoint(
                service_name=service_name,
                region_id=region_id,
                network=network,
            ),
            signature_algorithm="v2",
            user_agent=http_user_agent(),
            **kwargs,
        )
        client = cls.ClientByServiceName.get(service_name)(config)
        return client

    @classmethod
    def get_endpoint(
        cls, service_name: str, region_id: str, network: Optional[Network] = None
    ) -> str:
        """Get the endpoint for the service client."""
        if not region_id:
            raise ValueError("Please provide region_id to get the endpoint.")

        if network and network != Network.PUBLIC:
            if service_name == "pai-eas":
                # see endpoint list provided by PAI-EAS
                # https://next.api.aliyun.com/product/eas
                subdomain = f"pai-eas-manage-{network.value.lower()}"
            else:
                subdomain = f"{service_name}-{network.value.lower()}"
        else:
            subdomain = service_name
        return DEFAULT_SERVICE_ENDPOINT_PATTERN.format(subdomain, region_id)
