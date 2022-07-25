import os

from pai.core import Session
from pai.job.common import JobConfig, JobType
from pai.operator._custom_job import CustomJobOperator
from pai.operator.types import (
    ArtifactMetadataUtils,
    PipelineArtifact,
)
from pai.pipeline import Pipeline
from tests.integration import BaseIntegTestCase
from tests.test_data import CUSOMT_JOB_SCRIPT_PATH, IRIS_DATA_PATH


class TestCustomJobOperator(BaseIntegTestCase):

    iris_train_data_path = None
    iris_test_data_path = None
    job_output_path = None

    @classmethod
    def setUpClass(cls):
        super(TestCustomJobOperator, cls).setUpClass()
        oss_bucket = Session.current().oss_bucket  # type oss2.Bucket

        cls.iris_train_data_path = cls.upload_file(
            oss_bucket=oss_bucket,
            location="sdk-test/test_data/iris/train/",
            file=os.path.join(IRIS_DATA_PATH, "iris_train.csv"),
        )
        cls.iris_test_data_path = cls.upload_file(
            oss_bucket=oss_bucket,
            location="sdk-test/test_data/iris/test/",
            file=os.path.join(IRIS_DATA_PATH, "iris_test.csv"),
        )
        cls.job_output_path = (
            "oss://{bucket_name}.{endpoint}/sdk-test/job-output-path/".format(
                bucket_name=oss_bucket.bucket_name,
                endpoint=oss_bucket.endpoint.lstrip("https://"),
            )
        )

    @classmethod
    def prepare_job(cls):
        """Prepare custom job for test"""
        sess = Session.current()
        if not sess.is_inner:
            image_uri = "registry.{}.aliyuncs.com/pai-dlc/xgboost-training:1.6.0-cpu-py36-ubuntu18.04".format(
                sess.region_id
            )

            job_config = JobConfig.create(
                worker_instance_type="ecs.c6.large", worker_count=1
            )
        else:
            image_uri = "reg.docker.alibaba-inc.com/pai-dlc/xgboost-training:1.6.0-cpu-py36-ubuntu18.04"
            job_config = JobConfig.create(
                worker_instance_type="pai.1x2.xsmall",
                worker_count=1,
                workspace_id="36",
                resource_id="jspt-pai-dsw-dev",
                priority=9,
            )

        job_operator = CustomJobOperator(
            image_uri=image_uri,
            source_code=CUSOMT_JOB_SCRIPT_PATH,
            entry_point="train.py",
            parameters={
                "n_estimator": 100,
                "criterion": "gini",
                "max_depth": 5,
            },
            code_path="custom-job-test/",
            # Group inner XGBoostJob not support OSS Dataset (PAI DLC Service: bug)
            # job_type=JobType.XGBoostJob,
            job_type=JobType.TFJob,
            # outputs=[PipelineParameter("test-accuracy")],
        )

        return image_uri, job_config

    def test_submit_job(self):
        image_uri, job_config = self.prepare_job()
        job_operator = CustomJobOperator(
            image_uri=image_uri,
            source_code=CUSOMT_JOB_SCRIPT_PATH,
            entry_point="train.py",
            parameters={
                "n_estimator": 100,
                "criterion": "gini",
                "max_depth": 5,
            },
            code_path="custom-job-test/",
            # Group inner XGBoostJob not support OSS Dataset (PAI DLC Service: bug)
            # job_type=JobType.XGBoostJob,
            job_type=JobType.TFJob,
            # outputs=[PipelineParameter("test-accuracy")],
        )

        job_operator.run(
            job_name="custom-job-example",
            inputs={
                "train": self.iris_train_data_path,
                "test": self.iris_test_data_path,
            },
            output_path=self.job_output_path,
            job_config=job_config,
        )

    def test_custom_job_in_workflow(self):
        image_uri, job_config = self.prepare_job()

        op = CustomJobOperator(
            image_uri=image_uri,
            source_code=CUSOMT_JOB_SCRIPT_PATH,
            entry_point="train.py",
            parameters={
                "n_estimator": 100,
                "criterion": "gini",
                "max_depth": 5,
            },
            outputs=[
                # PipelineParameter("test-accuracy"),
            ],
            inputs=[
                PipelineArtifact("train", ArtifactMetadataUtils.oss_dataset()),
            ],
        )

        step1 = op.as_step(
            name="train-step-1",
            inputs={
                "job_config": job_config.to_dict(),
                "output_path": self.job_output_path + "train-step-1/",
                "train": self.iris_train_data_path,
                "n_estimator": 500,
            },
        )

        step2 = op.as_step(
            name="train-step-2",
            inputs={
                "job_config": job_config.to_dict(),
                "output_path": self.job_output_path + "train-step-1/",
                "train": self.iris_train_data_path,
                "n_estimator": 500,
            },
            depends=[step1],
        )

        p = Pipeline(steps=[step1, step2])
        p.run("example-workflow")
