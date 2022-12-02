from __future__ import absolute_import

from pai.common import ProviderAlibabaPAI
from pai.common.utils import gen_run_node_scoped_placeholder
from pai.pipeline import Pipeline, PipelineStep
from pai.pipeline.types import PipelineParameter


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
