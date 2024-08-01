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

import webbrowser
from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from .common import git_utils
from .common.consts import FileSystemInputScheme, JobType
from .common.logging import get_logger
from .common.utils import is_local_run_instance_type, make_list_resource_iterator
from .job import (
    AlgorithmSpec,
    Channel,
    HyperParameterDefinition,
    LocalTrainingJob,
    TrainingJob,
    UriOutput,
    _TrainingJobSubmitter,
)
from .job._training_job import (
    DEFAULT_CHECKPOINT_CHANNEL_NAME,
    DEFAULT_OUTPUT_MODEL_CHANNEL_NAME,
    DEFAULT_TENSORBOARD_CHANNEL_NAME,
    ExperimentConfig,
    ResourceType,
    SpotSpec,
    UserVpcConfig,
)
from .model import InferenceSpec, Model, ResourceConfig
from .predictor import Predictor
from .serializers import SerializerBase
from .session import Session, get_default_session

logger = get_logger(__name__)


class HyperParameterType(object):
    """Hyperparameter type."""

    INT = "Int"
    FLOAT = "Float"
    STRING = "String"
    BOOL = "Boolean"
    CHANNEL = "Channel"

    @classmethod
    def convert(
        cls,
        hp_value: Any,
        hp_type: str,
    ):
        """Convert hyperparameter value to the specified type."""
        if hp_type == cls.INT:
            hp_value = int(hp_value)
        elif hp_type == cls.FLOAT:
            hp_value = float(hp_value)
        return hp_value


class FileSystemInputBase(metaclass=ABCMeta):
    """Base class for FileSystemInput."""

    @abstractmethod
    def to_input_uri(self):
        pass


class FileSystemInput(FileSystemInputBase):
    """FileSystemInput is used to mount a Standard/Extreme NAS file system for a
    TrainingJob.

    Examples::

        est = Estimator(
            image_uri="<TrainingImageUri>",
            command="sh train.sh",
            instance_type="ecs.c6.xlarge",
        )

        est.fit({
            "input": FileSystemInput(
                file_system_id="<FileSystemId>",
                directory_path="/path/to/data/"),
        })

    """

    def __init__(self, file_system_id: str, directory_path: Optional[str] = None):
        self.file_system_id = file_system_id
        self.directory_path = (
            directory_path.lstrip("/")
            if directory_path and directory_path.startswith("/")
            else directory_path
        )

    def to_input_uri(self):
        """Convert FileSystemInput to input uri used for TrainingJob."""
        region_id = get_default_session().region_id
        return "{schema}://{file_system_id}.{region_id}/{directory}".format(
            schema=FileSystemInputScheme.NAS,
            file_system_id=self.file_system_id,
            region_id=region_id,
            directory=self.directory_path or "",
        )


class CpfsFileSystemInput(FileSystemInputBase):
    """CpfsFileSystemInput is used to mount a CPFS file system for a TrainingJob.

    More details about CPFS, please refer to documentation:
    https://help.aliyun.com/product/111536.html

    Examples::

        est = Estimator(
            image_uri="<TrainingImageUri>",
            command="sh train.sh",
            instance_type="ecs.c6.xlarge",
        )

        est.fit(
            inputs={"train": CpfsFileSystemInput(
                file_system_id="<FileSystemId>",
                protocol_service_id="<ProtocolServiceId>",
                export_id="<ExportId>",
            )},
        )

    """

    def __init__(self, file_system_id: str, protocol_service_id: str, export_id: str):
        """Initialize CpfsFileSystemInput.

        Args:
            file_system_id (str): CPFS file system id.
            protocol_service_id (str): CPFS protocol service id.
            export_id (str): CPFS export id.
        """

        self.file_system_id = file_system_id
        self.protocol_service_id = protocol_service_id
        self.export_id = export_id

    def to_input_uri(self):
        """Convert CpfsFileSystemInput instance to input uri used for TrainingJob."""
        region_id = get_default_session().region_id
        return (
            "{schema}://{file_system_id}.{region_id}/{protocol_service_id}/"
            "{export_id}/".format(
                schema=FileSystemInputScheme.CPFS,
                file_system_id=self.file_system_id,
                region_id=region_id,
                protocol_service_id=self.protocol_service_id,
                export_id=self.export_id,
            )
        )


class EstimatorBase(_TrainingJobSubmitter, metaclass=ABCMeta):
    """EstimatorBase is the base class for other Estimator classes, such as Estimator.

    The EstimatorBase class contains common attributes and methods for all estimators,
    such as the hyperparameters, instance type, instance count, etc. The EstimatorBase
    class is not intended to be used directly, please use the other Estimator classes
    instead.

    """

    def __init__(
        self,
        hyperparameters: Optional[Dict[str, Any]] = None,
        base_job_name: Optional[str] = None,
        max_run_time: Optional[int] = None,
        output_path: Optional[str] = None,
        checkpoints_path: Optional[str] = None,
        environments: Optional[Dict[str, str]] = None,
        requirements: Optional[List[str]] = None,
        instance_type: Optional[str] = None,
        spot_spec: Optional[SpotSpec] = None,
        instance_spec: Optional[Dict] = None,
        resource_id: Optional[Dict] = None,
        resource_type: Optional[Union[str, ResourceType]] = None,
        instance_count: Optional[int] = None,
        user_vpc_config: Optional[UserVpcConfig] = None,
        experiment_config: Optional[ExperimentConfig] = None,
        settings: Optional[Dict[str, Any]] = None,
        labels: Optional[Dict[str, str]] = None,
        session: Optional[Session] = None,
    ):
        """EstimatorBase constructor.

        Args:
            hyperparameters (dict, optional): A dictionary that represents the
                hyperparameters used in the training job. The hyperparameters will be
                stored in the `/ml/input/config/hyperparameters.json` as a JSON
                dictionary in the training container.
            base_job_name (str, optional): The base name used to generate the training
                job name.
            max_run_time (int, optional): The maximum time in seconds that the training
                job can run. The training job will be terminated after the time is
                reached (Default None).
            output_path (str, optional): An OSS URI to store the outputs of the training
                jobs. If not provided, an OSS URI will be generated using the default
                OSS bucket in the session. When the `estimator.fit` method is called,
                a specific OSS URI under the output_path for each channel is generated
                and mounted to the training container.

                A completed training container directory structure example::

                    /ml
                    |-- usercode            			// User source code directory.
                    |   |-- requirements.txt
                    |   `-- train.py
                    |-- input               			// TrainingJob input
                    |   `-- config
                    |       |-- hyperparameters.json	// Hyperparameters in JSON
                    |       |                           // dictionary format for the
                    |       |                           // TrainingJob
                    |       |
                    |   `-- data            			// TrainingJob input channels
                    |       |                           // `/ml/input/data/` is a input
                    |       |                           // channel, and the directory
                    |       |                           // name is the channel name.
                    |       |                           // Each directory under the
                    |       |-- test-data
                    |       |   `-- test.csv
                    |       `-- train-data
                    |           `-- train.csv
                    `-- output              			// TrainingJob output channels.
                            |                           // Each directory under the
                            |                           // `/ml/output/` is an output
                            |                           // channel, and the directory
                            |                           // name is the channel name.
                            `-- model
                            `-- checkpoints
            checkpoints_path (str, optional): An OSS URI that stores the checkpoint of the
                training job. If provided, the OSS URI will be mounted to the directory
                `/ml/output/checkpoints/`.
            environments: A dictionary that maps environment variable names to their values.
                This optional field allows you to provide a set of environment variables that will be
                applied to the context where the code is executed.
            requirements (list, optional): An optional list of strings that specifies the Python
                package dependencies with their versions. Each string in the list should be in the format
                'package' or 'package==version'. This is similar to the contents of a requirements.txt file used
                in Python projects. If requirements.txt is provided in user code directory, requirements
                will override the conflict dependencies directly.
            resource_type (str, optional): The resource type used to run the training job.
                By default, general computing resource is used. If the resource_type is
                'Lingjun', Lingjun computing resource is used.
            instance_type (str, optional): The machine instance type used to run the
                training job. To view the supported machine instance types, please refer
                to the document:
                https://help.aliyun.com/document_detail/171758.htm#section-55y-4tq-84y.
                If the instance_type is "local", the training job is executed locally
                using docker.
            spot_spec (:class:`pai.job.SpotSpec`, optional): The specification of the spot
                instance used to run the training job. If provided, the training job will
                use the spot instance to run the training job.
            instance_count (int): The number of machines used to run the training job.
            user_vpc_config (:class:`pai.estimator.UserVpcConfig`, optional): The VPC
                configuration used to enable the training job instance to connect to the
                specified user VPC. If provided, an Elastic Network Interface (ENI) will
                be created and attached to the training job instance, allowing the
                instance to access the resources within the specified VPC. Default to
                None.
            experiment_config (:class:`pai.estimator.ExperimentConfig`, optional): The
                experiment configuration used to construct the relationship between the
                training job and the experiment. If provided, the training job will belong
                to the specified experiment, in which case the training job will use
                artifact_uri of experiment as default output path. Default to None.
            settings (dict, optional): A dictionary that represents the additional settings
                for job, such as AIMaster configurations.
            labels (Dict[str, str], optional): A dictionary that maps label names to
                their values. This optional field allows you to provide a set of labels
                that will be applied to the training job.
            session (Session, optional): A PAI session instance used for communicating
                with PAI service.

        """
        self.hyperparameters = hyperparameters or dict()
        self.checkpoints_path = checkpoints_path
        self.session = session or get_default_session()
        super().__init__(
            base_job_name=base_job_name,
            output_path=output_path,
            experiment_config=experiment_config,
            instance_type=instance_type,
            instance_count=instance_count,
            resource_id=resource_id,
            resource_type=resource_type,
            spot_spec=spot_spec,
            instance_spec=instance_spec,
            user_vpc_config=user_vpc_config,
            max_run_time=max_run_time,
            environments=environments,
            requirements=requirements,
            settings=settings,
            labels=labels,
        )

    def set_hyperparameters(self, **kwargs):
        """Set hyperparameters for the training job.

        Args:
            **kwargs: Hyperparameters in key-value pairs.
        """
        self.hyperparameters.update(**kwargs)

    def _gen_job_display_name(self, job_name=None):
        """Generate job display name."""
        if job_name:
            return job_name
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        return "{}_{}".format(self.base_job_name or "training_job", ts)

    @abstractmethod
    def fit(
        self, inputs: Dict[str, Any] = None, wait: bool = True, show_logs: bool = True
    ):
        """Submit a training job with the given input data."""

    def model_data(self) -> str:
        """Model data output path.

        Returns:
            str: A string in OSS URI format refers to the output model of the submitted
                job.
        """
        if not self.latest_job:
            raise RuntimeError(
                "No TrainingJob for the estimator, output model data not found."
            )

        if not self.latest_job.is_succeeded():
            logger.warning(
                "The TrainingJob is currently not in a succeeded status, which means"
                " that the model data output may not be accessible."
            )

        return self.latest_job.output_path(
            channel_name=DEFAULT_OUTPUT_MODEL_CHANNEL_NAME
        )

    def checkpoints_data(self) -> str:
        """Checkpoints data output path.

        Returns:
            str: A string in OSS URI format refers to the checkpoints of submitted
                training job.
        """
        if not self.latest_job:
            raise RuntimeError(
                "No TrainingJob for the Estimator, output checkpoints data path "
                "not found."
            )
        return self.latest_job.output_path(channel_name=DEFAULT_CHECKPOINT_CHANNEL_NAME)

    def tensorboard_data(self) -> str:
        """Output TensorBoard logs path.

        Returns:
            str: A string in OSS URI format refers to the tensorboard log of submitted
                training job.
        """
        if not self.latest_job:
            raise RuntimeError(
                "No TrainingJob for the Estimator, output TensorBoard logs data path"
                " not found."
            )
        return self.latest_job.output_path(
            channel_name=DEFAULT_TENSORBOARD_CHANNEL_NAME,
        )

    def tensorboard(self, wait=True):
        """Launch a TensorBoard Application to view the output TensorBoard logs.

        Args:
            wait (bool): Specifies whether to block until the TensorBoard is running.

        Returns:
            :class:`pai.tensorboard.TensorBoard`: A TensorBoard instance.
        """
        from pai.tensorboard import TensorBoard

        if not self.latest_job:
            raise RuntimeError("Could not find a submitted training job.")

        source_type = "TrainingJob"
        if isinstance(self.latest_job, LocalTrainingJob):
            raise RuntimeError("Local training job does not support tensorboard.")
        res = self.session.tensorboard_api.list(
            source_type=source_type,
            source_id=self.latest_job.training_job_id,
        )

        if res.items:
            if len(res.items) > 1:
                logger.warning(
                    "Found multiple TensorBoard instances for the submitted training "
                    "job, use the first one."
                )
            tb_id = res.items[0]["TensorboardId"]
            tb = TensorBoard(tensorboard_id=tb_id, session=self.session)
            tb.start(wait=wait)
        else:
            tb = TensorBoard.create(
                uri=self.tensorboard_data(),
                wait=wait,
                display_name=self.latest_job.training_job_name,
                source_id=self.latest_job.training_job_id,
                source_type=source_type,
                session=self.session,
            )

        # Open the TensorBoard in the default browser.
        webbrowser.open(tb.app_uri)
        return tb

    def create_model(self, inference_spec: Union[InferenceSpec, Dict]) -> Model:
        """Create a Model object using output model of the training job.

        Args:
            inference_spec (InferenceSpec): A ``InferenceSpec`` instance that describe
             how to create a prediction service with the output model.

        Returns:
            :class:`pai.model.Model`: A ``Model`` object.
        """

        if isinstance(inference_spec, Dict):
            inference_spec = InferenceSpec.from_dict(inference_spec)

        m = Model(
            model_data=self.model_data(),
            inference_spec=inference_spec,
            session=self.session,
        )
        return m

    def deploy(
        self,
        service_name: str,
        inference_spec: InferenceSpec,
        instance_type: Optional[str] = None,
        instance_count: int = 1,
        resource_config: Optional[Union[ResourceConfig, Dict[str, int]]] = None,
        resource_id: str = None,
        options: Optional[Dict[str, Any]] = None,
        serializer: SerializerBase = None,
        wait=True,
    ) -> Predictor:
        """Deploy the output model to create an online prediction service.

        Args:
            service_name (str): Name for the online prediction service.
            inference_spec (InferenceSpec): A ``InferenceSpec`` instance used for
                creating the service.
            instance_type (str, optional): The machine instance type for the service.
            instance_count (int): Number of machine instance count.
            resource_config (Union[ResourceConfig, Dict[str, int]], optional): Resource
                config for each prediction service instance.
            resource_id (str, optional): The ID of the resource group. If not provided,
                the prediction service is deployed to ``public resource group``.
            serializer (SerializerBase): A SerializerBase instance used to serialize
                the prediction request data and deserialize the response data.
            options (Dict[str, Any], optional): Additional options for the prediction
                service.
            wait (bool): If true, wait until the service is ready (Default True).

        Returns:
            :class:`pai.predictor.Predictor`: A predictor instance refers to the created
                prediction service.
        """
        m = Model(
            model_data=self.model_data(),
            inference_spec=inference_spec,
        )

        p = m.deploy(
            service_name=service_name,
            instance_type=instance_type,
            instance_count=instance_count,
            resource_config=resource_config,
            resource_id=resource_id,
            serializer=serializer,
            options=options,
            wait=wait,
        )
        return p


class Estimator(EstimatorBase):
    """The Estimator object is responsible for submitting TrainingJob.

    The Estimator helps to run a training script in the PAI Training Service with a
    specific image.

    Example::

        est = Estimator(
            source_dir="./train/src/",
            command="python train.py",
            image_uri = training_image_uri,
            instance_type="ecs.c6.xlarge",
            hyperparameters={
                "n_estimators": 50,
                "objective": "binary:logistic",
                "max_depth": 5,
                "eval_metric": "auc",
            },
            output_path="oss://{YOUR_BUCKET_NAME}/pai/training_job/output_path",
        )

        est.fit(inputs={
            "train": "oss://{YOUR_BUCKET_NAME}/path/to/train-data",
            "test": "oss://{YOUR_BUCKET_NAME}/path/to/test-data",
        })

        print(est.model_data())

    """

    def __init__(
        self,
        image_uri: str,
        command: Union[str, List[str]],
        source_dir: Optional[str] = None,
        git_config: Optional[Dict[str, str]] = None,
        job_type: str = JobType.PyTorchJob,
        hyperparameters: Optional[Dict[str, Any]] = None,
        environments: Optional[Dict[str, str]] = None,
        requirements: Optional[List[str]] = None,
        base_job_name: Optional[str] = None,
        max_run_time: Optional[int] = None,
        checkpoints_path: Optional[str] = None,
        output_path: Optional[str] = None,
        metric_definitions: Optional[List[Dict[str, str]]] = None,
        instance_type: Optional[str] = None,
        instance_count: Optional[int] = None,
        user_vpc_config: Optional[UserVpcConfig] = None,
        experiment_config: Optional[ExperimentConfig] = None,
        resource_id: Optional[str] = None,
        session: Optional[Session] = None,
        **kwargs,
    ):
        """Estimator constructor.

        Args:
            image_uri (str): The image used in the training job. It can be an image
                provided by PAI or a user customized image. To view the images provided
                by PAI, please refer to the document:
                https://help.aliyun.com/document_detail/202834.htm.
            command (Union[str, List[str]]): The command used to run the training job.
            source_dir (str, optional): The local source code directory used in the
                training job. The directory will be packaged and uploaded to an OSS
                bucket, then downloaded to the `/ml/usercode` directory in the training
                job container. If there is a `requirements.txt` file in the source code
                directory, the corresponding dependencies will be installed before the
                training script runs.

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
            git_config (Dict[str, str]): Git configuration used to clone the repo.
                Including ``repo``, ``branch``, ``commit``, ``username``, ``password``
                and ``token``. The ``repo`` is required. All other fields are optional.
                ``repo`` specifies the Git repository. If you don't provide ``branch``,
                the default value 'master' is used. If you don't provide ``commit``, the
                latest commit in the specified branch is used. ``username``, ``password``
                and ``token`` are for authentication purpose.
                For example, the following config:

                .. code:: python

                    git_config = {
                        'repo': 'https://github.com/modelscope/modelscope.git',
                        'branch': 'master',
                        'commit': '9bfc4a9d83c4beaf8378d0a186261ffc1cd9f960'
                    }

                results in cloning the git repo specified in 'repo', then checking out
                the 'master' branch, and checking out the specified commit.
            job_type (str): The type of job, which can be TFJob, PyTorchJob, XGBoostJob,
                etc.
            hyperparameters (dict, optional): A dictionary that represents the
                hyperparameters used in the training job. The hyperparameters will be
                stored in the `/ml/input/config/hyperparameters.json` as a JSON
                dictionary in the training container.
            environments: A dictionary that maps environment variable names to their values.
                This optional field allows you to provide a set of environment variables that will be
                applied to the context where the code is executed.
            requirements (list, optional): An optional list of strings that specifies the Python
                package dependencies with their versions. Each string in the list should be in the format
                'package' or 'package==version'. This is similar to the contents of a requirements.txt file used
                in Python projects. If requirements.txt is provided in user code directory, requirements
                will override the conflict dependencies directly.
            instance_type (str): The machine instance type used to run the training job.
                To view the supported machine instance types, please refer to the
                document:
                https://help.aliyun.com/document_detail/171758.htm#section-55y-4tq-84y.
                If the instance_type is "local", the training job is executed locally
                using docker.
            max_run_time (int, optional): The maximum time in seconds that the training
                job can run. The training job will be terminated after the time is
                reached (Default None).
            instance_count (int): The number of machines used to run the training job.
            base_job_name (str, optional): The base name used to generate the training
                job name.
            checkpoints_path (str, optional): An OSS URI that stores the checkpoint of the
                training job. If provided, the OSS URI will be mounted to the directory
                `/ml/output/checkpoints/`.
            user_vpc_config (:class:`pai.estimator.UserVpcConfig`, optional): The VPC
                configuration used to enable the training job instance to connect to the
                specified user VPC. If provided, an Elastic Network Interface (ENI) will
                be created and attached to the training job instance, allowing the
                instance to access the resources within the specified VPC. Default to
                None.
            experiment_config(:class:`pai.estimator.ExperimentConfig`, optional): The
                experiment configuration used to construct the relationship between the
                training job and the experiment. If provided, the training job will belong
                to the specified experiment, in which case the training job will use
                artifact_uri of experiment as default output path. Default to None.
            output_path (str, optional): An OSS URI to store the outputs of the training
                jobs. If not provided, an OSS URI will be generated using the default
                OSS bucket in the session. When the `estimator.fit` method is called,
                a specific OSS URI under the output_path for each channel is generated
                and mounted to the training container.

                A completed training container directory structure example::

                    /ml
                    |-- usercode            			// User source code directory.
                    |   |-- requirements.txt
                    |   `-- train.py
                    |-- input               			// TrainingJob input
                    |   `-- config
                    |       |-- hyperparameters.json	// Hyperparameters in JSON
                    |       |                           // dictionary format for the
                    |       |                           // TrainingJob
                    |       |
                    |   `-- data            			// TrainingJob input channels
                    |       |                           // `/ml/input/data/` is a input
                    |       |                           // channel, and the directory
                    |       |                           // name is the channel name.
                    |       |                           // Each directory under the
                    |       |-- test-data
                    |       |   `-- test.csv
                    |       `-- train-data
                    |           `-- train.csv
                    `-- output              			// TrainingJob output channels.
                            |                           // Each directory under the
                            |                           // `/ml/output/` is an output
                            |                           // channel, and the directory
                            |                           // name is the channel name.
                            `-- model
                            `-- checkpoints

            metric_definitions (List[Dict[str, Any]): A list of dictionaries that
                defines the metrics used to evaluate the training jobs. Each dictionary
                contains two keys: "Name" for the name of the metric, and "Regex" for
                the regular expression used to extract the metric from the logs of the
                training job. The regular expression should contain only one capture
                group that is responsible for extracting the metric value.

                Example::

                    metric_definitions=[
                        {
                            "Name": "accuracy",
                            "Regex": r".*accuracy="
                                     r"([-+]?[0-9]*.?[0-9]+(?:[eE][-+]?[0-9]+)?).*",
                        },
                        {
                            "Name": "train-accuracy",
                            "Regex": r".*validation_0-auc="
                                     r"([-+]?[0-9]*.?[0-9]+(?:[eE][-+]?[0-9]+)?).*",
                        },
                    ]
            session (Session, optional): A PAI session instance used for communicating
                with PAI service.

        """
        self.image_uri = image_uri
        self.command = command
        self.source_dir = source_dir
        self.git_config = git_config
        self.job_type = job_type if job_type else JobType.PyTorchJob
        self.metric_definitions = metric_definitions

        super(Estimator, self).__init__(
            hyperparameters=hyperparameters,
            environments=environments,
            requirements=requirements,
            base_job_name=base_job_name,
            max_run_time=max_run_time,
            output_path=output_path,
            checkpoints_path=checkpoints_path,
            instance_type=instance_type,
            instance_count=instance_count,
            user_vpc_config=user_vpc_config,
            experiment_config=experiment_config,
            resource_id=resource_id,
            session=session,
        )

    def training_image_uri(self) -> str:
        """Return the Docker image to use for training.

        The fit() method, that does the model training, calls this method to
        find the image to use for model training.

        Returns:
            str: The URI of the Docker image.
        """
        return self.image_uri

    def _prepare_for_training(self):
        """Update args before starting the training job."""
        if self.git_config:
            updated_args = git_utils.git_clone_repo(
                git_config=self.git_config,
                source_dir=self.source_dir,
            )
            self.source_dir = updated_args["source_dir"]

    def _build_algorithm_spec(
        self, code_input, inputs: Dict[str, Any]
    ) -> AlgorithmSpec:
        """Build a temporary AlgorithmSpec used for submitting the TrainingJob."""
        algorithm_spec = AlgorithmSpec(
            command=(
                self.command
                if isinstance(self.command, list)
                else ["sh", "-c", self.command]
            ),
            image=self.training_image_uri(),
            job_type=self.job_type,
            metric_definitions=self.metric_definitions,
            code_dir=code_input,
            output_channels=self._default_training_output_channels(),
            input_channels=[
                Channel(name=channel_name, required=False)
                for channel_name in inputs.keys()
            ],
        )
        return algorithm_spec

    def fit(
        self,
        inputs: Dict[str, Any] = None,
        outputs: Dict[str, Any] = None,
        wait: bool = True,
        show_logs: bool = True,
        job_name: Optional[str] = None,
    ) -> Union[TrainingJob, LocalTrainingJob]:
        """Submit a training job with the given input data.

        Args:
            inputs (Dict[str, Any]): A dictionary representing the input data for the
                training job. Each key/value pair in the dictionary is an input channel,
                the key is the channel name, and the value is the input data. The input
                data can be an OSS URI or a NAS URI object and will be mounted to the
                `/ml/input/data/{channel_name}` directory in the training container.
             outputs (Dict[str, Any]): A dictionary representing the output locations for
                the training job. Each key/value pair in the dictionary is an output channel,
                the key is the channel name, and the value is the output data location.
            wait (bool): Specifies whether to block until the training job is completed,
                either succeeded, failed, or stopped. (Default True).
            show_logs (bool): Specifies whether to show the logs produced by the
                training job (Default True).
            job_name (str, optional): The name of the training job.

        Returns:
            :class:`pai.job.TrainingJob` or :class:`pai.job.LocalTrainingJob`: A
                submitted training job.

        Raises:
            UnExpectedStatusException: If the training job fails.

        """
        inputs = inputs or dict()
        self._prepare_for_training()
        job_name = self.job_name(job_name=job_name)
        if is_local_run_instance_type(self.instance_type):
            return self._local_run(
                job_name=job_name,
                inputs=inputs,
                instance_type=self.instance_type,
                wait=wait,
            )
        return self._fit(
            inputs=inputs,
            outputs=outputs,
            job_name=job_name,
            wait=wait,
            show_logs=show_logs,
        )

    def _fit(
        self,
        job_name,
        inputs: Dict[str, Any],
        outputs: Dict[str, Any],
        wait: bool = True,
        show_logs: bool = True,
    ) -> TrainingJob:
        # prepare input code.
        code_input = self._build_code_input(job_name, source_dir=self.source_dir)
        algo_spec = self._build_algorithm_spec(
            code_input=code_input,
            inputs=inputs,
        )
        inputs = self.build_inputs(
            inputs=inputs,
            input_channels=algo_spec.input_channels,
        )

        outputs = outputs or {}
        if self.checkpoints_path:
            outputs.update({DEFAULT_CHECKPOINT_CHANNEL_NAME: self.checkpoints_path})

        outputs = self.build_outputs(
            job_name=job_name,
            output_channels=algo_spec.output_channels,
            outputs=outputs,
        )

        return self._submit(
            job_name=job_name,
            algorithm_spec=algo_spec,
            instance_spec=self.instance_spec,
            instance_type=self.instance_type,
            instance_count=self.instance_count,
            resource_id=self.resource_id,
            hyperparameters=self.hyperparameters,
            environments=self.environments,
            requirements=self.requirements,
            max_run_time=self.max_run_time,
            inputs=inputs,
            outputs=outputs,
            user_vpc_config=self.user_vpc_config if self.user_vpc_config else None,
            experiment_config=(
                self.experiment_config if self.experiment_config else None
            ),
            labels=self.labels,
            wait=wait,
            show_logs=show_logs,
        )

    def _local_run(
        self,
        job_name,
        instance_type: str,
        inputs: Dict[str, Any] = None,
        wait: bool = True,
    ) -> "LocalTrainingJob":
        if self.instance_count > 1:
            raise RuntimeError("Local training job only supports single instance.")

        training_job = LocalTrainingJob(
            estimator=self,
            inputs=inputs,
            job_name=job_name,
            instance_type=instance_type,
        )
        training_job.run()
        if wait:
            training_job.wait()
        return training_job


class AlgorithmEstimator(EstimatorBase):
    """Handle training jobs with algorithms

    The AlgorithmEstimator provides a simple way for submitting training jobs with
    algorithms.

    Example::

        # Create an AlgorithmEstimator with built-in algorithms
        est = AlgorithmEstimator(
            algorithm_name="pai-algorithm-test",
            algorithm_version="0.1.0",
            algorithm_provider="pai",
        )

        # Inspect the definition of hyperparameters, input channels and output channels
        print(est.hyperparameter_definitions)
        print(est.input_channel_definitions)
        print(est.output_channel_definitions)
        print(est.supported_instance_types)

        # Submit a training job
        est.fit(
            inputs={
                "train": "oss://bucket/path/to/train/data",
                "test": "oss://bucket/path/to/test/data",
            },
        )

        # Inspect all outputs data
        print(est.get_outputs_data())

    """

    def __init__(
        self,
        algorithm_name: Optional[str] = None,
        algorithm_version: Optional[str] = None,
        algorithm_provider: Optional[str] = None,
        algorithm_spec: Optional[AlgorithmSpec] = None,
        hyperparameters: Optional[Dict[str, Any]] = None,
        environments: Optional[Dict[str, str]] = None,
        requirements: Optional[List[str]] = None,
        base_job_name: Optional[str] = None,
        max_run_time: Optional[int] = None,
        output_path: Optional[str] = None,
        instance_type: Optional[str] = None,
        instance_count: Optional[int] = None,
        user_vpc_config: Optional[UserVpcConfig] = None,
        session: Optional[Session] = None,
        instance_spec: Optional[Dict[str, Union[int, str]]] = None,
        **kwargs,
    ):
        """Initialize an AlgorithmEstimator.

        Args:
            algorithm_name (str, optional): The name of the registered algorithm. If not
                provided, the algorithm_spec must be provided.
            algorithm_version (str, optional): The version of the algorithm. If not
                provided, the latest version of the algorithm will be used. If algorithm
                name is not provided, this argument will be ignored.
            algorithm_provider (str, optional): The provider of the algorithm.
                Currently, only "pai" or None are supported. Set it to "pai" to retrieve
                 a PAI official algorithm. If not provided, the default provider is
                 user's PAI account. If algorithm name is not provided, this argument
                  will be ignored.
            algorithm_spec (AlgorithmSpec, optional): A temporary algorithm spec.
                Required if algorithm_name is not provided.
            hyperparameters (dict, optional): A dictionary that represents the
                hyperparameters used in the training job. Default hyperparameters will
                be retrieved from the algorithm definition.
            environments: A dictionary that maps environment variable names to their values.
                This optional field allows you to provide a set of environment variables that will be
                applied to the context where the code is executed.
            requirements (list, optional): An optional list of strings that specifies the Python
                package dependencies with their versions. Each string in the list should be in the format
                'package' or 'package==version'. This is similar to the contents of a requirements.txt file used
                in Python projects. If requirements.txt is provided in user code directory, requirements
                will override the conflict dependencies directly.
            base_job_name (str, optional): The base name used to generate the training
                job name. If not provided, a default job name will be generated.
            max_run_time (int, optional): The maximum time in seconds that the training
                job can run. The training job will be terminated after the time is
                reached (Default None).
            output_path (str, optional): An OSS URI to store the outputs of the training
                jobs. If not provided, an OSS URI will be generated using the default
                OSS bucket in the session. When the `estimator.fit` method is called,
                a specific OSS URI under the output_path for each channel is generated
                and mounted to the training container.
            instance_type (str, optional): The machine instance type used to run the
                training job. If not provider, the default instance type will be
                retrieved from the algorithm definition. To view the supported machine
                instance types, please refer to the document:
                https://help.aliyun.com/document_detail/171758.htm#section-55y-4tq-84y.
            instance_count (int, optional): The number of machines used to run the
                training job. If not provider, the default instance count will be
                retrieved from the algorithm definition.
            user_vpc_config (:class:`pai.estimator.UserVpcConfig`, optional): The VPC
                configuration used to enable the training job instance to connect to the
                specified user VPC. If provided, an Elastic Network Interface (ENI) will
                be created and attached to the training job instance, allowing the
                instance to access the resources within the specified VPC. Default to
                None.
            session (:class:`pai.session.Session`, optional): A PAI session object
                used for interacting with PAI Service.
        """
        self._check_args(
            algorithm_name=algorithm_name,
            algorithm_spec=algorithm_spec,
        )

        self.session = session or get_default_session()

        # Use _algo_spec to store the algorithm spec for inner use no matter the
        # algorithm_name is provided or the algorithm_spec is provided.
        # If algorithm_name is provided, retrieve the algorithm spec from the registry.
        if algorithm_name:
            _algo_version = self._get_algo_version(
                algorithm_name=algorithm_name,
                algorithm_version=algorithm_version,
                algorithm_provider=algorithm_provider,
            )
            self._algo_spec = AlgorithmSpec.model_validate(
                _algo_version["AlgorithmSpec"]
            )
            self.algorithm_name = _algo_version["AlgorithmName"]
            self.algorithm_version = _algo_version["AlgorithmVersion"]
            self.algorithm_provider = _algo_version["AlgorithmProvider"]
            self.algorithm_spec = None
        # If algorithm_name is not provided, use the provided algorithm_spec.
        else:
            self._algo_spec = algorithm_spec
            self.algorithm_name = None
            self.algorithm_version = None
            self.algorithm_provider = None
            self.algorithm_spec = algorithm_spec

        if not instance_type and not instance_spec:
            instance_type = self._get_default_training_instance_type()
        super(AlgorithmEstimator, self).__init__(
            hyperparameters=self._get_hyperparameters(hyperparameters),
            environments=environments,
            requirements=requirements,
            base_job_name=base_job_name,
            max_run_time=max_run_time,
            output_path=output_path,
            instance_type=instance_type,
            instance_count=instance_count,
            session=session,
            user_vpc_config=user_vpc_config,
            instance_spec=instance_spec,
            **kwargs,
        )

    # TODO: check if the hyperparameters are valid
    def set_hyperparameters(self, **kwargs):
        """Set hyperparameters for the algorithm training."""
        super(AlgorithmEstimator, self).set_hyperparameters(**kwargs)

    @property
    def hyperparameter_definitions(self) -> List[HyperParameterDefinition]:
        """Get the hyperparameter definitions from the algorithm spec."""
        res = self._algo_spec.hyperparameter_definitions
        return res

    @property
    def input_channel_definitions(self) -> List[Channel]:
        """Get the input channel definitions from the algorithm spec."""
        res = self._algo_spec.input_channels
        return res

    @property
    def output_channel_definitions(self) -> List[Channel]:
        """Get the output channel definitions from the algorithm spec."""
        res = self._algo_spec.output_channels
        return res

    @property
    def supported_instance_types(self) -> List[str]:
        """Get the supported instance types from the algorithm spec."""
        return self._algo_spec.supported_instance_types

    def _check_args(
        self,
        algorithm_name: str,
        algorithm_spec: Optional[AlgorithmSpec],
    ):
        """Check the algorithm_name and algorithm_spec.

        If neither algorithm_name nor algorithm_spec is provided, raise a ValueError.
        If both algorithm_name and algorithm_spec are provided, use the algorithm_name
        by default and ignore the algorithm_spec.

        Args:
            algorithm_name (str): The name of the algorithm.
            algorithm_spec (AlgorithmSpec): The algorithm spec.
        """
        if not algorithm_name and not algorithm_spec:
            raise ValueError(
                "Either algorithm_name or algorithm_spec should be provided."
            )
        if algorithm_name and algorithm_spec:
            logger.warning(
                "Both a tuple of (algorithm_name, algorithm_version,"
                " algorithm_provider) and algorithm_spec are provided. Use the tuple of"
                " (algorithm_name, algorithm_version, algorithm_provider) by default."
                " The provided algorithm_spec will be ignored."
            )

    def _get_algo_version(
        self,
        algorithm_name: str,
        algorithm_version: Optional[str] = None,
        algorithm_provider: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get the algorithm version object.

        Args:
            algorithm_name (str): The name of the algorithm.
            algorithm_version (str, optional): The version of the algorithm.
            algorithm_provider (str, optional): The provider of the algorithm.

        Returns:
            dict: A dict that represents algorithm version object.
        """
        if not algorithm_name:
            raise ValueError(
                "Parameter algorithm_name cannot be None or empty. Please provide a"
                " valid algorithm name."
            )

        resp_list_algo = self.session.algorithm_api.list(
            algorithm_name=algorithm_name,
            algorithm_provider=algorithm_provider,
        )
        if resp_list_algo.total_count == 0:
            raise ValueError(
                f"Could not find any algorithm with the specific"
                f" name='{algorithm_name}' and provider='{algorithm_provider}'."
                f" Please check the arguments."
            )
        algo_obj = resp_list_algo.items[0]
        algorithm_id = algo_obj["AlgorithmId"]

        if not algorithm_version:
            resp_list_algo_versions = self.session.algorithm_api.list_versions(
                algorithm_id=algorithm_id,
            )
            algo_version_obj = resp_list_algo_versions.items[-1]
            algorithm_version = algo_version_obj["AlgorithmVersion"]
            logger.warning(
                f"Parameter algorithm_version is not provided, the latest"
                f" version='{algorithm_version}' of the algorithm will be used."
            )

        resp_algo_version = self.session.algorithm_api.get_version(
            algorithm_id=algorithm_id,
            algorithm_version=algorithm_version,
        )
        return resp_algo_version

    def _get_hyperparameters(
        self, hyperparameters: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Get hyperparameters.

        Get the default hyperparameters from the algorithm spec and update it with the
        user provided hyperparameters.

        Args:
            hyperparameters (dict, optional): The user provided hyperparameters.

        Returns:
            dict: The dict of hyperparameters.
        """
        res = {}
        hps_def = self.hyperparameter_definitions
        if hps_def:
            # Get default hyperparameters.
            for hp in hps_def:
                hp_name = hp.name
                hp_value = hp.default_value
                hp_type = hp.type or "String"
                # For hyperparameters with type INT or FLOAT, if the default value is
                # empty, skip it.
                if (
                    hp_type in [HyperParameterType.INT, HyperParameterType.FLOAT]
                    and not hp_value
                ):
                    continue
                else:
                    # Convert the value to the corresponding type.
                    hp_value = HyperParameterType.convert(hp_value, hp_type)
                    res.update({hp_name: hp_value})
            # Update with user provided hyperparameters.
            for hp in hyperparameters if hyperparameters else {}:
                if hp not in res:
                    logger.warning(
                        f"Hyperparameter='{hp}' is not defined in hyperparameters"
                        f" definition. Make sure you are using the right"
                        f" hyperparameters and check the hyperparameter_definitions."
                    )
                    res.update({hp: hyperparameters[hp]})
                else:
                    res[hp] = hyperparameters[hp]
        else:
            # Use user provided hyperparameters.
            res = hyperparameters
        return res

    def _get_default_training_instance_type(self) -> str:
        """Get the default training instance type from the algorithm spec."""
        instance_generator = make_list_resource_iterator(
            self.session.job_api.list_ecs_specs
        )
        sup_instance_types = self.supported_instance_types
        machine_spec = next(
            (
                item
                for item in instance_generator
                if not sup_instance_types or item["InstanceType"] in sup_instance_types
            ),
            None,
        )
        if not machine_spec:
            raise RuntimeError(
                "No supported training instance type found. Please check the supported"
                " instance types."
            )
        return machine_spec["InstanceType"]

    def fit(
        self,
        inputs: Dict[str, Any] = None,
        outputs: Dict[str, Any] = None,
        wait: bool = True,
        show_logs: bool = True,
        job_name: Optional[str] = None,
    ) -> TrainingJob:
        """Submit a training job with the given input data.

        Args:
            inputs (Dict[str, Any]): A dictionary representing the input data for the
                training job. Each key/value pair in the dictionary is an input channel,
                the key is the channel name, and the value is the input data. The input
                data can be an OSS URI or a NAS URI object and will be mounted to the
                `/ml/input/data/{channel_name}` directory in the training container.
            wait (bool): Specifies whether to block until the training job is completed,
                either succeeded, failed, or stopped. (Default True).
            show_logs (bool): Whether to show the logs of the training job. Default to True.
                Note that the logs will be shown only when the `wait` is set to True.
            job_name (str, optional): The name of the training job.

        Returns:
            :class:`pai.training_job.TrainingJob`: The submitted training job.

        Raises:
            UnExpectedStatusException: If the training job fails.

        """
        job_name = self.job_name(job_name=job_name)
        input_configs = self.build_inputs(
            inputs,
            input_channels=self._algo_spec.input_channels,
        )
        output_configs = self.build_outputs(
            job_name,
            output_channels=self._algo_spec.output_channels,
            outputs=outputs,
        )
        return self._submit(
            instance_count=self.instance_count,
            instance_type=self.instance_type,
            instance_spec=self.instance_spec,
            resource_id=self.resource_id,
            job_name=job_name,
            hyperparameters=self.hyperparameters,
            max_run_time=self.max_run_time,
            inputs=input_configs,
            outputs=output_configs,
            environments=self.environments,
            requirements=self.requirements,
            algorithm_name=self.algorithm_name,
            algorithm_version=self.algorithm_version,
            algorithm_provider=self.algorithm_provider,
            algorithm_spec=self.algorithm_spec,
            user_vpc_config=(
                self.user_vpc_config.to_dict() if self.user_vpc_config else None
            ),
            experiment_config=(
                self.experiment_config.to_dict() if self.experiment_config else None
            ),
            labels=self.labels,
            wait=wait,
            show_logs=show_logs,
        )

    def get_outputs_data(self) -> Dict[str, str]:
        """Show all outputs data paths.

        Returns:
            dict[str, str]: A dictionary of all outputs data paths.
        """
        if not self.latest_job:
            raise RuntimeError(
                "Could not find a submitted training job. Please submit a training job"
                " before calling this method."
            )

        uri_outputs = [
            output
            for output in self.latest_job.outputs
            if isinstance(output, UriOutput)
        ]
        extra_outputs = [
            output
            for output in self.latest_job.outputs
            if not isinstance(output, UriOutput)
        ]

        if extra_outputs:
            logger.warning(
                "Extra outputs are provided in the training job, but only URI outputs"
                " are supported. The extra outputs will be ignored: %s",
                extra_outputs,
            )
        return {ch.name: ch.output_uri for ch in uri_outputs}
