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

from pai.image import ImageScope, list_images, retrieve
from tests.integration import BaseIntegTestCase


class TestImageUris(BaseIntegTestCase):
    def test_retrieve_training_image(self):
        tf_img = retrieve(
            "tensorflow", framework_version="latest", accelerator_type="gpu"
        )
        self.assertEqual(tf_img.accelerator_type.lower(), "gpu")
        self.assertEqual(tf_img.framework_name.lower(), "tensorflow")
        self.assertEqual(tf_img.image_scope, ImageScope.TRAINING)

        tf_image = retrieve(
            "tensorflow",
            framework_version="2.3",
            accelerator_type="gpu",
            image_scope=ImageScope.INFERENCE,
        )
        self.assertEqual(tf_image.framework_version, "2.3")
        self.assertEqual(tf_image.image_scope, ImageScope.INFERENCE)

        self.assertIsNotNone(
            retrieve("xgboost", framework_version="latest", accelerator_type="cpu")
        )

        xgb_image = retrieve("xgboost", framework_version="latest")
        self.assertTrue(xgb_image.accelerator_type.lower() == "cpu")

        torch_img = retrieve(
            "pytorch", framework_version="latest", accelerator_type="gpu"
        )

        self.assertEqual(torch_img.framework_name.lower(), "pytorch")
        self.assertEqual(torch_img.accelerator_type.lower(), "gpu")

        self.assertIsNotNone(
            retrieve("oneflow", framework_version="latest", accelerator_type="gpu")
        )

    def test_retrieve_inference_image(self):
        tf_image = retrieve(
            "tensorflow", framework_version="latest", image_scope=ImageScope.INFERENCE
        )
        self.assertIsNotNone("tensorflow" in tf_image.image_uri)
        self.assertIsNotNone("inference" in tf_image.image_uri)

        tf_gpu_image = retrieve(
            "tensorflow",
            framework_version="latest",
            accelerator_type="GPU",
            image_scope=ImageScope.INFERENCE,
        )
        self.assertIsNotNone("tensorflow" in tf_gpu_image.image_uri)
        self.assertIsNotNone("inference" in tf_gpu_image.image_uri)

        tf_gpu_image_23 = retrieve(
            "tensorflow",
            framework_version="2.3",
            accelerator_type="GPU",
            image_scope=ImageScope.INFERENCE,
        )
        self.assertIsNotNone(tf_gpu_image_23.image_uri)

        with self.assertRaises(RuntimeError):
            _ = retrieve(
                "tensorflow",
                framework_version="0.01",
                accelerator_type="GPU",
                image_scope=ImageScope.INFERENCE,
            )

    def test_list_pai_image_uris(self):
        tf_image_uris = list_images("tensorflow")
        self.assertTrue(len(tf_image_uris) > 0)
        self.assertTrue(all("tensorflow" in img.image_uri for img in tf_image_uris))

        torch_image_uris = list_images("pytorch")
        torch_image_uris = list(torch_image_uris)
        self.assertTrue(len(torch_image_uris) > 0)
        self.assertTrue(all("torch" in img.image_uri for img in torch_image_uris))

        inference_image_uris = list_images("pytorch", image_scope=ImageScope.INFERENCE)
        self.assertTrue(len(list(inference_image_uris)) > 0)
