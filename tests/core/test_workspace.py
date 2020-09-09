from __future__ import absolute_import

import random

from pai.workspace import Workspace, WorkspaceRole
from tests import BaseTestCase


class TestWorkspace(BaseTestCase):

    @classmethod
    def create_workspace(cls, name=None, desc=None):
        name = name or "test_workspace_%s" % random.randint(1000000, 9999999)
        return Workspace.create(name=name, desc=desc)

    @classmethod
    def get_sub_users(cls, workspace):
        return [sub_user for sub_user in
                workspace.list_excluded_user_info()]

    @classmethod
    def get_ws_member_count(cls, ws):
        return len([member for member in ws.list_member()])

    @classmethod
    def setUpClass(cls):
        super(TestWorkspace, cls).setUpClass()
        cls.workspace = cls.create_workspace()
        cls.sub_users = cls.get_sub_users(cls.workspace)

    def test(self):
        ws = self.workspace
        print(ws.creator)
        pass

    def test_list_workspace(self):
        self.create_workspace()
        self.create_workspace()
        max_iter = 100
        count = 0
        for _ in Workspace._get_workspace_client().list():
            count += 1
            if count >= max_iter:
                break
        self.assertTrue(count >= 2)

    def test_create_and_get_workspace(self):
        self.assertTrue(self.workspace is not None)

    def test_list_member(self):
        count = 0
        for _ in self.workspace.list_member():
            count += 1
        self.assertTrue(count >= 1)

    def test_add_member(self):
        if not self.sub_users:
            return

        ws = self.create_workspace()
        sub_user_count = len(self.sub_users)
        for sub_user in self.sub_users:
            ws.add_member(sub_user.user_id, role=WorkspaceRole.Developer)

        members = [member for member in ws.list_member(role=WorkspaceRole.Developer)]
        self.assertTrue(len(members) == sub_user_count)

        delete_member = members[0]
        ws.delete_member(delete_member.id)
        members = [member for member in ws.list_member(role=WorkspaceRole.Developer)]
        self.assertTrue(len(members) == sub_user_count - 1)
