from __future__ import absolute_import

from pai.core.workspace import Workspace
from pai.utils import iter_with_limit
from tests import BaseTestCase


class TestWorkspace(BaseTestCase):

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

    def test_list_workspace(self):
        res = list(iter_with_limit(Workspace.list(), 2))
        self.assertTrue(len(res) >= 1)

    def test_create_and_get_workspace(self):
        self.assertTrue(self.workspace is not None)

    # def test_add_member(self):
    #     if not self.sub_users:
    #         return
    #
    #     ws = Workspace.get_or_create_default_workspace()
    #     sub_user_count = len(self.sub_users)
    #     for sub_user in self.sub_users:
    #         ws.add_member(sub_user.user_id, role=WorkspaceRole.Developer)
    #
    #     members = [member for member in ws.list_member(role=WorkspaceRole.Developer)]
    #     self.assertTrue(len(members) == sub_user_count)
    #
    #     delete_member = members[0]
    #     ws.delete_member(delete_member.id)
    #     members = [member for member in ws.list_member(role=WorkspaceRole.Developer)]
    #     self.assertTrue(len(members) == sub_user_count - 1)
