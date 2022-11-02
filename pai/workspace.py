from __future__ import absolute_import

from collections import namedtuple
from typing import List, Sequence, Union

from pai.api.workspace_api import WorkspaceAPI
from pai.common.consts import DEFAULT_PAGE_SIZE
from pai.core.session import Session, get_default_session
from pai.decorator import config_default_session
from pai.entity.base import EntityBaseMixin, make_resource_iterator
from pai.schema.workspace_schema import WorkspaceMemberSchema, WorkspaceSchema

SubUserInfo = namedtuple("SubUserInfo", ["user_id", "name"])


class WorkspaceRole(object):
    Owner = "workspace_owner"
    Admin = "workspace_admin"
    Developer = "workspace_developer"
    Viewer = "workspace_viewer"


class Workspace(EntityBaseMixin):
    """Workspace manage a group of resource in PAI service.

    setup_default_session(workspace_name="example_workspace_name")

    """

    _schema_cls = WorkspaceSchema

    def __init__(
        self,
        name: str,
        display_name: str = None,
        is_default: str = None,
        creator_id: str = None,
        desc: str = None,
        status: str = None,
        env_types: List[str] = None,
        session: Session = None,
        **kwargs,
    ):
        """Workspace constructor.

        Args:
            id (str): Unique Identifier of the workspace.
            name (str): Unique name of workspace.
            creator_id (str): User id of workspace creator.
            desc:
        """
        super(Workspace, self).__init__(session)
        self.name = name
        self.creator_id = creator_id
        self.display_name = display_name
        self.desc = desc
        self.status = status
        self.env_types = env_types
        self.is_default = is_default

        # ReadOnly Fields.
        self._workspace_id = kwargs.pop("workspace_id", None)
        self._create_time = kwargs.pop("create_time", None)
        self._modified_time = kwargs.pop("modified_time", None)

    @property
    def id(self) -> str:
        return self._workspace_id

    @property
    def create_time(self) -> str:
        return self._create_time

    @property
    def modified_time(self):
        return self._modified_time

    def __str__(self):
        return "Workspace:%s:%s:%s" % (self.name, self.display_name, self.id)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.id == other.id

    @property
    def workspace_api(self) -> WorkspaceAPI:
        return self.session.workspace_api

    @classmethod
    @config_default_session
    def get(cls, workspace_id, session=None):
        """Get a Workspace instance by workspace_id.

        Args:
            workspace_id: Id of the workspace.
            session: Session used for get the workspace client.

        Returns:
            Workspace: None if specific workspace not exists.
        """
        sess = session or get_default_session()
        resp = sess.workspace_api.get(workspace_id=workspace_id)
        return cls.from_api_object(resp, session=session)

    @classmethod
    @config_default_session
    def get_by_name(cls, name, session=None) -> "Workspace":
        name = name.strip()
        if not name:
            raise ValueError("Please provide non-empty workspace name.")

        iterator = make_resource_iterator(cls.list, name=name, session=session)
        workspace = next(
            (ws for ws in iterator if ws.name == name),
            None,
        )

        return workspace

    @classmethod
    @config_default_session
    def list(
        cls,
        name: str = None,
        sort_by: str = None,
        order: str = None,
        session: Session = None,
        page_number: int = 1,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> List["Workspace"]:
        resp = session.workspace_api.list(
            name=name,
            sort_by=sort_by,
            order=order,
            page_number=page_number,
            page_size=page_size,
        )
        return [Workspace.from_api_object(item, session=session) for item in resp]

    @classmethod
    @config_default_session
    def create(cls, name, display_name=None, description=None, session=None):
        workspace_id = session.workspace_api.create(
            name=name, display_name=display_name, description=description
        )

        return cls.get(workspace_id, session=session)

    def list_members(
        self,
        member_name: str = None,
        role: Union[str, List[str]] = None,
        page_number=1,
        page_size=DEFAULT_PAGE_SIZE,
    ):

        if isinstance(role, str):
            role = [role]

        res = self.session.workspace_api.list_members(
            workspace_id=self._workspace_id,
            member_name=member_name,
            page_number=page_number,
            page_size=page_size,
            roles=role,
        )

        return [WorkspaceMember.from_api_object(item) for item in res]

    def add_member(
        self, user_id: str, role: Union[str, Sequence[str]]
    ) -> "WorkspaceMember":
        if not isinstance(role, Sequence):
            roles = [role]
        else:
            roles = role
        self.session.workspace_api.add_member(
            workspace_id=self._workspace_id,
            user_id=user_id,
            roles=roles,
        )

        return self.get_member(user_id=user_id)

    def get_member(self, user_id: str) -> "WorkspaceMember":
        """Get workspace member with user_id.

        Args:
            user_id: Aliyun user id of the workspace member.

        Returns:
            WorkspaceMember:

        """
        res = self.workspace_api.get_member(
            workspace_id=self._workspace_id,
            user_id=user_id,
        )
        return WorkspaceMember.from_api_object(res, session=self.session)

    def remove_member(self, member_id: Union[str, List[str]]) -> None:
        """Remove a workspace member

        Args:
            member_id:

        Returns:

        """

        if isinstance(member_id, str):
            member_id = [member_id]

        self.workspace_api.delete_members(
            workspace_id=self._workspace_id, member_ids=member_id
        )


class WorkspaceMember(EntityBaseMixin):
    """Class represent workspace member."""

    _schema_cls = WorkspaceMemberSchema

    def __init__(
        self,
        user_id,
        roles,
        member_id=None,
        name=None,
        workspace_id=None,
        display_name=None,
        session=None,
        **kwargs,
    ):
        super(WorkspaceMember, self).__init__(session=session)
        self.user_id = user_id
        self.roles = roles
        self.name = name
        self.id = id
        self.workspace_id = workspace_id
        self.display_name = display_name
        self.member_id = member_id
        self._create_time = kwargs.get("create_time")

    @property
    def create_time(self):
        return self._create_time

    def __repr__(self):
        return "WorkspaceMember:%s:%s:%s" % (self.id, self.user_id, self.name)
