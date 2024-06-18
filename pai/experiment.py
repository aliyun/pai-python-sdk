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
from typing import Iterator, Optional

from .common.logging import get_logger
from .session import Session, get_default_session
from .tensorboard import TensorBoard

logger = get_logger(__name__)


class Experiment(object):
    """An experiment is a collection of runs. It can be used to compare the
    performance of different training jobs. You can compare the metrics of
    different training jobs in a same experiment by one single TensorBoard.

    You can create an experiment by calling `Experiment.create`.

    When you create a training job, you can specify the experiment name to
    make the relationship between the job and the experiment. In this case,
    the training job will use the artifact_uri of experiment as default output
    path, so you do not need to specify the output path of the training job
    anymore.

    Example:
        experiment = Experiment.create(
            artifact_uri="oss://bucket/path",
            name="my_experiment",
        )
        est = Estimator(
            source_dir="./train/src/",
            command="python train.py",
            image_uri = training_image_uri,
            instance_type="ecs.c6.xlarge",
            hyperparameters={
                "n_estimators": 50
            },
            experiment_config=ExperimentConfig(
                experiment_name="my_experiment",
            )
        )

        est.fit(inputs={
            "train": "oss://{YOUR_BUCKET_NAME}/path/to/train-data",
            "test": "oss://{YOUR_BUCKET_NAME}/path/to/test-data",
        })

    """

    def __init__(
        self,
        experiment_id: str,
        name: str,
        artifact_uri: str,
        session: Optional[Session] = None,
    ):
        """Experiment constructor.

        Args:
            experiment_id (str): The UUID of the experiment. It is generated from the PAI service.
            name (str): The name of experiment is unique within the workspace. The experiment name must adhere to
                the following naming convention: The maximum length is 63 characters. It must start with an uppercase
                or lowercase letter or a number, and may include hyphens(-) and underscores(_).
            artifact_uri (str): An OSS URI which is the default base path to store the output of the job in the
                experiment, including model files and TensorBoard logs.
            session (Session, optional): A PAI session instance used for communicating
                with PAI service.
        """

        self.session = session or get_default_session()
        self.experiment_id = experiment_id
        self.name = name
        self.artifact_uri = artifact_uri
        self._api_object = session.experiment_api.get(experiment_id)

    @classmethod
    def create(
        cls,
        artifact_uri: str,
        name: str,
        session: Optional[Session] = None,
    ) -> "Experiment":
        """Create experiment.
        Args:
            artifact_uri (str): Specifies an OSS URI to store the output of the job in the experiment.
            name (str): The name of the experiment. The name must be unique within the workspace.
            session (Session): The session to be used.
        Returns:
            Experiment: The created experiment.
        """
        session = session or get_default_session()
        experiment_id = session.experiment_api.create(
            artifact_uri=artifact_uri, name=name, workspace_id=session.workspace_id
        )
        experiment = Experiment(
            experiment_id=experiment_id,
            name=name,
            artifact_uri=artifact_uri,
            session=session,
        )
        return experiment

    @classmethod
    def get(cls, experiment_id: str) -> "Experiment":
        session = get_default_session()
        experiment = session.experiment_api.get(experiment_id)
        return Experiment(
            experiment_id=experiment_id,
            name=experiment["Name"],
            artifact_uri=experiment["ArtifactUri"],
            session=session,
        )

    @classmethod
    def get_by_name(
        cls, name: str, session: Optional[Session] = None
    ) -> Optional["Experiment"]:
        """Get experiment by name.

        Args:
            name (str): The name of the experiment.
            session (Session): The session to be used.

        Returns:
            Experiment: The experiment with the specified name.

        """
        exp = next(
            (exp for exp in cls.list(name=name, session=session) if exp.name == name),
            None,
        )
        return exp

    def update(
        self,
        name: str,
    ) -> "Experiment":
        """Update experiment name.
        Args:
            name (str): New experiment name.
        Returns:
            Experiment: The updated experiment.
        """
        self.session.experiment_api.update(self.experiment_id, name=name)
        self.name = name
        return self

    def delete(self):
        """Delete experiment."""
        self.session.experiment_api.delete(self.experiment_id)

    @classmethod
    def list(
        cls,
        name: str = None,
        session: Optional[Session] = None,
    ) -> Iterator["Experiment"]:
        """List experiments.
        Args:
            name (str): Filter by name.
            session (Session): The session to be used.
        Return:
            Iterator[Experiment]: Experiment iterator.
        """
        session = session or get_default_session()
        page_size = 50
        page_number = 1
        while True:
            result = session.experiment_api.list(
                name=name,
                page_size=page_size,
                page_number=page_number,
            ).items
            if not result:
                break

            for item in result:
                yield cls(
                    session=session,
                    experiment_id=item["ExperimentId"],
                    name=item["Name"],
                    artifact_uri=item["ArtifactUri"],
                )
            page_number += 1

    def tensorboard_data(self) -> str:
        """Output TensorBoard logs path.

        Returns:
            str: A string in OSS URI format refers to the tensorboard log of experiment.
        """
        return self._api_object.get("TensorboardLogUri")

    def tensorboard(self, wait=True) -> "TensorBoard":
        """Launch a TensorBoard instance with the tensorboard logs path from the current experiment.
        Args:
            wait (bool): Wait for TensorBoard to be ready.
        """
        from pai.tensorboard import TensorBoard

        source_type = "experiment"
        res = self.session.tensorboard_api.list(
            source_type=source_type,
            source_id=self.experiment_id,
        )

        if res.items:
            if len(res.items) > 1:
                logger.warning(
                    "Found multiple TensorBoard instances for the experiment, use the first one."
                )
            tb_id = res.items[0]["TensorboardId"]
            tb = TensorBoard(tb_id, session=self.session)
            tb.start(wait=wait)
        else:
            tb = TensorBoard.create(
                uri=self.tensorboard_data(),
                wait=wait,
                display_name=self.name + "_TensorBoard",
                source_type=source_type,
                source_id=self.experiment_id,
                session=self.session,
            )
        webbrowser.open(tb.app_uri)
        return tb
