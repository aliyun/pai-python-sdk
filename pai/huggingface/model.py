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

from typing import Any, Dict, List, Optional, Union

from ..common.logging import get_logger
from ..common.utils import to_semantic_version
from ..image import ImageLabel
from ..model._model import (
    DefaultServiceConfig,
    ModelBase,
    ResourceConfig,
    StorageConfigBase,
    container_serving_spec,
)
from ..serializers import SerializerBase
from ..session import Session, get_default_session

logger = get_logger(__name__)


class HuggingFaceModel(ModelBase):
    """A HuggingFace ``Model`` that can be deployed in PAI to create a prediction service.

    A HuggingFaceModel instance includes the model artifact path and information on how to create
    prediction service in PAI. By calling the deploy method, a prediction service is created in
    PAI and a :class:`pai.predictor.Predictor` instance is returned that can be used to make
    prediction to the service.

    Example::

        # Initialize a HuggingFaceModel.
        m: HuggingFaceModel = HuggingFaceModel(
            model_data="oss://bucket-name/path/to/model",
            source_dir="./serving/src/",
            command="python serving.py",
            transformers_version="latest",
        )

        # Deploy the model to create an online prediction service.
        p: Predictor = m.deploy(
            service_name="hf_bert_serving",
            instance_type="ecs.gn6i-c4g1.xlarge",
            instance_count=1,
            options={
                "metadata.rpc.keepalive": 5000000,
                "features.eas.aliyun.com/extra-ephemeral-storage":"40Gi",
            },
        )

        # Make prediction by sending the data to the online prediction service.
        result = p.predict("weather is good")

    """

    def __init__(
        self,
        model_data: Optional[str] = None,
        image_uri: Optional[str] = None,
        transformers_version: Optional[str] = None,
        command: Optional[str] = None,
        source_dir: Optional[str] = None,
        git_config: Optional[Dict[str, str]] = None,
        port: Optional[int] = None,
        environment_variables: Optional[Dict[str, str]] = None,
        requirements: Optional[List[str]] = None,
        requirements_path: Optional[str] = None,
        health_check: Optional[Dict[str, Any]] = None,
        storage_configs: Optional[List[StorageConfigBase]] = None,
        session: Optional[Session] = None,
    ):
        """Initialize a HuggingFace Model.

        Args:
            model_data (str): An OSS URI or file path specifies the location of the
                model. If model_data is a local file path, it will be uploaded to OSS
                bucket before deployment or model registry.
            image_uri (str, optional): If specified, the model will use this image to
                create the online prediction service, instead of selecting the appropriate
                PAI official image based on transformers_version.

                If ``transformers_version`` is ``None``, then ``image_uri`` is required.
                If also ``None``, then a ``ValueError`` will be raised.
            transformers_version (str, optional): Transformers version you want to use for
                executing your model serving code. Defaults to ``None``. Required unless
                ``image_uri`` is provided.
            command (str): The command used to launch the Model server.
            source_dir (str, optional): A relative path or an absolute path to the source
                code directory used to load model and launch the Model server, it will be
                uploaded to the OSS bucket and mounted to the container. If there is a
                ``requirements.txt`` file under the directory, it will be installed before
                the prediction server started.

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
                Including ``repo``, ``branch``, ``commit``, ``username``, ``password`` and
                ``token``. The ``repo`` is required. All other fields are optional. ``repo``
                specifies the Git repository. If you don't provide ``branch``, the default
                value 'master' is used. If you don't provide ``commit``, the latest commit
                in the specified branch is used. ``username``, ``password`` and ``token``
                are for authentication purpose. For example, the following config:

                .. code:: python

                    git_config = {
                        'repo': 'https://github.com/huggingface/transformers.git',
                        'branch': 'main',
                        'commit': '5ba0c332b6bef130ab6dcb734230849c903839f7'
                    }

                results in cloning the repo specified in 'repo', then checking out the
                'main' branch, and checking out the specified commit.
            port (int, optional): Expose port of the server in container, the prediction
                request will be forward to the port. The environment variable ``LISTENING_PORT``
                in the container will be set to this value. If not set, the default
                value is 8000.
            environment_variables (Dict[str, str], optional): Dictionary of environment
                variable key-value pairs to set on the running container.
            requirements (List[str], optional): A list of Python package dependency, it
                will be installed before the serving container run.
            requirements_path (str, optional): A absolute path to the requirements.txt in
                the container.
            health_check (Dict[str, Any], optional): The health check configuration. If it
                not set, A TCP readiness probe will be used to check the health of the
                Model server.
            storage_configs (List[StorageConfigBase], optional): A list of storage configs
                used to mount the storage to the container. The storage can be OSS, NFS,
                SharedMemory, or NodeStorage, etc.
            session (:class:`pai.session.Session`, optional): A pai session object
                manages interactions with PAI REST API.

            **kwargs: Additional kwargs passed to the :class:`~pai.model.ModelBase` constructor.

        .. tip::

            You can find additional parameters for initializing this class at
            :class:`~pai.model.ModelBase`.
        """
        self._validate_args(
            image_uri=image_uri, transformers_version=transformers_version
        )
        session = session or get_default_session()

        self.model_data = model_data
        self.image_uri = image_uri
        self.transformers_version = transformers_version
        self.command = command
        self.source_dir = source_dir
        self.git_config = git_config
        self.port = port or DefaultServiceConfig.listen_port
        self.environment_variables = environment_variables
        self.requirements = requirements
        self.requirements_path = requirements_path
        self.health_check = health_check
        self.storage_configs = storage_configs

        super(HuggingFaceModel, self).__init__(
            model_data=self.model_data,
            session=session or get_default_session(),
        )
        # Check image_uri and transformers_version
        self.serving_image_uri()

    def _validate_args(self, image_uri: str, transformers_version: str) -> None:
        """Check if image_uri or transformers_version arguments are specified."""
        if not image_uri and not transformers_version:
            raise ValueError(
                "transformers_version, and image_uri are both None. "
                "Specify either transformers_version or image_uri."
            )

    def serving_image_uri(self) -> str:
        """Return the Docker image to use for serving.

        The :meth:`pai.huggingface.model.HuggingFaceModel.deploy` method, that does the
        model deployment, calls this method to find the image to use for the inference
        service.

        Returns:
            str: The URI of the Docker image.
        """
        if self.image_uri:
            return self.image_uri

        labels = [
            ImageLabel.OFFICIAL_LABEL,
            ImageLabel.EAS_LABEL,
            ImageLabel.PROVIDER_PAI_LABEL,
            ImageLabel.DEVICE_TYPE_GPU,
        ]
        # TODO: Filter images by instance type (CPU/GPU)
        # Filter images by Transformers version
        if self.transformers_version == "latest":
            latest_version = self._get_latest_tf_version_for_inference()
            labels.append(ImageLabel.framework_version("Transformers", latest_version))
        else:
            labels.append(
                ImageLabel.framework_version("Transformers", self.transformers_version)
            )

        name = "huggingface-inference:"
        resp = self.session.image_api.list(
            name=name,
            labels=labels,
            workspace_id=0,
            verbose=True,
        )

        if resp.total_count == 0:
            raise ValueError(
                "No official image found for Transformers version:"
                f" {self.transformers_version}. Currently supported versions are:"
                f" {self._get_supported_tf_versions_for_inference()}"
            )

        image = resp.items[0]["ImageUri"]
        return image

    def _get_supported_tf_versions_for_inference(self) -> List[str]:
        """Return the list of supported Transformers versions for inference."""

        labels = [
            ImageLabel.OFFICIAL_LABEL,
            ImageLabel.EAS_LABEL,
            ImageLabel.PROVIDER_PAI_LABEL,
            ImageLabel.DEVICE_TYPE_GPU,
            ImageLabel.framework_version("Transformers", "*"),
        ]
        name = "huggingface-inference:"
        list_images = self.session.image_api.list(
            name=name,
            labels=labels,
            verbose=True,
            workspace_id=0,
        ).items

        res = []
        for image in list_images:
            for label in image["Labels"]:
                if (
                    label["Key"] == "system.framework.Transformers"
                    and label["Value"] not in res
                ):
                    res.append(label["Value"])
        res.sort(key=lambda x: to_semantic_version(x))
        return res

    def _get_latest_tf_version_for_inference(self) -> str:
        """Return the latest transformers version for inference."""
        res = self._get_supported_tf_versions_for_inference()
        return max(
            res,
            key=lambda x: to_semantic_version(x),
        )

    def deploy(
        self,
        service_name: str,
        instance_type: Optional[str] = None,
        instance_count: Optional[int] = 1,
        resource_config: Optional[Union[Dict[str, int], ResourceConfig]] = None,
        resource_id: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        wait: bool = True,
        serializer: Optional["SerializerBase"] = None,
        **kwargs,
    ):
        """Deploy an online prediction service.

        Args:
            service_name (str, optional): Name for the online prediction service. The name
                must be unique in a region.
            instance_type (str, optional): Type of the machine instance, for example,
                'ecs.c6.large'. For all supported instance, view the appendix of the
                link:
                https://help.aliyun.com/document_detail/144261.htm?#section-mci-qh9-4j7
            instance_count (int): Number of instance request for the service deploy
                (Default 1).
            resource_config (Union[ResourceConfig, Dict[str, int]], optional):
                Request resource for each instance of the service. Required if
                instance_type is not set.  Example config:

                .. code::

                    resource_config = {
                        "cpu": 2,       # The number of CPUs that each instance requires
                        "memory: 4000,  # The amount of memory that each instance
                                        # requires, must be an integer, Unit: MB.
                        # "gpu": 1,         # The number of GPUs that each instance
                                            # requires.
                        # "gpu_memory": 3   # The amount of GPU memory that each
                                            # instance requires, must be an integer,
                                            # Unit: GB.
                    }

            resource_id (str, optional): The ID of the resource group. The service
                can be deployed to ``public resource group`` and
                ``dedicated resource group``.

                * If `resource_id` is not specified, the service is deployed
                    to public resource group.
                * If the service deployed in a dedicated resource group, provide
                    the parameter as the ID of the resource group. Example:
                    "eas-r-6dbzve8ip0xnzte5rp".

            options (Dict[str, Any], optional): Advanced deploy parameters used
                to create the online prediction service.
            wait (bool): Whether the call should wait until the online prediction
                service is ready (Default True).
            serializer (:class:`pai.predictor.serializers.BaseSerializer`, optional): A
                serializer object used to serialize the prediction request and
                deserialize the prediction response.
        Returns:
            :class:`pai.predictor.Predictor` : A PAI ``Predictor`` instance used for
                making prediction to the prediction service.
        """
        image_uri = self.serving_image_uri()
        self.inference_spec = container_serving_spec(
            command=self.command,
            image_uri=image_uri,
            port=self.port,
            source_dir=self.source_dir,
            git_config=self.git_config,
            environment_variables=self.environment_variables,
            requirements=self.requirements,
            requirements_path=self.requirements_path,
            health_check=self.health_check,
            storage_configs=self.storage_configs,
            session=self.session,
        )

        return super(HuggingFaceModel, self).deploy(
            service_name=service_name,
            instance_type=instance_type,
            instance_count=instance_count,
            resource_config=resource_config,
            resource_id=resource_id,
            options=options,
            wait=wait,
            serializer=serializer,
            **kwargs,
        )
