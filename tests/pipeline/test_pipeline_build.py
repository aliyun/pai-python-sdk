from __future__ import absolute_import

import os
import time
import unittest

from pai.pipeline import Pipeline, PipelineStep
from pai.pipeline.parameter import ParameterType
from pai.common import ProviderAlibabaPAI
from pai.pipeline.artifact import ArtifactDataType, ArtifactLocationType
from pai.pipeline.run import RunInstance, RunStatus
from pai.xflow.classifier import LogisticRegression
from tests import BaseTestCase
from tests.pipeline import load_local_yaml

_current_dir = os.path.dirname(os.path.abspath(__file__))


class TestPipelineBuild(BaseTestCase):

    def setUp(self):
        super(TestPipelineBuild, self).setUp()
        self.maxDiff = None

    @unittest.skip("Skip")
    def test_air_quality_pipeline_create(self):
        pipeline = self.create_air_quality_prediction(self.session)
        expected = load_local_yaml("unittest-air-quality.yaml")
        pipeline_def = pipeline.to_dict()
        self.assertDictEqual(pipeline_def, expected)

        new_version = "v%s" % (str(int(time.time() * 1000)))
        pipeline_def["metadata"]["version"] = new_version

        pipeline_id = self.session.create_pipeline(pipeline_def)
        self.assertIsNotNone(pipeline_id)

    def test_cycle_detection(self):
        with self.assertRaises(ValueError):
            self.create_cycle_pipeline()

    def test_general_input(self):
        p = self.create_general_input_pipeline()
        pipeline_def = p.to_dict()

        pipeline_executions = [param["from"] for p in pipeline_def["spec"]["pipelines"] for param in
                               p["spec"]["arguments"]["parameters"] if
                               param["name"] == "execution"]

        expected_execution = "{{inputs.parameters.execution}}"
        self.assertTrue(
            all(expected_execution == execution_param for execution_param in pipeline_executions))

        pipeline_generate_pmml = [param["value"] for p in pipeline_def["spec"]["pipelines"] for
                                  param in
                                  p["spec"]["arguments"]["parameters"] if
                                  param["name"] == "__generatePMML"]
        # expected_val = True
        self.assertTrue(all(param for param in pipeline_generate_pmml))

        return

    def test_parameter_with_feasible(self):
        pass

    def test_temp_composite_pipeline_run(self):
        p = self.create_composite_pipeline_case_1()
        arguments = {"execution":
            {
                "odpsInfoFile": "/share/base/odpsInfo.ini",
                "endpoint": "http://service.cn-shanghai.maxcompute.aliyun.com/api",
                "logViewHost": "http://logview.odps.aliyun.com",
                "odpsProject": "wyl_test",
            },
            "cols_to_double": "time,hour,pm2,pm10,so2,co,no2",
            "table_name": "pai_online_project.wumai_data",
        }

        run = p.run("pysdk-test-temp-pl-run", arguments=arguments,
                    wait=False)
        self.assertIsNotNone(run)
        self.assertEqual(run.get_status(), RunStatus.Running)
        run.wait(log_outputs=False)
        self.assertEqual(run.get_status(), RunStatus.Succeeded)

    def test_composite_pipeline_submit(self):
        p = self.create_composite_pipeline_case_1()
        arguments, env = self.args_for_composite_pipeline_1()

        pipeline_id = self.session.create_pipeline(p.to_dict())
        run_id = self.session.create_run("pysdk-test-composite-run",
                                         pipeline_id=pipeline_id,
                                         arguments=arguments, env=env)
        self.assertIsNotNone(run_id)
        time.sleep(1)
        run_instance = RunInstance(run_id=run_id, session=self.session)
        self.assertEqual(run_instance.get_status(), RunStatus.Running)
        run_instance.wait(log_outputs=False)
        self.assertEqual(run_instance.get_status(), RunStatus.Succeeded)

    @staticmethod
    def add_local_pipeline_step(pipeline, identifier, name=None):
        manifest = load_local_yaml("%s.yaml" % identifier)
        name = name if name else identifier
        step = PipelineStep.create_from_manifest(manifest, pipeline, name=name)
        pipeline.steps[step.name] = step
        return step

    @staticmethod
    def create_air_quality_prediction(session):
        # version = "v%s" % (str(int(time.time() * 1000)))
        p = Pipeline.new_pipeline("ut-air-quality", version="v1.0.0", session=session)

        execution_input = p.create_input_parameter("execution", "map", required=True)
        cols_to_double_input = p.create_input_parameter("cols_to_double", str, required=True)
        hist_cols_input = p.create_input_parameter("histogram_selected_col_names", str,
                                                   required=True)
        sql_input = p.create_input_parameter("sql", str, required=True)
        normalize_cols_input = p.create_input_parameter("normalize_selected_col_names", str,
                                                        required=True)
        fraction_input = p.create_input_parameter("fraction", float, required=True)
        randomforest_feature_cols_input = p.create_input_parameter("randomforest_feature_col_names",
                                                                   str, required=True)
        randomforest_label_col_input = p.create_input_parameter("randomforest_label_col_names", str,
                                                                required=True)
        prediction1_feature_col_input = p.create_input_parameter("prediction1_feature_col_names",
                                                                 str, required=True)
        prediction1_append_col_input = p.create_input_parameter("prediction1_append_col_names", str,
                                                                required=True)
        prediction1_result_col_input = p.create_input_parameter("prediction1_result_col_names", str,
                                                                required=True)
        prediction1_score_col_input = p.create_input_parameter("prediction1_score_col_names", str,
                                                               required=True)
        prediction1_detail_col_input = p.create_input_parameter("prediction1_detail_col_names", str,
                                                                required=True)

        evaluate1_label_col_input = p.create_input_parameter("evaluate1_label_col_name", str,
                                                             required=True)
        evaluate1_score_col_input = p.create_input_parameter("evaluate1_score_col_name", str,
                                                             required=True)
        evaluate1_positive_label_input = p.create_input_parameter("evaluate1_positive_label", int,
                                                                  required=True)
        evaluate1_bin_count_input = p.create_input_parameter("evaluate1_bin_count", int,
                                                             required=True)

        logistic_feature_col_input = p.create_input_parameter(
            "logisticregression_feature_col_names", str,
            required=True)
        logistic_label_col_names = p.create_input_parameter("logisticregression_label_col_names",
                                                            str, required=True)
        logistic_good_value_input = p.create_input_parameter("logisticregression_good_value", int,
                                                             required=True)

        prediction2_feature_col_input = p.create_input_parameter("prediction2_feature_col_names",
                                                                 str, required=True)
        prediction2_append_col_input = p.create_input_parameter("prediction2_append_col_names", str,
                                                                required=True)
        prediction2_result_col_input = p.create_input_parameter("prediction2_result_col_names", str,
                                                                required=True)
        prediction2_score_col_input = p.create_input_parameter("prediction2_score_col_names", str,
                                                               required=True)
        prediction2_detail_col_input = p.create_input_parameter("prediction2_detail_col_names", str,
                                                                required=True)

        evaluate2_label_col_input = p.create_input_parameter("evaluate2_label_col_name", str,
                                                             required=True)
        evaluate2_score_col_input = p.create_input_parameter("evaluate2_score_col_name", str,
                                                             required=True)
        evaluate2_positive_label_input = p.create_input_parameter("evaluate2_positive_label", int,
                                                                  required=True)
        evaluate2_bin_count_input = p.create_input_parameter("evaluate2_bin_count", int,
                                                             required=True)

        data_source_step = p.create_step("dataSource-xflow-maxCompute",
                                         provider=ProviderAlibabaPAI,
                                         name="dataSource")

        data_source_step.set_arguments(
            execution=execution_input,
            tableName="pai_online_project.wumai_data",
        )

        type_transform_step = p.create_step("type-transform-xflow-maxCompute",
                                            provider=ProviderAlibabaPAI,
                                            name="typeTransform")
        type_transform_step.set_arguments(
            inputArtifact=data_source_step.outputs["outputArtifact"],
            execution=execution_input,
            outputTable="type-transform-xflow-maxCompute",
            cols_to_double=cols_to_double_input,
        )

        histogram_step = p.create_step("histogram-xflow-maxCompute",
                                       provider=ProviderAlibabaPAI,
                                       name="histogram")
        histogram_step.set_arguments(
            inputArtifact=type_transform_step.outputs["outputArtifact"],
            execution=execution_input,
            outputTableName="pai_temp_172808_1779985_1",
            selectedColNames=hist_cols_input,
        )

        sql_step = p.create_step("sql-xflow-maxCompute",
                                 provider=ProviderAlibabaPAI,
                                 name="sql")
        sql_step.set_arguments(
            inputArtifact1=type_transform_step.outputs["outputArtifact"],
            execution=execution_input,
            outputTable="pai_temp_83935_1099579_1",
            sql=sql_input,
        )

        fe_meta_runner_step = p.create_step("fe-meta-runner-xflow-maxCompute",
                                            provider=ProviderAlibabaPAI,
                                            name="feMetaRunner")

        fe_meta_runner_step.set_arguments(
            inputArtifact=sql_step.outputs["outputArtifact"],
            execution=execution_input,
            outputTable="pai_temp_83935_1099581_1",
            mapTable="pai_temp_83935_1099581_2",
            selectedCols="pm10,so2,co,no2",
            labelCol="_c2",
        )

        normalized_step = p.create_step("normalize-xflow-maxCompute",
                                        provider=ProviderAlibabaPAI,
                                        name="normalize")
        normalized_step.set_arguments(
            inputArtifact=sql_step.outputs["outputArtifact"],
            execution=execution_input,
            outputTableName="pai_temp_83935_1099582_1",
            outputParaTableName="pai_temp_83935_1099582_2",
            selectedColNames=normalize_cols_input,
        )

        split_step = p.create_step("split-xflow-maxCompute",
                                   provider=ProviderAlibabaPAI,
                                   name="split")
        split_step.set_arguments(
            inputArtifact=normalized_step.outputs["outputArtifact"],
            execution=execution_input,
            output1TableName="pai_temp_83935_1099583_1",
            fraction=fraction_input,
            output2TableName="pai_temp_83935_1199583_1",
        )

        randomforest_step = p.create_step("randomforests-xflow-maxCompute",
                                          provider=ProviderAlibabaPAI,
                                          name="randomforests")
        randomforest_step.set_arguments(
            inputArtifact=split_step.outputs["outputArtifact1"],
            execution=execution_input,
            featureColNames=randomforest_feature_cols_input,
            labelColName=randomforest_label_col_input,
            treeNum=100,
            modelName="xlab_m_random_forests_1099584_v0",
        )

        prediction1_step = p.create_step("prediction-xflow-maxCompute",
                                         provider=ProviderAlibabaPAI,
                                         name="prediction1")
        prediction1_step.set_arguments(
            inputModelArtifact=randomforest_step.outputs["outputArtifact"],
            inputDataSetArtifact=split_step.outputs["outputArtifact2"],
            execution=execution_input,
            outputTableName="pai_temp_83935_1029583_1",
            featureColNames=prediction1_feature_col_input,
            appendColNames=prediction1_append_col_input,
            resultColName=prediction1_result_col_input,
            scoreColName=prediction1_score_col_input,
            detailColName=prediction1_detail_col_input,
        )
        evaluate1_step = p.create_step("evaluate-xflow-maxCompute",
                                       provider=ProviderAlibabaPAI,
                                       name="evaluate1")
        evaluate1_step.set_arguments(
            inputArtifact=prediction1_step.outputs["outputArtifact"],
            execution=execution_input,
            outputDetailTableName="pai_temp_83935_1099586_1",
            outputMetricTableName="pai_temp_83935_1228529_1",
            outputELDetailTableName="pai_temp_83935_1299589_1",
            labelColName=evaluate1_label_col_input,
            scoreColName=evaluate1_score_col_input,
            positiveLabel=evaluate1_positive_label_input,
            binCount=evaluate1_bin_count_input,
        )
        logistic_step = p.create_step("logisticregression-binary-xflow-maxCompute",
                                      provider=ProviderAlibabaPAI,
                                      name="logisticregression")

        logistic_step.set_arguments(
            inputArtifact=split_step.outputs["outputArtifact1"],
            execution=execution_input,
            modelName="xlab_m_logisticregres_1099587_v0",
            featureColNames=logistic_feature_col_input,
            labelColName=logistic_label_col_names,
            goodValue=logistic_good_value_input,
        )

        prediction2_step = p.create_step("prediction-xflow-maxCompute",
                                         provider=ProviderAlibabaPAI,
                                         name="prediction2")
        prediction2_step.set_arguments(
            inputModelArtifact=logistic_step.outputs["outputArtifact"],
            inputDataSetArtifact=split_step.outputs["outputArtifact2"],
            execution=execution_input,
            outputTableName="pai_temp_83935_1099588_1",
            featureColNames=prediction2_feature_col_input,
            appendColNames=prediction2_append_col_input,
            resultColName=prediction2_result_col_input,
            scoreColName=prediction2_score_col_input,
            detailColName=prediction2_detail_col_input,
        )

        evaluate2_step = p.create_step("evaluate-xflow-maxCompute",
                                       provider=ProviderAlibabaPAI,
                                       name="evaluate2")
        evaluate2_step.set_arguments(
            inputArtifact=prediction2_step.outputs["outputArtifact"],
            execution=execution_input,
            outputDetailTableName="pai_temp_83935_1099589_1",
            outputMetricTableName="pai_temp_83935_1428529_1",
            outputELDetailTableName="pai_temp_83935_1199589_1",
            labelColName=evaluate2_label_col_input,
            scoreColName=evaluate2_score_col_input,
            positiveLabel=evaluate2_positive_label_input,
            binCount=evaluate2_bin_count_input,
        )

        p.create_output_artifact("predictionResult",
                                 from_=evaluate2_step.outputs["outputDetailArtifact"])
        return p

    def create_cycle_pipeline(self):
        p = Pipeline.new_pipeline(identifier="unittest_cycle_case_1", version="v1.0.0",
                                  session=self.session)
        execution_input = p.create_input_parameter("execution", "map", required=True)
        cols_to_double_input = p.create_input_parameter("cols_to_double", str, required=True)
        data_source_step = p.create_step("dataSource-xflow-maxCompute",
                                         provider=ProviderAlibabaPAI,
                                         name="dataSource")
        data_source_step.set_arguments(
            execution=execution_input,
            tableName="pai_online_project.wumai_data",
        )

        type_transform_step = p.create_step("type-transform-xflow-maxCompute",
                                            provider=ProviderAlibabaPAI,
                                            name="typeTransform")
        type_transform_step.set_arguments(
            inputArtifact=data_source_step.outputs["outputArtifact"],
            execution=execution_input,
            outputTable="type-transform-xflow-maxCompute",
            cols_to_double=cols_to_double_input,
        )

        data_source_step.after(type_transform_step)

    @staticmethod
    def args_for_composite_pipeline_1():
        arguments = {"parameters": [
            {
                "name": "execution",
                "value": {
                    "odpsInfoFile": "/share/base/odpsInfo.ini",
                    "endpoint": "http://service.cn-shanghai.maxcompute.aliyun.com/api",
                    "logViewHost": "http://logview.odps.aliyun.com",
                    "odpsProject": "wyl_test",
                },
            },
            {
                "name": "cols_to_double",
                "value": "time,hour,pm2,pm10,so2,co,no2"
            },
            {
                "name": "table_name",
                "value": "pai_online_project.wumai_data",
            }]
        }
        env = None
        return arguments, env

    def create_composite_pipeline_case_1(self, version=None):
        """Composite data_source and type_transform pipeline"""

        if version is None:
            version = "v%s" % (str(int(time.time() * 1000)))
        p = Pipeline.new_pipeline(identifier="pysdk-test-data-source-type-transform",
                                  version=version,
                                  session=self.session)

        execution_input = p.create_input_parameter("execution", "map", required=True)
        cols_to_double_input = p.create_input_parameter("cols_to_double", str, required=True)
        input_table_name = p.create_input_parameter("table_name", str, required=True)

        data_source_step = p.create_step("dataSource-xflow-maxCompute",
                                         provider=ProviderAlibabaPAI,
                                         version="v1", name="dataSource")
        data_source_step.set_arguments(
            execution=execution_input,
            tableName=input_table_name,
        )

        type_transform_step = p.create_step("type-transform-xflow-maxCompute",
                                            provider=ProviderAlibabaPAI,
                                            version="v1", name="typeTransform")
        type_transform_step.set_arguments(
            inputArtifact=data_source_step.outputs["outputArtifact"],
            execution=execution_input,
            outputTable="pai_temp_181827919_818182838",
            cols_to_double=cols_to_double_input,
        )

        p.create_output_artifact("transformedArtifact",
                                 type_transform_step.outputs["outputArtifact"])
        return p

    def create_general_input_pipeline(self):
        p = Pipeline.new_pipeline("test_algo_build", version="1.0.0", session=self.session)

        dataset_input = p.create_input_artifact("dataset", data_type=ArtifactDataType.DataSet,
                                                location_type=ArtifactLocationType.MaxComputeTable,
                                                required=True)

        label_dataset_input = p.create_input_artifact(
            "label_data_set", data_type=ArtifactDataType.DataSet,
            location_type=ArtifactLocationType.MaxComputeTable, required=True)

        execution_input = p.create_input_parameter("execution", "map", required=True)
        model_name_input = p.create_input_parameter("model_name", str, required=True)
        feature_cols_input = p.create_input_parameter("feature_cols", str, required=True)
        label_col_input = p.create_input_parameter("label_col", str, required=True)
        user_project_input = p.create_input_parameter("user_project", str, required=True)

        pred_feature_col_input = p.create_input_parameter("prediction_feature_col_names", str,
                                                          required=True)
        pred_append_col_input = p.create_input_parameter("prediction_append_col_names", str,
                                                         required=True)
        pred_result_col_input = p.create_input_parameter("prediction_result_col_names", str,
                                                         required=True)
        pred_score_col_input = p.create_input_parameter("prediction_score_col_names", str,
                                                        required=True)
        pred_detail_col_input = p.create_input_parameter("prediction_detail_col_names", str,
                                                         required=True)
        pred_output_table_input = p.create_input_parameter("prediction_output_table", str,
                                                           required=True)

        eval_label_col_input = p.create_input_parameter("evaluate_label_col_name", str,
                                                        required=True)
        eval_score_col_input = p.create_input_parameter("evaluate_score_col_name", str,
                                                        required=True)
        eval_positive_label_input = p.create_input_parameter("evaluate_positive_label", int,
                                                             required=True)
        eval_bin_count_input = p.create_input_parameter("evaluate_bin_count", int, required=True)
        eval_output_detail_table_input = p.create_input_parameter("evaluate_output_detail_table",
                                                                  str, required=True)
        eval_output_metric_table_input = p.create_input_parameter("evaluate_output_metrics_table",
                                                                  str, required=True)
        eval_output_el_detail_table_input = p.create_input_parameter(
            "evaluate_output_el_detail_table", str,
            required=True)
        # set default input for step with some common parameter.
        p.set_step_input("execution", execution_input)
        # __userProject maybe remove from XFlow based manifest pipeline in future.
        p.set_step_input("__userProject", user_project_input)
        # user default value that could not be assign from pipeline arguments
        # p.set_step_input("__userProject", self.session.odps_project)
        p.set_step_input("__generatePMML", True)

        lr_step = p.create_step_from_manifest(
            LogisticRegression(session=self.session).get_pipeline_definition(),
            name="logistics_regression")
        lr_step.set_arguments(
            inputArtifact=dataset_input,
            modelName=model_name_input,
            featureColNames=feature_cols_input,
            labelColName=label_col_input,
        )

        prediction_step = p.create_step("prediction-xflow-maxCompute",
                                        provider=ProviderAlibabaPAI,
                                        name="prediction")
        prediction_step.set_arguments(
            inputModelArtifact=lr_step.outputs["outputArtifact"],
            inputDataSetArtifact=label_dataset_input,
            outputTableName=pred_output_table_input,
            featureColNames=pred_feature_col_input,
            appendColNames=pred_append_col_input,
            resultColName=pred_result_col_input,
            scoreColName=pred_score_col_input,
            detailColName=pred_detail_col_input,
        )

        evaluate_step = p.create_step("evaluate-xflow-maxCompute",
                                      provider=ProviderAlibabaPAI,
                                      name="evaluate")
        evaluate_step.set_arguments(
            inputArtifact=prediction_step.outputs["outputArtifact"],
            outputDetailTableName=eval_output_detail_table_input,
            outputMetricTableName=eval_output_metric_table_input,
            outputELDetailTableName=eval_output_el_detail_table_input,
            labelColName=eval_label_col_input,
            scoreColName=eval_score_col_input,
            positiveLabel=eval_positive_label_input,
            binCount=eval_bin_count_input,
        )

        p.create_output_artifact("predictionResult",
                                 from_=evaluate_step.outputs["outputDetailArtifact"])
        return p

    def test_nested_pipeline(self):
        # base pipeline: receiver str parameter, output data set artifact.

        def create_base_pipeline():
            version = "v%s" % (str(int(time.time() * 1000)))

            p = Pipeline.new_pipeline(
                identifier="test-nested-pipeline-base",
                version=version,
                session=self.session,
            )
            xflow_execution_input = p.create_input_parameter("xflow_execution",
                                                             typ=ParameterType.Map,
                                                             required=True)

            data_source_step = p.create_step("dataSource-xflow-maxCompute",
                                             provider=ProviderAlibabaPAI,
                                             version="v1", name="dataSource")

            data_source_step.set_arguments(
                execution=xflow_execution_input,
                tableName="pai_online_project.wumai_data",
            )
            type_transform_step = p.create_step("type-transform-xflow-maxCompute",
                                                provider=ProviderAlibabaPAI,
                                                name="typeTransform")
            type_transform_step.set_arguments(
                inputArtifact=data_source_step.outputs["outputArtifact"],
                execution=xflow_execution_input,
                outputTable="pai_temp_172808_1779985_100",
                cols_to_double="time,hour,pm2,pm10,so2,co,no2",
            )

            sql_step = p.create_step("sql-xflow-maxCompute",
                                     provider=ProviderAlibabaPAI,
                                     name="sql")
            sql_step.set_arguments(
                inputArtifact1=type_transform_step.outputs["outputArtifact"],
                execution=xflow_execution_input,
                outputTable="pai_temp_83935_1099579_1",
                sql='select time,hour,(case when pm2>200 then 1 else 0 end),pm10,so2,co,no2'
                    ' from pai_temp_172808_1779985_100',
            )

            normalized_step = p.create_step("normalize-xflow-maxCompute",
                                            provider=ProviderAlibabaPAI,
                                            name="normalize")
            normalized_step.set_arguments(
                inputArtifact=sql_step.outputs["outputArtifact"],
                execution=xflow_execution_input,
                outputTableName="pai_temp_83935_1099582_1",
                outputParaTableName="pai_temp_83935_1099582_2",
                selectedColNames="pm10,so2,co,no2",
            )

            p.create_output_artifact("outputArtifact",
                                     from_=normalized_step.outputs["outputArtifact"])
            return p

        base_pipeline = create_base_pipeline()
        pipeline_id = self.session.create_pipeline(base_pipeline.to_dict())
        self.assertIsNotNone(pipeline_id)

        prev_pipeline = base_pipeline
        for idx in range(1, 10):
            version = "v%s" % (str(int(time.time() * 1000)))
            p = Pipeline.new_pipeline(
                identifier="test-nest-pipeline-%s" % idx,
                version=version,
                session=self.session,
            )

            xflow_execution_input = p.create_input_parameter("xflow_execution", ParameterType.Map,
                                                             required=True)

            inner_step = p.create_step(
                identifier=prev_pipeline.identifier,
                version=prev_pipeline.version,
                provider=prev_pipeline.provider,
                name="inner-step-%s" % idx,
            )

            inner_step.set_arguments(
                xflow_execution=xflow_execution_input,
            )

            p.create_output_artifact(
                "outputArtifact", from_=inner_step.outputs["outputArtifact"]
            )
            pipeline_id = self.session.create_pipeline(p.to_dict())
            self.assertIsNotNone(pipeline_id)
            prev_pipeline = p

        run_instance = prev_pipeline.run(name="pysdk-test-nested-pipeline-run", arguments={
            "xflow_execution": {
                "odpsInfoFile": "/share/base/odpsInfo.ini",
                "endpoint": "http://service.cn-shanghai.maxcompute.aliyun.com/api",
                "logViewHost": "http://logview.odps.aliyun.com",
                "odpsProject": "pai_sdk_test",
            },
        }, wait=False)
        self.assertEqual(RunStatus.Running, run_instance.get_status())
        run_instance.wait(log_outputs=False)
        self.assertEqual(RunStatus.Succeeded, run_instance.get_status())

    def test_composite_pipeline_run(self):
        p = self.create_composite_pipeline_to_oss(self.session)
        arguments = {
            "xflow_execution": {
                "odpsInfoFile": "/share/base/odpsInfo.ini",
                "endpoint": "http://service.cn-shanghai.maxcompute.aliyun.com/api",
                "logViewHost": "http://logview.odps.aliyun.com",
                "odpsProject": "pai_sdk_test",
            },
            "rolearn": "acs:ram::1557702098194904:role/aliyunodpspaidefaultrole",
        }

        run_instance = p.run(name="pysdk-test-with-oss-model", arguments=arguments, wait=False)
        self.assertEqual(RunStatus.Running, run_instance.get_status())
        run_instance.wait(log_outputs=False)
        self.assertEqual(RunStatus.Succeeded, run_instance.get_status())

    @staticmethod
    def create_composite_pipeline_to_oss(session):
        p = Pipeline.new_pipeline(
            identifier="test-composite-lr-pipeline",
            version="v%s" % (str(int(time.time() * 1000))),
            session=session,
        )

        xflow_execution_input = p.create_input_parameter(
            "xflow_execution", ParameterType.Map, required=True,
        )

        table_input = p.create_input_parameter(
            "table_name", ParameterType.String, required=False,
            value="pai_online_project.wumai_data",
        )
        cols_to_double_input = p.create_input_parameter(
            "cols_to_double", ParameterType.String, required=False,
            value="time,hour,pm2,pm10,so2,co,no2",
        )
        sql_input = p.create_input_parameter(
            "sql", ParameterType.String, required=False,
            value="select time,hour,(case when pm2>200 then 1 else 0 end),pm10,so2,co,no2"
                  " from pai_temp_172808_1779985_100",
        )
        normalize_cols_input = p.create_input_parameter(
            "normalize_selected_col_names", ParameterType.String,
            required=False,
            value="pm10,so2,co,no2",
        )

        fraction_input = p.create_input_parameter(
            "fraction", ParameterType.Double, required=False,
            value=0.8)

        logistic_feature_col_input = p.create_input_parameter(
            "logisticregression_feature_col_names", ParameterType.String,
            required=False,
            value='pm10,so2,co,no2')

        logistic_label_col_names = p.create_input_parameter(
            "logisticregression_label_col_names", ParameterType.String,
            required=False,
            value="_c2")
        logistic_good_value_input = p.create_input_parameter(
            "logisticregression_good_value", ParameterType.Integer,
            required=False,
            value=1)

        prediction_feature_col_input = p.create_input_parameter(
            "prediction_feature_col_names", ParameterType.String, required=False,
            value="pm10,so2,co,no2",
        )
        prediction_append_col_input = p.create_input_parameter(
            "prediction_append_col_names", ParameterType.String, required=False,
            value="time,hour,_c2,pm10,so2,co,no2")
        prediction_result_col_input = p.create_input_parameter(
            "prediction_result_col_names", ParameterType.String, required=False,
            value="prediction_result")
        prediction_score_col_input = p.create_input_parameter(
            "prediction_score_col_names", ParameterType.String, required=False,
            value="prediction_score")
        prediction_detail_col_input = p.create_input_parameter(
            "prediction_detail_col_names", ParameterType.String, required=False,
            value="prediction_detail")

        evaluate_label_col_input = p.create_input_parameter(
            "evaluate_label_col_name", ParameterType.String, required=False,
            value="_c2")
        evaluate_score_col_input = p.create_input_parameter(
            "evaluate_score_col_name", ParameterType.String, required=False,
            value="prediction_score")
        evaluate_positive_label_input = p.create_input_parameter(
            "evaluate_positive_label", ParameterType.Integer, required=False,
            value=1)
        evaluate_bin_count_input = p.create_input_parameter(
            "evaluate2_bin_count", ParameterType.Integer, required=False,
            value=1000)

        oss_bucket_input = p.create_input_parameter(
            "oss_bucket", ParameterType.String, required=False,
            value="dataplus-pai-test",
        )

        oss_endpoint_input = p.create_input_parameter(
            "oss_endpoint", ParameterType.String, required=False,
            value="oss-cn-shanghai.aliyuncs.com",
        )
        oss_key_input = p.create_input_parameter(
            "oss_key", ParameterType.String, required=False,
            value="/paiflow/model_transfer2oss_test/",
        )
        rolearn_input = p.create_input_parameter(
            "rolearn", ParameterType.String, required=True
        )

        data_source_step = p.create_step("dataSource-xflow-maxCompute",
                                         provider=ProviderAlibabaPAI,
                                         version="v1", name="dataSource")

        data_source_step.set_arguments(
            execution=xflow_execution_input,
            tableName=table_input
        )

        type_transform_step = p.create_step("type-transform-xflow-maxCompute",
                                            provider=ProviderAlibabaPAI,
                                            name="typeTransform")
        type_transform_step.set_arguments(
            inputArtifact=data_source_step.outputs["outputArtifact"],
            execution=xflow_execution_input,
            outputTable="pai_temp_172808_1779985_100",
            cols_to_double=cols_to_double_input,
        )

        sql_step = p.create_step("sql-xflow-maxCompute",
                                 provider=ProviderAlibabaPAI,
                                 name="sql")
        sql_step.set_arguments(
            inputArtifact1=type_transform_step.outputs["outputArtifact"],
            execution=xflow_execution_input,
            outputTable="pai_temp_83935_1099579_1",
            sql=sql_input,
        )

        normalized_step = p.create_step("normalize-xflow-maxCompute",
                                        provider=ProviderAlibabaPAI,
                                        name="normalize")
        normalized_step.set_arguments(
            inputArtifact=sql_step.outputs["outputArtifact"],
            execution=xflow_execution_input,
            outputTableName="pai_temp_83935_1099582_1",
            outputParaTableName="pai_temp_83935_1099582_2",
            selectedColNames=normalize_cols_input,
        )

        split_step = p.create_step("split-xflow-maxCompute",
                                   provider=ProviderAlibabaPAI,
                                   name="split")
        split_step.set_arguments(
            inputArtifact=normalized_step.outputs["outputArtifact"],
            execution=xflow_execution_input,
            output1TableName="pai_temp_83935_1099583_1",
            fraction=fraction_input,
            output2TableName="pai_temp_83935_1199583_1",
        )

        logistic_step = p.create_step("logisticregression-binary-xflow-maxCompute",
                                      provider=ProviderAlibabaPAI,
                                      name="logisticregression")

        logistic_step.set_arguments(
            inputArtifact=split_step.outputs["outputArtifact1"],
            execution=xflow_execution_input,
            modelName="xlab_m_logisticregres_1099587_v0",
            featureColNames=logistic_feature_col_input,
            labelColName=logistic_label_col_names,
            goodValue=logistic_good_value_input,
        )

        prediction2_step = p.create_step("prediction-xflow-maxCompute",
                                         provider=ProviderAlibabaPAI,
                                         name="prediction2")
        prediction2_step.set_arguments(
            inputModelArtifact=logistic_step.outputs["outputArtifact"],
            inputDataSetArtifact=split_step.outputs["outputArtifact2"],
            execution=xflow_execution_input,
            outputTableName="pai_temp_83935_1099588_1",
            featureColNames=prediction_feature_col_input,
            appendColNames=prediction_append_col_input,
            resultColName=prediction_result_col_input,
            scoreColName=prediction_score_col_input,
            detailColName=prediction_detail_col_input,
        )

        evaluate2_step = p.create_step("evaluate-xflow-maxCompute",
                                       provider=ProviderAlibabaPAI,
                                       name="evaluate2")
        evaluate2_step.set_arguments(
            inputArtifact=prediction2_step.outputs["outputArtifact"],
            execution=xflow_execution_input,
            outputDetailTableName="pai_temp_83935_1099589_1",
            outputMetricTableName="pai_temp_83935_1428529_1",
            outputELDetailTableName="pai_temp_83935_1199589_1",
            labelColName=evaluate_label_col_input,
            scoreColName=evaluate_score_col_input,
            positiveLabel=evaluate_positive_label_input,
            binCount=evaluate_bin_count_input,
        )

        modeltransfer2oss_step = p.create_step(
            "modeltransfer2oss-xflow-maxCompute",
            provider=ProviderAlibabaPAI,
            version="v1",
            name="model-transfer2oss"
        )

        modeltransfer2oss_step.set_arguments(
            execution=xflow_execution_input,
            inputArtifact=logistic_step.outputs["outputArtifact"],
            bucket=oss_bucket_input,
            endpoint=oss_endpoint_input,
            path=oss_key_input,
            rolearn=rolearn_input
        )

        p.create_output_artifact("offlineModel", from_=logistic_step.outputs["outputArtifact"])
        p.create_output_artifact("pmmlModel",
                                 from_=modeltransfer2oss_step.outputs["outputArtifact"])
        p.create_output_artifact("predictionResult",
                                 from_=evaluate2_step.outputs["outputDetailArtifact"])
        return p

    @staticmethod
    def create_composite_with_default(session):
        p = Pipeline.new_pipeline(
            identifier="test_composite_lr_pipeline",
            version="v%s" % (str(int(time.time() * 1000))),
            session=session,
        )

        xflow_execution_input = p.create_input_parameter(
            "xflow_execution", ParameterType.Map, required=True,
        )

        data_source_step = p.create_step("dataSource-xflow-maxCompute",
                                         provider=ProviderAlibabaPAI,
                                         version="v1", name="dataSource")

        data_source_step.set_arguments(
            execution=xflow_execution_input,
            tableName="pai_online_project.wumai_data",
        )

        type_transform_step = p.create_step("type-transform-xflow-maxCompute",
                                            provider=ProviderAlibabaPAI,
                                            name="typeTransform")
        type_transform_step.set_arguments(
            inputArtifact=data_source_step.outputs["outputArtifact"],
            execution=xflow_execution_input,
            outputTable="pai_temp_172808_1779985_100",
            cols_to_double="time,hour,pm2,pm10,so2,co,no2",
        )

        sql_step = p.create_step("sql-xflow-maxCompute",
                                 provider=ProviderAlibabaPAI,
                                 name="sql")
        sql_step.set_arguments(
            inputArtifact1=type_transform_step.outputs["outputArtifact"],
            execution=xflow_execution_input,
            outputTable="pai_temp_83935_1099579_1",
            sql="select time,hour,(case when pm2>200 then 1 else 0 end),pm10,so2,co,no2"
                " from pai_temp_83935_1099578_1",
        )

        normalized_step = p.create_step("normalize-xflow-maxCompute",
                                        provider=ProviderAlibabaPAI,
                                        name="normalize")
        normalized_step.set_arguments(
            inputArtifact=sql_step.outputs["outputArtifact"],
            execution=xflow_execution_input,
            outputTableName="pai_temp_83935_1099582_1",
            outputParaTableName="pai_temp_83935_1099582_2",
            selectedColNames="pm10,so2,co,no2",
        )

        split_step = p.create_step("split-xflow-maxCompute",
                                   provider=ProviderAlibabaPAI,
                                   name="split")
        split_step.set_arguments(
            inputArtifact=normalized_step.outputs["outputArtifact"],
            execution=xflow_execution_input,
            output1TableName="pai_temp_83935_1099583_1",
            fraction=0.8,
            output2TableName="pai_temp_83935_1199583_1",
        )

        logistic_step = p.create_step("logisticregression-binary-xflow-maxCompute",
                                      provider=ProviderAlibabaPAI,
                                      name="logisticregression")

        logistic_step.set_arguments(
            inputArtifact=split_step.outputs["outputArtifact1"],
            execution=xflow_execution_input,
            modelName="xlab_m_logisticregres_1099587_v0",
            featureColNames='pm10,so2,co,no2',
            labelColName="_c2",
            goodValue=1,
        )

        prediction2_step = p.create_step("prediction-xflow-maxCompute",
                                         provider=ProviderAlibabaPAI,
                                         name="prediction2")
        prediction2_step.set_arguments(
            inputModelArtifact=logistic_step.outputs["outputArtifact"],
            inputDataSetArtifact=split_step.outputs["outputArtifact2"],
            execution=xflow_execution_input,
            outputTableName="pai_temp_83935_1099588_1",
            featureColNames="pm10,so2,co,no2",
            appendColNames="time,hour,_c2,pm10,so2,co,no2",
            resultColName="prediction_result",
            scoreColName="prediction_score",
            detailColName="prediction_detail",
        )

        evaluate2_step = p.create_step("evaluate-xflow-maxCompute",
                                       provider=ProviderAlibabaPAI,
                                       name="evaluate2")
        evaluate2_step.set_arguments(
            inputArtifact=prediction2_step.outputs["outputArtifact"],
            execution=xflow_execution_input,
            outputDetailTableName="pai_temp_83935_1099589_1",
            outputMetricTableName="pai_temp_83935_1428529_1",
            outputELDetailTableName="pai_temp_83935_1199589_1",
            labelColName="_c2",
            scoreColName="prediction_score",
            positiveLabel=1,
            binCount=1000,
        )

        p.create_output_artifact("lrModel", from_=logistic_step.outputs["outputArtifact"])
        p.create_output_artifact("predictionResult",
                                 from_=evaluate2_step.outputs["outputDetailArtifact"])
        return p


if __name__ == "__main__":
    unittest.main()
