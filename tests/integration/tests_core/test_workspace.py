from __future__ import absolute_import

from pai.core.workspace import Workspace
from pai.common.utils import iter_with_limit
from tests.integration import BaseIntegTestCase


class TestWorkspace(BaseIntegTestCase):
    @classmethod
    def get_ws_member_count(cls, ws):
        return len([member for member in ws.list_member()])

    @classmethod
    def setUpClass(cls):
        super(TestWorkspace, cls).setUpClass()
        cls.workspace = Workspace.get_or_create_default_workspace()

    def test_get_default(self):
        ws = Workspace.get_or_create_default_workspace()
        self.assertIsNotNone(ws)
        ws2 = Workspace.get_or_create_default_workspace()
        self.assertTrue(ws.id == ws2.id)

    def test_create_and_get_workspace(self):
        self.assertTrue(self.workspace is not None)
