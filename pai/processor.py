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
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from .common.consts import JobType, StoragePathCategory
from .common.logging import get_logger
from .common.utils import experimental, random_str, to_plain_text
from .job import (
    AlgorithmSpec,
    Channel,
    CodeDir,
    ExperimentConfig,
    SpotSpec,
    TrainingJob,
    UriOutput,
    UserVpcConfig,
    _TrainingJobSubmitter,
)
from .job._training_job import ResourceType
from .session import Session, get_default_session

logger = get_logger(__name__)


@experimental
class Processor(_TrainingJobSubmitter):
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
        spot_spec: Optional[SpotSpec] = None,
        resource_type: Optional[Union[str, ResourceType]] = None,
        instance_count: Optional[int] = None,
        user_vpc_config: Optional[UserVpcConfig] = None,
        experiment_config: Optional[ExperimentConfig] = None,
        settings: Optional[Dict[str, Any]] = None,
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
            resource_type (str, optional): The resource type used to run the training job.
                By default, general computing resource is used. If the resource_type is
                'Lingjun', Lingjun computing resource is used.
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
            settings (dict, optional): A dictionary that represents the additional settings
                for job, such as AIMaster configurations.
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
        self.session = session or get_default_session()

        self._input_channels = None
        self._output_channels = None
        super().__init__(
            resource_type=resource_type,
            spot_spec=spot_spec,
            base_job_name=base_job_name,
            output_path=output_path,
            experiment_config=experiment_config,
            instance_type=instance_type,
            instance_count=instance_count or 1,
            user_vpc_config=user_vpc_config,
            max_run_time=max_run_time,
            environments=environments,
            requirements=requirements,
            labels=labels,
            settings=settings,
        )

    def run(
        self,
        inputs: Dict[str, Any] = None,
        outputs: Dict[str, Any] = None,
        wait: bool = True,
        show_logs: bool = True,
    ) -> TrainingJob:
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
            show_logs (bool): Whether to show the logs of the job. Default to True.
                Note that the logs will be shown only when the `wait` is set to True.

        Returns:
            :class:`pai.job.TrainingJob`: A submitted training job.

        Raises:
            UnExpectedStatusException: If the job fails.

        """
        inputs = inputs or dict()
        outputs = outputs or dict()
        job_name = self._gen_job_display_name()

        code_dest = Session.get_storage_path_by_category(
            StoragePathCategory.ProcessingSrc, to_plain_text(job_name)
        )
        code_dir = self._build_code_input(job_name, self.source_dir, code_dest)
        algo_spec = self._build_algorithm_spec(
            code_input=code_dir,
        )
        inputs = self.build_inputs(inputs, input_channels=algo_spec.input_channels)
        outputs = self.build_outputs(
            job_name=job_name,
            output_channels=algo_spec.output_channels,
            outputs=outputs,
        )

        return self._submit(
            instance_count=self.instance_count,
            instance_type=self.instance_type,
            job_name=job_name,
            hyperparameters=self.parameters,
            environments=self.environments,
            requirements=self.requirements,
            max_run_time=self.max_run_time,
            inputs=inputs,
            outputs=outputs,
            algorithm_spec=algo_spec,
            user_vpc_config=(
                self.user_vpc_config.model_dump() if self.user_vpc_config else None
            ),
            experiment_config=(
                self.experiment_config.model_dump() if self.experiment_config else None
            ),
            labels=self.labels,
            wait=wait,
            show_logs=show_logs,
        )

    def _gen_job_display_name(self, job_name=None):
        """Generate job display name."""
        if job_name:
            return job_name
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        return "{}_{}".format(self.base_job_name or "processing_job", ts)

    def _build_algorithm_spec(self, code_input: CodeDir) -> AlgorithmSpec:
        """Build a temporary AlgorithmSpec used for submitting the Job."""

        algorithm_spec = AlgorithmSpec(
            command=(
                self.command
                if isinstance(self.command, list)
                else [
                    "sh",
                    "-c",
                    self.command,
                ]
            ),
            image=self.image_uri,
            job_type=self.job_type,
            code_dir=code_input,
            input_channels=self._input_channels or [],
            output_channels=self._output_channels or [],
        )
        return algorithm_spec

    def _training_job_base_output(self, job_name: str) -> str:
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

    def get_outputs_data(self) -> Dict[str, str]:
        """Show all outputs data paths.

        Returns:
            dict[str, str]: A dictionary of all outputs data paths.
        """
        if not self.latest_job:
            raise RuntimeError("Current no Job for the processor.")

        return {
            ch.name: ch.output_uri if isinstance(ch, UriOutput) else ch.dataset_id
            for ch in self.latest_job.outputs
        }

    def set_input_channels(self, channels: List[Channel]):
        self._input_channels = channels

    def set_output_channels(self, channels: List[Channel]):
        self._output_channels = channels
