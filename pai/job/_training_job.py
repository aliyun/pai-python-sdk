#  Copyright 2024 Alibaba, Inc. or its affiliates.
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

import os
import posixpath
import time
import typing
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_pascal
from Tea.exceptions import TeaException

from ..api.base import PaginatedResult
from ..common.consts import StoragePathCategory
from ..common.logging import get_logger
from ..common.oss_utils import OssUriObj, is_oss_uri, upload
from ..common.utils import (
    is_dataset_id,
    is_filesystem_uri,
    is_odps_table_uri,
    name_from_base,
    print_table,
    random_str,
    retry,
    to_plain_text,
)
from ..exception import UnexpectedStatusException
from ..session import Session, get_default_session

if typing.TYPE_CHECKING:
    from ..estimator import FileSystemInputBase

logger = get_logger(__name__)


def as_oss_dir_uri(uri: str):
    return uri if uri.endswith("/") else uri + "/"


DEFAULT_OUTPUT_MODEL_CHANNEL_NAME = "model"
DEFAULT_CHECKPOINT_CHANNEL_NAME = "checkpoints"
DEFAULT_TENSORBOARD_CHANNEL_NAME = "tensorboard"


class SpotStrategy(str, Enum):
    SpotWithPriceLimit = "SpotWithPriceLimit"
    SpotAsPriceGo = "SpotAsPriceGo"

    def __repr__(self):
        return self.value


class ResourceType(str, Enum):
    Lingjun = "Lingjun"
    General = "General"


class BaseAPIModel(BaseModel):

    model_config = ConfigDict(
        alias_generator=to_pascal,
        populate_by_name=True,
    )

    def model_dump(self, **kwargs) -> Dict[str, Any]:
        kwargs.update({"by_alias": True, "exclude_none": True})
        return super().model_dump(**kwargs)

    def to_dict(self):
        return self.model_dump()


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


class UserVpcConfig(BaseAPIModel):
    """UserVpcConfig represents the VPC configuration for the training job instance."""

    vpc_id: str = Field(
        ...,
        description="Specifies the ID of the VPC that training job instance connects to.",
    )
    security_group_id: str = Field(
        ...,
        description="The ID of the security group that training job instances belong to.",
    )
    switch_id: Optional[str] = Field(
        None,
        description="The ID of the vSwitch to which the instance belongs. Defaults to None.",
    )
    extended_cidrs: Optional[List[str]] = Field(
        None,
        description="The CIDR blocks configured for the ENI of the training job instance. "
        "If it is not specified, the CIDR block will be configured as the same as the VPC "
        "network segmentation, which means that the training job instance can access all "
        "resources in the VPC. Defaults to None.",
    )


class ExperimentConfig(BaseAPIModel):
    """ExperimentConfig is used to configure the experiment to which the job belongs."""

    experiment_id: str = Field(
        ...,
        description="Specifies the ID of the experiment that training job instance belongs to.",
    )


class OssLocation(BaseAPIModel):
    """OSS location."""

    bucket: str = Field(..., description="OSS bucket name.")
    key: str = Field(..., description="Object key in the OSS bucket.")
    endpoint: Optional[str] = Field(None, description="OSS service endpoint URL.")


class CodeDir(BaseAPIModel):
    """Source code location"""

    location_value: Union[OssLocation, Dict[str, Any]] = Field(
        ..., description="Location of the code directory."
    )
    location_type: str = Field(
        ..., description="Type of the code directory location, e.g., OSS."
    )


# HyperParameter
class HyperParameter(BaseAPIModel):
    """A hyperparameter for a training job."""

    value: str = Field(..., description="Value of the hyperparameter.")
    name: str = Field(..., description="Name of the hyperparameter.")


class InstanceSpec(BaseAPIModel):
    """Instance resource configuration"""

    memory: str = Field(..., description="Memory allocation for the instance.")
    cpu: str = Field(..., alias="CPU", description="CPU allocation for the instance.")
    gpu: str = Field(..., alias="GPU", description="GPU allocation for the instance.")
    shared_memory: Optional[str] = Field(
        None, description="Shared memory allocation, if applicable."
    )


class ComputeResource(BaseAPIModel):
    """Compute Resource Configuration."""

    ecs_count: Optional[int] = Field(None, description="Number of ECS instances.")
    ecs_spec: Optional[str] = Field(None, description="Specification of ECS instances.")
    instance_count: Optional[int] = Field(None, description="Number of instances.")
    instance_spec: Optional[InstanceSpec] = Field(
        None, description="Specification for instances."
    )


# URI Input and Output
class UriInput(BaseAPIModel):
    """URI Input for a training job."""

    name: str = Field(..., description="Name of the input.")
    input_uri: str = Field(..., description="URI of the input data.")


class UriOutput(BaseAPIModel):
    """URI Output for a training job."""

    name: str = Field(..., description="Name of the output.")
    output_uri: str = Field(..., description="URI of the output data.")


class DatasetConfig(BaseAPIModel):
    """Dataset Configuration"""

    dataset_id: str = Field(..., description="Unique ID of the dataset.")
    name: Optional[str] = Field(None, description="Name of the dataset.")
    dataset_name: Optional[str] = Field(
        None, description="Alternative name of the dataset."
    )


class Channel(BaseAPIModel):
    """Channel Configuration."""

    name: str = Field(..., description="Name of the channel.")
    description: Optional[str] = Field(None, description="Description of the channel.")
    required: Optional[bool] = Field(
        None, description="Indicates if the channel is required."
    )
    supported_channel_types: Optional[List[str]] = Field(
        None, description="Supported types for this channel."
    )
    properties: Optional[Dict[str, Any]] = Field(
        None, description="Additional properties of the channel."
    )


# HyperParameter Definition
class HyperParameterDefinition(BaseAPIModel):
    """HyerParameter Definition."""

    name: str = Field(..., description="Name of the hyperparameter.")
    type: Optional[str] = Field(None, description="Type of the hyperparameter.")
    default_value: Optional[str] = Field(
        None, description="Default value of the hyperparameter."
    )
    description: Optional[str] = Field(
        None, description="Description of the hyperparameter."
    )
    required: bool = Field(
        False, description="Indicates if the hyperparameter is required."
    )


class SchedulerConfig(BaseAPIModel):
    max_running_time_in_seconds: Optional[int] = None


class MetricDefinition(BaseAPIModel):
    description: Optional[str] = Field(None, description="Description of the metric.")
    name: str = Field(..., description="Name of the metric.")
    regex: str = Field(
        ..., description="Regular expression used for capturing the metric."
    )


class AlgorithmSpec(BaseAPIModel):
    """Algorithm Specification."""

    command: List[str] = Field(..., description="Command to run the training job.")
    image: str = Field(..., description="Docker image for the training job.")
    supported_channel_types: List[str] = Field(default_factory=list)
    output_channels: List[Channel] = Field(
        default_factory=list, description="Output channels."
    )
    input_channels: List[Channel] = Field(
        default_factory=list, description="Input channels."
    )
    supports_distributed_training: Optional[bool] = Field(
        True, description="Whether the algorithm supports distributed training."
    )
    supported_instance_types: Optional[List[str]] = Field(
        None, description="Supported instance types."
    )
    metric_definitions: Optional[List[MetricDefinition]] = Field(
        None, description="Metric definitions."
    )
    hyperparameter_definitions: List[HyperParameterDefinition] = Field(
        default_factory=list,
        alias="HyperParameters",
        description="Hyperparameter definitions.",
    )
    job_type: str = Field(default="PyTorchJob")
    code_dir: Optional[CodeDir] = Field(None, description="Source code location.")
    customization: Optional[Dict[str, Any]] = Field(
        None, description="Whether the algorithm supports customize code."
    )


class ModelRecipeSpec(BaseAPIModel):
    compute_resource: Optional[ComputeResource] = None
    hyperparameters: List[HyperParameter] = Field(
        default_factory=list, alias="HyperParameters"
    )
    inputs: List[Union[UriInput, DatasetConfig]] = Field(
        default_factory=list, alias="InputChannels"
    )
    scheduler: Optional[SchedulerConfig] = None
    supported_instance_types: Optional[List[str]] = None
    algorithm_spec: Optional[AlgorithmSpec] = None
    algorithm_version: Optional[str] = None
    algorithm_provider: Optional[str] = None
    algorithm_name: Optional[str] = None
    environments: Optional[Dict[str, str]] = None
    requirements: Optional[List[str]] = None


class SpotSpec(BaseAPIModel):
    spot_strategy: SpotStrategy = Field(
        ...,
        description="Spot instance strategy, support 'SpotWithPriceLimit', 'SpotAsPriceGo'",
    )
    spot_discount_limit: Optional[float] = Field(
        None,
        description="Spot instance discount limit, maximum 2 decimal places, "
        "required when spot_strategy is 'SpotWithPriceLimit'."
        "For example, 0.5 means 50% off the original price.",
    )


class TrainingJob(BaseAPIModel):
    """TrainingJob represents a training job in the PAI service."""

    algorithm_id: Optional[str] = None
    algorithm_name: Optional[str] = None
    algorithm_provider: Optional[str] = None
    algorithm_version: Optional[str] = None
    algorithm_spec: Optional[AlgorithmSpec] = None
    compute_resource: Optional[ComputeResource] = None
    scheduler: Optional[SchedulerConfig] = None
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
    reason_code: Optional[str] = None
    reason_message: Optional[str] = None

    def __hash__(self):
        return hash(self.training_job_id)

    def __eq__(self, other: "TrainingJob"):
        return (
            isinstance(other, TrainingJob)
            and self.training_job_id == other.training_job_id
        )

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
        status: Optional[str] = None,
        session: Optional[Session] = None,
        page_size: int = 50,
        page_number: int = 1,
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

    def wait(self, interval: int = 5, show_logs: bool = True):
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

    def __init__(
        self,
        base_job_name: Optional[str] = None,
        output_path: Optional[str] = None,
        experiment_config: Optional[ExperimentConfig] = None,
        user_vpc_config: Optional[UserVpcConfig] = None,
        max_run_time: Optional[int] = None,
        instance_type: Optional[str] = None,
        instance_spec: Optional[Dict] = None,
        instance_count: Optional[int] = None,
        resource_id: Optional[Dict] = None,
        resource_type: Optional[Union[str, ResourceType]] = None,
        spot_spec: Optional[SpotSpec] = None,
        environments: Optional[Dict] = None,
        requirements: Optional[List[str]] = None,
        labels: Optional[Dict[str, str]] = None,
        settings: Optional[Dict[str, Any]] = None,
    ):
        self.session = get_default_session()
        self._training_jobs = []
        self.base_job_name = base_job_name or type(self).__name__.lower()
        self.output_path = output_path
        self.user_vpc_config = user_vpc_config
        self.spot_spec = spot_spec
        self.experiment_config = experiment_config
        self.max_run_time = max_run_time
        self.instance_type = instance_type
        self.instance_spec = instance_spec
        self.instance_count = instance_count or 1
        self.resource_id = resource_id
        self.resource_type = ResourceType(resource_type) if resource_type else None
        self.environments = environments
        self.requirements = requirements
        self.settings = settings
        self.labels = labels

    def wait(self, interval: int = 5, show_logs: bool = True, all_jobs: bool = False):
        """Block until the jobs is completed.

        Args:
            interval(int): Interval to reload job status
            show_logs(bool): Specifies whether to fetch and print the logs produced by
                the job.
            all_jobs(bool): Wait latest job or wait all jobs in processor, show_logs disabled while
                wait all jobs.

        Raises:
            RuntimeError: If no job is submitted.

        """
        if all_jobs:
            if not self._training_jobs:
                raise RuntimeError("Could not find any submitted job.")
            remains = set(self._training_jobs)
            while remains:
                for job in self._training_jobs:
                    if job in remains and job.is_completed():
                        remains.remove(job)

                time.sleep(interval)
            self._generate_jobs_report()
        else:
            latest_job = self.latest_job
            if not latest_job:
                raise RuntimeError("Could not find a submitted job.")
            latest_job.wait(interval=interval, show_logs=show_logs)
            return latest_job

    def _generate_jobs_report(self):
        """Generate current jobs report and output to stdout"""
        print(f"Jobs status report, total jobs count: {len(self._training_jobs)}")
        rows = []
        headers = ["JobName", "JobID", "Status"]
        for job in self._training_jobs:
            rows.append([job.training_job_name, job.id, job.status])
        print_table(headers, rows)

    def job_name(self, job_name: Optional[str] = None):
        if job_name:
            return job_name
        sep = "-"
        base_name = self.base_job_name
        return name_from_base(base_name, sep)

    def build_inputs(
        self,
        inputs: Dict[str, Any],
        input_channels: List[Channel],
        default_inputs: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, str]]:
        res = []
        inputs = inputs or dict()
        input_channels = input_channels or []
        default_inputs = default_inputs or {}

        inputs = {**default_inputs, **inputs}
        requires = {ch.name for ch in input_channels if ch.required} - set(
            inputs.keys()
        )
        if requires:
            raise ValueError(
                "Required input channels are not provided: {}".format(
                    ",".join(requires)
                )
            )
        for name, item in inputs.items():
            input_config = self._get_input_config(name, item)
            res.append(input_config.model_dump())

        return res

    @staticmethod
    def _default_training_output_channels() -> List[Channel]:
        channels = [
            Channel(
                name=DEFAULT_OUTPUT_MODEL_CHANNEL_NAME,
                description="Training output models",
                required=True,
            ),
            Channel(
                name=DEFAULT_CHECKPOINT_CHANNEL_NAME,
                description="Training checkpoints channel",
                required=False,
            ),
            Channel(
                name=DEFAULT_TENSORBOARD_CHANNEL_NAME,
                properties={"ossAppendable": "true"},
                description="TensorBoard logs channel",
                required=False,
            ),
        ]

        return channels

    def _training_job_base_output(self, job_name):
        job_name = to_plain_text(job_name)
        if self.output_path:
            if not is_oss_uri(self.output_path):
                raise ValueError("Output path should be an OSS path.")
            return os.path.join(self.output_path, f"{job_name}_{random_str(6)}")

        session = get_default_session()
        bucket_name = session.oss_bucket.bucket_name
        storage_path = session.get_storage_path_by_category(
            StoragePathCategory.TrainingJob,
            f"{to_plain_text(job_name)}_{random_str(6)}",
        )
        base_output_path = (
            f"oss://{bucket_name}.{session.oss_endpoint}/"
            f"{storage_path}"
        )
        return base_output_path

    def build_outputs(
        self,
        job_name: str,
        output_channels: List[Channel],
        outputs: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, str]]:
        base_output_path = self._training_job_base_output(job_name)
        res = []
        outputs = outputs or dict()

        for ch in output_channels:
            if ch.name in outputs:
                output = self._get_output_config(name=ch.name, item=outputs[ch.name])
            else:
                output_uri = as_oss_dir_uri(posixpath.join(base_output_path, ch.name))
                output = UriOutput(name=ch.name, output_uri=output_uri)
            res.append(output)

        extra_outputs = set(outputs.keys()) - {ch.name for ch in output_channels}

        for name in extra_outputs:
            output = self._get_output_config(
                name=name,
                item=outputs[name],
            )
            res.append(output)

        return [item.model_dump() for item in res]

    # TODO: get arguments, such as VPCConfig, instance_type etc, from self instance.
    def _submit(
        self,
        job_name: str,
        algorithm_spec: Optional[AlgorithmSpec] = None,
        algorithm_name: Optional[str] = None,
        algorithm_version: Optional[str] = None,
        algorithm_provider: Optional[str] = None,
        instance_count: int = 1,
        instance_type: Optional[str] = None,
        instance_spec: Optional[InstanceSpec] = None,
        resource_id: Optional[str] = None,
        inputs: Optional[List[Dict[str, Any]]] = None,
        outputs: Optional[List[Dict[str, Any]]] = None,
        hyperparameters: Optional[Dict[str, str]] = None,
        max_run_time: Optional[int] = None,
        environments: Optional[Dict[str, str]] = None,
        user_vpc_config: Optional[Dict[str, str]] = None,
        requirements: Optional[List[str]] = None,
        experiment_config: Optional[Dict[str, Any]] = None,
        labels: Optional[Dict[str, str]] = None,
        wait: bool = True,
        show_logs: bool = False,
    ):
        session = get_default_session()

        if not self.resource_type or self.resource_type == ResourceType.General:
            resource_type = None
        else:
            resource_type = self.resource_type.value

        if self.spot_spec:
            spot_spec = {
                "SpotStrategy": self.spot_spec.spot_strategy.value,
            }
            if self.spot_spec.spot_discount_limit:
                spot_spec["SpotDiscountLimit"] = self.spot_spec.spot_discount_limit
        else:
            spot_spec = None

        # user vpc
        if self.user_vpc_config:
            user_vpc_config = {
                "VpcId": self.user_vpc_config.vpc_id,
                "SecurityGroupId": self.user_vpc_config.security_group_id,
            }
        else:
            user_vpc_config = None

        training_job_id = session.training_job_api.create(
            instance_count=instance_count,
            instance_spec=instance_spec.model_dump() if instance_spec else None,
            algorithm_name=algorithm_name,
            algorithm_provider=algorithm_provider,
            experiment_config=(
                experiment_config.model_dump()
                if experiment_config and isinstance(experiment_config, ExperimentConfig)
                else experiment_config
            ),
            spot_spec=spot_spec,
            algorithm_version=algorithm_version,
            instance_type=instance_type,
            resource_id=resource_id,
            resource_type=resource_type,
            job_name=job_name,
            hyperparameters=hyperparameters,
            max_running_in_seconds=max_run_time,
            input_channels=inputs,
            output_channels=outputs,
            algorithm_spec=algorithm_spec.model_dump() if algorithm_spec else None,
            requirements=requirements,
            user_vpc_config=user_vpc_config,
            labels=labels,
            environments=environments,
            settings=self.settings,
        )
        training_job = TrainingJob.get(training_job_id)
        self._training_jobs.append(training_job)
        print(
            f"View the job detail by accessing the console URI: {training_job.console_uri}"
        )
        if wait:
            training_job.wait(show_logs=show_logs)
        return training_job

    @classmethod
    def _get_input_config(
        cls, name: str, item: Union[str, "FileSystemInputBase", DatasetConfig]
    ) -> Union[UriInput, DatasetConfig]:
        """Get input uri for training_job from given input."""
        from pai.estimator import FileSystemInputBase

        if not isinstance(item, (str, FileSystemInputBase, DatasetConfig)):
            raise ValueError(f"Input data of type {type(item)} is not supported.")

        if isinstance(item, FileSystemInputBase):
            input_ = UriInput(
                name=name,
                input_uri=item.to_input_uri(),
            )
        elif isinstance(item, DatasetConfig):
            input_ = DatasetConfig(
                name=name,
                dataset_id=item.dataset_id,
            )
        elif is_oss_uri(item) or is_filesystem_uri(item) or is_odps_table_uri(item):
            input_ = UriInput(
                name=name,
                input_uri=item,
            )
        elif isinstance(item, str):
            if os.path.exists(item):
                store_path = Session.get_storage_path_by_category(
                    StoragePathCategory.InputData
                )
                input_ = UriInput(name=name, input_uri=upload(item, store_path))
            else:
                raise ValueError("Invalid input data path, file not found: {item}.")
        else:
            raise ValueError(
                f"Invalid input data, supported inputs are OSS, NAS, MaxCompute "
                f"table or local path: {type(item)}."
            )
        return input_

    @classmethod
    def _get_output_config(
        cls, name: str, item: str
    ) -> Union[UriOutput, DatasetConfig]:
        from pai.estimator import FileSystemInputBase

        if not isinstance(item, (str, FileSystemInputBase, DatasetConfig)):
            raise ValueError(f"Output data of type {type(item)} is not supported.")

        if isinstance(item, FileSystemInputBase):
            output = UriOutput(
                name=name,
                output_uri=item.to_input_uri(),
            )
        elif isinstance(item, DatasetConfig):
            output = DatasetConfig(name=name, dataset_id=item.dataset_id)
        elif is_oss_uri(item) or is_filesystem_uri(item) or is_odps_table_uri(item):
            output = UriOutput(
                name=name,
                output_uri=as_oss_dir_uri(item),
            )
        else:
            raise ValueError(
                "Invalid output data, supported outputs are OSS, NAS, MaxCompute "
            )

        return output

    @property
    def latest_job(self) -> "TrainingJob":
        return self._training_jobs[-1] if self._training_jobs else None

    def _build_code_input(
        self, job_name: str, source_dir: Optional[str], code_dest: Optional[str] = None
    ) -> Optional[CodeDir]:
        """Upload source files to OSS and return the code input for training job."""
        if not source_dir:
            return
        if is_oss_uri(source_dir):
            code_uri = source_dir
        elif not os.path.exists(source_dir):
            raise ValueError(f"Source directory {source_dir} does not exist.")
        else:
            code_dest = code_dest or self.session.get_storage_path_by_category(
                StoragePathCategory.TrainingSrc, to_plain_text(job_name)
            )
            code_uri = upload(
                source_path=source_dir,
                oss_path=code_dest,
                bucket=self.session.oss_bucket,
                is_tar=True,
            )
        oss_uri_obj = OssUriObj(uri=self.session.patch_oss_endpoint(code_uri))
        code_dir = CodeDir(
            location_type="oss",
            location_value=OssLocation(
                bucket=oss_uri_obj.bucket_name,
                key=oss_uri_obj.object_key,
                endpoint=oss_uri_obj.endpoint,
            ),
        )

        return code_dir
