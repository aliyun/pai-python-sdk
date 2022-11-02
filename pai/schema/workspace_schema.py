from marshmallow import fields, post_load

from pai.schema.base import BaseAPIResourceSchema


class WorkspaceSchema(BaseAPIResourceSchema):
    """
    {
            "WorkspaceName":"DemoChanel",
            "WorkspaceId":"268637",
            "Status":"ENABLED",
            "IsDefault":false,
            "Description":"demo dec",
            "AdminNames":[
                    "pai_test_1@test.aliyunid.com",
                    "mingmeng"
            ],
            "Creator":"1157703270994901",
            "GmtModifiedTime":"2022-08-31T06:15:09.000Z",
            "DisplayName":"DemoChanel",
            "ExtraInfos":{
                    "TenantId":"428674451108098"
            },
            "GmtCreateTime":"2022-08-31T06:15:06.000Z",
            "EnvTypes":[
                    "prod"
            ]
    },
    """

    FieldNameMapping = {
        "GmtCreateTime": "create_time",
        "GmtModifyTime": "modified_time",
        "Creator": "creator_id",
        "WorkspaceName": "name",
    }

    name = fields.Str()
    status = fields.Str()
    is_default = fields.Bool()
    description = fields.Str()
    admin_names = fields.List(fields.Str)
    env_types = fields.List(fields.Str)
    creator_id = fields.Str()
    display_name = fields.Str()
    extra_infos = fields.Dict()

    create_time = fields.DateTime(load_only=True)
    modified_time = fields.DateTime(load_only=True)
    workspace_id = fields.Str(load_only=True)

    @post_load
    def _make(self, data, **kwargs):
        from pai.workspace import Workspace

        return self.make_or_reload(instance_cls=Workspace, data=data)


class WorkspaceMemberSchema(BaseAPIResourceSchema):
    """
    Example API Object:

    {
                    "MemberId":"268637-242255525452045138",
                    "UserId":"242255525452045138",
                    "DisplayName":"mingmeng",
                    "Roles":[
                            "PAI.WorkspaceAdmin"
                    ],
                    "MemberName":"mingmeng",
                    "GmtCreateTime":"2021-07-05T02:27:25.000Z",
                    "AccountName":"mingmeng"
            },
    """

    FieldNameMapping = {
        "GmtCreateTime": "create_time",
        "GmtModifyTime": "modified_time",
        "MemberName": "name",
    }

    name = fields.Str()
    display_name = fields.Str()
    account_name = fields.Str()

    roles = fields.List(fields.Str)
    user_id = fields.Str()
    member_id = fields.Str()

    create_time = fields.DateTime(load_only=True)

    @post_load
    def _make(self, data, **kwargs):
        from pai.workspace import WorkspaceMember

        return self.make_or_reload(instance_cls=WorkspaceMember, data=data)
