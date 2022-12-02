from __future__ import absolute_import

from pai.common.utils import iter_with_limit
from pai.workspace import Workspace
from tests.integration import BaseIntegTestCase


class TestWorkspace(BaseIntegTestCase):

    default_workspace = None

    @classmethod
    def setUpClass(cls):
        super(TestWorkspace, cls).setUpClass()
        cls.default_workspace = Workspace.get(cls.pai_service_config.workspace_id)

    def test_list_workspace(self):
        self.assertIsNotNone(self.default_workspace)
        limit = 10
        workspaces = [ws for ws in iter_with_limit(Workspace.list(), limit)]
        self.assertTrue(0 < len(workspaces) <= limit)
        ws = Workspace.list()[0]
        ws_v2 = Workspace.get(ws.id)
        self.assertEqual(ws_v2, ws)

    def test_get_by_name(self):
        ws = Workspace.get_by_name(name=self.default_workspace.name)
        self.assertEqual(ws.name, self.default_workspace.name)
        self.assertEqual(ws.id, self.default_workspace.id)
        self.assertTrue(len(ws.list_members()) > 0)

    @classmethod
    def test_workspace(cls):
        pass
