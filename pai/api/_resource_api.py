from __future__ import absolute_import

from pai.api.algorithm_api import AlgorithmAPI
from pai.api.client_factory import ClientFactory
from pai.api.code_source_api import CodeSourceAPI
from pai.api.dataset_api import DatasetAPI
from pai.api.image_api import ImageAPI
from pai.api.job_api import JobAPI
from pai.api.model_api import ModelAPI
from pai.api.pipeline_api import PipelineAPI
from pai.api.pipeline_run_api import PipelineRunAPI
from pai.api.service_api import ServiceAPI
from pai.api.training_job_api import TrainingJobAPI
from pai.api.workspace_api import WorkspaceAPI
from pai.common.consts import PAIRestResourceTypes, PAIServiceName


class ResourceAPIsContainerMixin(object):
    """ResourceAPIsMixin provide resource operation API."""

    _access_key_id = None
    _access_key_secret = None
    _security_token = None
    _region_id = None
    _workspace_id = None

    def __init__(self):
        self._api_container = dict()
        self._job_api = None
        self._acs_client_container = dict()

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

        self._acs_client_container[PAIServiceName.PAIFLOW] = paiflow_client

        dlc_client = ClientFactory.create_client(
            service_name=PAIServiceName.PAI_DLC,
            access_key_id=self._access_key_id,
            access_key_secret=self._access_key_secret,
            security_token=self._security_token,
            region_id=self._region_id,
        )
        self._acs_client_container[PAIServiceName.PAI_DLC] = dlc_client

        ws_client = ClientFactory.create_client(
            service_name=PAIServiceName.AIWORKSPACE,
            access_key_id=self._access_key_id,
            access_key_secret=self._access_key_secret,
            security_token=self._security_token,
            region_id=self._region_id,
        )
        self._acs_client_container[PAIServiceName.AIWORKSPACE] = ws_client

        eas_client = ClientFactory.create_client(
            service_name=PAIServiceName.PAI_EAS,
            access_key_id=self._access_key_id,
            access_key_secret=self._access_key_secret,
            security_token=self._security_token,
            region_id=self._region_id,
        )
        self._acs_client_container[PAIServiceName.PAI_EAS] = eas_client

        training_service_client = ClientFactory.create_client(
            service_name=PAIServiceName.TRAINING_SERVICE,
            access_key_id=self._access_key_id,
            access_key_secret=self._access_key_secret,
            security_token=self._security_token,
            region_id=self._region_id,
        )

        self._acs_client_container[
            PAIServiceName.TRAINING_SERVICE
        ] = training_service_client

    @property
    def _acs_workspace_client(self):
        return self._acs_client_container[PAIServiceName.AIWORKSPACE]

    @property
    def _acs_dlc_client(self):
        return self._acs_client_container[PAIServiceName.PAI_DLC]

    @property
    def _acs_paiflow_client(self):
        return self._acs_client_container[PAIServiceName.PAIFLOW]

    @property
    def _acs_eas_client(self):
        return self._acs_client_container[PAIServiceName.PAI_EAS]

    @property
    def _acs_training_client(self):
        return self._acs_client_container[PAIServiceName.TRAINING_SERVICE]

    def _initialize_apis(self):
        """Initialize resource operation APIs."""

        self._job_api = JobAPI(
            self._workspace_id,
            self._acs_dlc_client,
        )
        self._api_container[PAIRestResourceTypes.DlcJob] = self._job_api

        self._code_source_api = CodeSourceAPI(
            self._workspace_id,
            self._acs_workspace_client,
        )
        self._api_container[PAIRestResourceTypes.CodeSource] = self._code_source_api

        self._dataset_api = DatasetAPI(
            self._workspace_id,
            self._acs_workspace_client,
        )
        self._api_container[PAIRestResourceTypes.Dataset] = self._dataset_api

        self._image_api = ImageAPI(
            self._workspace_id,
            self._acs_workspace_client,
        )
        self._api_container[PAIRestResourceTypes.Image] = self._image_api

        self._service_api = ServiceAPI(
            region_id=self._region_id, acs_client=self._acs_eas_client
        )
        self._api_container[PAIRestResourceTypes.EasService] = self._service_api

        self._model_api = ModelAPI(
            self._workspace_id,
            self._acs_workspace_client,
        )
        self._api_container[PAIRestResourceTypes.Model] = self._model_api

        self._workspace_api = WorkspaceAPI(
            acs_client=self._acs_workspace_client,
        )
        self._api_container[PAIRestResourceTypes.Workspace] = self._workspace_api

        self._algorithm_api = AlgorithmAPI(
            workspace_id=self._workspace_id,
            acs_client=self._acs_training_client,
        )

        self._training_job_api = TrainingJobAPI(
            workspace_id=self._workspace_id,
            acs_client=self._acs_training_client,
        )

        self._pipeline_api = PipelineAPI(
            workspace_id=self._workspace_id,
            acs_client=self._acs_paiflow_client,
        )
        self._pipeline_run_api = PipelineRunAPI(
            workspace_id=self._workspace_id,
            acs_client=self._acs_paiflow_client,
        )

    def get_api_by_resource(self, resource_type):
        return self._api_container[resource_type]

    @property
    def job_api(self) -> JobAPI:
        """Returns JobAPI for job operation."""
        return self._job_api

    @property
    def code_source_api(self) -> CodeSourceAPI:
        """Return CodeSource API for code_source operation"""
        return self._code_source_api

    @property
    def dataset_api(self) -> DatasetAPI:
        """Return Dataset API for dataset operation"""
        return self._dataset_api

    @property
    def image_api(self) -> ImageAPI:
        return self._image_api

    @property
    def model_api(self) -> ModelAPI:
        return self._model_api

    @property
    def service_api(self) -> ServiceAPI:
        """

        Returns:

        """
        return self._service_api

    @property
    def workspace_api(self) -> WorkspaceAPI:
        return self._workspace_api

    @property
    def algorithm_api(self) -> AlgorithmAPI:
        return self._algorithm_api

    @property
    def training_job_api(self) -> TrainingJobAPI:
        return self._training_job_api

    @property
    def pipeline_api(self) -> PipelineAPI:
        return self._pipeline_api

    @property
    def pipeline_run_api(self) -> PipelineRunAPI:
        return self._pipeline_run_api
