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

from tests.integration import BaseIntegTestCase


class TestSession(BaseIntegTestCase):
    def test_provider(self):
        session = self.default_session
        self.assertIsNotNone(session.provider)

    def test_is_gpu_inference_instance(self):
        sess = self.default_session
        cases = [
            {
                "name": "case_gpu",
                "input": "ecs.gn7i-c8g1.2xlarge",
                "expected": True,
            },
            {
                "name": "case_cpu",
                "input": "ecs.c7.2xlarge",
                "expected": False,
            },
            {
                "name": "case_not_exists",
                "input": "ecs.abc.defg",
                "expected": None,
            },
        ]

        for case in cases:
            with self.subTest(case=case):
                if case["expected"] is None:
                    with self.assertRaises(ValueError):
                        sess.is_gpu_inference_instance(case["input"])
                else:
                    result = sess.is_gpu_inference_instance(case["input"])
                    self.assertEqual(
                        result, case["expected"], "case:%s failed" % case["name"]
                    )

    def test_is_supported_inference_instance(self):
        sess = self.default_session

        cases = [
            {
                "name": "case_supported",
                "input": "ecs.c7.2xlarge",
                "expected": True,
            },
            {
                "name": "case_not_exists",
                "input": "ecs.abc.defg",
                "expected": False,
            },
        ]

        for case in cases:
            with self.subTest(case=case):
                result = sess.is_supported_inference_instance(case["input"])
                self.assertEqual(
                    result, case["expected"], "case:%s failed" % case["name"]
                )

    def test_is_supported_train_instance(self):
        sess = self.default_session
        cases = [
            {
                "name": "case_supported",
                "input": "ecs.gn6i-c8g1.2xlarge",
                "expected": True,
            },
            {
                "name": "case_not_exists",
                "input": "ecs.abc.defg",
                "expected": False,
            },
        ]

        for case in cases:
            with self.subTest(case=case):
                result = sess.is_supported_training_instance(case["input"])
                self.assertEqual(
                    result, case["expected"], "case:%s failed" % case["name"]
                )

    def test_is_gpu_train_instance(self):
        sess = self.default_session
        cases = [
            {
                "name": "case_gpu",
                "input": "ecs.gn7i-c8g1.2xlarge",
                "expected": True,
            },
            {
                "name": "case_cpu",
                "input": "ecs.c6.large",
                "expected": False,
            },
            {
                "name": "case_not_exists",
                "input": "ecs.abc.defg",
                "expected": None,
            },
        ]

        for case in cases:
            with self.subTest(case=case):
                if case["expected"] is None:
                    with self.assertRaises(ValueError):
                        sess.is_gpu_training_instance(case["input"])
                else:
                    result = sess.is_gpu_training_instance(case["input"])
                    self.assertEqual(
                        result, case["expected"], "case:%s failed" % case["name"]
                    )
