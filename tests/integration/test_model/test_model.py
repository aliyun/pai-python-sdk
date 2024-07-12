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

import io
import json
import os.path
from itertools import islice
from unittest import skipUnless

import numpy as np
import pandas as pd
import pytest
from Tea.exceptions import TeaException

from pai.common.oss_utils import is_oss_uri, upload
from pai.common.utils import camel_to_snake
from pai.image import retrieve
from pai.model import (
    InferenceSpec,
    Model,
    NodeStorageConfig,
    RegisteredModel,
    ResourceConfig,
    SharedMemoryConfig,
    container_serving_spec,
)
from tests.integration import BaseIntegTestCase
from tests.integration.utils import (
    NumpyBytesSerializer,
    make_eas_service_name,
    make_resource_name,
    t_context,
)
from tests.test_data import PMML_MODEL_PATH, test_data_dir


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

    def test_container_serving(self):
        image_uri = retrieve("xgboost", framework_version="latest").image_uri
        inference_spec = container_serving_spec(
            source_dir=os.path.join(test_data_dir, "xgb_serving"),
            command="python serving.py",
            image_uri=image_uri,
            port=5000,
            storage_configs=[
                SharedMemoryConfig(size_limit=1),
                NodeStorageConfig(mount_path="/ml/disk/"),
            ],
        )
        self.assertEqual(len(inference_spec.storage), 3)
        model = Model(
            inference_spec=inference_spec,
            model_data=os.path.join(test_data_dir, "xgb_model/model.json"),
        )

        predictor = model.deploy(
            service_name=make_eas_service_name("container_serving"),
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
        result1 = predictor.predict(
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
        self.assertEqual(len(result1), 2)
        resp = predictor.raw_predict(
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
            )
        )
        result2 = resp.json()
        resp = predictor.raw_predict(
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
        result3 = resp.json()
        self.assertListEqual(result1, result2)
        self.assertListEqual(result3, result1)

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


class TestRegisteredModelTrainDeploy(BaseIntegTestCase):
    """Test :class:`pai.model.RegisteredModel` class"""

    predictors = []

    @classmethod
    def tearDownClass(cls):
        super(TestRegisteredModelTrainDeploy, cls).tearDownClass()
        for p in cls.predictors:
            p.delete_service()

    @pytest.mark.timeout(60 * 10)
    def test_tmp_algo_rm_train(self):
        """Test training registered model with temporary algorithm"""
        m = RegisteredModel(
            model_name="qwen1.5-0.5b-chat",
            model_provider="pai",
        )

        est = m.get_estimator()
        inputs = m.get_estimator_inputs()
        est.fit(inputs=inputs)

        outputs_data = est.get_outputs_data()
        self.assertTrue(isinstance(outputs_data, dict))
        self.assertTrue(outputs_data)
        self.assertTrue(len(outputs_data) == 2)

        model_path = os.path.join(outputs_data["model"], "model.safetensors")
        self.assertTrue(self.is_oss_object_exists(model_path))

    @pytest.mark.timeout(60 * 10)
    def test_builtin_algo_rm_train(self):
        """Test training registered model with builtin algorithm"""
        m = RegisteredModel(
            model_name="easycv_object_detection_yolox_nano",
            model_version="0.1.0",
            model_provider="pai",
        )

        est = m.get_estimator()

        self.assertEqual(
            est.labels.get("BaseModelUri"),
            m.uri,
        )

        self.assertEqual(
            est.labels.get("RootModelName"),
            m.model_name,
        )
        self.assertEqual(
            est.labels.get("RootModelID"),
            m.model_id,
        )

        inputs = m.get_estimator_inputs()
        est.hyperparameters["max_epochs"] = 5
        est.hyperparameters["warmup_epochs"] = 2
        est.hyperparameters["image_scale"] = "640,640"
        est.hyperparameters["train_batch_size"] = 8
        est.fit(inputs=inputs)

        outputs_data = est.get_outputs_data()
        self.assertTrue(isinstance(outputs_data, dict))
        self.assertTrue(outputs_data)
        self.assertTrue(len(outputs_data) == 2)

        model_path = os.path.join(outputs_data["model"], "epoch_5_export.pt")
        checkpoint_path = os.path.join(outputs_data["checkpoints"], "epoch_5.pth")
        self.assertTrue(self.is_oss_object_exists(model_path))
        self.assertTrue(self.is_oss_object_exists(checkpoint_path))

    def test_rm_deploy(self):
        """Test deploying registered model"""
        m = RegisteredModel(
            model_name="easynlp_pai_bert_tiny_zh",
            model_version="0.1.0",
            model_provider="pai",
        )

        p = m.deploy()
        self.predictors.append(p)

        self.assertEqual(p.labels.get("RootModelID"), m.model_id)
        self.assertEqual(p.labels.get("RootModelName"), m.model_name)
        self.assertEqual(p.labels.get("RootModelVersion"), m.model_version)
        self.assertEqual(p.labels.get("BaseModelUri"), m.uri)
        self.assertEqual(p.labels.get("Task"), m.task)
        self.assertEqual(p.labels.get("Domain"), m.domain)
        self.assertTrue(p.service_name)
        res = p.predict(["开心", "死亡"])
        self.assertTrue(isinstance(res, list))
        self.assertTrue(len(res) == 2)
        self.assertTrue(res[0]["label"] == "正向")
        self.assertTrue(res[1]["label"] == "负向")

    @pytest.mark.timeout(60 * 10)
    @skipUnless(
        False, "No available model in prod environment, please run this case manually."
    )
    def test_model_evaluation(self):
        m = RegisteredModel(
            model_name="qwen-7b-chat",
            model_version="0.2.5",
            model_provider="pai",
        )
        self.assertIsNotNone(m.evaluation_spec)

        inputs = m.get_evaluation_inputs()
        processor = m.get_eval_processor(
            instance_type="ecs.c6.large",
        )
        processor.run(inputs=inputs)


class TestInferenceSpec(BaseIntegTestCase):
    def test_mount_local_source(self):
        infer_spec = InferenceSpec()
        infer_spec.mount(
            os.path.join(test_data_dir, "xgb_serving"), mount_path="/ml/model/"
        )
        storage_config = infer_spec.storage[0]

        self.assertEqual(storage_config["mount_path"], "/ml/model/")
        self.assertTrue(is_oss_uri(storage_config["oss"]["path"]))

    def test_mount_oss(self):
        oss_uri = "oss://your_oss_bucket/test_xgb_model_deploy/"
        infer_spec = InferenceSpec()
        infer_spec.mount(oss_uri, mount_path="/ml/model/")
        storage_config = infer_spec.storage[0]
        self.assertEqual(storage_config["mount_path"], "/ml/model/")
        self.assertEqual(storage_config["oss"]["path"], oss_uri)


@skipUnless(t_context.has_docker, "Model local deployment requires docker.")
class TestModelLocalDeploy(BaseIntegTestCase):
    def test_from_serving_local_scripts(self):
        xgb_image_uri = retrieve("xgboost", framework_version="latest").image_uri
        inference_spec = container_serving_spec(
            source_dir=os.path.join(test_data_dir, "xgb_serving"),
            command="python serving.py",
            image_uri=xgb_image_uri,
            port=8000,
            requirements=[
                "xgboost==1.5.2",
                "fastapi",
                "uvicorn[standard]",
                "scikit-learn",
            ],
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

        data = io.BytesIO()
        np.save(data, x.to_numpy())
        resp = predictor.raw_predict(
            data=data.getvalue(),
        )
        f = io.BytesIO(resp.content)
        res2 = np.load(f)
        self.assertListEqual(res.tolist(), res2.tolist())
        resp2 = predictor.raw_predict(
            data=data.getvalue(),
            path="/predict",
        )
        f = io.BytesIO(resp2.content)
        res3 = np.load(f)
        self.assertListEqual(res.tolist(), res3.tolist())


@skipUnless(
    t_context.has_docker and t_context.has_gpu,
    "Local deployment using GPU requires docker and GPU.",
)
class TestModelLocalGpuDeploy(BaseIntegTestCase):
    def test(self):
        torch_image_uri = retrieve(
            "pytorch",
            framework_version="1.12",
            accelerator_type="GPU",
        ).image_uri
        inference_spec = container_serving_spec(
            source_dir=os.path.join(test_data_dir, "local_gpu_serve"),
            command="python run.py",
            image_uri=torch_image_uri,
            port=8000,
        )
        m = Model(
            inference_spec=inference_spec,
        )
        p = m.deploy(
            service_name="local_gpu_serve",
            instance_type="local_gpu",
        )
        res = p.raw_predict(
            b"HelloWorld",
        )
        self.assertTrue(isinstance(res.json(), list))


class TestRegisteredModelBaseOperation(BaseIntegTestCase):
    def test_create_delete(self):
        torch_image_uri = retrieve(
            "pytorch",
            framework_version="1.12",
            accelerator_type="GPU",
        ).image_uri

        m = Model(
            model_data="oss://example-bucket/path/to/model/",
            inference_spec=container_serving_spec(
                source_dir=os.path.join(test_data_dir, "local_gpu_serve"),
                command="python run.py",
                image_uri=torch_image_uri,
                port=8000,
            ),
        )

        model_name = make_resource_name(case_name="test_reg_model")
        reg_model_1 = m.register(
            model_name=model_name,
            version="1.0.0",
            version_labels={
                "Alice": "Bob",
            },
        )
        reg_model_2 = m.register(
            model_name=model_name,
            version="1.1.0",
            version_labels={
                "Foo": "Bar",
            },
        )

        latest_model = RegisteredModel(model_name=model_name)

        self.assertTrue(bool(latest_model.model_data))
        self.assertTrue(bool(latest_model.uri))
        self.assertTrue(bool(latest_model.version_labels))
        self.assertDictEqual(latest_model.version_labels, {"Foo": "Bar"})
        self.assertEqual(latest_model.model_version, "1.1.0")

        self.assertEqual(reg_model_2, latest_model)
        models = [m for m in islice(RegisteredModel.list(), 10)]
        self.assertTrue(len(models) >= 0)

        versions = [m for m in islice(latest_model.list_versions(), 2)]
        self.assertTrue(len(versions) >= 2)

        reg_model_1.delete()
        # try to get delete model version.
        with self.assertRaises(TeaException):
            RegisteredModel(model_name, model_version=reg_model_1.model_version)

        new_reg_model_2 = RegisteredModel(
            model_name=model_name, model_version=reg_model_2.model_version
        )
        self.assertEqual(new_reg_model_2, reg_model_2)

    def test_list_public(self):
        models = [m for m in islice(RegisteredModel.list(model_provider="pai"), 10)]
        self.assertTrue(len(models) >= 10)
        self.assertTrue(all(m for m in models if m.model_provider == "pai"))

        models = [
            m
            for m in islice(
                RegisteredModel.list(
                    model_provider="huggingface", task="text-generation"
                ),
                10,
            )
        ]
        self.assertTrue(len(models) >= 10)
        self.assertTrue(all(m for m in models if m.model_provider == "huggingface"))

    def test_list_files_case_upload_file(self):
        # test upload single model file
        model_v1 = Model(
            model_data=os.path.join(test_data_dir, "xgb_model/model.json"),
        )
        model_name = make_resource_name(case_name="test_list_file")
        reg_model_v1 = model_v1.register(model_name=model_name)
        self.assertTrue(self.is_oss_object_exists(reg_model_v1.model_data))
        model_files = [f for f in reg_model_v1.list_model_files()]
        self.assertListEqual(model_files, ["model.json"])
        reg_model_v1.delete()

        # test upload directory
        model_v2 = Model(
            model_data=os.path.join(test_data_dir, "xgb_model/"),
        )
        reg_model_v2 = model_v2.register(model_name=model_name)
        self.assertFalse(self.is_oss_object_exists(reg_model_v2.model_data))
        model_files = [f for f in reg_model_v2.list_model_files()]
        self.assertListEqual(sorted(model_files), sorted(["model.json", "README.md"]))
        model_file_objs = [
            uri for uri in reg_model_v2.list_model_files(uri_format=True)
        ]
        self.assertTrue(
            (all(self.is_oss_object_exists(uri) for uri in model_file_objs))
        )
        reg_model_v2.delete(delete_all_version=True)
