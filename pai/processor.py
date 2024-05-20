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
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from .common.configs import UserVpcConfig
from .common.consts import JobType, StoragePathCategory
from .common.logging import get_logger
from .common.oss_utils import OssUriObj, is_oss_uri, upload
from .common.utils import (
    experimental,
    is_dataset_id,
    is_filesystem_uri,
    is_odps_table_uri,
    random_str,
    to_plain_text,
)
from .estimator import FileSystemInputBase
from .estimator import _TrainingJob as _Job
from .experiment import ExperimentConfig
from .session import Session, get_default_session

logger = get_logger(__name__)


def build_code_input(
    source_dir: str, upload_data_path: str
) -> Optional[Dict[str, Any]]:
    """Upload local code and build CodeDir config for job."""
    if not source_dir:
        return

    from pai.session import get_default_session

    sess = get_default_session()

    if is_oss_uri(source_dir):
        code_oss_uri = source_dir
    elif os.path.exists(source_dir):
        code_oss_uri = upload(
            source_path=source_dir,
            oss_path=upload_data_path,
            bucket=sess.oss_bucket,
            is_tar=True,
        )
    else:
        raise ValueError(f"Source directory {source_dir} does not exist.")

    code_oss_obj = OssUriObj(uri=sess.patch_oss_endpoint(code_oss_uri))
    res = {
        "LocationType": "oss",
        "LocationValue": {
            "Bucket": code_oss_obj.bucket_name,
            "Key": code_oss_obj.object_key,
            "Endpoint": code_oss_obj.endpoint,
        },
    }

    return res


def get_input_channel_config(
    item: Optional[Union[str, FileSystemInputBase]]
) -> Dict[str, str]:
    """Get channel config from given job input."""

    if not isinstance(item, (str, FileSystemInputBase)):
        raise ValueError(f"Input data of type {type(item)} is not supported.")

    if isinstance(item, FileSystemInputBase):
        config = {"InputUri": item.to_input_uri()}
    elif is_oss_uri(item) or is_filesystem_uri(item) or is_odps_table_uri(item):
        config = {"InputUri": item}
    elif is_dataset_id(item):
        config = {"DatasetId": item}
    elif os.path.exists(item):
        store_path = Session.get_storage_path_by_category(StoragePathCategory.InputData)
        config = {"InputUri": upload(item, store_path)}
    else:
        raise ValueError(
            "Invalid input data, supported inputs are OSS, NAS, MaxCompute "
            "table or local path."
        )

    return config


def get_output_channel_config(
    item: Optional[Union[str, FileSystemInputBase]]
) -> Dict[str, str]:
    """Get channel config from given job output."""

    if not isinstance(item, (str, FileSystemInputBase)):
        raise ValueError(f"Output data of type {type(item)} is not supported.")

    # OSS URI for output channel will be mounted to directory
    # "/ml/output/{ChannelName}/" and the output OSS URI should be a "directory"
    def as_oss_dir_uri(uri: str):
        folder_uri = uri if uri.endswith("/") else uri + "/"
        if folder_uri != uri:
            logger.warning(
                f"This output URI {uri} is not in the format of a folder path, "
                f"system will automatically use {folder_uri} instead."
            )
        return folder_uri

    if isinstance(item, FileSystemInputBase):
        config = {"OutputUri": item.to_input_uri()}
    elif is_oss_uri(item):
        config = {"OutputUri": as_oss_dir_uri(item)}
    elif is_filesystem_uri(item) or is_odps_table_uri(item):
        config = {"OutputUri": item}
    elif is_dataset_id(item):
        config = {"DatasetId": item}
    else:
        raise ValueError(
            "Invalid output data, supported inputs are OSS, NAS, MaxCompute table."
        )

    return config


@experimental
class Processor(object):
    def __init__(
        self,
        image_uri: str,
        command: Union[str, List[str]],
        source_dir: Optional[str] = None,
        job_type: str = JobType.PyTorchJob,
        parameters: Optional[Dict[str, Any]] = None,
        environments: Optional[Dict[str, str]] = None,
        requirements: Optional[List[str]] = None,
        max_run_time: Optional[int] = None,
        base_job_name: Optional[str] = None,
        output_path: Optional[str] = None,
        instance_type: Optional[str] = None,
        instance_count: Optional[int] = None,
        user_vpc_config: Optional[UserVpcConfig] = None,
        experiment_config: Optional[ExperimentConfig] = None,
        labels: Optional[Dict[str, str]] = None,
        session: Optional[Session] = None,
    ):
        """Processor constructor.

        Args:
            image_uri (str): The image used in the job. It can be an image
                provided by PAI or a user customized image. To view the images provided
                by PAI, please refer to the document:
                https://help.aliyun.com/document_detail/202834.htm.
            command (Union[str, List[str]): The command used to run the job.
            source_dir (str, optional): The local source code directory used in the
                job. The directory will be packaged and uploaded to an OSS
                bucket, then downloaded to the `/ml/usercode` directory in the
                job container. If there is a `requirements.txt` file in the source code
                directory, the corresponding dependencies will be installed before the
                script runs.

                If 'git_config' is provided, 'source_dir' should be a relative location
                to a directory in the Git repo. With the following GitHub repo directory
                structure:

                .. code::

                    |----- README.md
                    |----- src
                             |----- train.py
                             |----- test.py

                if you need 'src' directory as the source code directory, you can assign
                source_dir='./src/'.
            job_type (str): The type of job, which can be TFJob, PyTorchJob, XGBoostJob,
                etc. Default value is PyTorchJob.
            parameters (dict, optional): A dictionary that represents the
                parameters used in the job. The parameters will be
                stored in the `/ml/input/config/hyperparameters.json` as a JSON
                dictionary in the container.
            environments: A dictionary that maps environment variable names to their values.
                This optional field allows you to provide a set of environment variables that will be
                applied to the context where the code is executed.
            requirements (list, optional): An optional list of strings that specifies the Python
                package dependencies with their versions. Each string in the list should be in the format
                'package' or 'package==version'. This is similar to the contents of a requirements.txt file used
                in Python projects. If requirements.txt is provided in user code directory, requirements
                will override the conflict dependencies directly.
            max_run_time (int, optional): The maximum time in seconds that the
                job can run. The job will be terminated after the time is
                reached (Default None).
            base_job_name (str, optional): The base name used to generate the
                job name.
            output_path (str, optional): An OSS URI to store the outputs of the
                jobs. If not provided, an OSS URI will be generated using the default
                OSS bucket in the session. When the `estimator.fit` method is called,
                a specific OSS URI under the output_path for each channel is generated
                and mounted to the container.

                A completed container directory structure example::

                    /ml
                    |-- usercode            			// User source code directory.
                    |   |-- requirements.txt
                    |   `-- train.py
                    |-- input               			// Job input
                    |   `-- config
                    |       |-- hyperparameters.json	// Hyperparameters in JSON
                    |       |                           // dictionary format for the
                    |       |                           // Job
                    |       |
                    |   `-- data            			// Job input channels
                    |       |                           // `/ml/input/data/` is a input
                    |       |                           // channel, and the directory
                    |       |                           // name is the channel name.
                    |       |                           // Each directory under the
                    |       |-- test-data
                    |       |   `-- test.csv
                    |       `-- train-data
                    |           `-- train.csv
                    `-- output              			// Job output channels.
                            |                           // Each directory under the
                            |                           // `/ml/output/` is an output
                            |                           // channel, and the directory
                            |                           // name is the channel name.
                            `-- model
                            `-- checkpoints

            instance_type (str): The machine instance type used to run the job.
                To view the supported machine instance types, please refer to the
                document:
                https://help.aliyun.com/document_detail/171758.htm#section-55y-4tq-84y.
                If the instance_type is "local", the job is executed locally
                using docker.
            instance_count (int): The number of machines used to run the job.
            user_vpc_config (:class:`pai.estimator.UserVpcConfig`, optional): The VPC
                configuration used to enable the job instance to connect to the
                specified user VPC. If provided, an Elastic Network Interface (ENI) will
                be created and attached to the job instance, allowing the
                instance to access the resources within the specified VPC. Default to
                None.
            experiment_config(:class:`pai.estimator.ExperimentConfig`, optional): The
                experiment configuration used to construct the relationship between the
                job and the experiment. If provided, the training job will belong to the
                specified experiment, in which case the job will use artifact_uri of
                experiment as default output path. Default to None.
            labels (Dict[str, str], optional): A dictionary that maps label names to
                their values. This optional field allows you to provide a set of labels
                that will be applied to the training job.
            session (Session, optional): A PAI session instance used for communicating
                with PAI service.

        """
        self.image_uri = image_uri
        self.command = command
        self.source_dir = source_dir
        self.job_type = job_type or JobType.PyTorchJob
        self.parameters = parameters or dict()
        self.environments = environments
        self.requirements = requirements
        self.max_run_time = max_run_time

        self.base_job_name = base_job_name
        self.output_path = output_path

        self.instance_type = instance_type
        self.instance_count = instance_count or 1
        self.labels = labels
        self.user_vpc_config = user_vpc_config
        self.experiment_config = experiment_config
        self.session = session or get_default_session()

        self._latest_job = None
        self._jobs = []

        self._input_channel_definitions = None
        self._output_channel_definitions = None

    def run(
        self,
        inputs: Dict[str, Any] = None,
        outputs: Dict[str, Any] = None,
        wait: bool = True,
        show_logs=True,
    ):
        """Submit a job with the given input and output channels.

        Args:
            inputs (Dict[str, Any]): A dictionary representing the input data for the
                job. Each key/value pair in the dictionary is an input channel,
                the key is the channel name, and the value is the input data. The input
                data can be an OSS URI or a NAS URI object and will be mounted to the
                `/ml/input/data/{channel_name}` directory in the job container.
            outputs (Dict[str, Any]): A dictionary representing the output data for the
                job. Each key/value pair in the dictionary is an output channel,
                the key is the channel name, and the value is the output path. The output
                path can be an OSS URI or a NAS URI object and will be mounted to the
                `/ml/outputs/data/{channel_name}` directory in the job container.
            wait (bool): Specifies whether to block until the training job is completed,
                either succeeded, failed, or stopped. (Default True).
            show_logs (bool): Specifies whether to show the logs produced by the
                job (Default True).
        Raises:
            UnExpectedStatusException: If the job fails.

        """
        inputs = inputs or dict()
        outputs = outputs or dict()
        job_name = self._gen_job_display_name()

        job = self._fit(inputs=inputs, outputs=outputs, job_name=job_name)
        self._latest_job = job
        self._jobs.append(job)

        if wait:
            self.wait(show_logs=show_logs)

    def _gen_job_display_name(self, job_name=None):
        """Generate job display name."""
        if job_name:
            return job_name
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        return "{}_{}".format(self.base_job_name or "processing_job", ts)

    def _build_algorithm_spec(self, code_input) -> Dict[str, Any]:
        """Build a temporary AlgorithmSpec used for submitting the Job."""
        command = (
            self.command
            if isinstance(self.command, list)
            else [
                "/bin/sh",
                "-c",
                self.command,
            ]
        )

        algo_spec = {
            "Command": command,
            "Image": self.image_uri,
            "JobType": self.job_type,
            "CodeDir": code_input,
            "InputChannels": self._input_channel_definitions or None,
            "OutputChannels": self._output_channel_definitions or None,
        }

        return algo_spec

    def _fit(
        self, job_name, inputs: Dict[str, Any] = None, outputs: Dict[str, Any] = None
    ):
        output_path = self._get_job_base_output_path(job_name)
        upload_path = Session.get_storage_path_by_category(
            StoragePathCategory.ProcessingSrc, to_plain_text(job_name)
        )

        input_configs = self._build_input_data_configs(inputs)
        output_configs = self._build_output_data_configs(output_path, outputs)

        algo_spec = self._build_algorithm_spec(
            code_input=build_code_input(self.source_dir, upload_path),
        )

        job_id = self.session.training_job_api.create(
            instance_count=self.instance_count,
            instance_type=self.instance_type,
            job_name=job_name,
            hyperparameters=self.parameters,
            environments=self.environments,
            requirements=self.requirements,
            max_running_in_seconds=self.max_run_time,
            input_channels=input_configs,
            output_channels=output_configs,
            algorithm_spec=algo_spec,
            user_vpc_config=self.user_vpc_config.to_dict()
            if self.user_vpc_config
            else None,
            experiment_config=self.experiment_config.to_dict()
            if self.experiment_config
            else None,
            labels=self.labels,
        )
        job = _Job.get(job_id)
        print(f"View the job {job_id} by accessing the console URI: {job.console_uri}")
        return job

    def wait(self, interval: int = 2, show_logs: bool = True, all_jobs: bool = False):
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
            if not self._jobs:
                raise RuntimeError("Could not find any submitted job.")

            remains = set(self._jobs)
            while remains:
                for job in self._jobs:
                    if job in remains and job.is_completed():
                        remains.remove(job)

                time.sleep(interval)

            self._generate_jobs_report()
        else:
            if not self._latest_job:
                raise RuntimeError("Could not find a submitted job.")

            self._latest_job.wait(interval=interval, show_logs=show_logs)

    def _generate_jobs_report(self):
        """Generate current jobs report and output to stdout"""
        print(f"Jobs status report, total jobs count: {len(self._jobs)}")

        rows = []
        headers = ["JobName", "JobID", "Status"]
        for job in self._jobs:
            rows.append([job.training_job_name, job.id, job.status])

        column_widths = [
            max(len(str(value)) for value in column) for column in zip(headers, *rows)
        ]
        header_row = " | ".join(
            f"{header:<{column_widths[i]}}" for i, header in enumerate(headers)
        )

        print(header_row)
        print("-" * len(header_row))
        for row in rows:
            print(
                " | ".join(
                    f"{str(value):<{column_widths[i]}}" for i, value in enumerate(row)
                )
            )

    def _get_job_base_output_path(self, job_name: str) -> str:
        """Generate the base output path for the job."""

        bucket_name = self.session.oss_bucket.bucket_name
        # replace non-alphanumeric character in job name.
        job_name = to_plain_text(job_name)

        if self.output_path:
            return os.path.join(self.output_path, f"{job_name}_{random_str(6)}")

        job_output_path = Session.get_storage_path_by_category(
            StoragePathCategory.ProcessingJob, f"{job_name}_{random_str(6)}"
        )
        return f"oss://{bucket_name}/{job_output_path}"

    def _build_input_data_configs(
        self,
        inputs: Dict[str, Any] = None,
    ) -> List[Dict[str, str]]:
        """Build the input data config for jobs."""

        res = []
        remain_inputs = {}

        if self._input_channel_definitions:
            remains = set(inputs.keys())
            for channel in self._input_channel_definitions:
                channel_name = channel["Name"]
                channel_required = channel["Required"]
                channel_config = {"Name": channel_name}

                if channel_name in inputs:
                    updated_value = get_input_channel_config(inputs[channel_name])
                    channel_config.update(updated_value)
                    res.append(channel_config)
                    remains.remove(channel_name)
                elif channel_required:
                    raise ValueError(
                        f"Input channel {channel_name} is required but not provided."
                        " Please check the input channels definition."
                    )

            # follow the rest of user input channels in Processor.
            remain_inputs = {channel: inputs[channel] for channel in remains}

            if remains:
                logger.warning(
                    f"Following input channels={list(remains)} are not defined in input"
                    " channels definition. Please check the input channels definition."
                )

        for name, item in remain_inputs.items():
            channel_config = {"Name": name}
            updated_value = get_input_channel_config(item)
            channel_config.update(updated_value)
            res.append(channel_config)

        return res

    def _build_output_data_configs(
        self,
        output_path: str,
        outputs: Dict[str, Any] = None,
    ) -> List[Dict[str, str]]:
        """Build the output data config for jobs."""

        res = []

        if self._output_channel_definitions:
            # we create all channel config no matter whether channel is required or not for backward compatibility.
            for channel in self._output_channel_definitions:
                channel_name = channel["Name"]
                channel_config = {"Name": channel_name}

                if channel_name in outputs:
                    updated_value = get_output_channel_config(outputs[channel_name])
                    channel_config.update(updated_value)
                else:
                    output_uri = posixpath.join(output_path, channel["Name"])
                    updated_value = get_output_channel_config(output_uri)
                    channel_config.update(updated_value)

                res.append(channel_config)
        else:
            for name, item in outputs.items():
                channel_config = {"Name": name}
                updated_value = get_output_channel_config(item)
                channel_config.update(updated_value)

                res.append(channel_config)

        return res

    @property
    def latest_job(self):
        """Return the latest submitted processing job."""
        return self._latest_job

    def get_outputs_data(self) -> Dict[str, str]:
        """Show all outputs data paths.

        Returns:
            dict[str, str]: A dictionary of all outputs data paths.
        """
        if not self._latest_job:
            raise RuntimeError("Current no Job for the processor.")

        return {
            ch["Name"]: ch["OutputUri"] or ch["DatasetId"]
            for ch in self._latest_job.output_channels
        }

    def set_input_channel_definitions(self, definitions: List[Dict[str, Any]]):
        self._input_channel_definitions = definitions

    def set_output_channel_definitions(self, definitions: List[Dict[str, Any]]):
        self._output_channel_definitions = definitions
