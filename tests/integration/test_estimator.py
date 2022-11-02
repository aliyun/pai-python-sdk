import os

from pai.core.session import get_default_session
from pai.entity.job import JobSpec
from pai.estimator import Estimator
from tests.integration import BaseIntegTestCase
from tests.test_data import CUSTOM_JOB_SCRIPT_PATH, IRIS_DATA_PATH


class TestEstimator(BaseIntegTestCase):

    iris_train_data_path = None
    iris_test_data_path = None
    job_output_path = None

    @classmethod
    def setUpClass(cls):
        super(TestEstimator, cls).setUpClass()

        oss_bucket = get_default_session().oss_bucket  # type oss2.Bucket

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

    def _make_estimator(self):
        sess = get_default_session()
        image_uri = "registry.{}.aliyuncs.com/pai-dlc/xgboost-training:1.6.0-cpu-py36-ubuntu18.04".format(
            sess.region_id
        )

        est = Estimator(
            image_uri=image_uri,
            source_code=CUSTOM_JOB_SCRIPT_PATH,
            entry_point="train.py",
            hyperparameters={
                "n_estimator": 100,
                "criterion": "gini",
                "max_depth": 5,
            },
            code_path="custom-job-test/",
            # Group inner XGBoostJob not support OSS Dataset (PAI DLC Service: bug)
            # job_type=JobType.XGBoostJob,
            job_type="TFJob",
            job_specs=JobSpec.from_instance_type(
                worker_instance_type="ecs.c6.large", worker_count=1
            ),
        )
        return est

    def test_base(self):
        est = self._make_estimator()
        est.fit(
            inputs={
                "train": self.iris_train_data_path,
                "test": self.iris_test_data_path,
            },
        )

    def test_estimator_local_run(self):
        est = self._make_estimator()

        est.local_run(
            inputs={
                "train": os.path.join(IRIS_DATA_PATH, "iris_train.csv"),
            },
        )
