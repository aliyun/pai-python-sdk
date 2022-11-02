import logging
import time
from typing import Any, Dict, List

from pai.common import ProviderAlibabaPAI
from pai.core import Session
from pai.decorator import config_default_session
from pai.entity.algorithm import Algorithm, AlgorithmSpec
from pai.entity.base import EntityBaseMixin
from pai.exception import UnExpectedStatusException
from pai.schema.training_job_schema import TrainingJobSchema

logger = logging.getLogger(__name__)

TRAINING_JOB_URL_PATTERN = "https://pai.console.aliyun.com/?regionId={region_id}&workspaceId={workspace_id}#/training/jobs/{job_id}/configs"


class TrainingJobStatus(object):
    # TODO: add more training job status
    InitializeFailed = "InitializeFailed"
    Succeed = "Succeed"
    Failed = "Failed"
    Terminated = "Terminated"

    @classmethod
    def is_completed_status(cls, status):
        return status in [
            cls.InitializeFailed,
            cls.Succeed,
            cls.Failed,
            cls.Terminated,
        ]

    @classmethod
    def is_failed_status(cls, status):
        return status in [
            cls.InitializeFailed,
            cls.Failed,
            cls.Terminated,
        ]


class TrainingJobMetric(object):
    def __init__(self, name, timestamp, value):
        self.name = name
        self.timestamp = timestamp
        self.value = value


class TrainingJobChannel(object):
    def __init__(self, dataset_id=None, input_uri=None, name=None):
        self.dataset_id = dataset_id
        self.input_uri = input_uri
        self.name = name


class TrainingJob(EntityBaseMixin):
    _schema_cls = TrainingJobSchema

    @config_default_session
    def __init__(
        self,
        algorithm_name=None,
        algorithm_version="1.0.0",
        algorithm_provider=ProviderAlibabaPAI,
        hyperparameters: Dict[str, Any] = None,
        job_name: str = None,
        instance_type: str = None,
        instance_count: int = None,
        output_config: List[Dict[str, str]] = None,
        input_config: List[Dict[str, str]] = None,
        labels: Dict[str, str] = None,
        max_running_time_in_seconds: int = None,
        description: str = None,
        session: Session = None,
        **kwargs,
    ):
        super(TrainingJob, self).__init__(session=session, **kwargs)
        self.algorithm_name = algorithm_name
        self.algorithm_version = algorithm_version
        self.algorithm_provider = algorithm_provider
        self.job_name = job_name
        self.description = description
        self.labels = labels
        self.hyperparameters = hyperparameters
        self.input_config = input_config
        self.output_config = output_config
        self.instance_type = instance_type
        self.instance_count = instance_count
        self.max_running_time_in_seconds = max_running_time_in_seconds
        algorithm_spec = self._get_algorithm_spec()
        if not algorithm_spec:
            raise ValueError(
                "Specific algorithm not found: algorithm_name={} algorithm_version={}, algorithm_provider={}".format(
                    algorithm_name, algorithm_version, algorithm_provider
                )
            )
        self.algorithm_spec = algorithm_spec

        # Load only fields
        self.create_time = kwargs.pop("create_time", None)
        self.modified_time = kwargs.pop("modified_time", None)
        self.reason_code = kwargs.pop("reason_code", None)
        self.reason_message = kwargs.pop("reason_message", None)
        self.status = kwargs.pop("status", None)
        self.status_transitions = kwargs.pop("status_transitions", None)
        self.job_id = kwargs.pop("job_id", None)

    @property
    def id(self):
        return self.job_id

    @classmethod
    @config_default_session
    def get(cls, training_job_id, session: Session = None) -> "TrainingJob":
        res = session.training_job_api.get(training_job_id=training_job_id)
        return cls.from_api_object(res, session=session)

    def _get_algorithm_spec(self) -> AlgorithmSpec:
        algo = Algorithm.get_by_name(self.algorithm_name, self.algorithm_provider)
        algorithm_version = algo.get_version(self.algorithm_version)
        return algorithm_version.algorithm_spec if algorithm_version else None

    def run(self, wait=False):
        job_id = self.session.training_job_api.create(
            instance_count=self.instance_count,
            instance_type=self.instance_type,
            job_name=self.job_name,
            hyperparameters=self.hyperparameters,
            input_channels=self.input_config,
            output_channels=self.output_config,
            labels=self.labels,
            max_running_in_seconds=self.max_running_time_in_seconds,
            description=self.description,
            algorithm_name=self.algorithm_name,
            algorithm_version=self.algorithm_version,
            algorithm_provider=self.algorithm_provider,
        )
        self.job_id = job_id
        print("TrainingJob console URL: {}".format(self.console_uri))
        if wait:
            self.wait_for_completion()
        self.session.training_job_api.refresh_entity(self.job_id, self)
        return job_id

    @property
    def console_uri(self):
        if not self.job_id:
            raise ValueError("The TrainingJob is not submitted")

        return TRAINING_JOB_URL_PATTERN.format(
            region_id=self.session.region_id,
            workspace_id=self.session.workspace_id,
            job_id=self.job_id,
        )

    def wait_for_completion(self, interval=5):
        self.session.training_job_api.refresh_entity(self.job_id, self)
        while not TrainingJobStatus.is_completed_status(self.status):
            time.sleep(interval)
            self.session.training_job_api.refresh_entity(self.job_id, self)

        self._on_job_completed()

    def _on_job_completed(self):
        if self.status == TrainingJobStatus.Succeed:
            return
        elif TrainingJobStatus.is_failed_status(self.status):
            raise UnExpectedStatusException(
                message="TrainingJob failed: training_job_id={} reason_code={} reason_message={}".format(
                    self.job_id, self.reason_code, self.reason_message
                ),
                status=self.status,
            )
