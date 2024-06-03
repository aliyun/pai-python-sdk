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

import pytest

from pai.common.utils import random_str
from pai.model import RegisteredModel
from tests.integration import BaseIntegTestCase
from tests.test_data import test_data_dir


@pytest.mark.timeout(60 * 30)
class TestModelRecipe(BaseIntegTestCase):
    def test_training_e2e(self):
        model = RegisteredModel(model_name="qwen1.5-0.5b-chat", model_provider="pai")
        training_recipe = model.training_recipe(training_method="QLoRA_LLM")
        training_recipe.retrieve_scripts("./scripts")
        training_recipe.train()
        self.assertIsNotNone(training_recipe.model_data())

        predictor = training_recipe.deploy(
            service_name="test_model_recipe_{}".format(random_str(6)),
        )
        openai = predictor.openai()
        resp = openai.chat.completions.create(
            model="default",
            messages=[
                {"role": "system", "content": "Hello, how are you?"},
                {"role": "user", "content": "I am fine, thank you."},
            ],
            max_tokens=100,
        )
        self.assertIsNotNone(resp.choices[0].message.content)

    def test_custom_inputs_train(self):
        model = RegisteredModel(model_name="qwen1.5-0.5b-chat", model_provider="pai")
        training_recipe = model.training_recipe(training_method="QLoRA_LLM")
        self.assertTrue(
            bool(training_recipe.default_inputs),
            "Default inputs is empty for ModelTrainingRecipe.",
        )

        train_data = os.path.join(test_data_dir, "chinese_medical/train_sampled.json")
        training_recipe.train(
            inputs={
                "train": train_data,
            },
        )
        self.assertIsNotNone(training_recipe.model_data())

    def test_evaluation(self):
        model = RegisteredModel(model_name="qwen1.5-0.5b-chat", model_provider="pai")
        eval_recipe = model.evaluation_recipe()
        eval_recipe.evaluate()
