import logging
from typing import Any, Dict, List, Optional, Union

from pai.image import ImageScope, retrieve
from pai.model import (
    DEFAULT_SERVICE_PORT,
    ModelBase,
    ResourceConfig,
    container_serving_spec,
)
from pai.serializers import SerializerBase
from pai.session import Session, config_default_session

logger = logging.getLogger(__name__)


class HuggingFaceModel(ModelBase):
    """A HuggingFace ``Model`` that can be deployed in PAI to create a prediction service.

    A HuggingFaceModel instance includes the model artifact path and information on how to create
    prediction service in PAI. By calling the deploy() method, a prediction service is created in
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

    @config_default_session
    def __init__(
        self,
        model_data: Optional[str] = None,
        image_uri: Optional[str] = None,
        transformers_version: Optional[str] = None,
        command: Optional[str] = None,
        source_dir: Optional[str] = None,
        port: int = DEFAULT_SERVICE_PORT,
        environment_variables: Optional[Dict[str, str]] = None,
        requirements: Optional[List[str]] = None,
        requirements_path: Optional[str] = None,
        health_check: Optional[Dict[str, Any]] = None,
        session: Optional[Session] = None,
        **kwargs,
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
            source_dir (str, optional): Local path to the source code directory to be
                uploaded and used for the model server.
            port (int, optional): Expose port of the server in container, the prediction
                request will be forward to the port. The environment variable ``LISTENING_PORT``
                in the container will be set to this value.
            environment_variables (Dict[str, str], optional): Dictionary of environment
                variable key-value pairs to set on the running container.
            requirements (List[str], optional): A list of Python package dependency, it
                will be installed before the serving container run.
            requirements_path (str, optional): A absolute path to the requirements.txt in
                the container.
            health_check (Dict[str, Any], optional): The health check configuration. If it
                not set, A TCP readiness probe will be used to check the health of the
                HTTP server.
            session (:class:`pai.session.Session`, optional): A pai session object
                manages interactions with PAI REST API.

            **kwargs: Additional kwargs passed to the :class:`~pai.model.ModelBase` constructor.

        .. tip::

            You can find additional parameters for initializing this class at
            :class:`~pai.model.ModelBase`.
        """
        self._validate_args(
            image_uri=image_uri, transformers_verison=transformers_version
        )

        self.model_data = model_data
        self.image_uri = image_uri
        self.transformers_version = transformers_version
        self.command = command
        self.source_dir = source_dir
        self.port = port
        self.environment_variables = environment_variables
        self.requirements = requirements
        self.requirements_path = requirements_path
        self.health_check = health_check
        self.session = session
        inference_spec = dict()

        super(HuggingFaceModel, self).__init__(
            model_data=self.model_data,
            inference_spec=inference_spec,
            session=self.session,
            **kwargs,
        )

    def _validate_args(self, image_uri: str, transformers_verison: str) -> None:
        """Check if image_uri or transformers_version arguments are specified."""
        if not image_uri and not transformers_verison:
            raise ValueError(
                "transformers_version, and image_uri are both None. "
                "Specify either transformers_version or image_uri."
            )

    def serving_image_uri(self, instance_type: str) -> str:
        """Return the Docker image to use for serving.

        The deploy() method, that does the model deployment, calls this method to
        find the image to use for the inference service.

        Returns:
            str: The URI of the Docker image.
        """
        if self.image_uri:
            return self.image_uri

        framework_name = "huggingface"
        framework_version = self.transformers_version
        if self.session.is_gpu_inference_instance(instance_type):
            accelerator_type = "GPU"
        else:
            accelerator_type = "CPU"
        return retrieve(
            framework_name=framework_name,
            framework_version=framework_version,
            accelerator_type=accelerator_type,
            image_scope=ImageScope.INFERENCE,
        ).image_uri

    def deploy(
        self,
        service_name: Optional[str] = None,
        instance_type: Optional[str] = None,
        instance_count: Optional[int] = 1,
        resource_config: Optional[Union[Dict[str, int], ResourceConfig]] = None,
        resource_id: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        wait: bool = True,
        serializer: Optional["SerializerBase"] = None,
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

        self.image_uri = self.serving_image_uri(instance_type=instance_type)
        self.inference_spec = container_serving_spec(
            command=self.command,
            image_uri=self.image_uri,
            port=self.port,
            source_dir=self.source_dir,
            environment_variables=self.environment_variables,
            requirements=self.requirements,
            requirements_path=self.requirements_path,
            health_check=self.health_check,
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
        )
