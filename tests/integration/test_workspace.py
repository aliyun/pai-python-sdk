from __future__ import absolute_import

from pai.common.utils import iter_with_limit
from pai.core.workspace import Workspace
from tests.integration import BaseIntegTestCase


class TestWorkspace(BaseIntegTestCase):

    default_workspace = None

    @classmethod
    def setUpClass(cls):
        super(TestWorkspace, cls).setUpClass()
        cls.default_workspace = Workspace.get(cls.pai_service_config.workspace_id)

    def test_list_sub_users(self):
        sub_users = list(
            Workspace.list_sub_users(exclude_workspace_id=self.default_workspace.id)
        )
        self.assertTrue(len(sub_users) > 0)

    @classmethod
    def get_ws_member_count(cls, ws):
        return len([member for member in ws.list_member()])

    def test_workspace_api(self):
        self.assertIsNotNone(self.default_workspace)
        limit = 10
        workspaces = [ws for ws in iter_with_limit(Workspace.list(), limit)]
        self.assertTrue(0 < len(workspaces) <= limit)

    def test_list_members(self):
        self.assertTrue(
            len([member for member in self.default_workspace.list_member()]) > 0
        )

    def test_get_tenant(self):
        self.assertIsNotNone(self.default_workspace.get_tenant())

    def test_get_compute_engine(self):
        engines = list(
            iter_with_limit(self.default_workspace.list_compute_engines(), 10)
        )
        self.assertTrue(len(engines) >= 0)

    def test_get_resource_groups(self):
        self.assertTrue(len(Workspace.list_resource_groups()) > 0)

    # def test_list_commodities(self):
    #     print(Workspace.list_commodities())

    def test_get_by_name(self):
        ws = Workspace.get_by_name(name=self.default_workspace.name)
        self.assertEqual(ws, self.default_workspace)
