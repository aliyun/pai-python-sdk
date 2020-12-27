from __future__ import absolute_import

import random
import unittest

import time

from pai.common import ProviderAlibabaPAI
from pai.core.job import JobStatus
from pai.pipeline import PipelineRunStatus, PipelineStep
from pai.pipeline.core import Pipeline, get_default_session
from pai.pipeline.template import PipelineTemplate
from pai.pipeline.types.artifact import (
    ArtifactDataType,
    ArtifactLocationType,
    ArtifactMetadata,
    PipelineArtifact,
)
from pai.pipeline.types.parameter import ParameterType, PipelineParameter
from pai.common.utils import gen_temp_table
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
            "execution": lr.max_compute_execution,
        }

        compiled_args = lr._compile_args("pai_temp_table", **args)

        result_args = {k: v for k, v in compiled_args.items() if k in expected}

        self.assertDictEqual(result_args, expected)

    def test_multiple_call_fit(self):
        pass


class TestXFlowAlgo(BaseIntegTestCase):

    # TODO: Simplify the test case
    @unittest.skip("Simplify the test case")
    def test_algo_chain(self):
        default_project = self.odps_client.project
        maxc_execution = self.get_default_maxc_execution()
        data_set = self.odps_client.get_table(
            self.TestDataSetTables["processed_wumai_data_1"]
        )

        split_job = PipelineTemplate.get_by_identifier(
            identifier="split-xflow-maxCompute",
            provider=ProviderAlibabaPAI,
            version="v1",
        ).run(
            job_name="split-job",
            arguments={
                "execution": maxc_execution,
                "fraction": 0.7,
                "inputArtifact": data_set,
                "output1TableName": gen_temp_table(),
                "output2TableName": gen_temp_table(),
            },
        )

        self.assertEqual(PipelineRunStatus.Succeeded, split_job.get_status())
        time.sleep(10)  # Because of outputs delay.
        job_outputs = split_job.get_outputs()
        dataset1 = job_outputs[0]
        dataset2 = job_outputs[1]

        oss_endpoint = self.oss_config.endpoint
        oss_path = "/pai_test/test_algo_chain/"
        oss_bucket = self.oss_config.bucket_name

        model_name = "test_iris_model_%d" % (random.randint(0, 999999))
        lr = LogisticRegression(
            regularized_type="l2",
            pmml_gen=True,
            pmml_oss_bucket=oss_bucket,
            pmml_oss_path=oss_path,
            pmml_oss_endpoint=oss_endpoint,
            pmml_oss_rolearn=self.oss_config.role_arn,
            max_compute_execution=maxc_execution,
        )

        feature_cols = ["pm10", "so2", "co", "no2"]
        label_col = "_c2"

        job = lr.fit(
            wait=True,
            input_data=dataset1,
            job_name="pysdk-test-lr-sync-fit",
            model_name=model_name,
            good_value=1,
            label_col=label_col,
            feature_cols=feature_cols,
        )
        self.assertEqual(JobStatus.Succeeded, job.get_status())
        time.sleep(10)  # Because of outputs delay.
        self.assertTrue(
            self.odps_client.exist_offline_model(
                model_name,
                default_project,
            )
        )
        model = job.create_model(output_name="outputArtifact")
        tf = model.transformer(xflow_execution=maxc_execution)
        job = tf.transform(
            input_data=dataset2,
            wait=False,
            feature_cols=feature_cols,
            append_cols=feature_cols + [label_col],
            label_col=label_col,
        )
        job.wait_for_completion(show_outputs=False)
        self.assertEqual(JobStatus.Succeeded, job.get_status())

    # TODO: Simplify the test case
    @unittest.skip("Simplify the test case")
    def test_heart_disease_step_by_step(self):
        xflow_execution = self.get_default_maxc_execution()

        dataset_table = self.odps_client.get_table(
            self.TestDataSetTables["heart_disease_prediction"]
        )

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
        sql_job = PipelineTemplate.get_by_identifier(
            identifier="sql-xflow-maxCompute", provider=ProviderAlibabaPAI, version="v1"
        ).run(
            job_name="sql-job",
            arguments={
                "execution": xflow_execution,
                "inputArtifact1": dataset_table,
                "sql": sql,
                "outputTable": gen_temp_table(),
            },
        )

        time.sleep(10)
        output_table_artifact = sql_job.get_outputs()[0]

        type_transform_job = PipelineTemplate.get_by_identifier(
            identifier="type-transform-xflow-maxCompute",
            provider=ProviderAlibabaPAI,
            version="v1",
        ).run(
            job_name="transform-job",
            arguments={
                "execution": xflow_execution,
                "inputArtifact": output_table_artifact,
                "cols_to_double": "sex,cp,fbs,restecg,exang,slop,thal,"
                "ifhealth,age,trestbps,chol,thalach,oldpeak,ca",
                "outputTable": gen_temp_table(),
            },
        )

        time.sleep(20)
        type_transform_result = type_transform_job.get_outputs()[0]

        # Normalize Feature
        normalize_job = PipelineTemplate.get_by_identifier(
            identifier="normalize-xflow-maxCompute",
            provider=ProviderAlibabaPAI,
            version="v1",
        ).run(
            job_name="normalize-job",
            arguments={
                "execution": xflow_execution,
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

        split_job = PipelineTemplate.get_by_identifier(
            identifier="split-xflow-maxCompute",
            provider=ProviderAlibabaPAI,
            version="v1",
        ).run(
            job_name="split-job",
            arguments={
                "inputArtifact": normalized_dataset,
                "execution": xflow_execution,
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
            xflow_execution=xflow_execution,
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
        transform_job = PipelineTemplate.get_by_identifier(
            identifier="prediction-xflow-maxCompute",
            provider=ProviderAlibabaPAI,
            version="v1",
        ).run(
            job_name="pred-job",
            arguments={
                "inputModelArtifact": offlinemodel_artifact,
                "inputDataSetArtifact": split_output_2,
                "execution": xflow_execution,
                "outputTableName": gen_temp_table(),
                "featureColNames": "sex,cp,fbs,restecg,exang,slop,thal,"
                "age,trestbps,chol,thalach,oldpeak,ca",
                "appendColNames": "ifhealth",
            },
        )

        time.sleep(20)
        transform_result = transform_job.get_outputs()[0]

        evaluate_job = PipelineTemplate.get_by_identifier(
            identifier="evaluate-xflow-maxCompute",
            provider=ProviderAlibabaPAI,
            version="v1",
        ).run(
            job_name="evaluate-job",
            arguments={
                "execution": xflow_execution,
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
        def create_pipeline():
            pmml_oss_bucket = PipelineParameter("pmml_oss_bucket")
            pmml_oss_rolearn = PipelineParameter("pmml_oss_rolearn")
            pmml_oss_path = PipelineParameter("pmml_oss_path")
            pmml_oss_endpoint = PipelineParameter("pmml_oss_endpoint")
            xflow_execution = PipelineParameter("xflow_execution", ParameterType.Map)
            dataset_input = PipelineArtifact(
                "dataset-table",
                metadata=ArtifactMetadata(
                    data_type=ArtifactDataType.DataSet,
                    location_type=ArtifactLocationType.MaxComputeTable,
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
                "sql-xflow-maxCompute",
                name="sql-1",
                provider=ProviderAlibabaPAI,
                version="v1",
                inputs={
                    "inputArtifact1": dataset_input,
                    "execution": xflow_execution,
                    "sql": sql,
                    "outputTable": gen_temp_table(),
                },
            )

            type_transform_step = PipelineStep(
                "type-transform-xflow-maxCompute",
                name="type-transform-1",
                provider=ProviderAlibabaPAI,
                version="v1",
                inputs={
                    "execution": xflow_execution,
                    "inputArtifact": sql_step.outputs["outputArtifact"],
                    "cols_to_double": "sex,cp,fbs,restecg,exang,slop,thal,ifhealth,age,trestbps,"
                    "chol,thalach,oldpeak,ca",
                    "outputTable": gen_temp_table(),
                },
            )

            normalize_step = PipelineStep(
                "normalize-xflow-maxCompute",
                name="normalize-1",
                provider=ProviderAlibabaPAI,
                version="v1",
                inputs={
                    "execution": xflow_execution,
                    "inputArtifact": type_transform_step.outputs["outputArtifact"],
                    "selectedColNames": "sex,cp,fbs,restecg,exang,slop,thal,ifhealth,age,trestbps,"
                    "chol,thalach,oldpeak,ca",
                    "lifecycle": 1,
                    "outputTableName": gen_temp_table(),
                    "outputParaTableName": gen_temp_table(),
                },
            )

            split_step = PipelineStep(
                identifier="split-xflow-maxCompute",
                name="split-1",
                provider=ProviderAlibabaPAI,
                version="v1",
                inputs={
                    "inputArtifact": normalize_step.outputs["outputArtifact"],
                    "execution": xflow_execution,
                    "fraction": 0.8,
                    "output1TableName": gen_temp_table(),
                    "output2TableName": gen_temp_table(),
                },
            )

            model_name = "test_health_prediction_by_pipeline_%s" % (
                random.randint(0, 999999)
            )

            lr_step = PipelineStep(
                identifier="logisticregression-binary-xflow-maxCompute",
                name="logisticregression-1",
                provider=ProviderAlibabaPAI,
                version="v1",
                inputs={
                    "inputArtifact": split_step.outputs["outputArtifact1"],
                    "execution": xflow_execution,
                    "generatePmml": True,
                    "endpoint": pmml_oss_endpoint,
                    "bucket": pmml_oss_bucket,
                    "path": pmml_oss_path,
                    "rolearn": pmml_oss_rolearn,
                    "regularizedLevel": 1.0,
                    # "regularizedType": "l2",
                    "modelName": model_name,
                    "goodValue": 1,
                    "featureColNames": "sex,cp,fbs,restecg,exang,slop,"
                    "thal,age,trestbps,chol,thalach,oldpeak,ca",
                    "labelColName": "ifhealth",
                },
            )

            offline_model_pred_step = PipelineStep(
                identifier="prediction-xflow-maxCompute",
                name="offlinemodel-pred",
                provider=ProviderAlibabaPAI,
                version="v1",
                inputs={
                    "inputModelArtifact": lr_step.outputs["outputArtifact"],
                    "inputDataSetArtifact": split_step.outputs["outputArtifact2"],
                    "execution": xflow_execution,
                    "outputTableName": gen_temp_table(),
                    "featureColNames": "sex,cp,fbs,restecg,exang,slop,"
                    "thal,age,trestbps,chol,thalach,oldpeak,ca",
                    "appendColNames": "ifhealth",
                },
            )

            evaluate_step = PipelineStep(
                identifier="evaluate-xflow-maxCompute",
                name="evaluate-1",
                provider=ProviderAlibabaPAI,
                version="v1",
                inputs={
                    "execution": xflow_execution,
                    "inputArtifact": offline_model_pred_step.outputs["outputArtifact"],
                    "outputDetailTableName": gen_temp_table(),
                    "outputELDetailTableName": gen_temp_table(),
                    "outputMetricTableName": gen_temp_table(),
                    "scoreColName": "prediction_score",
                    "labelColName": "ifhealth",
                    "coreNum": 2,
                    "memSizePerCore": 512,
                },
            )

            p = Pipeline(
                steps=[evaluate_step, offline_model_pred_step],
                outputs={
                    "pmmlModel": lr_step.outputs["outputArtifact"],
                    "evaluateResult": evaluate_step.outputs["outputMetricsArtifact"],
                },
            )
            return p

        p = create_pipeline()
        p.dot()

        pmml_oss_endpoint = self.oss_config.endpoint
        pmml_oss_path = "/paiflow/model_transfer2oss_test/"
        pmml_oss_bucket = self.oss_config.bucket_name
        pmml_oss_rolearn = self.oss_config.role_arn

        dataset_table = self.odps_client.get_table(
            self.TestDataSetTables["heart_disease_prediction"]
        )

        run_instance = p.run(
            job_name="test_run",
            arguments={
                "xflow_execution": self.get_default_maxc_execution(),
                "pmml_oss_rolearn": pmml_oss_rolearn,
                "pmml_oss_path": pmml_oss_path,
                "pmml_oss_bucket": pmml_oss_bucket,
                "pmml_oss_endpoint": pmml_oss_endpoint,
                "dataset-table": dataset_table,
            },
            wait=False,
        )
        run_instance.wait_for_completion(show_outputs=True)

        self.assertEqual(PipelineRunStatus.Succeeded, run_instance.get_status())
