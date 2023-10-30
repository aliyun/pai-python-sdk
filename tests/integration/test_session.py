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
