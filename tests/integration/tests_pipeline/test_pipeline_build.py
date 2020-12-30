from __future__ import absolute_import

import uuid

import time
import unittest
import yaml
from unittest import skip

from pai.common import ProviderAlibabaPAI
from pai.pipeline import Pipeline, PipelineStep
from pai.pipeline.run import PipelineRunStatus
from pai.pipeline.types.artifact import (
    DataType,
    LocationType,
    LocationArtifactMetadata,
    PipelineArtifact,
)
from pai.pipeline.types.parameter import PipelineParameter
from pai.common.utils import gen_temp_table
from tests.integration import BaseIntegTestCase
from tests.integration.tests_pipeline import create_simple_composite_pipeline


class TestSimpleCompositePipeline(BaseIntegTestCase):
    def test_run_composite_pipeline(self):
        (
            p,
            data_source_step,
            type_transform_step,
            split_step,
        ) = create_simple_composite_pipeline()
        self.assertEqual(len(p.steps), 3)
        self.assertTrue(all(step for step in p.steps if step.name))

        manifest = p.to_dict()
        input_ports = [
            param["name"] for param in manifest["spec"]["inputs"]["parameters"]
        ] + [af["name"] for af in manifest["spec"]["inputs"]["artifacts"]]
        self.assertEqual(input_ports, ["execution", "cols_to_double", "table_name"])

        output_ports = [
            param["name"] for param in manifest["spec"]["outputs"]["parameters"]
        ] + [af["name"] for af in manifest["spec"]["outputs"]["artifacts"]]

        expected = [
            item.name
            for item in [
                split_step.outputs[0],
                data_source_step.outputs[0],
                split_step.outputs[-1],
            ]
        ]
        self.assertEqual(expected, output_ports)

        pipeline_run = p.run(
            job_name="job_name",
            arguments={
                "execution": self.get_default_maxc_execution(),
                "cols_to_double": ",".join(self.wumai_dataset.columns),
                "table_name": self.wumai_dataset.get_table(),
            },
            wait=True,
            show_outputs=True,
        )

        self.assertEqual(PipelineRunStatus.Succeeded, pipeline_run.get_status())

    def test_composite_pipeline_save(self):
        (
            p,
            data_source_step,
            type_transform_step,
            split_step,
        ) = create_simple_composite_pipeline()

        new_version = uuid.uuid4().hex[:30]
        identifier = "test-composite-pipeline"
        saved_pipeline = p.save(identifier=identifier, version=new_version)

        self.assertEqual(saved_pipeline.version, new_version)
        self.assertEqual(saved_pipeline.identifier, identifier)

    def test_conflict_step_names(self):
        execution_input = PipelineParameter(name="execution", typ="map")
        dataset_input = PipelineArtifact(
            name="dataset_table",
            metadata=LocationArtifactMetadata(
                data_type=DataType.DataSet, location_type=LocationType.MaxComputeTable
            ),
        )

        split_step_1 = PipelineStep(
            name="split-step",
            identifier="split",
            provider=ProviderAlibabaPAI,
            version="v1",
            inputs={
                "inputTable": dataset_input,
                "execution": execution_input,
                "output1TableName": gen_temp_table(),
                "fraction": 0.5,
                "output2TableName": gen_temp_table(),
            },
        )
        split_step_2 = PipelineStep(
            name="split-step",
            identifier="split",
            provider=ProviderAlibabaPAI,
            version="v1",
            inputs={
                "inputTable": dataset_input,
                "execution": execution_input,
                "output1TableName": gen_temp_table(),
                "fraction": 0.5,
                "output2TableName": gen_temp_table(),
            },
        )

        with self.assertRaisesRegexp(ValueError, "name conflict") as _:
            _ = Pipeline(steps=[split_step_1, split_step_2])

    def test_auto_step_name(self):
        execution_input = PipelineParameter(name="execution", typ="map")
        dataset_input = PipelineArtifact(
            name="dataset_table",
            metadata=LocationArtifactMetadata(
                data_type=DataType.DataSet, location_type=LocationType.MaxComputeTable
            ),
        )

        split_step_1 = PipelineStep(
            name="split-step-1",
            identifier="split",
            provider=ProviderAlibabaPAI,
            version="v1",
            inputs={
                "inputArtifact": dataset_input,
                "execution": execution_input,
                "output1TableName": gen_temp_table(),
                "fraction": 0.5,
                "output2TableName": gen_temp_table(),
            },
        )
        split_step_2 = PipelineStep(
            identifier="split",
            provider=ProviderAlibabaPAI,
            version="v1",
            inputs={
                "inputArtifact": dataset_input,
                "execution": execution_input,
                "output1TableName": gen_temp_table(),
                "fraction": 0.5,
                "output2TableName": gen_temp_table(),
            },
        )
        self.assertIsNone(split_step_2.name)
        _ = Pipeline(steps=[split_step_1, split_step_2])
        self.assertIsNotNone(split_step_2.name)

    def test_pipeline_cycle_detect(self):
        execution_input = PipelineParameter(name="execution", typ="map")
        cols_to_double_input = PipelineParameter(name="cols_to_double", typ=str)
        table_input = PipelineParameter(name="table_name", typ=str)

        data_source_step = PipelineStep(
            identifier="data_source",
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
            identifier="type_transform",
            provider=ProviderAlibabaPAI,
            version="v1",
            name="typeTransform",
            inputs={
                "inputArtifact": data_source_step.outputs["outputArtifact"],
                "execution": execution_input,
                "outputTable": gen_temp_table(),
                "cols_to_double": cols_to_double_input,
            },
        )
        data_source_step.after(type_transform_step)

        with self.assertRaisesRegexp(ValueError, "Cycle dependency detected") as _:
            _ = Pipeline(
                steps=[type_transform_step, data_source_step],
            )


class TestPipelineBuild(BaseIntegTestCase):
    def setUp(self):
        super(TestPipelineBuild, self).setUp()
        self.maxDiff = None

    def test_nested_pipeline(self):

        dataset = self.wumai_dataset

        def create_saved_base_pipeline():
            execution_input = PipelineParameter(name="execution", typ="map")

            data_source_step = PipelineStep(
                identifier="data_source",
                provider=ProviderAlibabaPAI,
                version="v1",
                name="dataSource",
                inputs={
                    "execution": execution_input,
                    "inputTableName": dataset.get_table(),
                    "inputTablePartitions": "",
                },
            )

            type_transform_step = PipelineStep(
                identifier="type_transform",
                provider=ProviderAlibabaPAI,
                version="v1",
                name="typeTransform",
                inputs={
                    "inputTable": data_source_step.outputs["outputTable"],
                    "execution": execution_input,
                    "outputTable": gen_temp_table(),
                    "cols_to_double": ",".join(dataset.columns),
                },
            )
            split_step = PipelineStep(
                identifier="split",
                provider=ProviderAlibabaPAI,
                version="v1",
                inputs={
                    "inputTable": type_transform_step.outputs[0],
                    "execution": execution_input,
                    "output1TableName": gen_temp_table(),
                    "fraction": 0.5,
                    "output2TableName": gen_temp_table(),
                },
            )

            version = "v%s" % (str(int(time.time() * 1000)))
            p = Pipeline(
                steps=[split_step],
                outputs=split_step.outputs[:1],
            )

            return p.save(
                identifier="nested-pipeline-test",
                version=version,
            )

        pipeline = create_saved_base_pipeline()
        self.assertIsNotNone(pipeline.pipeline_id)

        prev_pipeline = pipeline
        for idx in range(1, 10):
            execution_input = PipelineParameter(name="execution", typ="map")
            inner_step = PipelineStep(
                identifier=prev_pipeline.identifier,
                version=prev_pipeline.version,
                provider=prev_pipeline.provider,
                name="inner-step-%s" % idx,
                inputs={"execution": execution_input},
            )

            p = Pipeline(steps=[inner_step], outputs=inner_step.outputs[:1],).save(
                identifier="test-nest-pipeline-%s" % idx,
                version="v%s" % (str(int(time.time() * 1000))),
            )

            self.assertIsNotNone(p.pipeline_id)
            prev_pipeline = p

        run_instance = prev_pipeline.run(
            job_name="pysdk-test-nested-pipeline-run",
            arguments={
                "execution": self.get_default_maxc_execution(),
            },
            wait=False,
        )
        run_instance.wait_for_completion(show_outputs=False)
        self.assertEqual(PipelineRunStatus.Succeeded, run_instance.get_status())


if __name__ == "__main__":
    unittest.main()
