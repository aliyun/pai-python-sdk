from __future__ import absolute_import

import time
import unittest
from unittest import skip

import yaml

from pai.common import ProviderAlibabaPAI
from pai.pipeline import Pipeline, PipelineStep
from pai.pipeline.core import ContainerComponent
from pai.pipeline.run import PipelineRunStatus
from pai.pipeline.types.artifact import ArtifactDataType, ArtifactLocationType, ArtifactMetadata, \
    PipelineArtifact
from pai.pipeline.types.parameter import PipelineParameter
from pai.session import get_current_pai_session
from pai.utils import gen_temp_table
from tests import BaseTestCase
from . import create_simple_composite_pipeline


class TestSimpleCompositePipeline(BaseTestCase):

    def test_run_composite_pipeline(self):
        p, data_source_step, type_transform_step, split_step = create_simple_composite_pipeline()
        self.assertEqual(len(p.steps), 3)
        self.assertTrue(all(step for step in p.steps if step.name))

        manifest = p.to_dict()
        input_ports = [param["name"] for param in manifest["spec"]["inputs"]["parameters"]] + \
                      [af["name"] for af in manifest["spec"]["inputs"]["artifacts"]]
        self.assertEqual(input_ports, ["execution", "cols_to_double", "table_name"])

        output_ports = [param["name"] for param in manifest["spec"]["outputs"]["parameters"]] + \
                       [af["name"] for af in manifest["spec"]["outputs"]["artifacts"]]

        expected = [item.name for item in
                    [split_step.outputs[0], data_source_step.outputs[0], split_step.outputs[-1]]]
        self.assertEqual(expected, output_ports)

        pipeline_run = p.run(job_name="job_name", arguments={
            "execution": self.get_default_xflow_execution(),
            "cols_to_double": "time,hour,pm2,pm10,so2,co,no2",
            "table_name": self.TestDataSetTables["wumai_data"],
        }, wait=True, log_outputs=True)

        self.assertEqual(pipeline_run.get_status(), PipelineRunStatus.Succeeded)

    def test_composite_pipeline_save(self):
        p, data_source_step, type_transform_step, split_step = create_simple_composite_pipeline()
        self.assertIsNone(p.pipeline_id)

        new_version = "%s" % int(time.time())
        _ = p.save(identifier="test-composite-pipeline", version=new_version)
        self.assertIsNotNone(p.pipeline_id)
        self.assertEqual(p.version, new_version)

    def test_conflict_step_names(self):
        execution_input = PipelineParameter(name="execution", typ="map")
        dataset_input = PipelineArtifact(name="dataset_table", metadata=ArtifactMetadata(
            data_type=ArtifactDataType.DataSet,
            location_type=ArtifactLocationType.MaxComputeTable))

        split_step_1 = PipelineStep(
            name="split-step",
            identifier="split-xflow-maxCompute",
            provider=ProviderAlibabaPAI,
            version="v1",
            inputs={
                "inputArtifact": dataset_input,
                "execution": execution_input,
                "output1TableName": gen_temp_table(),
                "fraction": 0.5,
                "output2TableName": gen_temp_table(),
            }
        )
        split_step_2 = PipelineStep(
            name="split-step",
            identifier="split-xflow-maxCompute",
            provider=ProviderAlibabaPAI,
            version="v1",
            inputs={
                "inputArtifact": dataset_input,
                "execution": execution_input,
                "output1TableName": gen_temp_table(),
                "fraction": 0.5,
                "output2TableName": gen_temp_table(),
            }
        )

        with self.assertRaisesRegexp(ValueError, "name conflict") as _:
            _ = Pipeline(steps=[split_step_1, split_step_2])

    def test_auto_step_name(self):
        execution_input = PipelineParameter(name="execution", typ="map")
        dataset_input = PipelineArtifact(name="dataset_table", metadata=ArtifactMetadata(
            data_type=ArtifactDataType.DataSet,
            location_type=ArtifactLocationType.MaxComputeTable))

        split_step_1 = PipelineStep(
            name="split-step-1", identifier="split-xflow-maxCompute", provider=ProviderAlibabaPAI,
            version="v1", inputs={
                "inputArtifact": dataset_input,
                "execution": execution_input,
                "output1TableName": gen_temp_table(),
                "fraction": 0.5,
                "output2TableName": gen_temp_table(),
            }
        )
        split_step_2 = PipelineStep(
            identifier="split-xflow-maxCompute", provider=ProviderAlibabaPAI, version="v1",
            inputs={
                "inputArtifact": dataset_input,
                "execution": execution_input,
                "output1TableName": gen_temp_table(),
                "fraction": 0.5,
                "output2TableName": gen_temp_table(),
            }
        )
        self.assertIsNone(split_step_2.name)
        _ = Pipeline(steps=[split_step_1, split_step_2])
        self.assertIsNotNone(split_step_2.name)

    def test_pipeline_cycle_detect(self):
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
            }
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
            }
        )
        data_source_step.after(type_transform_step)

        with self.assertRaisesRegexp(ValueError, 'Cycle dependency detected') as _:
            _ = Pipeline(
                identifier="test-pipeline",
                version="v1",
                steps=[type_transform_step, data_source_step],
            )


class TestPipelineBuild(BaseTestCase):

    def setUp(self):
        super(TestPipelineBuild, self).setUp()
        self.maxDiff = None

    def test_nested_pipeline(self):
        def create_saved_base_pipeline():
            execution_input = PipelineParameter(name="xflow_execution", typ="map")

            data_source_step = PipelineStep(
                identifier="dataSource-xflow-maxCompute",
                provider=ProviderAlibabaPAI,
                version="v1",
                name="dataSource",
                inputs={
                    "execution": execution_input,
                    "tableName": self.TestDataSetTables["wumai_data"],
                    "partition": "",
                }
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
                    "cols_to_double": "pm10,so2,co,no2",
                }
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
                }
            )

            version = "v%s" % (str(int(time.time() * 1000)))
            p = Pipeline(
                identifier="nested-pipeline-test",
                version=version,
                steps=[split_step],
                outputs=split_step.outputs[:1]
            )

            return p.save()

        pipeline = create_saved_base_pipeline()
        self.assertIsNotNone(pipeline.pipeline_id)

        prev_pipeline = pipeline
        for idx in range(1, 10):
            xflow_execution_input = PipelineParameter(name="xflow_execution", typ="map")
            inner_step = PipelineStep(
                identifier=prev_pipeline.identifier,
                version=prev_pipeline.version,
                provider=prev_pipeline.provider,
                name="inner-step-%s" % idx,
                inputs={
                    "xflow_execution": xflow_execution_input
                }
            )

            p = Pipeline(
                identifier="test-nest-pipeline-%s" % idx,
                version="v%s" % (str(int(time.time() * 1000))),
                steps=[inner_step],
                outputs=inner_step.outputs[:1],
            ).save()

            self.assertIsNotNone(p.pipeline_id)
            prev_pipeline = p

        run_instance = prev_pipeline.run(job_name="pysdk-test-nested-pipeline-run", arguments={
            "xflow_execution": self.get_default_xflow_execution(),
        }, wait=False)
        self.assertEqual(PipelineRunStatus.Running, run_instance.get_status())
        run_instance.wait_for_completion(log_outputs=False)
        self.assertEqual(PipelineRunStatus.Succeeded, run_instance.get_status())


class TestContainerComponent(BaseTestCase):

    @skip("Only admin has privilege to create container-execution pipeline")
    def test_component_base(self):
        inputs = [
            PipelineParameter(name="xflow_name", typ=str),
            PipelineParameter(name="execution", typ=dict,
                              default=self.get_default_xflow_execution())

        ]
        outputs = [
            PipelineArtifact(name="output1", metadata=ArtifactMetadata(
                data_type=ArtifactDataType.DataSet,
                location_type=ArtifactLocationType.OSS))
        ]

        comp = ContainerComponent(
            image_uri="registry.cn-shanghai.aliyuncs.com/paiflow-core/xflow_base:v1.1",
            inputs=inputs,
            outputs=outputs,
            command=[
                "python",
                "-m",
                "train",
                "--parameter={{inputs.parameters}}"
            ])
        p = comp.save(identifier="test-comp", version=str(time.time()))

        session = get_current_pai_session()

        _ = session.create_run(
            pipeline_id=p.pipeline_id, name="test",
            arguments={
            })


if __name__ == "__main__":
    unittest.main()
