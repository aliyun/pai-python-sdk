import copy
import distutils.dir_util
import json
import logging
import os
import posixpath
import re
import shlex
import shutil
import tempfile
import textwrap
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pai.api.entity_base import EntityBaseMixin
from pai.common import ProviderAlibabaPAI, git_utils
from pai.common.consts import INSTANCE_TYPE_LOCAL_GPU, JobType
from pai.common.docker_utils import ContainerRun, run_container
from pai.common.oss_utils import OssUriObj, download, is_oss_uri, upload
from pai.common.utils import (
    is_local_run_instance_type,
    make_list_resource_iterator,
    random_str,
    to_plain_text,
)
from pai.exception import UnexpectedStatusException
from pai.model import InferenceSpec, Model, ResourceConfig
from pai.predictor import Predictor
from pai.schema.training_job_schema import TrainingJobSchema
from pai.serializers import SerializerBase
from pai.session import Session, config_default_session, get_default_session

logger = logging.getLogger(__name__)

DEFAULT_OUTPUT_MODEL_CHANNEL_NAME = "model"
DEFAULT_CHECKPOINT_CHANNEL_NAME = "checkpoints"
DEFAULT_LOGS_CHANNEL_NAME = "logs"


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


class Estimator(object):
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
        command: str,
        source_dir: Optional[str] = None,
        git_config: Optional[Dict[str, str]] = None,
        job_type: str = JobType.PyTorchJob,
        hyperparameters: Optional[Dict[str, Any]] = None,
        base_job_name: Optional[str] = None,
        max_run_time: Optional[int] = None,
        checkpoints_path: Optional[str] = None,
        output_path: Optional[str] = None,
        metric_definitions: Optional[List[Dict[str, str]]] = None,
        instance_type: Optional[str] = None,
        instance_count: int = 1,
        session: Optional[Session] = None,
    ):
        """Estimator constructor.

        Args:
            image_uri (str): The image used in the training job. It can be an image
                provided by PAI or a user customized image. To view the images provided
                by PAI, please refer to the document:
                https://help.aliyun.com/document_detail/202834.htm.
            command (str): The command used to run the training job.
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
        self.hyperparameters = hyperparameters or dict()
        self.instance_type = instance_type
        self.instance_count = instance_count
        self.job_type = job_type if job_type else JobType.PyTorchJob
        self.max_run_time = max_run_time
        self.base_job_name = base_job_name
        self.output_path = output_path
        self.checkpoints_path = checkpoints_path
        self.metric_definitions = metric_definitions
        self.session = session or get_default_session()
        self._latest_training_job = None

        self.__uploaded_source_files = None

        self._check_instance_type()

    def _prepare_for_training(self):
        """Update args before starting the training job."""
        if self.git_config:
            updated_args = git_utils.git_clone_repo(
                git_config=self.git_config,
                source_dir=self.source_dir,
            )
            self.source_dir = updated_args["source_dir"]

    def _gen_job_display_name(self, job_name=None):
        """Generate job display name."""
        if job_name:
            return job_name
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        return "{}_{}".format(self.base_job_name or "training_job", ts)

    def _check(self):
        if not self.image_uri:
            raise ValueError("Please provide image_uri to create the job.")

    def _check_instance_type(self):
        """Check if the given instance_type is supported for training job."""
        if not is_local_run_instance_type(
            self.instance_type
        ) and not self.session.is_supported_training_instance(self.instance_type):
            raise ValueError(
                f"Instance type='{self.instance_type}' is not supported."
                " Please provide a supported instance type to create the job."
            )

    def _upload_source_files(self, job_name: str) -> Optional[str]:
        """Upload local source files to OSS."""
        if not self.source_dir:
            return

        if is_oss_uri(self.source_dir):
            return self.source_dir
        elif not os.path.exists(self.source_dir):
            raise ValueError(f"Source directory {self.source_dir} does not exist.")
        # compress the source files to a Tar Gz file and upload to OSS bucket.
        upload_data_path = self.session.get_storage_path_by_category(
            "training_src", to_plain_text(job_name)
        )
        self.__uploaded_source_files = upload(
            source_path=self.source_dir,
            oss_path=upload_data_path,
            bucket=self.session.oss_bucket,
            is_tar=True,
        )
        return self.__uploaded_source_files

    def _build_algorithm_spec(
        self,
        code_input,
    ) -> Dict[str, Any]:
        """Build a temporary AlgorithmSpec used for submitting the TrainingJob."""
        command = [
            "/bin/sh",
            "-c",
            self.command,
        ]
        algo_spec = {
            "Command": command,
            "Image": self.training_image_uri(),
            "JobType": self.job_type,
            "MetricDefinitions": [m for m in self.metric_definitions]
            if self.metric_definitions
            else [],
            "CodeDir": code_input,
            "OutputChannels": [
                {
                    "Name": "logs",
                    "Properties": {
                        "ossAppendable": "true",
                    },
                }
            ],
        }
        return algo_spec

    def _build_input_data_configs(
        self, inputs: Dict[str, Any] = None
    ) -> List[Dict[str, str]]:
        inputs = inputs or dict()
        res = []
        for name, item in inputs.items():
            if not isinstance(item, str):
                raise ValueError(
                    f"The Estimator supports OSS URI or NAS URI as input data."
                    f" Input data of type {type(item)} is not supported."
                )
            if is_oss_uri(item):
                input_uri = item
            elif os.path.exists(item):
                store_path = self.session.get_storage_path_by_category("train_data")
                input_uri = upload(item, store_path)
            else:
                raise ValueError(
                    f"Input data path should be a valid OSS URI or local path:"
                    f" input={item}"
                )
            res.append({"Name": name, "InputUri": input_uri})

        return res

    def _build_output_data_configs(self, job_name: str) -> List[Dict[str, str]]:
        job_base_output_path = self._generate_job_base_output_path(job_name)

        # OSS URI for output channel will be mounted to directory
        # "/ml/output/{ChannelName}/" and the output OSS URI should be a "directory"
        def as_oss_dir_uri(uri: str):
            return uri if uri.endswith("/") else uri + "/"

        model_path = posixpath.join(
            job_base_output_path,
            DEFAULT_OUTPUT_MODEL_CHANNEL_NAME,
        )
        # Use checkpoints_path from user or construct a checkpoint path using
        # default output path.
        checkpoints_path = self.checkpoints_path or posixpath.join(
            job_base_output_path,
            DEFAULT_CHECKPOINT_CHANNEL_NAME,
        )

        # Output logs path
        logs_path = posixpath.join(
            job_base_output_path,
            DEFAULT_LOGS_CHANNEL_NAME,
        )
        res = [
            {
                "Name": DEFAULT_OUTPUT_MODEL_CHANNEL_NAME,
                "OutputUri": as_oss_dir_uri(model_path),
            },
            {
                "Name": DEFAULT_CHECKPOINT_CHANNEL_NAME,
                "OutputUri": as_oss_dir_uri(checkpoints_path),
            },
            {
                "Name": DEFAULT_LOGS_CHANNEL_NAME,
                "OutputUri": as_oss_dir_uri(logs_path),
            },
        ]
        return res

    def _build_code_input(self, job_name: str) -> Optional[Dict[str, Any]]:
        """Build a dict to represent AlgorithmSpecCodeDir used in the TrainingJob."""
        upload_source_files = self._upload_source_files(job_name)
        if not upload_source_files:
            return
        oss_uri_obj = OssUriObj(
            uri=self.session.patch_oss_endpoint(upload_source_files)
        )

        code_dir = {
            "LocationType": "oss",
            "LocationValue": {
                "Bucket": oss_uri_obj.bucket_name,
                "Key": oss_uri_obj.object_key,
                "Endpoint": oss_uri_obj.endpoint,
            },
        }

        return code_dir

    def _generate_job_base_output_path(self, job_name: str) -> str:
        bucket = self.session.oss_bucket
        bucket_name = bucket.bucket_name
        # replace non-alphanumeric character in training job name.
        name = to_plain_text(job_name)

        if self.output_path:
            return os.path.join(self.output_path, f"{name}_{random_str(6)}")
        else:
            job_output_path = self.session.get_storage_path_by_category(
                "training_job", f"{name}_{random_str(6)}"
            )
            return f"oss://{bucket_name}/{job_output_path}"

    def training_image_uri(self) -> str:
        """Return the Docker image to use for training.

        The fit() method, that does the model training, calls this method to
        find the image to use for model training.

        Returns:
            str: The URI of the Docker image.
        """
        return self.image_uri

    @property
    def latest_training_job(self):
        """Return the latest submitted training job."""
        return self._latest_training_job

    def fit(
        self, inputs: Dict[str, Any] = None, wait: bool = True, show_logs: bool = True
    ):
        """Submit a training job with the given input data.

        Args:
            inputs (Dict[str, Any]): A dictionary representing the input data for the
                training job. Each key/value pair in the dictionary is an input channel,
                the key is the channel name, and the value is the input data. The input
                data can be an OSS URI or a NAS URI object and will be mounted to the
                `/ml/input/data/{channel_name}` directory in the training container.
            wait (bool): Specifies whether to block until the training job is completed,
                either succeeded, failed, or stopped. (Default True).
            show_logs (bool): Specifies whether to show the logs produced by the
                training job (Default True).
        Raises:
            UnExpectedStatusException: If the training job fails.

        """
        inputs = inputs or dict()
        self._prepare_for_training()
        job_name = self._gen_job_display_name()
        if is_local_run_instance_type(self.instance_type):
            training_job = self._local_run(
                job_name=job_name, inputs=inputs, instance_type=self.instance_type
            )
        else:
            training_job = self._fit(inputs=inputs, job_name=job_name)
        self._latest_training_job = training_job

        if wait:
            self.wait(show_logs=show_logs)

    def wait(self, show_logs: bool = True):
        """Block until the latest training job is completed.

        Args:
            show_logs(bool): Specifies whether to fetch and print the logs produced by
                the training job.

        """
        if not self._latest_training_job:
            raise RuntimeError("Could not find a submitted training job.")
        self._latest_training_job.wait(show_logs=show_logs)

    def tensorboard(self, wait=True):
        """Launch a TensorBoard Application to view the output TensorBoard logs.

        Args:
            wait (bool): Specifies whether to block until the TensorBoard is running.

        Returns:
            :class:`pai.tensorboard.TensorBoard`: A TensorBoard instance.
        """
        from pai.tensorboard import TensorBoard

        if not self.latest_training_job:
            raise RuntimeError("Could not find a submitted training job.")

        if isinstance(self.latest_training_job, _LocalTrainingJob):
            raise RuntimeError("Local training job does not support tensorboard.")
        res = self.session.tensorboard_api.list(
            source_type="TrainingJob",
            source_id=self.latest_training_job.training_job_id,
        )

        if res.items:
            if len(res.items) > 1:
                logger.warning(
                    "Found multiple TensorBoard instances, use the first one."
                )
            tb_id = res.items[0]["TensorboardId"]
            tb = TensorBoard(tensorboard_id=tb_id, session=self.session)
            tb.start(wait=wait)
        else:
            tb = TensorBoard.create(
                uri=self.logs_data(),
                wait=wait,
                display_name=self._latest_training_job.training_job_name,
                source_id=self.latest_training_job.training_job_id,
                source_type="TrainingJob",
                session=self.session,
            )
        return tb

    def _fit(self, job_name, inputs: Dict[str, Any] = None):
        input_configs = self._build_input_data_configs(inputs)
        for c in input_configs:
            if "InputUri" in c and is_oss_uri(c["InputUri"]):
                c["InputUri"] = self._patch_default_oss_endpoint(c["InputUri"])
        output_configs = self._build_output_data_configs(job_name)
        for c in output_configs:
            if "OutputUri" in c and is_oss_uri(c["OutputUri"]):
                c["OutputUri"] = self._patch_default_oss_endpoint(c["OutputUri"])

        # prepare input code.
        code_input = self._build_code_input(job_name)
        algo_spec = self._build_algorithm_spec(
            code_input=code_input,
        )

        training_job_id = self.session.training_job_api.create(
            instance_count=self.instance_count,
            instance_type=self.instance_type,
            job_name=job_name,
            hyperparameters=self.hyperparameters,
            max_running_in_seconds=self.max_run_time,
            input_channels=input_configs,
            output_channels=output_configs,
            algorithm_spec=algo_spec,
        )
        training_job = _TrainingJob.get(training_job_id)
        print(
            f"View the job detail by accessing the console URI: {training_job.console_uri}"
        )
        return training_job

    def _patch_default_oss_endpoint(self, uri: str):
        """Patch default OSS endpoint for Input/Output OSS data uri for TrainingJob."""
        return self.session.patch_oss_endpoint(uri)

    def _local_run(
        self,
        job_name,
        instance_type: str,
        inputs: Dict[str, Any] = None,
    ) -> "_LocalTrainingJob":
        if self.instance_count > 1:
            raise RuntimeError("Local training job only supports single instance.")

        training_job = _LocalTrainingJob(
            estimator=self,
            inputs=inputs,
            job_name=job_name,
            instance_type=instance_type,
        )
        training_job.run()
        return training_job

    def model_data(self) -> str:
        """Model data output path.

        Returns:
            str: A string in OSS URI format refers to the output model of the submitted
                job.
        """
        if not self._latest_training_job:
            raise RuntimeError(
                "No TrainingJob for the estimator, output model data not found."
            )

        if not self._latest_training_job.is_succeeded():
            logger.warning(
                "The TrainingJob is currently not in a succeeded status, which means"
                " that the model data output may not be accessible."
            )

        return self._latest_training_job.output_path(
            channel_name=DEFAULT_OUTPUT_MODEL_CHANNEL_NAME
        )

    def checkpoints_data(self) -> str:
        """Checkpoints data output path.

        Returns:
            str: A string in OSS URI format refers to the checkpoints of submitted
                training job.
        """
        if not self._latest_training_job:
            raise RuntimeError(
                "No TrainingJob for the estimator, output checkpoints data not found."
            )
        return self._latest_training_job.output_path(
            channel_name=DEFAULT_CHECKPOINT_CHANNEL_NAME
        )

    def logs_data(self) -> str:
        """Output logs path.

        Returns:
            str: A string in OSS URI format refers to the checkpoints of submitted
                training job.
        """
        if not self._latest_training_job:
            raise RuntimeError(
                "No TrainingJob for the estimator, output logs data not found."
            )
        return self._latest_training_job.output_path(
            channel_name=DEFAULT_LOGS_CHANNEL_NAME,
        )

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


class AlgorithmEstimator(Estimator):
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
        algorithm_spec: Optional[Dict[str, Any]] = None,
        hyperparameters: Optional[Dict[str, Any]] = None,
        base_job_name: Optional[str] = None,
        max_run_time: Optional[int] = None,
        output_path: Optional[str] = None,
        instance_type: Optional[str] = None,
        instance_count: Optional[int] = None,
        session: Optional[Session] = None,
    ):
        """Initialize an AlgorithmEstimator.

        Args:
            algorithm_name (str, optional): The name of the registered algorithm. If not
                provided, the algorithm_spec must be provided.
            algorithm_version (str, optional): The version of the algorithm. If not
                provided, the latest version of the algorithm will be used. If algorithm
                name is not provided, this argument will be ignored.
            algorithm_provider (str, optional): The provider of the algorithm. Currently
                only "pai" or None are supported. Set it to "pai" to retrieve a PAI
                official algorithm. If not provided, the default provider is user's PAI
                account. If algorithm name is not provided, this argument will be
                ignored.
            algorithm_spec (Dict[str, Any], optional): A temporary algorithm spec.
                Required if algorithm_name is not provided.
            hyperparameters (dict, optional): A dictionary that represents the
                hyperparameters used in the training job. Default hyperparameters will
                be retrieved from the algorithm definition. The hyperparameters will be
                stored in the `/ml/input/config/hyperparameters.json` as a JSON
                dictionary in the training container.
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

            instance_type (str, optional): The machine instance type used to run the
                training job. If not provider, the default instance type will be
                retrieved from the algorithm definition. To view the supported machine
                instance types, please refer to the document:
                https://help.aliyun.com/document_detail/171758.htm#section-55y-4tq-84y.
            instance_count (int, optional): The number of machines used to run the
                training job. If not provider, the default instance count will be
                retrieved from the algorithm definition.
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
            self._algo_spec = _algo_version["AlgorithmSpec"]
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

        self.hyperparameters = self._get_hyperparameters(hyperparameters)
        self.base_job_name = base_job_name
        self.max_run_time = max_run_time
        self.output_path = output_path
        self.instance_type = (
            instance_type
            if instance_type
            else self._get_default_training_instance_type()
        )
        self.instance_count = instance_count if instance_count else 1

        self._latest_training_job = None
        self._output_channels = None

        self._check_instance_type()

    @property
    def hyperparameter_definitions(self) -> List[Dict[str, Any]]:
        """Get the hyperparameter definitions from the algorithm spec."""
        res = self._algo_spec.get("HyperParameters", [])
        return res

    @property
    def input_channel_definitions(self) -> List[Dict[str, Any]]:
        """Get the input channel definitions from the algorithm spec."""
        res = self._algo_spec.get("InputChannels", [])
        return res

    @property
    def output_channel_definitions(self) -> List[Dict[str, Any]]:
        """Get the output channel definitions from the algorithm spec."""
        res = self._algo_spec.get("OutputChannels", [])
        return res

    @property
    def supported_instance_types(self) -> List[str]:
        """Get the supported instance types from the algorithm spec."""
        res = (
            self._algo_spec["SupportedInstanceTypes"]
            if "SupportedInstanceTypes" in self._algo_spec
            else []
        )
        return res

    def _check_args(
        self,
        algorithm_name: str,
        algorithm_spec: Dict[str, Any],
    ):
        """Check the algorithm_name and algorithm_spec.

        If neither algorithm_name nor algorithm_spec is provided, raise a ValueError.
        If both algorithm_name and algorithm_spec are provided, use the algorithm_name
        by default and ignore the algorithm_spec.

        Args:
            algorithm_name (str): The name of the algorithm.
            algorithm_spec (dict): The algorithm spec.
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

    def _check_instance_type(self):
        """Check if the given instance_type is supported for training job."""
        if not self.session.is_supported_training_instance(self.instance_type):
            raise ValueError(
                f"Instance type='{self.instance_type}' is not supported."
                " Please provide a supported instance type to create the job."
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
                hp_name = hp.get("Name")
                hp_value = hp.get("DefaultValue", "")
                hp_type = hp.get("Type", "String")
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

    def _build_input_data_configs(
        self,
        inputs: Dict[str, Any] = None,
    ) -> List[Dict[str, str]]:
        """Build input data configs."""

        def _check_input_uri(uri: str):
            if not isinstance(uri, str):
                raise ValueError(
                    f"The Estimator supports OSS URI or NAS URI as input data."
                    f" Input data of type{type(uri)} is not supported."
                )
            if is_oss_uri(uri):
                input_uri = uri
            elif os.path.exists(uri):
                store_path = self.session.get_storage_path_by_category("train_data")
                input_uri = upload(uri, store_path)
            else:
                raise ValueError(
                    f"Input data path should be a valid OSS URI or local path:"
                    f" input={uri}"
                )
            return input_uri

        inputs = copy.deepcopy(inputs) or {}
        res = []
        input_channels_def = self.input_channel_definitions
        if input_channels_def:
            for channel in input_channels_def:
                channel_name = channel["Name"]
                channel_required = channel["Required"]
                if channel_required is True and channel_name not in inputs:
                    raise ValueError(
                        f"Input channel {channel_name} is required but not provided."
                        " Please check the input channels definition."
                    )
                elif channel_name in inputs:
                    input_uri = _check_input_uri(inputs[channel_name])
                    res.append({"Name": channel_name, "InputUri": input_uri})
                    inputs.pop(channel_name)
                else:
                    pass
            if inputs != {}:
                raise ValueError(
                    f"Following input channels={inputs.keys()} are not defined in input"
                    " channels definition. Please check the input channels definition."
                )
        else:
            for name, item in inputs.items():
                input_uri = _check_input_uri(item)
                res.append({"Name": name, "InputUri": input_uri})

        return res

    def _build_output_data_configs(self, job_name: str) -> List[Dict[str, str]]:
        """Build output data configs."""
        job_base_output_path = self._generate_job_base_output_path(job_name)

        # OSS URI for output channel will be mounted to directory
        # "/ml/output/{ChannelName}/" and the output OSS URI should be a "directory"
        def as_oss_dir_uri(uri: str):
            return uri if uri.endswith("/") else uri + "/"

        model_path = posixpath.join(
            job_base_output_path,
            DEFAULT_OUTPUT_MODEL_CHANNEL_NAME,
        )
        # Use checkpoints_path from user or construct a checkpoint path using default
        # output path.
        checkpoints_path = posixpath.join(
            job_base_output_path,
            DEFAULT_CHECKPOINT_CHANNEL_NAME,
        )
        # Output logs path
        logs_path = posixpath.join(
            job_base_output_path,
            DEFAULT_LOGS_CHANNEL_NAME,
        )

        # Record the output channels
        self._output_channels = []
        res = []
        output_channels_def = self.output_channel_definitions
        if output_channels_def:
            for channel in output_channels_def:
                channel_name = channel["Name"]
                channel_path = posixpath.join(
                    job_base_output_path,
                    channel_name,
                )
                res.append(
                    {
                        "Name": channel_name,
                        "OutputUri": as_oss_dir_uri(channel_path),
                    }
                )
                self._output_channels.append(channel_name)
        else:
            res = [
                {
                    "Name": DEFAULT_OUTPUT_MODEL_CHANNEL_NAME,
                    "OutputUri": as_oss_dir_uri(model_path),
                },
                {
                    "Name": DEFAULT_CHECKPOINT_CHANNEL_NAME,
                    "OutputUri": as_oss_dir_uri(checkpoints_path),
                },
                {
                    "Name": DEFAULT_LOGS_CHANNEL_NAME,
                    "OutputUri": as_oss_dir_uri(logs_path),
                },
            ]
            self._output_channels = [
                DEFAULT_OUTPUT_MODEL_CHANNEL_NAME,
                DEFAULT_CHECKPOINT_CHANNEL_NAME,
                DEFAULT_LOGS_CHANNEL_NAME,
            ]

        return res

    def fit(
        self, inputs: Dict[str, Any] = None, wait: bool = True, show_logs: bool = True
    ):
        """Submit a training job with the given input data.

        Args:
            inputs (Dict[str, Any]): A dictionary representing the input data for the
                training job. Each key/value pair in the dictionary is an input channel,
                the key is the channel name, and the value is the input data. The input
                data can be an OSS URI or a NAS URI object and will be mounted to the
                `/ml/input/data/{channel_name}` directory in the training container.
            wait (bool): Specifies whether to block until the training job is completed,
                either succeeded, failed, or stopped. (Default True).
            show_logs (bool): Specifies whether to show the logs produced by the
                training job (Default True).
        Raises:
            UnExpectedStatusException: If the training job fails.

        """
        inputs = inputs or dict()
        job_name = self._gen_job_display_name()
        training_job = self._fit(inputs=inputs, job_name=job_name)
        self._latest_training_job = training_job

        if wait:
            self.wait(show_logs=show_logs)

    def _fit(self, job_name, inputs: Dict[str, Any] = None):
        input_configs = self._build_input_data_configs(inputs)
        for c in input_configs:
            if "InputUri" in c and is_oss_uri(c["InputUri"]):
                c["InputUri"] = self._patch_default_oss_endpoint(c["InputUri"])
        output_configs = self._build_output_data_configs(job_name)
        for c in output_configs:
            if "OutputUri" in c and is_oss_uri(c["OutputUri"]):
                c["OutputUri"] = self._patch_default_oss_endpoint(c["OutputUri"])

        training_job_id = self.session.training_job_api.create(
            instance_count=self.instance_count,
            instance_type=self.instance_type,
            job_name=job_name,
            hyperparameters=self.hyperparameters,
            max_running_in_seconds=self.max_run_time,
            input_channels=input_configs,
            output_channels=output_configs,
            algorithm_name=self.algorithm_name,
            algorithm_version=self.algorithm_version,
            algorithm_provider=self.algorithm_provider,
            algorithm_spec=self.algorithm_spec,
        )
        training_job = _TrainingJob.get(training_job_id)
        print(
            f"View the job detail by accessing the console URI:"
            f" {training_job.console_uri}"
        )
        return training_job

    def model_data(self) -> str:
        """Model data output path.

        Returns:
            str: A string in OSS URI format refers to the output model of the submitted
                job.
        """
        if not self._latest_training_job:
            raise RuntimeError(
                "No TrainingJob for the estimator, output model data not found."
            )

        if not self._latest_training_job.is_succeeded():
            logger.warning(
                "The TrainingJob is currently not in a succeeded status, which means"
                " that the model data output may not be accessible."
            )

        if DEFAULT_OUTPUT_MODEL_CHANNEL_NAME not in self._output_channels:
            raise RuntimeError(
                f"Default output model channel={DEFAULT_OUTPUT_MODEL_CHANNEL_NAME} not"
                " found in the output channels definition. Please check the output"
                " channels definition."
            )

        res = self._latest_training_job.output_path(
            channel_name=DEFAULT_OUTPUT_MODEL_CHANNEL_NAME
        )
        return res

    def get_outputs_data(self) -> Dict[str, str]:
        """Show all outputs data paths.

        Returns:
            dict[str, str]: A dictionary of all outputs data paths.
        """
        if not self._latest_training_job:
            raise RuntimeError(
                "No TrainingJob for the estimator, output checkpoints data not found."
            )

        res = {}
        for channel_name in self._output_channels:
            res.update(
                {
                    channel_name: self._latest_training_job.output_path(
                        channel_name=channel_name
                    )
                }
            )
        return res


_TRAINING_LAUNCH_SCRIPT_TEMPLATE = textwrap.dedent(
    """\
#!/bin/sh

env

# change to working directory
if [ -n "$PAI_WORKING_DIR" ]; then
    echo "Change to Working Directory", $PAI_WORKING_DIR
    mkdir -p $PAI_WORKING_DIR && cd $PAI_WORKING_DIR
fi

# install requirements
if [ -e "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt"
    python -m pip install -r requirements.txt
fi

echo "User program launching"
echo "-----------------------------------------------------------------"

sh {0}
"""
)


class _TrainingEnv(object):
    ENV_PAI_HPS = "PAI_HPS"
    ENV_PAI_HPS_PREFIX = "PAI_HPS_"
    ENV_PAI_USER_ARGS = "PAI_USER_ARGS"
    ENV_PAI_INPUT_PREFIX = "PAI_INPUT_"
    ENV_PAI_OUTPUT_PREFIX = "PAI_OUTPUT_"
    ENV_PAI_WORKING_DIR = "PAI_WORKING_DIR"


class _TrainingJobConfig(object):
    WORKING_DIR = "/ml/usercode/"
    INPUT_CONFIG_DIR = "/ml/input/config/"
    INPUT_DATA_DIR = "/ml/input/data/"
    OUTPUT_DIR = "/ml/output/"


_ENV_NOT_ALLOWED_CHARS = re.compile(r"[^a-zA-Z0-9_]")


class _LocalTrainingJob(object):
    """A class that represents a local training job running with docker container."""

    def __init__(
        self,
        estimator: Estimator,
        inputs: Dict[str, Any],
        instance_type: str = None,
        temp_dir: str = None,
        job_name: str = None,
    ):
        self.estimator = estimator
        self.inputs = inputs
        self.tmp_dir = temp_dir or tempfile.mkdtemp()
        self.job_name = job_name
        self.instance_type = instance_type
        logger.info("Local TrainingJob temporary directory: {}".format(self.tmp_dir))
        self._container_run: ContainerRun = None

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if self._container_run:
            container = self._container_run.container
            container_name, container_id, status = (
                container.name,
                container.id,
                container.status,
            )
        else:
            container_name, container_id, status = None, None, None
        return f"LocalTrainingJob(container_name={container_name}, container_id={container_id}, status={status})"

    @property
    def session(self) -> Session:
        return self.estimator.session

    def prepare_env(self) -> Dict[str, str]:
        """Prepare environment variables for the training job."""

        # Hyperparameters environment variables
        def _normalize_name(name: str) -> str:
            # replace all non-alphanumeric characters with underscore
            return _ENV_NOT_ALLOWED_CHARS.sub("_", name).upper()

        env = {}
        user_args = []
        for name, value in self.estimator.hyperparameters.items():
            env[_TrainingEnv.ENV_PAI_HPS_PREFIX + _normalize_name(name)] = str(value)
            user_args.extend(["--" + name, shlex.quote(str(value))])
        env[_TrainingEnv.ENV_PAI_USER_ARGS] = shlex.join(user_args)
        env[_TrainingEnv.ENV_PAI_HPS] = json.dumps(
            {name: str(value) for name, value in self.estimator.hyperparameters.items()}
        )

        # Environments for input channel
        for name, value in self.inputs.items():
            if (is_oss_uri(value) and value.endswith("/")) or os.path.isdir(value):
                env[
                    _TrainingEnv.ENV_PAI_INPUT_PREFIX + _normalize_name(name)
                ] = posixpath.join(_TrainingJobConfig.INPUT_DATA_DIR, name)
            else:
                file_name = os.path.basename(value)
                env[
                    _TrainingEnv.ENV_PAI_INPUT_PREFIX + _normalize_name(name)
                ] = posixpath.join(_TrainingJobConfig.INPUT_DATA_DIR, name, file_name)

        # Environments for output channel.
        # By default, TrainingJob invoked by Estimator will have two output channels:
        # 'model' and 'checkpoints'
        output_channel = ["model", "checkpoints"]
        for name in output_channel:
            env[
                _TrainingEnv.ENV_PAI_OUTPUT_PREFIX + _normalize_name(name)
            ] = posixpath.join(_TrainingJobConfig.OUTPUT_DIR, name)

        env[_TrainingEnv.ENV_PAI_WORKING_DIR] = _TrainingJobConfig.WORKING_DIR
        return env

    def run(self):
        """Run estimator job in local with docker."""
        output_model_path = self.output_path()
        os.makedirs(output_model_path, exist_ok=True)
        volumes = {}

        tmp_dir = tempfile.mkdtemp()
        # 1. Prepare source code to directory /ml/usercode
        user_code_dir = os.path.join(self.tmp_dir, "user_code")
        if is_oss_uri(self.estimator.source_dir):
            raise RuntimeError("OSS source code is not supported in local training.")
        shutil.copytree(self.estimator.source_dir, user_code_dir)
        volumes[user_code_dir] = {
            "bind": _TrainingJobConfig.WORKING_DIR,
            "mode": "rw",
        }

        # 2. Prepare input data for training job.
        input_data = self.prepare_input_data()
        for host_path, container_path in input_data.items():
            volumes[host_path] = {
                "bind": container_path,
                "mode": "rw",
            }

        # 3. Prepare input config files, such as hyperparameters.json,
        # training-job.json, etc.
        input_config_path = os.path.join(tmp_dir, "config")
        os.makedirs(input_config_path, exist_ok=True)
        self.prepare_input_config(input_config_path=input_config_path)
        volumes[input_config_path] = {
            "bind": _TrainingJobConfig.INPUT_CONFIG_DIR,
            "mode": "rw",
        }

        execution_dir = os.path.join(tmp_dir, "config", "execution")
        os.makedirs(execution_dir, exist_ok=True)
        command_path = os.path.join(execution_dir, "command.sh")
        with open(command_path, "w") as f:
            f.write(self.estimator.command)
        launch_script_path = os.path.join(input_config_path, "launch.sh")
        with open(launch_script_path, "w") as f:
            f.write(
                _TRAINING_LAUNCH_SCRIPT_TEMPLATE.format(
                    posixpath.join(
                        _TrainingJobConfig.INPUT_CONFIG_DIR, "execution/command.sh"
                    )
                )
            )

        # 4. Config output model channel
        volumes[output_model_path] = {
            "bind": posixpath.join(_TrainingJobConfig.OUTPUT_DIR, "model"),
            "mode": "rw",
        }

        gpu_count = (
            -1 if self.instance_type.strip() == INSTANCE_TYPE_LOCAL_GPU else None
        )
        self._container_run = run_container(
            environment_variables=self.prepare_env(),
            image_uri=self.estimator.image_uri,
            entry_point=[
                "/bin/sh",
                posixpath.join(_TrainingJobConfig.INPUT_CONFIG_DIR, "launch.sh"),
            ],
            volumes=volumes,
            working_dir=_TrainingJobConfig.WORKING_DIR,
            gpu_count=gpu_count,
        )

    def prepare_input_config(self, input_config_path):
        """Prepare input config for TrainingJob, such as hyperparameters.json,
        trainingjob.json."""
        with open(os.path.join(input_config_path, "hyperparameters.json"), "w") as f:
            hps = self.estimator.hyperparameters or dict()
            f.write(json.dumps({k: str(v) for k, v in hps.items()}))

    def prepare_input_data(self) -> Dict[str, str]:
        """Prepare input data config."""
        input_data_configs = {}

        for name, input_data in self.inputs.items():
            local_channel_path = os.path.join(self.tmp_dir, f"input/data/{name}")
            os.makedirs(local_channel_path, exist_ok=True)
            input_data_configs[local_channel_path] = posixpath.join(
                _TrainingJobConfig.INPUT_DATA_DIR, name
            )
            if is_oss_uri(input_data):
                oss_uri_obj = OssUriObj(input_data)
                oss_bucket = self.session.get_oss_bucket(oss_uri_obj.bucket_name)
                os.makedirs(local_channel_path, exist_ok=True)
                download(
                    oss_uri_obj.object_key,
                    local_path=local_channel_path,
                    bucket=oss_bucket,
                )
                input_data_configs[local_channel_path] = posixpath.join(
                    _TrainingJobConfig.INPUT_DATA_DIR, name
                )
            else:
                # If the input data is local files, copy the input data to a
                # temporary directory.
                if not os.path.exists(input_data):
                    raise ValueError(
                        "Input data not exists: name={} input_data={}".format(
                            name, input_data
                        )
                    )
                elif os.path.isdir(input_data):
                    distutils.dir_util.copy_tree(input_data, local_channel_path)
                else:
                    shutil.copy(
                        input_data,
                        os.path.join(local_channel_path, os.path.basename(input_data)),
                    )

        return input_data_configs

    def wait(self, show_logs: bool = True):
        self._container_run.watch(show_logs=show_logs)

    def output_path(self, channel_name="model"):
        return os.path.join(self.tmp_dir, "output", f"{channel_name}/")

    def is_succeeded(self):
        """Return True if the training job is succeeded, otherwise return False."""
        return self._container_run.is_succeeded()


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


class TrainingJobChannel(object):
    def __init__(self, dataset_id=None, input_uri=None, name=None):
        self.dataset_id = dataset_id
        self.input_uri = input_uri
        self.name = name


class _TrainingJob(EntityBaseMixin):
    _schema_cls = TrainingJobSchema

    @config_default_session
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
        description: str = None,
        session: Session = None,
        **kwargs,
    ):
        super(_TrainingJob, self).__init__(session=session, **kwargs)
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
    @config_default_session
    def get(cls, training_job_id, session: Session = None) -> "_TrainingJob":
        res = session.training_job_api.get(training_job_id=training_job_id)
        return cls.from_api_object(res, session=session)

    @classmethod
    @config_default_session
    def list(
        cls,
        status=None,
        session: Session = None,
        page_size=50,
        page_number=1,
    ):
        res = session.training_job_api.list(
            status=status, page_size=page_size, page_number=page_number
        )
        return [cls.from_api_object(item, session=session) for item in res.items]

    def output_path(self, channel_name="model"):
        for output_channel in self.output_channels:
            if output_channel["Name"] == channel_name:
                return output_channel["OutputUri"]
        raise RuntimeError(
            f"Output model path not found: model_channel_name={channel_name}"
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
            while self.status not in TrainingJobStatus.completed_status():
                time.sleep(interval)
                self.session.training_job_api.refresh_entity(self.training_job_id, self)
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

    def _list_logs(self):
        page_number, page_offset = 1, 0
        # print training job logs.
        while not self._stop:
            res = self.session.training_job_api.list_logs(
                self.training_job_id,
                page_number=page_number,
                page_size=self.page_size,
            )
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
            res = self.session.training_job_api.list_logs(
                self.training_job_id,
                page_number=page_number,
                page_size=self.page_size,
            )
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
