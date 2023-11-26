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

import asyncio
import io
import os
import time

import numpy as np
import pandas as pd

from pai.exception import PredictionException
from pai.image import retrieve
from pai.model import InferenceSpec, Model, container_serving_spec
from pai.predictor import AsyncPredictor, ServiceType
from tests.integration import BaseIntegTestCase
from tests.integration.utils import NumpyBytesSerializer, make_eas_service_name
from tests.test_data import PMML_MODEL_PATH, test_data_dir


class TestAsyncPredictorBuiltinProcessor(BaseIntegTestCase):

    predictors = []

    @classmethod
    def tearDownClass(cls):
        for p in cls.predictors:
            p.delete_service()

    def test(self):
        m = Model(
            inference_spec=InferenceSpec(
                processor="pmml",
            ),
            model_data=PMML_MODEL_PATH,
        )
        predictor: AsyncPredictor = m.deploy(
            service_name=make_eas_service_name("async_pmml"),
            instance_type="ecs.c6.xlarge",
            service_type=ServiceType.Async,
        )
        type(self).predictors.append(predictor)
        data = [
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

        res1 = predictor.predict(data=data).result()
        res2 = asyncio.run(predictor.predict_async(data=data))
        self.assertListEqual(res1, res2)

        raw_res1 = predictor.raw_predict(data=data).result().json()
        raw_res2 = asyncio.run(predictor.raw_predict_async(data=data)).json()
        self.assertListEqual(raw_res1, raw_res2)


class TestAsyncPredictorContainerServing(BaseIntegTestCase):

    predictors = []

    @classmethod
    def tearDownClass(cls):
        for p in cls.predictors:
            p.delete_service()

    def test(self):
        m = Model(
            inference_spec=container_serving_spec(
                source_dir=os.path.join(test_data_dir, "xgb_serving"),
                command="python serving.py",
                image_uri=retrieve("xgboost", framework_version="latest").image_uri,
                port=5000,
            ),
            model_data=os.path.join(test_data_dir, "xgb_model/model.json"),
        )
        predictor: AsyncPredictor = m.deploy(
            service_name=make_eas_service_name("async_container"),
            instance_type="ecs.c6.xlarge",
            service_type=ServiceType.Async,
            serializer=NumpyBytesSerializer(),
        )
        type(self).predictors.append(predictor)

        # get test data
        df = pd.read_csv(
            os.path.join(test_data_dir, "breast_cancer_data/test.csv"),
        )
        x = df.drop(["target"], axis=1)[:10]

        # test predict
        results = []
        task = predictor.predict(data=x, callback=lambda x: results.append(x))
        res1 = task.result()
        res2 = asyncio.run(predictor.predict_async(data=x))
        self.assertTrue(len(results) > 0)
        self.assertListEqual(results[0].tolist(), res1.tolist())
        self.assertListEqual(res1.tolist(), res2.tolist())

        # test raw predict
        raw_results = []
        data = io.BytesIO()
        np.save(data, x.to_numpy())
        resp1 = predictor.raw_predict(
            data=data.getvalue(), callback=lambda x: raw_results.append(x)
        ).result()

        self.assertTrue(len(raw_results) > 0)
        self.assertEqual(raw_results[0].content, resp1.content)
        raw_res1 = np.load(io.BytesIO(resp1.content))
        raw_res2 = np.load(
            io.BytesIO(
                asyncio.run(predictor.raw_predict_async(data=data.getvalue())).content
            )
        )
        self.assertEqual(raw_res1.tolist(), raw_res2.tolist())

        # test multi callbacks
        multi_callback_results = []
        predictor.raw_predict(
            data=data.getvalue(),
            callback=[
                lambda x: print(x),
                lambda x: multi_callback_results.append(x),
                lambda x: multi_callback_results.append(x),
            ],
        ).result()

        # wait for callbacks to finish
        time.sleep(1)
        self.assertEqual(len(multi_callback_results), 2)

        # test error response
        with self.assertRaises(PredictionException):
            predictor.raw_predict(data="test").result()
