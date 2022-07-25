from __future__ import absolute_import

from pai.api.common import DataSourceType
from pai.api.dlc import DlcClient
from pai.common.utils import random_str
from pai.core.session import Session
from tests.integration import BaseIntegTestCase


class TestDlcAPI(BaseIntegTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestDlcAPI, cls).setUpClass()
        session = Session.current()
        cls.client = session.dlc_client  # type: DlcClient
        cls.workspace_id = session.workspace.id

    def test_dataset(self):
        dataset_id = self.client.create_data_source(
            name="tmp-test-api-{}".format(random_str(8)),
            data_source_type=DataSourceType.OSS,
            path="oss://lq-pai-test-1/example-dataset",
            mount_path="/mnt/data",
        )
        self.assertIsNotNone(dataset_id)
        self.client.delete_data_source(dataset_id)

    def test_code_source(self):
        code_source_id = self.client.create_code_source(
            code_repo="https://github.com/mit-pdos/xv6-public.git",
            # code_branch="master",
            name="tmp-test-api-{}".format(random_str(8)),
        )
        self.client.delete_code_source(code_source_id)
