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
from unittest import skipIf

import pytest

from pai.huggingface.estimator import HuggingFaceEstimator
from pai.huggingface.model import HuggingFaceModel
from tests.integration import BaseIntegTestCase
from tests.integration.utils import make_eas_service_name, t_context


class TestHuggingFaceEstimator(BaseIntegTestCase):
    """Test :class:`pai.huggingface.estimator.HuggingFaceEstimator`."""

    def test_base(self):
        est = HuggingFaceEstimator(
            command="python -c 'import transformers; print(transformers.__version__)'",
            instance_type="ecs.c6.large",
            transformers_version="4.29.2",
            base_job_name="sdk-hf-base",
        )
        self.assertIsNotNone(est.training_image_uri())
        est.fit()

    def test_latest_version(self):
        """Test training job with HuggingFaceFaceEstimator."""

        est = HuggingFaceEstimator(
            command="python -c 'import transformers; print(transformers.__version__)'",
            instance_type="ecs.c6.large",
            transformers_version="latest",
            base_job_name="sdk-hf-latest",
        )
        self.assertIsNotNone(est.training_image_uri())
        est.fit()

    @skipIf(
        t_context.pai_service_config.region_id.startswith("cn-"),
        "HuggingFaceEstimator github repo train only support oversea region for now.",
    )
    @pytest.mark.timeout(60 * 10)
    def test_git_repo_train(self):
        """Test training job with HuggingFaceEstimator."""

        git_config = {
            "repo": "https://github.com/huggingface/transformers.git",
            "branch": "v4.29.2",
        }
        hyperparameters = {
            "model_name_or_path": "bert-base-uncased",
            "output_dir": "/ml/output/model/",
            "task_name": "mrpc",
            "do_train": True,
            "do_eval": True,
            "max_seq_length": 128,
            "per_device_train_batch_size": 32,
            "learning_rate": 2e-5,
            "num_train_epochs": 3,
        }

        est = HuggingFaceEstimator(
            source_dir="./examples/pytorch/text-classification",
            git_config=git_config,
            command="python3 run_glue.py $PAI_USER_ARGS",
            instance_type="ecs.gn7i-c32g1.8xlarge",
            transformers_version="4.29.2",
            hyperparameters=hyperparameters,
            base_job_name="sdk-hf-git-repo-train",
        )

        est.fit()

        model_path = os.path.join(est.model_data(), "pytorch_model.bin")
        self.assertTrue(self.is_oss_object_exists(model_path))


class TestHuggingFaceModel(BaseIntegTestCase):
    """Test :class:`pai.huggingface.model.HuggingFaceModel`."""

    predictors = []

    @classmethod
    def tearDownClass(cls):
        super(TestHuggingFaceModel, cls).tearDownClass()
        for p in cls.predictors:
            p.delete_service()

    def test_huggingface_model_deploy(self):
        """Test deploying model with HuggingFaceModel."""
        m = HuggingFaceModel(
            command="python app.py",
            transformers_version="latest",
            environment_variables={
                "MODEL_ID": "distilbert-base-uncased-finetuned-sst-2-english",
                "TASK": "text-classification",
                "REVISION": "main",
            },
        )

        p = m.deploy(
            service_name=make_eas_service_name("huggingface_model_deploy"),
            instance_type="ecs.gn6i-c4g1.xlarge",
            options={
                "metadata.rpc.keepalive": 5000000,
                "features.eas.aliyun.com/extra-ephemeral-storage": "40Gi",
            },
        )

        self.predictors.append(p)
        self.assertTrue(p.service_name)

        res = p.predict({"data": ["it's so easy!"]})
        self.assertTrue(isinstance(res, dict))
        self.assertTrue(len(res) == 4)
        self.assertTrue(res["data"][0]["label"] == "POSITIVE")
