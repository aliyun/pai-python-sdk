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

import os

from pai.pipeline.types import (
    DataType,
    InputsSpec,
    LocationArtifactMetadata,
    LocationType,
    PipelineArtifact,
    PipelineParameter,
)
from pai.pipeline.types.spec import sort_variable_by_category
from tests.unit import BaseUnitTestCase

_current_dir = os.path.dirname(os.path.abspath(__file__))


class TestInputOutputSpec(BaseUnitTestCase):
    def test_spec_getitem(self):
        items = [
            PipelineParameter(name="A", typ=int, default=10),
            PipelineParameter(name="B", typ=str, default="result"),
            PipelineParameter(name="C", typ=bool, default=True),
            PipelineArtifact(
                name="D",
                metadata=LocationArtifactMetadata(
                    data_type=DataType.DataSet,
                    location_type=LocationType.MaxComputeTable,
                ),
            ),
            PipelineArtifact(
                name="E",
                metadata=LocationArtifactMetadata(
                    data_type=DataType.DataSet,
                    location_type=LocationType.MaxComputeTable,
                ),
            ),
        ]

        specs = InputsSpec(items)
        self.assertTrue(specs[0].name == "A")
        self.assertTrue(specs["B"].name == "B")
        self.assertTrue([item.name for item in specs[:2]] == ["A", "B"])
        self.assertTrue([item.name for item in specs[::2]] == ["A", "C", "E"])

    def test_spec_order(self):
        param_a = PipelineParameter(name="A", typ=int, default=10)
        param_b = PipelineParameter(name="B", typ=str, default="result")
        param_c = PipelineParameter(name="C", typ=bool, default=True)

        param_a_2 = PipelineParameter(name="A", typ=bool, default=True)

        af_d = PipelineArtifact(
            name="D",
            metadata=LocationArtifactMetadata(
                data_type=DataType.DataSet, location_type=LocationType.MaxComputeTable
            ),
        )
        af_e = PipelineArtifact(
            name="E",
            metadata=LocationArtifactMetadata(
                data_type=DataType.DataSet, location_type=LocationType.MaxComputeTable
            ),
        )
        af_f = PipelineArtifact(
            name="F",
            metadata=LocationArtifactMetadata(
                data_type=DataType.DataSet, location_type=LocationType.MaxComputeTable
            ),
        )
        # af_a = PipelineArtifact(
        #     name="A",
        #     metadata=LocationArtifactMetadata(
        #         data_type=DataType.DataSet, location_type=LocationType.MaxComputeTable
        #     ),
        # )

        success_cases = [
            {
                "name": "empty_case",
                "inputs": [],
            },
            {"name": "params_case_1", "inputs": [param_a]},
            {
                "name": "params_case_2",
                "inputs": [param_a, param_b, param_c],
            },
            {
                "name": "artifacts_case_1",
                "inputs": [af_d],
            },
            {
                "name": "artifacts_case_2",
                "inputs": [af_d, af_e, af_f],
            },
            {
                "name": "mix_case_1",
                "inputs": [param_a, af_d],
            },
            {
                "name": "mix_case_2",
                "inputs": [param_a, param_b, param_c, af_d, af_e, af_f],
            },
        ]

        for case in success_cases:
            _ = sort_variable_by_category(case["inputs"])

        error_cases = [
            {
                "name": "error_order_1",
                "inputs": [param_a, param_b, af_d, af_e, param_b],
            },
            {
                "name": "error_order_2",
                "inputs": [af_d, af_e, param_b, af_d],
            },
            {
                "name": "name_conflict_1",
                "inputs": [param_a, param_a_2],
            },
            {
                "name": "name_conflict_2",
                "inputs": [param_a, param_a],
            },
        ]

        for case in error_cases:
            with self.assertRaises(ValueError):
                sort_variable_by_category(case["inputs"])
