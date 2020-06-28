from __future__ import absolute_import

import os
import unittest

from pai.pipeline import Pipeline, default_step_parameter, PipelineStep
from tests import BaseTestCase
from tests.test_paiflow import load_local_yaml

_current_dir_path = os.path.dirname(os.path.abspath(__file__))


class TestPipeline(BaseTestCase):

    def setUp(self):
        super(TestPipeline, self).setUp()

    def tearDown(self):
        super(TestPipeline, self).tearDown()

    def test_pipeline_create(self):
        pipeline = self.create_forest_pipeline()
        expected = load_local_yaml("unittest_randomforest.yaml")
        self.assertDictEqual(pipeline.to_dict(), expected)

    def test_pipeline_run(self):
        pipeline = self.create_forest_pipeline()
        run_id = pipeline.run("unitest_randomforest_run",
                              manifest=pipeline.to_dict(),
                              arguments={"parameters": {
                                  "featureColName": "hour,pm10,so2,co,no2,pm2",
                                  "modelName": "wyl_test",
                                  "outputDetailTableName1": "pai_temp_11800817_81828"
                              }},
                              env={
                                  "workflowService": {
                                      "name": "argo",
                                      "config": {
                                          "endpoint": "http://service.cn-shanghai.argo.aliyun.com/"
                                      }
                                  },
                                  "resource": {
                                      "compute": {
                                          "max_compute": {
                                              "accessId": "AccessKeyId",
                                              "accessKey": "3AccessKeySecret",
                                              "logViewHost": "http://logview.odps.aliyun.com/",
                                              "endpoint": "http://service.cn-shanghai.maxcompute.aliyun.com/api",
                                              "odpsProject": "wyl_test",
                                              "userId": 15577,
                                          }
                                      }

                                  }
                              })

    @staticmethod
    def add_local_pipeline_step(pipeline, identifier, name=None):
        manifest = load_local_yaml("%s.yaml" % identifier)
        step = PipelineStep.create_from_manifest(manifest, pipeline, name=name if name else identifier)
        pipeline.steps[step.name] = step
        return step

    def create_forest_pipeline(self):
        version = "v0.1.0"
        p = Pipeline.new_pipeline(identifier="unittest_randomforest", version=version, session=self.session)

        user_proj_input = p.create_input_parameter("__userProject", str)
        execution_input = p.create_input_parameter("__execution", 'map')
        feature_col_names_input = p.create_input_parameter("featureColNames", str)
        model_name_input = p.create_input_parameter("modelName", str, value="test_randomforest", required=True)

        output_detail_table_1_input = p.create_input_parameter("outputDetailTableName1", str, required=True)
        output_detail_table_2_input = p.create_input_parameter("outputDetailTableName2", str, required=True)
        output_metric_table_1_input = p.create_input_parameter("outputMetricTableName1", str, required=True)
        output_metric_table_2_input = p.create_input_parameter("outputMetricTableName2", str, required=True)
        output_table_input = p.create_input_parameter("outputTableName", str, required=True)

        input_artifact1 = p.create_input_artifact("inputArtifact", typ={"DataSet": {"locationType": "MaxComputeTable"}},
                                                  required=True)
        input_artifact2 = p.create_input_artifact("inputArtifact2",
                                                  typ={"DataSet": {"locationType": "MaxComputeTable"}},
                                                  required=True)

        randomforest_step = self.add_local_pipeline_step(p, "randomforests-xflow-ODPS")
        randomforest_step.run_with(
            inputArtifact=input_artifact1,
            __userProject=user_proj_input,
            __execution=execution_input,
            featureColNames=feature_col_names_input,
            modelName=model_name_input,
            labelColName=default_step_parameter(typ=str, value="_c2"),
            treeNum=default_step_parameter(typ=int, value=100),
            __generatePMML=default_step_parameter(typ=bool, value=True),
            __pmmlModelPublicProject=default_step_parameter(typ=str, value="pai_online_project"),
            __pmmlModelPublicEndpoint=default_step_parameter(typ=str,
                                                             value="http://service.cn-shanghai.maxcompute.aliyun.com/api"),
            __pmmlModelVolume=default_step_parameter(typ=str, value="pai_model_1557702098194904"),
            __pmmlModelPartition=default_step_parameter(typ=str, value="partition_1099584"),
        )

        prediction_step1 = self.add_local_pipeline_step(p, "prediction-evaluate", name="prediction1")

        prediction_step1.run_with(
            __execution=execution_input,
            outputTableName=output_table_input,
            outputDetailTableName=output_detail_table_1_input,
            outputMetricTableName=output_metric_table_1_input,
            outputDetailTableName2=output_detail_table_2_input,
            outputMetricTableName2=output_metric_table_2_input,
            outputELDetailTableName=default_step_parameter(typ=str, value="pai_temp_83935_1299589_1"),
            outputELDetailTableName2=default_step_parameter(typ=str, value="pai_temp_83935_1399589_1"),
            inputModelArtifact=randomforest_step.outputs["outputArtifact"],
            inputDataSetArtifact=input_artifact2,
        )

        prediction_step2 = self.add_local_pipeline_step(p, "prediction-evaluate", name="prediction2")
        prediction_step2.run_with(
            __execution=execution_input,
            outputDetailTableName2=default_step_parameter(typ=str, value="pai_temp_183935_1099586_1"),
            outputMetricTableName2=default_step_parameter(typ=str, value="pai_temp_183935_1228529_1"),
            outputDetailTableName=default_step_parameter(typ=str, value="pai_temp_183935_1099586_2"),
            outputMetricTableName=default_step_parameter(typ=str, value="pai_temp_183935_1228529_2"),
            outputTableName=default_step_parameter(typ=str, value="pai_temp_183935_1029583_1"),
            outputELDetailTableName=default_step_parameter(typ=str, value="pai_temp_83935_1299589_2"),
            outputELDetailTableName2=default_step_parameter(typ=str, value="pai_temp_83935_1399589_2"),
            inputModelArtifact=randomforest_step.outputs["outputArtifact"],
            inputDataSetArtifact=input_artifact2,
        )

        p.create_output_artifact("predictionResult", from_=prediction_step1.outputs["predictionResult"])
        p.create_output_artifact("predictionResult2", from_=prediction_step2.outputs["predictionResult"])
        return p

    # todo: create air-quality-prediction composite pipeline
    def create_air_quality_prediction(self):
        p = Pipeline.new_pipeline("unittest_air_quality", version="v1.0.0", session=self.session)

        project_input = p.create_input_parameter("__project", str)
        execution_input = p.create_input_parameter("__execution", 'map', required=True)
        cols_to_double_input = p.create_input_parameter("cols_to_double", str, required=True)
        hist_cols_input = p.create_input_parameter("histogram_selected_col_names", str, required=True)
        sql_input = p.create_input_parameter("sql", str, required=True)
        normalize_cols_input = p.create_input_parameter("normalize_selected_col_names", str, required=True)
        fraction_input = p.create_input_parameter("fraction", str, required=True)
        randomforest_feature_cols_input = p.create_input_parameter("randomforest_feature_col_names", str, required=True)
        randomforest_label_col_input = p.create_input_parameter("randomforest_label_col_names", str, required=True)
        prediction1_feature_col_input = p.create_input_parameter("prediction1_feature_col_names", str, required=True)
        prediction1_append_col_input = p.create_input_parameter("prediction1_append_col_names", str, required=True)
        prediction1_result_col_input = p.create_input_parameter("prediction1_result_col_names", str, required=True)
        prediction1_score_col_input = p.create_input_parameter("prediction1_score_col_names", str, required=True)
        prediction1_detail_col_input = p.create_input_parameter("prediction1_detail_col_names", str, required=True)

        evaluate1_label_col_input = p.create_input_parameter("evaluate1_label_col_name", str, required=True)
        evaluate1_score_col_input = p.create_input_parameter("evaluate1_score_col_name", str, required=True)
        evaluate1_positive_label_input = p.create_input_parameter("evaluate1_positive_label", str, required=True)
        evaluate1_bin_count_input = p.create_input_parameter("evaluate1_bin_count", int, required=True)

        logistic_feature_col_input = p.create_input_parameter("logisticregression_feature_col_names", str,
                                                              required=True)
        logistic_label_col_names = p.create_input_parameter("logisticregression_label_col_names", str, required=True)
        logistic_good_value_input = p.create_input_parameter("logisticregression_good_value", str, required=True)

        prediction2_feature_col_input = p.create_input_parameter("prediction2_feature_col_names", str, required=True)
        prediction2_append_col_input = p.create_input_parameter("prediction2_append_col_names", str, required=True)
        prediction2_result_col_input = p.create_input_parameter("prediction2_result_col_names", str, required=True)
        prediction2_score_col_input = p.create_input_parameter("prediction2_score_col_names", str, required=True)
        prediction2_detail_col_input = p.create_input_parameter("prediction2_detail_col_names", str, required=True)

        evaluate2_label_col_input = p.create_input_parameter("evaluate2_label_col_name", str, required=True)
        evaluate2_score_col_input = p.create_input_parameter("evaluate2_score_col_name", str, required=True)
        evaluate2_positive_label_input = p.create_input_parameter("evaluate2_positive_label", str, required=True)
        evaluate2_bin_count_input = p.create_input_parameter("evaluate2_bin_count", int, required=True)

        data_source_step = self.add_local_pipeline_step(p, "odps-data-source", name="dataSource")

        data_source_step.run_with(
            __execution=execution_input,
            tableName="pai_online_project.wumai_data",
        )

        type_transform_step = self.add_local_pipeline_step(p, "type-transform-xflow-ODPS", name="typeTransform")
        type_transform_step.run_with(
            inputArtifat=data_source_step.outputs["outputArtifact"],
            __exeution=execution_input,
            outputTable="type-transform-xflow-ODPS",
            cols_to_doubel=cols_to_double_input,
        )

        histogram_step = self.add_local_pipeline_step(p, "histogram-xflow-ODPS", "histogram")
        histogram_step.run_with(
            inputArtifact=type_transform_step.outputs["outputArtifact"],
        )


if __name__ == "__main__":
    unittest.main()
