from __future__ import absolute_import

from pai.api.algorithm import AlgorithmAPI
from pai.api.base import PAIRestResourceTypes, PAIServiceName
from pai.api.client_factory import ClientFactory
from pai.api.code_source import CodeSourceAPI
from pai.api.dataset import DatasetAPI
from pai.api.image import ImageAPI
from pai.api.job import JobAPI
from pai.api.model import ModelAPI
from pai.api.pipeline import PipelineAPI
from pai.api.pipeline_run import PipelineRunAPI
from pai.api.service import ServiceAPI
from pai.api.training_job import TrainingJobAPI
from pai.api.workspace import WorkspaceAPI


class ResourceAPIsContainerMixin(object):
    """ResourceAPIsContainerMixin provides Resource Operation APIs."""

    _access_key_id = None
    _access_key_secret = None
    _security_token = None
    _region_id = None
    _workspace_id = None

    def __init__(self, header=None, runtime=None):
        self.header = header
        self.runtime = runtime
        self.api_container = dict()
        self.acs_client_container = dict()
        self._initialize_clients()
        self._initialize_apis()

    def _initialize_clients(self):
        """Initialize AlibabaCloud Service Client."""
        paiflow_client = ClientFactory.create_client(
            service_name=PAIServiceName.PAIFLOW,
            access_key_id=self._access_key_id,
            access_key_secret=self._access_key_secret,
            security_token=self._security_token,
            region_id=self._region_id,
        )

        self.acs_client_container[PAIServiceName.PAIFLOW] = paiflow_client

        dlc_client = ClientFactory.create_client(
            service_name=PAIServiceName.PAI_DLC,
            access_key_id=self._access_key_id,
            access_key_secret=self._access_key_secret,
            security_token=self._security_token,
            region_id=self._region_id,
        )
        self.acs_client_container[PAIServiceName.PAI_DLC] = dlc_client

        ws_client = ClientFactory.create_client(
            service_name=PAIServiceName.AIWORKSPACE,
            access_key_id=self._access_key_id,
            access_key_secret=self._access_key_secret,
            security_token=self._security_token,
            region_id=self._region_id,
        )
        self.acs_client_container[PAIServiceName.AIWORKSPACE] = ws_client

        eas_client = ClientFactory.create_client(
            service_name=PAIServiceName.PAI_EAS,
            access_key_id=self._access_key_id,
            access_key_secret=self._access_key_secret,
            security_token=self._security_token,
            region_id=self._region_id,
        )
        self.acs_client_container[PAIServiceName.PAI_EAS] = eas_client

        training_service_client = ClientFactory.create_client(
            service_name=PAIServiceName.TRAINING_SERVICE,
            access_key_id=self._access_key_id,
            access_key_secret=self._access_key_secret,
            security_token=self._security_token,
            region_id=self._region_id,
        )

        self.acs_client_container[
            PAIServiceName.TRAINING_SERVICE
        ] = training_service_client

    @property
    def _acs_workspace_client(self):
        return self.acs_client_container[PAIServiceName.AIWORKSPACE]

    @property
    def _acs_dlc_client(self):
        return self.acs_client_container[PAIServiceName.PAI_DLC]

    @property
    def _acs_paiflow_client(self):
        return self.acs_client_container[PAIServiceName.PAIFLOW]

    @property
    def _acs_eas_client(self):
        return self.acs_client_container[PAIServiceName.PAI_EAS]

    @property
    def _acs_training_client(self):
        return self.acs_client_container[PAIServiceName.TRAINING_SERVICE]

    def _initialize_apis(self):
        """Initialize resource operation APIs."""

        self.api_container[PAIRestResourceTypes.DlcJob] = JobAPI(
            self._workspace_id,
            self._acs_dlc_client,
            header=self.header,
            runtime=self.runtime,
        )
        self.api_container[PAIRestResourceTypes.CodeSource] = CodeSourceAPI(
            self._workspace_id,
            self._acs_workspace_client,
            header=self.header,
            runtime=self.runtime,
        )
        self.api_container[PAIRestResourceTypes.Dataset] = DatasetAPI(
            self._workspace_id,
            self._acs_workspace_client,
            header=self.header,
            runtime=self.runtime,
        )
        self.api_container[PAIRestResourceTypes.Image] = ImageAPI(
            self._workspace_id,
            self._acs_workspace_client,
            header=self.header,
            runtime=self.runtime,
        )

        self.api_container[PAIRestResourceTypes.Service] = ServiceAPI(
            region_id=self._region_id,
            acs_client=self._acs_eas_client,
            header=self.header,
            runtime=self.runtime,
        )

        self.api_container[PAIRestResourceTypes.Model] = ModelAPI(
            self._workspace_id,
            self._acs_workspace_client,
            header=self.header,
            runtime=self.runtime,
        )

        self.api_container[PAIRestResourceTypes.Workspace] = WorkspaceAPI(
            acs_client=self._acs_workspace_client,
            header=self.header,
            runtime=self.runtime,
        )

        self.api_container[PAIRestResourceTypes.Algorithm] = AlgorithmAPI(
            workspace_id=self._workspace_id,
            acs_client=self._acs_training_client,
            header=self.header,
            runtime=self.runtime,
        )
        self.api_container[PAIRestResourceTypes.TrainingJob] = TrainingJobAPI(
            workspace_id=self._workspace_id,
            acs_client=self._acs_training_client,
            header=self.header,
            runtime=self.runtime,
        )

        self.api_container[PAIRestResourceTypes.Pipeline] = PipelineAPI(
            workspace_id=self._workspace_id,
            acs_client=self._acs_paiflow_client,
            header=self.header,
            runtime=self.runtime,
        )

        self.api_container[PAIRestResourceTypes.PipelineRun] = PipelineRunAPI(
            workspace_id=self._workspace_id,
            acs_client=self._acs_paiflow_client,
            header=self.header,
            runtime=self.runtime,
        )

    def get_api_by_resource(self, resource_type):
        return self.api_container[resource_type]

    @property
    def job_api(self) -> JobAPI:
        """Returns JobAPI for job operation."""
        return self.api_container[PAIRestResourceTypes.DlcJob]

    @property
    def code_source_api(self) -> CodeSourceAPI:
        """Return CodeSource API for code_source operation"""
        return self.api_container[PAIRestResourceTypes.CodeSource]

    @property
    def dataset_api(self) -> DatasetAPI:
        """Return Dataset API for dataset operation"""
        return self.api_container[PAIRestResourceTypes.Dataset]

    @property
    def image_api(self) -> ImageAPI:
        return self.api_container[PAIRestResourceTypes.Image]

    @property
    def model_api(self) -> ModelAPI:
        return self.api_container[PAIRestResourceTypes.Model]

    @property
    def service_api(self) -> ServiceAPI:
        """"""
        return self.api_container[PAIRestResourceTypes.Service]

    @property
    def workspace_api(self) -> WorkspaceAPI:
        return self.api_container[PAIRestResourceTypes.Workspace]

    @property
    def algorithm_api(self) -> AlgorithmAPI:
        return self.api_container[PAIRestResourceTypes.Algorithm]

    @property
    def training_job_api(self) -> TrainingJobAPI:
        return self.api_container[PAIRestResourceTypes.TrainingJob]

    @property
    def pipeline_api(self) -> PipelineAPI:
        return self.api_container[PAIRestResourceTypes.Pipeline]

    @property
    def pipeline_run_api(self) -> PipelineRunAPI:
        return self.api_container[PAIRestResourceTypes.PipelineRun]
