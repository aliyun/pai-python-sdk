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

from __future__ import absolute_import

import unittest

from pai.common import ProviderAlibabaPAI
from tests.integration import BaseIntegTestCase


class TestPaiFlowAPI(BaseIntegTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestPaiFlowAPI, cls).setUpClass()
        cls.pipeline_run_api = cls.default_session.pipeline_run_api
        cls.pipeline_api = cls.default_session.pipeline_api

    def test_get_pipeline_schema(self):
        identifier = "evaluate_1"
        results = self.pipeline_api.list(
            identifier=identifier, provider=ProviderAlibabaPAI, version="v1"
        )

        pipeline_info = results.items[0]
        self.assertIsNotNone(pipeline_info["PipelineId"])

    def test_list_pipeline(self):
        result = self.pipeline_api.list(
            identifier="evaluate_1", provider=ProviderAlibabaPAI, version="v1"
        )
        pipelines, count = result.items, result.total_count

        self.assertEqual(count, 1)
        self.assertEqual(len(pipelines), 1)
        self.assertEqual(pipelines[0]["Identifier"], "evaluate_1")
        self.assertEqual(pipelines[0]["Provider"], ProviderAlibabaPAI)

    def test_list_run_generator(self):
        result = self.pipeline_run_api.list(status="Succeeded")

        if result.items:
            self.assertIsNotNone(result.items[0]["RunId"])


if __name__ == "__main__":
    unittest.main()
