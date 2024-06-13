import os
import posixpath
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_pascal
from Tea.exceptions import TeaException

from ..api.base import PaginatedResult
from ..api.entity_base import EntityBaseMixin
from ..common import ProviderAlibabaPAI
from ..common.consts import StoragePathCategory
from ..common.logging import get_logger
from ..common.oss_utils import is_oss_uri, upload
from ..common.utils import (
    is_dataset_id,
    is_filesystem_uri,
    is_odps_table_uri,
    name_from_base,
    random_str,
    retry,
    to_plain_text,
)
from ..exception import UnexpectedStatusException
from ..schema.training_job_schema import TrainingJobSchema
from ..session import Session, get_default_session

logger = get_logger(__name__)


class TrainingJob(EntityBaseMixin):
    _schema_cls = TrainingJobSchema

    def __init__(
        self,
        algorithm_name=None,
        algorithm_version="1.0.0",
        algorithm_provider=ProviderAlibabaPAI,
        hyperparameters: Dict[str, Any] = None,
        training_job_name: str = None,
        instance_type: str = None,
        instance_count: int = None,
        output_channels: List[Dict[str, str]] = None,
        input_channels: List[Dict[str, str]] = None,
        labels: Dict[str, str] = None,
        max_running_time_in_seconds: int = None,
        experiment_config: Dict[str, str] = None,
        description: str = None,
        session: Session = None,
        **kwargs,
    ):
        super(TrainingJob, self).__init__(session=session, **kwargs)
        self.algorithm_name = algorithm_name
        self.algorithm_version = algorithm_version
        self.algorithm_provider = algorithm_provider
        self.training_job_name = training_job_name
        self.description = description
        self.labels = labels
        self.hyperparameters = hyperparameters
        self.input_channels = input_channels
        self.output_channels = output_channels
        self.instance_type = instance_type
        self.instance_count = instance_count
        self.max_running_time_in_seconds = max_running_time_in_seconds
        self.experiment_config = experiment_config

        # Load only fields
        self.create_time = kwargs.pop("create_time", None)
        self.modified_time = kwargs.pop("modified_time", None)
        self.reason_code = kwargs.pop("reason_code", None)
        self.reason_message = kwargs.pop("reason_message", None)
        self.status = kwargs.pop("status", None)
        self.status_transitions = kwargs.pop("status_transitions", None)
        self.training_job_id = kwargs.pop("training_job_id", None)
        self.training_job_url = kwargs.pop("training_job_url", None)

    def __repr__(self):
        return "TrainingJob(id={})".format(self.training_job_id)

    def __str__(self):
        return self.__repr__()

    @property
    def id(self):
        return self.training_job_id

    @classmethod
    def get(cls, training_job_id, session: Session = None) -> "TrainingJob":
        session = session or get_default_session()
        res = session.training_job_api.get(training_job_id=training_job_id)
        return cls.from_api_object(res, session=session)

    @classmethod
    def list(
        cls,
        status=None,
        session: Session = None,
        page_size=50,
        page_number=1,
    ):
        session = session or get_default_session()
        res = session.training_job_api.list(
            status=status, page_size=page_size, page_number=page_number
        )
        return [cls.from_api_object(item, session=session) for item in res.items]

    def output_path(self, channel_name="model"):
        for output_channel in self.output_channels:
            if output_channel["Name"] == channel_name:
                return output_channel["OutputUri"]
        raise RuntimeError(
            f"Output channel is not specified: channel_name={channel_name}"
        )

    @property
    def console_uri(self):
        if not self.training_job_id:
            raise ValueError("The TrainingJob is not submitted")

        return self.training_job_url

    def wait(self, interval=2, show_logs: bool = True):
        self.session.training_job_api.refresh_entity(self.training_job_id, self)

        if show_logs:
            job_log_printer = _TrainingJobLogPrinter(
                training_job_id=self.training_job_id, page_size=20, session=self.session
            )
            job_log_printer.start()
        else:
            job_log_printer = None
        try:
            while not self.is_completed():
                time.sleep(interval)
        finally:
            if job_log_printer:
                job_log_printer.stop(wait=True)

        self._on_job_completed()

    def _on_job_completed(self):
        # Print an empty line to separate the training job logs and the following logs
        print()
        if self.status == TrainingJobStatus.Succeed:
            print(
                f"Training job ({self.training_job_id}) succeeded, you can check the"
                f" logs/metrics/output in  the console:\n{self.console_uri}"
            )
        elif self.status == TrainingJobStatus.Terminated:
            print(
                f"Training job is ended with status {self.status}: "
                f"reason_code={self.reason_code}, reason_message={self.reason_message}."
                f"Check the training job in the console:\n{self.console_uri}"
            )
        elif self.status in TrainingJobStatus.failed_status():
            print(
                f"Training job ({self.training_job_id}) failed, please check the logs"
                f" in the console: \n{self.console_uri}"
            )

            message = f"TrainingJob failed: name={self.training_job_name}, "
            f"training_job_id={self.training_job_id}, "
            f"reason_code={self.reason_code}, status={self.status}, "
            f"reason_message={self.reason_message}"

            raise UnexpectedStatusException(message=message, status=self.status)

    def _reload(self):
        """Reload the training job from the PAI Service,"""
        self.session.training_job_api.refresh_entity(self.training_job_id, self)

    def is_succeeded(self):
        """Return True if the training job is succeeded"""
        self._reload()
        return self.status == TrainingJobStatus.Succeed

    @retry(wait_secs=10)
    def is_completed(self):
        """Return True if the training job is completed, including failed status"""
        if self.status in TrainingJobStatus.completed_status():
            return True
        self._reload()

        return self.status in TrainingJobStatus.completed_status()


class _TrainingJobLogPrinter(object):
    """A class used to print logs for a training job"""

    executor = ThreadPoolExecutor(5)

    def __init__(
        self, training_job_id: str, page_size=10, session: Optional[Session] = None
    ):
        self.training_job_id = training_job_id
        self.session = session
        self.page_size = page_size
        self._future = None
        self._stop = False

    def _list_logs_api(self, page_number: int = 1):
        try:
            res = self.session.training_job_api.list_logs(
                self.training_job_id,
                page_number=page_number,
                page_size=self.page_size,
            )
            return res
        except TeaException as e:
            # hack: Backend service may raise an exception when the training job
            # instance is not found.
            if e.code == "TRAINING_JOB_INSTANCE_NOT_FOUND":
                return PaginatedResult(items=[], total_count=0)
            else:
                raise e

    def _list_logs(self):
        page_number, page_offset = 1, 0
        # print training job logs.
        while not self._stop:
            res = self._list_logs_api(page_number=page_number)
            # 1. move to next page
            if len(res.items) == self.page_size:
                # print new logs starting from page_offset
                self._print_logs(logs=res.items[page_offset:])
                page_number += 1
                page_offset = 0
            # 2. stay at the current page.
            else:
                if len(res.items) > page_offset:
                    # print new logs starting from page_offset
                    self._print_logs(logs=res.items[page_offset:])
                    page_offset = len(res.items)
                time.sleep(1)

        # When _stop is True, wait and print remaining logs.
        time.sleep(10)
        while True:
            res = self._list_logs_api(page_number=page_number)
            # There maybe more logs in the next page
            if len(res.items) == self.page_size:
                self._print_logs(logs=res.items[page_offset:])
                page_number += 1
                page_offset = 0
            # No more logs in the next page.
            else:
                if len(res.items) > page_offset:
                    self._print_logs(logs=res.items[page_offset:])
                break

    def _print_logs(self, logs: List[str]):
        for log in logs:
            print(log)

    def start(self):
        if self._future:
            raise ValueError("The training job log printer is already started")
        self._stop = False
        self._future = self.executor.submit(self._list_logs)

    def stop(self, wait: bool = True):
        self._stop = True
        if self._future:
            self._future.result()


class TrainingJobStatus(object):
    CreateFailed = "CreateFailed"
    InitializeFailed = "InitializeFailed"
    Succeed = "Succeed"
    Failed = "Failed"
    Terminated = "Terminated"
    Creating = "Creating"
    Created = "Created"
    Initializing = "Initializing"
    Submitted = "Submitted"
    Running = "Running"

    @classmethod
    def completed_status(cls):
        return [
            cls.InitializeFailed,
            cls.Succeed,
            cls.Failed,
            cls.Terminated,
        ]

    @classmethod
    def failed_status(cls):
        return [
            cls.InitializeFailed,
            cls.Failed,
            cls.CreateFailed,
        ]


class BaseAPIModel(BaseModel):

    model_config = ConfigDict(
        alias_generator=to_pascal,
        populate_by_name=True,
    )

    def model_dump(self, **kwargs) -> Dict[str, Any]:
        kwargs.update({"by_alias": True, "exclude_none": True})
        return super().model_dump(**kwargs)


class OssLocation(BaseAPIModel):
    bucket: str
    key: str
    endpoint: Optional[str]


class CodeDir(BaseAPIModel):
    location_value: Union[OssLocation, Dict[str, Any]]
    location_type: str


class HyperParameter(BaseAPIModel):
    value: str
    Name: str


class InstanceSpec(BaseAPIModel):
    memory: str
    cpu: str = Field(alias="CPU")
    gpu: str = Field(alias="GPU")
    shared_memory: Optional[str] = None


class ComputeResource(BaseAPIModel):
    ecs_count: int
    ecs_spec: str
    instance_count: int
    instance_spec: Optional[InstanceSpec] = None


class UriInput(BaseAPIModel):
    name: str
    uri: str = Field(alias="InputUri")


class DatasetInput(BaseAPIModel):
    name: str
    dataset_id: str
    dataset_name: Optional[str] = None


class Channel(BaseAPIModel):
    name: str
    description: Optional[str] = None
    required: Optional[bool] = None
    supported_channel_types: Optional[List[str]] = None
    properties: Optional[Dict[str, Any]] = None


class AlgorithmSpec(BaseAPIModel):
    command: List[str]
    image: str
    supported_channel_types: List[str] = Field(default_factory=list)
    output_channels: List[Channel] = Field(default_factory=list)
    input_channels: List[Channel] = Field(default_factory=list)
    supports_distributed_training: bool = False
    metric_definitions: List = Field(default_factory=list)
    hyperparameter_definitions: List[Dict[str, Any]] = Field(
        default_factory=list, alias="HyperParameter"
    )
    job_type: Literal["PyTorchJob"] = Field(default="PyTorchJob")
    code_dir: Optional[CodeDir] = None


class TrainingJobSpec(BaseAPIModel):
    compute_resource: ComputeResource
    hyperparameters: List[HyperParameter] = Field(
        default_factory=list, alias="HyperParameters"
    )
    inputs: List[Union[UriInput, DatasetInput]] = Field(
        default_factory=list, alias="InputChannels"
    )
    algorithm_spec: Optional[AlgorithmSpec] = None
    algorithm_version: Optional[str] = None
    algorithm_provider: Optional[str] = None
    algorithm_name: Optional[str] = None


class _TrainingJobSubmitter(object):
    def __init__(self):
        self.session = get_default_session()
        self._training_jobs = []

    def base_job_name(self):
        return type(self).__name__.lower()

    def job_name(self, job_name: Optional[str] = None):
        if job_name:
            return job_name
        sep = "-"
        base_name = self.base_job_name()
        return name_from_base(base_name, sep)

    def build_inputs(
        self,
        inputs: Dict[str, Any],
        input_channels: List[Channel],
        extra_inputs: List[Union[DatasetInput, UriInput]] = None,
    ) -> List[Dict[str, str]]:
        res = []
        inputs = inputs or dict()
        input_channels = input_channels or []
        extra_inputs = extra_inputs or []

        input_keys = set(list(inputs.keys()) + [item.name for item in extra_inputs])

        requires = {ch.name for ch in input_channels if ch.required} - input_keys
        if requires:
            raise ValueError(
                "Required input channels are not provided: {}".format(
                    ",".join(requires)
                )
            )
        more = input_keys - {ch.name for ch in input_channels}
        if more:
            logger.warning(
                "Following input channels are not defined in the algorithm spec: %s",
                ",".join(more),
            )

        for name, item in inputs.items():
            input_config = self._get_input_config(name, item)
            res.append(input_config)

        for item in extra_inputs:
            res.append(item.model_dump())

        return res

    @classmethod
    def training_job_base_output(cls, job_name):
        session = get_default_session()
        bucket_name = session.oss_bucket.bucket_name
        storage_path = session.get_storage_path_by_category(
            StoragePathCategory.TrainingJob,
            f"{to_plain_text(job_name)}_{random_str(6)}",
        )
        base_output_path = f"oss://{bucket_name}/{storage_path}"
        return base_output_path

    def build_outputs(
        self, job_name: str, output_channels: List[Channel]
    ) -> List[Dict[str, str]]:
        base_output_path = self.training_job_base_output(job_name)

        def as_oss_dir_uri(uri: str):
            return uri if uri.endswith("/") else uri + "/"

        res = []
        for ch in output_channels:
            # if checkpoint path is provided, use it as the checkpoint channel output.
            output_uri = as_oss_dir_uri(posixpath.join(base_output_path, ch.name))
            res.append(
                {
                    "Name": ch.name,
                    "OutputUri": output_uri,
                }
            )
        return res

    def _submit(
        self,
        job_name: str,
        algorithm_spec: AlgorithmSpec,
        instance_count: int = 1,
        instance_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        inputs: Optional[List[Dict[str, Any]]] = None,
        outputs: Optional[List[Dict[str, Any]]] = None,
        hyperparameters: Optional[Dict[str, str]] = None,
        max_run_time: Optional[int] = None,
        user_vpc_config: Optional[Dict[str, str]] = None,
        labels: Optional[Dict[str, str]] = None,
        wait: bool = True,
    ):
        session = get_default_session()
        training_job_id = session.training_job_api.create(
            instance_count=instance_count,
            # instance_spec=self.instance_spec,
            instance_type=instance_type,
            resource_id=resource_id,
            job_name=job_name,
            hyperparameters=hyperparameters,
            max_running_in_seconds=max_run_time,
            input_channels=inputs,
            output_channels=outputs,
            algorithm_spec=algorithm_spec.model_dump(),
            # experiment_config=
            user_vpc_config=user_vpc_config,
            labels=labels,
        )
        training_job = TrainingJob.get(training_job_id)
        self._training_jobs.append(training_job)
        print(
            f"View the job detail by accessing the console URI: {training_job.console_uri}"
        )
        if wait:
            training_job.wait()

    def _get_input_config(self, name: str, item: str):
        """Get input uri for training_job from given input."""
        from pai.estimator import FileSystemInputBase

        if not isinstance(item, (str, FileSystemInputBase)):
            raise ValueError(f"Input data of type {type(item)} is not supported.")

        if isinstance(item, FileSystemInputBase):
            config = {"InputUri": item.to_input_uri()}
        elif is_oss_uri(item) or is_filesystem_uri(item) or is_odps_table_uri(item):
            config = {"InputUri": item}
        elif os.path.exists(item):
            store_path = Session.get_storage_path_by_category(
                StoragePathCategory.InputData
            )
            config = {"InputUri": upload(item, store_path)}
        elif is_dataset_id(item):
            config = {"DatasetId": item}
        else:
            raise ValueError(
                "Invalid input data, supported inputs are OSS, NAS, MaxCompute "
                "table or local path."
            )
        config.update({"Name": name})

        return config

    @property
    def latest_job(self) -> "TrainingJob":
        return self._training_jobs[-1] if self._training_jobs else None
