from pai.common.utils import random_str
from pai.entity import Dataset
from tests.integration import BaseIntegTestCase
from tests.integration.utils import make_resource_name


class TestDataset(BaseIntegTestCase):
    def test_dataset(self):
        dataset = Dataset.upload(
            name=make_resource_name("test_dataset"),
            source="oss://lq-test-bucket.oss-cn-hangzhou.aliyuncs.com/train-data/",
            labels={"DlcJobExampleTrainDataset": "True"},
            mount_path="/ml/input/data/train/",
        )
        self.assertIsNotNone(dataset.id)
        self.assertIsNotNone(dataset.create_time)

        dataset2 = Dataset.get(dataset.id)

        self.assertEqual(dataset2.create_time, dataset.create_time)
        self.assertEqual(dataset2.id, dataset.id)
        datasets = Dataset.list()
        self.assertTrue(len(datasets) >= 1)
