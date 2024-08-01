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

import os
import posixpath
import re
from unittest import skipUnless

import pytest

from pai.common.oss_utils import upload
from pai.common.utils import random_str
from pai.estimator import AlgorithmEstimator, Estimator
from pai.experiment import Experiment
from pai.image import retrieve
from pai.job._training_job import ExperimentConfig, ResourceType, SpotSpec
from pai.session import get_default_session
from tests.integration import BaseIntegTestCase
from tests.integration.utils import t_context
from tests.test_data import test_data_dir


class TestEstimator(BaseIntegTestCase):
    job_output_path = None

    @classmethod
    def setUpClass(cls):
        super(TestEstimator, cls).setUpClass()
        oss_bucket = get_default_session().oss_bucket  # type oss2.Bucket

        cls.breast_cancer_train_data_uri = cls.upload_file(
            oss_bucket=oss_bucket,
            location="sdk-test/test_data/breast_cancer_data/train/",
            file=os.path.join(test_data_dir, "breast_cancer_data/train.csv"),
        )
        cls.breast_cancer_test_data_uri = cls.upload_file(
            oss_bucket=oss_bucket,
            location="sdk-test/test_data/breast_cancer_data/test/",
            file=os.path.join(test_data_dir, "breast_cancer_data/test.csv"),
        )

    def test_xgb_train(self):
        xgb_image_uri = retrieve("xgboost", framework_version="latest").image_uri

        est = Estimator(
            image_uri=xgb_image_uri,
            source_dir=os.path.join(test_data_dir, "xgb_train"),
            command="python train.py",
            hyperparameters={
                "n_estimators": 50,
                "objective": "binary:logistic",
                "max_depth": 5,
                "eval_metric": "auc",
            },
            instance_type="ecs.c6.large",
        )

        est.fit(
            inputs={
                "train": self.breast_cancer_train_data_uri,
                "test": self.breast_cancer_test_data_uri,
            },
        )
        model_path = os.path.join(os.path.join(est.model_data(), "model.json"))
        self.assertTrue(self.is_oss_object_exists(model_path))

    def test_output_config(self):
        xgb_image_uri = retrieve("xgboost", framework_version="latest").image_uri
        sess = get_default_session()

        est = Estimator(
            image_uri=xgb_image_uri,
            source_dir=os.path.join(test_data_dir, "xgb_train"),
            command="python train.py",
            hyperparameters={
                "n_estimators": 50,
                "objective": "binary:logistic",
                "max_depth": 5,
                "eval_metric": "auc",
            },
            instance_type="ecs.c6.large",
        )
        test_output_path = (
            f"oss://{sess.oss_bucket.bucket_name}/sdk-test/test-output/{random_str(6)}/"
        )
        est.fit(
            inputs={
                "train": self.breast_cancer_train_data_uri,
                "test": self.breast_cancer_test_data_uri,
            },
            outputs={
                "model": test_output_path,
            },
        )

        self.assertEqual(test_output_path, est.model_data())
        model_path = os.path.join(os.path.join(test_output_path, "model.json"))
        self.assertTrue(self.is_oss_object_exists(model_path))

    @skipUnless(t_context.support_spot_instance, "Skip spot instance test")
    def test_use_spot_instance(self):
        xgb_image_uri = retrieve("xgboost", framework_version="latest").image_uri
        est = Estimator(
            command="echo helloworld",
            instance_type="ml.gu7ef.8xlarge-gu100",
            image_uri=xgb_image_uri,
            spot_spec=SpotSpec(
                spot_strategy="SpotWithPriceLimit",
                spot_discount_limit=0.5,
            ),
            resource_type=ResourceType.Lingjun,
        )
        est.fit()

    def test_torch_run(self):
        torch_image_uri = retrieve("pytorch", framework_version="1.12").image_uri
        est = Estimator(
            image_uri=torch_image_uri,
            command="python -c 'import torch; print(torch.__version__);'",
            instance_type="ecs.c6.large",
            base_job_name="torch_run_",
        )

        est.fit(
            inputs={
                "training": self.breast_cancer_train_data_uri,
                "test": self.breast_cancer_test_data_uri,
            },
            wait=False,
        )

        tb = est.tensorboard()
        self.assertIsNotNone(tb.app_uri)
        tb.delete()

    def test_checkpoints(self):
        sess = get_default_session()
        torch_image_uri = retrieve("pytorch", framework_version="1.12").image_uri
        filename = "output.txt"
        command = (
            f"echo helloworld > /ml/output/checkpoints/{filename} && echo 'helloworld'"
        )
        checkpoint_path = f"oss://{sess.oss_bucket.bucket_name}/sdk-test/test-checkpoints/{random_str(6)}/"

        est = Estimator(
            image_uri=torch_image_uri,
            command=command,
            instance_type="ecs.c6.large",
            base_job_name="torch_run_",
            checkpoints_path=checkpoint_path,
        )

        est.fit(
            inputs={
                "training": self.breast_cancer_train_data_uri,
                "test": self.breast_cancer_test_data_uri,
            },
            wait=True,
        )
        self.assertEqual(checkpoint_path, est.checkpoints_data())
        self.assertTrue(
            self.is_oss_object_exists(posixpath.join(checkpoint_path, filename))
        )

    def test_max_compute_input(self):
        image_uri = retrieve("xgboost", framework_version="latest").image_uri
        est = Estimator(
            image_uri=image_uri,
            source_dir=os.path.join(test_data_dir, "read_mc_table"),
            command="python run.py",
            instance_type="ecs.c6.large",
            base_job_name="test_read_mc_table",
        )
        est.fit(inputs={"train": "odps://pai_online_project/tables/wumai_data"})


class TestAlgorithmEstimator(BaseIntegTestCase):
    """Test :class:`pai.estimator.AlgorithmEstimator`."""

    @pytest.mark.timeout(60 * 10)
    def test_algo_train(self):
        """Test training job with AlgorithmEstimator."""
        region = self.default_session.region_id

        est = AlgorithmEstimator(
            algorithm_name="easycv_detection_yolox",
            algorithm_version="v0.1.0",
            algorithm_provider="pai",
            hyperparameters={
                "model_size_type": "nano",
                "learning_rate": "0.001",
                "max_epochs": "5",
                "last_fixed_lr_epochs": "15",
                "warmup_epochs": "2",
                "image_scale": "640,640",
                "train_batch_size": "8",
                "num_workers_per_gpu": "1",
                "save_ckpt_epoch_interval": "1",
                "eval_interval": "1",
                "log_interval": "10",
                "num_visualizations": "20",
                "score_threshold": "0.5",
                "resume_from": "",
            },
            base_job_name="easycv_detection_yolox_training",
        )

        est.fit(
            inputs={
                "pretrained_model": f"oss://pai-quickstart-{region}/easycv/models/detection/yolox/v0.1.0/pth/yolox_nano_epoch_300/",
                "train": f"oss://pai-quickstart-{region}/easycv/datasets/small_coco/train_data/",
                "validation": f"oss://pai-quickstart-{region}/easycv/datasets/small_coco/val_data/",
            },
        )

        outputs_data = est.get_outputs_data()
        self.assertTrue(isinstance(outputs_data, dict))
        self.assertTrue(outputs_data)
        self.assertTrue(len(outputs_data) == 2)

        model_path = os.path.join(outputs_data["model"], "epoch_5_export.pt")
        checkpoint_path = os.path.join(outputs_data["checkpoints"], "epoch_5.pth")
        self.assertTrue(self.is_oss_object_exists(model_path))
        self.assertTrue(self.is_oss_object_exists(checkpoint_path))


@skipUnless(t_context.has_docker, "Estimator local train requires docker.")
class TestEstimatorLocalRun(BaseIntegTestCase):
    def test_local_data(self):
        image_uri = retrieve("xgboost", framework_version="latest").image_uri
        train_file = os.path.join(test_data_dir, "breast_cancer_data/train.csv")
        test_file = os.path.join(test_data_dir, "breast_cancer_data/test.csv")

        est = Estimator(
            image_uri=image_uri,
            source_dir=os.path.join(test_data_dir, "xgb_train"),
            command="python train.py $PAI_USER_ARGS",
            hyperparameters={
                "n_estimators": 50,
                "objective": "binary:logistic",
                "max_depth": 5,
                "eval_metric": "auc",
            },
            instance_type="local",
        )

        est.fit(
            inputs={
                "train": train_file,
                "test": test_file,
            },
        )
        self.assertTrue(os.path.exists(os.path.join(est.model_data(), "model.json")))

    def test_remote_data(self):
        image_uri = retrieve("xgboost", framework_version="latest").image_uri
        train_data_uri = upload(
            os.path.join(test_data_dir, "breast_cancer_data/train.csv"),
            oss_path="sdk-test/test_data/breast_cancer_data/train/",
        )
        test_data_uri = upload(
            os.path.join(test_data_dir, "breast_cancer_data/test.csv"),
            oss_path="sdk-test/test_data/breast_cancer_data/test/",
        )

        est = Estimator(
            image_uri=image_uri,
            source_dir=os.path.join(test_data_dir, "xgb_train"),
            command="python train.py $PAI_USER_ARGS",
            hyperparameters={
                "n_estimators": 50,
                "objective": "binary:logistic",
                "max_depth": 5,
                "eval_metric": "auc",
            },
            instance_type="local",
        )

        est.fit(
            inputs={
                "train": train_data_uri,
                "test": test_data_uri,
            },
        )
        self.assertTrue(os.path.exists(os.path.join(est.model_data(), "model.json")))


@skipUnless(
    t_context.has_docker and t_context.has_gpu,
    "Estimator local gpu train requires docker and gpu.",
)
class TestEstimatorLocalRunGPU(BaseIntegTestCase):
    def test(self):
        image_uri = retrieve("xgboost", framework_version="latest").image_uri

        est = Estimator(
            image_uri=image_uri,
            command="python train.py",
            source_dir=os.path.join(test_data_dir, "local_gpu_torch"),
            instance_type="local_gpu",
        )
        est.fit()


class TestTrainWithExperimentConfig(BaseIntegTestCase):
    def setUp(self):
        exp_name = f"sdk_estimator_test_{random_str(6)}"
        self.experiment = Experiment.create(
            artifact_uri="oss://{}/sdktest/test_experiment/sdk_estimator_test_experiment/".format(
                self.default_session.oss_bucket.bucket_name
            ),
            name=exp_name,
        )
        self.image_uri = retrieve(
            "pytorch",
            "1.12",
            accelerator_type="GPU",
        ).image_uri
        self.command = "python train.py"
        self.source_dir = os.path.join(test_data_dir, "experiment_train")
        self.instance_type = "ecs.c6.large"
        tensorboard_data_escaped = re.escape(self.experiment.tensorboard_data())
        self.tensorboard_path_regex_pattern = f"^{tensorboard_data_escaped}[a-z0-9]+/$"

    def test_train_with_experiment_config(self):
        est = Estimator(
            image_uri=self.image_uri,
            command=self.command,
            source_dir=self.source_dir,
            instance_type=self.instance_type,
            experiment_config=ExperimentConfig(
                experiment_id=self.experiment.experiment_id,
            ),
        )
        est.fit()

        tensorboard_path = est.tensorboard_data()
        self.assertRegex(tensorboard_path, self.tensorboard_path_regex_pattern)
        artifact_uri_escaped = re.escape(self.experiment.artifact_uri)
        model_path_regex_pattern = f"^{artifact_uri_escaped}[a-z0-9]+/model/$"
        self.assertRegex(est.model_data(), model_path_regex_pattern)

    def test_train_with_output_and_experiment_config(self):
        output_path = "oss://{}/sdktest/test_experiment/output_config_path/".format(
            self.default_session.oss_bucket.bucket_name
        )
        est = Estimator(
            image_uri=self.image_uri,
            command=self.command,
            source_dir=self.source_dir,
            instance_type=self.instance_type,
            output_path=output_path,
            experiment_config=ExperimentConfig(
                experiment_id=self.experiment.experiment_id,
            ),
        )
        est.fit()

        output_escaped = re.escape(output_path)
        model_path_regex_pattern = f"^{output_escaped}[a-z0-9_]+/model/$"
        self.assertRegex(est.model_data(), model_path_regex_pattern)
        tensorboard_path = est.tensorboard_data()
        self.assertRegex(tensorboard_path, self.tensorboard_path_regex_pattern)

    def tearDown(self):
        self.experiment.delete()
