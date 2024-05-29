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
import pprint

import pytest

from pai._training_job import UriInput
from pai.common.utils import random_str
from pai.model import RegisteredModel
from pai.session import get_default_session
from tests.integration import BaseIntegTestCase
from tests.test_data import test_data_dir


@pytest.mark.timeout(60 * 30)
class TestModelRecipe(BaseIntegTestCase):
    def test_list_model(self):
        for m in RegisteredModel.list(
            model_name="qwen1.5-0.5b-chat", model_provider="pai"
        ):
            print(m)

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

        train_data = os.path.join(test_data_dir, "chinese_medical/train_sampled.json")
        self.assertTrue(os.path.exists(train_data))
        training_recipe.train(
            inputs={
                "train": train_data,
            },
        )
        self.assertIsNotNone(training_recipe.model_data())

    def test_retrieve_scripts(self):
        model = RegisteredModel(model_name="qwen1.5-0.5b-chat", model_provider="pai")
        recipe = model.training_recipe()
        pprint.pprint(recipe.spec.model_dump())

    def test_evaluation(self):
        model = RegisteredModel(model_name="qwen1.5-0.5b-chat", model_provider="pai")
        eval_recipe = model.evaluation_recipe()
        eval_recipe.evaluate()

    def test_input_dump(self):
        uri_input = UriInput(Name="Hello", InputUri="abc")
        print(uri_input.model_dump(by_alias=True))

    def test_algorithm(self):
        algorithm_name = "llm_deepspeed_peft"
        algorithm_version = "v0.0.5"

        session = get_default_session()
        algo = session.algorithm_api.get_by_name(
            algorithm_name=algorithm_name, algorithm_provider="pai"
        )
        raw_algo_version_spec = session.algorithm_api.get_version(
            algorithm_id=algo["AlgorithmId"], algorithm_version=algorithm_version
        )
        pprint.pprint(raw_algo_version_spec)
