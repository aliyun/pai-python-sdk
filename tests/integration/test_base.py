from __future__ import absolute_import

import random
import unittest

from pai.common import ProviderAlibabaPAI
from pai.common.utils import gen_run_node_scoped_placeholder
from pai.core.session import EnvType
from pai.pipeline import PipelineRunStatus, PipelineStep
from pai.pipeline.core import Pipeline
from pai.operator.types import (
    MetadataBuilder,
    PipelineArtifact,
)
from pai.operator.types import ParameterType, PipelineParameter
from tests.integration import BaseIntegTestCase
from tests.integration.utils import t_context


@unittest.skipIf(
    t_context.env_type == EnvType.Light,
    "Light Env do not contain operator provide by PAI",
)
class TestAlgo(BaseIntegTestCase):
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
                metadata=MetadataBuilder.maxc_table(),
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
            sql_step = PipelineStep.from_registered_op(
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

            type_transform_step = PipelineStep.from_registered_op(
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

            normalize_step = PipelineStep.from_registered_op(
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

            split_step = PipelineStep.from_registered_op(
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

            lr_step = PipelineStep.from_registered_op(
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

            offline_model_pred_step = PipelineStep.from_registered_op(
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

            evaluate_step = PipelineStep.from_registered_op(
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
            wait=True,
        )

        self.assertEqual(PipelineRunStatus.Succeeded, run_instance.get_status())
