from __future__ import absolute_import

import os
import time
import unittest

import yaml

from pai.pipeline import Pipeline, PipelineStep
from pai.pipeline.artifact import ArtifactDataType, ArtifactLocationType
from pai.pipeline.run import RunInstance, RunStatus
from pai.xflow.classifier import LogisticRegression
from test import BaseTestCase
from test.pipeline import load_local_yaml

_current_dir = os.path.dirname(os.path.abspath(__file__))


class TestPipeline(BaseTestCase):

    def setUp(self):
        super(TestPipeline, self).setUp()
        self.maxDiff = None

    @unittest.skip
    def test_forest_pipeline_create(self):
        with self.assertRaises(ValueError):
            _ = self.create_forest_pipeline()

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

    @staticmethod
    def add_local_pipeline_step(pipeline, identifier, name=None):
        manifest = load_local_yaml("%s.yaml" % identifier)
        name = name if name else identifier
        step = PipelineStep.create_from_manifest(manifest, pipeline, name=name)
        pipeline.steps[step.name] = step
        return step

    def create_forest_pipeline(self):
        p = Pipeline.new_pipeline(identifier="ut-randomforest", version="v0.1.0",
                                  session=self.session)

        execution_input = p.create_input_parameter("__execution", 'map')
        feature_col_names_input = p.create_input_parameter("featureColNames", str)
        model_name_input = p.create_input_parameter("modelName", str, value="test_randomforest",
                                                    required=True)

        output_detail_table_1_input = p.create_input_parameter("outputDetailTableName1", str,
                                                               required=True)
        output_detail_table_2_input = p.create_input_parameter("outputDetailTableName2", str,
                                                               required=True)
        output_metric_table_1_input = p.create_input_parameter("outputMetricTableName1", str,
                                                               required=True)
        output_metric_table_2_input = p.create_input_parameter("outputMetricTableName2", str,
                                                               required=True)
        output_table_input = p.create_input_parameter("outputTableName", str, required=True)

        input_artifact1 = p.create_input_artifact(
            "inputArtifact", data_type=ArtifactDataType.DataSet,
            location_type=ArtifactLocationType.MaxComputeTable, required=True)
        input_artifact2 = p.create_input_artifact(
            "inputArtifact2", data_type=ArtifactDataType.DataSet,
            location_type=ArtifactLocationType.MaxComputeTable, required=True)

        randomforest_step = p.create_step("randomforests-xflow-ODPS", name="randomforests")
        randomforest_step.set_arguments(
            inputArtifact=input_artifact1,
            __execution=execution_input,
            featureColNames=feature_col_names_input,
            modelName=model_name_input,
            labelColName="_c2",
            treeNum=100,
            __generatePMML=True,
            __pmmlModelPublicProject="pai_online_project",
            __pmmlModelPublicEndpoint="http://service.cn-shanghai.maxcompute.aliyun.com/api",
            __pmmlModelVolume="pai_model_1557702098194904",
            __pmmlModelPartition="partition_1099584",
        )

        prediction_step1 = p.create_step("prediction-evaluate", name="prediction1")

        prediction_step1.set_arguments(
            __execution=execution_input,
            outputTableName=output_table_input,
            outputDetailTableName=output_detail_table_1_input,
            outputMetricTableName=output_metric_table_1_input,
            outputDetailTableName2=output_detail_table_2_input,
            outputMetricTableName2=output_metric_table_2_input,
            outputELDetailTableName="pai_temp_83935_1299589_1",
            outputELDetailTableName2="pai_temp_83935_1399589_1",
            inputModelArtifact=randomforest_step.outputs["outputArtifact"],
            inputDataSetArtifact=input_artifact2,
        )

        prediction_step2 = p.create_step("prediction-evaluate", name="prediction")
        prediction_step2.set_arguments(
            __execution=execution_input,
            outputDetailTableName2="pai_temp_183935_1099586_1",
            outputMetricTableName2="pai_temp_183935_1228529_1",
            outputDetailTableName="pai_temp_183935_1099586_2",
            outputMetricTableName="pai_temp_183935_1228529_2",
            outputTableName="pai_temp_183935_1029583_1",
            outputELDetailTableName="pai_temp_83935_1299589_2",
            outputELDetailTableName2="pai_temp_83935_1399589_2",
            inputModelArtifact=randomforest_step.outputs["outputArtifact"],
            inputDataSetArtifact=input_artifact2,
        )

        p.create_output_artifact("predictionResult",
                                 from_=prediction_step1.outputs["predictionResult"])
        p.create_output_artifact("predictionResult2",
                                 from_=prediction_step2.outputs["predictionResult"])
        return p

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
        evaluate1_positive_label_input = p.create_input_parameter("evaluate1_positive_label", str,
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
        evaluate2_positive_label_input = p.create_input_parameter("evaluate2_positive_label", str,
                                                                  required=True)
        evaluate2_bin_count_input = p.create_input_parameter("evaluate2_bin_count", int,
                                                             required=True)

        data_source_step = p.create_step("odps-data-source", name="dataSource")

        data_source_step.set_arguments(
            __execution=execution_input,
            tableName="pai_online_project.wumai_data",
        )

        type_transform_step = p.create_step("type-transform-xflow-ODPS", name="typeTransform")
        type_transform_step.set_arguments(
            inputArtifact=data_source_step.outputs["outputArtifact"],
            __execution=execution_input,
            outputTable="type-transform-xflow-ODPS",
            cols_to_double=cols_to_double_input,
        )

        histogram_step = p.create_step("histogram-xflow-ODPS", name="histogram")
        histogram_step.set_arguments(
            inputArtifact=type_transform_step.outputs["outputArtifact"],
            __execution=execution_input,
            outputTableName="pai_temp_172808_1779985_1",
            selectedColNames=hist_cols_input,
        )

        sql_step = p.create_step("sql-xflow-ODPS", name="sql")
        sql_step.set_arguments(
            inputArtifact1=type_transform_step.outputs["outputArtifact"],
            __execution=execution_input,
            outputTable="pai_temp_83935_1099579_1",
            sql=sql_input,
        )

        fe_meta_runner_step = p.create_step("fe-meta-runner-xflow-ODPS", name="feMetaRunner")

        fe_meta_runner_step.set_arguments(
            inputArtifact=sql_step.outputs["outputArtifact"],
            __execution=execution_input,
            outputTable="pai_temp_83935_1099581_1",
            mapTable="pai_temp_83935_1099581_2",
            selectedCols="pm10,so2,co,no2",
            labelCol="_c2",
        )

        normalized_step = p.create_step("normalize-xflow-ODPS", name="normalize")
        normalized_step.set_arguments(
            inputArtifact=sql_step.outputs["outputArtifact"],
            __execution=execution_input,
            outputTableName="pai_temp_83935_1099582_1",
            outputParaTableName="pai_temp_83935_1099582_2",
            selectedColNames=normalize_cols_input,
        )

        split_step = p.create_step("split-xflow-ODPS", name="split")
        split_step.set_arguments(
            inputArtifact=normalized_step.outputs["outputArtifact"],
            __execution=execution_input,
            output1TableName="pai_temp_83935_1099583_1",
            fraction=fraction_input,
            output2TableName="pai_temp_83935_1199583_1",
        )

        randomforest_step = p.create_step("randomforests-xflow-ODPS", name="randomforests")
        randomforest_step.set_arguments(
            inputArtifact=split_step.outputs["outputArtifact1"],
            __execution=execution_input,
            featureColNames=randomforest_feature_cols_input,
            labelColName=randomforest_label_col_input,
            treeNum=100,
            modelName="xlab_m_random_forests_1099584_v0",
            __generatePMML=True,
            __pmmlModelPublicProject="pai_online_project",
            __pmmlModelPublicEndpoint="http://service.cn-shanghai.maxcompute.aliyun.com/api",
            __pmmlModelVolume="pai_model_1557702098194904",
            __pmmlModelPartition="partition_1099584",
        )

        prediction1_step = p.create_step("prediction-xflow-ODPS", name="prediction1")
        prediction1_step.set_arguments(
            inputModelArtifact=randomforest_step.outputs["outputArtifact"],
            inputDataSetArtifact=split_step.outputs["outputArtifact2"],
            __execution=execution_input,
            outputTableName="pai_temp_83935_1029583_1",
            featureColNames=prediction1_feature_col_input,
            appendColNames=prediction1_append_col_input,
            resultColName=prediction1_result_col_input,
            scoreColName=prediction1_score_col_input,
            detailColName=prediction1_detail_col_input,
        )
        evaluate1_step = p.create_step("evaluate-xflow-ODPS", name="evaluate1")
        evaluate1_step.set_arguments(
            inputArtifact=prediction1_step.outputs["outputArtifact"],
            __execution=execution_input,
            outputDetailTableName="pai_temp_83935_1099586_1",
            outputMetricTableName="pai_temp_83935_1228529_1",
            outputELDetailTableName="pai_temp_83935_1299589_1",
            labelColName=evaluate1_label_col_input,
            scoreColName=evaluate1_score_col_input,
            positiveLabel=evaluate1_positive_label_input,
            binCount=evaluate1_bin_count_input,
        )
        logistic_step = p.create_step("logisticregression-binary-xflow-ODPS",
                                      name="logisticregression")

        logistic_step.set_arguments(
            inputArtifact=split_step.outputs["outputArtifact1"],
            __execution=execution_input,
            modelName="xlab_m_logisticregres_1099587_v0",
            featureColNames=logistic_feature_col_input,
            labelColName=logistic_label_col_names,
            goodValue=logistic_good_value_input,
            __generatePMML=True,
            __pmmlModelPublicProject="pai_online_project",
            __pmmlModelPublicEndpoint="http://service.cn-shanghai.maxcompute.aliyun.com/api",
            __pmmlModelVolume="pai_model_1557702098194904",
            __pmmlModelPartition="partition_1099587",
        )

        prediction2_step = p.create_step("prediction-xflow-ODPS", name="prediction2")
        prediction2_step.set_arguments(
            inputModelArtifact=logistic_step.outputs["outputArtifact"],
            inputDataSetArtifact=split_step.outputs["outputArtifact2"],
            __execution=execution_input,
            outputTableName="pai_temp_83935_1099588_1",
            featureColNames=prediction2_feature_col_input,
            appendColNames=prediction2_append_col_input,
            resultColName=prediction2_result_col_input,
            scoreColName=prediction2_score_col_input,
            detailColName=prediction2_detail_col_input,
        )

        evaluate2_step = p.create_step("evaluate-xflow-ODPS", name="evaluate2")
        evaluate2_step.set_arguments(
            inputArtifact=prediction2_step.outputs["outputArtifact"],
            __execution=execution_input,
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
        execution_input = p.create_input_parameter("__execution", "map", required=True)
        cols_to_double_input = p.create_input_parameter("cols_to_double", str, required=True)

        data_source_step = p.create_step("odps-data-source", name="dataSource")
        data_source_step.set_arguments(
            __execution=execution_input,
            tableName="pai_online_project.wumai_data",
        )

        type_transform_step = p.create_step("type-transform-xflow-ODPS", name="typeTransform")
        type_transform_step.set_arguments(
            inputArtifact=data_source_step.outputs["outputArtifact"],
            __execution=execution_input,
            outputTable="type-transform-xflow-ODPS",
            cols_to_double=cols_to_double_input,
        )

        data_source_step.after(type_transform_step)

    @staticmethod
    def args_for_composite_pipeline_1():
        arguments = {"parameters": [
            {
                "name": "__execution",
                "value": {
                    "__odpsInfoFile": "/share/base/odpsInfo.ini",
                    "endpoint": "http://service.cn-shanghai.maxcompute.aliyun.com/api",
                    "logViewHost": "http://logview.odps.aliyun.com",
                    "odpsProject": "wyl_test",
                    "userId": 15577
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

        env = {"resource": {
            "compute": {
                "max_compute": {
                    "__odpsInfoFile": "/share/base/odpsInfo.ini",
                    "endpoint": "http://service.cn-shanghai.maxcompute.aliyun.com/api",
                    "logViewHost": "http://logview.odps.aliyun.com",
                    "odpsProject": "wyl_test",
                }
            }
        },
            # "workflowService": {
            #     "config": {
            #         "endpoint": "http://service.cn-shanghai.argo.aliyun.com"
            #     },
            #     "name": "argo"
            # }
        }
        return arguments, env

    def create_composite_pipeline_case_1(self, version=None):
        """Composite data_source and type_transform pipeline"""

        if version is None:
            version = "v%s" % (str(int(time.time() * 1000)))
        p = Pipeline.new_pipeline(identifier="ut-data-source-type-transform", version=version,
                                  session=self.session)

        execution_input = p.create_input_parameter("__execution", "map", required=True)
        cols_to_double_input = p.create_input_parameter("cols_to_double", str, required=True)
        input_table_name = p.create_input_parameter("table_name", str, required=True)

        data_source_step = p.create_step("odps-data-source", provider="1557702098194904",
                                         version="v1", name="dataSource")
        data_source_step.set_arguments(
            __execution=execution_input,
            tableName=input_table_name,
        )

        type_transform_step = p.create_step("type-transform-xflow-ODPS",
                                            provider="1557702098194904",
                                            version="v1", name="typeTransform")
        type_transform_step.set_arguments(
            inputArtifact=data_source_step.outputs["outputArtifact"],
            __execution=execution_input,
            outputTable="pai_temp_181827919_818182838",
            cols_to_double=cols_to_double_input,
        )

        p.create_output_artifact("transformedArtifact",
                                 type_transform_step.outputs["outputArtifact"])
        return p

    def test_temp_composite_pipeline_run(self):
        p = self.create_composite_pipeline_case_1()
        arguments, env = self.args_for_composite_pipeline_1()
        run_id = p.run("ut_temp_composite_pipeline_run", arguments=arguments, env=env, wait=False)
        self.assertIsNotNone(run_id)
        run = RunInstance(run_id=run_id, session=self.session)
        self.assertEqual(run.get_status(), RunStatus.Running)
        run.wait()
        self.assertEqual(run.get_status(), RunStatus.Succeeded)
        run.get_outputs()

    def test_composite_pipeline_submit(self):
        p = self.create_composite_pipeline_case_1()
        arguments, env = self.args_for_composite_pipeline_1()
        pipeline_id = self.session.create_pipeline(p.to_dict())
        run_id = self.session.create_pipeline_run("ut_composite_pipeline_run",
                                                  pipeline_id=pipeline_id,
                                                  arguments=arguments, env=env)
        self.assertIsNotNone(run_id)
        time.sleep(1)
        run_instance = RunInstance(run_id=run_id, session=self.session)
        self.assertEqual(run_instance.get_status(), RunStatus.Running)
        run_instance.wait()
        self.assertEqual(run_instance.get_status(), RunStatus.Succeeded)

    def test_general_input(self):
        p = Pipeline.new_pipeline("test_alogo_build", version="1.0.0", session=self.session)

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
        pmml_volume_input = p.create_input_parameter("pmml_volume", str, required=True)

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
        eval_positive_label_input = p.create_input_parameter("evaluate_positive_label", str,
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
        p.set_step_input("__execution", execution_input)
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
            __pmmlModelPublicProject="pai_online_project",
            __pmmlModelPublicEndpoint="http://service.cn-shanghai.maxcompute.aliyun.com/api",
            __pmmlModelVolume=pmml_volume_input,
            __pmmlModelPartition="partition_1099587",
        )

        prediction_step = p.create_step("prediction-xflow-ODPS", name="prediction")
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

        evaluate_step = p.create_step("evaluate-xflow-ODPS", name="evaluate")
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

        pipeline_def = p.to_dict()

        pipeline_executions = [param["from"] for p in pipeline_def["spec"]["pipelines"] for param in
                               p["spec"]["arguments"]["parameters"] if
                               param["name"] == "__execution"]

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


if __name__ == "__main__":
    unittest.main()
