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

from pai.common import ProviderAlibabaPAI
from pai.pipeline import PipelineRunStatus
from pai.pipeline.component import RegisteredComponent
from tests.integration import BaseIntegTestCase


class TestRegisteredComponent(BaseIntegTestCase):
    def test_list(self):
        ops = RegisteredComponent.list(provider=ProviderAlibabaPAI)
        self.assertTrue(len(ops) > 0)

    def test_run(self):
        op = RegisteredComponent.get_by_identifier(
            "split",
            provider=ProviderAlibabaPAI,
        )
        self.assertIsNotNone(op.pipeline_id)
        self.assertEqual(op.identifier, "split")
        self.assertEqual(op.provider, ProviderAlibabaPAI)
        self.assertEqual(op.version, "v1")

        run = op.run(
            job_name="integ_test_save_op_run",
            arguments={
                "execution": self.get_default_maxc_execution(),
                "inputTable": "odps://{}/tables/{}".format(
                    self.breast_cancer_dataset.default_dataset_project,
                    self.breast_cancer_dataset.table_name,
                ),
                "fraction": "0.7",
            },
        )

        self.assertEqual(run.get_status(), PipelineRunStatus.Succeeded)
