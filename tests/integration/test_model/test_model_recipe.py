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
from unittest import skipUnless

import pytest

from pai.common.utils import camel_to_snake, random_str
from pai.job import SpotSpec
from pai.job._training_job import ResourceType
from pai.model import ModelTrainingRecipe, RegisteredModel
from tests.integration import BaseIntegTestCase
from tests.integration.utils import t_context
from tests.test_data import test_data_dir


@pytest.mark.timeout(60 * 30)
class TestModelRecipe(BaseIntegTestCase):

    _service_names = []

    @classmethod
    def tearDownClass(cls):
        sess = cls.default_session
        for s in cls._service_names:
            try:
                sess.service_api.delete(s)
            except Exception as e:
                print("Failed to delete service: ", e)

    def _gen_service_name(self, prefix: str = None):
        prefix = prefix or "sdk_test_" + camel_to_snake(type(self).__name__)
        name = "{}_{}".format(prefix, random_str(6))
        self._service_names.append(name)
        return name

    def test_training_e2e(self):
        model = RegisteredModel(model_name="qwen1.5-0.5b-chat", model_provider="pai")
        training_recipe = model.training_recipe(method="QLoRA_LLM")
        training_recipe.train()
        self.assertIsNotNone(training_recipe.model_data())

        predictor = training_recipe.deploy(
            service_name=self._gen_service_name("test_recipe_e2e"),
        )
        openai = predictor.openai()
        resp = openai.chat.completions.create(
            model="default",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is the meaning of life?"},
            ],
            max_tokens=100,
        )
        self.assertIsNotNone(resp.choices[0].message.content)

    @skipUnless(t_context.support_spot_instance, "Skip spot instance test")
    def test_spot_instance(self):
        training_recipe = ModelTrainingRecipe(
            model_name="qwen2-7b-instruct",
            model_provider="pai",
            method="Standard",
            resource_type=ResourceType.Lingjun,
            spot_spec=SpotSpec(
                spot_strategy="SpotWithPriceLimit",
                spot_discount_limit=0.5,
            ),
            instance_type="ml.gu7ef.8xlarge-gu100",
        )
        train_data = os.path.join(test_data_dir, "chinese_medical/train_sampled.json")
        training_recipe.train(
            inputs={
                "train": train_data,
            },
        )

    def test_custom_inputs_train(self):
        model = RegisteredModel(model_name="qwen1.5-0.5b-chat", model_provider="pai")
        training_recipe = model.training_recipe(method="QLoRA_LLM")
        self.assertTrue(
            bool(training_recipe.default_inputs),
            "Default inputs is empty for ModelTrainingRecipe.",
        )

        train_data = os.path.join(test_data_dir, "chinese_medical/train_sampled.json")
        training_job = training_recipe.train(
            inputs={
                "train": train_data,
            },
        )
        self.assertIsNotNone(training_job)
        self.assertIsNotNone(training_recipe.model_data())
        predictor = training_recipe.deploy(
            service_name=self._gen_service_name("test_custom"),
        )
        openai = predictor.openai()
        resp = openai.chat.completions.create(
            model="default",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is the meaning of life?"},
            ],
            max_tokens=100,
        )
        self.assertIsNotNone(resp.choices[0].message.content)
