import os
from urllib.parse import urlencode

from six.moves.urllib import parse
import tempfile
from pai.common.oss_utils import parse_oss_url
from pai.core import Session
from pai.job import CustomJob
from pai.job.common import JobConfig, JobType
from pai.operator._custom_job import CustomJobOperator, _CustomJobEnv
from pai.operator.types import (
    PipelineParameter,
    PipelineArtifact,
    ArtifactMetadataUtils,
)
from tests.integration import BaseIntegTestCase
from tests.test_data import CUSOMT_JOB_SCRIPT_PATH, IRIS_DATA_PATH


class TestCustomJob(BaseIntegTestCase):

    iris_train_data_path = None
    iris_test_data_path = None
    job_output_path = None

    @classmethod
    def setUpClass(cls):
        super(TestCustomJob, cls).setUpClass()
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

        job = CustomJob(
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
        )

        return job, job_config

    def test_custom_job(self):
        job, job_config = self.prepare_job()
        job.run(
            name="custom-job-example",
            inputs={
                "train": self.iris_train_data_path,
                "test": self.iris_test_data_path,
            },
            output_path=self.job_output_path,
            job_config=job_config,
        )

    def test_custom_job_as_component(self):
        job, job_config = self.prepare_job()
        op: CustomJobOperator = job.as_component(
            inputs=[
                PipelineArtifact(
                    "train",
                    metadata=ArtifactMetadataUtils.oss_dataset(),
                ),
                PipelineArtifact(
                    "test",
                    metadata=ArtifactMetadataUtils.oss_dataset(),
                ),
            ],
            outputs=[PipelineParameter("test-accuracy")],
        )

        self.assertListEqual(
            sorted([item.name for item in op.inputs]),
            sorted(
                [
                    "train",
                    "test",
                    "n_estimator",
                    "criterion",
                    "max_depth",
                    "job_config",
                    "output_path",
                ]
            ),
        )

        self.assertListEqual(
            sorted([item.name for item in op.outputs]), sorted(["test-accuracy"])
        )

        self.assertEqual(
            op.to_dict()["spec"]["container"]["envs"][
                _CustomJobEnv.ENV_CUSTOM_JOB_IMAGE_URI
            ],
            job.image_uri,
        )
        self.assertEqual(
            op.to_dict()["spec"]["container"]["envs"][
                _CustomJobEnv.ENV_CUSTOM_JOB_TYPE
            ],
            job.job_type,
        )

        self.assertEqual(
            op.to_dict()["spec"]["container"]["envs"][
                _CustomJobEnv.ENV_CUSTOM_JOB_TYPE
            ],
            job.job_type,
        )
        self.assertEqual(
            op.to_dict()["spec"]["container"]["envs"][
                _CustomJobEnv.ENV_CUSTOM_JOB_ENTRY_POINT
            ],
            job.entry_point,
        )

        source_file = op.to_dict()["spec"]["container"]["envs"][
            _CustomJobEnv.ENV_CUSTOM_JOB_SOURCE_FILE
        ]

        parsed = parse_oss_url(source_file)
        self.assertTrue(parsed.object_key.startswith(job.code_path))

        op.run(
            job_name="custom-job-component-example",
            inputs={
                "train": self.iris_train_data_path,
                "test": self.iris_test_data_path,
            },
            output_path=self.job_output_path,
            job_config=job_config,
        )

    def test_custom_job_local_run(self):
        job, _ = self.prepare_job()
        output_path = tempfile.mkdtemp()

        job.local_run(
            inputs={
                "train": os.path.join(IRIS_DATA_PATH, "iris_train.csv"),
            },
            output_path=output_path,
        )

        self.assertTrue(
            os.path.exists(os.path.join(output_path, "model/model/model.pkl"))
        )
