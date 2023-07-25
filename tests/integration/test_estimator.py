import os
from unittest import skipUnless

from pai.common.oss_utils import OssUriObj, upload
from pai.estimator import Estimator
from pai.image import retrieve
from pai.session import get_default_session
from tests.integration import BaseIntegTestCase
from tests.integration.utils import t_context
from tests.test_data import test_data_dir


class TestEstimator(BaseIntegTestCase):

    job_output_path = None

    @classmethod
    def setUpClass(cls):
        super(TestEstimator, cls).setUpClass()
        oss_bucket = get_default_session().oss_bucket  # type oss2.Bucket

        cls.breast_cancer_train_data_uri = cls.upload_file(
            oss_bucket=oss_bucket,
            location="sdk-test/test_data/breast_cancer_data/train/",
            file=os.path.join(test_data_dir, "breast_cancer_data/train.csv"),
        )
        cls.breast_cancer_test_data_uri = cls.upload_file(
            oss_bucket=oss_bucket,
            location="sdk-test/test_data/breast_cancer_data/test/",
            file=os.path.join(test_data_dir, "breast_cancer_data/test.csv"),
        )

    def test_xgb_train(self):
        xgb_image_uri = retrieve("xgboost", framework_version="latest").image_uri

        est = Estimator(
            image_uri=xgb_image_uri,
            source_dir=os.path.join(test_data_dir, "xgb_train"),
            command="python train.py",
            hyperparameters={
                "n_estimators": 50,
                "objective": "binary:logistic",
                "max_depth": 5,
                "eval_metric": "auc",
            },
            instance_type="ecs.c6.large",
        )

        est.fit(
            inputs={
                "train": self.breast_cancer_train_data_uri,
                "test": self.breast_cancer_test_data_uri,
            },
        )

        model_path = os.path.join(os.path.join(est.model_data(), "model.json"))

        self.assertTrue(self.is_oss_object_exists(model_path))

    def is_oss_object_exists(self, model_path):
        uri_obj = OssUriObj(model_path)

        oss_bucket = self.default_session.get_oss_bucket(uri_obj.bucket_name)

        return oss_bucket.object_exists(uri_obj.object_key)

    def test_torch_run(self):
        torch_image_uri = retrieve("pytorch", framework_version="1.12").image_uri
        est = Estimator(
            image_uri=torch_image_uri,
            command="python -c 'import torch; print(torch.__version__);'",
            instance_type="ecs.c6.large",
            base_job_name="torch_run_",
        )

        est.fit(
            inputs={
                "training": self.breast_cancer_train_data_uri,
                "test": self.breast_cancer_test_data_uri,
            },
            wait=False,
        )

        tb = est.tensorboard()
        self.assertIsNotNone(tb.app_uri)
        tb.delete()


@skipUnless(t_context.has_docker, "Estimator local train requires docker.")
class TestEstimatorLocalRun(BaseIntegTestCase):
    def test_local_data(self):
        image_uri = retrieve("xgboost", framework_version="latest").image_uri
        train_file = os.path.join(test_data_dir, "breast_cancer_data/train.csv")
        test_file = os.path.join(test_data_dir, "breast_cancer_data/test.csv")

        est = Estimator(
            image_uri=image_uri,
            source_dir=os.path.join(test_data_dir, "xgb_train"),
            command="python train.py $PAI_USER_ARGS",
            hyperparameters={
                "n_estimators": 50,
                "objective": "binary:logistic",
                "max_depth": 5,
                "eval_metric": "auc",
            },
            instance_type="local",
        )

        est.fit(
            inputs={
                "train": train_file,
                "test": test_file,
            },
        )
        self.assertTrue(os.path.exists(os.path.join(est.model_data(), "model.json")))

    def test_remote_data(self):
        image_uri = retrieve("xgboost", framework_version="latest").image_uri
        train_data_uri = upload(
            os.path.join(test_data_dir, "breast_cancer_data/train.csv"),
            oss_path="sdk-test/test_data/breast_cancer_data/train/",
        )
        test_data_uri = upload(
            os.path.join(test_data_dir, "breast_cancer_data/test.csv"),
            oss_path="sdk-test/test_data/breast_cancer_data/test/",
        )

        est = Estimator(
            image_uri=image_uri,
            source_dir=os.path.join(test_data_dir, "xgb_train"),
            command="python train.py $PAI_USER_ARGS",
            hyperparameters={
                "n_estimators": 50,
                "objective": "binary:logistic",
                "max_depth": 5,
                "eval_metric": "auc",
            },
            instance_type="local",
        )

        est.fit(
            inputs={
                "train": train_data_uri,
                "test": test_data_uri,
            },
        )
        self.assertTrue(os.path.exists(os.path.join(est.model_data(), "model.json")))


@skipUnless(
    t_context.has_docker and t_context.has_gpu,
    "Estimator local gpu train requires docker and gpu.",
)
class TestEstimatorLocalRunGPU(BaseIntegTestCase):
    def test(self):
        image_uri = retrieve(
            "pytorch",
            "1.12",
            accelerator_type="GPU",
        ).image_uri

        est = Estimator(
            image_uri=image_uri,
            command="python train.py",
            source_dir=os.path.join(test_data_dir, "local_gpu_torch"),
            instance_type="local_gpu",
        )
        est.fit()
