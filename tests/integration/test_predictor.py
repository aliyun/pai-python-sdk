import json
import os
import time

import numpy as np

from pai.common.consts import ModelFormat
from pai.common.oss_utils import parse_oss_uri, upload
from pai.common.utils import camel_to_snake
from pai.model import _BuiltinProcessor
from pai.predictor import Predictor, ServiceStatus
from tests.integration import BaseIntegTestCase
from tests.integration.utils import make_resource_name
from tests.test_data import (
    PMML_MODEL_PATH,
    PYTORCH_MNIST_MODEL_PATH,
    TF_MNIST_MODEL_PATH,
)


def _truncate_endpoint(uri):
    """Remove endpoint if it is present as host in OSS URI"""

    parsed = parse_oss_uri(uri)

    return "oss://{bucket_name}/{key}".format(
        bucket_name=parsed.bucket_name, key=parsed.object_key
    )


class TestPredictorBase(BaseIntegTestCase):
    model_path: str = None
    model_format = ModelFormat.PMML
    predictor: Predictor = None

    @classmethod
    def setUpClass(cls):
        super(TestPredictorBase, cls).setUpClass()
        cls.predictor = cls._init_predictor()

    @classmethod
    def _init_predictor(cls):
        case_name = camel_to_snake(cls.__name__)
        if not os.path.isdir(cls.model_path):
            file_name = os.path.basename(cls.model_path)
            obj_key = f"sdk-integration-test/{case_name}/{file_name}"
        else:
            obj_key = f"sdk-integration-test/{case_name}/"
        model_path = upload(
            cls.model_path,
            obj_key,
            cls.default_session.oss_bucket,
        )

        name = make_resource_name(
            camel_to_snake(cls.__name__), sep="_", time_suffix=False
        )

        service_name = cls.default_session.service_api.create(
            {
                "name": name,
                "metadata": {
                    "instance": 2,
                    "cpu": 2,
                    "memory": 4000,
                },
                "processor": _BuiltinProcessor.get_default_by_model_format(
                    model_format=cls.model_format,
                ),
                "model_path": _truncate_endpoint(model_path),
            },
        )

        p = Predictor(service_name=service_name)
        p.wait_for_ready()
        time.sleep(5)
        return p

    @classmethod
    def tearDownClass(cls):
        super(TestPredictorBase, cls).tearDownClass()
        if cls.predictor:
            cls.predictor.delete_service()


class TestPmmlPredictor(TestPredictorBase):
    model_path = PMML_MODEL_PATH
    model_format = ModelFormat.PMML

    def test_json_serializer(self):
        resp = self.predictor.predict(
            [
                {
                    "pm10": 1.0,
                    "so2": 2.0,
                    "co": 0.5,
                },
                {
                    "pm10": 1.0,
                    "so2": 2.0,
                    "co": 0.5,
                },
            ]
        )

        self.assertTrue(isinstance(resp, list), "resp is not a list")
        self.assertTrue(len(resp) == 2, "resp doesn't have length 2")
        self.assertTrue("p_0" in resp[0], "p_0 is not in resp[0]")

    def test_raw_request(self):
        p = self.predictor

        result = p.raw_predict(
            json.dumps(
                [
                    {
                        "pm10": 1.0,
                        "so2": 2.0,
                        "co": 0.5,
                    },
                    {
                        "pm10": 1.0,
                        "so2": 2.0,
                        "co": 0.5,
                    },
                ]
            ).encode()
        )

        res = json.loads(result)

        self.assertEqual(len(res), 2)


class TestTensorFlowPredictor(TestPredictorBase):
    model_path = TF_MNIST_MODEL_PATH
    model_format = ModelFormat.SavedModel

    def test_tf_predict(self):
        predictor = self.predictor
        result_1 = predictor.predict(
            {
                # batch_size = 2
                "flatten_input": [1]
                * 784
                * 2,
            }
        )

        self.assertTupleEqual(result_1["dense_1"].shape, (2, 10))

        result_2 = predictor.predict([1] * 784 * 3)
        self.assertTupleEqual(result_2["dense_1"].shape, (3, 10))

        result_3 = predictor.predict(
            {
                # batch_size = 2
                "flatten_input": np.asarray([1] * 784 * 4)
            }
        )
        self.assertTupleEqual(result_3["dense_1"].shape, (4, 10))

    def test_signature_def(self):
        signature_def = self.predictor.inspect_model_signature_def()
        self.assertTrue(signature_def["signature_name"], "serving_default")
        self.assertTrue("inputs" in signature_def)
        self.assertTrue("outputs" in signature_def)


class TestTorchPredictor(TestPredictorBase):
    model_path = PYTORCH_MNIST_MODEL_PATH
    model_format = ModelFormat.TorchScript

    def test_torch_predict(self):
        result = self.predictor.predict(
            np.asarray([0.5] * 28 * 28 * 2, dtype=np.float32).reshape((2, 1, 28, 28)),
        )

        self.assertTrue(isinstance(result, np.ndarray))

        self.assertTupleEqual(result.shape, (2, 10))


class TestPredictorOperation(BaseIntegTestCase):
    model_path = PMML_MODEL_PATH
    model_format = ModelFormat.PMML
    predictor: Predictor = None

    @classmethod
    def setUpClass(cls):
        super(TestPredictorOperation, cls).setUpClass()
        cls.predictor = cls._init_predictor()

    @classmethod
    def _init_predictor(cls):
        case_name = camel_to_snake(cls.__name__)

        if not os.path.isdir(cls.model_path):
            file_name = os.path.basename(cls.model_path)
            obj_key = f"sdk-integration-test/{case_name}/{file_name}"
        else:
            obj_key = f"sdk-integration-test/{case_name}/"
        model_path = upload(
            cls.model_path,
            obj_key,
            cls.default_session.oss_bucket,
        )
        name = make_resource_name(
            camel_to_snake(cls.__name__), sep="_", time_suffix=False
        )
        service_name = cls.default_session.service_api.create(
            {
                "name": name,
                "metadata": {
                    "instance": 2,
                    "cpu": 2,
                    "memory": 4000,
                },
                "processor": _BuiltinProcessor.get_default_by_model_format(
                    model_format=cls.model_format,
                ),
                "model_path": _truncate_endpoint(model_path),
            },
        )

        p = Predictor(service_name=service_name)
        p.wait_for_ready()

        # hack: wait for the service to be 'really' ready
        time.sleep(5)
        return p

    @classmethod
    def tearDownClass(cls):
        super(TestPredictorOperation, cls).tearDownClass()
        if cls.predictor:
            cls.predictor.delete_service()

    def test_predictor_operation_pmml(self):
        resp = self.predictor.predict(
            [
                {
                    "pm10": 1.0,
                    "so2": 2.0,
                    "co": 0.5,
                },
                {
                    "pm10": 1.0,
                    "so2": 2.0,
                    "co": 0.5,
                },
            ]
        )
        self.assertTrue(isinstance(resp, list), "resp is not a list")
        self.assertTrue(len(resp) == 2, "resp doesn't have length 2")
        self.assertTrue("p_0" in resp[0], "p_0 is not in resp[0]")
        self.assertTrue(
            self.predictor.service_status == ServiceStatus.Running,
            "service is not running",
        )
        self.predictor.stop_service()
        self.assertTrue(
            self.predictor.service_status == ServiceStatus.Stopped,
            "service does not stop",
        )
        self.predictor.start_service()
        self.assertTrue(
            self.predictor.service_status == ServiceStatus.Running,
            "service does not start",
        )
        self.predictor.delete_service()