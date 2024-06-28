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

from pai.common.utils import random_str
from pai.experiment import Experiment
from pai.tensorboard import TensorBoardStatus
from tests.integration import BaseIntegTestCase

tensorboard_path_suffix = "tensorboard/"


class TestExperiment(BaseIntegTestCase):
    def setUp(self):
        super(TestExperiment, self).setUp()
        self.artifact_uri = "oss://{}/sdktest/test_experiment/".format(
            self.default_session.oss_bucket.bucket_name
        )

    def test_create(self):
        # Init test data
        exp_name = "test_experiment_" + random_str(10)
        # Test create
        self.experiment = Experiment.create(
            artifact_uri=self.artifact_uri,
            name=exp_name,
        )
        self.assertEqual(self.experiment.name, exp_name)
        expected_tb_path = self.artifact_uri + tensorboard_path_suffix
        self.assertEqual(self.experiment.tensorboard_data(), expected_tb_path)

    def test_update(self):
        exp_name = "test_experiment_" + random_str(10)
        self.experiment = Experiment.create(
            artifact_uri=self.artifact_uri,
            name=exp_name,
        )
        # Test update
        exp_name = exp_name + "_updated"
        self.experiment.update(name=exp_name)
        self.assertEqual(self.experiment.name, exp_name)

    def test_list(self):
        exp_name = "test_experiment_" + random_str(10)
        self.experiment = Experiment.create(
            artifact_uri=self.artifact_uri,
            name=exp_name,
        )
        # Test list
        experiment_iterator = Experiment.list(name=exp_name)
        experiment_names = [e.name for e in experiment_iterator]
        self.assertEqual(len(experiment_names), 1)
        self.assertEqual(experiment_names[0], exp_name)

    def test_get(self):
        exp_name = "test_experiment_" + random_str(10)
        self.experiment = Experiment.create(
            artifact_uri=self.artifact_uri,
            name=exp_name,
        )
        # Test get
        exp1 = Experiment.get(experiment_id=self.experiment.experiment_id)
        self.assertEqual(self.experiment.name, exp1.name)
        self.assertEqual(self.experiment.experiment_id, exp1.experiment_id)
        self.assertEqual(self.experiment.tensorboard_data(), exp1.tensorboard_data())

    def test_tensorboard(self):
        exp_name = "test_experiment_" + random_str(10)
        self.experiment = Experiment.create(
            artifact_uri=self.artifact_uri,
            name=exp_name,
        )
        # Test tensorboard
        tb = self.experiment.tensorboard()
        self.assertIsNotNone(tb.app_uri)
        self.assertEqual(tb.status, TensorBoardStatus.Running)
        tb.delete()

    def tearDown(self):
        if hasattr(self, "experiment") and self.experiment:
            self.experiment.delete()
