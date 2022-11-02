from pai.common import ProviderAlibabaPAI
from pai.entity.training_job import TrainingJob
from tests.integration import BaseIntegTestCase


class TestTrainingJob(BaseIntegTestCase):
    def test_base(self):
        job = TrainingJob(
            algorithm_name="xgboost",
            algorithm_version="v1.5.2",
            algorithm_provider=ProviderAlibabaPAI,
            hyperparameters={
                "feature_col": "feature",
                "label_col": "label",
                "num_round": "2",
                "booster": "gbtree",
                "objective": "binary:logistic",
                "eta": "1.0",
                "gamma": "1.0",
                "min_child_weight": "1.0",
                "max_depth": "3",
            },
            input_channels=[
                {
                    "Name": "train",
                    "InputUri": "oss://alink-test-2.oss-cn-shanghai-internal.aliyuncs.com/deps-files/",
                },
            ],
            output_channels=[
                {
                    "Name": "model",
                    "OutputUri": "oss://lq-pai-test-1-sh.oss-cn-shanghai-internal.aliyuncs.com/sdk-demo/",
                }
            ],
            instance_count=1,
            instance_type="ecs.c6.large",
            job_name="test",
        )
        job.run(wait=True)
