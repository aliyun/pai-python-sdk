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

from pai.common.utils import random_str
from pai.experiment import Experiment
from pai.image import retrieve
from pai.job import ExperimentConfig
from pai.processor import Processor
from pai.session import get_default_session
from tests.integration import BaseIntegTestCase
from tests.test_data import SCRIPT_DIR_PATH, test_data_dir


class TestProcessor(BaseIntegTestCase):
    job_output_path = None

    @classmethod
    def setUpClass(cls):
        super(TestProcessor, cls).setUpClass()
        oss_bucket = get_default_session().oss_bucket  # type oss2.Bucket

        cls.breast_cancer_test_data_uri = cls.upload_file(
            oss_bucket=oss_bucket,
            location="sdk-test/test_data/breast_cancer_data/test/",
            file=os.path.join(test_data_dir, "breast_cancer_data/test.csv"),
        )
        cls.processing_output_uri = cls.get_oss_uri(
            oss_bucket=oss_bucket,
            location="sdk-test/output/processing/",
        )

    def test_processing_run(self):
        image_uri = retrieve("pytorch", framework_version="1.12").image_uri
        processor = Processor(
            image_uri=image_uri,
            source_dir=SCRIPT_DIR_PATH,
            command="python main.py --output_path=/ml/output/flag",
            instance_type="ecs.c6.large",
            base_job_name="processing",
        )

        processor.run(
            inputs={"test": self.breast_cancer_test_data_uri},
            outputs={"flag": self.processing_output_uri},
        )

        success_flag = os.path.join(self.processing_output_uri, "output.txt")

        self.assertIsNotNone(self.is_oss_object_exists(success_flag))

    def test_train_with_experiment_config(self):
        exp_name = f"sdk_estimator_test_{random_str(6)}"
        self.experiment = Experiment.create(
            artifact_uri="oss://{}/sdktest/test_experiment/sdk_estimator_test_experiment/".format(
                self.default_session.oss_bucket.bucket_name
            ),
            name=exp_name,
        )

        image_uri = retrieve("pytorch", framework_version="1.12").image_uri
        processor = Processor(
            image_uri=image_uri,
            source_dir=SCRIPT_DIR_PATH,
            command="python main.py --output_path=/ml/output/flag",
            instance_type="ecs.c6.large",
            base_job_name="processing",
            experiment_config=ExperimentConfig(
                experiment_id=self.experiment.experiment_id
            ),
        )

        processor.run(
            inputs={"test": self.breast_cancer_test_data_uri},
            outputs={"flag": self.processing_output_uri},
        )

        self.assertIsNotNone(processor.latest_job)
        self.assertIsNotNone(processor.latest_job.training_job_name)
        self.assertIsNotNone(processor.latest_job.experiment_config)
