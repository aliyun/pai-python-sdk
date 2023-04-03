import io
import os.path
from typing import Union
from unittest import skipUnless

import numpy as np
import pandas as pd

from pai.common.oss_utils import is_oss_uri, upload
from pai.common.utils import camel_to_snake
from pai.image import retrieve
from pai.model import InferenceSpec, Model, ResourceConfig
from pai.serializers import JsonSerializer, SerializerBase
from tests.integration import BaseIntegTestCase
from tests.integration.utils import make_eas_service_name, t_context
from tests.test_data import PMML_MODEL_PATH, test_data_dir


class NumpyBytesSerializer(SerializerBase):
    def serialize(self, data: Union[np.ndarray, pd.DataFrame, bytes]) -> bytes:
        if isinstance(data, bytes):
            return data
        elif isinstance(data, str):
            return data.encode()
        elif isinstance(data, pd.DataFrame):
            data = data.to_numpy()

        res = io.BytesIO()
        np.save(res, data)
        return res.getvalue()

    def deserialize(self, data: bytes) -> np.ndarray:
        f = io.BytesIO(data)
        return np.load(f)


class TestModelContainerDeploy(BaseIntegTestCase):
    """Test model deploy with container"""

    oss_model_path = None
    x_test = None
    predictors = []

    @classmethod
    def tearDownClass(cls):
        super(TestModelContainerDeploy, cls).tearDownClass()
        for p in cls.predictors:
            p.delete_service()

    @classmethod
    def setUpClass(cls):
        super(TestModelContainerDeploy, cls).setUpClass()
        case_name = camel_to_snake(cls.__name__)
        filename = "randomforest_wine.tar.gz"
        obj_key = f"sdk-integration-test/{case_name}/{filename}"
        model_path = os.path.join(test_data_dir, "python_processor", filename)
        cls.oss_model_path = upload(
            model_path,
            obj_key,
            cls.default_session.oss_bucket,
        )

        x_test_path = os.path.join(test_data_dir, "python_processor", "x_test.npy")
        cls.x_test = np.load(x_test_path)

    def test_from_serving_script(self):
        image_uri = retrieve("xgboost", framework_version="latest").image_uri
        inference_spec = InferenceSpec.from_serving_script(
            source_dir=os.path.join(test_data_dir, "xgb_serving"),
            entry_point="serving.py",
            image_uri=image_uri,
            port=5000,
            environment_variables={"PYTHONUNBUFFERED": "1"},
        )
        model = Model(
            inference_spec=inference_spec,
            model_data=os.path.join(test_data_dir, "xgb_model/model.json"),
        )

        predictor = model.deploy(
            service_name=make_eas_service_name("serving_script"),
            instance_count=1,
            instance_type="ecs.c6.xlarge",
            serializer=NumpyBytesSerializer(),
        )
        self.predictors.append(predictor)

        df = pd.read_csv(
            os.path.join(test_data_dir, "breast_cancer_data/test.csv"),
        )
        y = df["target"]
        x = df.drop(["target"], axis=1)
        res = predictor.predict(x)
        self.assertEqual(len(y), len(res))

    def test_model_mount(self):
        image_uri = retrieve("xgboost", framework_version="latest").image_uri
        inference_spec = InferenceSpec.from_serving_script(
            source_dir=os.path.join(test_data_dir, "xgb_serving"),
            entry_point="serving.py",
            image_uri=image_uri,
            port=5000,
            environment_variables={
                "PYTHONUNBUFFERED": "1",
            },
        )
        model = Model(
            inference_spec=inference_spec,
            model_data=os.path.join(test_data_dir, "xgb_model/model.json"),
        )
        predictor = model.deploy(
            service_name=make_eas_service_name("mount_model"),
            instance_type="ecs.c6.xlarge",
            serializer=NumpyBytesSerializer(),
        )
        self.predictors.append(predictor)

        df = pd.read_csv(
            os.path.join(test_data_dir, "breast_cancer_data/test.csv"),
        )
        y = df["target"]
        x = df.drop(["target"], axis=1)
        res = predictor.predict(x)
        self.assertEqual(len(y), len(res))


class TestModelProcessorDeploy(BaseIntegTestCase):
    """Test model deploy with processor"""

    _created_services = []

    @classmethod
    def tearDownClass(cls):
        super(TestModelProcessorDeploy, cls).tearDownClass()
        for service_name in cls._created_services:
            cls.default_session.service_api.delete(service_name)

    def test_builtin_pmml_processor(self):
        m = Model(
            inference_spec=InferenceSpec(
                processor="pmml",
            ),
            model_data=PMML_MODEL_PATH,
        )

        predictor = m.deploy(
            service_name=make_eas_service_name("test_builtin_pmml"),
            instance_count=1,
            instance_type="ecs.c6.xlarge",
        )
        self._created_services.append(predictor.service_name)
        result = predictor.predict(
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
        self.assertEqual(len(result), 2)

    def test_deploy_by_resource_config(self):
        m = Model(
            inference_spec=InferenceSpec(
                processor="pmml",
            ),
            model_data=PMML_MODEL_PATH,
        )

        pred1 = m.deploy(
            service_name=make_eas_service_name("resource_cfg_v1"),
            instance_count=1,
            resource_config={
                "cpu": 2,
                "memory": 4096,
            },
        )
        self._created_services.append(pred1.service_name)
        result = pred1.predict(
            [
                {
                    "pm10": 1.0,
                    "so2": 2.0,
                    "co": 0.5,
                },
            ]
        )
        self.assertEqual(len(result), 1)

        pred2 = m.deploy(
            service_name=make_eas_service_name("resource_cfg_v2"),
            instance_count=1,
            resource_config=ResourceConfig(
                cpu=2,
                memory=4096,
            ),
        )
        self._created_services.append(pred2.service_name)
        result = pred2.predict(
            [
                {
                    "pm10": 1.0,
                    "so2": 2.0,
                    "co": 0.5,
                },
            ]
        )
        self.assertEqual(len(result), 1)

    def test_xgb_built_processor(self):
        val = pd.read_csv(os.path.join(test_data_dir, "breast_cancer_data/test.csv"))
        val_y = val["target"]
        val_x = val.drop("target", axis=1)

        model_path = upload(
            source_path=os.path.join(test_data_dir, "xgb_model/model.json"),
            oss_path="sdk-integration-test/test_xgb_model_deploy/",
            oss_bucket=self.default_session.oss_bucket,
        )

        m = Model(
            model_data=model_path,
            inference_spec=InferenceSpec(
                processor="xgboost",
            ),
        )
        p = m.deploy(
            service_name=make_eas_service_name("xgb_builtin"),
            instance_count=1,
            instance_type="ecs.c6.xlarge",
            serializer=JsonSerializer(),
            options={
                # "metadata.rpc.batching": True,
                # "metadata.rpc.keepalive": 20000,
            },
        )

        self._created_services.append(p.service_name)
        pred_y = p.predict(val_x)
        self.assertEqual(len(pred_y), len(val_y))


class TestInferenceSpec(BaseIntegTestCase):
    def test_mount_local_source(self):
        infer_spec = InferenceSpec().mount(
            os.path.join(test_data_dir, "xgb_serving"), mount_path="/ml/model/"
        )
        storage_config = infer_spec.storage[0]

        self.assertEqual(storage_config["mount_path"], "/ml/model/")
        self.assertTrue(is_oss_uri(storage_config["oss"]["path"]))

    def test_mount_oss(self):
        oss_uri = "oss://your_oss_bucket/test_xgb_model_deploy/"
        infer_spec = InferenceSpec().mount(oss_uri, mount_path="/ml/model/")
        storage_config = infer_spec.storage[0]
        self.assertEqual(storage_config["mount_path"], "/ml/model/")
        self.assertEqual(storage_config["oss"]["path"], oss_uri)


@skipUnless(t_context.has_docker, "Estimator local train requires docker.")
class TestModelLocalDeploy(BaseIntegTestCase):
    def test_from_serving_local_scripts(self):
        inference_spec = InferenceSpec.from_serving_script(
            source_dir=os.path.join(test_data_dir, "xgb_serving"),
            entry_point="serving.py",
            image_uri="registry.{}.aliyuncs.com/lq-test-v2/python:xgb_serving_python37".format(
                self.default_session.region_id
            ),
            port=8000,
        )

        model = Model(
            inference_spec=inference_spec,
            model_data=os.path.join(test_data_dir, "xgb_model/model.json"),
        )

        predictor = model.deploy(
            service_name=make_eas_service_name("serving_script"),
            instance_count=1,
            instance_type="local",
            serializer=NumpyBytesSerializer(),
        )

        df = pd.read_csv(
            os.path.join(test_data_dir, "breast_cancer_data/test.csv"),
        )
        y = df["target"]
        x = df.drop(["target"], axis=1)
        res = predictor.predict(x)
        self.assertEqual(len(y), len(res))
        predictor.delete_service()
