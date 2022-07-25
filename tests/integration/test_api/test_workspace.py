from __future__ import absolute_import

from pai.core.session import Session
from tests.integration import BaseIntegTestCase

from pai.api.common import (
    ResourceAccessibility,
    DataSourceType,
    FileProperty,
    PAI_DLC_INTEGRATED_WITH_WORKSPACE_FEATURE,
)
from pai.common.utils import random_str


class TestWorkspaceAPI(BaseIntegTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestWorkspaceAPI, cls).setUpClass()
        session = Session.current()
        cls.client = session.ws_client
        cls.workspace_id = session.workspace.id

    def test_dataset(self):
        dataset_id = self.client.create_dataset(
            accessibility=ResourceAccessibility.PUBLIC,
            name="tmp-test-ws-api-{}".format(random_str(8)),
            data_source_type=DataSourceType.OSS,
            property=FileProperty.FILE,
            uri="oss://lq-pai-test-1/example-dataset",
            workspace_id=self.workspace_id,
        )
        self.assertIsNotNone(dataset_id)
        self.client.delete_dataset(dataset_id)

    def test_list_features(self):
        self.client.list_feature(names=PAI_DLC_INTEGRATED_WITH_WORKSPACE_FEATURE)

    def test_code_source(self):
        pass
