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
from pai.pipeline import Pipeline, PipelineStep
from pai.pipeline.types import PipelineParameter
from tests.integration.utils import gen_run_node_scoped_placeholder


def create_simple_composite_pipeline():
    """Composite data_source and type_transform pipeline"""
    execution_input = PipelineParameter(name="execution", typ="map")
    cols_to_double_input = PipelineParameter(name="cols_to_double", typ=str)
    table_input = PipelineParameter(name="table_name", typ=str)

    data_source_step = PipelineStep.from_registered_component(
        identifier="data_source",
        provider=ProviderAlibabaPAI,
        version="v1",
        name="dataSource",
        inputs={
            "execution": execution_input,
            "inputTableName": table_input,
            "inputTablePartitions": "",
        },
    )

    type_transform_step = PipelineStep.from_registered_component(
        identifier="type_transform",
        provider=ProviderAlibabaPAI,
        version="v1",
        name="typeTransform",
        inputs={
            "inputTable": data_source_step.outputs["outputTable"],
            "execution": execution_input,
            "outputTable": gen_run_node_scoped_placeholder(suffix="outputTable"),
            "cols_to_double": cols_to_double_input,
            "coreNum": 2,
            "memSizePerCore": 1024,
        },
    )
    split_step = PipelineStep.from_registered_component(
        identifier="split",
        provider=ProviderAlibabaPAI,
        version="v1",
        inputs={
            "inputTable": type_transform_step.outputs[0],
            "execution": execution_input,
            "output1TableName": gen_run_node_scoped_placeholder(suffix="output1Table"),
            "fraction": 0.5,
            "output2TableName": gen_run_node_scoped_placeholder(suffix="output2Table"),
            "coreNum": 2,
            "memSizePerCore": 1024,
            "lifecycle": 28,
        },
    )

    p = Pipeline(
        inputs=[execution_input, cols_to_double_input, table_input],
        steps=[data_source_step, type_transform_step, split_step],
        outputs=split_step.outputs[:1]
        + data_source_step.outputs[:1]
        + split_step.outputs[-1:],
    )

    return p, data_source_step, type_transform_step, split_step
