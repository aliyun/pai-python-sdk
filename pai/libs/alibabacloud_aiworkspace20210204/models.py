# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel
from Tea.converter import TeaConverter


class AddMemberRoleResponseBody(TeaModel):
    def __init__(self, request_id=None):
        # 请求 id
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class AddMemberRoleResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: AddMemberRoleResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = AddMemberRoleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class AddWorkspaceQuotaRequest(TeaModel):
    def __init__(self, quota_type=None, mode=None, product_code=None):
        # 产品类型，  支持PAI，MaxCompute，
        self.quota_type = TeaConverter.to_unicode(quota_type)  # type: unicode
        # 模式  isolate 预付费  share 后付费  develop 开发模式
        self.mode = TeaConverter.to_unicode(mode)  # type: unicode
        # 产品代码
        self.product_code = TeaConverter.to_unicode(product_code)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.quota_type is not None:
            result['QuotaType'] = self.quota_type
        if self.mode is not None:
            result['Mode'] = self.mode
        if self.product_code is not None:
            result['ProductCode'] = self.product_code
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('QuotaType') is not None:
            self.quota_type = m.get('QuotaType')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        if m.get('ProductCode') is not None:
            self.product_code = m.get('ProductCode')
        return self


class AddWorkspaceQuotaResponseBody(TeaModel):
    def __init__(self, request_id=None):
        # 请求 id
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class AddWorkspaceQuotaResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: AddWorkspaceQuotaResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = AddWorkspaceQuotaResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateMemberRequestMembers(TeaModel):
    def __init__(self, user_id=None, roles=None):
        # 用户 id
        self.user_id = TeaConverter.to_unicode(user_id)  # type: unicode
        # 角色列表
        self.roles = roles  # type: list[unicode]

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.roles is not None:
            result['Roles'] = self.roles
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('Roles') is not None:
            self.roles = m.get('Roles')
        return self


class CreateMemberRequest(TeaModel):
    def __init__(self, members=None):
        # 用户列表
        self.members = members  # type: list[CreateMemberRequestMembers]

    def validate(self):
        if self.members:
            for k in self.members:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Members'] = []
        if self.members is not None:
            for k in self.members:
                result['Members'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        self.members = []
        if m.get('Members') is not None:
            for k in m.get('Members'):
                temp_model = CreateMemberRequestMembers()
                self.members.append(temp_model.from_map(k))
        return self


class CreateMemberResponseBodyMembers(TeaModel):
    def __init__(self, user_id=None, roles=None, display_name=None, member_id=None):
        # 用户 id
        self.user_id = TeaConverter.to_unicode(user_id)  # type: unicode
        # 角色列表
        self.roles = roles  # type: list[unicode]
        # 成员显示名
        self.display_name = TeaConverter.to_unicode(display_name)  # type: unicode
        # 成员 id
        self.member_id = TeaConverter.to_unicode(member_id)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.roles is not None:
            result['Roles'] = self.roles
        if self.display_name is not None:
            result['DisplayName'] = self.display_name
        if self.member_id is not None:
            result['MemberId'] = self.member_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('Roles') is not None:
            self.roles = m.get('Roles')
        if m.get('DisplayName') is not None:
            self.display_name = m.get('DisplayName')
        if m.get('MemberId') is not None:
            self.member_id = m.get('MemberId')
        return self


class CreateMemberResponseBody(TeaModel):
    def __init__(self, request_id=None, members=None):
        # 请求 id
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        # 成员列表
        self.members = members  # type: list[CreateMemberResponseBodyMembers]

    def validate(self):
        if self.members:
            for k in self.members:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Members'] = []
        if self.members is not None:
            for k in self.members:
                result['Members'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.members = []
        if m.get('Members') is not None:
            for k in m.get('Members'):
                temp_model = CreateMemberResponseBodyMembers()
                self.members.append(temp_model.from_map(k))
        return self


class CreateMemberResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: CreateMemberResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateMemberResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateWorkspaceRequest(TeaModel):
    def __init__(self, workspace_name=None, description=None, display_name=None, env_types=None):
        # 名字 3-23 个字符, 需要字母开头，只能包含字母下划线和数字，region内唯一
        self.workspace_name = TeaConverter.to_unicode(workspace_name)  # type: unicode
        # 描述，最多80个字符
        self.description = TeaConverter.to_unicode(description)  # type: unicode
        # 显示名称
        self.display_name = TeaConverter.to_unicode(display_name)  # type: unicode
        # 环境列表
        self.env_types = env_types  # type: list[unicode]

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.workspace_name is not None:
            result['WorkspaceName'] = self.workspace_name
        if self.description is not None:
            result['Description'] = self.description
        if self.display_name is not None:
            result['DisplayName'] = self.display_name
        if self.env_types is not None:
            result['EnvTypes'] = self.env_types
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('WorkspaceName') is not None:
            self.workspace_name = m.get('WorkspaceName')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('DisplayName') is not None:
            self.display_name = m.get('DisplayName')
        if m.get('EnvTypes') is not None:
            self.env_types = m.get('EnvTypes')
        return self


class CreateWorkspaceResponseBody(TeaModel):
    def __init__(self, request_id=None, workspace_id=None):
        # 请求 id
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        # 工作空间 id
        self.workspace_id = TeaConverter.to_unicode(workspace_id)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class CreateWorkspaceResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: CreateWorkspaceResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateWorkspaceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateWorkspaceResourceRequestResourcesQuotas(TeaModel):
    def __init__(self, name=None, product_code=None, quota_type=None, mode=None, spec=None, card_type=None):
        # 配额名称
        self.name = TeaConverter.to_unicode(name)  # type: unicode
        # 商品 code
        self.product_code = TeaConverter.to_unicode(product_code)  # type: unicode
        # 产品类型， 支持PAI，MaxCompute
        self.quota_type = TeaConverter.to_unicode(quota_type)  # type: unicode
        # 模式 isolate 预付费 share 后付费 develop 开发模式
        self.mode = TeaConverter.to_unicode(mode)  # type: unicode
        # 规格描述
        self.spec = TeaConverter.to_unicode(spec)  # type: unicode
        # 卡类型，支持cpu、gpu
        self.card_type = TeaConverter.to_unicode(card_type)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.product_code is not None:
            result['ProductCode'] = self.product_code
        if self.quota_type is not None:
            result['QuotaType'] = self.quota_type
        if self.mode is not None:
            result['Mode'] = self.mode
        if self.spec is not None:
            result['Spec'] = self.spec
        if self.card_type is not None:
            result['CardType'] = self.card_type
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('ProductCode') is not None:
            self.product_code = m.get('ProductCode')
        if m.get('QuotaType') is not None:
            self.quota_type = m.get('QuotaType')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        if m.get('Spec') is not None:
            self.spec = m.get('Spec')
        if m.get('CardType') is not None:
            self.card_type = m.get('CardType')
        return self


class CreateWorkspaceResourceRequestResources(TeaModel):
    def __init__(self, name=None, product_type=None, env_type=None, workspace_id=None, is_default=None, quotas=None,
                 spec=None, group_name=None):
        # 资源名 长度需要在3到27个字符 region内唯一
        self.name = TeaConverter.to_unicode(name)  # type: unicode
        # 产品类型， 支持PAI，MaxCompute
        self.product_type = TeaConverter.to_unicode(product_type)  # type: unicode
        # 环境， 支持dev（开发）、prod（生产）
        self.env_type = TeaConverter.to_unicode(env_type)  # type: unicode
        # 所属的工作空间 id
        self.workspace_id = TeaConverter.to_unicode(workspace_id)  # type: unicode
        # 是否默认资源 每个类型都有一个默认的资源
        self.is_default = is_default  # type: bool
        self.quotas = quotas  # type: list[CreateWorkspaceResourceRequestResourcesQuotas]
        # 对于MaxCompute是个json，有如下key： Endpoint Project
        self.spec = TeaConverter.to_unicode(spec)  # type: unicode
        # 分组名，主账户内唯一 一个 GroupName 下可能有一个 dev 资源和一个 prod 资源
        self.group_name = TeaConverter.to_unicode(group_name)  # type: unicode

    def validate(self):
        if self.quotas:
            for k in self.quotas:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.product_type is not None:
            result['ProductType'] = self.product_type
        if self.env_type is not None:
            result['EnvType'] = self.env_type
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        if self.is_default is not None:
            result['IsDefault'] = self.is_default
        result['Quotas'] = []
        if self.quotas is not None:
            for k in self.quotas:
                result['Quotas'].append(k.to_map() if k else None)
        if self.spec is not None:
            result['Spec'] = self.spec
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('ProductType') is not None:
            self.product_type = m.get('ProductType')
        if m.get('EnvType') is not None:
            self.env_type = m.get('EnvType')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        if m.get('IsDefault') is not None:
            self.is_default = m.get('IsDefault')
        self.quotas = []
        if m.get('Quotas') is not None:
            for k in m.get('Quotas'):
                temp_model = CreateWorkspaceResourceRequestResourcesQuotas()
                self.quotas.append(temp_model.from_map(k))
        if m.get('Spec') is not None:
            self.spec = m.get('Spec')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        return self


class CreateWorkspaceResourceRequest(TeaModel):
    def __init__(self, resources=None):
        # 资源列表
        self.resources = resources  # type: list[CreateWorkspaceResourceRequestResources]

    def validate(self):
        if self.resources:
            for k in self.resources:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Resources'] = []
        if self.resources is not None:
            for k in self.resources:
                result['Resources'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        self.resources = []
        if m.get('Resources') is not None:
            for k in m.get('Resources'):
                temp_model = CreateWorkspaceResourceRequestResources()
                self.resources.append(temp_model.from_map(k))
        return self


class CreateWorkspaceResourceResponseBodyResources(TeaModel):
    def __init__(self, id=None):
        # 资源Id
        self.id = TeaConverter.to_unicode(id)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class CreateWorkspaceResourceResponseBody(TeaModel):
    def __init__(self, request_id=None, resources=None, total_count=None):
        # 请求 id
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        # 资源集合
        self.resources = resources  # type: list[CreateWorkspaceResourceResponseBodyResources]
        # 总数
        self.total_count = total_count  # type: long

    def validate(self):
        if self.resources:
            for k in self.resources:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Resources'] = []
        if self.resources is not None:
            for k in self.resources:
                result['Resources'].append(k.to_map() if k else None)
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.resources = []
        if m.get('Resources') is not None:
            for k in m.get('Resources'):
                temp_model = CreateWorkspaceResourceResponseBodyResources()
                self.resources.append(temp_model.from_map(k))
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class CreateWorkspaceResourceResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: CreateWorkspaceResourceResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateWorkspaceResourceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteMembersRequest(TeaModel):
    def __init__(self, member_ids=None):
        # 需要删除的成员 Id 列表，以逗号分隔
        self.member_ids = TeaConverter.to_unicode(member_ids)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.member_ids is not None:
            result['MemberIds'] = self.member_ids
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('MemberIds') is not None:
            self.member_ids = m.get('MemberIds')
        return self


class DeleteMembersResponseBody(TeaModel):
    def __init__(self, request_id=None):
        # 请求 id
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteMembersResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: DeleteMembersResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteMembersResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetPermissionResponseBody(TeaModel):
    def __init__(self, request_id=None, permission_code=None):
        # 请求 id
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        # 权限
        self.permission_code = TeaConverter.to_unicode(permission_code)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.permission_code is not None:
            result['PermissionCode'] = self.permission_code
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PermissionCode') is not None:
            self.permission_code = m.get('PermissionCode')
        return self


class GetPermissionResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: GetPermissionResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetPermissionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetRoleStatisticsRequest(TeaModel):
    def __init__(self, workspace_id=None):
        # 工作空间 id
        self.workspace_id = TeaConverter.to_unicode(workspace_id)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class GetRoleStatisticsResponseBodyRoles(TeaModel):
    def __init__(self, role_name=None, member_size=None):
        # 角色名
        self.role_name = TeaConverter.to_unicode(role_name)  # type: unicode
        # 成员数量
        self.member_size = member_size  # type: long

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.role_name is not None:
            result['RoleName'] = self.role_name
        if self.member_size is not None:
            result['MemberSize'] = self.member_size
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RoleName') is not None:
            self.role_name = m.get('RoleName')
        if m.get('MemberSize') is not None:
            self.member_size = m.get('MemberSize')
        return self


class GetRoleStatisticsResponseBody(TeaModel):
    def __init__(self, request_id=None, roles=None, total_count=None):
        # 请求 id
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        # 角色信息统计
        self.roles = roles  # type: list[GetRoleStatisticsResponseBodyRoles]
        # 总数
        self.total_count = total_count  # type: long

    def validate(self):
        if self.roles:
            for k in self.roles:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Roles'] = []
        if self.roles is not None:
            for k in self.roles:
                result['Roles'].append(k.to_map() if k else None)
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.roles = []
        if m.get('Roles') is not None:
            for k in m.get('Roles'):
                temp_model = GetRoleStatisticsResponseBodyRoles()
                self.roles.append(temp_model.from_map(k))
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class GetRoleStatisticsResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: GetRoleStatisticsResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetRoleStatisticsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetWorkspaceResponseBody(TeaModel):
    def __init__(self, request_id=None, workspace_id=None, workspace_name=None, gmt_create_time=None,
                 gmt_modified_time=None, display_name=None, description=None, env_types=None, creator=None, status=None,
                 admin_names=None, resource_count=None):
        # 请求 id
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        # 工作空间 id
        self.workspace_id = TeaConverter.to_unicode(workspace_id)  # type: unicode
        # 项目空间名称， region 内唯一
        self.workspace_name = TeaConverter.to_unicode(workspace_name)  # type: unicode
        # 创建 UTC 时间，日期格式 iso8601
        self.gmt_create_time = TeaConverter.to_unicode(gmt_create_time)  # type: unicode
        # 修改 UTC 时间，日期格式 iso8601
        self.gmt_modified_time = TeaConverter.to_unicode(gmt_modified_time)  # type: unicode
        # 显示名称
        self.display_name = TeaConverter.to_unicode(display_name)  # type: unicode
        # 描述
        self.description = TeaConverter.to_unicode(description)  # type: unicode
        # 环境，用作判断简单模式还是标准模式
        self.env_types = env_types  # type: list[unicode]
        # 创建人
        self.creator = TeaConverter.to_unicode(creator)  # type: unicode
        # 工作空间状态
        self.status = TeaConverter.to_unicode(status)  # type: unicode
        # 管理员账户
        self.admin_names = admin_names  # type: list[unicode]
        # 资源数目
        self.resource_count = resource_count  # type: int

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        if self.workspace_name is not None:
            result['WorkspaceName'] = self.workspace_name
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.display_name is not None:
            result['DisplayName'] = self.display_name
        if self.description is not None:
            result['Description'] = self.description
        if self.env_types is not None:
            result['EnvTypes'] = self.env_types
        if self.creator is not None:
            result['Creator'] = self.creator
        if self.status is not None:
            result['Status'] = self.status
        if self.admin_names is not None:
            result['AdminNames'] = self.admin_names
        if self.resource_count is not None:
            result['ResourceCount'] = self.resource_count
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        if m.get('WorkspaceName') is not None:
            self.workspace_name = m.get('WorkspaceName')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('DisplayName') is not None:
            self.display_name = m.get('DisplayName')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('EnvTypes') is not None:
            self.env_types = m.get('EnvTypes')
        if m.get('Creator') is not None:
            self.creator = m.get('Creator')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('AdminNames') is not None:
            self.admin_names = m.get('AdminNames')
        if m.get('ResourceCount') is not None:
            self.resource_count = m.get('ResourceCount')
        return self


class GetWorkspaceResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: GetWorkspaceResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetWorkspaceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListMembersRequest(TeaModel):
    def __init__(self, page_number=None, page_size=None, roles=None, member_name=None):
        # 分页，从1开始，默认1
        self.page_number = page_number  # type: long
        # 页大小，默认20
        self.page_size = page_size  # type: int
        # Role 过滤列表，逗号分隔
        self.roles = TeaConverter.to_unicode(roles)  # type: unicode
        # 成员名
        self.member_name = TeaConverter.to_unicode(member_name)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.roles is not None:
            result['Roles'] = self.roles
        if self.member_name is not None:
            result['MemberName'] = self.member_name
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Roles') is not None:
            self.roles = m.get('Roles')
        if m.get('MemberName') is not None:
            self.member_name = m.get('MemberName')
        return self


class ListMembersResponseBodyMembers(TeaModel):
    def __init__(self, user_id=None, user_name=None, gmt_create_time=None, roles=None, display_name=None,
                 member_id=None):
        # 用户 id
        self.user_id = TeaConverter.to_unicode(user_id)  # type: unicode
        # 云账号用户名
        self.user_name = TeaConverter.to_unicode(user_name)  # type: unicode
        # 创建 UTC 时间，日期格式 iso8601
        self.gmt_create_time = TeaConverter.to_unicode(gmt_create_time)  # type: unicode
        # 角色列表
        self.roles = roles  # type: list[unicode]
        # 成员显示名
        self.display_name = TeaConverter.to_unicode(display_name)  # type: unicode
        # 成员 id
        self.member_id = TeaConverter.to_unicode(member_id)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.user_name is not None:
            result['UserName'] = self.user_name
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.roles is not None:
            result['Roles'] = self.roles
        if self.display_name is not None:
            result['DisplayName'] = self.display_name
        if self.member_id is not None:
            result['MemberId'] = self.member_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('UserName') is not None:
            self.user_name = m.get('UserName')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('Roles') is not None:
            self.roles = m.get('Roles')
        if m.get('DisplayName') is not None:
            self.display_name = m.get('DisplayName')
        if m.get('MemberId') is not None:
            self.member_id = m.get('MemberId')
        return self


class ListMembersResponseBody(TeaModel):
    def __init__(self, request_id=None, members=None, total_count=None):
        # 请求 id
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        # 成员列表
        self.members = members  # type: list[ListMembersResponseBodyMembers]
        # 符合过滤条件的数量
        self.total_count = total_count  # type: long

    def validate(self):
        if self.members:
            for k in self.members:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Members'] = []
        if self.members is not None:
            for k in self.members:
                result['Members'].append(k.to_map() if k else None)
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.members = []
        if m.get('Members') is not None:
            for k in m.get('Members'):
                temp_model = ListMembersResponseBodyMembers()
                self.members.append(temp_model.from_map(k))
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListMembersResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: ListMembersResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListMembersResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListOperationLogsRequest(TeaModel):
    def __init__(self, page_number=None, page_size=None, order=None, entity_types=None, operations=None,
                 operation_status=None, sort_by=None, entity_status=None):
        # 当前页，页码从1开始
        self.page_number = page_number  # type: long
        # 每页返回的输出数目
        self.page_size = page_size  # type: int
        # 排序顺序， 顺序：ASC，倒序：DESC
        self.order = TeaConverter.to_unicode(order)  # type: unicode
        # 以逗号分隔的日志类型，包含 Resource
        self.entity_types = TeaConverter.to_unicode(entity_types)  # type: unicode
        # 以逗号分隔的操作
        self.operations = TeaConverter.to_unicode(operations)  # type: unicode
        # 以逗号分隔的操作状态
        self.operation_status = TeaConverter.to_unicode(operation_status)  # type: unicode
        # 排序字段
        self.sort_by = TeaConverter.to_unicode(sort_by)  # type: unicode
        self.entity_status = TeaConverter.to_unicode(entity_status)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.order is not None:
            result['Order'] = self.order
        if self.entity_types is not None:
            result['EntityTypes'] = self.entity_types
        if self.operations is not None:
            result['Operations'] = self.operations
        if self.operation_status is not None:
            result['OperationStatus'] = self.operation_status
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.entity_status is not None:
            result['EntityStatus'] = self.entity_status
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('EntityTypes') is not None:
            self.entity_types = m.get('EntityTypes')
        if m.get('Operations') is not None:
            self.operations = m.get('Operations')
        if m.get('OperationStatus') is not None:
            self.operation_status = m.get('OperationStatus')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('EntityStatus') is not None:
            self.entity_status = m.get('EntityStatus')
        return self


class ListOperationLogsResponseBodyLogs(TeaModel):
    def __init__(self, gmt_create_time=None, operator=None, message=None, operation=None, entity_type=None,
                 entity_id=None, operation_status=None):
        # 2021-01-30T12:51:33.028Z
        self.gmt_create_time = TeaConverter.to_unicode(gmt_create_time)  # type: unicode
        # 操作人
        self.operator = TeaConverter.to_unicode(operator)  # type: unicode
        # 日志
        self.message = TeaConverter.to_unicode(message)  # type: unicode
        # 操作，目前支持Create, Update, SetDefault
        self.operation = TeaConverter.to_unicode(operation)  # type: unicode
        # 实体类型，目前支持Resource
        self.entity_type = TeaConverter.to_unicode(entity_type)  # type: unicode
        # 实体 id
        self.entity_id = TeaConverter.to_unicode(entity_id)  # type: unicode
        # 操作状态，支持 Processing、Succeeded、Failed
        self.operation_status = TeaConverter.to_unicode(operation_status)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.operator is not None:
            result['Operator'] = self.operator
        if self.message is not None:
            result['Message'] = self.message
        if self.operation is not None:
            result['Operation'] = self.operation
        if self.entity_type is not None:
            result['EntityType'] = self.entity_type
        if self.entity_id is not None:
            result['EntityId'] = self.entity_id
        if self.operation_status is not None:
            result['OperationStatus'] = self.operation_status
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('Operator') is not None:
            self.operator = m.get('Operator')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('Operation') is not None:
            self.operation = m.get('Operation')
        if m.get('EntityType') is not None:
            self.entity_type = m.get('EntityType')
        if m.get('EntityId') is not None:
            self.entity_id = m.get('EntityId')
        if m.get('OperationStatus') is not None:
            self.operation_status = m.get('OperationStatus')
        return self


class ListOperationLogsResponseBody(TeaModel):
    def __init__(self, request_id=None, total_count=None, logs=None):
        # 请求 id
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        # 符合过滤条件的日志数量
        self.total_count = total_count  # type: long
        # 输出日志列表
        self.logs = logs  # type: list[ListOperationLogsResponseBodyLogs]

    def validate(self):
        if self.logs:
            for k in self.logs:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        result['Logs'] = []
        if self.logs is not None:
            for k in self.logs:
                result['Logs'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        self.logs = []
        if m.get('Logs') is not None:
            for k in m.get('Logs'):
                temp_model = ListOperationLogsResponseBodyLogs()
                self.logs.append(temp_model.from_map(k))
        return self


class ListOperationLogsResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: ListOperationLogsResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListOperationLogsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListPermissionsResponseBodyPermissions(TeaModel):
    def __init__(self, permission_code=None):
        # 权限 code
        self.permission_code = TeaConverter.to_unicode(permission_code)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.permission_code is not None:
            result['PermissionCode'] = self.permission_code
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('PermissionCode') is not None:
            self.permission_code = m.get('PermissionCode')
        return self


class ListPermissionsResponseBody(TeaModel):
    def __init__(self, request_id=None, permissions=None, total_count=None):
        # 请求 id
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        # 权限列表
        self.permissions = permissions  # type: list[ListPermissionsResponseBodyPermissions]
        # 符合过滤条件的数量
        self.total_count = total_count  # type: long

    def validate(self):
        if self.permissions:
            for k in self.permissions:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Permissions'] = []
        if self.permissions is not None:
            for k in self.permissions:
                result['Permissions'].append(k.to_map() if k else None)
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.permissions = []
        if m.get('Permissions') is not None:
            for k in m.get('Permissions'):
                temp_model = ListPermissionsResponseBodyPermissions()
                self.permissions.append(temp_model.from_map(k))
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListPermissionsResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: ListPermissionsResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListPermissionsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListProductsRequest(TeaModel):
    def __init__(self, product_codes=None):
        # 逗号分割的商品 code
        self.product_codes = TeaConverter.to_unicode(product_codes)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.product_codes is not None:
            result['ProductCodes'] = self.product_codes
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('ProductCodes') is not None:
            self.product_codes = m.get('ProductCodes')
        return self


class ListProductsResponseBodyProducts(TeaModel):
    def __init__(self, buy_url=None, product_code=None, is_purchased=None, total_count=None):
        # 购买链接
        self.buy_url = TeaConverter.to_unicode(buy_url)  # type: unicode
        # 商品 code
        self.product_code = TeaConverter.to_unicode(product_code)  # type: unicode
        # 是否已购买
        self.is_purchased = is_purchased  # type: bool
        # 符合过滤条件的作业数量
        self.total_count = total_count  # type: long

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.buy_url is not None:
            result['BuyUrl'] = self.buy_url
        if self.product_code is not None:
            result['ProductCode'] = self.product_code
        if self.is_purchased is not None:
            result['IsPurchased'] = self.is_purchased
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('BuyUrl') is not None:
            self.buy_url = m.get('BuyUrl')
        if m.get('ProductCode') is not None:
            self.product_code = m.get('ProductCode')
        if m.get('IsPurchased') is not None:
            self.is_purchased = m.get('IsPurchased')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListProductsResponseBody(TeaModel):
    def __init__(self, request_id=None, products=None):
        # 请求 id
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        # 工作空间列表
        self.products = products  # type: list[ListProductsResponseBodyProducts]

    def validate(self):
        if self.products:
            for k in self.products:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Products'] = []
        if self.products is not None:
            for k in self.products:
                result['Products'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.products = []
        if m.get('Products') is not None:
            for k in m.get('Products'):
                temp_model = ListProductsResponseBodyProducts()
                self.products.append(temp_model.from_map(k))
        return self


class ListProductsResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: ListProductsResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListProductsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListQuotasResponseBodyQuotasSpecs(TeaModel):
    def __init__(self, name=None, value=None, type=None):
        # 规格名
        self.name = TeaConverter.to_unicode(name)  # type: unicode
        # 规格描述
        self.value = TeaConverter.to_unicode(value)  # type: unicode
        # 类型，可为空
        self.type = TeaConverter.to_unicode(type)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.value is not None:
            result['Value'] = self.value
        if self.type is not None:
            result['Type'] = self.type
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        return self


class ListQuotasResponseBodyQuotas(TeaModel):
    def __init__(self, quota_type=None, mode=None, product_code=None, name=None, specs=None, id=None):
        # 产品类型， 支持PAI，MaxCompute
        self.quota_type = TeaConverter.to_unicode(quota_type)  # type: unicode
        # 模式  isolate 预付费  share 后付费  develop 开发模式
        self.mode = TeaConverter.to_unicode(mode)  # type: unicode
        # 产品代码
        self.product_code = TeaConverter.to_unicode(product_code)  # type: unicode
        # quota名字
        self.name = TeaConverter.to_unicode(name)  # type: unicode
        # 规格描述列表
        self.specs = specs  # type: list[ListQuotasResponseBodyQuotasSpecs]
        # quota的id
        self.id = TeaConverter.to_unicode(id)  # type: unicode

    def validate(self):
        if self.specs:
            for k in self.specs:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.quota_type is not None:
            result['QuotaType'] = self.quota_type
        if self.mode is not None:
            result['Mode'] = self.mode
        if self.product_code is not None:
            result['ProductCode'] = self.product_code
        if self.name is not None:
            result['Name'] = self.name
        result['Specs'] = []
        if self.specs is not None:
            for k in self.specs:
                result['Specs'].append(k.to_map() if k else None)
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('QuotaType') is not None:
            self.quota_type = m.get('QuotaType')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        if m.get('ProductCode') is not None:
            self.product_code = m.get('ProductCode')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        self.specs = []
        if m.get('Specs') is not None:
            for k in m.get('Specs'):
                temp_model = ListQuotasResponseBodyQuotasSpecs()
                self.specs.append(temp_model.from_map(k))
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class ListQuotasResponseBody(TeaModel):
    def __init__(self, request_id=None, quotas=None, total_count=None):
        # 请求 id
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        # 配额列表
        self.quotas = quotas  # type: list[ListQuotasResponseBodyQuotas]
        # 符合过滤条件的数量
        self.total_count = total_count  # type: long

    def validate(self):
        if self.quotas:
            for k in self.quotas:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Quotas'] = []
        if self.quotas is not None:
            for k in self.quotas:
                result['Quotas'].append(k.to_map() if k else None)
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.quotas = []
        if m.get('Quotas') is not None:
            for k in m.get('Quotas'):
                temp_model = ListQuotasResponseBodyQuotas()
                self.quotas.append(temp_model.from_map(k))
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListQuotasResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: ListQuotasResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListQuotasResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListResourcesRequest(TeaModel):
    def __init__(self, workspace_id=None, page_number=None, page_size=None, product_types=None,
                 resource_group_name=None, resource_name=None):
        # 工作空间 id
        self.workspace_id = TeaConverter.to_unicode(workspace_id)  # type: unicode
        # 分页，从1开始，默认1
        self.page_number = page_number  # type: long
        # 页大小，默认20
        self.page_size = page_size  # type: int
        # 逗号分隔的产品类型，可选值 MaxCompute，DLC
        self.product_types = TeaConverter.to_unicode(product_types)  # type: unicode
        # 资源的group名字
        self.resource_group_name = TeaConverter.to_unicode(resource_group_name)  # type: unicode
        # 资源的名字
        self.resource_name = TeaConverter.to_unicode(resource_name)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.product_types is not None:
            result['ProductTypes'] = self.product_types
        if self.resource_group_name is not None:
            result['ResourceGroupName'] = self.resource_group_name
        if self.resource_name is not None:
            result['ResourceName'] = self.resource_name
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('ProductTypes') is not None:
            self.product_types = m.get('ProductTypes')
        if m.get('ResourceGroupName') is not None:
            self.resource_group_name = m.get('ResourceGroupName')
        if m.get('ResourceName') is not None:
            self.resource_name = m.get('ResourceName')
        return self


class ListResourcesResponseBodyResourcesQuotasSpecs(TeaModel):
    def __init__(self, name=None, value=None):
        # 规格名字
        self.name = TeaConverter.to_unicode(name)  # type: unicode
        # 规格描述
        self.value = TeaConverter.to_unicode(value)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class ListResourcesResponseBodyResourcesQuotas(TeaModel):
    def __init__(self, name=None, product_code=None, quota_type=None, mode=None, specs=None, card_type=None, id=None):
        # 配额名称
        self.name = TeaConverter.to_unicode(name)  # type: unicode
        # 商品 code
        self.product_code = TeaConverter.to_unicode(product_code)  # type: unicode
        # 产品类型， 支持PAI，MaxCompute
        self.quota_type = TeaConverter.to_unicode(quota_type)  # type: unicode
        # 模式 isolate 预付费 share 后付费 develop 开发模式
        self.mode = TeaConverter.to_unicode(mode)  # type: unicode
        # 规格描述列表
        self.specs = specs  # type: list[ListResourcesResponseBodyResourcesQuotasSpecs]
        # 卡类型，支持cpu、gpu
        self.card_type = TeaConverter.to_unicode(card_type)  # type: unicode
        # 配额id
        self.id = TeaConverter.to_unicode(id)  # type: unicode

    def validate(self):
        if self.specs:
            for k in self.specs:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.product_code is not None:
            result['ProductCode'] = self.product_code
        if self.quota_type is not None:
            result['QuotaType'] = self.quota_type
        if self.mode is not None:
            result['Mode'] = self.mode
        result['Specs'] = []
        if self.specs is not None:
            for k in self.specs:
                result['Specs'].append(k.to_map() if k else None)
        if self.card_type is not None:
            result['CardType'] = self.card_type
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('ProductCode') is not None:
            self.product_code = m.get('ProductCode')
        if m.get('QuotaType') is not None:
            self.quota_type = m.get('QuotaType')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        self.specs = []
        if m.get('Specs') is not None:
            for k in m.get('Specs'):
                temp_model = ListResourcesResponseBodyResourcesQuotasSpecs()
                self.specs.append(temp_model.from_map(k))
        if m.get('CardType') is not None:
            self.card_type = m.get('CardType')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class ListResourcesResponseBodyResources(TeaModel):
    def __init__(self, id=None, name=None, product_type=None, env_type=None, workspace_id=None, is_default=None,
                 quotas=None, spec=None, group_name=None, gmt_create_time=None):
        # 资源 id
        self.id = TeaConverter.to_unicode(id)  # type: unicode
        # 资源名 长度需要在3到27个字符 region内唯一
        self.name = TeaConverter.to_unicode(name)  # type: unicode
        # 产品类型， 支持PAI，MaxCompute
        self.product_type = TeaConverter.to_unicode(product_type)  # type: unicode
        # 环境， 支持dev（开发）、prod（生产）
        self.env_type = TeaConverter.to_unicode(env_type)  # type: unicode
        # 所属的工作空间 id
        self.workspace_id = TeaConverter.to_unicode(workspace_id)  # type: unicode
        # 是否默认资源 每个类型都有一个默认的资源
        self.is_default = is_default  # type: bool
        self.quotas = quotas  # type: list[ListResourcesResponseBodyResourcesQuotas]
        # 对于MaxCompute是个json，有如下key： Endpoint Project
        self.spec = spec  # type: dict[unicode, any]
        # 分组名，主账户内唯一 一个 GroupName 下可能有一个 dev 资源和一个 prod 资源
        self.group_name = TeaConverter.to_unicode(group_name)  # type: unicode
        # 创建 UTC 时间，日期格式 iso8601
        self.gmt_create_time = TeaConverter.to_unicode(gmt_create_time)  # type: unicode

    def validate(self):
        if self.quotas:
            for k in self.quotas:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.id is not None:
            result['id'] = self.id
        if self.name is not None:
            result['Name'] = self.name
        if self.product_type is not None:
            result['ProductType'] = self.product_type
        if self.env_type is not None:
            result['EnvType'] = self.env_type
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        if self.is_default is not None:
            result['IsDefault'] = self.is_default
        result['Quotas'] = []
        if self.quotas is not None:
            for k in self.quotas:
                result['Quotas'].append(k.to_map() if k else None)
        if self.spec is not None:
            result['Spec'] = self.spec
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('id') is not None:
            self.id = m.get('id')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('ProductType') is not None:
            self.product_type = m.get('ProductType')
        if m.get('EnvType') is not None:
            self.env_type = m.get('EnvType')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        if m.get('IsDefault') is not None:
            self.is_default = m.get('IsDefault')
        self.quotas = []
        if m.get('Quotas') is not None:
            for k in m.get('Quotas'):
                temp_model = ListResourcesResponseBodyResourcesQuotas()
                self.quotas.append(temp_model.from_map(k))
        if m.get('Spec') is not None:
            self.spec = m.get('Spec')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        return self


class ListResourcesResponseBody(TeaModel):
    def __init__(self, request_id=None, resources=None, total_count=None):
        # 请求 id
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        # 资源列表
        self.resources = resources  # type: list[ListResourcesResponseBodyResources]
        # 符合过滤条件的作业数量
        self.total_count = total_count  # type: long

    def validate(self):
        if self.resources:
            for k in self.resources:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Resources'] = []
        if self.resources is not None:
            for k in self.resources:
                result['Resources'].append(k.to_map() if k else None)
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.resources = []
        if m.get('Resources') is not None:
            for k in m.get('Resources'):
                temp_model = ListResourcesResponseBodyResources()
                self.resources.append(temp_model.from_map(k))
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListResourcesResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: ListResourcesResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListResourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListWorkspacesRequest(TeaModel):
    def __init__(self, page_number=None, page_size=None, sort_by=None, order=None, workspace_name=None,
                 module_list=None, status=None, option=None, verbose=None):
        # 分页，从1开始，默认1
        self.page_number = page_number  # type: long
        # 页大小，默认20
        self.page_size = page_size  # type: int
        # 排序字段：CreateTime
        self.sort_by = TeaConverter.to_unicode(sort_by)  # type: unicode
        # 排序方向： ASC - 升序 DESC - 降序
        self.order = TeaConverter.to_unicode(order)  # type: unicode
        # 工作空间名字
        self.workspace_name = TeaConverter.to_unicode(workspace_name)  # type: unicode
        # 逗号分割的模块列表，目前填入PAI
        self.module_list = TeaConverter.to_unicode(module_list)  # type: unicode
        # 状态
        self.status = TeaConverter.to_unicode(status)  # type: unicode
        # 逗号分隔的选项
        self.option = TeaConverter.to_unicode(option)  # type: unicode
        # 是否显示详细信息，默认true
        self.verbose = verbose  # type: bool

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.order is not None:
            result['Order'] = self.order
        if self.workspace_name is not None:
            result['WorkspaceName'] = self.workspace_name
        if self.module_list is not None:
            result['ModuleList'] = self.module_list
        if self.status is not None:
            result['Status'] = self.status
        if self.option is not None:
            result['Option'] = self.option
        if self.verbose is not None:
            result['Verbose'] = self.verbose
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('WorkspaceName') is not None:
            self.workspace_name = m.get('WorkspaceName')
        if m.get('ModuleList') is not None:
            self.module_list = m.get('ModuleList')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('Option') is not None:
            self.option = m.get('Option')
        if m.get('Verbose') is not None:
            self.verbose = m.get('Verbose')
        return self


class ListWorkspacesResponseBodyWorkspaces(TeaModel):
    def __init__(self, workspace_id=None, workspace_name=None, gmt_create_time=None, gmt_modified_time=None,
                 description=None, creator=None, env_types=None, status=None, admin_names=None, resource_count=None):
        # 工作空间 id
        self.workspace_id = TeaConverter.to_unicode(workspace_id)  # type: unicode
        # 工作空间名字
        self.workspace_name = TeaConverter.to_unicode(workspace_name)  # type: unicode
        # 创建 UTC 时间，日期格式 iso8601
        self.gmt_create_time = TeaConverter.to_unicode(gmt_create_time)  # type: unicode
        # 修改 UTC 时间，日期格式 iso8601
        self.gmt_modified_time = TeaConverter.to_unicode(gmt_modified_time)  # type: unicode
        # 描述
        self.description = TeaConverter.to_unicode(description)  # type: unicode
        # 创建人
        self.creator = TeaConverter.to_unicode(creator)  # type: unicode
        # 环境，用作判断简单模式还是标准模式
        self.env_types = env_types  # type: list[unicode]
        # 工作空间状态
        self.status = TeaConverter.to_unicode(status)  # type: unicode
        # 管理员名字
        self.admin_names = admin_names  # type: list[unicode]
        # 资源数目
        self.resource_count = resource_count  # type: int

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        if self.workspace_name is not None:
            result['WorkspaceName'] = self.workspace_name
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.description is not None:
            result['Description'] = self.description
        if self.creator is not None:
            result['Creator'] = self.creator
        if self.env_types is not None:
            result['EnvTypes'] = self.env_types
        if self.status is not None:
            result['Status'] = self.status
        if self.admin_names is not None:
            result['AdminNames'] = self.admin_names
        if self.resource_count is not None:
            result['ResourceCount'] = self.resource_count
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        if m.get('WorkspaceName') is not None:
            self.workspace_name = m.get('WorkspaceName')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Creator') is not None:
            self.creator = m.get('Creator')
        if m.get('EnvTypes') is not None:
            self.env_types = m.get('EnvTypes')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('AdminNames') is not None:
            self.admin_names = m.get('AdminNames')
        if m.get('ResourceCount') is not None:
            self.resource_count = m.get('ResourceCount')
        return self


class ListWorkspacesResponseBody(TeaModel):
    def __init__(self, request_id=None, workspaces=None, total_count=None, resource_limits=None):
        # 请求 id
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        # 工作空间列表
        self.workspaces = workspaces  # type: list[ListWorkspacesResponseBodyWorkspaces]
        # 符合过滤条件的作业数量
        self.total_count = total_count  # type: long
        # 资源限制
        self.resource_limits = resource_limits  # type: dict[unicode, any]

    def validate(self):
        if self.workspaces:
            for k in self.workspaces:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Workspaces'] = []
        if self.workspaces is not None:
            for k in self.workspaces:
                result['Workspaces'].append(k.to_map() if k else None)
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.resource_limits is not None:
            result['ResourceLimits'] = self.resource_limits
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.workspaces = []
        if m.get('Workspaces') is not None:
            for k in m.get('Workspaces'):
                temp_model = ListWorkspacesResponseBodyWorkspaces()
                self.workspaces.append(temp_model.from_map(k))
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('ResourceLimits') is not None:
            self.resource_limits = m.get('ResourceLimits')
        return self


class ListWorkspacesResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: ListWorkspacesResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListWorkspacesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListWorkspaceUsersResponseBodyUsers(TeaModel):
    def __init__(self, user_id=None, user_name=None):
        # 用户 id
        self.user_id = TeaConverter.to_unicode(user_id)  # type: unicode
        # 用户名
        self.user_name = TeaConverter.to_unicode(user_name)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.user_name is not None:
            result['UserName'] = self.user_name
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('UserName') is not None:
            self.user_name = m.get('UserName')
        return self


class ListWorkspaceUsersResponseBody(TeaModel):
    def __init__(self, request_id=None, total_count=None, users=None):
        # 请求 id
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        # 符合过滤条件的用户数量
        self.total_count = total_count  # type: long
        # 用户列表
        self.users = users  # type: list[ListWorkspaceUsersResponseBodyUsers]

    def validate(self):
        if self.users:
            for k in self.users:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        result['Users'] = []
        if self.users is not None:
            for k in self.users:
                result['Users'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        self.users = []
        if m.get('Users') is not None:
            for k in m.get('Users'):
                temp_model = ListWorkspaceUsersResponseBodyUsers()
                self.users.append(temp_model.from_map(k))
        return self


class ListWorkspaceUsersResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: ListWorkspaceUsersResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListWorkspaceUsersResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RemoveMemberRoleResponseBody(TeaModel):
    def __init__(self, request_id=None):
        # 请求 id
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class RemoveMemberRoleResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: RemoveMemberRoleResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = RemoveMemberRoleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RemoveWorkspaceQuotaResponseBody(TeaModel):
    def __init__(self, request_id=None):
        # 请求 id
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class RemoveWorkspaceQuotaResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: RemoveWorkspaceQuotaResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = RemoveWorkspaceQuotaResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateWorkspaceRequest(TeaModel):
    def __init__(self, display_name=None):
        # 显示名称
        self.display_name = TeaConverter.to_unicode(display_name)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.display_name is not None:
            result['DisplayName'] = self.display_name
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('DisplayName') is not None:
            self.display_name = m.get('DisplayName')
        return self


class UpdateWorkspaceResponseBody(TeaModel):
    def __init__(self, request_id=None):
        # 请求 id
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateWorkspaceResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: UpdateWorkspaceResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateWorkspaceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateWorkspaceResourceRequest(TeaModel):
    def __init__(self, is_default=None):
        # 是否默认资源实例，目前只能填 true，不支持填 false
        self.is_default = is_default  # type: bool

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.is_default is not None:
            result['IsDefault'] = self.is_default
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('IsDefault') is not None:
            self.is_default = m.get('IsDefault')
        return self


class UpdateWorkspaceResourceResponseBody(TeaModel):
    def __init__(self, request_id=None):
        # 请求 id
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateWorkspaceResourceResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: UpdateWorkspaceResourceResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateWorkspaceResourceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


