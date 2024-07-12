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

import dataclasses
import enum
import shutil
from typing import Any, Dict, List, Optional, Tuple, Union

from ..common.logging import get_logger
from ..common.oss_utils import download, is_oss_uri
from ..job._training_job import (
    DEFAULT_OUTPUT_MODEL_CHANNEL_NAME,
    AlgorithmSpec,
    Channel,
    ComputeResource,
    DatasetConfig,
    ExperimentConfig,
    HyperParameterDefinition,
    InstanceSpec,
    ModelRecipeSpec,
    OssLocation,
    ResourceType,
    SpotSpec,
    TrainingJob,
    UriInput,
    UserVpcConfig,
    _TrainingJobSubmitter,
)
from ..predictor import Predictor
from ..session import get_default_session
from ._model import InferenceSpec, Model, RegisteredModel, ResourceConfig

logger = get_logger(__name__)


@dataclasses.dataclass
class RecipeInitKwargs(object):
    model_name: Optional[str]
    model_version: Optional[str]
    model_provider: Optional[str]
    method: Optional[str]
    # following fields are generated from model or overridden
    model_channel_name: Optional[str]
    model_uri: Optional[str]
    hyperparameters: Optional[Dict[str, Any]]
    hyperparameter_definitions: Optional[List[HyperParameterDefinition]]
    job_type: Optional[str]
    image_uri: Optional[str]
    source_dir: Optional[str]
    command: Union[str, List[str]]
    resource_id: Optional[str]
    instance_count: Optional[int]
    instance_type: Optional[str]
    instance_spec: Optional[InstanceSpec]
    max_run_time: Optional[int]
    labels: Optional[Dict[str, str]]
    requirements: Optional[List[str]]
    environments: Optional[Dict[str, str]]
    input_channels: Optional[List[Channel]]
    output_channels: Optional[List[Channel]]
    default_inputs: Optional[Union[UriInput, DatasetConfig]]
    customization: Optional[Dict[str, Any]]
    supported_instance_types: Optional[List[str]]


class ModelRecipeType(enum.Enum):
    TRAINING = "training"
    EVALUATION = "evaluation"
    COMPRESSION = "compression"

    @classmethod
    def supported_types(cls):
        return [cls.TRAINING, cls.EVALUATION, cls.COMPRESSION]


class ModelRecipe(_TrainingJobSubmitter):
    MODEL_CHANNEL_NAME = "model"

    def __init__(
        self,
        model_name: Optional[str] = None,
        model_version: Optional[str] = None,
        model_provider: Optional[str] = None,
        model_uri: Optional[str] = None,
        recipe_type: ModelRecipeType = ModelRecipeType.TRAINING,
        method: Optional[str] = None,
        source_dir: Optional[str] = None,
        model_channel_name: Optional[str] = "model",
        hyperparameters: Optional[Dict[str, Any]] = None,
        job_type: Optional[str] = None,
        image_uri: Optional[str] = None,
        command: Union[str, List[str]] = None,
        instance_count: Optional[int] = None,
        instance_type: Optional[str] = None,
        instance_spec: Optional[InstanceSpec] = None,
        resource_id: Optional[str] = None,
        resource_type: Optional[Union[str, ResourceType]] = None,
        spot_spec: Optional[SpotSpec] = None,
        user_vpc_config: Optional[UserVpcConfig] = None,
        labels: Optional[Dict[str, str]] = None,
        requirements: Optional[List[str]] = None,
        environments: Optional[Dict[str, str]] = None,
        experiment_config: Optional[ExperimentConfig] = None,
        input_channels: Optional[List[Channel]] = None,
        output_channels: Optional[List[Channel]] = None,
        max_run_time: Optional[int] = None,
        default_inputs: Optional[Dict[str, Any]] = None,
        base_job_name: Optional[str] = None,
        supported_instance_type: Optional[List[str]] = None,
        settings: Optional[Dict[str, Any]] = None,
    ):
        init_kwargs = self._init_kwargs(
            model_name=model_name,
            model_version=model_version,
            model_provider=model_provider,
            recipe_type=recipe_type,
            method=method,
            # get from model or override
            model_uri=model_uri,
            model_channel_name=model_channel_name,
            hyperparameters=hyperparameters,
            job_type=job_type,
            image_uri=image_uri,
            source_dir=source_dir,
            command=command,
            instance_count=instance_count,
            instance_spec=instance_spec,
            instance_type=instance_type,
            labels=labels,
            requirements=requirements,
            environments=environments,
            input_channels=input_channels,
            output_channels=output_channels,
            default_inputs=default_inputs,
            max_run_time=max_run_time,
            supported_instance_types=supported_instance_type,
        )
        self.model_name = init_kwargs.model_name
        self.model_version = init_kwargs.model_version
        self.model_provider = init_kwargs.model_provider
        self.method = init_kwargs.method
        self.model_uri = init_kwargs.model_uri
        self.model_channel_name = init_kwargs.model_channel_name
        self.job_type = init_kwargs.job_type
        self.hyperparameters = init_kwargs.hyperparameters
        self.image_uri = init_kwargs.image_uri
        self.command = init_kwargs.command
        self.source_dir = init_kwargs.source_dir
        self.default_inputs = init_kwargs.default_inputs
        self.customization = init_kwargs.customization
        self.supported_instance_types = init_kwargs.supported_instance_types
        self.input_channels = init_kwargs.input_channels
        self.output_channels = init_kwargs.output_channels
        self.hyperparameter_definitions = init_kwargs.hyperparameter_definitions

        super().__init__(
            resource_type=resource_type,
            base_job_name=base_job_name,
            experiment_config=experiment_config,
            resource_id=resource_id,
            user_vpc_config=user_vpc_config,
            spot_spec=spot_spec,
            instance_type=init_kwargs.instance_type,
            instance_count=init_kwargs.instance_count,
            instance_spec=init_kwargs.instance_spec,
            max_run_time=init_kwargs.max_run_time,
            environments=init_kwargs.environments,
            requirements=init_kwargs.requirements,
            labels=init_kwargs.labels,
            settings=settings,
        )

    @classmethod
    def _init_kwargs(
        cls,
        model_name: Optional[str] = None,
        model_version: Optional[str] = None,
        model_provider: Optional[str] = None,
        recipe_type: ModelRecipeType = ModelRecipeType.TRAINING,
        method: Optional[str] = None,
        model_channel_name: Optional[str] = "model",
        model_uri: Optional[str] = None,
        hyperparameters: Optional[Dict[str, Any]] = None,
        job_type: Optional[str] = None,
        image_uri: Optional[str] = None,
        source_dir: Optional[str] = None,
        command: Union[str, List[str]] = None,
        instance_count: Optional[int] = None,
        instance_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        instance_spec: Optional[InstanceSpec] = None,
        max_run_time: Optional[int] = None,
        labels: Optional[Dict[str, str]] = None,
        requirements: Optional[List[str]] = None,
        environments: Optional[Dict[str, str]] = None,
        input_channels: List[Channel] = None,
        output_channels: List[Channel] = None,
        default_inputs: Optional[Union[UriInput, DatasetConfig]] = None,
        supported_instance_types: Optional[List[str]] = None,
    ) -> RecipeInitKwargs:
        model = (
            RegisteredModel(
                model_name=model_name,
                model_version=model_version,
                model_provider=model_provider,
            )
            if model_name
            else None
        )
        model_recipe_spec = (
            model.get_recipe_spec(recipe_type=recipe_type, method=method)
            if model
            else None
        )
        model_uri = model_uri or (model and model.uri)
        customization = None
        if not model_recipe_spec:
            return RecipeInitKwargs(
                model_name=model_name,
                model_version=model_version,
                model_provider=model_provider,
                method=method,
                model_channel_name=model_channel_name,
                model_uri=model_uri,
                hyperparameters=hyperparameters,
                job_type=job_type,
                image_uri=image_uri,
                source_dir=source_dir,
                command=command,
                instance_count=instance_count,
                instance_type=instance_type,
                instance_spec=instance_spec,
                resource_id=resource_id,
                labels=labels,
                requirements=requirements,
                environments=environments,
                input_channels=input_channels,
                output_channels=output_channels,
                max_run_time=max_run_time,
                default_inputs=default_inputs,
                customization=customization,
                supported_instance_types=supported_instance_types,
                hyperparameter_definitions=None,
            )
        if not model_uri:
            input_ = next(
                (
                    item
                    for item in model_recipe_spec.inputs
                    if item.name == model_channel_name
                ),
                None,
            )

            if input_:
                if isinstance(input_, UriInput):
                    model_uri = input_.input_uri
                else:
                    logger.warning(
                        "Input channel '%s' is not a URI input: %s",
                        model_channel_name,
                        type(input_),
                    )

        if not default_inputs and model_recipe_spec.inputs:
            default_inputs = {}
            for item in model_recipe_spec.inputs:
                if isinstance(item, UriInput):
                    default_inputs[item.name] = item.input_uri
                else:
                    default_inputs[item.name] = item
        algorithm_spec = cls._get_algorithm_spec(model_recipe_spec)
        supported_instance_types = (
            supported_instance_types or model_recipe_spec.supported_instance_types
        )
        hyperparameter_definitions = None
        if algorithm_spec:
            if (
                not source_dir
                and algorithm_spec.code_dir
                and isinstance(algorithm_spec.code_dir.location_value, OssLocation)
            ):
                oss_location = algorithm_spec.code_dir.location_value
                if oss_location.endpoint:
                    source_dir = f"oss://{oss_location.bucket}.{oss_location.endpoint}/{oss_location.key.lstrip('/')}"
                else:
                    source_dir = (
                        f"oss://{oss_location.bucket}/{oss_location.key.lstrip('/')}"
                    )
            image_uri = image_uri or algorithm_spec.image
            command = command or algorithm_spec.command
            job_type = job_type or algorithm_spec.job_type
            input_channels = input_channels or algorithm_spec.input_channels
            output_channels = output_channels or algorithm_spec.output_channels
            customization = algorithm_spec.customization
            supported_instance_types = (
                supported_instance_types or algorithm_spec.supported_channel_types
            )
            hyperparameter_definitions = algorithm_spec.hyperparameter_definitions

        instance_type, instance_spec, instance_count = cls._get_compute_resource_config(
            instance_type=instance_type,
            instance_spec=instance_spec,
            instance_count=instance_count,
            resource_id=resource_id,
            compute_resource=model_recipe_spec.compute_resource,
            supported_instance_types=supported_instance_types,
        )
        hyperparameters = hyperparameters or {}
        hyperparameters = {
            **{
                hp.name: hp.default_value
                for hp in (
                    algorithm_spec and algorithm_spec.hyperparameter_definitions or {}
                )
                if hp.default_value is not None and hp.default_value != ""
            },
            **{hp.name: hp.value for hp in model_recipe_spec.hyperparameters},
            **hyperparameters,
        }
        requirements = requirements or model_recipe_spec.requirements
        environments = environments or model_recipe_spec.environments

        return RecipeInitKwargs(
            model_name=model_name,
            model_version=model_version,
            model_provider=model_provider,
            method=method,
            model_uri=model_uri,
            model_channel_name=model_channel_name,
            hyperparameters=hyperparameters,
            job_type=job_type,
            image_uri=image_uri,
            source_dir=source_dir,
            command=command,
            instance_count=instance_count,
            instance_spec=instance_spec,
            instance_type=instance_type,
            max_run_time=max_run_time,
            labels=labels,
            requirements=requirements,
            environments=environments,
            input_channels=input_channels,
            output_channels=output_channels,
            resource_id=resource_id,
            default_inputs=default_inputs,
            customization=customization,
            supported_instance_types=supported_instance_types,
            hyperparameter_definitions=hyperparameter_definitions,
        )

    @staticmethod
    def _get_compute_resource_config(
        instance_type: str,
        instance_count: int,
        instance_spec: InstanceSpec,
        resource_id: str,
        compute_resource: ComputeResource,
        supported_instance_types: List[str],
    ) -> Tuple[str, InstanceSpec, int]:
        if resource_id:
            if instance_type:
                logger.warning(
                    "The instance type is ignored when resource_id is provided."
                )
            instance_spec = instance_spec or (
                compute_resource and compute_resource.instance_spec
            )
            if not instance_spec:
                raise ValueError(
                    "Running in dedicated resource group, please provide instance spec"
                    " for the training job."
                )
            instance_count = (
                instance_count
                or (compute_resource and compute_resource.instance_count)
                or 1
            )
        else:
            if instance_spec:
                logger.warning(
                    "The instance spec is ignored when resource_id is not provided."
                )
            instance_type = instance_type or (
                compute_resource and compute_resource.ecs_spec
            )
            if not instance_type:
                if not supported_instance_types:
                    raise ValueError(
                        "No instance type is specified for the training job"
                    )
                else:
                    instance_type = supported_instance_types[0]
            instance_count = (
                instance_count or (compute_resource and compute_resource.ecs_count) or 1
            )
        return instance_type, instance_spec, instance_count

    @staticmethod
    def _get_algorithm_spec(model_recipe_spec: ModelRecipeSpec) -> AlgorithmSpec:
        session = get_default_session()
        if model_recipe_spec.algorithm_spec:
            return model_recipe_spec.algorithm_spec

        if not model_recipe_spec.algorithm_name:
            raise ValueError(
                "Both algorithm_name and algorithm_spec are not provided "
                "in the model training spec."
            )

        algo = session.algorithm_api.get_by_name(
            algorithm_name=model_recipe_spec.algorithm_name,
            algorithm_provider=model_recipe_spec.algorithm_provider,
        )
        raw_algo_version_spec = session.algorithm_api.get_version(
            algorithm_id=algo["AlgorithmId"],
            algorithm_version=model_recipe_spec.algorithm_version,
        )
        return AlgorithmSpec.model_validate(raw_algo_version_spec["AlgorithmSpec"])

    def _build_algorithm_spec(
        self, code_input, inputs: Dict[str, Any]
    ) -> AlgorithmSpec:
        algorithm_spec = AlgorithmSpec(
            command=(
                self.command
                if isinstance(self.command, list)
                else ["sh", "-c", self.command]
            ),
            image=self.image_uri,
            job_type=self.job_type,
            code_dir=code_input,
            output_channels=self.output_channels
            or self._default_training_output_channels(),
            input_channels=self.input_channels
            or [
                Channel(name=channel_name, required=False)
                for channel_name in inputs.keys()
            ],
            customization=self.customization,
        )
        return algorithm_spec

    def retrieve_scripts(self, local_path: str) -> str:
        """Retrieve the training scripts to the local file system.

        Args:
            local_path (str): The local path where the training scripts are saved.

        Returns:
            str: The local path where the training scripts are saved.

        """

        if not self.source_dir:
            raise RuntimeError("Source code is not available for the training job.")

        if is_oss_uri(self.source_dir):
            return download(self.source_dir, local_path, un_tar=True)
        else:
            shutil.copytree(self.source_dir, local_path)
            return local_path

    def run(
        self,
        inputs: Optional[Dict[str, Union[str, DatasetConfig]]] = None,
        outputs: Optional[Dict[str, Union[str, DatasetConfig]]] = None,
        wait: bool = True,
        job_name: Optional[str] = None,
        show_logs: bool = True,
    ) -> TrainingJob:
        """Start a training job with the given inputs.

        Args:
            inputs (Dict[str, Union[str, DatasetConfig]], optional): A dictionary of inputs
                used in the training job. The keys are the channel name and the values are
                the URIs of the input data. If not specified, the default inputs will be
                used.
            wait (bool): Whether to wait for the job to complete before returning. Default
                to True.
            job_name (str, optional): The name of the training job. If not provided, a default
                job name will be generated.
            show_logs (bool): Whether to show the logs of the training job. Default to True.

        Returns:
            :class:`pai.training.TrainingJob`: A submitted training job.

        """
        job_name = self.job_name(job_name)

        inputs = inputs or dict()
        code_input = self._build_code_input(job_name, source_dir=self.source_dir)
        algo_spec = self._build_algorithm_spec(
            code_input=code_input,
            inputs=inputs,
        )

        if self.model_channel_name not in inputs:
            inputs[self.model_channel_name] = self.model_uri

        if len(inputs.keys()) == 1 and self.model_channel_name in inputs:
            default_inputs = self.default_inputs
        else:
            default_inputs = None

        inputs = self.build_inputs(
            inputs=inputs,
            input_channels=algo_spec.input_channels,
            default_inputs=default_inputs,
        )
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
            # experiment_config=self.experiment_config if self.experiment_config else None,
            labels=self.labels,
            wait=wait,
            show_logs=show_logs,
        )


class ModelTrainingRecipe(ModelRecipe):
    """A recipe used to train a model."""

    def __init__(
        self,
        model_name: Optional[str] = None,
        model_version: Optional[str] = None,
        model_provider: Optional[str] = None,
        model_uri: Optional[str] = None,
        method: Optional[str] = None,
        source_dir: Optional[str] = None,
        model_channel_name: Optional[str] = "model",
        hyperparameters: Optional[Dict[str, Any]] = None,
        job_type: Optional[str] = None,
        image_uri: Optional[str] = None,
        command: Union[str, List[str]] = None,
        instance_count: Optional[int] = None,
        instance_type: Optional[str] = None,
        spot_spec: Optional[SpotSpec] = None,
        instance_spec: Optional[InstanceSpec] = None,
        resource_id: Optional[str] = None,
        resource_type: Optional[Union[str, ResourceType]] = None,
        user_vpc_config: Optional[UserVpcConfig] = None,
        labels: Optional[Dict[str, str]] = None,
        requirements: Optional[List[str]] = None,
        environments: Optional[Dict[str, str]] = None,
        experiment_config: Optional[ExperimentConfig] = None,
        input_channels: Optional[List[Channel]] = None,
        output_channels: Optional[List[Channel]] = None,
        max_run_time: Optional[int] = None,
        default_training_inputs: Optional[Dict[str, Any]] = None,
        base_job_name: Optional[str] = None,
        **kwargs,
    ):
        """Initialize a ModelTrainingRecipe object.

        Args:
            model_name (str, optional): The name of the registered model. Default to
                None.
            model_version (str, optional): The version of the registered model. Default
                to None.
            model_provider (str, optional): The provider of the registered model.
                Optional values are "pai", "huggingface" or None. If None, list
                registered models in the workspace of the current session. Default to
                None.
            method (str, optional): The training method used to select the
                specific training recipe while the registered model contains multiple
                model training specs. Default to None.
            model_channel_name (str, optional): The name of the model channel. Default to
                "model".
            model_uri (str, optional): The URI of the input pretrained model. If the URI
                is not provided, the model from the registered model will be used.
                Default to None.
            hyperparameters (dict, optional): A dictionary of hyperparameters used in
                the training job. Default to None.
            job_type (str, optional): The type of the job, supported values are "PyTorch",
                "TfJob", "XGBoostJob" etc.
            image_uri (str, optional): The URI of the Docker image. Default to None.
            source_dir (str, optional): The source code using in the training job, which
                is a directory containing the training script or an OSS URI. Default to
                None.
            command (str or list, optional): The command to execute in the training job.
                Default to None.
            requirements (list, optional): A list of Python requirements used to install
                the dependencies in the training job. Default to None.
            instance_count (int, optional): The number of instances to use for training.
                Default to None.
            instance_type (str, optional): The instance type to use for training. Default
                to None.
            instance_spec (:class:`pai.model.InstanceSpec`, optional): The resource config
                for each instance of the training job. The dedicated resource group must
                be provided when the instance spec is set. Default to None.
            resource_id (str, optional): The ID of the resource group used to run the
                training job. Default to None.
            spot_spec (:class:`pai.model.SpotSpec`, optional): The spot instance config
                used to run the training job. If provided, spot instance will be used.
            resource_type (str, optional): The resource type used to run the training job.
                By default, general computing resource is used. If the resource_type is
                'Lingjun', Lingjun computing resource is used.
            user_vpc_config (:class:`pai.model.UserVpcConfig`, optional): The VPC
                configuration used to enable the job instance to connect to the
                specified user VPC. Default to None.
            environments (dict, optional): A dictionary of environment variables used in
                the training job. Default to None.
            experiment_config (:class:`pai.model.ExperimentConfig`, optional): The
                experiment
            labels (dict, optional): A dictionary of labels used to tag the training job.
                Default to None.

        """
        super().__init__(
            model_name=model_name,
            model_version=model_version,
            model_provider=model_provider,
            model_uri=model_uri,
            method=method,
            recipe_type=ModelRecipeType.TRAINING,
            source_dir=source_dir,
            model_channel_name=model_channel_name,
            hyperparameters=hyperparameters,
            job_type=job_type,
            image_uri=image_uri,
            command=command,
            instance_count=instance_count,
            instance_type=instance_type,
            instance_spec=instance_spec,
            resource_type=resource_type,
            resource_id=resource_id,
            spot_spec=spot_spec,
            user_vpc_config=user_vpc_config,
            labels=labels,
            requirements=requirements,
            environments=environments,
            experiment_config=experiment_config,
            input_channels=input_channels,
            output_channels=output_channels,
            max_run_time=max_run_time,
            default_inputs=default_training_inputs,
            base_job_name=base_job_name,
            **kwargs,
        )

    def train(
        self,
        inputs: Optional[Dict[str, Union[str, DatasetConfig]]] = None,
        outputs: Optional[Dict[str, Union[str, DatasetConfig]]] = None,
        wait: bool = True,
        job_name: Optional[str] = None,
        show_logs: bool = True,
    ) -> TrainingJob:
        """Start a training job with the given inputs.

        Args:
            inputs (Dict[str, Union[str, DatasetConfig]], optional): A dictionary of inputs
                used in the training job. The keys are the channel name and the values are
                the URIs of the input data. If not specified, the default inputs will be
                used.
            outputs (Dict[str, Union[str, DatasetConfig]], optional): A dictionary of outputs
                used in the training job. The keys are the channel name and the values are
                the URIs or Dataset of the output data.
            wait (bool): Whether to wait for the job to complete before returning. Default
                to True.
            job_name (str, optional): The name of the training job. If not provided, a default
                job name will be generated.
            show_logs (bool): Whether to show the logs of the training job. Default to True.
                Note that the logs will be shown only when the `wait` is set to True.

        Returns:
            :class:`pai.training.TrainingJob`: A submitted training job.

        """
        return self.run(
            inputs=inputs,
            outputs=outputs,
            wait=wait,
            job_name=job_name,
            show_logs=show_logs,
        )

    def deploy(
        self,
        service_name: str,
        instance_type: Optional[str] = None,
        instance_count: int = 1,
        resource_config: Optional[Union[ResourceConfig, Dict[str, int]]] = None,
        resource_id: str = None,
        options: Optional[Dict[str, Any]] = None,
        wait=True,
        inference_spec: Optional[InferenceSpec] = None,
        **kwargs,
    ) -> Predictor:
        """Deploy the training job output model as a online prediction service.

        Args:
            service_name (str): The name of the online prediction service.
            instance_type (str, optional): The instance type used to run the service.
            instance_count (int, optional): The number of instances used to run the
                service. Default to 1.
            resource_config (Union[ResourceConfig, Dict[str, int]], optional): The resource
                config for the service. Default to None.
            resource_id (str, optional): The ID of the resource group used to run the
                service. Default to None.
            options (Dict[str, Any], optional): The options used to deploy the service.
                Default to None.
            wait (bool, optional): Whether to wait for the service endpoint to be ready.
            inference_spec (:class:`pai.model.InferenceSpec`, optional): The inference
                spec used to deploy the service. If not provided, the `inference_spec` of
                the model will be used. Default to None.
            kwargs: Additional keyword arguments used to deploy the service.

        Returns:
            :class:`pai.predictor.Predictor`: A predictor object refers to the created
                service.
        """
        if not inference_spec and self.model_name:
            model = RegisteredModel(
                model_name=self.model_name,
                model_version=self.model_version,
                model_provider=self.model_provider,
            )
            inference_spec = model.inference_spec

        if not inference_spec:
            raise RuntimeError("No inference_spec is available for model deployment.")

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
            options=options,
            wait=wait,
            **kwargs,
        )
        return p

    def model_data(self):

        if not self._training_jobs:
            raise RuntimeError("No training job is available for deployment.")

        if not self.latest_job.is_succeeded():
            logger.warning(
                "The latest training job is not succeeded, the deployment may not work."
            )

        return self.latest_job.output_path(
            channel_name=DEFAULT_OUTPUT_MODEL_CHANNEL_NAME
        )
