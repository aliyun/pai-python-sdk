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

from typing import Any, Dict, List, Optional

from ..api.image import ImageLabel
from ..common.logging import get_logger
from ..common.utils import to_semantic_version
from ..estimator import Estimator
from ..session import Session

logger = get_logger(__name__)


class HuggingFaceEstimator(Estimator):
    """Handle training of custom HuggingFace model.

    The HuggingFace Estimator is optimized to run a HuggingFace training
    script in the PAI Training Service with a specific image.

    Example::

        est = HuggingFaceEstimator(
            source_dir="./train/src/",
            command="python train.py",
            transformers_version = 'latest',
            instance_type="ecs.c6.xlarge",
        )

        est.fit()

        print(est.model_data())

    """

    def __init__(
        self,
        command: str,
        source_dir: Optional[str] = None,
        git_config: Optional[Dict[str, str]] = None,
        image_uri: Optional[str] = None,
        transformers_version: Optional[str] = None,
        hyperparameters: Optional[Dict[str, Any]] = None,
        base_job_name: Optional[str] = None,
        checkpoints_path: Optional[str] = None,
        output_path: Optional[str] = None,
        instance_type: Optional[str] = None,
        instance_count: int = 1,
        session: Optional[Session] = None,
        **kwargs,
    ):
        """Initialize a HuggingFace Estimator constructor.

        Args:
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
                        'repo': 'https://github.com/huggingface/transformers.git',
                        'branch': 'main',
                        'commit': '5ba0c332b6bef130ab6dcb734230849c903839f7'
                    }

                results in cloning the git repo specified in 'repo', then checking out
                the 'main' branch, and checking out the specified commit.
            image_uri (str, optional): If specified, the estimator will use this image
                in the training job, instead of selecting the appropriate PAI official
                image based on transformers_version. It can be an image provided by PAI
                or a user customized image. To view the images provided by PAI, please
                refer to the document:
                https://help.aliyun.com/document_detail/202834.htm.

                If ``transformers_version`` is ``None``, then ``image_uri`` is required.
                If also ``None``, then a ``ValueError`` will be raised.
            transformers_version (str, optional): Transformers version you want to use for
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
            image_uri=image_uri, transformers_version=transformers_version
        )
        self.image_uri = image_uri
        self.transformers_version = transformers_version

        super(HuggingFaceEstimator, self).__init__(
            image_uri=self.image_uri,
            command=command,
            source_dir=source_dir,
            git_config=git_config,
            hyperparameters=hyperparameters,
            base_job_name=base_job_name,
            checkpoints_path=checkpoints_path,
            output_path=output_path,
            instance_type=instance_type,
            instance_count=instance_count,
            session=session,
            **kwargs,
        )
        # Check image_uri and transformers_version
        self.training_image_uri()

    def _validate_image_uri(self, image_uri: str, transformers_version: str) -> None:
        """Check if image_uri or transformers_version arguments are specified."""
        if not image_uri and not transformers_version:
            raise ValueError(
                "transformers_version, and image_uri are both None. "
                "Specify either transformers_version or image_uri."
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

        labels = [
            ImageLabel.OFFICIAL_LABEL,
            ImageLabel.DLC_LABEL,
            ImageLabel.PROVIDER_COMMUNITY_LABEL,
            ImageLabel.DEVICE_TYPE_GPU,
            ImageLabel.framework_version("PyTorch", "*"),
        ]

        # Filter images by Transformers version
        if self.transformers_version == "latest":
            latest_version = self._get_latest_tf_version_for_training()
            labels.append(ImageLabel.framework_version("Transformers", latest_version))
        else:
            labels.append(
                ImageLabel.framework_version("Transformers", self.transformers_version)
            )

        resp = self.session.image_api.list(
            labels=labels,
            workspace_id=0,
            verbose=True,
        )

        if resp.total_count == 0:
            raise ValueError(
                "No official image found for Transformers version:"
                f" {self.transformers_version}. Currently supported versions are:"
                f" {self._get_supported_tf_versions_for_training()}"
            )

        image = resp.items[0]["ImageUri"]
        return image

    def _get_supported_tf_versions_for_training(self) -> List[str]:
        """Return the list of supported Transformers versions for training."""
        label_keys = "system.framework.Transformers"
        label_filter = [
            ImageLabel.OFFICIAL_LABEL,
            ImageLabel.DLC_LABEL,
            ImageLabel.PROVIDER_COMMUNITY_LABEL,
            ImageLabel.DEVICE_TYPE_GPU,
            ImageLabel.framework_version("PyTorch", "*"),
            ImageLabel.framework_version("Transformers", "*"),
        ]
        list_image_labels = self.session.image_api.list_labels(
            label_keys=label_keys,
            label_filter=label_filter,
            workspace_id=0,
        )

        res = []
        for label in list_image_labels:
            if label["Value"] not in res:
                res.append(label["Value"])

        res.sort(key=lambda x: to_semantic_version(x))
        return res

    def _get_latest_tf_version_for_training(self) -> str:
        """Return the latest Transformers version for training."""
        res = self._get_supported_tf_versions_for_training()
        return max(
            res,
            key=lambda x: to_semantic_version(x),
        )
