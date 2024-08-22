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
from typing import Optional, Union

from alibabacloud_credentials.client import Client as CredentialClient
from alibabacloud_sts20150401.client import Client as StsClient

from ..common.consts import DEFAULT_NETWORK_TYPE, PAI_VPC_ENDPOINT, Network
from ..common.utils import is_domain_connectable
from .algorithm import AlgorithmAPI
from .base import PAIRestResourceTypes, ServiceName, WorkspaceScopedResourceAPI
from .client_factory import ClientFactory
from .code_source import CodeSourceAPI
from .dataset import DatasetAPI
from .experiment import ExperimentAPI
from .image import ImageAPI
from .job import JobAPI
from .model import ModelAPI
from .pipeline import PipelineAPI
from .pipeline_run import PipelineRunAPI
from .service import ServiceAPI
from .tensorboard import TensorBoardAPI
from .training_job import TrainingJobAPI
from .workspace import WorkspaceAPI

_RESOURCE_API_MAPPING = {
    PAIRestResourceTypes.DlcJob: JobAPI,
    PAIRestResourceTypes.CodeSource: CodeSourceAPI,
    PAIRestResourceTypes.Dataset: DatasetAPI,
    PAIRestResourceTypes.Image: ImageAPI,
    PAIRestResourceTypes.Service: ServiceAPI,
    PAIRestResourceTypes.Model: ModelAPI,
    PAIRestResourceTypes.Workspace: WorkspaceAPI,
    PAIRestResourceTypes.Algorithm: AlgorithmAPI,
    PAIRestResourceTypes.TrainingJob: TrainingJobAPI,
    PAIRestResourceTypes.Pipeline: PipelineAPI,
    PAIRestResourceTypes.PipelineRun: PipelineRunAPI,
    PAIRestResourceTypes.TensorBoard: TensorBoardAPI,
    PAIRestResourceTypes.Experiment: ExperimentAPI,
}


class ResourceAPIsContainerMixin(object):
    """ResourceAPIsContainerMixin provides Resource Operation APIs."""

    _credential_client = None
    _credential_config = None
    _region_id = None
    _workspace_id = None

    def __init__(
        self, header=None, runtime=None, network: Optional[Union[str, Network]] = None
    ):
        """Initialize ResourceAPIsContainerMixin.

        Args:
            header: Header for API request.
            runtime: Runtime for API request.
            network: Network type used to connect to PAI services.
        """
        self.header = header
        self.runtime = runtime
        self.api_container = dict()
        self.acs_client_container = dict()
        if network:
            self.network = (
                Network.from_string(network) if isinstance(network, str) else network
            )
        elif DEFAULT_NETWORK_TYPE:
            self.network = Network.from_string(DEFAULT_NETWORK_TYPE)
        else:
            self.network = (
                Network.VPC
                if is_domain_connectable(PAI_VPC_ENDPOINT.format(self._region_id))
                else Network.PUBLIC
            )

    def _acs_credential_client(self):
        if self._credential_client:
            return self._credential_client
        self._credential_client = CredentialClient(config=self._credential_config)
        return self._credential_client

    def _get_acs_client(self, service_name):
        if service_name in self.acs_client_container:
            return self.acs_client_container[service_name]
        acs_client = ClientFactory.create_client(
            service_name=service_name,
            credential_client=self._acs_credential_client(),
            region_id=self._region_id,
            network=self.network,
        )
        self.acs_client_container[service_name] = acs_client
        return acs_client

    @property
    def _acs_workspace_client(self):
        return self._get_acs_client(ServiceName.PAI_WORKSPACE)

    @property
    def _acs_dlc_client(self):
        return self._get_acs_client(ServiceName.PAI_DLC)

    @property
    def _acs_paiflow_client(self):
        return self._get_acs_client(ServiceName.PAIFLOW)

    @property
    def _acs_eas_client(self):
        return self._get_acs_client(ServiceName.PAI_EAS)

    @property
    def _acs_training_client(self):
        return self._get_acs_client(ServiceName.PAI_STUDIO)

    @property
    def _acs_sts_client(self) -> StsClient:
        return self._get_acs_client(ServiceName.STS)

    def get_api_by_resource(self, resource_type):
        if resource_type in self.api_container:
            return self.api_container[resource_type]

        api_cls = _RESOURCE_API_MAPPING[resource_type]
        acs_client = self._get_acs_client(api_cls.BACKEND_SERVICE_NAME)
        if issubclass(api_cls, WorkspaceScopedResourceAPI):
            api = api_cls(
                workspace_id=self._workspace_id,
                acs_client=acs_client,
                header=self.header,
                runtime=self.runtime,
            )
        elif api_cls == ServiceAPI:
            # for PAI-EAS service api, we need to pass region_id.
            api = api_cls(
                acs_client=acs_client,
                region_id=self._region_id,
                header=self.header,
                runtime=self.runtime,
            )
        else:
            api = api_cls(
                acs_client=acs_client,
                header=self.header,
                runtime=self.runtime,
            )
        self.api_container[resource_type] = api
        return api

    @property
    def job_api(self) -> JobAPI:
        """Returns JobAPI for job operation."""
        return self.get_api_by_resource(PAIRestResourceTypes.DlcJob)

    @property
    def tensorboard_api(self) -> TensorBoardAPI:
        return self.get_api_by_resource(PAIRestResourceTypes.TensorBoard)

    @property
    def code_source_api(self) -> CodeSourceAPI:
        """Return CodeSource API for code_source operation"""
        return self.get_api_by_resource(PAIRestResourceTypes.CodeSource)

    @property
    def dataset_api(self) -> DatasetAPI:
        """Return Dataset API for dataset operation"""
        return self.get_api_by_resource(PAIRestResourceTypes.Dataset)

    @property
    def image_api(self) -> ImageAPI:
        return self.get_api_by_resource(PAIRestResourceTypes.Image)

    @property
    def model_api(self) -> ModelAPI:
        return self.get_api_by_resource(PAIRestResourceTypes.Model)

    @property
    def service_api(self) -> ServiceAPI:
        return self.get_api_by_resource(PAIRestResourceTypes.Service)

    @property
    def workspace_api(self) -> WorkspaceAPI:
        return self.get_api_by_resource(PAIRestResourceTypes.Workspace)

    @property
    def algorithm_api(self) -> AlgorithmAPI:
        return self.get_api_by_resource(PAIRestResourceTypes.Algorithm)

    @property
    def training_job_api(self) -> TrainingJobAPI:
        return self.get_api_by_resource(PAIRestResourceTypes.TrainingJob)

    @property
    def pipeline_api(self) -> PipelineAPI:
        return self.get_api_by_resource(PAIRestResourceTypes.Pipeline)

    @property
    def pipeline_run_api(self) -> PipelineRunAPI:
        return self.get_api_by_resource(PAIRestResourceTypes.PipelineRun)

    @property
    def experiment_api(self) -> ExperimentAPI:
        return self.get_api_by_resource(PAIRestResourceTypes.Experiment)
