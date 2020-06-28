from __future__ import absolute_import

import os
import unittest

from pai.pipeline import Pipeline, default_step_parameter, PipelineStep
from tests import BaseTestCase
from tests.test_paiflow import load_local_yaml

_current_dir_path = os.path.dirname(os.path.abspath(__file__))


class MockPropertySession(object):

    @property
    def account_id(self):
        return 0


class TestPipeline(BaseTestCase):

    def setUp(self):
        super(TestPipeline, self).setUp()

    def tearDown(self):
        super(TestPipeline, self).tearDown()

    def test_forest_pipeline_create(self):
        pipeline = self.create_forest_pipeline()
        expected = load_local_yaml("unittest-randomforest.yaml")
        self.assertDictEqual(pipeline.to_dict(), expected)

    def test_air_quality_pipeline_create(self):
        pipeline = self.create_air_quality_prediction()
        expected = load_local_yaml("unittest-air-quality.yaml")
        self.assertDictEqual(pipeline.to_dict(), expected)

    def test_cycle_detection(self):
        with self.assertRaises(ValueError):
            self.create_cycle_pipeline()

    @staticmethod
    def add_local_pipeline_step(pipeline, identifier, name=None):
        manifest = load_local_yaml("%s.yaml" % identifier)
        step = PipelineStep.create_from_manifest(manifest, pipeline, name=name if name else identifier)
        pipeline.steps[step.name] = step
        return step

    def create_forest_pipeline(self):
        version = "v0.1.0"
        p = Pipeline.new_pipeline(identifier="unittest_randomforest", version=version, session=MockPropertySession())

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

        randomforest_step = self.add_local_pipeline_step(p, "random-forests-xflow-ODPS")
        randomforest_step.run_with(
            inputArtifact=input_artifact1,
            __userProject=user_proj_input,
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

        p.create_output_artifact("predictionResult", from_=prediction_step1.outputs["predictionResult"])
        p.create_output_artifact("predictionResult2", from_=prediction_step2.outputs["predictionResult"])
        return p

    def create_air_quality_prediction(self):
        p = Pipeline.new_pipeline("unittest_air_quality", version="v1.0.0", session=MockPropertySession())

        project_input = p.create_input_parameter("__project", str)
        execution_input = p.create_input_parameter("__execution", 'map', required=True)
        cols_to_double_input = p.create_input_parameter("cols_to_double", str, required=True)
        hist_cols_input = p.create_input_parameter("histogram_selected_col_names", str, required=True)
        sql_input = p.create_input_parameter("sql", str, required=True)
        normalize_cols_input = p.create_input_parameter("normalize_selected_col_names", str, required=True)
        fraction_input = p.create_input_parameter("fraction", float, required=True)
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
        logistic_good_value_input = p.create_input_parameter("logisticregression_good_value", int, required=True)

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
            inputArtifact=data_source_step.outputs["outputArtifact"],
            __execution=execution_input,
            outputTable="type-transform-xflow-ODPS",
            cols_to_double=cols_to_double_input,
        )

        histogram_step = self.add_local_pipeline_step(p, "histogram-xflow-ODPS", "histogram")
        histogram_step.run_with(
            inputArtifact=type_transform_step.outputs["outputArtifact"],
            __execution=execution_input,
            outputTableName="pai_temp_172808_1779985_1",
            selectedColNames=hist_cols_input,
        )

        sql_step = self.add_local_pipeline_step(p, "sql-xflow-ODPS", name="sql")
        sql_step.run_with(
            inputArtifact1=type_transform_step.outputs["outputArtifact"],
            __execution=execution_input,
            outputTable="pai_temp_83935_1099579_1",
            sql=sql_input,
        )

        fe_meta_runner_step = self.add_local_pipeline_step(p, "fe-meta-runner-xflow-ODPS", name="feMetaRunner")

        fe_meta_runner_step.run_with(
            inputArtifact=sql_step.outputs["outputArtifact"],
            __execution=execution_input,
            outputTable="pai_temp_83935_1099581_1",
            mapTable="pai_temp_83935_1099581_2",
            selectedCols="pm10,so2,co,no2",
            labelCol="_c2",
        )

        normalized_step = self.add_local_pipeline_step(p, "normalize-xflow-ODPS", name="normalize")
        normalized_step.run_with(
            inputArtifact=sql_step.outputs["outputArtifact"],
            __execution=execution_input,
            outputTableName="pai_temp_83935_1099582_1",
            outputParaTableName="pai_temp_83935_1099582_2",
            selectedColNames=normalize_cols_input,
        )

        split_step = self.add_local_pipeline_step(p, "split-xflow-ODPS", name="split")
        split_step.run_with(
            inputArtifact=normalized_step.outputs["outputArtifact"],
            __execution=execution_input,
            output1TableName="pai_temp_83935_1099583_1",
            fraction=fraction_input,
            output2TableName="pai_temp_83935_1199583_1",
        )

        randomforest_step = self.add_local_pipeline_step(p, "random-forests-xflow-ODPS", "randomforests")
        randomforest_step.run_with(
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
            __userProject=project_input,
        )

        prediction1_step = self.add_local_pipeline_step(p, "prediction-xflow-ODPS", "prediction1")
        prediction1_step.run_with(
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
        evaluate1_step = self.add_local_pipeline_step(p, "evaluate-xflow-ODPS", "evaluate1")
        evaluate1_step.run_with(
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
        logistic_step = self.add_local_pipeline_step(p, "logisticregression-binary-xflow-ODPS", "logisticregression")

        logistic_step.run_with(
            inputArtifact=split_step.outputs["outputArtifact1"],
            __userProject=project_input,
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

        prediction2_step = self.add_local_pipeline_step(p, "prediction-xflow-ODPS", "prediction2")
        prediction2_step.run_with(
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

        evaluate2_step = self.add_local_pipeline_step(p, "evaluate-xflow-ODPS", "evaluate2")
        evaluate2_step.run_with(
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

        p.create_output_artifact("predictionResult", from_=evaluate2_step.outputs["outputDetailArtifact"])
        return p

    def create_cycle_pipeline(self):
        p = Pipeline.new_pipeline(identifier="unittest_cycle_case_1", version="v1.0.0", session=MockPropertySession())
        execution_input = p.create_input_parameter("__execution", 'map', required=True)
        cols_to_double_input = p.create_input_parameter("cols_to_double", str, required=True)

        data_source_step = self.add_local_pipeline_step(p, "odps-data-source", name="dataSource")
        data_source_step.run_with(
            __execution=execution_input,
            tableName="pai_online_project.wumai_data",
        )

        type_transform_step = self.add_local_pipeline_step(p, "type-transform-xflow-ODPS", name="typeTransform")
        type_transform_step.run_with(
            inputArtifact=data_source_step.outputs["outputArtifact"],
            __execution=execution_input,
            outputTable="type-transform-xflow-ODPS",
            cols_to_double=cols_to_double_input,
        )

        data_source_step.run_after(type_transform_step)


if __name__ == "__main__":
    unittest.main()
