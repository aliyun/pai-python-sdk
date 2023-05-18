import logging
from typing import Any, Dict, Optional

from pai.estimator import Estimator
from pai.image import ImageScope, retrieve
from pai.session import Session

logger = logging.getLogger(__name__)


class ModelScopeEstimator(Estimator):
    """Handle training of custom ModelScope model.

    The ModelScope Estimator is optimized to run a ModelScope training
    script in the PAI Training Service with a specific image.

    Example::

        est = ModelScopeEstimator(
            source_dir="./train/src/",
            command="python train.py",
            modelscope_version = 'latest',
            instance_type="ecs.c6.xlarge",
        )

        est.fit()

        print(est.model_data())

    """

    def __init__(
        self,
        command: str,
        source_dir: Optional[str] = None,
        image_uri: Optional[str] = None,
        modelscope_version: Optional[str] = None,
        hyperparameters: Optional[Dict[str, Any]] = None,
        base_job_name: Optional[str] = None,
        checkpoints_path: Optional[str] = None,
        output_path: Optional[str] = None,
        instance_type: str = "ecs.c6.xlarge",
        instance_count: int = 1,
        session: Optional[Session] = None,
        **kwargs,
    ):
        """Initialize a ModelScope Estimator.

        Args:
            command (str): The command used to run the training job.
            source_dir (str, optional): The local source code directory used in the
                training job. The directory will be packaged and uploaded to an OSS
                bucket, then downloaded to the `/ml/usercode` directory in the training
                job container. If there is a `requirements.txt` file in the source code
                directory, the corresponding dependencies will be installed before the
                training script runs.
            image_uri (str, optional): If specified, the estimator will use this image
                in the training job, instead of selecting the appropriate PAI official
                image based on modelscope_version. It can be an image provided by PAI
                or a user customized image. To view the images provided by PAI, please
                refer to the document:
                https://help.aliyun.com/document_detail/202834.htm.

                If ``modelscope_version`` is ``None``, then ``image_uri`` is required.
                If also ``None``, then a ``ValueError`` will be raised.
            modelscope_version (str, optional): Modelscope version you want to use for
                executing your model training code. Defaults to ``None``. Required unless
                ``image_uri`` is provided.
            hyperparameters (dict, optional): A dictionary that represents the
                hyperparameters used in the training job. The hyperparameters will be
                stored in the `/ml/input/config/hyperparameters.json` as a JSON
                dictionary in the training container.
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
            instance_type (str): The machine instance type used to run the training job.
                To view the supported machine instance types, please refer to the
                document:
                https://help.aliyun.com/document_detail/171758.htm#section-55y-4tq-84y.
                If the instance_type is "local", the training job is executed locally
                using docker.
            instance_count (int): The number of machines used to run the training job.
            session (:class:`pai.session.Session`, optional): A pai session object manages
                interactions with PAI REST API.

            **kwargs: Additional kwargs passed to the :class:`~pai.estimator.Estimator`
                constructor.

        .. tip::

            You can find additional parameters for initializing this class at
            :class:`~pai.estimator.Estimator`.
        """
        self._validate_image_uri(
            image_uri=image_uri, modelscope_version=modelscope_version
        )
        self.image_uri = image_uri
        self.modelscope_version = modelscope_version

        super(ModelScopeEstimator, self).__init__(
            image_uri=self.image_uri,
            command=command,
            source_dir=source_dir,
            hyperparameters=hyperparameters,
            base_job_name=base_job_name,
            checkpoints_path=checkpoints_path,
            output_path=output_path,
            instance_type=instance_type,
            instance_count=instance_count,
            session=session,
            **kwargs,
        )

    def _validate_image_uri(self, image_uri: str, modelscope_version: str) -> None:
        """Check if image_uri or modelscope_version arguments are specified."""
        if not image_uri and not modelscope_version:
            raise ValueError(
                "modelscope_version, and image_uri are both None. "
                "Specify either modelscope_version or image_uri."
            )

    def training_image_uri(self) -> str:
        """Return the Docker image to use for training.

        The :meth:`~pai.estimator.Estimator.fit` method, which does the model training,
        calls this method to find the image to use for model training.

        Returns:
            str: The URI of the Docker image.
        """
        if self.image_uri:
            return self.image_uri
        framework_name = "modelscope"
        framework_version = self.modelscope_version
        if self.session.is_gpu_training_instance(self.instance_type):
            accelerator_type = "GPU"
        else:
            accelerator_type = "CPU"
        return retrieve(
            framework_name=framework_name,
            framework_version=framework_version,
            accelerator_type=accelerator_type,
            image_scope=ImageScope.TRAINING,
        ).image_uri
