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

import random
import re
import time
import unittest
import uuid

import pytest

from pai.common import ProviderAlibabaPAI
from pai.pipeline import Pipeline, PipelineStep
from pai.pipeline.run import PipelineRunStatus
from pai.pipeline.types import (
    ArtifactMetadataUtils,
    DataType,
    LocationArtifactMetadata,
    LocationType,
    ParameterType,
    PipelineArtifact,
    PipelineParameter,
)
from tests.integration import BaseIntegTestCase
from tests.integration.tests_pipeline import create_simple_composite_pipeline
from tests.integration.utils import gen_run_node_scoped_placeholder, gen_temp_table


class TestPipelineRun(BaseIntegTestCase):
    @pytest.mark.timeout(60 * 10)
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

        split_step_1 = PipelineStep.from_registered_component(
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
        split_step_2 = PipelineStep.from_registered_component(
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

        with self.assertRaisesRegex(ValueError, "name conflict") as _:
            _ = Pipeline(steps=[split_step_1, split_step_2])

    def test_auto_step_name(self):
        execution_input = PipelineParameter(name="execution", typ="map")
        dataset_input = PipelineArtifact(
            name="dataset_table",
            metadata=LocationArtifactMetadata(
                data_type=DataType.DataSet, location_type=LocationType.MaxComputeTable
            ),
        )

        split_step_1 = PipelineStep.from_registered_component(
            name="split-step-1",
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
        split_step_2 = PipelineStep.from_registered_component(
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
        self.assertIsNone(split_step_2.name)
        _ = Pipeline(steps=[split_step_1, split_step_2])
        self.assertIsNotNone(split_step_2.name)

    def test_pipeline_cycle_detect(self):
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
                "outputTable": gen_temp_table(),
                "cols_to_double": cols_to_double_input,
            },
        )
        data_source_step.after(type_transform_step)

        with self.assertRaisesRegex(ValueError, "Cycle dependency detected") as _:
            _ = Pipeline(
                steps=[type_transform_step, data_source_step],
            )


class TestPipelineBuild(BaseIntegTestCase):
    def setUp(self):
        super(TestPipelineBuild, self).setUp()
        self.maxDiff = None

    @pytest.mark.timeout(60 * 10)
    def test_nested_pipeline(self):
        dataset = self.wumai_dataset

        def create_saved_base_pipeline():
            execution_input = PipelineParameter(name="execution", typ="map")

            data_source_step = PipelineStep.from_registered_component(
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

            type_transform_step = PipelineStep.from_registered_component(
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
            split_step = PipelineStep.from_registered_component(
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
            inner_step = PipelineStep.from_registered_component(
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

    @pytest.mark.timeout(60 * 15)
    def test_heart_disease_prediction_pipeline(self):
        dataset = type(self).heart_disease_prediction_dataset
        full_col_names = ",".join(dataset.feature_cols + [dataset.label_col])
        print(full_col_names)

        def create_pipeline():
            pmml_oss_bucket = PipelineParameter("pmml_oss_bucket")
            pmml_oss_rolearn = PipelineParameter("pmml_oss_rolearn")
            pmml_oss_path = PipelineParameter("pmml_oss_path")
            pmml_oss_endpoint = PipelineParameter("pmml_oss_endpoint")
            execution = PipelineParameter("execution", ParameterType.Map)
            dataset_input = PipelineArtifact(
                "dataset-table",
                metadata=ArtifactMetadataUtils.maxc_table(),
                required=True,
            )

            sql = (
                "select age, (case sex when 'male' then 1 else 0 end) as sex,(case cp when"
                " 'angina' then 0  when 'notang' then 1 else 2 end) as cp, trestbps, chol,"
                " (case fbs when 'true' then 1 else 0 end) as fbs, (case restecg when 'norm'"
                " then 0  when 'abn' then 1 else 2 end) as restecg, thalach, (case exang when"
                " 'true' then 1 else 0 end) as exang, oldpeak, (case slop when 'up' then 0  "
                "when 'flat' then 1 else 2 end) as slop, ca, (case thal when 'norm' then 0 "
                " when 'fix' then 1 else 2 end) as thal, (case status when 'sick' then 1 else "
                "0 end) as ifHealth from ${t1};"
            )
            sql_step = PipelineStep.from_registered_component(
                "sql",
                name="sql-1",
                provider=ProviderAlibabaPAI,
                version="v1",
                inputs={
                    "inputTable1": dataset_input,
                    "execution": execution,
                    "sql": sql,
                    "outputTableName": gen_run_node_scoped_placeholder(
                        suffix="outputTable"
                    ),
                },
            )

            type_transform_step = PipelineStep.from_registered_component(
                "type_transform",
                name="type-transform-1",
                provider=ProviderAlibabaPAI,
                version="v1",
                inputs={
                    "execution": execution,
                    "inputTable": sql_step.outputs["outputTable"],
                    "cols_to_double": full_col_names,
                    "outputTable": gen_run_node_scoped_placeholder(
                        suffix="outputTable"
                    ),
                },
            )

            normalize_step = PipelineStep.from_registered_component(
                "normalize_1",
                name="normalize-1",
                provider=ProviderAlibabaPAI,
                version="v1",
                inputs={
                    "execution": execution,
                    "inputTable": type_transform_step.outputs["outputTable"],
                    "selectedColNames": full_col_names,
                    "lifecycle": 1,
                    "outputTableName": gen_run_node_scoped_placeholder(
                        suffix="outputTable"
                    ),
                    "outputParaTableName": gen_run_node_scoped_placeholder(
                        suffix="outputParaTable"
                    ),
                },
            )

            split_step = PipelineStep.from_registered_component(
                identifier="split",
                name="split-1",
                provider=ProviderAlibabaPAI,
                version="v1",
                inputs={
                    "inputTable": normalize_step.outputs["outputTable"],
                    "execution": execution,
                    "fraction": 0.8,
                    "output1TableName": gen_run_node_scoped_placeholder(
                        suffix="output1Table"
                    ),
                    "output2TableName": gen_run_node_scoped_placeholder(
                        suffix="output2Table"
                    ),
                },
            )

            model_name = "test_health_prediction_by_pipeline_%s" % (
                random.randint(0, 999999)
            )

            lr_step = PipelineStep.from_registered_component(
                identifier="logisticregression_binary",
                name="logisticregression-1",
                provider=ProviderAlibabaPAI,
                version="v1",
                inputs={
                    "inputTable": split_step.outputs["output1Table"],
                    "execution": execution,
                    "generatePmml": True,
                    "pmmlOssEndpoint": pmml_oss_endpoint,
                    "pmmlOssBucket": pmml_oss_bucket,
                    "pmmlOssPath": pmml_oss_path,
                    "pmmlOverwrite": True,
                    "roleArn": pmml_oss_rolearn,
                    "regularizedLevel": 1.0,
                    "regularizedType": "l2",
                    "modelName": model_name,
                    "goodValue": 1,
                    "featureColNames": ",".join(dataset.feature_cols),
                    "labelColName": dataset.label_col,
                },
            )

            offline_model_pred_step = PipelineStep.from_registered_component(
                identifier="Prediction_1",
                name="offlinemodel-pred",
                provider=ProviderAlibabaPAI,
                version="v1",
                inputs={
                    "model": lr_step.outputs["model"],
                    "inputTable": split_step.outputs["output2Table"],
                    "execution": execution,
                    "outputTableName": gen_run_node_scoped_placeholder(
                        suffix="outputTable"
                    ),
                    "featureColNames": ",".join(dataset.feature_cols),
                    "appendColNames": dataset.label_col,
                },
            )

            evaluate_step = PipelineStep.from_registered_component(
                identifier="evaluate_1",
                name="evaluate-1",
                provider=ProviderAlibabaPAI,
                version="v1",
                inputs={
                    "execution": execution,
                    "inputTable": offline_model_pred_step.outputs["outputTable"],
                    "outputDetailTableName": gen_run_node_scoped_placeholder(
                        suffix="outputDetail"
                    ),
                    "outputELDetailTableName": gen_run_node_scoped_placeholder(
                        suffix="outputELDetail"
                    ),
                    "outputMetricTableName": gen_run_node_scoped_placeholder(
                        suffix="outputMetricDetail"
                    ),
                    "scoreColName": "prediction_score",
                    "labelColName": dataset.label_col,
                },
            )

            p = Pipeline(
                steps=[evaluate_step, offline_model_pred_step],
                outputs={
                    "pmmlModel": lr_step.outputs["PMMLOutput"],
                    "evaluateResult": evaluate_step.outputs["outputMetricTable"],
                },
            )
            return p

        p = create_pipeline()

        pmml_oss_endpoint = self.to_internal_endpoint(self.oss_config.endpoint)
        pmml_oss_path = "/test/pai/model_transfer2oss_test/"
        pmml_oss_bucket = self.oss_config.bucket_name
        pmml_oss_rolearn = self.oss_config.role_arn

        run_instance = p.run(
            job_name="test_heart_disease_pred",
            arguments={
                "execution": self.get_default_maxc_execution(),
                "pmml_oss_rolearn": pmml_oss_rolearn,
                "pmml_oss_path": pmml_oss_path,
                "pmml_oss_bucket": pmml_oss_bucket,
                "pmml_oss_endpoint": pmml_oss_endpoint,
                "dataset-table": dataset.to_url(),
            },
            wait=True,
        )

        self.assertEqual(PipelineRunStatus.Succeeded, run_instance.get_status())

    @classmethod
    def to_internal_endpoint(cls, oss_endpoint):
        """Transform OSS endpoint to internal endpoint."""
        OssEndpointPattern = re.compile(
            r"oss-(.[a-zA-Z0-9\-]+?)(?:-internal)?\.aliyuncs\.com"
        )
        m = OssEndpointPattern.match(oss_endpoint)
        if not m:
            return oss_endpoint
        region = m.groups()[0]
        return "oss-{}-internal.aliyuncs.com".format(region)


if __name__ == "__main__":
    unittest.main()
