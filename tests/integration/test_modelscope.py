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

from pai.modelscope.estimator import ModelScopeEstimator
from pai.modelscope.model import ModelScopeModel
from tests.integration import BaseIntegTestCase
from tests.integration.utils import make_eas_service_name, t_context


class TestModelScopeEstimator(BaseIntegTestCase):
    """Test :class:`pai.modelscope.estimator.ModelScopeEstimator`."""

    def test_base(self):
        est = ModelScopeEstimator(
            command="python -c 'import modelscope; print(modelscope.__version__)'",
            instance_type="ecs.c6.large",
            modelscope_version="1.12.0",
            base_job_name="sdk-ms-train",
        )
        self.assertIsNotNone(est.training_image_uri())
        est.fit()

    def test_latest_version(self):
        est = ModelScopeEstimator(
            command="python -c 'import modelscope; print(modelscope.__version__)'",
            instance_type="ecs.c6.large",
            modelscope_version="latest",
            base_job_name="sdk-ms-latest",
        )
        self.assertIsNotNone(est.training_image_uri())
        est.fit()

    @skipIf(
        t_context.pai_service_config.region_id.startswith("cn-"),
        "ModelScope github repo train only support oversea region for now.",
    )
    @pytest.mark.timeout(60 * 25)
    def test_git_repo_train(self):
        """Test training job with ModelScopeEstimator."""

        git_config = {
            "repo": "https://github.com/modelscope/modelscope.git",
            "branch": "v1.6.1",
        }
        hyperparameters = {
            "task": "text-classification",
            "model": "damo/nlp_structbert_backbone_base_std",
            "train_dataset_name": "clue",
            "train_subset_name": "tnews",
            "first_sequence": "sentence",
            "preprocessor.label": "label",
            "model.num_labels": 15,
            "labels": "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14",
            "preprocessor": "sen-cls-tokenizer",
            "use_model_config": True,
            "max_epochs": 1,
            "train.dataloader.workers_per_gpu": 0,
            "evaluation.dataloader.workers_per_gpu": 0,
            "train.optimizer.lr": 1e-5,
            "eval_metrics": "seq-cls-metric",
            "work_dir": "/ml/output/model/",
        }

        est = ModelScopeEstimator(
            source_dir="./examples/pytorch/text_classification",
            git_config=git_config,
            command="python3 finetune_text_classification.py $PAI_USER_ARGS",
            instance_type="ecs.gn7i-c32g1.8xlarge",
            modelscope_version="1.6.1",
            hyperparameters=hyperparameters,
            base_job_name="sdk-ms-git-repo",
        )

        est.fit()

        model_path = os.path.join(est.model_data(), "epoch_1.pth")
        self.assertTrue(self.is_oss_object_exists(model_path))


@pytest.mark.timeout(60 * 10)
class TestModelScopeModel(BaseIntegTestCase):
    """Test :class:`pai.modelscope.model.ModelScopeModel`."""

    predictors = []

    @classmethod
    def tearDownClass(cls):
        super(TestModelScopeModel, cls).tearDownClass()
        for p in cls.predictors:
            p.delete_service()

    def test_modelscope_model_deploy(self):
        """Test deploying model with ModelScopeModel."""
        m = ModelScopeModel(
            command="python app.py",
            modelscope_version="1.8.1",
            environment_variables={
                "MODEL_ID": "damo/nlp_csanmt_translation_zh2en",
                "TASK": "translation",
                "REVISION": "v1.0.1",
            },
        )

        p = m.deploy(
            service_name=make_eas_service_name("modelscope_model_deploy"),
            instance_count=1,
            instance_type="ecs.gn6i-c4g1.xlarge",
            options={
                "metadata.rpc.keepalive": 5000000,
                "features.eas.aliyun.com/extra-ephemeral-storage": "40Gi",
            },
        )

        self.predictors.append(p)
        self.assertTrue(p.service_name)

        res = p.predict({"input": {"text": "今天天气不错"}})
        self.assertTrue(isinstance(res, dict))
        self.assertTrue(len(res) == 1)
        self.assertTrue(res.get("translation"))
