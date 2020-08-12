from __future__ import absolute_import

import random
import time

from pai.pipeline.artifact import ArtifactDataType, ArtifactLocationType
from pai.pipeline.parameter import ParameterType
from pai.utils import gen_temp_table

from pai import Pipeline
from pai.common import ProviderAlibabaPAI
from pai.estimator import EstimatorJob
from pai.job import JobStatus
from pai.pipeline import PipelineRun, PipelineStep, PipelineRunStatus
from pai.transformer import PipelineTransformer
from pai.xflow.classifier import LogisticRegression
from tests import BaseTestCase


class TestXFlowEstimator(BaseTestCase):

    def test_algo_init(self):
        lr = LogisticRegression(
            session=self.session,
            regularized_level=1.0,
            regularized_type="l2",
            max_iter=200,
            epsilon=1e-6
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
            session=self.session,
            regularized_level=2.0,
            regularized_type="l1",
            max_iter=100,
            epsilon=1e-5,
            pmml_gen=True,
            pmml_oss_rolearn="test_role_arn",
            pmml_oss_bucket="test_oss_bucket",
            pmml_oss_path="test_oss_path",
            pmml_oss_endpoint="cn-hangzhou.oss.aliyuncs.com"
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
        lr = LogisticRegression(
            session=self.session
        )

        args = {
            "regularized_level": 1.0,
            "regularized_type": "l2",
            "max_iter": 200,
            "epsilon": 1e-6,
            "feature_cols": ["pm2", "co2"],
            "label_col": "_c2",
            "model_name": "ut_lr_model",
            "enable_sparse": True,
            "sparse_delimiter": (",", ":")
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
            "execution": lr.xflow_execution,
        }

        compiled_args = lr._compile_args(
            "pai_temp_table",
            **args
        )

        result_args = {k: v for k, v in compiled_args.items() if k in expected}

        self.assertDictEqual(result_args, expected)

    def test_multiple_call_fit(self):
        pass


class TestXFlowAlgo(BaseTestCase):

    def test_algo_chain(self):
        default_project = self.odps_client.project
        xflow_execution = {
            "odpsInfoFile": "/share/base/odpsInfo.ini",
            "endpoint": "http://service.cn-shanghai.maxcompute.aliyun.com/api",
            "logViewHost": "http://logview.odps.aliyun.com",
            "odpsProject": default_project,
        }

        tf = Pipeline.get_by_identifier(session=self.session, identifier="split-xflow-maxCompute",
                                        provider=ProviderAlibabaPAI, version="v1").to_transformer(
            parameters={"execution": xflow_execution, "fraction": 0.7, })

        job = tf.transform(wait=False, args={
            "inputArtifact": "odps://{0}/tables/{1}".format(default_project, "iris_data"),
            "output1TableName": gen_temp_table(),
            "output2TableName": gen_temp_table(),
        })

        job.attach(log_outputs=False)
        self.assertEqual(JobStatus.Succeeded, job.get_status())
        time.sleep(20)  # Because of outputs delay.
        job_outputs = job.get_outputs()
        dataset1 = job_outputs["outputArtifact1"]
        dataset2 = job_outputs["outputArtifact2"]

        oss_endpoint = self.oss_info.endpoint
        oss_path = "/pai_test/test_algo_chain/"
        oss_bucket = self.oss_info.bucket

        model_name = 'test_iris_model_%d' % (random.randint(0, 999999))
        lr = LogisticRegression(session=self.session, regularized_type="l2",
                                pmml_gen=True, pmml_oss_bucket=oss_bucket,
                                pmml_oss_path=oss_path, pmml_oss_endpoint=oss_endpoint,
                                pmml_oss_rolearn="acs:ram::1557702098194904:role/aliyunodpspaidefaultrole",
                                xflow_execution=xflow_execution)

        feature_cols = ["f1", "f2", "f3", "f4"]
        label_col = "type"

        job = lr.fit(wait=True, input_data=dataset1,
                     job_name="pysdk-test-lr-sync-fit",
                     model_name=model_name, good_value=1, label_col=label_col,
                     feature_cols=feature_cols)
        self.assertEqual(JobStatus.Succeeded, job.get_status())
        time.sleep(20)  # Because of outputs delay.
        self.assertTrue(self.odps_client.exist_offline_model(
            model_name, default_project,
        ))
        oss_bucket = self.session.get_oss_bucket(endpoint=oss_endpoint, bucket=oss_bucket)
        object_key = oss_path + model_name + ".xml"
        self.assertTrue(oss_bucket.object_exists(object_key))
        model = job.create_model(output_name="outputArtifact")
        tf = model.transformer()
        job = tf.transform(
            input_data="odps://{0}/tables/{1}".format(default_project, "pai_temp_iris_split_2"),
            wait=False, feature_cols=["f1", "f2", "f3", "f4"],
            append_cols=["f1", "f2", "f3", "f4", "type"],
            label_col="type")
        job.attach(log_outputs=False)
        self.assertEqual(JobStatus.Succeeded, job.get_status())
        # TODO: multi-class-evaluate pipeline is required

    def test_heart_disease_step_by_step(self):
        default_project = "pai_sdk_test"
        xflow_execution = {
            "odpsInfoFile": "/share/base/odpsInfo.ini",
            "endpoint": "http://service.cn-shanghai.maxcompute.aliyun.com/api",
            "logViewHost": "http://logview.odps.aliyun.com",
            "odpsProject": default_project,
        }

        dataset_table = "odps://pai_online_project/tables/heart_disease_prediction"

        sql = "select age, (case sex when 'male' then 1 else 0 end) as sex, (case cp when " \
              "'angina' then 0  when 'notang' then 1 else 2 end) as cp, trestbps, chol, (case" \
              " fbs when 'true' then 1 else 0 end) as fbs, (case restecg when 'norm' then 0 " \
              " when 'abn' then 1 else 2 end) as restecg, thalach, (case exang when 'true' then" \
              " 1 else 0 end) as exang, oldpeak, (case slop when 'up' then 0  when 'flat' then " \
              "1 else 2 end) as slop, ca, (case thal when 'norm' then 0  when 'fix' then 1" \
              " else 2 end) as thal, (case status  when 'sick' then 1 else 0 end) as" \
              " ifHealth from ${t1};"

        # Extract and transform dataset using max_compute sql.
        sql_job = Pipeline.get_by_identifier(identifier="sql-xflow-maxCompute",
                                             provider=ProviderAlibabaPAI, version="v1",
                                             session=self.session).to_estimator(
            parameters={
                "execution": xflow_execution,
                "inputArtifact1": dataset_table,
                "sql": sql,
                "outputTable": gen_temp_table(),
            }).fit(wait=True, log_outputs=True)

        time.sleep(10)
        output_table_artifact = sql_job.get_outputs()[0]

        type_transform_job = Pipeline.get_by_identifier(
            identifier="type-transform-xflow-maxCompute",
            provider=ProviderAlibabaPAI, version="v1",
            session=self.session).to_estimator(
            parameters={
                "execution": xflow_execution,
                "inputArtifact": output_table_artifact,
                "cols_to_double": 'sex,cp,fbs,restecg,exang,slop,thal,ifhealth,age,trestbps,chol,thalach,oldpeak,ca',
                "outputTable": gen_temp_table(),
            }
        ).fit()

        time.sleep(20)
        type_transform_result = type_transform_job.get_outputs()[0]

        # Normalize Feature
        normalize_job = Pipeline.get_by_identifier(identifier="normalize-xflow-maxCompute",
                                                   provider=ProviderAlibabaPAI, version="v1",
                                                   session=self.session).to_estimator(
            parameters={
                "execution": xflow_execution,
                "inputArtifact": type_transform_result,
                "selectedColNames": 'sex,cp,fbs,restecg,exang,slop,thal,ifhealth,age,trestbps,'
                                    'chol,thalach,oldpeak,ca',
                "lifecycle": 1,
                "outputTableName": gen_temp_table(),
                "outputParaTableName": gen_temp_table(),
            }
        ).fit()
        time.sleep(20)
        normalized_dataset = normalize_job.get_outputs()[0]

        split_job = Pipeline.get_by_identifier(
            identifier="split-xflow-maxCompute",
            provider=ProviderAlibabaPAI, version="v1",
            session=self.session).to_estimator(
            parameters={
                "inputArtifact": normalized_dataset,
                "execution": xflow_execution,
                "fraction": 0.8,
                "output1TableName": gen_temp_table(),
                "output2TableName": gen_temp_table(),
            }
        ).fit()

        time.sleep(20)
        split_output_1, split_output_2 = split_job.get_outputs()

        oss_endpoint = "oss-cn-shanghai.aliyuncs.com"
        oss_path = "/paiflow/model_transfer2oss_test/"
        oss_bucket = "dataplus-pai-test"
        lr_job = LogisticRegression(
            session=self.session, regularized_type="l2", xflow_execution=xflow_execution,
            pmml_gen=True, pmml_oss_bucket=oss_bucket,
            pmml_oss_path=oss_path, pmml_oss_endpoint=oss_endpoint,
            pmml_oss_rolearn="acs:ram::1557702098194904:role/aliyunodpspaidefaultrole",
        ).fit(split_output_1,
              wait=True,
              feature_cols='sex,cp,fbs,restecg,exang,slop,thal,age,trestbps,chol,thalach,oldpeak,ca',
              label_col="ifhealth",
              good_value=1,
              model_name="test_health_prediction")

        time.sleep(20)
        offlinemodel_artifact, pmml_output = lr_job.get_outputs()
        transform_job = Pipeline.get_by_identifier(
            identifier="prediction-xflow-maxCompute",
            provider=ProviderAlibabaPAI, version="v1",
            session=self.session).to_estimator(
            parameters={
                "inputModelArtifact": offlinemodel_artifact,
                "inputDataSetArtifact": split_output_2,
                "execution": xflow_execution,
                "outputTableName": gen_temp_table(),
                "featureColNames": 'sex,cp,fbs,restecg,exang,slop,thal,age,trestbps,chol,thalach,oldpeak,ca',
                "appendColNames": "ifhealth",
            }
        ).fit()

        time.sleep(20)
        transform_result = transform_job.get_outputs()[0]

        evaluate_job = Pipeline.get_by_identifier(
            identifier="evaluate-xflow-maxCompute",
            provider=ProviderAlibabaPAI, version="v1",
            session=self.session).to_estimator(
            parameters={
                "execution": xflow_execution,
                "inputArtifact": transform_result,
                "outputDetailTableName": gen_temp_table(),
                "outputELDetailTableName": gen_temp_table(),
                "outputMetricTableName": gen_temp_table(),
                "scoreColName": "prediction_score",
                "labelColName": "ifhealth",
                "coreNum": 2,
                "memSizePerCore": 512,
            }
        ).fit()

        time.sleep(20)

        self.assertEqual(JobStatus.Succeeded, evaluate_job.get_status())
        time.sleep(10)
        evaluate_result = evaluate_job.get_outputs()[2]
        print(evaluate_result)

    def test_heart_disease_prediction_pipeline(self):
        def create_pipeline():
            p = Pipeline.new_pipeline("test-heart-prediction", version="v1",
                                      session=self.session)

            pmml_oss_bucket = p.create_input_parameter("pmml_oss_bucket", ParameterType.String,
                                                       required=True)
            pmml_oss_rolearn = p.create_input_parameter("pmml_oss_rolearn", ParameterType.String,
                                                        required=True)
            pmml_oss_path = p.create_input_parameter("pmml_oss_path", ParameterType.String,
                                                     required=True)
            pmml_oss_endpoint = p.create_input_parameter("pmml_oss_endpoint", ParameterType.String,
                                                         required=True)
            xflow_execution = p.create_input_parameter("xflow_execution", ParameterType.Map,
                                                       required=True)
            dataset_input = p.create_input_artifact("dataset-table",
                                                    data_type=ArtifactDataType.DataSet,
                                                    location_type=ArtifactLocationType.MaxComputeTable,
                                                    required=True)

            sql = "select age, (case sex when 'male' then 1 else 0 end) as sex,(case cp when" \
                  " 'angina' then 0  when 'notang' then 1 else 2 end) as cp, trestbps, chol," \
                  " (case fbs when 'true' then 1 else 0 end) as fbs, (case restecg when 'norm'" \
                  " then 0  when 'abn' then 1 else 2 end) as restecg, thalach, (case exang when" \
                  " 'true' then 1 else 0 end) as exang, oldpeak, (case slop when 'up' then 0  " \
                  "when 'flat' then 1 else 2 end) as slop, ca, (case thal when 'norm' then 0 " \
                  " when 'fix' then 1 else 2 end) as thal, (case status when 'sick' then 1 else " \
                  "0 end) as ifHealth from ${t1};"
            sql_step = p.create_step("sql-xflow-maxCompute", name="sql-1",
                                     provider=ProviderAlibabaPAI,
                                     version="v1",
                                     arguments={
                                         "inputArtifact1": dataset_input,
                                         "execution": xflow_execution,
                                         "sql": sql,
                                         "outputTable": gen_temp_table(),
                                     })

            type_transform_step = p.create_step(
                "type-transform-xflow-maxCompute",
                name="type-transform-1",
                provider=ProviderAlibabaPAI, version="v1",
                arguments={
                    "execution": xflow_execution,
                    "inputArtifact": sql_step.outputs["outputArtifact"],
                    "cols_to_double": 'sex,cp,fbs,restecg,exang,slop,thal,ifhealth,age,trestbps,'
                                      'chol,thalach,oldpeak,ca',
                    "outputTable": gen_temp_table(),

                })

            normalize_step = p.create_step(
                "normalize-xflow-maxCompute",
                name="normalize-1",
                provider=ProviderAlibabaPAI,
                version="v1", arguments={
                    "execution": xflow_execution,
                    "inputArtifact": type_transform_step.outputs["outputArtifact"],
                    "selectedColNames": 'sex,cp,fbs,restecg,exang,slop,thal,ifhealth,age,trestbps,'
                                        'chol,thalach,oldpeak,ca',
                    "lifecycle": 1,
                    "outputTableName": gen_temp_table(),
                    "outputParaTableName": gen_temp_table(),

                })

            split_step = p.create_step(
                identifier="split-xflow-maxCompute",
                name='split-1',
                provider=ProviderAlibabaPAI, version="v1", arguments={
                    "inputArtifact": normalize_step.outputs["outputArtifact"],
                    "execution": xflow_execution,
                    "fraction": 0.8,
                    "output1TableName": gen_temp_table(),
                    "output2TableName": gen_temp_table(),

                }
            )

            model_name = 'test_health_prediction_by_pipeline_%s' % (random.randint(0, 999999))

            lr_step = p.create_step(
                identifier="logisticregression-binary-xflow-maxCompute",
                name="logisticregression-1",
                provider=ProviderAlibabaPAI, version="v1", arguments={
                    "inputArtifact": split_step.outputs["outputArtifact1"],
                    "execution": xflow_execution,
                    "generatePmml": True,
                    "endpoint": pmml_oss_endpoint,
                    "bucket": pmml_oss_bucket,
                    "path": pmml_oss_path,
                    "rolearn": pmml_oss_rolearn,
                    # "regulizedType": "l2",
                    "modelName": model_name,
                    "goodValue": 1,
                    "featureColNames": "sex,cp,fbs,restecg,exang,slop,thal,age,trestbps,chol,thalach,oldpeak,ca",
                    "labelColName": "ifhealth",
                }
            )

            offline_model_pred_step = p.create_step(
                identifier="prediction-xflow-maxCompute",
                name="offlinemodel-pred",
                provider=ProviderAlibabaPAI, version="v1", arguments={
                    "inputModelArtifact": lr_step.outputs["outputArtifact"],
                    "inputDataSetArtifact": split_step.outputs["outputArtifact2"],
                    "execution": xflow_execution,
                    "outputTableName": gen_temp_table(),
                    "featureColNames": 'sex,cp,fbs,restecg,exang,slop,thal,age,trestbps,chol,thalach,oldpeak,ca',
                    "appendColNames": "ifhealth",
                }
            )

            evaluate_step = p.create_step(
                identifier="evaluate-xflow-maxCompute",
                name="evaluate-1",
                provider=ProviderAlibabaPAI, version="v1",
                arguments={
                    "execution": xflow_execution,
                    "inputArtifact": offline_model_pred_step.outputs["outputArtifact"],
                    "outputDetailTableName": gen_temp_table(),
                    "outputELDetailTableName": gen_temp_table(),
                    "outputMetricTableName": gen_temp_table(),
                    "scoreColName": "prediction_score",
                    "labelColName": "ifhealth",
                    "coreNum": 2,
                    "memSizePerCore": 512,
                }
            )

            p.create_output_artifact("pmmlModel", from_=lr_step.outputs["outputArtifact"])
            p.create_output_artifact("evaluateResult",
                                     from_=evaluate_step.outputs["outputMetricsArtifact"])

            return p

        p = create_pipeline()

        pmml_oss_endpoint = "oss-cn-shanghai.aliyuncs.com"
        pmml_oss_path = "/paiflow/model_transfer2oss_test/"
        pmml_oss_bucket = "dataplus-pai-test"
        pmml_oss_rolearn = "acs:ram::1557702098194904:role/aliyunodpspaidefaultrole"

        default_project = "pai_sdk_test"

        dataset_table = 'odps://pai_online_project/tables/heart_disease_prediction'

        print(p.to_dict())

        run_instance = p.run(name="test_run", arguments={
            "xflow_execution": {
                "odpsInfoFile": "/share/base/odpsInfo.ini",
                "endpoint": "http://service.cn-shanghai.maxcompute.aliyun.com/api",
                "logViewHost": "http://logview.odps.aliyun.com",
                "odpsProject": default_project,
            },
            "pmml_oss_rolearn": pmml_oss_rolearn,
            "pmml_oss_path": pmml_oss_path,
            "pmml_oss_bucket": pmml_oss_bucket,
            "pmml_oss_endpoint": pmml_oss_endpoint,
            "dataset-table": dataset_table,
        }, wait=False)
        run_instance.wait(log_outputs=False)

        self.assertEqual(PipelineRunStatus.Succeeded, run_instance.get_status())
