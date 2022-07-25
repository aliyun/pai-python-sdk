from __future__ import absolute_import

from collections import namedtuple
from datetime import datetime


SubUserInfo = namedtuple("SubUserInfo", ["user_id", "name"])


class WorkspaceRole(object):
    Owner = "workspace_owner"
    Admin = "workspace_admin"
    Developer = "workspace_developer"
    Viewer = "workspace_viewer"


class Workspace(object):
    """Workspace manage a group of resource in PAI service.

    setup_default_session(workspace_name="example_workspace_name")

    """

    def __init__(
        self,
        id,
        name,
        creator_id,
        display_name=None,
        desc=None,
        status=None,
        resource_count=None,
        env_types=None,
    ):
        """Workspace constructor.

        Args:
            id (str): Unique Identifier of the workspace.
            name (str): Unique name of workspace.
            creator_id (str): User id of workspace creator.
            desc:
        """
        self.id = id
        self.name = name
        self.creator_id = creator_id
        self.display_name = display_name
        self.desc = desc
        self.status = status
        self.resource_count = resource_count
        self.env_types = env_types

    def __str__(self):
        return "Workspace:%s:%s:%s" % (self.name, self.display_name, self.id)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.id == other.id

    @classmethod
    def _get_service_client(cls):
        from pai.core.session import Session

        session = Session.current()
        return session.ws_client

    @classmethod
    def deserialize(cls, obj_dict):
        return cls(
            id=obj_dict["WorkspaceId"],
            name=obj_dict["WorkspaceName"],
            display_name=obj_dict.get("DisplayName"),
            status=obj_dict.get("Status"),
            desc=obj_dict.get("Description"),
            creator_id=obj_dict.get("Creator"),
            resource_count=obj_dict.get("ResourceCount"),
            env_types=obj_dict.get("EnvTypes"),
            # admin_names=obj_dict["AdminNames"],
        )

    @classmethod
    def list_sub_users(cls, exclude_workspace_id=None):
        return [
            SubUserInfo(
                user_id=sub_user_info["SubUserId"], name=sub_user_info["SubUserName"]
            )
            for sub_user_info in cls._get_service_client().list_sub_users(
                exclude_workspace_id=exclude_workspace_id
            )["Data"]
        ]

    @classmethod
    def get(cls, workspace_id, session=None):
        """Get a Workspace instance by workspace_id.

        Args:
            workspace_id: Id of the workspace.
            session: Session used for get the workspace client.

        Returns:
            Workspace: None if specific workspace not exists.
        """
        from pai.core import Session

        sess = session or Session.current()
        resp = sess.ws_client.get_workspace(workspace_id=workspace_id)
        return cls.deserialize(resp)

    @classmethod
    def get_by_name(cls, name):
        name = name.strip()
        if not name:
            raise ValueError("Please provide non-empty workspace name.")

        ws_info = next(
            (
                ws
                for ws in cls._get_service_client().list_workspace_generator(
                    workspace_name=name, page_size=1
                )
                if ws["WorkspaceName"] == name
            ),
            None,
        )
        if not ws_info:
            return
        return cls.deserialize(ws_info)

    @classmethod
    def list(cls, name=None, sort_by=None, order=None):
        for ws in cls._get_service_client().list_workspace_generator(
            workspace_name=name,
            sort_by=sort_by,
            order=order,
        ):
            yield cls.deserialize(ws)

    @classmethod
    def create(cls, name, alias=None, desc=None):
        r = cls._get_service_client().deserialize(
            name=name, alias=alias, description=desc
        )
        ws_id = r["Data"]["WorkspaceId"]
        return cls.get(ws_id)

    def list_member(self, name=None, role=None):
        infos = self._get_service_client().list_member(
            workspace_id=self.id, name=name, role=role
        )
        for info in infos:
            yield WorkspaceMember.deserialize(info)

    def add_member(self, user_id, role):
        if not isinstance(role, (list, tuple)):
            roles = [role]
        else:
            roles = role
        resp = self._get_service_client().add_member(
            self.id,
            {
                "UserId": user_id,
                "Roles": roles,
            },
        )
        member_info = resp["Data"][0]
        return WorkspaceMember.deserialize(member_info)

    def delete_member(self, member_id):
        self._get_service_client().delete_member(self.id, member_id)


class WorkspaceMember(object):
    def __init__(
        self,
        id,
        user_id,
        roles,
        name=None,
        workspace_id=None,
        alias=None,
        create_time=None,
    ):
        self.user_id = user_id
        self.roles = roles
        self.name = name
        self.id = id
        self.workspace_id = workspace_id
        self.alias = alias
        self.create_time = create_time

    def __repr__(self):
        return "WorkspaceMember:%s:%s:%s" % (self.id, self.user_id, self.name)

    def get(self, member_id):
        return

    @classmethod
    def deserialize(cls, obj_dict):
        return cls(
            user_id=obj_dict["UserId"],
            id=obj_dict["MemberId"],
            name=obj_dict["MemberName"],
            alias=obj_dict["MemberAlias"],
            roles=obj_dict["Roles"],
            create_time=datetime.fromtimestamp(int(obj_dict["CreateTime"]) / 1000)
            if obj_dict.get("CreateTime")
            else None,
        )
