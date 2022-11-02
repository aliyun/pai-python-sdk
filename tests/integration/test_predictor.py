import os

import numpy as np

from pai.common.consts import ModelFormat
from pai.common.oss_utils import upload_to_oss
from pai.common.utils import camel_to_snake
from pai.eas.processor import BuildInProcessor
from pai.entity.service import ComputeConfig, Service
from pai.serializer import TorchIOSpec, TorchSerializer
from tests.integration import BaseIntegTestCase
from tests.integration.utils import make_resource_name
from tests.test_data import (
    PMML_MODEL_PATH,
    PYTORCH_MNIST_MODEL_PATH,
    TF_MNIST_MODEL_PATH,
)


class TestPredictBase(BaseIntegTestCase):
    model_path: str = None
    model_format = ModelFormat.PMML
    service: Service = None

    @classmethod
    def setUpClass(cls):
        super(TestPredictBase, cls).setUpClass()
        cls.service = cls._init_service()

    @classmethod
    def _init_service(cls):
        case_name = camel_to_snake(cls.__name__)

        if not os.path.isdir(cls.model_path):
            file_name = os.path.basename(cls.model_path)
            obj_key = f"sdk-integration-test/{case_name}/{file_name}"
        else:
            obj_key = f"sdk-integration-test/{case_name}/"
        model_path = upload_to_oss(
            cls.model_path,
            obj_key,
            cls.default_session.oss_bucket,
        )

        name = make_resource_name(
            camel_to_snake(cls.__name__), sep="_", time_suffix=False
        )
        service = Service.deploy(
            name=name,
            instance_count=2,
            compute_config=ComputeConfig.from_resource_config(
                cpu=2,
                memory=4000,
            ),
            processor=BuildInProcessor.from_model_format(
                model_format=cls.model_format,
            ),
            model_path=model_path,
            wait_for_ready=True,
        )
        return service

    @classmethod
    def tearDownClass(cls):
        super(TestPredictBase, cls).tearDownClass()
        if cls.service:
            cls.service.delete()


class TestPmmlPredict(TestPredictBase):
    model_path = PMML_MODEL_PATH
    model_format = ModelFormat.PMML
    service: Service = None

    def test_pmml(self):
        resp = self.service.predict(
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
        self.assertTrue(isinstance(resp, list))
        self.assertTrue(len(resp) == 2)
        self.assertTrue("p_0" in resp[0])


class TestTensorFlowPredict(TestPredictBase):
    model_path = TF_MNIST_MODEL_PATH
    model_format = ModelFormat.SavedModel
    service: Service = None

    def test_tf_predict(self):
        self.assertTrue(
            "signature_name" in self.service.inspect_tensorflow_signature_def()
        )
        result_1 = self.service.predict(
            [1] * 784,
        )
        result_2 = self.service.predict({"flatten_input": [1] * 784})

        self.assertListEqual(result_1["dense_1"].tolist(), result_2["dense_1"].tolist())


class TestTorchPredict(TestPredictBase):
    model_path = PYTORCH_MNIST_MODEL_PATH
    model_format = ModelFormat.TorchScript
    service: Service = None

    def test_torch_predict(self):
        # service: EasService = EasService.get("lq_mnist_torch_1_8")
        # print(service.config.processor)
        service = self.service
        result_1 = service.predict(
            np.asarray([0.5] * 28 * 28 * 2).reshape((2, 1, 28, 28)),
        )

        self.assertIsNotNone(result_1)
        self.assertTupleEqual(np.shape(result_1), (2, 10))

        result_2 = service.predict(
            np.asarray([0.5] * 28 * 28 * 2),
            serializer=TorchSerializer(
                input_specs=TorchIOSpec(
                    index=0,
                    shape=(2, 1, 28, 28),
                    data_type=TorchSerializer.DT_FLOAT,
                ),
                output_filter=[0],
            ),
        )
        self.assertIsNotNone(result_2)
        self.assertTupleEqual(np.shape(result_2), (2, 10))
