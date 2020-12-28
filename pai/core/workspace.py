from __future__ import absolute_import

from collections import namedtuple
from datetime import datetime
from pai.core.engine import ComputeEngineType, ComputeEngine, ResourceGroup

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

    def __init__(self, id, name, creator_id, alias=None, desc=None):
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
        self.alias = alias
        self.desc = desc

    def __str__(self):
        return "Workspace:%s:%s:%s" % (self.name, self.alias, self.id)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.id == other.id

    @classmethod
    def get_tenant(cls):
        return Tenant.create()

    @classmethod
    def _get_service_client(cls):
        from pai.core.session import get_default_session

        session = get_default_session()
        return session.ws_client

    @classmethod
    def deserialize(cls, obj_dict):
        return cls(
            id=obj_dict["WorkspaceId"],
            name=obj_dict["WorkspaceName"],
            desc=obj_dict["Description"],
            creator_id=obj_dict["Creator"],
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
    def get(cls, ws_id):
        ws = cls._get_service_client().get(workspace_id=ws_id)
        print(ws)
        return cls.deserialize(ws["Data"])

    @classmethod
    def get_by_name(cls, name):
        name = name.strip()
        if not name:
            raise ValueError("Please provide non-empty workspace name.")

        ws_info = next(
            (
                ws
                for ws in cls._get_service_client().list(name=name)
                if ws["WorkspaceName"] == name
            ),
            None,
        )
        if not ws_info:
            return
        return cls.deserialize(ws_info)

    @classmethod
    def list(cls, name=None, sorted_by=None, sorted_sequence=None):
        for ws in cls._get_service_client().list(
            name=name, sorted_by=sorted_by, sorted_sequence=sorted_sequence
        ):
            yield cls.deserialize(ws)

    @classmethod
    def create(cls, name, alias=None, desc=None):
        r = cls._get_service_client().deserialize(
            name=name, alias=alias, description=desc
        )
        print(r)
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

    def list_compute_engines(
        self, name=None, engine_type=ComputeEngineType.MaxCompute, **kwargs
    ):
        obj_dicts = self._get_service_client().list_compute_engines(
            name=name, workspace_id=self.id, engine_type=engine_type, **kwargs
        )

        for obj_dict in obj_dicts:
            yield ComputeEngine.deserialize(obj_dict)

    @classmethod
    def list_resource_groups(cls):
        tenant = cls.get_tenant()
        rs = cls._get_service_client().list_resource_groups(tenant.id)
        return [ResourceGroup.deserialize(obj_dict) for obj_dict in rs["Data"]]

    @classmethod
    def list_commodities(cls):
        return cls._get_service_client().list_commodities()


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


class Tenant(object):
    def __init__(self, tenant_id, resource_limits):
        self.id = tenant_id
        self.resource_limits = resource_limits

    def __str__(self):
        return "%s:%s" % (type(self), self.id)

    @classmethod
    def deserialize(cls, obj_dict):
        return cls(
            tenant_id=obj_dict["TenantId"], resource_limits=obj_dict["ResourceLimits"]
        )

    @classmethod
    def _get_service_client(cls):
        from pai.core.session import get_default_session

        session = get_default_session()
        return session.ws_client

    @classmethod
    def create(cls):
        client = cls._get_service_client()
        rs = client.create_tenant()
        return cls.deserialize(rs["Data"])
