from __future__ import absolute_import

import random
import unittest

import time

from pai.common import ProviderAlibabaPAI
from pai.core.job import JobStatus
from pai.pipeline import PipelineRunStatus, PipelineStep
from pai.operator import SavedOperator
from pai.pipeline.core import Pipeline
from pai.pipeline.types.artifact import (
    DataType,
    LocationType,
    LocationArtifactMetadata,
    PipelineArtifact,
)
from pai.pipeline.types.parameter import ParameterType, PipelineParameter
from pai.common.utils import gen_temp_table, gen_run_node_scoped_placeholder
from pai.algo.classifier import LogisticRegression
from tests.integration import BaseIntegTestCase


class TestEstimator(BaseIntegTestCase):
    def test_algo_init(self):
        lr = LogisticRegression(
            regularized_level=1.0, regularized_type="l2", max_iter=200, epsilon=1e-6
        )
        expected_parameters = {
            "regularized_level": 1.0,
            "regularized_type": "l2",
            "max_iter": 200,
            "epsilon": 1e-6,
        }

        parameters = {k: v for k, v in lr.parameters.items() if v is not None}

        self.assertEqual(expected_parameters, parameters)

    def test_algo_init_with_pmml(self):
        lr = LogisticRegression(
            regularized_level=2.0,
            regularized_type="l1",
            max_iter=100,
            epsilon=1e-5,
            pmml_gen=True,
            pmml_oss_rolearn="test_role_arn",
            pmml_oss_bucket="test_oss_bucket",
            pmml_oss_path="test_oss_path",
            pmml_oss_endpoint="cn-hangzhou.oss.aliyuncs.com",
        )
        expected_parameters = {
            "regularized_level": 2.0,
            "regularized_type": "l1",
            "max_iter": 100,
            "epsilon": 1e-5,
            "pmml_gen": True,
            "pmml_oss_rolearn": "test_role_arn",
            "pmml_oss_bucket": "test_oss_bucket",
            "pmml_oss_path": "test_oss_path",
            "pmml_oss_endpoint": "cn-hangzhou.oss.aliyuncs.com",
        }
        parameters = {k: v for k, v in lr.parameters.items() if v is not None}
        self.assertEqual(expected_parameters, parameters)

    def test_estimator_build(self):
        lr = LogisticRegression()

        args = {
            "regularized_level": 1.0,
            "regularized_type": "l2",
            "max_iter": 200,
            "epsilon": 1e-6,
            "feature_cols": ["pm2", "co2"],
            "label_col": "_c2",
            "model_name": "ut_lr_model",
            "enable_sparse": True,
            "sparse_delimiter": (",", ":"),
        }

        expected = {
            "regularizedLevel": 1.0,
            "maxIter": 200,
            "epsilon": 1e-6,
            "featureColNames": "pm2,co2",
            "labelColName": "_c2",
            "modelName": "ut_lr_model",
            "enableSparse": True,
            "itemDelimiter": ",",
            "kvDelimiter": ":",
            "execution": lr.execution,
        }

        compiled_args = lr._compile_args("pai_temp_table", **args)

        result_args = {k: v for k, v in compiled_args.items() if k in expected}

        self.assertDictEqual(result_args, expected)


class TestAlgo(BaseIntegTestCase):
    @unittest.skip("Simplify the test case")
    def test_heart_disease_step_by_step(self):
        maxc_execution = self.get_default_maxc_execution()

        dataset = self.heart_disease_prediction_dataset

        sql = (
            "select age, (case sex when 'male' then 1 else 0 end) as sex, (case cp when "
            "'angina' then 0  when 'notang' then 1 else 2 end) as cp, trestbps, chol, (case"
            " fbs when 'true' then 1 else 0 end) as fbs, (case restecg when 'norm' then 0 "
            " when 'abn' then 1 else 2 end) as restecg, thalach, (case exang when 'true' then"
            " 1 else 0 end) as exang, oldpeak, (case slop when 'up' then 0  when 'flat' then "
            "1 else 2 end) as slop, ca, (case thal when 'norm' then 0  when 'fix' then 1"
            " else 2 end) as thal, (case status  when 'sick' then 1 else 0 end) as"
            " ifHealth from ${t1};"
        )

        # Extract and transform dataset using max_compute sql.
        sql_job = SavedOperator.get_by_identifier(
            identifier="sql", provider=ProviderAlibabaPAI, version="v1"
        ).run(
            job_name="sql-job",
            arguments={
                "execution": maxc_execution,
                "inputArtifact1": dataset.to_url(),
                "sql": sql,
                "outputTable": gen_temp_table(),
            },
        )

        time.sleep(10)
        output_table_artifact = sql_job.get_outputs()[0]

        type_transform_job = SavedOperator.get_by_identifier(
            identifier="type_transform",
            provider=ProviderAlibabaPAI,
            version="v1",
        ).run(
            job_name="transform-job",
            arguments={
                "execution": maxc_execution,
                "inputArtifact": output_table_artifact,
                "cols_to_double": "sex,cp,fbs,restecg,exang,slop,thal,"
                "ifhealth,age,trestbps,chol,thalach,oldpeak,ca",
                "outputTable": gen_temp_table(),
            },
        )

        time.sleep(20)
        type_transform_result = type_transform_job.get_outputs()[0]

        # Normalize Feature
        normalize_job = SavedOperator.get_by_identifier(
            identifier="normalize_1",
            provider=ProviderAlibabaPAI,
            version="v1",
        ).run(
            job_name="normalize-job",
            arguments={
                "execution": maxc_execution,
                "inputArtifact": type_transform_result,
                "selectedColNames": "sex,cp,fbs,restecg,exang,slop,thal,ifhealth,age,trestbps,"
                "chol,thalach,oldpeak,ca",
                "lifecycle": 1,
                "outputTableName": gen_temp_table(),
                "outputParaTableName": gen_temp_table(),
            },
        )
        time.sleep(20)
        normalized_dataset = normalize_job.get_outputs()[0]

        split_job = SavedOperator.get_by_identifier(
            identifier="split",
            provider=ProviderAlibabaPAI,
            version="v1",
        ).run(
            job_name="split-job",
            arguments={
                "inputArtifact": normalized_dataset,
                "execution": maxc_execution,
                "fraction": 0.8,
                "output1TableName": gen_temp_table(),
                "output2TableName": gen_temp_table(),
            },
        )

        time.sleep(20)
        split_output_1, split_output_2 = split_job.get_outputs()

        oss_endpoint = self.oss_config.endpoint
        oss_path = "/paiflow/model_transfer2oss_test/"
        oss_bucket = self.oss_config.bucket_name
        lr_job = LogisticRegression(
            regularized_type="l2",
            xflow_execution=maxc_execution,
            pmml_gen=True,
            pmml_oss_bucket=oss_bucket,
            pmml_oss_path=oss_path,
            pmml_oss_endpoint=oss_endpoint,
            pmml_oss_rolearn=self.oss_config.role_arn,
        ).fit(
            split_output_1,
            wait=True,
            feature_cols="sex,cp,fbs,restecg,exang,slop,"
            "thal,age,trestbps,chol,thalach,oldpeak,ca",
            label_col="ifhealth",
            good_value=1,
            model_name="test_health_prediction",
        )

        time.sleep(20)
        offlinemodel_artifact, pmml_output = lr_job.get_outputs()
        transform_job = SavedOperator.get_by_identifier(
            identifier="Prediction_1",
            provider=ProviderAlibabaPAI,
            version="v1",
        ).run(
            job_name="pred-job",
            arguments={
                "inputModelArtifact": offlinemodel_artifact,
                "inputDataSetArtifact": split_output_2,
                "execution": maxc_execution,
                "outputTableName": gen_temp_table(),
                "featureColNames": "sex,cp,fbs,restecg,exang,slop,thal,"
                "age,trestbps,chol,thalach,oldpeak,ca",
                "appendColNames": "ifhealth",
            },
        )

        time.sleep(20)
        transform_result = transform_job.get_outputs()[0]

        evaluate_job = SavedOperator.get_by_identifier(
            identifier="evaluate_1",
            provider=ProviderAlibabaPAI,
            version="v1",
        ).run(
            job_name="evaluate-job",
            arguments={
                "execution": maxc_execution,
                "inputArtifact": transform_result,
                "outputDetailTableName": gen_temp_table(),
                "outputELDetailTableName": gen_temp_table(),
                "outputMetricTableName": gen_temp_table(),
                "scoreColName": "prediction_score",
                "labelColName": "ifhealth",
                "coreNum": 2,
                "memSizePerCore": 512,
            },
        )

        time.sleep(20)

        self.assertEqual(JobStatus.Succeeded, evaluate_job.get_status())
        time.sleep(10)

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
                metadata=LocationArtifactMetadata(
                    data_type=DataType.DataSet,
                    location_type=LocationType.MaxComputeTable,
                ),
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
            sql_step = PipelineStep(
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

            type_transform_step = PipelineStep(
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

            normalize_step = PipelineStep(
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

            split_step = PipelineStep(
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

            lr_step = PipelineStep(
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

            offline_model_pred_step = PipelineStep(
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

            evaluate_step = PipelineStep(
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
        p.dot()

        pmml_oss_endpoint = self.oss_config.endpoint
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
        )

        self.assertEqual(PipelineRunStatus.Succeeded, run_instance.get_status())
