from __future__ import absolute_import

from pai.common import ProviderAlibabaPAI
from pai.pipeline import PipelineParameter, PipelineStep, Pipeline
from pai.common.utils import gen_temp_table


def create_simple_composite_pipeline():
    """Composite data_source and type_transform pipeline"""
    execution_input = PipelineParameter(name="execution", typ="map")
    cols_to_double_input = PipelineParameter(name="cols_to_double", typ=str)
    table_input = PipelineParameter(name="table_name", typ=str)

    data_source_step = PipelineStep(
        identifier="dataSource-xflow-maxCompute",
        provider=ProviderAlibabaPAI,
        version="v1",
        name="dataSource",
        inputs={
            "execution": execution_input,
            "tableName": table_input,
            "partition": "",
        },
    )

    type_transform_step = PipelineStep(
        identifier="type-transform-xflow-maxCompute",
        provider=ProviderAlibabaPAI,
        version="v1",
        name="typeTransform",
        inputs={
            "inputArtifact": data_source_step.outputs["outputArtifact"],
            "execution": execution_input,
            "outputTable": gen_temp_table(),
            "cols_to_double": cols_to_double_input,
            "coreNum": 2,
            "memSizePerCore": 1024,
        },
    )
    split_step = PipelineStep(
        identifier="split-xflow-maxCompute",
        provider=ProviderAlibabaPAI,
        version="v1",
        inputs={
            "inputArtifact": type_transform_step.outputs[0],
            "execution": execution_input,
            "output1TableName": gen_temp_table(),
            "fraction": 0.5,
            "output2TableName": gen_temp_table(),
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
