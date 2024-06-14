import os
import posixpath
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_pascal
from Tea.exceptions import TeaException

from ..api.base import PaginatedResult
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
from ..session import Session, get_default_session

logger = get_logger(__name__)


class BaseAPIModel(BaseModel):

    model_config = ConfigDict(
        alias_generator=to_pascal,
        populate_by_name=True,
    )

    def model_dump(self, **kwargs) -> Dict[str, Any]:
        kwargs.update({"by_alias": True, "exclude_none": True})
        return super().model_dump(**kwargs)


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


class OssLocation(BaseAPIModel):
    bucket: str
    key: str
    endpoint: Optional[str]


class CodeDir(BaseAPIModel):
    location_value: Union[OssLocation, Dict[str, Any]]
    location_type: str


class HyperParameter(BaseAPIModel):
    value: str
    name: str


class InstanceSpec(BaseAPIModel):
    memory: str
    cpu: str = Field(alias="CPU")
    gpu: str = Field(alias="GPU")
    shared_memory: Optional[str] = None


class ComputeResource(BaseAPIModel):
    ecs_count: Optional[int] = None
    ecs_spec: Optional[str] = None
    instance_count: Optional[int] = None
    instance_spec: Optional[InstanceSpec] = None


class UriInput(BaseAPIModel):
    name: str
    input_uri: str


class UriOutput(BaseAPIModel):
    name: str
    output_uri: str


class DatasetConfig(BaseAPIModel):
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
    inputs: List[Union[UriInput, DatasetConfig]] = Field(
        default_factory=list, alias="InputChannels"
    )
    algorithm_spec: Optional[AlgorithmSpec] = None
    algorithm_version: Optional[str] = None
    algorithm_provider: Optional[str] = None
    algorithm_name: Optional[str] = None


class TrainingJob(BaseAPIModel):
    """TrainingJob represents a training job in the PAI service."""

    algorithm_id: Optional[str] = None
    algorithm_name: Optional[str] = None
    algorithm_provider: Optional[str] = None
    algorithm_version: Optional[str] = None
    algorithm_spec: Optional[AlgorithmSpec] = None
    compute_resource: Optional[ComputeResource] = None
    experiment_config: Optional[Dict[str, Any]] = None
    inputs: List[Union[UriInput, DatasetConfig]] = Field(
        default=list, alias="InputChannels"
    )
    outputs: List[Union[UriOutput, DatasetConfig]] = Field(
        default=list, alias="OutputChannels"
    )
    hyperparameters: List[HyperParameter] = Field(
        default_factory=list, alias="HyperParameters"
    )
    labels: Optional[List[Dict[str, str]]] = Field(default_factory=list)
    training_job_description: Optional[str] = None
    training_job_id: Optional[str] = None
    training_job_name: Optional[str] = None
    workspace_id: Optional[str] = None
    training_job_url: Optional[str] = None
    status: Optional[str] = None

    @property
    def id(self):
        return self.training_job_id

    @classmethod
    def get(cls, training_job_id, session: Session = None) -> "TrainingJob":
        session = session or get_default_session()
        res = session.training_job_api.get(training_job_id=training_job_id)
        return cls.model_validate(res)

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
        return [cls.model_validate(item) for item in res.items]

    def output_path(self, channel_name="model"):
        for output_channel in self.outputs:
            if output_channel.name == channel_name:
                return output_channel.output_uri
        raise RuntimeError(
            f"Output channel is not specified: channel_name={channel_name}"
        )

    @property
    def console_uri(self):
        if not self.training_job_id:
            raise ValueError("The TrainingJob is not submitted")

        return self.training_job_url

    def wait(self, interval=2, show_logs: bool = True):
        session = get_default_session()
        self._refresh_status()

        if show_logs:
            job_log_printer = _TrainingJobLogPrinter(
                training_job_id=self.training_job_id, page_size=20, session=session
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

    def _refresh_status(self):
        """Reload the training job from the PAI Service,"""
        session = get_default_session()
        training_job = type(self).model_validate(
            session.training_job_api.get(training_job_id=self.training_job_id)
        )
        self.status = training_job.status

    def is_succeeded(self):
        """Return True if the training job is succeeded"""
        self._refresh_status()
        return self.status == TrainingJobStatus.Succeed

    @retry(wait_secs=10)
    def is_completed(self):
        """Return True if the training job is completed, including failed status"""
        if self.status in TrainingJobStatus.completed_status():
            return True
        self._refresh_status()

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


class _TrainingJobSubmitter(object):
    """A class used to submit a training job to the PAI service."""

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
        extra_inputs: List[Union[DatasetConfig, UriInput]] = None,
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
            res.append(input_config.model_dump())

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
        instance_spec: Optional[InstanceSpec] = None,
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
            instance_spec=instance_spec.model_dump() if instance_spec else None,
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

    @classmethod
    def _get_input_config(cls, name: str, item: str):
        """Get input uri for training_job from given input."""
        from pai.estimator import FileSystemInputBase

        if not isinstance(item, (str, FileSystemInputBase)):
            raise ValueError(f"Input data of type {type(item)} is not supported.")

        if isinstance(item, FileSystemInputBase):
            input_ = UriInput(
                name=name,
                input_uri=item.to_input_uri(),
            )
        elif is_oss_uri(item) or is_filesystem_uri(item) or is_odps_table_uri(item):
            input_ = UriInput(
                name=name,
                input_uri=item,
            )
        elif os.path.exists(item):
            store_path = Session.get_storage_path_by_category(
                StoragePathCategory.InputData
            )
            input_ = UriInput(name=name, input_uri=upload(item, store_path))
        elif is_dataset_id(item):
            input_ = DatasetConfig(
                dataset_id=item,
                name=name,
            )
        else:
            raise ValueError(
                "Invalid input data, supported inputs are OSS, NAS, MaxCompute "
                "table or local path."
            )
        return input_

    @property
    def latest_job(self) -> "TrainingJob":
        return self._training_jobs[-1] if self._training_jobs else None
