from __future__ import absolute_import

from collections import namedtuple

SubUserInfo = namedtuple(
    "SubUserInfo", ["user_id", "name"]
)


class WorkspaceRole(object):
    Owner = "workspace_owner"
    Admin = "workspace_admin"
    Developer = "workspace_developer"
    Viewer = "workspace_viewer"


class Workspace(object):
    """Workspace manage a group of resource in PAI service.

    setup_default_session(workspace_name="example_workspace_name")

    """

    def __init__(self, id, name, creator_id, desc=None):
        """Workspace constructor.

        Args:
            id (str): Unique Identifier of the workspace.
            name (str): Unique name of workspace.
            creator_id (str): User id of workspace creator.
            desc:
        """
        self._id = id
        self._name = name
        self._creator_id = creator_id
        self._desc = desc

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def creator_id(self):
        return self._creator_id

    @property
    def desc(self):
        return self._desc

    def __repr__(self):
        return 'Workspace:%s:%s' % (self._name, self._id)

    @classmethod
    def _get_workspace_client(cls):
        from pai.core.session import get_default_session
        session = get_default_session()
        return session.ws_client

    @classmethod
    def get_or_create_default_workspace(cls):
        data = cls._get_workspace_client().get_default_workspace()
        return cls._load_from_dict(data["Data"])

    @classmethod
    def _load_from_dict(cls, d):
        return cls(id=d["WorkspaceId"],
                   name=d["WorkspaceName"],
                   desc=d["Description"],
                   creator_id=d["Creator"])

    def list_excluded_user_info(self):
        for sub_user_info in self._get_workspace_client().list_sub_users(
                exclude_workspace_id=self.id):
            yield SubUserInfo(
                user_id=sub_user_info["SubUserId"],
                name=sub_user_info["SubUserName"],
            )

    @classmethod
    def get(cls, ws_id):
        ws = cls._get_workspace_client().get(workspace_id=ws_id)
        return cls._load_from_dict(ws["Data"])

    @classmethod
    def get_by_name(cls, name):
        if not name:
            raise ValueError("Please given validate workspace name.")

        ws_info = next(cls._get_workspace_client().list(name=name), None)
        if not ws_info:
            return
        return cls._load_from_dict(ws_info)

    @classmethod
    def list(cls, name=None, sorted_by=None, sorted_sequence=None):
        for ws in cls._get_workspace_client().list(name=name, sorted_by=sorted_by,
                                                   sorted_sequence=sorted_sequence):
            yield cls._load_from_dict(ws)

    @classmethod
    def create(cls, name, desc=None):
        r = cls._get_workspace_client().create(name=name, description=desc)
        ws_id = r["Data"]["WorkspaceId"]
        return cls.get(ws_id)

    def list_member(self, name=None, role=None):
        infos = self._get_workspace_client().list_member(workspace_id=self.id, name=name,
                                                         role=role)
        for info in infos:
            yield WorkspaceMember.load_from_dict(info)

    def add_member(self, user_id, role):
        if not isinstance(role, (list, tuple)):
            roles = [role]
        else:
            roles = role
        resp = self._get_workspace_client().add_member(self.id, {
            "UserId": user_id,
            "Roles": roles,
        })
        member_info = resp["Data"][0]
        return WorkspaceMember.load_from_dict(member_info)

    def delete_member(self, member_id):
        self._get_workspace_client().delete_member(self.id, member_id)


class WorkspaceMember(object):

    def __init__(self, id, user_id, roles, name=None, workspace_id=None, display_name=None):
        self.user_id = user_id
        self.roles = roles
        self.name = name
        self.id = id
        self.workspace_id = workspace_id
        self.display_name = display_name

    def __repr__(self):
        return "WorkspaceMember:%s:%s:%s" % (self.id, self.user_id, self.name)

    def get(self, member_id):
        return

    @classmethod
    def load_from_dict(cls, d):
        return cls(
            user_id=d["UserId"],
            id=d["MemberId"],
            name=d["MemberName"],
            display_name=d["DisplayName"],
            roles=d["Roles"],
        )
