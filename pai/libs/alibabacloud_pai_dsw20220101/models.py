# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel
from typing import List, Dict, Any


class CredentialConfigConfigsRolesUserInfo(TeaModel):
    def __init__(
        self,
        access_key_id: str = None,
        id: str = None,
        security_token: str = None,
        type: str = None,
    ):
        self.access_key_id = access_key_id
        self.id = id
        self.security_token = security_token
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.access_key_id is not None:
            result['AccessKeyId'] = self.access_key_id
        if self.id is not None:
            result['Id'] = self.id
        if self.security_token is not None:
            result['SecurityToken'] = self.security_token
        if self.type is not None:
            result['Type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccessKeyId') is not None:
            self.access_key_id = m.get('AccessKeyId')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('SecurityToken') is not None:
            self.security_token = m.get('SecurityToken')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        return self


class CredentialConfigConfigsRoles(TeaModel):
    def __init__(
        self,
        assume_role_for: str = None,
        policy: str = None,
        role_arn: str = None,
        role_type: str = None,
        user_info: CredentialConfigConfigsRolesUserInfo = None,
    ):
        self.assume_role_for = assume_role_for
        self.policy = policy
        # This parameter is required.
        self.role_arn = role_arn
        # This parameter is required.
        self.role_type = role_type
        self.user_info = user_info

    def validate(self):
        if self.user_info:
            self.user_info.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.assume_role_for is not None:
            result['AssumeRoleFor'] = self.assume_role_for
        if self.policy is not None:
            result['Policy'] = self.policy
        if self.role_arn is not None:
            result['RoleArn'] = self.role_arn
        if self.role_type is not None:
            result['RoleType'] = self.role_type
        if self.user_info is not None:
            result['UserInfo'] = self.user_info.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AssumeRoleFor') is not None:
            self.assume_role_for = m.get('AssumeRoleFor')
        if m.get('Policy') is not None:
            self.policy = m.get('Policy')
        if m.get('RoleArn') is not None:
            self.role_arn = m.get('RoleArn')
        if m.get('RoleType') is not None:
            self.role_type = m.get('RoleType')
        if m.get('UserInfo') is not None:
            temp_model = CredentialConfigConfigsRolesUserInfo()
            self.user_info = temp_model.from_map(m['UserInfo'])
        return self


class CredentialConfigConfigs(TeaModel):
    def __init__(
        self,
        key: str = None,
        roles: List[CredentialConfigConfigsRoles] = None,
        type: str = None,
    ):
        # This parameter is required.
        self.key = key
        self.roles = roles
        # This parameter is required.
        self.type = type

    def validate(self):
        if self.roles:
            for k in self.roles:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        result['Roles'] = []
        if self.roles is not None:
            for k in self.roles:
                result['Roles'].append(k.to_map() if k else None)
        if self.type is not None:
            result['Type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        self.roles = []
        if m.get('Roles') is not None:
            for k in m.get('Roles'):
                temp_model = CredentialConfigConfigsRoles()
                self.roles.append(temp_model.from_map(k))
        if m.get('Type') is not None:
            self.type = m.get('Type')
        return self


class CredentialConfig(TeaModel):
    def __init__(
        self,
        aliyun_env_role_key: str = None,
        configs: List[CredentialConfigConfigs] = None,
        enable: bool = None,
    ):
        self.aliyun_env_role_key = aliyun_env_role_key
        self.configs = configs
        self.enable = enable

    def validate(self):
        if self.configs:
            for k in self.configs:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.aliyun_env_role_key is not None:
            result['AliyunEnvRoleKey'] = self.aliyun_env_role_key
        result['Configs'] = []
        if self.configs is not None:
            for k in self.configs:
                result['Configs'].append(k.to_map() if k else None)
        if self.enable is not None:
            result['Enable'] = self.enable
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AliyunEnvRoleKey') is not None:
            self.aliyun_env_role_key = m.get('AliyunEnvRoleKey')
        self.configs = []
        if m.get('Configs') is not None:
            for k in m.get('Configs'):
                temp_model = CredentialConfigConfigs()
                self.configs.append(temp_model.from_map(k))
        if m.get('Enable') is not None:
            self.enable = m.get('Enable')
        return self


class DemoCategory(TeaModel):
    def __init__(
        self,
        category_code: str = None,
        category_name: str = None,
        order: int = None,
        sub_categories: List['DemoCategory'] = None,
    ):
        self.category_code = category_code
        self.category_name = category_name
        self.order = order
        self.sub_categories = sub_categories

    def validate(self):
        if self.sub_categories:
            for k in self.sub_categories:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.category_code is not None:
            result['CategoryCode'] = self.category_code
        if self.category_name is not None:
            result['CategoryName'] = self.category_name
        if self.order is not None:
            result['Order'] = self.order
        result['SubCategories'] = []
        if self.sub_categories is not None:
            for k in self.sub_categories:
                result['SubCategories'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CategoryCode') is not None:
            self.category_code = m.get('CategoryCode')
        if m.get('CategoryName') is not None:
            self.category_name = m.get('CategoryName')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        self.sub_categories = []
        if m.get('SubCategories') is not None:
            for k in m.get('SubCategories'):
                temp_model = DemoCategory()
                self.sub_categories.append(temp_model.from_map(k))
        return self


class DynamicMountPoint(TeaModel):
    def __init__(
        self,
        options: str = None,
        root_path: str = None,
    ):
        self.options = options
        # This parameter is required.
        self.root_path = root_path

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.options is not None:
            result['Options'] = self.options
        if self.root_path is not None:
            result['RootPath'] = self.root_path
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Options') is not None:
            self.options = m.get('Options')
        if m.get('RootPath') is not None:
            self.root_path = m.get('RootPath')
        return self


class DynamicMount(TeaModel):
    def __init__(
        self,
        enable: bool = None,
        mount_points: List[DynamicMountPoint] = None,
    ):
        self.enable = enable
        self.mount_points = mount_points

    def validate(self):
        if self.mount_points:
            for k in self.mount_points:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.enable is not None:
            result['Enable'] = self.enable
        result['MountPoints'] = []
        if self.mount_points is not None:
            for k in self.mount_points:
                result['MountPoints'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Enable') is not None:
            self.enable = m.get('Enable')
        self.mount_points = []
        if m.get('MountPoints') is not None:
            for k in m.get('MountPoints'):
                temp_model = DynamicMountPoint()
                self.mount_points.append(temp_model.from_map(k))
        return self


class ForwardInfo(TeaModel):
    def __init__(
        self,
        container_name: str = None,
        eip_allocation_id: str = None,
        enable: bool = None,
        nat_gateway_id: str = None,
        port: str = None,
        sshpublic_key: str = None,
    ):
        self.container_name = container_name
        self.eip_allocation_id = eip_allocation_id
        self.enable = enable
        self.nat_gateway_id = nat_gateway_id
        self.port = port
        self.sshpublic_key = sshpublic_key

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.container_name is not None:
            result['ContainerName'] = self.container_name
        if self.eip_allocation_id is not None:
            result['EipAllocationId'] = self.eip_allocation_id
        if self.enable is not None:
            result['Enable'] = self.enable
        if self.nat_gateway_id is not None:
            result['NatGatewayId'] = self.nat_gateway_id
        if self.port is not None:
            result['Port'] = self.port
        if self.sshpublic_key is not None:
            result['SSHPublicKey'] = self.sshpublic_key
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ContainerName') is not None:
            self.container_name = m.get('ContainerName')
        if m.get('EipAllocationId') is not None:
            self.eip_allocation_id = m.get('EipAllocationId')
        if m.get('Enable') is not None:
            self.enable = m.get('Enable')
        if m.get('NatGatewayId') is not None:
            self.nat_gateway_id = m.get('NatGatewayId')
        if m.get('Port') is not None:
            self.port = m.get('Port')
        if m.get('SSHPublicKey') is not None:
            self.sshpublic_key = m.get('SSHPublicKey')
        return self


class ForwardInfoResponseConnectInfoInternet(TeaModel):
    def __init__(
        self,
        endpoint: str = None,
        port: str = None,
    ):
        self.endpoint = endpoint
        self.port = port

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.endpoint is not None:
            result['Endpoint'] = self.endpoint
        if self.port is not None:
            result['Port'] = self.port
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Endpoint') is not None:
            self.endpoint = m.get('Endpoint')
        if m.get('Port') is not None:
            self.port = m.get('Port')
        return self


class ForwardInfoResponseConnectInfoIntranet(TeaModel):
    def __init__(
        self,
        endpoint: str = None,
        port: str = None,
    ):
        self.endpoint = endpoint
        self.port = port

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.endpoint is not None:
            result['Endpoint'] = self.endpoint
        if self.port is not None:
            result['Port'] = self.port
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Endpoint') is not None:
            self.endpoint = m.get('Endpoint')
        if m.get('Port') is not None:
            self.port = m.get('Port')
        return self


class ForwardInfoResponseConnectInfo(TeaModel):
    def __init__(
        self,
        internet: ForwardInfoResponseConnectInfoInternet = None,
        intranet: ForwardInfoResponseConnectInfoIntranet = None,
        message: str = None,
        phase: str = None,
    ):
        self.internet = internet
        self.intranet = intranet
        self.message = message
        self.phase = phase

    def validate(self):
        if self.internet:
            self.internet.validate()
        if self.intranet:
            self.intranet.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.internet is not None:
            result['Internet'] = self.internet.to_map()
        if self.intranet is not None:
            result['Intranet'] = self.intranet.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.phase is not None:
            result['Phase'] = self.phase
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Internet') is not None:
            temp_model = ForwardInfoResponseConnectInfoInternet()
            self.internet = temp_model.from_map(m['Internet'])
        if m.get('Intranet') is not None:
            temp_model = ForwardInfoResponseConnectInfoIntranet()
            self.intranet = temp_model.from_map(m['Intranet'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('Phase') is not None:
            self.phase = m.get('Phase')
        return self


class ForwardInfoResponse(TeaModel):
    def __init__(
        self,
        connect_info: ForwardInfoResponseConnectInfo = None,
        container_name: str = None,
        eip_allocation_id: str = None,
        enable: bool = None,
        nat_gateway_id: str = None,
        port: str = None,
        sshpublic_key: str = None,
    ):
        self.connect_info = connect_info
        self.container_name = container_name
        self.eip_allocation_id = eip_allocation_id
        self.enable = enable
        self.nat_gateway_id = nat_gateway_id
        self.port = port
        self.sshpublic_key = sshpublic_key

    def validate(self):
        if self.connect_info:
            self.connect_info.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.connect_info is not None:
            result['ConnectInfo'] = self.connect_info.to_map()
        if self.container_name is not None:
            result['ContainerName'] = self.container_name
        if self.eip_allocation_id is not None:
            result['EipAllocationId'] = self.eip_allocation_id
        if self.enable is not None:
            result['Enable'] = self.enable
        if self.nat_gateway_id is not None:
            result['NatGatewayId'] = self.nat_gateway_id
        if self.port is not None:
            result['Port'] = self.port
        if self.sshpublic_key is not None:
            result['SSHPublicKey'] = self.sshpublic_key
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConnectInfo') is not None:
            temp_model = ForwardInfoResponseConnectInfo()
            self.connect_info = temp_model.from_map(m['ConnectInfo'])
        if m.get('ContainerName') is not None:
            self.container_name = m.get('ContainerName')
        if m.get('EipAllocationId') is not None:
            self.eip_allocation_id = m.get('EipAllocationId')
        if m.get('Enable') is not None:
            self.enable = m.get('Enable')
        if m.get('NatGatewayId') is not None:
            self.nat_gateway_id = m.get('NatGatewayId')
        if m.get('Port') is not None:
            self.port = m.get('Port')
        if m.get('SSHPublicKey') is not None:
            self.sshpublic_key = m.get('SSHPublicKey')
        return self


class CheckInstanceExistenceRequest(TeaModel):
    def __init__(
        self,
        instance_name: str = None,
        workspace_id: str = None,
    ):
        # This parameter is required.
        self.instance_name = instance_name
        # This parameter is required.
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class CheckInstanceExistenceResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        http_status_code: int = None,
        is_existed: bool = None,
        message: str = None,
        request_id: str = None,
    ):
        self.code = code
        self.http_status_code = http_status_code
        self.is_existed = is_existed
        self.message = message
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.is_existed is not None:
            result['IsExisted'] = self.is_existed
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('IsExisted') is not None:
            self.is_existed = m.get('IsExisted')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class CheckInstanceExistenceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CheckInstanceExistenceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CheckInstanceExistenceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateEndpointRequest(TeaModel):
    def __init__(
        self,
        action: str = None,
        app: str = None,
        endpoint: str = None,
        method: str = None,
        path_name: str = None,
        protocol: str = None,
        req_body_type: str = None,
        style: str = None,
        timeout: int = None,
        version: str = None,
    ):
        self.action = action
        self.app = app
        self.endpoint = endpoint
        self.method = method
        self.path_name = path_name
        self.protocol = protocol
        self.req_body_type = req_body_type
        self.style = style
        self.timeout = timeout
        self.version = version

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.action is not None:
            result['Action'] = self.action
        if self.app is not None:
            result['App'] = self.app
        if self.endpoint is not None:
            result['Endpoint'] = self.endpoint
        if self.method is not None:
            result['Method'] = self.method
        if self.path_name is not None:
            result['PathName'] = self.path_name
        if self.protocol is not None:
            result['Protocol'] = self.protocol
        if self.req_body_type is not None:
            result['ReqBodyType'] = self.req_body_type
        if self.style is not None:
            result['Style'] = self.style
        if self.timeout is not None:
            result['Timeout'] = self.timeout
        if self.version is not None:
            result['Version'] = self.version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Action') is not None:
            self.action = m.get('Action')
        if m.get('App') is not None:
            self.app = m.get('App')
        if m.get('Endpoint') is not None:
            self.endpoint = m.get('Endpoint')
        if m.get('Method') is not None:
            self.method = m.get('Method')
        if m.get('PathName') is not None:
            self.path_name = m.get('PathName')
        if m.get('Protocol') is not None:
            self.protocol = m.get('Protocol')
        if m.get('ReqBodyType') is not None:
            self.req_body_type = m.get('ReqBodyType')
        if m.get('Style') is not None:
            self.style = m.get('Style')
        if m.get('Timeout') is not None:
            self.timeout = m.get('Timeout')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        return self


class CreateEndpointResponseBody(TeaModel):
    def __init__(
        self,
        action: str = None,
        app: str = None,
        code: str = None,
        endpoint: str = None,
        http_status_code: int = None,
        message: str = None,
        method: str = None,
        path_name: str = None,
        protocol: str = None,
        req_body_type: str = None,
        request_id: str = None,
        style: str = None,
        success: bool = None,
        timeout: int = None,
        version: str = None,
    ):
        self.action = action
        self.app = app
        self.code = code
        self.endpoint = endpoint
        self.http_status_code = http_status_code
        self.message = message
        self.method = method
        self.path_name = path_name
        self.protocol = protocol
        self.req_body_type = req_body_type
        self.request_id = request_id
        self.style = style
        self.success = success
        self.timeout = timeout
        self.version = version

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.action is not None:
            result['Action'] = self.action
        if self.app is not None:
            result['App'] = self.app
        if self.code is not None:
            result['Code'] = self.code
        if self.endpoint is not None:
            result['Endpoint'] = self.endpoint
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.message is not None:
            result['Message'] = self.message
        if self.method is not None:
            result['Method'] = self.method
        if self.path_name is not None:
            result['PathName'] = self.path_name
        if self.protocol is not None:
            result['Protocol'] = self.protocol
        if self.req_body_type is not None:
            result['ReqBodyType'] = self.req_body_type
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.style is not None:
            result['Style'] = self.style
        if self.success is not None:
            result['Success'] = self.success
        if self.timeout is not None:
            result['Timeout'] = self.timeout
        if self.version is not None:
            result['Version'] = self.version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Action') is not None:
            self.action = m.get('Action')
        if m.get('App') is not None:
            self.app = m.get('App')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Endpoint') is not None:
            self.endpoint = m.get('Endpoint')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('Method') is not None:
            self.method = m.get('Method')
        if m.get('PathName') is not None:
            self.path_name = m.get('PathName')
        if m.get('Protocol') is not None:
            self.protocol = m.get('Protocol')
        if m.get('ReqBodyType') is not None:
            self.req_body_type = m.get('ReqBodyType')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Style') is not None:
            self.style = m.get('Style')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Timeout') is not None:
            self.timeout = m.get('Timeout')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        return self


class CreateEndpointResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateEndpointResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateEndpointResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateIdleInstanceCullerRequest(TeaModel):
    def __init__(
        self,
        cpu_percent_threshold: int = None,
        gpu_percent_threshold: int = None,
        max_idle_time_in_minutes: int = None,
    ):
        self.cpu_percent_threshold = cpu_percent_threshold
        self.gpu_percent_threshold = gpu_percent_threshold
        self.max_idle_time_in_minutes = max_idle_time_in_minutes

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cpu_percent_threshold is not None:
            result['CpuPercentThreshold'] = self.cpu_percent_threshold
        if self.gpu_percent_threshold is not None:
            result['GpuPercentThreshold'] = self.gpu_percent_threshold
        if self.max_idle_time_in_minutes is not None:
            result['MaxIdleTimeInMinutes'] = self.max_idle_time_in_minutes
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CpuPercentThreshold') is not None:
            self.cpu_percent_threshold = m.get('CpuPercentThreshold')
        if m.get('GpuPercentThreshold') is not None:
            self.gpu_percent_threshold = m.get('GpuPercentThreshold')
        if m.get('MaxIdleTimeInMinutes') is not None:
            self.max_idle_time_in_minutes = m.get('MaxIdleTimeInMinutes')
        return self


class CreateIdleInstanceCullerResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        instance_id: str = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.code = code
        self.instance_id = instance_id
        self.message = message
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateIdleInstanceCullerResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateIdleInstanceCullerResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateIdleInstanceCullerResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateInstanceRequestAffinityCPU(TeaModel):
    def __init__(
        self,
        enable: bool = None,
    ):
        self.enable = enable

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.enable is not None:
            result['Enable'] = self.enable
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Enable') is not None:
            self.enable = m.get('Enable')
        return self


class CreateInstanceRequestAffinity(TeaModel):
    def __init__(
        self,
        cpu: CreateInstanceRequestAffinityCPU = None,
    ):
        self.cpu = cpu

    def validate(self):
        if self.cpu:
            self.cpu.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cpu is not None:
            result['CPU'] = self.cpu.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CPU') is not None:
            temp_model = CreateInstanceRequestAffinityCPU()
            self.cpu = temp_model.from_map(m['CPU'])
        return self


class CreateInstanceRequestCloudDisksStatus(TeaModel):
    def __init__(
        self,
        available: int = None,
        capacity: int = None,
        usage: int = None,
    ):
        self.available = available
        self.capacity = capacity
        self.usage = usage

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.available is not None:
            result['Available'] = self.available
        if self.capacity is not None:
            result['Capacity'] = self.capacity
        if self.usage is not None:
            result['Usage'] = self.usage
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Available') is not None:
            self.available = m.get('Available')
        if m.get('Capacity') is not None:
            self.capacity = m.get('Capacity')
        if m.get('Usage') is not None:
            self.usage = m.get('Usage')
        return self


class CreateInstanceRequestCloudDisks(TeaModel):
    def __init__(
        self,
        capacity: str = None,
        mount_path: str = None,
        path: str = None,
        status: CreateInstanceRequestCloudDisksStatus = None,
        sub_type: str = None,
    ):
        self.capacity = capacity
        self.mount_path = mount_path
        self.path = path
        self.status = status
        self.sub_type = sub_type

    def validate(self):
        if self.status:
            self.status.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.capacity is not None:
            result['Capacity'] = self.capacity
        if self.mount_path is not None:
            result['MountPath'] = self.mount_path
        if self.path is not None:
            result['Path'] = self.path
        if self.status is not None:
            result['Status'] = self.status.to_map()
        if self.sub_type is not None:
            result['SubType'] = self.sub_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Capacity') is not None:
            self.capacity = m.get('Capacity')
        if m.get('MountPath') is not None:
            self.mount_path = m.get('MountPath')
        if m.get('Path') is not None:
            self.path = m.get('Path')
        if m.get('Status') is not None:
            temp_model = CreateInstanceRequestCloudDisksStatus()
            self.status = temp_model.from_map(m['Status'])
        if m.get('SubType') is not None:
            self.sub_type = m.get('SubType')
        return self


class CreateInstanceRequestDatasets(TeaModel):
    def __init__(
        self,
        dataset_id: str = None,
        dynamic: bool = None,
        mount_path: str = None,
        option_type: str = None,
        options: str = None,
        uri: str = None,
    ):
        self.dataset_id = dataset_id
        self.dynamic = dynamic
        self.mount_path = mount_path
        self.option_type = option_type
        self.options = options
        self.uri = uri

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.dataset_id is not None:
            result['DatasetId'] = self.dataset_id
        if self.dynamic is not None:
            result['Dynamic'] = self.dynamic
        if self.mount_path is not None:
            result['MountPath'] = self.mount_path
        if self.option_type is not None:
            result['OptionType'] = self.option_type
        if self.options is not None:
            result['Options'] = self.options
        if self.uri is not None:
            result['Uri'] = self.uri
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DatasetId') is not None:
            self.dataset_id = m.get('DatasetId')
        if m.get('Dynamic') is not None:
            self.dynamic = m.get('Dynamic')
        if m.get('MountPath') is not None:
            self.mount_path = m.get('MountPath')
        if m.get('OptionType') is not None:
            self.option_type = m.get('OptionType')
        if m.get('Options') is not None:
            self.options = m.get('Options')
        if m.get('Uri') is not None:
            self.uri = m.get('Uri')
        return self


class CreateInstanceRequestLabels(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class CreateInstanceRequestRequestedResource(TeaModel):
    def __init__(
        self,
        cpu: str = None,
        gpu: str = None,
        gputype: str = None,
        memory: str = None,
        shared_memory: str = None,
    ):
        self.cpu = cpu
        self.gpu = gpu
        self.gputype = gputype
        self.memory = memory
        self.shared_memory = shared_memory

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cpu is not None:
            result['CPU'] = self.cpu
        if self.gpu is not None:
            result['GPU'] = self.gpu
        if self.gputype is not None:
            result['GPUType'] = self.gputype
        if self.memory is not None:
            result['Memory'] = self.memory
        if self.shared_memory is not None:
            result['SharedMemory'] = self.shared_memory
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CPU') is not None:
            self.cpu = m.get('CPU')
        if m.get('GPU') is not None:
            self.gpu = m.get('GPU')
        if m.get('GPUType') is not None:
            self.gputype = m.get('GPUType')
        if m.get('Memory') is not None:
            self.memory = m.get('Memory')
        if m.get('SharedMemory') is not None:
            self.shared_memory = m.get('SharedMemory')
        return self


class CreateInstanceRequestUserVpc(TeaModel):
    def __init__(
        self,
        default_route: str = None,
        extended_cidrs: List[str] = None,
        forward_infos: List[ForwardInfo] = None,
        security_group_id: str = None,
        v_switch_id: str = None,
        vpc_id: str = None,
    ):
        self.default_route = default_route
        self.extended_cidrs = extended_cidrs
        self.forward_infos = forward_infos
        self.security_group_id = security_group_id
        self.v_switch_id = v_switch_id
        self.vpc_id = vpc_id

    def validate(self):
        if self.forward_infos:
            for k in self.forward_infos:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.default_route is not None:
            result['DefaultRoute'] = self.default_route
        if self.extended_cidrs is not None:
            result['ExtendedCIDRs'] = self.extended_cidrs
        result['ForwardInfos'] = []
        if self.forward_infos is not None:
            for k in self.forward_infos:
                result['ForwardInfos'].append(k.to_map() if k else None)
        if self.security_group_id is not None:
            result['SecurityGroupId'] = self.security_group_id
        if self.v_switch_id is not None:
            result['VSwitchId'] = self.v_switch_id
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DefaultRoute') is not None:
            self.default_route = m.get('DefaultRoute')
        if m.get('ExtendedCIDRs') is not None:
            self.extended_cidrs = m.get('ExtendedCIDRs')
        self.forward_infos = []
        if m.get('ForwardInfos') is not None:
            for k in m.get('ForwardInfos'):
                temp_model = ForwardInfo()
                self.forward_infos.append(temp_model.from_map(k))
        if m.get('SecurityGroupId') is not None:
            self.security_group_id = m.get('SecurityGroupId')
        if m.get('VSwitchId') is not None:
            self.v_switch_id = m.get('VSwitchId')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        return self


class CreateInstanceRequest(TeaModel):
    def __init__(
        self,
        accessibility: str = None,
        affinity: CreateInstanceRequestAffinity = None,
        cloud_disks: List[CreateInstanceRequestCloudDisks] = None,
        credential_config: CredentialConfig = None,
        datasets: List[CreateInstanceRequestDatasets] = None,
        driver: str = None,
        dynamic_mount: DynamicMount = None,
        ecs_spec: str = None,
        environment_variables: Dict[str, str] = None,
        image_auth: str = None,
        image_id: str = None,
        image_url: str = None,
        instance_name: str = None,
        labels: List[CreateInstanceRequestLabels] = None,
        priority: int = None,
        requested_resource: CreateInstanceRequestRequestedResource = None,
        resource_id: str = None,
        system_image_url: str = None,
        user_id: str = None,
        user_vpc: CreateInstanceRequestUserVpc = None,
        workspace_id: str = None,
        workspace_source: str = None,
    ):
        self.accessibility = accessibility
        self.affinity = affinity
        self.cloud_disks = cloud_disks
        self.credential_config = credential_config
        self.datasets = datasets
        self.driver = driver
        self.dynamic_mount = dynamic_mount
        self.ecs_spec = ecs_spec
        self.environment_variables = environment_variables
        self.image_auth = image_auth
        self.image_id = image_id
        self.image_url = image_url
        self.instance_name = instance_name
        self.labels = labels
        self.priority = priority
        self.requested_resource = requested_resource
        self.resource_id = resource_id
        self.system_image_url = system_image_url
        self.user_id = user_id
        self.user_vpc = user_vpc
        self.workspace_id = workspace_id
        self.workspace_source = workspace_source

    def validate(self):
        if self.affinity:
            self.affinity.validate()
        if self.cloud_disks:
            for k in self.cloud_disks:
                if k:
                    k.validate()
        if self.credential_config:
            self.credential_config.validate()
        if self.datasets:
            for k in self.datasets:
                if k:
                    k.validate()
        if self.dynamic_mount:
            self.dynamic_mount.validate()
        if self.labels:
            for k in self.labels:
                if k:
                    k.validate()
        if self.requested_resource:
            self.requested_resource.validate()
        if self.user_vpc:
            self.user_vpc.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.accessibility is not None:
            result['Accessibility'] = self.accessibility
        if self.affinity is not None:
            result['Affinity'] = self.affinity.to_map()
        result['CloudDisks'] = []
        if self.cloud_disks is not None:
            for k in self.cloud_disks:
                result['CloudDisks'].append(k.to_map() if k else None)
        if self.credential_config is not None:
            result['CredentialConfig'] = self.credential_config.to_map()
        result['Datasets'] = []
        if self.datasets is not None:
            for k in self.datasets:
                result['Datasets'].append(k.to_map() if k else None)
        if self.driver is not None:
            result['Driver'] = self.driver
        if self.dynamic_mount is not None:
            result['DynamicMount'] = self.dynamic_mount.to_map()
        if self.ecs_spec is not None:
            result['EcsSpec'] = self.ecs_spec
        if self.environment_variables is not None:
            result['EnvironmentVariables'] = self.environment_variables
        if self.image_auth is not None:
            result['ImageAuth'] = self.image_auth
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.image_url is not None:
            result['ImageUrl'] = self.image_url
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.requested_resource is not None:
            result['RequestedResource'] = self.requested_resource.to_map()
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.system_image_url is not None:
            result['SystemImageUrl'] = self.system_image_url
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.user_vpc is not None:
            result['UserVpc'] = self.user_vpc.to_map()
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        if self.workspace_source is not None:
            result['WorkspaceSource'] = self.workspace_source
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Accessibility') is not None:
            self.accessibility = m.get('Accessibility')
        if m.get('Affinity') is not None:
            temp_model = CreateInstanceRequestAffinity()
            self.affinity = temp_model.from_map(m['Affinity'])
        self.cloud_disks = []
        if m.get('CloudDisks') is not None:
            for k in m.get('CloudDisks'):
                temp_model = CreateInstanceRequestCloudDisks()
                self.cloud_disks.append(temp_model.from_map(k))
        if m.get('CredentialConfig') is not None:
            temp_model = CredentialConfig()
            self.credential_config = temp_model.from_map(m['CredentialConfig'])
        self.datasets = []
        if m.get('Datasets') is not None:
            for k in m.get('Datasets'):
                temp_model = CreateInstanceRequestDatasets()
                self.datasets.append(temp_model.from_map(k))
        if m.get('Driver') is not None:
            self.driver = m.get('Driver')
        if m.get('DynamicMount') is not None:
            temp_model = DynamicMount()
            self.dynamic_mount = temp_model.from_map(m['DynamicMount'])
        if m.get('EcsSpec') is not None:
            self.ecs_spec = m.get('EcsSpec')
        if m.get('EnvironmentVariables') is not None:
            self.environment_variables = m.get('EnvironmentVariables')
        if m.get('ImageAuth') is not None:
            self.image_auth = m.get('ImageAuth')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('ImageUrl') is not None:
            self.image_url = m.get('ImageUrl')
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = CreateInstanceRequestLabels()
                self.labels.append(temp_model.from_map(k))
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('RequestedResource') is not None:
            temp_model = CreateInstanceRequestRequestedResource()
            self.requested_resource = temp_model.from_map(m['RequestedResource'])
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('SystemImageUrl') is not None:
            self.system_image_url = m.get('SystemImageUrl')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('UserVpc') is not None:
            temp_model = CreateInstanceRequestUserVpc()
            self.user_vpc = temp_model.from_map(m['UserVpc'])
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        if m.get('WorkspaceSource') is not None:
            self.workspace_source = m.get('WorkspaceSource')
        return self


class CreateInstanceResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        http_status_code: int = None,
        instance_id: str = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.code = code
        self.http_status_code = http_status_code
        self.instance_id = instance_id
        self.message = message
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateInstanceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateInstanceShutdownTimerRequest(TeaModel):
    def __init__(
        self,
        due_time: str = None,
        remaining_time_in_ms: int = None,
    ):
        self.due_time = due_time
        self.remaining_time_in_ms = remaining_time_in_ms

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.due_time is not None:
            result['DueTime'] = self.due_time
        if self.remaining_time_in_ms is not None:
            result['RemainingTimeInMs'] = self.remaining_time_in_ms
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DueTime') is not None:
            self.due_time = m.get('DueTime')
        if m.get('RemainingTimeInMs') is not None:
            self.remaining_time_in_ms = m.get('RemainingTimeInMs')
        return self


class CreateInstanceShutdownTimerResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        http_status_code: int = None,
        instance_id: str = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.code = code
        self.http_status_code = http_status_code
        self.instance_id = instance_id
        self.message = message
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateInstanceShutdownTimerResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateInstanceShutdownTimerResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateInstanceShutdownTimerResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateInstanceSnapshotRequestLabels(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class CreateInstanceSnapshotRequest(TeaModel):
    def __init__(
        self,
        exclude_paths: List[str] = None,
        image_url: str = None,
        labels: List[CreateInstanceSnapshotRequestLabels] = None,
        overwrite: bool = None,
        snapshot_description: str = None,
        snapshot_name: str = None,
    ):
        self.exclude_paths = exclude_paths
        self.image_url = image_url
        self.labels = labels
        self.overwrite = overwrite
        self.snapshot_description = snapshot_description
        self.snapshot_name = snapshot_name

    def validate(self):
        if self.labels:
            for k in self.labels:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.exclude_paths is not None:
            result['ExcludePaths'] = self.exclude_paths
        if self.image_url is not None:
            result['ImageUrl'] = self.image_url
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        if self.overwrite is not None:
            result['Overwrite'] = self.overwrite
        if self.snapshot_description is not None:
            result['SnapshotDescription'] = self.snapshot_description
        if self.snapshot_name is not None:
            result['SnapshotName'] = self.snapshot_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ExcludePaths') is not None:
            self.exclude_paths = m.get('ExcludePaths')
        if m.get('ImageUrl') is not None:
            self.image_url = m.get('ImageUrl')
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = CreateInstanceSnapshotRequestLabels()
                self.labels.append(temp_model.from_map(k))
        if m.get('Overwrite') is not None:
            self.overwrite = m.get('Overwrite')
        if m.get('SnapshotDescription') is not None:
            self.snapshot_description = m.get('SnapshotDescription')
        if m.get('SnapshotName') is not None:
            self.snapshot_name = m.get('SnapshotName')
        return self


class CreateInstanceSnapshotResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        http_status_code: int = None,
        instance_id: str = None,
        message: str = None,
        request_id: str = None,
        snapshot_id: str = None,
        success: bool = None,
    ):
        self.code = code
        self.http_status_code = http_status_code
        self.instance_id = instance_id
        self.message = message
        self.request_id = request_id
        self.snapshot_id = snapshot_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.snapshot_id is not None:
            result['SnapshotId'] = self.snapshot_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('SnapshotId') is not None:
            self.snapshot_id = m.get('SnapshotId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateInstanceSnapshotResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateInstanceSnapshotResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateInstanceSnapshotResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateShareRequest(TeaModel):
    def __init__(
        self,
        file_name: str = None,
        ttl: int = None,
        version: str = None,
    ):
        self.file_name = file_name
        self.ttl = ttl
        self.version = version

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.file_name is not None:
            result['FileName'] = self.file_name
        if self.ttl is not None:
            result['Ttl'] = self.ttl
        if self.version is not None:
            result['Version'] = self.version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FileName') is not None:
            self.file_name = m.get('FileName')
        if m.get('Ttl') is not None:
            self.ttl = m.get('Ttl')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        return self


class CreateShareResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        expiration_time: str = None,
        file_name: str = None,
        gmt_create_time: str = None,
        gmt_modified_time: str = None,
        http_status_code: int = None,
        message: str = None,
        request_id: str = None,
        resource_url: str = None,
        success: bool = None,
        ttl: int = None,
        user_id: str = None,
        version: str = None,
    ):
        self.code = code
        self.expiration_time = expiration_time
        self.file_name = file_name
        self.gmt_create_time = gmt_create_time
        self.gmt_modified_time = gmt_modified_time
        self.http_status_code = http_status_code
        self.message = message
        self.request_id = request_id
        self.resource_url = resource_url
        self.success = success
        self.ttl = ttl
        self.user_id = user_id
        self.version = version

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.expiration_time is not None:
            result['ExpirationTime'] = self.expiration_time
        if self.file_name is not None:
            result['FileName'] = self.file_name
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.resource_url is not None:
            result['ResourceUrl'] = self.resource_url
        if self.success is not None:
            result['Success'] = self.success
        if self.ttl is not None:
            result['Ttl'] = self.ttl
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.version is not None:
            result['Version'] = self.version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('ExpirationTime') is not None:
            self.expiration_time = m.get('ExpirationTime')
        if m.get('FileName') is not None:
            self.file_name = m.get('FileName')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ResourceUrl') is not None:
            self.resource_url = m.get('ResourceUrl')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Ttl') is not None:
            self.ttl = m.get('Ttl')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        return self


class CreateShareResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateShareResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateShareResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateTempFileRequest(TeaModel):
    def __init__(
        self,
        capacity: int = None,
        instance_id: str = None,
        name: str = None,
        prefix: str = None,
        task_id: str = None,
    ):
        self.capacity = capacity
        self.instance_id = instance_id
        self.name = name
        self.prefix = prefix
        self.task_id = task_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.capacity is not None:
            result['Capacity'] = self.capacity
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.name is not None:
            result['Name'] = self.name
        if self.prefix is not None:
            result['Prefix'] = self.prefix
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Capacity') is not None:
            self.capacity = m.get('Capacity')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Prefix') is not None:
            self.prefix = m.get('Prefix')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        return self


class CreateTempFileResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        http_status_code: int = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
        temp_file_id: str = None,
    ):
        self.code = code
        self.http_status_code = http_status_code
        self.message = message
        self.request_id = request_id
        self.success = success
        self.temp_file_id = temp_file_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.temp_file_id is not None:
            result['TempFileId'] = self.temp_file_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('TempFileId') is not None:
            self.temp_file_id = m.get('TempFileId')
        return self


class CreateTempFileResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateTempFileResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateTempFileResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateTempFileTaskRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
    ):
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class CreateTempFileTaskResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        http_status_code: int = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
        temp_file_task_id: str = None,
    ):
        self.code = code
        self.http_status_code = http_status_code
        self.message = message
        self.request_id = request_id
        self.success = success
        self.temp_file_task_id = temp_file_task_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.temp_file_task_id is not None:
            result['TempFileTaskId'] = self.temp_file_task_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('TempFileTaskId') is not None:
            self.temp_file_task_id = m.get('TempFileTaskId')
        return self


class CreateTempFileTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateTempFileTaskResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateTempFileTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteIdleInstanceCullerResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        instance_id: str = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.code = code
        self.instance_id = instance_id
        self.message = message
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteIdleInstanceCullerResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteIdleInstanceCullerResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteIdleInstanceCullerResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteInstanceResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        http_status_code: int = None,
        instance_id: str = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.code = code
        self.http_status_code = http_status_code
        self.instance_id = instance_id
        self.message = message
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteInstanceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteInstanceLabelsRequest(TeaModel):
    def __init__(
        self,
        label_keys: str = None,
    ):
        # This parameter is required.
        self.label_keys = label_keys

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.label_keys is not None:
            result['LabelKeys'] = self.label_keys
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LabelKeys') is not None:
            self.label_keys = m.get('LabelKeys')
        return self


class DeleteInstanceLabelsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteInstanceLabelsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteInstanceLabelsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteInstanceLabelsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteInstanceShutdownTimerResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        http_status_code: int = None,
        instance_id: str = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.code = code
        self.http_status_code = http_status_code
        self.instance_id = instance_id
        self.message = message
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteInstanceShutdownTimerResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteInstanceShutdownTimerResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteInstanceShutdownTimerResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteInstanceSnapshotResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        http_status_code: int = None,
        instance_id: str = None,
        message: str = None,
        request_id: str = None,
        snapshot_id: str = None,
        success: bool = None,
    ):
        self.code = code
        self.http_status_code = http_status_code
        self.instance_id = instance_id
        self.message = message
        self.request_id = request_id
        self.snapshot_id = snapshot_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.snapshot_id is not None:
            result['SnapshotId'] = self.snapshot_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('SnapshotId') is not None:
            self.snapshot_id = m.get('SnapshotId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteInstanceSnapshotResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteInstanceSnapshotResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteInstanceSnapshotResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteTempFileResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        http_status_code: int = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
        temp_file_id: str = None,
    ):
        self.code = code
        self.http_status_code = http_status_code
        self.message = message
        self.request_id = request_id
        self.success = success
        self.temp_file_id = temp_file_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.temp_file_id is not None:
            result['TempFileId'] = self.temp_file_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('TempFileId') is not None:
            self.temp_file_id = m.get('TempFileId')
        return self


class DeleteTempFileResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteTempFileResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteTempFileResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteTempFileTaskResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        http_status_code: int = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
        temp_file_task_id: str = None,
    ):
        self.code = code
        self.http_status_code = http_status_code
        self.message = message
        self.request_id = request_id
        self.success = success
        self.temp_file_task_id = temp_file_task_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.temp_file_task_id is not None:
            result['TempFileTaskId'] = self.temp_file_task_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('TempFileTaskId') is not None:
            self.temp_file_task_id = m.get('TempFileTaskId')
        return self


class DeleteTempFileTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteTempFileTaskResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteTempFileTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetIdleInstanceCullerResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        cpu_percent_threshold: int = None,
        gpu_percent_threshold: int = None,
        idle_time_in_minutes: int = None,
        instance_id: str = None,
        max_idle_time_in_minutes: int = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.code = code
        self.cpu_percent_threshold = cpu_percent_threshold
        self.gpu_percent_threshold = gpu_percent_threshold
        self.idle_time_in_minutes = idle_time_in_minutes
        self.instance_id = instance_id
        self.max_idle_time_in_minutes = max_idle_time_in_minutes
        self.message = message
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.cpu_percent_threshold is not None:
            result['CpuPercentThreshold'] = self.cpu_percent_threshold
        if self.gpu_percent_threshold is not None:
            result['GpuPercentThreshold'] = self.gpu_percent_threshold
        if self.idle_time_in_minutes is not None:
            result['IdleTimeInMinutes'] = self.idle_time_in_minutes
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.max_idle_time_in_minutes is not None:
            result['MaxIdleTimeInMinutes'] = self.max_idle_time_in_minutes
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('CpuPercentThreshold') is not None:
            self.cpu_percent_threshold = m.get('CpuPercentThreshold')
        if m.get('GpuPercentThreshold') is not None:
            self.gpu_percent_threshold = m.get('GpuPercentThreshold')
        if m.get('IdleTimeInMinutes') is not None:
            self.idle_time_in_minutes = m.get('IdleTimeInMinutes')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('MaxIdleTimeInMinutes') is not None:
            self.max_idle_time_in_minutes = m.get('MaxIdleTimeInMinutes')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class GetIdleInstanceCullerResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetIdleInstanceCullerResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetIdleInstanceCullerResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetInstanceResponseBodyAffinityCPU(TeaModel):
    def __init__(
        self,
        enable: bool = None,
    ):
        self.enable = enable

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.enable is not None:
            result['Enable'] = self.enable
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Enable') is not None:
            self.enable = m.get('Enable')
        return self


class GetInstanceResponseBodyAffinity(TeaModel):
    def __init__(
        self,
        cpu: GetInstanceResponseBodyAffinityCPU = None,
    ):
        self.cpu = cpu

    def validate(self):
        if self.cpu:
            self.cpu.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cpu is not None:
            result['CPU'] = self.cpu.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CPU') is not None:
            temp_model = GetInstanceResponseBodyAffinityCPU()
            self.cpu = temp_model.from_map(m['CPU'])
        return self


class GetInstanceResponseBodyCloudDisks(TeaModel):
    def __init__(
        self,
        capacity: str = None,
        mount_path: str = None,
        path: str = None,
        sub_type: str = None,
    ):
        self.capacity = capacity
        self.mount_path = mount_path
        self.path = path
        self.sub_type = sub_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.capacity is not None:
            result['Capacity'] = self.capacity
        if self.mount_path is not None:
            result['MountPath'] = self.mount_path
        if self.path is not None:
            result['Path'] = self.path
        if self.sub_type is not None:
            result['SubType'] = self.sub_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Capacity') is not None:
            self.capacity = m.get('Capacity')
        if m.get('MountPath') is not None:
            self.mount_path = m.get('MountPath')
        if m.get('Path') is not None:
            self.path = m.get('Path')
        if m.get('SubType') is not None:
            self.sub_type = m.get('SubType')
        return self


class GetInstanceResponseBodyDatasets(TeaModel):
    def __init__(
        self,
        dataset_id: str = None,
        dynamic: bool = None,
        mount_path: str = None,
        option_type: str = None,
        options: str = None,
        uri: str = None,
    ):
        self.dataset_id = dataset_id
        self.dynamic = dynamic
        self.mount_path = mount_path
        self.option_type = option_type
        self.options = options
        self.uri = uri

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.dataset_id is not None:
            result['DatasetId'] = self.dataset_id
        if self.dynamic is not None:
            result['Dynamic'] = self.dynamic
        if self.mount_path is not None:
            result['MountPath'] = self.mount_path
        if self.option_type is not None:
            result['OptionType'] = self.option_type
        if self.options is not None:
            result['Options'] = self.options
        if self.uri is not None:
            result['Uri'] = self.uri
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DatasetId') is not None:
            self.dataset_id = m.get('DatasetId')
        if m.get('Dynamic') is not None:
            self.dynamic = m.get('Dynamic')
        if m.get('MountPath') is not None:
            self.mount_path = m.get('MountPath')
        if m.get('OptionType') is not None:
            self.option_type = m.get('OptionType')
        if m.get('Options') is not None:
            self.options = m.get('Options')
        if m.get('Uri') is not None:
            self.uri = m.get('Uri')
        return self


class GetInstanceResponseBodyIdleInstanceCuller(TeaModel):
    def __init__(
        self,
        cpu_percent_threshold: int = None,
        gpu_percent_threshold: int = None,
        idle_time_in_minutes: int = None,
        instance_id: str = None,
        max_idle_time_in_minutes: int = None,
    ):
        self.cpu_percent_threshold = cpu_percent_threshold
        self.gpu_percent_threshold = gpu_percent_threshold
        self.idle_time_in_minutes = idle_time_in_minutes
        self.instance_id = instance_id
        self.max_idle_time_in_minutes = max_idle_time_in_minutes

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cpu_percent_threshold is not None:
            result['CpuPercentThreshold'] = self.cpu_percent_threshold
        if self.gpu_percent_threshold is not None:
            result['GpuPercentThreshold'] = self.gpu_percent_threshold
        if self.idle_time_in_minutes is not None:
            result['IdleTimeInMinutes'] = self.idle_time_in_minutes
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.max_idle_time_in_minutes is not None:
            result['MaxIdleTimeInMinutes'] = self.max_idle_time_in_minutes
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CpuPercentThreshold') is not None:
            self.cpu_percent_threshold = m.get('CpuPercentThreshold')
        if m.get('GpuPercentThreshold') is not None:
            self.gpu_percent_threshold = m.get('GpuPercentThreshold')
        if m.get('IdleTimeInMinutes') is not None:
            self.idle_time_in_minutes = m.get('IdleTimeInMinutes')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('MaxIdleTimeInMinutes') is not None:
            self.max_idle_time_in_minutes = m.get('MaxIdleTimeInMinutes')
        return self


class GetInstanceResponseBodyInstanceShutdownTimer(TeaModel):
    def __init__(
        self,
        due_time: str = None,
        gmt_create_time: str = None,
        gmt_modified_time: str = None,
        instance_id: str = None,
        remaining_time_in_ms: int = None,
    ):
        self.due_time = due_time
        self.gmt_create_time = gmt_create_time
        self.gmt_modified_time = gmt_modified_time
        self.instance_id = instance_id
        self.remaining_time_in_ms = remaining_time_in_ms

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.due_time is not None:
            result['DueTime'] = self.due_time
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.remaining_time_in_ms is not None:
            result['RemainingTimeInMs'] = self.remaining_time_in_ms
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DueTime') is not None:
            self.due_time = m.get('DueTime')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('RemainingTimeInMs') is not None:
            self.remaining_time_in_ms = m.get('RemainingTimeInMs')
        return self


class GetInstanceResponseBodyInstanceSnapshotList(TeaModel):
    def __init__(
        self,
        gmt_create_time: str = None,
        gmt_modified_time: str = None,
        image_id: str = None,
        image_name: str = None,
        image_url: str = None,
        reason_code: str = None,
        reason_message: str = None,
        repository_url: str = None,
        status: str = None,
    ):
        # 快照创建时间
        self.gmt_create_time = gmt_create_time
        # 快照修改时间
        self.gmt_modified_time = gmt_modified_time
        # 镜像Id
        self.image_id = image_id
        # 镜像名称
        self.image_name = image_name
        # 镜像Url
        self.image_url = image_url
        # 实例快照错误代码
        self.reason_code = reason_code
        # 实例快照错误消息
        self.reason_message = reason_message
        # 镜像仓库Url
        self.repository_url = repository_url
        # 实例快照状态
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.image_name is not None:
            result['ImageName'] = self.image_name
        if self.image_url is not None:
            result['ImageUrl'] = self.image_url
        if self.reason_code is not None:
            result['ReasonCode'] = self.reason_code
        if self.reason_message is not None:
            result['ReasonMessage'] = self.reason_message
        if self.repository_url is not None:
            result['RepositoryUrl'] = self.repository_url
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('ImageName') is not None:
            self.image_name = m.get('ImageName')
        if m.get('ImageUrl') is not None:
            self.image_url = m.get('ImageUrl')
        if m.get('ReasonCode') is not None:
            self.reason_code = m.get('ReasonCode')
        if m.get('ReasonMessage') is not None:
            self.reason_message = m.get('ReasonMessage')
        if m.get('RepositoryUrl') is not None:
            self.repository_url = m.get('RepositoryUrl')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class GetInstanceResponseBodyLabels(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class GetInstanceResponseBodyLatestSnapshot(TeaModel):
    def __init__(
        self,
        gmt_create_time: str = None,
        gmt_modified_time: str = None,
        image_id: str = None,
        image_name: str = None,
        image_url: str = None,
        reason_code: str = None,
        reason_message: str = None,
        repository_url: str = None,
        status: str = None,
    ):
        self.gmt_create_time = gmt_create_time
        self.gmt_modified_time = gmt_modified_time
        self.image_id = image_id
        self.image_name = image_name
        self.image_url = image_url
        # 实例快照错误代码
        self.reason_code = reason_code
        # 实例快照错误消息
        self.reason_message = reason_message
        self.repository_url = repository_url
        # 实例快照状态
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.image_name is not None:
            result['ImageName'] = self.image_name
        if self.image_url is not None:
            result['ImageUrl'] = self.image_url
        if self.reason_code is not None:
            result['ReasonCode'] = self.reason_code
        if self.reason_message is not None:
            result['ReasonMessage'] = self.reason_message
        if self.repository_url is not None:
            result['RepositoryUrl'] = self.repository_url
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('ImageName') is not None:
            self.image_name = m.get('ImageName')
        if m.get('ImageUrl') is not None:
            self.image_url = m.get('ImageUrl')
        if m.get('ReasonCode') is not None:
            self.reason_code = m.get('ReasonCode')
        if m.get('ReasonMessage') is not None:
            self.reason_message = m.get('ReasonMessage')
        if m.get('RepositoryUrl') is not None:
            self.repository_url = m.get('RepositoryUrl')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class GetInstanceResponseBodyNodeErrorRecovery(TeaModel):
    def __init__(
        self,
        auto_switch_countdown_seconds: int = None,
        enable_auto_switch_on_node_error: bool = None,
        has_node_error: bool = None,
    ):
        self.auto_switch_countdown_seconds = auto_switch_countdown_seconds
        self.enable_auto_switch_on_node_error = enable_auto_switch_on_node_error
        self.has_node_error = has_node_error

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.auto_switch_countdown_seconds is not None:
            result['autoSwitchCountdownSeconds'] = self.auto_switch_countdown_seconds
        if self.enable_auto_switch_on_node_error is not None:
            result['enableAutoSwitchOnNodeError'] = self.enable_auto_switch_on_node_error
        if self.has_node_error is not None:
            result['hasNodeError'] = self.has_node_error
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('autoSwitchCountdownSeconds') is not None:
            self.auto_switch_countdown_seconds = m.get('autoSwitchCountdownSeconds')
        if m.get('enableAutoSwitchOnNodeError') is not None:
            self.enable_auto_switch_on_node_error = m.get('enableAutoSwitchOnNodeError')
        if m.get('hasNodeError') is not None:
            self.has_node_error = m.get('hasNodeError')
        return self


class GetInstanceResponseBodyRequestedResource(TeaModel):
    def __init__(
        self,
        cpu: str = None,
        gpu: str = None,
        gputype: str = None,
        memory: str = None,
        shared_memory: str = None,
    ):
        self.cpu = cpu
        self.gpu = gpu
        self.gputype = gputype
        self.memory = memory
        self.shared_memory = shared_memory

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cpu is not None:
            result['CPU'] = self.cpu
        if self.gpu is not None:
            result['GPU'] = self.gpu
        if self.gputype is not None:
            result['GPUType'] = self.gputype
        if self.memory is not None:
            result['Memory'] = self.memory
        if self.shared_memory is not None:
            result['SharedMemory'] = self.shared_memory
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CPU') is not None:
            self.cpu = m.get('CPU')
        if m.get('GPU') is not None:
            self.gpu = m.get('GPU')
        if m.get('GPUType') is not None:
            self.gputype = m.get('GPUType')
        if m.get('Memory') is not None:
            self.memory = m.get('Memory')
        if m.get('SharedMemory') is not None:
            self.shared_memory = m.get('SharedMemory')
        return self


class GetInstanceResponseBodyUserVpc(TeaModel):
    def __init__(
        self,
        default_route: str = None,
        extended_cidrs: List[str] = None,
        forward_infos: List[ForwardInfoResponse] = None,
        security_group_id: str = None,
        v_switch_id: str = None,
        vpc_id: str = None,
    ):
        self.default_route = default_route
        self.extended_cidrs = extended_cidrs
        self.forward_infos = forward_infos
        self.security_group_id = security_group_id
        self.v_switch_id = v_switch_id
        # Vpc Id。
        self.vpc_id = vpc_id

    def validate(self):
        if self.forward_infos:
            for k in self.forward_infos:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.default_route is not None:
            result['DefaultRoute'] = self.default_route
        if self.extended_cidrs is not None:
            result['ExtendedCIDRs'] = self.extended_cidrs
        result['ForwardInfos'] = []
        if self.forward_infos is not None:
            for k in self.forward_infos:
                result['ForwardInfos'].append(k.to_map() if k else None)
        if self.security_group_id is not None:
            result['SecurityGroupId'] = self.security_group_id
        if self.v_switch_id is not None:
            result['VSwitchId'] = self.v_switch_id
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DefaultRoute') is not None:
            self.default_route = m.get('DefaultRoute')
        if m.get('ExtendedCIDRs') is not None:
            self.extended_cidrs = m.get('ExtendedCIDRs')
        self.forward_infos = []
        if m.get('ForwardInfos') is not None:
            for k in m.get('ForwardInfos'):
                temp_model = ForwardInfoResponse()
                self.forward_infos.append(temp_model.from_map(k))
        if m.get('SecurityGroupId') is not None:
            self.security_group_id = m.get('SecurityGroupId')
        if m.get('VSwitchId') is not None:
            self.v_switch_id = m.get('VSwitchId')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        return self


class GetInstanceResponseBody(TeaModel):
    def __init__(
        self,
        accelerator_type: str = None,
        accessibility: str = None,
        accumulated_running_time_in_ms: int = None,
        affinity: GetInstanceResponseBodyAffinity = None,
        cloud_disks: List[GetInstanceResponseBodyCloudDisks] = None,
        code: str = None,
        datasets: List[GetInstanceResponseBodyDatasets] = None,
        driver: str = None,
        dynamic_mount: DynamicMount = None,
        ecs_spec: str = None,
        environment_variables: Dict[str, str] = None,
        gmt_create_time: str = None,
        gmt_modified_time: str = None,
        http_status_code: int = None,
        idle_instance_culler: GetInstanceResponseBodyIdleInstanceCuller = None,
        image_auth: str = None,
        image_id: str = None,
        image_name: str = None,
        image_url: str = None,
        instance_id: str = None,
        instance_name: str = None,
        instance_shutdown_timer: GetInstanceResponseBodyInstanceShutdownTimer = None,
        instance_snapshot_list: List[GetInstanceResponseBodyInstanceSnapshotList] = None,
        instance_url: str = None,
        jupyterlab_url: str = None,
        labels: List[GetInstanceResponseBodyLabels] = None,
        latest_snapshot: GetInstanceResponseBodyLatestSnapshot = None,
        message: str = None,
        node_error_recovery: GetInstanceResponseBodyNodeErrorRecovery = None,
        payment_type: str = None,
        priority: int = None,
        reason_code: str = None,
        reason_message: str = None,
        request_id: str = None,
        requested_resource: GetInstanceResponseBodyRequestedResource = None,
        resource_id: str = None,
        resource_name: str = None,
        status: str = None,
        success: bool = None,
        system_image_url: str = None,
        terminal_url: str = None,
        user_id: str = None,
        user_name: str = None,
        user_vpc: GetInstanceResponseBodyUserVpc = None,
        web_ideurl: str = None,
        workspace_id: str = None,
        workspace_name: str = None,
        workspace_source: str = None,
    ):
        self.accelerator_type = accelerator_type
        self.accessibility = accessibility
        self.accumulated_running_time_in_ms = accumulated_running_time_in_ms
        self.affinity = affinity
        self.cloud_disks = cloud_disks
        self.code = code
        self.datasets = datasets
        self.driver = driver
        self.dynamic_mount = dynamic_mount
        self.ecs_spec = ecs_spec
        self.environment_variables = environment_variables
        self.gmt_create_time = gmt_create_time
        self.gmt_modified_time = gmt_modified_time
        self.http_status_code = http_status_code
        self.idle_instance_culler = idle_instance_culler
        self.image_auth = image_auth
        self.image_id = image_id
        self.image_name = image_name
        self.image_url = image_url
        self.instance_id = instance_id
        self.instance_name = instance_name
        self.instance_shutdown_timer = instance_shutdown_timer
        self.instance_snapshot_list = instance_snapshot_list
        self.instance_url = instance_url
        # Jupyterlab Url。
        self.jupyterlab_url = jupyterlab_url
        self.labels = labels
        self.latest_snapshot = latest_snapshot
        self.message = message
        self.node_error_recovery = node_error_recovery
        self.payment_type = payment_type
        self.priority = priority
        self.reason_code = reason_code
        self.reason_message = reason_message
        self.request_id = request_id
        self.requested_resource = requested_resource
        self.resource_id = resource_id
        self.resource_name = resource_name
        self.status = status
        self.success = success
        self.system_image_url = system_image_url
        self.terminal_url = terminal_url
        self.user_id = user_id
        self.user_name = user_name
        self.user_vpc = user_vpc
        # Web IDE url。
        self.web_ideurl = web_ideurl
        self.workspace_id = workspace_id
        self.workspace_name = workspace_name
        self.workspace_source = workspace_source

    def validate(self):
        if self.affinity:
            self.affinity.validate()
        if self.cloud_disks:
            for k in self.cloud_disks:
                if k:
                    k.validate()
        if self.datasets:
            for k in self.datasets:
                if k:
                    k.validate()
        if self.dynamic_mount:
            self.dynamic_mount.validate()
        if self.idle_instance_culler:
            self.idle_instance_culler.validate()
        if self.instance_shutdown_timer:
            self.instance_shutdown_timer.validate()
        if self.instance_snapshot_list:
            for k in self.instance_snapshot_list:
                if k:
                    k.validate()
        if self.labels:
            for k in self.labels:
                if k:
                    k.validate()
        if self.latest_snapshot:
            self.latest_snapshot.validate()
        if self.node_error_recovery:
            self.node_error_recovery.validate()
        if self.requested_resource:
            self.requested_resource.validate()
        if self.user_vpc:
            self.user_vpc.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.accelerator_type is not None:
            result['AcceleratorType'] = self.accelerator_type
        if self.accessibility is not None:
            result['Accessibility'] = self.accessibility
        if self.accumulated_running_time_in_ms is not None:
            result['AccumulatedRunningTimeInMs'] = self.accumulated_running_time_in_ms
        if self.affinity is not None:
            result['Affinity'] = self.affinity.to_map()
        result['CloudDisks'] = []
        if self.cloud_disks is not None:
            for k in self.cloud_disks:
                result['CloudDisks'].append(k.to_map() if k else None)
        if self.code is not None:
            result['Code'] = self.code
        result['Datasets'] = []
        if self.datasets is not None:
            for k in self.datasets:
                result['Datasets'].append(k.to_map() if k else None)
        if self.driver is not None:
            result['Driver'] = self.driver
        if self.dynamic_mount is not None:
            result['DynamicMount'] = self.dynamic_mount.to_map()
        if self.ecs_spec is not None:
            result['EcsSpec'] = self.ecs_spec
        if self.environment_variables is not None:
            result['EnvironmentVariables'] = self.environment_variables
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.idle_instance_culler is not None:
            result['IdleInstanceCuller'] = self.idle_instance_culler.to_map()
        if self.image_auth is not None:
            result['ImageAuth'] = self.image_auth
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.image_name is not None:
            result['ImageName'] = self.image_name
        if self.image_url is not None:
            result['ImageUrl'] = self.image_url
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        if self.instance_shutdown_timer is not None:
            result['InstanceShutdownTimer'] = self.instance_shutdown_timer.to_map()
        result['InstanceSnapshotList'] = []
        if self.instance_snapshot_list is not None:
            for k in self.instance_snapshot_list:
                result['InstanceSnapshotList'].append(k.to_map() if k else None)
        if self.instance_url is not None:
            result['InstanceUrl'] = self.instance_url
        if self.jupyterlab_url is not None:
            result['JupyterlabUrl'] = self.jupyterlab_url
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        if self.latest_snapshot is not None:
            result['LatestSnapshot'] = self.latest_snapshot.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.node_error_recovery is not None:
            result['NodeErrorRecovery'] = self.node_error_recovery.to_map()
        if self.payment_type is not None:
            result['PaymentType'] = self.payment_type
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.reason_code is not None:
            result['ReasonCode'] = self.reason_code
        if self.reason_message is not None:
            result['ReasonMessage'] = self.reason_message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.requested_resource is not None:
            result['RequestedResource'] = self.requested_resource.to_map()
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_name is not None:
            result['ResourceName'] = self.resource_name
        if self.status is not None:
            result['Status'] = self.status
        if self.success is not None:
            result['Success'] = self.success
        if self.system_image_url is not None:
            result['SystemImageUrl'] = self.system_image_url
        if self.terminal_url is not None:
            result['TerminalUrl'] = self.terminal_url
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.user_name is not None:
            result['UserName'] = self.user_name
        if self.user_vpc is not None:
            result['UserVpc'] = self.user_vpc.to_map()
        if self.web_ideurl is not None:
            result['WebIDEUrl'] = self.web_ideurl
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        if self.workspace_name is not None:
            result['WorkspaceName'] = self.workspace_name
        if self.workspace_source is not None:
            result['WorkspaceSource'] = self.workspace_source
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AcceleratorType') is not None:
            self.accelerator_type = m.get('AcceleratorType')
        if m.get('Accessibility') is not None:
            self.accessibility = m.get('Accessibility')
        if m.get('AccumulatedRunningTimeInMs') is not None:
            self.accumulated_running_time_in_ms = m.get('AccumulatedRunningTimeInMs')
        if m.get('Affinity') is not None:
            temp_model = GetInstanceResponseBodyAffinity()
            self.affinity = temp_model.from_map(m['Affinity'])
        self.cloud_disks = []
        if m.get('CloudDisks') is not None:
            for k in m.get('CloudDisks'):
                temp_model = GetInstanceResponseBodyCloudDisks()
                self.cloud_disks.append(temp_model.from_map(k))
        if m.get('Code') is not None:
            self.code = m.get('Code')
        self.datasets = []
        if m.get('Datasets') is not None:
            for k in m.get('Datasets'):
                temp_model = GetInstanceResponseBodyDatasets()
                self.datasets.append(temp_model.from_map(k))
        if m.get('Driver') is not None:
            self.driver = m.get('Driver')
        if m.get('DynamicMount') is not None:
            temp_model = DynamicMount()
            self.dynamic_mount = temp_model.from_map(m['DynamicMount'])
        if m.get('EcsSpec') is not None:
            self.ecs_spec = m.get('EcsSpec')
        if m.get('EnvironmentVariables') is not None:
            self.environment_variables = m.get('EnvironmentVariables')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('IdleInstanceCuller') is not None:
            temp_model = GetInstanceResponseBodyIdleInstanceCuller()
            self.idle_instance_culler = temp_model.from_map(m['IdleInstanceCuller'])
        if m.get('ImageAuth') is not None:
            self.image_auth = m.get('ImageAuth')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('ImageName') is not None:
            self.image_name = m.get('ImageName')
        if m.get('ImageUrl') is not None:
            self.image_url = m.get('ImageUrl')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        if m.get('InstanceShutdownTimer') is not None:
            temp_model = GetInstanceResponseBodyInstanceShutdownTimer()
            self.instance_shutdown_timer = temp_model.from_map(m['InstanceShutdownTimer'])
        self.instance_snapshot_list = []
        if m.get('InstanceSnapshotList') is not None:
            for k in m.get('InstanceSnapshotList'):
                temp_model = GetInstanceResponseBodyInstanceSnapshotList()
                self.instance_snapshot_list.append(temp_model.from_map(k))
        if m.get('InstanceUrl') is not None:
            self.instance_url = m.get('InstanceUrl')
        if m.get('JupyterlabUrl') is not None:
            self.jupyterlab_url = m.get('JupyterlabUrl')
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = GetInstanceResponseBodyLabels()
                self.labels.append(temp_model.from_map(k))
        if m.get('LatestSnapshot') is not None:
            temp_model = GetInstanceResponseBodyLatestSnapshot()
            self.latest_snapshot = temp_model.from_map(m['LatestSnapshot'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('NodeErrorRecovery') is not None:
            temp_model = GetInstanceResponseBodyNodeErrorRecovery()
            self.node_error_recovery = temp_model.from_map(m['NodeErrorRecovery'])
        if m.get('PaymentType') is not None:
            self.payment_type = m.get('PaymentType')
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('ReasonCode') is not None:
            self.reason_code = m.get('ReasonCode')
        if m.get('ReasonMessage') is not None:
            self.reason_message = m.get('ReasonMessage')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('RequestedResource') is not None:
            temp_model = GetInstanceResponseBodyRequestedResource()
            self.requested_resource = temp_model.from_map(m['RequestedResource'])
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceName') is not None:
            self.resource_name = m.get('ResourceName')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('SystemImageUrl') is not None:
            self.system_image_url = m.get('SystemImageUrl')
        if m.get('TerminalUrl') is not None:
            self.terminal_url = m.get('TerminalUrl')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('UserName') is not None:
            self.user_name = m.get('UserName')
        if m.get('UserVpc') is not None:
            temp_model = GetInstanceResponseBodyUserVpc()
            self.user_vpc = temp_model.from_map(m['UserVpc'])
        if m.get('WebIDEUrl') is not None:
            self.web_ideurl = m.get('WebIDEUrl')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        if m.get('WorkspaceName') is not None:
            self.workspace_name = m.get('WorkspaceName')
        if m.get('WorkspaceSource') is not None:
            self.workspace_source = m.get('WorkspaceSource')
        return self


class GetInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetInstanceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetInstanceEventsRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        max_events_num: int = None,
        start_time: str = None,
    ):
        self.end_time = end_time
        self.max_events_num = max_events_num
        self.start_time = start_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.max_events_num is not None:
            result['MaxEventsNum'] = self.max_events_num
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('MaxEventsNum') is not None:
            self.max_events_num = m.get('MaxEventsNum')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        return self


class GetInstanceEventsResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        events: List[str] = None,
        http_status_code: int = None,
        instance_id: str = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.code = code
        self.events = events
        self.http_status_code = http_status_code
        self.instance_id = instance_id
        self.message = message
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.events is not None:
            result['Events'] = self.events
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Events') is not None:
            self.events = m.get('Events')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class GetInstanceEventsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetInstanceEventsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetInstanceEventsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetInstanceMetricsRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        metric_type: str = None,
        start_time: str = None,
        time_step: str = None,
    ):
        self.end_time = end_time
        # This parameter is required.
        self.metric_type = metric_type
        self.start_time = start_time
        self.time_step = time_step

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.metric_type is not None:
            result['MetricType'] = self.metric_type
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.time_step is not None:
            result['TimeStep'] = self.time_step
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('MetricType') is not None:
            self.metric_type = m.get('MetricType')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('TimeStep') is not None:
            self.time_step = m.get('TimeStep')
        return self


class GetInstanceMetricsResponseBodyPodMetricsMetrics(TeaModel):
    def __init__(
        self,
        time: int = None,
        value: float = None,
    ):
        self.time = time
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.time is not None:
            result['Time'] = self.time
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Time') is not None:
            self.time = m.get('Time')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class GetInstanceMetricsResponseBodyPodMetrics(TeaModel):
    def __init__(
        self,
        metrics: List[GetInstanceMetricsResponseBodyPodMetricsMetrics] = None,
        pod_id: str = None,
    ):
        self.metrics = metrics
        self.pod_id = pod_id

    def validate(self):
        if self.metrics:
            for k in self.metrics:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Metrics'] = []
        if self.metrics is not None:
            for k in self.metrics:
                result['Metrics'].append(k.to_map() if k else None)
        if self.pod_id is not None:
            result['PodId'] = self.pod_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.metrics = []
        if m.get('Metrics') is not None:
            for k in m.get('Metrics'):
                temp_model = GetInstanceMetricsResponseBodyPodMetricsMetrics()
                self.metrics.append(temp_model.from_map(k))
        if m.get('PodId') is not None:
            self.pod_id = m.get('PodId')
        return self


class GetInstanceMetricsResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        http_status_code: int = None,
        instance_id: str = None,
        message: str = None,
        pod_metrics: List[GetInstanceMetricsResponseBodyPodMetrics] = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.code = code
        self.http_status_code = http_status_code
        self.instance_id = instance_id
        self.message = message
        self.pod_metrics = pod_metrics
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.pod_metrics:
            for k in self.pod_metrics:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.message is not None:
            result['Message'] = self.message
        result['PodMetrics'] = []
        if self.pod_metrics is not None:
            for k in self.pod_metrics:
                result['PodMetrics'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        self.pod_metrics = []
        if m.get('PodMetrics') is not None:
            for k in m.get('PodMetrics'):
                temp_model = GetInstanceMetricsResponseBodyPodMetrics()
                self.pod_metrics.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class GetInstanceMetricsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetInstanceMetricsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetInstanceMetricsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetInstanceShutdownTimerResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        due_time: str = None,
        gmt_create_time: str = None,
        gmt_modified_time: str = None,
        http_status_code: int = None,
        instance_id: str = None,
        message: str = None,
        remaining_time_in_ms: int = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.code = code
        self.due_time = due_time
        self.gmt_create_time = gmt_create_time
        self.gmt_modified_time = gmt_modified_time
        self.http_status_code = http_status_code
        self.instance_id = instance_id
        self.message = message
        self.remaining_time_in_ms = remaining_time_in_ms
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.due_time is not None:
            result['DueTime'] = self.due_time
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.message is not None:
            result['Message'] = self.message
        if self.remaining_time_in_ms is not None:
            result['RemainingTimeInMs'] = self.remaining_time_in_ms
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('DueTime') is not None:
            self.due_time = m.get('DueTime')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RemainingTimeInMs') is not None:
            self.remaining_time_in_ms = m.get('RemainingTimeInMs')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class GetInstanceShutdownTimerResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetInstanceShutdownTimerResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetInstanceShutdownTimerResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetInstanceSnapshotResponseBodyLabels(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class GetInstanceSnapshotResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        exclude_paths: List[str] = None,
        gmt_create_time: str = None,
        gmt_modified_time: str = None,
        http_status_code: int = None,
        image_id: str = None,
        image_url: str = None,
        instance_id: str = None,
        labels: List[GetInstanceSnapshotResponseBodyLabels] = None,
        message: str = None,
        reason_code: str = None,
        reason_message: str = None,
        request_id: str = None,
        snapshot_id: str = None,
        snapshot_name: str = None,
        status: str = None,
        success: bool = None,
    ):
        self.code = code
        self.exclude_paths = exclude_paths
        self.gmt_create_time = gmt_create_time
        self.gmt_modified_time = gmt_modified_time
        self.http_status_code = http_status_code
        self.image_id = image_id
        self.image_url = image_url
        self.instance_id = instance_id
        self.labels = labels
        self.message = message
        self.reason_code = reason_code
        self.reason_message = reason_message
        self.request_id = request_id
        self.snapshot_id = snapshot_id
        self.snapshot_name = snapshot_name
        self.status = status
        self.success = success

    def validate(self):
        if self.labels:
            for k in self.labels:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.exclude_paths is not None:
            result['ExcludePaths'] = self.exclude_paths
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.image_url is not None:
            result['ImageUrl'] = self.image_url
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        if self.message is not None:
            result['Message'] = self.message
        if self.reason_code is not None:
            result['ReasonCode'] = self.reason_code
        if self.reason_message is not None:
            result['ReasonMessage'] = self.reason_message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.snapshot_id is not None:
            result['SnapshotId'] = self.snapshot_id
        if self.snapshot_name is not None:
            result['SnapshotName'] = self.snapshot_name
        if self.status is not None:
            result['Status'] = self.status
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('ExcludePaths') is not None:
            self.exclude_paths = m.get('ExcludePaths')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('ImageUrl') is not None:
            self.image_url = m.get('ImageUrl')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = GetInstanceSnapshotResponseBodyLabels()
                self.labels.append(temp_model.from_map(k))
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('ReasonCode') is not None:
            self.reason_code = m.get('ReasonCode')
        if m.get('ReasonMessage') is not None:
            self.reason_message = m.get('ReasonMessage')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('SnapshotId') is not None:
            self.snapshot_id = m.get('SnapshotId')
        if m.get('SnapshotName') is not None:
            self.snapshot_name = m.get('SnapshotName')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class GetInstanceSnapshotResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetInstanceSnapshotResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetInstanceSnapshotResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetLifecycleRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        limit: int = None,
        order: str = None,
        session_number: int = None,
        start_time: str = None,
    ):
        self.end_time = end_time
        self.limit = limit
        self.order = order
        self.session_number = session_number
        self.start_time = start_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.limit is not None:
            result['Limit'] = self.limit
        if self.order is not None:
            result['Order'] = self.order
        if self.session_number is not None:
            result['SessionNumber'] = self.session_number
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('Limit') is not None:
            self.limit = m.get('Limit')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('SessionNumber') is not None:
            self.session_number = m.get('SessionNumber')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        return self


class GetLifecycleResponseBodyLifecycle(TeaModel):
    def __init__(
        self,
        status: str = None,
        reason_code: str = None,
        reason_message: str = None,
        gmt_create_time: str = None,
    ):
        self.status = status
        self.reason_code = reason_code
        self.reason_message = reason_message
        self.gmt_create_time = gmt_create_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.reason_code is not None:
            result['ReasonCode'] = self.reason_code
        if self.reason_message is not None:
            result['ReasonMessage'] = self.reason_message
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('ReasonCode') is not None:
            self.reason_code = m.get('ReasonCode')
        if m.get('ReasonMessage') is not None:
            self.reason_message = m.get('ReasonMessage')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        return self


class GetLifecycleResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        lifecycle: List[List[GetLifecycleResponseBodyLifecycle]] = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
        total_count: int = None,
    ):
        self.code = code
        self.lifecycle = lifecycle
        self.message = message
        self.request_id = request_id
        self.success = success
        self.total_count = total_count

    def validate(self):
        if self.lifecycle:
            for k in self.lifecycle:
                for k1 in k:
                    if k1:
                        k1.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        result['Lifecycle'] = []
        if self.lifecycle is not None:
            for k in self.lifecycle:
                l1 = []
                for k1 in k:
                    l1.append(k1.to_map() if k1 else None)
                result['Lifecycle'].append(l1)
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        self.lifecycle = []
        if m.get('Lifecycle') is not None:
            for k in m.get('Lifecycle'):
                l1 = []
                for k1 in k:
                    temp_model = GetLifecycleResponseBodyLifecycle()
                    l1.append(temp_model.from_map(k1))
                self.lifecycle.append(l1)
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class GetLifecycleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetLifecycleResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetLifecycleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetMetricsRequest(TeaModel):
    def __init__(
        self,
        dimensions: str = None,
        end_time: str = None,
        length: str = None,
        metric_name: str = None,
        namespace: str = None,
        next_token: str = None,
        period: str = None,
        start_time: str = None,
    ):
        self.dimensions = dimensions
        self.end_time = end_time
        self.length = length
        self.metric_name = metric_name
        self.namespace = namespace
        self.next_token = next_token
        self.period = period
        self.start_time = start_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.dimensions is not None:
            result['Dimensions'] = self.dimensions
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.length is not None:
            result['Length'] = self.length
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.period is not None:
            result['Period'] = self.period
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Dimensions') is not None:
            self.dimensions = m.get('Dimensions')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('Length') is not None:
            self.length = m.get('Length')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        return self


class GetMetricsResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        datapoints: str = None,
        message: str = None,
        next_token: str = None,
        period: str = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.code = code
        self.datapoints = datapoints
        self.message = message
        self.next_token = next_token
        self.period = period
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.datapoints is not None:
            result['Datapoints'] = self.datapoints
        if self.message is not None:
            result['Message'] = self.message
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.period is not None:
            result['Period'] = self.period
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Datapoints') is not None:
            self.datapoints = m.get('Datapoints')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class GetMetricsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetMetricsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetMetricsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetResourceGroupStatisticsRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        resource_id: str = None,
        start_time: str = None,
        workspace_ids: str = None,
    ):
        # This parameter is required.
        self.end_time = end_time
        # This parameter is required.
        self.resource_id = resource_id
        # This parameter is required.
        self.start_time = start_time
        # This parameter is required.
        self.workspace_ids = workspace_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.workspace_ids is not None:
            result['WorkspaceIds'] = self.workspace_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('WorkspaceIds') is not None:
            self.workspace_ids = m.get('WorkspaceIds')
        return self


class GetResourceGroupStatisticsResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        http_status_code: int = None,
        message: str = None,
        request_id: str = None,
        statistics: Dict[str, dict] = None,
        success: bool = None,
    ):
        self.code = code
        self.http_status_code = http_status_code
        self.message = message
        self.request_id = request_id
        self.statistics = statistics
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class GetResourceGroupStatisticsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetResourceGroupStatisticsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetResourceGroupStatisticsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetTempFileResponseBody(TeaModel):
    def __init__(
        self,
        bandwidth: int = None,
        capacity: int = None,
        code: str = None,
        description: str = None,
        download_url: str = None,
        gmt_create_time: str = None,
        gmt_expired_time: str = None,
        gmt_modified_time: str = None,
        http_status_code: int = None,
        instance_id: str = None,
        message: str = None,
        name: str = None,
        owner_id: str = None,
        prefix: str = None,
        request_id: str = None,
        status: str = None,
        success: bool = None,
        task_id: str = None,
        type: str = None,
        upload_url: str = None,
        user_id: str = None,
        uuid: str = None,
    ):
        self.bandwidth = bandwidth
        self.capacity = capacity
        self.code = code
        self.description = description
        self.download_url = download_url
        self.gmt_create_time = gmt_create_time
        self.gmt_expired_time = gmt_expired_time
        self.gmt_modified_time = gmt_modified_time
        self.http_status_code = http_status_code
        self.instance_id = instance_id
        self.message = message
        self.name = name
        self.owner_id = owner_id
        self.prefix = prefix
        self.request_id = request_id
        self.status = status
        self.success = success
        self.task_id = task_id
        self.type = type
        self.upload_url = upload_url
        self.user_id = user_id
        self.uuid = uuid

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.bandwidth is not None:
            result['Bandwidth'] = self.bandwidth
        if self.capacity is not None:
            result['Capacity'] = self.capacity
        if self.code is not None:
            result['Code'] = self.code
        if self.description is not None:
            result['Description'] = self.description
        if self.download_url is not None:
            result['DownloadUrl'] = self.download_url
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_expired_time is not None:
            result['GmtExpiredTime'] = self.gmt_expired_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.message is not None:
            result['Message'] = self.message
        if self.name is not None:
            result['Name'] = self.name
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.prefix is not None:
            result['Prefix'] = self.prefix
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.status is not None:
            result['Status'] = self.status
        if self.success is not None:
            result['Success'] = self.success
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.type is not None:
            result['Type'] = self.type
        if self.upload_url is not None:
            result['UploadUrl'] = self.upload_url
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.uuid is not None:
            result['Uuid'] = self.uuid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Bandwidth') is not None:
            self.bandwidth = m.get('Bandwidth')
        if m.get('Capacity') is not None:
            self.capacity = m.get('Capacity')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('DownloadUrl') is not None:
            self.download_url = m.get('DownloadUrl')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtExpiredTime') is not None:
            self.gmt_expired_time = m.get('GmtExpiredTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('Prefix') is not None:
            self.prefix = m.get('Prefix')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('UploadUrl') is not None:
            self.upload_url = m.get('UploadUrl')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('Uuid') is not None:
            self.uuid = m.get('Uuid')
        return self


class GetTempFileResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetTempFileResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetTempFileResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetTokenRequest(TeaModel):
    def __init__(
        self,
        expire_time: int = None,
        instance_id: str = None,
    ):
        self.expire_time = expire_time
        # This parameter is required.
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.expire_time is not None:
            result['ExpireTime'] = self.expire_time
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ExpireTime') is not None:
            self.expire_time = m.get('ExpireTime')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class GetTokenResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
        token: str = None,
    ):
        self.code = code
        self.message = message
        self.request_id = request_id
        self.success = success
        self.token = token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.token is not None:
            result['Token'] = self.token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Token') is not None:
            self.token = m.get('Token')
        return self


class GetTokenResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetTokenResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetTokenResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetUserConfigResponseBodyFreeTier(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        init_base_unit: str = None,
        init_base_value: float = None,
        init_show_unit: str = None,
        init_show_value: str = None,
        is_free_tier_user: bool = None,
        period_base_unit: str = None,
        period_base_value: float = None,
        period_show_unit: str = None,
        period_show_value: str = None,
        start_time: str = None,
        status: str = None,
    ):
        self.end_time = end_time
        self.init_base_unit = init_base_unit
        self.init_base_value = init_base_value
        self.init_show_unit = init_show_unit
        self.init_show_value = init_show_value
        self.is_free_tier_user = is_free_tier_user
        self.period_base_unit = period_base_unit
        self.period_base_value = period_base_value
        self.period_show_unit = period_show_unit
        self.period_show_value = period_show_value
        self.start_time = start_time
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.init_base_unit is not None:
            result['InitBaseUnit'] = self.init_base_unit
        if self.init_base_value is not None:
            result['InitBaseValue'] = self.init_base_value
        if self.init_show_unit is not None:
            result['InitShowUnit'] = self.init_show_unit
        if self.init_show_value is not None:
            result['InitShowValue'] = self.init_show_value
        if self.is_free_tier_user is not None:
            result['IsFreeTierUser'] = self.is_free_tier_user
        if self.period_base_unit is not None:
            result['PeriodBaseUnit'] = self.period_base_unit
        if self.period_base_value is not None:
            result['PeriodBaseValue'] = self.period_base_value
        if self.period_show_unit is not None:
            result['PeriodShowUnit'] = self.period_show_unit
        if self.period_show_value is not None:
            result['PeriodShowValue'] = self.period_show_value
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('InitBaseUnit') is not None:
            self.init_base_unit = m.get('InitBaseUnit')
        if m.get('InitBaseValue') is not None:
            self.init_base_value = m.get('InitBaseValue')
        if m.get('InitShowUnit') is not None:
            self.init_show_unit = m.get('InitShowUnit')
        if m.get('InitShowValue') is not None:
            self.init_show_value = m.get('InitShowValue')
        if m.get('IsFreeTierUser') is not None:
            self.is_free_tier_user = m.get('IsFreeTierUser')
        if m.get('PeriodBaseUnit') is not None:
            self.period_base_unit = m.get('PeriodBaseUnit')
        if m.get('PeriodBaseValue') is not None:
            self.period_base_value = m.get('PeriodBaseValue')
        if m.get('PeriodShowUnit') is not None:
            self.period_show_unit = m.get('PeriodShowUnit')
        if m.get('PeriodShowValue') is not None:
            self.period_show_value = m.get('PeriodShowValue')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class GetUserConfigResponseBody(TeaModel):
    def __init__(
        self,
        account_sufficient: bool = None,
        code: str = None,
        enable_eci_disk: bool = None,
        free_tier: GetUserConfigResponseBodyFreeTier = None,
        free_tier_spec_available: bool = None,
        http_status_code: int = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.account_sufficient = account_sufficient
        self.code = code
        self.enable_eci_disk = enable_eci_disk
        self.free_tier = free_tier
        self.free_tier_spec_available = free_tier_spec_available
        self.http_status_code = http_status_code
        self.message = message
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.free_tier:
            self.free_tier.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.account_sufficient is not None:
            result['AccountSufficient'] = self.account_sufficient
        if self.code is not None:
            result['Code'] = self.code
        if self.enable_eci_disk is not None:
            result['EnableEciDisk'] = self.enable_eci_disk
        if self.free_tier is not None:
            result['FreeTier'] = self.free_tier.to_map()
        if self.free_tier_spec_available is not None:
            result['FreeTierSpecAvailable'] = self.free_tier_spec_available
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccountSufficient') is not None:
            self.account_sufficient = m.get('AccountSufficient')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('EnableEciDisk') is not None:
            self.enable_eci_disk = m.get('EnableEciDisk')
        if m.get('FreeTier') is not None:
            temp_model = GetUserConfigResponseBodyFreeTier()
            self.free_tier = temp_model.from_map(m['FreeTier'])
        if m.get('FreeTierSpecAvailable') is not None:
            self.free_tier_spec_available = m.get('FreeTierSpecAvailable')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class GetUserConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetUserConfigResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetUserConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListAppEndpointsResponseBodyEndpoints(TeaModel):
    def __init__(
        self,
        action: str = None,
        app: str = None,
        endpoint: str = None,
        method: str = None,
        path_name: str = None,
        protocol: str = None,
        req_body_type: str = None,
        style: str = None,
        timeout: int = None,
        version: str = None,
    ):
        self.action = action
        self.app = app
        self.endpoint = endpoint
        self.method = method
        self.path_name = path_name
        self.protocol = protocol
        self.req_body_type = req_body_type
        self.style = style
        self.timeout = timeout
        self.version = version

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.action is not None:
            result['Action'] = self.action
        if self.app is not None:
            result['App'] = self.app
        if self.endpoint is not None:
            result['Endpoint'] = self.endpoint
        if self.method is not None:
            result['Method'] = self.method
        if self.path_name is not None:
            result['PathName'] = self.path_name
        if self.protocol is not None:
            result['Protocol'] = self.protocol
        if self.req_body_type is not None:
            result['ReqBodyType'] = self.req_body_type
        if self.style is not None:
            result['Style'] = self.style
        if self.timeout is not None:
            result['Timeout'] = self.timeout
        if self.version is not None:
            result['Version'] = self.version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Action') is not None:
            self.action = m.get('Action')
        if m.get('App') is not None:
            self.app = m.get('App')
        if m.get('Endpoint') is not None:
            self.endpoint = m.get('Endpoint')
        if m.get('Method') is not None:
            self.method = m.get('Method')
        if m.get('PathName') is not None:
            self.path_name = m.get('PathName')
        if m.get('Protocol') is not None:
            self.protocol = m.get('Protocol')
        if m.get('ReqBodyType') is not None:
            self.req_body_type = m.get('ReqBodyType')
        if m.get('Style') is not None:
            self.style = m.get('Style')
        if m.get('Timeout') is not None:
            self.timeout = m.get('Timeout')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        return self


class ListAppEndpointsResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        endpoints: List[ListAppEndpointsResponseBodyEndpoints] = None,
        http_status_code: int = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
        total_count: int = None,
    ):
        self.code = code
        self.endpoints = endpoints
        self.http_status_code = http_status_code
        self.message = message
        self.request_id = request_id
        self.success = success
        self.total_count = total_count

    def validate(self):
        if self.endpoints:
            for k in self.endpoints:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        result['Endpoints'] = []
        if self.endpoints is not None:
            for k in self.endpoints:
                result['Endpoints'].append(k.to_map() if k else None)
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        self.endpoints = []
        if m.get('Endpoints') is not None:
            for k in m.get('Endpoints'):
                temp_model = ListAppEndpointsResponseBodyEndpoints()
                self.endpoints.append(temp_model.from_map(k))
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListAppEndpointsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListAppEndpointsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListAppEndpointsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListEcsSpecsRequest(TeaModel):
    def __init__(
        self,
        accelerator_type: str = None,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        sort_by: str = None,
    ):
        # This parameter is required.
        self.accelerator_type = accelerator_type
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        self.sort_by = sort_by

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.accelerator_type is not None:
            result['AcceleratorType'] = self.accelerator_type
        if self.order is not None:
            result['Order'] = self.order
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AcceleratorType') is not None:
            self.accelerator_type = m.get('AcceleratorType')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        return self


class ListEcsSpecsResponseBodyEcsSpecsLabels(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class ListEcsSpecsResponseBodyEcsSpecs(TeaModel):
    def __init__(
        self,
        accelerator_type: str = None,
        cpu: int = None,
        currency: str = None,
        gpu: int = None,
        gputype: str = None,
        instance_bandwidth_rx: int = None,
        instance_type: str = None,
        is_available: bool = None,
        labels: List[ListEcsSpecsResponseBodyEcsSpecsLabels] = None,
        memory: float = None,
        price: float = None,
        system_disk_capacity: int = None,
    ):
        self.accelerator_type = accelerator_type
        self.cpu = cpu
        self.currency = currency
        self.gpu = gpu
        self.gputype = gputype
        self.instance_bandwidth_rx = instance_bandwidth_rx
        self.instance_type = instance_type
        self.is_available = is_available
        self.labels = labels
        self.memory = memory
        self.price = price
        self.system_disk_capacity = system_disk_capacity

    def validate(self):
        if self.labels:
            for k in self.labels:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.accelerator_type is not None:
            result['AcceleratorType'] = self.accelerator_type
        if self.cpu is not None:
            result['CPU'] = self.cpu
        if self.currency is not None:
            result['Currency'] = self.currency
        if self.gpu is not None:
            result['GPU'] = self.gpu
        if self.gputype is not None:
            result['GPUType'] = self.gputype
        if self.instance_bandwidth_rx is not None:
            result['InstanceBandwidthRx'] = self.instance_bandwidth_rx
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        if self.is_available is not None:
            result['IsAvailable'] = self.is_available
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        if self.memory is not None:
            result['Memory'] = self.memory
        if self.price is not None:
            result['Price'] = self.price
        if self.system_disk_capacity is not None:
            result['SystemDiskCapacity'] = self.system_disk_capacity
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AcceleratorType') is not None:
            self.accelerator_type = m.get('AcceleratorType')
        if m.get('CPU') is not None:
            self.cpu = m.get('CPU')
        if m.get('Currency') is not None:
            self.currency = m.get('Currency')
        if m.get('GPU') is not None:
            self.gpu = m.get('GPU')
        if m.get('GPUType') is not None:
            self.gputype = m.get('GPUType')
        if m.get('InstanceBandwidthRx') is not None:
            self.instance_bandwidth_rx = m.get('InstanceBandwidthRx')
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        if m.get('IsAvailable') is not None:
            self.is_available = m.get('IsAvailable')
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = ListEcsSpecsResponseBodyEcsSpecsLabels()
                self.labels.append(temp_model.from_map(k))
        if m.get('Memory') is not None:
            self.memory = m.get('Memory')
        if m.get('Price') is not None:
            self.price = m.get('Price')
        if m.get('SystemDiskCapacity') is not None:
            self.system_disk_capacity = m.get('SystemDiskCapacity')
        return self


class ListEcsSpecsResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        ecs_specs: List[ListEcsSpecsResponseBodyEcsSpecs] = None,
        http_status_code: int = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
        total_count: int = None,
    ):
        self.code = code
        self.ecs_specs = ecs_specs
        self.http_status_code = http_status_code
        self.message = message
        self.request_id = request_id
        self.success = success
        self.total_count = total_count

    def validate(self):
        if self.ecs_specs:
            for k in self.ecs_specs:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        result['EcsSpecs'] = []
        if self.ecs_specs is not None:
            for k in self.ecs_specs:
                result['EcsSpecs'].append(k.to_map() if k else None)
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        self.ecs_specs = []
        if m.get('EcsSpecs') is not None:
            for k in m.get('EcsSpecs'):
                temp_model = ListEcsSpecsResponseBodyEcsSpecs()
                self.ecs_specs.append(temp_model.from_map(k))
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListEcsSpecsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListEcsSpecsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListEcsSpecsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListEcsSpecsByInstanceTypesRequest(TeaModel):
    def __init__(
        self,
        instance_types: str = None,
    ):
        self.instance_types = instance_types

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instance_types is not None:
            result['InstanceTypes'] = self.instance_types
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceTypes') is not None:
            self.instance_types = m.get('InstanceTypes')
        return self


class ListEcsSpecsByInstanceTypesResponseBodyEcsSpecsLabels(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: Any = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class ListEcsSpecsByInstanceTypesResponseBodyEcsSpecs(TeaModel):
    def __init__(
        self,
        accelerator_type: str = None,
        cpu: int = None,
        currency: str = None,
        gpu: int = None,
        gputype: str = None,
        instance_bandwidth_rx: int = None,
        instance_type: str = None,
        is_available: bool = None,
        labels: List[ListEcsSpecsByInstanceTypesResponseBodyEcsSpecsLabels] = None,
        memory: float = None,
        price: float = None,
        system_disk_capacity: int = None,
    ):
        self.accelerator_type = accelerator_type
        self.cpu = cpu
        self.currency = currency
        self.gpu = gpu
        self.gputype = gputype
        self.instance_bandwidth_rx = instance_bandwidth_rx
        self.instance_type = instance_type
        self.is_available = is_available
        self.labels = labels
        self.memory = memory
        self.price = price
        self.system_disk_capacity = system_disk_capacity

    def validate(self):
        if self.labels:
            for k in self.labels:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.accelerator_type is not None:
            result['AcceleratorType'] = self.accelerator_type
        if self.cpu is not None:
            result['CPU'] = self.cpu
        if self.currency is not None:
            result['Currency'] = self.currency
        if self.gpu is not None:
            result['GPU'] = self.gpu
        if self.gputype is not None:
            result['GPUType'] = self.gputype
        if self.instance_bandwidth_rx is not None:
            result['InstanceBandwidthRx'] = self.instance_bandwidth_rx
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        if self.is_available is not None:
            result['IsAvailable'] = self.is_available
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        if self.memory is not None:
            result['Memory'] = self.memory
        if self.price is not None:
            result['Price'] = self.price
        if self.system_disk_capacity is not None:
            result['SystemDiskCapacity'] = self.system_disk_capacity
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AcceleratorType') is not None:
            self.accelerator_type = m.get('AcceleratorType')
        if m.get('CPU') is not None:
            self.cpu = m.get('CPU')
        if m.get('Currency') is not None:
            self.currency = m.get('Currency')
        if m.get('GPU') is not None:
            self.gpu = m.get('GPU')
        if m.get('GPUType') is not None:
            self.gputype = m.get('GPUType')
        if m.get('InstanceBandwidthRx') is not None:
            self.instance_bandwidth_rx = m.get('InstanceBandwidthRx')
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        if m.get('IsAvailable') is not None:
            self.is_available = m.get('IsAvailable')
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = ListEcsSpecsByInstanceTypesResponseBodyEcsSpecsLabels()
                self.labels.append(temp_model.from_map(k))
        if m.get('Memory') is not None:
            self.memory = m.get('Memory')
        if m.get('Price') is not None:
            self.price = m.get('Price')
        if m.get('SystemDiskCapacity') is not None:
            self.system_disk_capacity = m.get('SystemDiskCapacity')
        return self


class ListEcsSpecsByInstanceTypesResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        ecs_specs: List[ListEcsSpecsByInstanceTypesResponseBodyEcsSpecs] = None,
        http_status_code: int = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
        total_count: int = None,
    ):
        self.code = code
        self.ecs_specs = ecs_specs
        self.http_status_code = http_status_code
        self.message = message
        self.request_id = request_id
        self.success = success
        self.total_count = total_count

    def validate(self):
        if self.ecs_specs:
            for k in self.ecs_specs:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        result['EcsSpecs'] = []
        if self.ecs_specs is not None:
            for k in self.ecs_specs:
                result['EcsSpecs'].append(k.to_map() if k else None)
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        self.ecs_specs = []
        if m.get('EcsSpecs') is not None:
            for k in m.get('EcsSpecs'):
                temp_model = ListEcsSpecsByInstanceTypesResponseBodyEcsSpecs()
                self.ecs_specs.append(temp_model.from_map(k))
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListEcsSpecsByInstanceTypesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListEcsSpecsByInstanceTypesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListEcsSpecsByInstanceTypesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListInstanceSnapshotRequest(TeaModel):
    def __init__(
        self,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        sort_by: str = None,
    ):
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        self.sort_by = sort_by

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.order is not None:
            result['Order'] = self.order
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        return self


class ListInstanceSnapshotResponseBodySnapshotsLabels(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class ListInstanceSnapshotResponseBodySnapshots(TeaModel):
    def __init__(
        self,
        exclude_paths: List[str] = None,
        gmt_create_time: str = None,
        gmt_modified_time: str = None,
        image_id: str = None,
        image_url: str = None,
        instance_id: str = None,
        labels: List[ListInstanceSnapshotResponseBodySnapshotsLabels] = None,
        reason_code: str = None,
        reason_message: str = None,
        snapshot_id: str = None,
        snapshot_name: str = None,
        status: str = None,
    ):
        self.exclude_paths = exclude_paths
        self.gmt_create_time = gmt_create_time
        self.gmt_modified_time = gmt_modified_time
        self.image_id = image_id
        self.image_url = image_url
        self.instance_id = instance_id
        self.labels = labels
        self.reason_code = reason_code
        self.reason_message = reason_message
        self.snapshot_id = snapshot_id
        self.snapshot_name = snapshot_name
        self.status = status

    def validate(self):
        if self.labels:
            for k in self.labels:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.exclude_paths is not None:
            result['ExcludePaths'] = self.exclude_paths
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.image_url is not None:
            result['ImageUrl'] = self.image_url
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        if self.reason_code is not None:
            result['ReasonCode'] = self.reason_code
        if self.reason_message is not None:
            result['ReasonMessage'] = self.reason_message
        if self.snapshot_id is not None:
            result['SnapshotId'] = self.snapshot_id
        if self.snapshot_name is not None:
            result['SnapshotName'] = self.snapshot_name
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ExcludePaths') is not None:
            self.exclude_paths = m.get('ExcludePaths')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('ImageUrl') is not None:
            self.image_url = m.get('ImageUrl')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = ListInstanceSnapshotResponseBodySnapshotsLabels()
                self.labels.append(temp_model.from_map(k))
        if m.get('ReasonCode') is not None:
            self.reason_code = m.get('ReasonCode')
        if m.get('ReasonMessage') is not None:
            self.reason_message = m.get('ReasonMessage')
        if m.get('SnapshotId') is not None:
            self.snapshot_id = m.get('SnapshotId')
        if m.get('SnapshotName') is not None:
            self.snapshot_name = m.get('SnapshotName')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class ListInstanceSnapshotResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        http_status_code: int = None,
        message: str = None,
        request_id: str = None,
        snapshots: List[ListInstanceSnapshotResponseBodySnapshots] = None,
        success: bool = None,
        total_count: int = None,
    ):
        self.code = code
        self.http_status_code = http_status_code
        self.message = message
        self.request_id = request_id
        self.snapshots = snapshots
        self.success = success
        self.total_count = total_count

    def validate(self):
        if self.snapshots:
            for k in self.snapshots:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Snapshots'] = []
        if self.snapshots is not None:
            for k in self.snapshots:
                result['Snapshots'].append(k.to_map() if k else None)
        if self.success is not None:
            result['Success'] = self.success
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.snapshots = []
        if m.get('Snapshots') is not None:
            for k in m.get('Snapshots'):
                temp_model = ListInstanceSnapshotResponseBodySnapshots()
                self.snapshots.append(temp_model.from_map(k))
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListInstanceSnapshotResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListInstanceSnapshotResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListInstanceSnapshotResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListInstanceStatisticsRequest(TeaModel):
    def __init__(
        self,
        workspace_ids: str = None,
    ):
        # This parameter is required.
        self.workspace_ids = workspace_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.workspace_ids is not None:
            result['WorkspaceIds'] = self.workspace_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('WorkspaceIds') is not None:
            self.workspace_ids = m.get('WorkspaceIds')
        return self


class ListInstanceStatisticsResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        http_status_code: int = None,
        message: str = None,
        request_id: str = None,
        statistics: Dict[str, dict] = None,
        success: bool = None,
    ):
        self.code = code
        self.http_status_code = http_status_code
        self.message = message
        self.request_id = request_id
        self.statistics = statistics
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ListInstanceStatisticsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListInstanceStatisticsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListInstanceStatisticsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListInstancesRequest(TeaModel):
    def __init__(
        self,
        accelerator_type: str = None,
        accessibility: str = None,
        create_user_id: str = None,
        gpu_type: str = None,
        image_name: str = None,
        instance_id: str = None,
        instance_name: str = None,
        labels: Dict[str, Any] = None,
        max_cpu: str = None,
        max_gpu: str = None,
        max_gpu_memory: str = None,
        max_memory: str = None,
        min_cpu: str = None,
        min_gpu: str = None,
        min_gpu_memory: str = None,
        min_memory: str = None,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        payment_type: str = None,
        resource_id: str = None,
        sort_by: str = None,
        status: str = None,
        workspace_id: str = None,
    ):
        self.accelerator_type = accelerator_type
        self.accessibility = accessibility
        self.create_user_id = create_user_id
        self.gpu_type = gpu_type
        self.image_name = image_name
        self.instance_id = instance_id
        self.instance_name = instance_name
        self.labels = labels
        self.max_cpu = max_cpu
        self.max_gpu = max_gpu
        self.max_gpu_memory = max_gpu_memory
        self.max_memory = max_memory
        self.min_cpu = min_cpu
        self.min_gpu = min_gpu
        self.min_gpu_memory = min_gpu_memory
        self.min_memory = min_memory
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        self.payment_type = payment_type
        self.resource_id = resource_id
        self.sort_by = sort_by
        self.status = status
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.accelerator_type is not None:
            result['AcceleratorType'] = self.accelerator_type
        if self.accessibility is not None:
            result['Accessibility'] = self.accessibility
        if self.create_user_id is not None:
            result['CreateUserId'] = self.create_user_id
        if self.gpu_type is not None:
            result['GpuType'] = self.gpu_type
        if self.image_name is not None:
            result['ImageName'] = self.image_name
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        if self.labels is not None:
            result['Labels'] = self.labels
        if self.max_cpu is not None:
            result['MaxCpu'] = self.max_cpu
        if self.max_gpu is not None:
            result['MaxGpu'] = self.max_gpu
        if self.max_gpu_memory is not None:
            result['MaxGpuMemory'] = self.max_gpu_memory
        if self.max_memory is not None:
            result['MaxMemory'] = self.max_memory
        if self.min_cpu is not None:
            result['MinCpu'] = self.min_cpu
        if self.min_gpu is not None:
            result['MinGpu'] = self.min_gpu
        if self.min_gpu_memory is not None:
            result['MinGpuMemory'] = self.min_gpu_memory
        if self.min_memory is not None:
            result['MinMemory'] = self.min_memory
        if self.order is not None:
            result['Order'] = self.order
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.payment_type is not None:
            result['PaymentType'] = self.payment_type
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.status is not None:
            result['Status'] = self.status
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AcceleratorType') is not None:
            self.accelerator_type = m.get('AcceleratorType')
        if m.get('Accessibility') is not None:
            self.accessibility = m.get('Accessibility')
        if m.get('CreateUserId') is not None:
            self.create_user_id = m.get('CreateUserId')
        if m.get('GpuType') is not None:
            self.gpu_type = m.get('GpuType')
        if m.get('ImageName') is not None:
            self.image_name = m.get('ImageName')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        if m.get('Labels') is not None:
            self.labels = m.get('Labels')
        if m.get('MaxCpu') is not None:
            self.max_cpu = m.get('MaxCpu')
        if m.get('MaxGpu') is not None:
            self.max_gpu = m.get('MaxGpu')
        if m.get('MaxGpuMemory') is not None:
            self.max_gpu_memory = m.get('MaxGpuMemory')
        if m.get('MaxMemory') is not None:
            self.max_memory = m.get('MaxMemory')
        if m.get('MinCpu') is not None:
            self.min_cpu = m.get('MinCpu')
        if m.get('MinGpu') is not None:
            self.min_gpu = m.get('MinGpu')
        if m.get('MinGpuMemory') is not None:
            self.min_gpu_memory = m.get('MinGpuMemory')
        if m.get('MinMemory') is not None:
            self.min_memory = m.get('MinMemory')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('PaymentType') is not None:
            self.payment_type = m.get('PaymentType')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class ListInstancesShrinkRequest(TeaModel):
    def __init__(
        self,
        accelerator_type: str = None,
        accessibility: str = None,
        create_user_id: str = None,
        gpu_type: str = None,
        image_name: str = None,
        instance_id: str = None,
        instance_name: str = None,
        labels_shrink: str = None,
        max_cpu: str = None,
        max_gpu: str = None,
        max_gpu_memory: str = None,
        max_memory: str = None,
        min_cpu: str = None,
        min_gpu: str = None,
        min_gpu_memory: str = None,
        min_memory: str = None,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        payment_type: str = None,
        resource_id: str = None,
        sort_by: str = None,
        status: str = None,
        workspace_id: str = None,
    ):
        self.accelerator_type = accelerator_type
        self.accessibility = accessibility
        self.create_user_id = create_user_id
        self.gpu_type = gpu_type
        self.image_name = image_name
        self.instance_id = instance_id
        self.instance_name = instance_name
        self.labels_shrink = labels_shrink
        self.max_cpu = max_cpu
        self.max_gpu = max_gpu
        self.max_gpu_memory = max_gpu_memory
        self.max_memory = max_memory
        self.min_cpu = min_cpu
        self.min_gpu = min_gpu
        self.min_gpu_memory = min_gpu_memory
        self.min_memory = min_memory
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        self.payment_type = payment_type
        self.resource_id = resource_id
        self.sort_by = sort_by
        self.status = status
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.accelerator_type is not None:
            result['AcceleratorType'] = self.accelerator_type
        if self.accessibility is not None:
            result['Accessibility'] = self.accessibility
        if self.create_user_id is not None:
            result['CreateUserId'] = self.create_user_id
        if self.gpu_type is not None:
            result['GpuType'] = self.gpu_type
        if self.image_name is not None:
            result['ImageName'] = self.image_name
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        if self.labels_shrink is not None:
            result['Labels'] = self.labels_shrink
        if self.max_cpu is not None:
            result['MaxCpu'] = self.max_cpu
        if self.max_gpu is not None:
            result['MaxGpu'] = self.max_gpu
        if self.max_gpu_memory is not None:
            result['MaxGpuMemory'] = self.max_gpu_memory
        if self.max_memory is not None:
            result['MaxMemory'] = self.max_memory
        if self.min_cpu is not None:
            result['MinCpu'] = self.min_cpu
        if self.min_gpu is not None:
            result['MinGpu'] = self.min_gpu
        if self.min_gpu_memory is not None:
            result['MinGpuMemory'] = self.min_gpu_memory
        if self.min_memory is not None:
            result['MinMemory'] = self.min_memory
        if self.order is not None:
            result['Order'] = self.order
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.payment_type is not None:
            result['PaymentType'] = self.payment_type
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.status is not None:
            result['Status'] = self.status
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AcceleratorType') is not None:
            self.accelerator_type = m.get('AcceleratorType')
        if m.get('Accessibility') is not None:
            self.accessibility = m.get('Accessibility')
        if m.get('CreateUserId') is not None:
            self.create_user_id = m.get('CreateUserId')
        if m.get('GpuType') is not None:
            self.gpu_type = m.get('GpuType')
        if m.get('ImageName') is not None:
            self.image_name = m.get('ImageName')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        if m.get('Labels') is not None:
            self.labels_shrink = m.get('Labels')
        if m.get('MaxCpu') is not None:
            self.max_cpu = m.get('MaxCpu')
        if m.get('MaxGpu') is not None:
            self.max_gpu = m.get('MaxGpu')
        if m.get('MaxGpuMemory') is not None:
            self.max_gpu_memory = m.get('MaxGpuMemory')
        if m.get('MaxMemory') is not None:
            self.max_memory = m.get('MaxMemory')
        if m.get('MinCpu') is not None:
            self.min_cpu = m.get('MinCpu')
        if m.get('MinGpu') is not None:
            self.min_gpu = m.get('MinGpu')
        if m.get('MinGpuMemory') is not None:
            self.min_gpu_memory = m.get('MinGpuMemory')
        if m.get('MinMemory') is not None:
            self.min_memory = m.get('MinMemory')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('PaymentType') is not None:
            self.payment_type = m.get('PaymentType')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class ListInstancesResponseBodyInstancesAffinityCPU(TeaModel):
    def __init__(
        self,
        enable: bool = None,
    ):
        self.enable = enable

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.enable is not None:
            result['Enable'] = self.enable
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Enable') is not None:
            self.enable = m.get('Enable')
        return self


class ListInstancesResponseBodyInstancesAffinity(TeaModel):
    def __init__(
        self,
        cpu: ListInstancesResponseBodyInstancesAffinityCPU = None,
    ):
        self.cpu = cpu

    def validate(self):
        if self.cpu:
            self.cpu.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cpu is not None:
            result['CPU'] = self.cpu.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CPU') is not None:
            temp_model = ListInstancesResponseBodyInstancesAffinityCPU()
            self.cpu = temp_model.from_map(m['CPU'])
        return self


class ListInstancesResponseBodyInstancesCloudDisks(TeaModel):
    def __init__(
        self,
        capacity: str = None,
        mount_path: str = None,
        path: str = None,
        sub_type: str = None,
    ):
        self.capacity = capacity
        self.mount_path = mount_path
        self.path = path
        self.sub_type = sub_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.capacity is not None:
            result['Capacity'] = self.capacity
        if self.mount_path is not None:
            result['MountPath'] = self.mount_path
        if self.path is not None:
            result['Path'] = self.path
        if self.sub_type is not None:
            result['SubType'] = self.sub_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Capacity') is not None:
            self.capacity = m.get('Capacity')
        if m.get('MountPath') is not None:
            self.mount_path = m.get('MountPath')
        if m.get('Path') is not None:
            self.path = m.get('Path')
        if m.get('SubType') is not None:
            self.sub_type = m.get('SubType')
        return self


class ListInstancesResponseBodyInstancesDatasets(TeaModel):
    def __init__(
        self,
        dataset_id: str = None,
        dynamic: bool = None,
        mount_path: str = None,
        option_type: str = None,
        options: str = None,
        uri: str = None,
    ):
        self.dataset_id = dataset_id
        self.dynamic = dynamic
        self.mount_path = mount_path
        self.option_type = option_type
        self.options = options
        self.uri = uri

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.dataset_id is not None:
            result['DatasetId'] = self.dataset_id
        if self.dynamic is not None:
            result['Dynamic'] = self.dynamic
        if self.mount_path is not None:
            result['MountPath'] = self.mount_path
        if self.option_type is not None:
            result['OptionType'] = self.option_type
        if self.options is not None:
            result['Options'] = self.options
        if self.uri is not None:
            result['Uri'] = self.uri
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DatasetId') is not None:
            self.dataset_id = m.get('DatasetId')
        if m.get('Dynamic') is not None:
            self.dynamic = m.get('Dynamic')
        if m.get('MountPath') is not None:
            self.mount_path = m.get('MountPath')
        if m.get('OptionType') is not None:
            self.option_type = m.get('OptionType')
        if m.get('Options') is not None:
            self.options = m.get('Options')
        if m.get('Uri') is not None:
            self.uri = m.get('Uri')
        return self


class ListInstancesResponseBodyInstancesIdleInstanceCuller(TeaModel):
    def __init__(
        self,
        cpu_percent_threshold: int = None,
        gpu_percent_threshold: int = None,
        idle_time_in_minutes: int = None,
        instance_id: str = None,
        max_idle_time_in_minutes: int = None,
    ):
        self.cpu_percent_threshold = cpu_percent_threshold
        self.gpu_percent_threshold = gpu_percent_threshold
        self.idle_time_in_minutes = idle_time_in_minutes
        self.instance_id = instance_id
        self.max_idle_time_in_minutes = max_idle_time_in_minutes

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cpu_percent_threshold is not None:
            result['CpuPercentThreshold'] = self.cpu_percent_threshold
        if self.gpu_percent_threshold is not None:
            result['GpuPercentThreshold'] = self.gpu_percent_threshold
        if self.idle_time_in_minutes is not None:
            result['IdleTimeInMinutes'] = self.idle_time_in_minutes
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.max_idle_time_in_minutes is not None:
            result['MaxIdleTimeInMinutes'] = self.max_idle_time_in_minutes
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CpuPercentThreshold') is not None:
            self.cpu_percent_threshold = m.get('CpuPercentThreshold')
        if m.get('GpuPercentThreshold') is not None:
            self.gpu_percent_threshold = m.get('GpuPercentThreshold')
        if m.get('IdleTimeInMinutes') is not None:
            self.idle_time_in_minutes = m.get('IdleTimeInMinutes')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('MaxIdleTimeInMinutes') is not None:
            self.max_idle_time_in_minutes = m.get('MaxIdleTimeInMinutes')
        return self


class ListInstancesResponseBodyInstancesInstanceShutdownTimer(TeaModel):
    def __init__(
        self,
        due_time: str = None,
        gmt_create_time: str = None,
        gmt_modified_time: str = None,
        instance_id: str = None,
        remaining_time_in_ms: int = None,
    ):
        self.due_time = due_time
        self.gmt_create_time = gmt_create_time
        self.gmt_modified_time = gmt_modified_time
        self.instance_id = instance_id
        self.remaining_time_in_ms = remaining_time_in_ms

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.due_time is not None:
            result['DueTime'] = self.due_time
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.remaining_time_in_ms is not None:
            result['RemainingTimeInMs'] = self.remaining_time_in_ms
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DueTime') is not None:
            self.due_time = m.get('DueTime')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('RemainingTimeInMs') is not None:
            self.remaining_time_in_ms = m.get('RemainingTimeInMs')
        return self


class ListInstancesResponseBodyInstancesInstanceSnapshotList(TeaModel):
    def __init__(
        self,
        gmt_create_time: str = None,
        gmt_modified_time: str = None,
        image_id: str = None,
        image_name: str = None,
        image_url: str = None,
        reason_code: str = None,
        reason_message: str = None,
        repository_url: str = None,
        status: str = None,
    ):
        self.gmt_create_time = gmt_create_time
        self.gmt_modified_time = gmt_modified_time
        self.image_id = image_id
        self.image_name = image_name
        self.image_url = image_url
        self.reason_code = reason_code
        self.reason_message = reason_message
        self.repository_url = repository_url
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.image_name is not None:
            result['ImageName'] = self.image_name
        if self.image_url is not None:
            result['ImageUrl'] = self.image_url
        if self.reason_code is not None:
            result['ReasonCode'] = self.reason_code
        if self.reason_message is not None:
            result['ReasonMessage'] = self.reason_message
        if self.repository_url is not None:
            result['RepositoryUrl'] = self.repository_url
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('ImageName') is not None:
            self.image_name = m.get('ImageName')
        if m.get('ImageUrl') is not None:
            self.image_url = m.get('ImageUrl')
        if m.get('ReasonCode') is not None:
            self.reason_code = m.get('ReasonCode')
        if m.get('ReasonMessage') is not None:
            self.reason_message = m.get('ReasonMessage')
        if m.get('RepositoryUrl') is not None:
            self.repository_url = m.get('RepositoryUrl')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class ListInstancesResponseBodyInstancesLabels(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class ListInstancesResponseBodyInstancesLatestSnapshot(TeaModel):
    def __init__(
        self,
        gmt_create_time: str = None,
        gmt_modified_time: str = None,
        image_id: str = None,
        image_name: str = None,
        image_url: str = None,
        reason_code: str = None,
        reason_message: str = None,
        repository_url: str = None,
        status: str = None,
    ):
        self.gmt_create_time = gmt_create_time
        self.gmt_modified_time = gmt_modified_time
        self.image_id = image_id
        self.image_name = image_name
        self.image_url = image_url
        self.reason_code = reason_code
        self.reason_message = reason_message
        self.repository_url = repository_url
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.image_name is not None:
            result['ImageName'] = self.image_name
        if self.image_url is not None:
            result['ImageUrl'] = self.image_url
        if self.reason_code is not None:
            result['ReasonCode'] = self.reason_code
        if self.reason_message is not None:
            result['ReasonMessage'] = self.reason_message
        if self.repository_url is not None:
            result['RepositoryUrl'] = self.repository_url
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('ImageName') is not None:
            self.image_name = m.get('ImageName')
        if m.get('ImageUrl') is not None:
            self.image_url = m.get('ImageUrl')
        if m.get('ReasonCode') is not None:
            self.reason_code = m.get('ReasonCode')
        if m.get('ReasonMessage') is not None:
            self.reason_message = m.get('ReasonMessage')
        if m.get('RepositoryUrl') is not None:
            self.repository_url = m.get('RepositoryUrl')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class ListInstancesResponseBodyInstancesRequestedResource(TeaModel):
    def __init__(
        self,
        cpu: str = None,
        gpu: str = None,
        gputype: str = None,
        memory: str = None,
        shared_memory: str = None,
    ):
        self.cpu = cpu
        self.gpu = gpu
        self.gputype = gputype
        self.memory = memory
        self.shared_memory = shared_memory

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cpu is not None:
            result['CPU'] = self.cpu
        if self.gpu is not None:
            result['GPU'] = self.gpu
        if self.gputype is not None:
            result['GPUType'] = self.gputype
        if self.memory is not None:
            result['Memory'] = self.memory
        if self.shared_memory is not None:
            result['SharedMemory'] = self.shared_memory
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CPU') is not None:
            self.cpu = m.get('CPU')
        if m.get('GPU') is not None:
            self.gpu = m.get('GPU')
        if m.get('GPUType') is not None:
            self.gputype = m.get('GPUType')
        if m.get('Memory') is not None:
            self.memory = m.get('Memory')
        if m.get('SharedMemory') is not None:
            self.shared_memory = m.get('SharedMemory')
        return self


class ListInstancesResponseBodyInstancesUserVpc(TeaModel):
    def __init__(
        self,
        default_route: str = None,
        extended_cidrs: List[str] = None,
        forward_infos: List[ForwardInfoResponse] = None,
        security_group_id: str = None,
        v_switch_id: str = None,
        vpc_id: str = None,
    ):
        self.default_route = default_route
        self.extended_cidrs = extended_cidrs
        self.forward_infos = forward_infos
        self.security_group_id = security_group_id
        self.v_switch_id = v_switch_id
        self.vpc_id = vpc_id

    def validate(self):
        if self.forward_infos:
            for k in self.forward_infos:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.default_route is not None:
            result['DefaultRoute'] = self.default_route
        if self.extended_cidrs is not None:
            result['ExtendedCIDRs'] = self.extended_cidrs
        result['ForwardInfos'] = []
        if self.forward_infos is not None:
            for k in self.forward_infos:
                result['ForwardInfos'].append(k.to_map() if k else None)
        if self.security_group_id is not None:
            result['SecurityGroupId'] = self.security_group_id
        if self.v_switch_id is not None:
            result['VSwitchId'] = self.v_switch_id
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DefaultRoute') is not None:
            self.default_route = m.get('DefaultRoute')
        if m.get('ExtendedCIDRs') is not None:
            self.extended_cidrs = m.get('ExtendedCIDRs')
        self.forward_infos = []
        if m.get('ForwardInfos') is not None:
            for k in m.get('ForwardInfos'):
                temp_model = ForwardInfoResponse()
                self.forward_infos.append(temp_model.from_map(k))
        if m.get('SecurityGroupId') is not None:
            self.security_group_id = m.get('SecurityGroupId')
        if m.get('VSwitchId') is not None:
            self.v_switch_id = m.get('VSwitchId')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        return self


class ListInstancesResponseBodyInstances(TeaModel):
    def __init__(
        self,
        accelerator_type: str = None,
        accessibility: str = None,
        accumulated_running_time_in_ms: int = None,
        affinity: ListInstancesResponseBodyInstancesAffinity = None,
        cloud_disks: List[ListInstancesResponseBodyInstancesCloudDisks] = None,
        datasets: List[ListInstancesResponseBodyInstancesDatasets] = None,
        driver: str = None,
        dynamic_mount: DynamicMount = None,
        ecs_spec: str = None,
        environment_variables: Dict[str, str] = None,
        gmt_create_time: str = None,
        gmt_modified_time: str = None,
        idle_instance_culler: ListInstancesResponseBodyInstancesIdleInstanceCuller = None,
        image_auth: str = None,
        image_id: str = None,
        image_name: str = None,
        image_url: str = None,
        instance_id: str = None,
        instance_name: str = None,
        instance_shutdown_timer: ListInstancesResponseBodyInstancesInstanceShutdownTimer = None,
        instance_snapshot_list: List[ListInstancesResponseBodyInstancesInstanceSnapshotList] = None,
        instance_url: str = None,
        jupyterlab_url: str = None,
        labels: List[ListInstancesResponseBodyInstancesLabels] = None,
        latest_snapshot: ListInstancesResponseBodyInstancesLatestSnapshot = None,
        payment_type: str = None,
        priority: int = None,
        reason_code: str = None,
        reason_message: str = None,
        requested_resource: ListInstancesResponseBodyInstancesRequestedResource = None,
        resource_id: str = None,
        resource_name: str = None,
        status: str = None,
        system_image_url: str = None,
        terminal_url: str = None,
        user_id: str = None,
        user_name: str = None,
        user_vpc: ListInstancesResponseBodyInstancesUserVpc = None,
        web_ideurl: str = None,
        workspace_id: str = None,
        workspace_name: str = None,
        workspace_source: str = None,
    ):
        self.accelerator_type = accelerator_type
        self.accessibility = accessibility
        self.accumulated_running_time_in_ms = accumulated_running_time_in_ms
        self.affinity = affinity
        self.cloud_disks = cloud_disks
        self.datasets = datasets
        self.driver = driver
        self.dynamic_mount = dynamic_mount
        self.ecs_spec = ecs_spec
        self.environment_variables = environment_variables
        self.gmt_create_time = gmt_create_time
        self.gmt_modified_time = gmt_modified_time
        self.idle_instance_culler = idle_instance_culler
        self.image_auth = image_auth
        self.image_id = image_id
        self.image_name = image_name
        self.image_url = image_url
        self.instance_id = instance_id
        self.instance_name = instance_name
        self.instance_shutdown_timer = instance_shutdown_timer
        self.instance_snapshot_list = instance_snapshot_list
        self.instance_url = instance_url
        # Jupyterlab Url。
        self.jupyterlab_url = jupyterlab_url
        self.labels = labels
        self.latest_snapshot = latest_snapshot
        self.payment_type = payment_type
        self.priority = priority
        self.reason_code = reason_code
        self.reason_message = reason_message
        self.requested_resource = requested_resource
        self.resource_id = resource_id
        self.resource_name = resource_name
        self.status = status
        self.system_image_url = system_image_url
        self.terminal_url = terminal_url
        self.user_id = user_id
        self.user_name = user_name
        self.user_vpc = user_vpc
        # Web IDE url。
        self.web_ideurl = web_ideurl
        self.workspace_id = workspace_id
        self.workspace_name = workspace_name
        self.workspace_source = workspace_source

    def validate(self):
        if self.affinity:
            self.affinity.validate()
        if self.cloud_disks:
            for k in self.cloud_disks:
                if k:
                    k.validate()
        if self.datasets:
            for k in self.datasets:
                if k:
                    k.validate()
        if self.dynamic_mount:
            self.dynamic_mount.validate()
        if self.idle_instance_culler:
            self.idle_instance_culler.validate()
        if self.instance_shutdown_timer:
            self.instance_shutdown_timer.validate()
        if self.instance_snapshot_list:
            for k in self.instance_snapshot_list:
                if k:
                    k.validate()
        if self.labels:
            for k in self.labels:
                if k:
                    k.validate()
        if self.latest_snapshot:
            self.latest_snapshot.validate()
        if self.requested_resource:
            self.requested_resource.validate()
        if self.user_vpc:
            self.user_vpc.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.accelerator_type is not None:
            result['AcceleratorType'] = self.accelerator_type
        if self.accessibility is not None:
            result['Accessibility'] = self.accessibility
        if self.accumulated_running_time_in_ms is not None:
            result['AccumulatedRunningTimeInMs'] = self.accumulated_running_time_in_ms
        if self.affinity is not None:
            result['Affinity'] = self.affinity.to_map()
        result['CloudDisks'] = []
        if self.cloud_disks is not None:
            for k in self.cloud_disks:
                result['CloudDisks'].append(k.to_map() if k else None)
        result['Datasets'] = []
        if self.datasets is not None:
            for k in self.datasets:
                result['Datasets'].append(k.to_map() if k else None)
        if self.driver is not None:
            result['Driver'] = self.driver
        if self.dynamic_mount is not None:
            result['DynamicMount'] = self.dynamic_mount.to_map()
        if self.ecs_spec is not None:
            result['EcsSpec'] = self.ecs_spec
        if self.environment_variables is not None:
            result['EnvironmentVariables'] = self.environment_variables
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.idle_instance_culler is not None:
            result['IdleInstanceCuller'] = self.idle_instance_culler.to_map()
        if self.image_auth is not None:
            result['ImageAuth'] = self.image_auth
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.image_name is not None:
            result['ImageName'] = self.image_name
        if self.image_url is not None:
            result['ImageUrl'] = self.image_url
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        if self.instance_shutdown_timer is not None:
            result['InstanceShutdownTimer'] = self.instance_shutdown_timer.to_map()
        result['InstanceSnapshotList'] = []
        if self.instance_snapshot_list is not None:
            for k in self.instance_snapshot_list:
                result['InstanceSnapshotList'].append(k.to_map() if k else None)
        if self.instance_url is not None:
            result['InstanceUrl'] = self.instance_url
        if self.jupyterlab_url is not None:
            result['JupyterlabUrl'] = self.jupyterlab_url
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        if self.latest_snapshot is not None:
            result['LatestSnapshot'] = self.latest_snapshot.to_map()
        if self.payment_type is not None:
            result['PaymentType'] = self.payment_type
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.reason_code is not None:
            result['ReasonCode'] = self.reason_code
        if self.reason_message is not None:
            result['ReasonMessage'] = self.reason_message
        if self.requested_resource is not None:
            result['RequestedResource'] = self.requested_resource.to_map()
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_name is not None:
            result['ResourceName'] = self.resource_name
        if self.status is not None:
            result['Status'] = self.status
        if self.system_image_url is not None:
            result['SystemImageUrl'] = self.system_image_url
        if self.terminal_url is not None:
            result['TerminalUrl'] = self.terminal_url
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.user_name is not None:
            result['UserName'] = self.user_name
        if self.user_vpc is not None:
            result['UserVpc'] = self.user_vpc.to_map()
        if self.web_ideurl is not None:
            result['WebIDEUrl'] = self.web_ideurl
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        if self.workspace_name is not None:
            result['WorkspaceName'] = self.workspace_name
        if self.workspace_source is not None:
            result['WorkspaceSource'] = self.workspace_source
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AcceleratorType') is not None:
            self.accelerator_type = m.get('AcceleratorType')
        if m.get('Accessibility') is not None:
            self.accessibility = m.get('Accessibility')
        if m.get('AccumulatedRunningTimeInMs') is not None:
            self.accumulated_running_time_in_ms = m.get('AccumulatedRunningTimeInMs')
        if m.get('Affinity') is not None:
            temp_model = ListInstancesResponseBodyInstancesAffinity()
            self.affinity = temp_model.from_map(m['Affinity'])
        self.cloud_disks = []
        if m.get('CloudDisks') is not None:
            for k in m.get('CloudDisks'):
                temp_model = ListInstancesResponseBodyInstancesCloudDisks()
                self.cloud_disks.append(temp_model.from_map(k))
        self.datasets = []
        if m.get('Datasets') is not None:
            for k in m.get('Datasets'):
                temp_model = ListInstancesResponseBodyInstancesDatasets()
                self.datasets.append(temp_model.from_map(k))
        if m.get('Driver') is not None:
            self.driver = m.get('Driver')
        if m.get('DynamicMount') is not None:
            temp_model = DynamicMount()
            self.dynamic_mount = temp_model.from_map(m['DynamicMount'])
        if m.get('EcsSpec') is not None:
            self.ecs_spec = m.get('EcsSpec')
        if m.get('EnvironmentVariables') is not None:
            self.environment_variables = m.get('EnvironmentVariables')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('IdleInstanceCuller') is not None:
            temp_model = ListInstancesResponseBodyInstancesIdleInstanceCuller()
            self.idle_instance_culler = temp_model.from_map(m['IdleInstanceCuller'])
        if m.get('ImageAuth') is not None:
            self.image_auth = m.get('ImageAuth')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('ImageName') is not None:
            self.image_name = m.get('ImageName')
        if m.get('ImageUrl') is not None:
            self.image_url = m.get('ImageUrl')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        if m.get('InstanceShutdownTimer') is not None:
            temp_model = ListInstancesResponseBodyInstancesInstanceShutdownTimer()
            self.instance_shutdown_timer = temp_model.from_map(m['InstanceShutdownTimer'])
        self.instance_snapshot_list = []
        if m.get('InstanceSnapshotList') is not None:
            for k in m.get('InstanceSnapshotList'):
                temp_model = ListInstancesResponseBodyInstancesInstanceSnapshotList()
                self.instance_snapshot_list.append(temp_model.from_map(k))
        if m.get('InstanceUrl') is not None:
            self.instance_url = m.get('InstanceUrl')
        if m.get('JupyterlabUrl') is not None:
            self.jupyterlab_url = m.get('JupyterlabUrl')
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = ListInstancesResponseBodyInstancesLabels()
                self.labels.append(temp_model.from_map(k))
        if m.get('LatestSnapshot') is not None:
            temp_model = ListInstancesResponseBodyInstancesLatestSnapshot()
            self.latest_snapshot = temp_model.from_map(m['LatestSnapshot'])
        if m.get('PaymentType') is not None:
            self.payment_type = m.get('PaymentType')
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('ReasonCode') is not None:
            self.reason_code = m.get('ReasonCode')
        if m.get('ReasonMessage') is not None:
            self.reason_message = m.get('ReasonMessage')
        if m.get('RequestedResource') is not None:
            temp_model = ListInstancesResponseBodyInstancesRequestedResource()
            self.requested_resource = temp_model.from_map(m['RequestedResource'])
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceName') is not None:
            self.resource_name = m.get('ResourceName')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('SystemImageUrl') is not None:
            self.system_image_url = m.get('SystemImageUrl')
        if m.get('TerminalUrl') is not None:
            self.terminal_url = m.get('TerminalUrl')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('UserName') is not None:
            self.user_name = m.get('UserName')
        if m.get('UserVpc') is not None:
            temp_model = ListInstancesResponseBodyInstancesUserVpc()
            self.user_vpc = temp_model.from_map(m['UserVpc'])
        if m.get('WebIDEUrl') is not None:
            self.web_ideurl = m.get('WebIDEUrl')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        if m.get('WorkspaceName') is not None:
            self.workspace_name = m.get('WorkspaceName')
        if m.get('WorkspaceSource') is not None:
            self.workspace_source = m.get('WorkspaceSource')
        return self


class ListInstancesResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        http_status_code: int = None,
        instances: List[ListInstancesResponseBodyInstances] = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
        total_count: int = None,
    ):
        self.code = code
        self.http_status_code = http_status_code
        self.instances = instances
        self.message = message
        self.request_id = request_id
        self.success = success
        self.total_count = total_count

    def validate(self):
        if self.instances:
            for k in self.instances:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        result['Instances'] = []
        if self.instances is not None:
            for k in self.instances:
                result['Instances'].append(k.to_map() if k else None)
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        self.instances = []
        if m.get('Instances') is not None:
            for k in m.get('Instances'):
                temp_model = ListInstancesResponseBodyInstances()
                self.instances.append(temp_model.from_map(k))
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListInstancesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListInstancesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListInstancesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListSharesRequest(TeaModel):
    def __init__(
        self,
        expiration_time_greater_than: str = None,
        expiration_time_less_than: str = None,
        file_name: str = None,
        version: str = None,
    ):
        self.expiration_time_greater_than = expiration_time_greater_than
        self.expiration_time_less_than = expiration_time_less_than
        self.file_name = file_name
        self.version = version

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.expiration_time_greater_than is not None:
            result['ExpirationTimeGreaterThan'] = self.expiration_time_greater_than
        if self.expiration_time_less_than is not None:
            result['ExpirationTimeLessThan'] = self.expiration_time_less_than
        if self.file_name is not None:
            result['FileName'] = self.file_name
        if self.version is not None:
            result['Version'] = self.version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ExpirationTimeGreaterThan') is not None:
            self.expiration_time_greater_than = m.get('ExpirationTimeGreaterThan')
        if m.get('ExpirationTimeLessThan') is not None:
            self.expiration_time_less_than = m.get('ExpirationTimeLessThan')
        if m.get('FileName') is not None:
            self.file_name = m.get('FileName')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        return self


class ListSharesResponseBodyShares(TeaModel):
    def __init__(
        self,
        expiration_time: str = None,
        file_name: str = None,
        gmt_create_time: str = None,
        gmt_modified_time: str = None,
        resource_url: str = None,
        ttl: int = None,
        user_id: str = None,
        version: str = None,
    ):
        self.expiration_time = expiration_time
        self.file_name = file_name
        self.gmt_create_time = gmt_create_time
        self.gmt_modified_time = gmt_modified_time
        self.resource_url = resource_url
        self.ttl = ttl
        self.user_id = user_id
        self.version = version

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.expiration_time is not None:
            result['ExpirationTime'] = self.expiration_time
        if self.file_name is not None:
            result['FileName'] = self.file_name
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.resource_url is not None:
            result['ResourceUrl'] = self.resource_url
        if self.ttl is not None:
            result['Ttl'] = self.ttl
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.version is not None:
            result['Version'] = self.version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ExpirationTime') is not None:
            self.expiration_time = m.get('ExpirationTime')
        if m.get('FileName') is not None:
            self.file_name = m.get('FileName')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('ResourceUrl') is not None:
            self.resource_url = m.get('ResourceUrl')
        if m.get('Ttl') is not None:
            self.ttl = m.get('Ttl')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        return self


class ListSharesResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        http_status_code: int = None,
        message: str = None,
        request_id: str = None,
        shares: List[ListSharesResponseBodyShares] = None,
        success: bool = None,
    ):
        self.code = code
        self.http_status_code = http_status_code
        self.message = message
        self.request_id = request_id
        self.shares = shares
        self.success = success

    def validate(self):
        if self.shares:
            for k in self.shares:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Shares'] = []
        if self.shares is not None:
            for k in self.shares:
                result['Shares'].append(k.to_map() if k else None)
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.shares = []
        if m.get('Shares') is not None:
            for k in m.get('Shares'):
                temp_model = ListSharesResponseBodyShares()
                self.shares.append(temp_model.from_map(k))
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ListSharesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListSharesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListSharesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListTempFilesRequest(TeaModel):
    def __init__(
        self,
        delimiter: str = None,
        instance_id: str = None,
        name: str = None,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        prefix: str = None,
        sort_by: str = None,
    ):
        self.delimiter = delimiter
        self.instance_id = instance_id
        self.name = name
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        self.prefix = prefix
        self.sort_by = sort_by

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.delimiter is not None:
            result['Delimiter'] = self.delimiter
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.name is not None:
            result['Name'] = self.name
        if self.order is not None:
            result['Order'] = self.order
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.prefix is not None:
            result['Prefix'] = self.prefix
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Delimiter') is not None:
            self.delimiter = m.get('Delimiter')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Prefix') is not None:
            self.prefix = m.get('Prefix')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        return self


class ListTempFilesResponseBodyQuota(TeaModel):
    def __init__(
        self,
        total_capacity: int = None,
        total_file_num: int = None,
        used_capacity: int = None,
        used_file_num: int = None,
    ):
        self.total_capacity = total_capacity
        self.total_file_num = total_file_num
        self.used_capacity = used_capacity
        self.used_file_num = used_file_num

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.total_capacity is not None:
            result['TotalCapacity'] = self.total_capacity
        if self.total_file_num is not None:
            result['TotalFileNum'] = self.total_file_num
        if self.used_capacity is not None:
            result['UsedCapacity'] = self.used_capacity
        if self.used_file_num is not None:
            result['UsedFileNum'] = self.used_file_num
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCapacity') is not None:
            self.total_capacity = m.get('TotalCapacity')
        if m.get('TotalFileNum') is not None:
            self.total_file_num = m.get('TotalFileNum')
        if m.get('UsedCapacity') is not None:
            self.used_capacity = m.get('UsedCapacity')
        if m.get('UsedFileNum') is not None:
            self.used_file_num = m.get('UsedFileNum')
        return self


class ListTempFilesResponseBodyTempFiles(TeaModel):
    def __init__(
        self,
        bandwidth: int = None,
        capacity: int = None,
        description: str = None,
        download_url: str = None,
        gmt_create_time: str = None,
        gmt_expired_time: str = None,
        gmt_modified_time: str = None,
        instance_id: str = None,
        name: str = None,
        owner_id: str = None,
        prefix: str = None,
        status: str = None,
        task_id: str = None,
        type: str = None,
        upload_url: str = None,
        user_id: str = None,
        uuid: str = None,
    ):
        self.bandwidth = bandwidth
        self.capacity = capacity
        self.description = description
        self.download_url = download_url
        self.gmt_create_time = gmt_create_time
        self.gmt_expired_time = gmt_expired_time
        self.gmt_modified_time = gmt_modified_time
        self.instance_id = instance_id
        self.name = name
        self.owner_id = owner_id
        self.prefix = prefix
        self.status = status
        self.task_id = task_id
        self.type = type
        self.upload_url = upload_url
        self.user_id = user_id
        self.uuid = uuid

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.bandwidth is not None:
            result['Bandwidth'] = self.bandwidth
        if self.capacity is not None:
            result['Capacity'] = self.capacity
        if self.description is not None:
            result['Description'] = self.description
        if self.download_url is not None:
            result['DownloadUrl'] = self.download_url
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_expired_time is not None:
            result['GmtExpiredTime'] = self.gmt_expired_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.name is not None:
            result['Name'] = self.name
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.prefix is not None:
            result['Prefix'] = self.prefix
        if self.status is not None:
            result['Status'] = self.status
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.type is not None:
            result['Type'] = self.type
        if self.upload_url is not None:
            result['UploadUrl'] = self.upload_url
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.uuid is not None:
            result['Uuid'] = self.uuid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Bandwidth') is not None:
            self.bandwidth = m.get('Bandwidth')
        if m.get('Capacity') is not None:
            self.capacity = m.get('Capacity')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('DownloadUrl') is not None:
            self.download_url = m.get('DownloadUrl')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtExpiredTime') is not None:
            self.gmt_expired_time = m.get('GmtExpiredTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('Prefix') is not None:
            self.prefix = m.get('Prefix')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('UploadUrl') is not None:
            self.upload_url = m.get('UploadUrl')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('Uuid') is not None:
            self.uuid = m.get('Uuid')
        return self


class ListTempFilesResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        http_status_code: int = None,
        message: str = None,
        quota: ListTempFilesResponseBodyQuota = None,
        request_id: str = None,
        success: bool = None,
        temp_files: List[ListTempFilesResponseBodyTempFiles] = None,
        total_count: int = None,
    ):
        self.code = code
        self.http_status_code = http_status_code
        self.message = message
        self.quota = quota
        self.request_id = request_id
        self.success = success
        self.temp_files = temp_files
        self.total_count = total_count

    def validate(self):
        if self.quota:
            self.quota.validate()
        if self.temp_files:
            for k in self.temp_files:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.message is not None:
            result['Message'] = self.message
        if self.quota is not None:
            result['Quota'] = self.quota.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        result['TempFiles'] = []
        if self.temp_files is not None:
            for k in self.temp_files:
                result['TempFiles'].append(k.to_map() if k else None)
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('Quota') is not None:
            temp_model = ListTempFilesResponseBodyQuota()
            self.quota = temp_model.from_map(m['Quota'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        self.temp_files = []
        if m.get('TempFiles') is not None:
            for k in m.get('TempFiles'):
                temp_model = ListTempFilesResponseBodyTempFiles()
                self.temp_files.append(temp_model.from_map(k))
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListTempFilesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListTempFilesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListTempFilesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StartInstanceResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        http_status_code: int = None,
        instance_id: str = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.code = code
        self.http_status_code = http_status_code
        self.instance_id = instance_id
        self.message = message
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class StartInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: StartInstanceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = StartInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StopInstanceRequest(TeaModel):
    def __init__(
        self,
        save_image: bool = None,
    ):
        self.save_image = save_image

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.save_image is not None:
            result['SaveImage'] = self.save_image
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SaveImage') is not None:
            self.save_image = m.get('SaveImage')
        return self


class StopInstanceResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        http_status_code: int = None,
        instance_id: str = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.code = code
        self.http_status_code = http_status_code
        self.instance_id = instance_id
        self.message = message
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class StopInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: StopInstanceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = StopInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateInstanceRequestAffinityCPU(TeaModel):
    def __init__(
        self,
        enable: bool = None,
    ):
        self.enable = enable

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.enable is not None:
            result['Enable'] = self.enable
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Enable') is not None:
            self.enable = m.get('Enable')
        return self


class UpdateInstanceRequestAffinity(TeaModel):
    def __init__(
        self,
        cpu: UpdateInstanceRequestAffinityCPU = None,
    ):
        self.cpu = cpu

    def validate(self):
        if self.cpu:
            self.cpu.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cpu is not None:
            result['CPU'] = self.cpu.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CPU') is not None:
            temp_model = UpdateInstanceRequestAffinityCPU()
            self.cpu = temp_model.from_map(m['CPU'])
        return self


class UpdateInstanceRequestCloudDisks(TeaModel):
    def __init__(
        self,
        capacity: str = None,
        sub_type: str = None,
    ):
        self.capacity = capacity
        self.sub_type = sub_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.capacity is not None:
            result['Capacity'] = self.capacity
        if self.sub_type is not None:
            result['SubType'] = self.sub_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Capacity') is not None:
            self.capacity = m.get('Capacity')
        if m.get('SubType') is not None:
            self.sub_type = m.get('SubType')
        return self


class UpdateInstanceRequestDatasets(TeaModel):
    def __init__(
        self,
        dataset_id: str = None,
        dynamic: bool = None,
        mount_path: str = None,
        option_type: str = None,
        options: str = None,
        uri: str = None,
    ):
        self.dataset_id = dataset_id
        self.dynamic = dynamic
        self.mount_path = mount_path
        self.option_type = option_type
        self.options = options
        self.uri = uri

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.dataset_id is not None:
            result['DatasetId'] = self.dataset_id
        if self.dynamic is not None:
            result['Dynamic'] = self.dynamic
        if self.mount_path is not None:
            result['MountPath'] = self.mount_path
        if self.option_type is not None:
            result['OptionType'] = self.option_type
        if self.options is not None:
            result['Options'] = self.options
        if self.uri is not None:
            result['Uri'] = self.uri
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DatasetId') is not None:
            self.dataset_id = m.get('DatasetId')
        if m.get('Dynamic') is not None:
            self.dynamic = m.get('Dynamic')
        if m.get('MountPath') is not None:
            self.mount_path = m.get('MountPath')
        if m.get('OptionType') is not None:
            self.option_type = m.get('OptionType')
        if m.get('Options') is not None:
            self.options = m.get('Options')
        if m.get('Uri') is not None:
            self.uri = m.get('Uri')
        return self


class UpdateInstanceRequestRequestedResource(TeaModel):
    def __init__(
        self,
        cpu: str = None,
        gpu: str = None,
        gputype: str = None,
        memory: str = None,
        shared_memory: str = None,
    ):
        self.cpu = cpu
        self.gpu = gpu
        self.gputype = gputype
        self.memory = memory
        self.shared_memory = shared_memory

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cpu is not None:
            result['CPU'] = self.cpu
        if self.gpu is not None:
            result['GPU'] = self.gpu
        if self.gputype is not None:
            result['GPUType'] = self.gputype
        if self.memory is not None:
            result['Memory'] = self.memory
        if self.shared_memory is not None:
            result['SharedMemory'] = self.shared_memory
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CPU') is not None:
            self.cpu = m.get('CPU')
        if m.get('GPU') is not None:
            self.gpu = m.get('GPU')
        if m.get('GPUType') is not None:
            self.gputype = m.get('GPUType')
        if m.get('Memory') is not None:
            self.memory = m.get('Memory')
        if m.get('SharedMemory') is not None:
            self.shared_memory = m.get('SharedMemory')
        return self


class UpdateInstanceRequestUserVpc(TeaModel):
    def __init__(
        self,
        default_route: str = None,
        extended_cidrs: List[str] = None,
        forward_infos: List[ForwardInfo] = None,
        security_group_id: str = None,
        v_switch_id: str = None,
        vpc_id: str = None,
    ):
        self.default_route = default_route
        self.extended_cidrs = extended_cidrs
        self.forward_infos = forward_infos
        self.security_group_id = security_group_id
        self.v_switch_id = v_switch_id
        self.vpc_id = vpc_id

    def validate(self):
        if self.forward_infos:
            for k in self.forward_infos:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.default_route is not None:
            result['DefaultRoute'] = self.default_route
        if self.extended_cidrs is not None:
            result['ExtendedCIDRs'] = self.extended_cidrs
        result['ForwardInfos'] = []
        if self.forward_infos is not None:
            for k in self.forward_infos:
                result['ForwardInfos'].append(k.to_map() if k else None)
        if self.security_group_id is not None:
            result['SecurityGroupId'] = self.security_group_id
        if self.v_switch_id is not None:
            result['VSwitchId'] = self.v_switch_id
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DefaultRoute') is not None:
            self.default_route = m.get('DefaultRoute')
        if m.get('ExtendedCIDRs') is not None:
            self.extended_cidrs = m.get('ExtendedCIDRs')
        self.forward_infos = []
        if m.get('ForwardInfos') is not None:
            for k in m.get('ForwardInfos'):
                temp_model = ForwardInfo()
                self.forward_infos.append(temp_model.from_map(k))
        if m.get('SecurityGroupId') is not None:
            self.security_group_id = m.get('SecurityGroupId')
        if m.get('VSwitchId') is not None:
            self.v_switch_id = m.get('VSwitchId')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        return self


class UpdateInstanceRequest(TeaModel):
    def __init__(
        self,
        accessibility: str = None,
        affinity: UpdateInstanceRequestAffinity = None,
        cloud_disks: List[UpdateInstanceRequestCloudDisks] = None,
        credential_config: CredentialConfig = None,
        datasets: List[UpdateInstanceRequestDatasets] = None,
        disassociate_credential: bool = None,
        disassociate_datasets: bool = None,
        disassociate_driver: bool = None,
        disassociate_forward_infos: bool = None,
        disassociate_vpc: bool = None,
        driver: str = None,
        dynamic_mount: DynamicMount = None,
        ecs_spec: str = None,
        image_auth: str = None,
        image_id: str = None,
        image_url: str = None,
        instance_name: str = None,
        priority: int = None,
        requested_resource: UpdateInstanceRequestRequestedResource = None,
        system_image_url: str = None,
        user_id: str = None,
        user_vpc: UpdateInstanceRequestUserVpc = None,
        workspace_source: str = None,
    ):
        self.accessibility = accessibility
        self.affinity = affinity
        self.cloud_disks = cloud_disks
        self.credential_config = credential_config
        self.datasets = datasets
        self.disassociate_credential = disassociate_credential
        self.disassociate_datasets = disassociate_datasets
        self.disassociate_driver = disassociate_driver
        self.disassociate_forward_infos = disassociate_forward_infos
        self.disassociate_vpc = disassociate_vpc
        self.driver = driver
        self.dynamic_mount = dynamic_mount
        self.ecs_spec = ecs_spec
        self.image_auth = image_auth
        self.image_id = image_id
        self.image_url = image_url
        self.instance_name = instance_name
        self.priority = priority
        self.requested_resource = requested_resource
        self.system_image_url = system_image_url
        self.user_id = user_id
        self.user_vpc = user_vpc
        self.workspace_source = workspace_source

    def validate(self):
        if self.affinity:
            self.affinity.validate()
        if self.cloud_disks:
            for k in self.cloud_disks:
                if k:
                    k.validate()
        if self.credential_config:
            self.credential_config.validate()
        if self.datasets:
            for k in self.datasets:
                if k:
                    k.validate()
        if self.dynamic_mount:
            self.dynamic_mount.validate()
        if self.requested_resource:
            self.requested_resource.validate()
        if self.user_vpc:
            self.user_vpc.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.accessibility is not None:
            result['Accessibility'] = self.accessibility
        if self.affinity is not None:
            result['Affinity'] = self.affinity.to_map()
        result['CloudDisks'] = []
        if self.cloud_disks is not None:
            for k in self.cloud_disks:
                result['CloudDisks'].append(k.to_map() if k else None)
        if self.credential_config is not None:
            result['CredentialConfig'] = self.credential_config.to_map()
        result['Datasets'] = []
        if self.datasets is not None:
            for k in self.datasets:
                result['Datasets'].append(k.to_map() if k else None)
        if self.disassociate_credential is not None:
            result['DisassociateCredential'] = self.disassociate_credential
        if self.disassociate_datasets is not None:
            result['DisassociateDatasets'] = self.disassociate_datasets
        if self.disassociate_driver is not None:
            result['DisassociateDriver'] = self.disassociate_driver
        if self.disassociate_forward_infos is not None:
            result['DisassociateForwardInfos'] = self.disassociate_forward_infos
        if self.disassociate_vpc is not None:
            result['DisassociateVpc'] = self.disassociate_vpc
        if self.driver is not None:
            result['Driver'] = self.driver
        if self.dynamic_mount is not None:
            result['DynamicMount'] = self.dynamic_mount.to_map()
        if self.ecs_spec is not None:
            result['EcsSpec'] = self.ecs_spec
        if self.image_auth is not None:
            result['ImageAuth'] = self.image_auth
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.image_url is not None:
            result['ImageUrl'] = self.image_url
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.requested_resource is not None:
            result['RequestedResource'] = self.requested_resource.to_map()
        if self.system_image_url is not None:
            result['SystemImageUrl'] = self.system_image_url
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.user_vpc is not None:
            result['UserVpc'] = self.user_vpc.to_map()
        if self.workspace_source is not None:
            result['WorkspaceSource'] = self.workspace_source
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Accessibility') is not None:
            self.accessibility = m.get('Accessibility')
        if m.get('Affinity') is not None:
            temp_model = UpdateInstanceRequestAffinity()
            self.affinity = temp_model.from_map(m['Affinity'])
        self.cloud_disks = []
        if m.get('CloudDisks') is not None:
            for k in m.get('CloudDisks'):
                temp_model = UpdateInstanceRequestCloudDisks()
                self.cloud_disks.append(temp_model.from_map(k))
        if m.get('CredentialConfig') is not None:
            temp_model = CredentialConfig()
            self.credential_config = temp_model.from_map(m['CredentialConfig'])
        self.datasets = []
        if m.get('Datasets') is not None:
            for k in m.get('Datasets'):
                temp_model = UpdateInstanceRequestDatasets()
                self.datasets.append(temp_model.from_map(k))
        if m.get('DisassociateCredential') is not None:
            self.disassociate_credential = m.get('DisassociateCredential')
        if m.get('DisassociateDatasets') is not None:
            self.disassociate_datasets = m.get('DisassociateDatasets')
        if m.get('DisassociateDriver') is not None:
            self.disassociate_driver = m.get('DisassociateDriver')
        if m.get('DisassociateForwardInfos') is not None:
            self.disassociate_forward_infos = m.get('DisassociateForwardInfos')
        if m.get('DisassociateVpc') is not None:
            self.disassociate_vpc = m.get('DisassociateVpc')
        if m.get('Driver') is not None:
            self.driver = m.get('Driver')
        if m.get('DynamicMount') is not None:
            temp_model = DynamicMount()
            self.dynamic_mount = temp_model.from_map(m['DynamicMount'])
        if m.get('EcsSpec') is not None:
            self.ecs_spec = m.get('EcsSpec')
        if m.get('ImageAuth') is not None:
            self.image_auth = m.get('ImageAuth')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('ImageUrl') is not None:
            self.image_url = m.get('ImageUrl')
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('RequestedResource') is not None:
            temp_model = UpdateInstanceRequestRequestedResource()
            self.requested_resource = temp_model.from_map(m['RequestedResource'])
        if m.get('SystemImageUrl') is not None:
            self.system_image_url = m.get('SystemImageUrl')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('UserVpc') is not None:
            temp_model = UpdateInstanceRequestUserVpc()
            self.user_vpc = temp_model.from_map(m['UserVpc'])
        if m.get('WorkspaceSource') is not None:
            self.workspace_source = m.get('WorkspaceSource')
        return self


class UpdateInstanceResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        http_status_code: int = None,
        instance_id: str = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.code = code
        self.http_status_code = http_status_code
        self.instance_id = instance_id
        self.message = message
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class UpdateInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateInstanceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateInstanceLabelsRequestLabels(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        # This parameter is required.
        self.key = key
        # This parameter is required.
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class UpdateInstanceLabelsRequest(TeaModel):
    def __init__(
        self,
        labels: List[UpdateInstanceLabelsRequestLabels] = None,
    ):
        # This parameter is required.
        self.labels = labels

    def validate(self):
        if self.labels:
            for k in self.labels:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = UpdateInstanceLabelsRequestLabels()
                self.labels.append(temp_model.from_map(k))
        return self


class UpdateInstanceLabelsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateInstanceLabelsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateInstanceLabelsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateInstanceLabelsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateTempFileRequest(TeaModel):
    def __init__(
        self,
        gmt_expired_time: str = None,
        status: str = None,
    ):
        self.gmt_expired_time = gmt_expired_time
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.gmt_expired_time is not None:
            result['GmtExpiredTime'] = self.gmt_expired_time
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GmtExpiredTime') is not None:
            self.gmt_expired_time = m.get('GmtExpiredTime')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class UpdateTempFileResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        http_status_code: int = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
        temp_file_id: str = None,
    ):
        self.code = code
        self.http_status_code = http_status_code
        self.message = message
        self.request_id = request_id
        self.success = success
        self.temp_file_id = temp_file_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.temp_file_id is not None:
            result['TempFileId'] = self.temp_file_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('TempFileId') is not None:
            self.temp_file_id = m.get('TempFileId')
        return self


class UpdateTempFileResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateTempFileResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateTempFileResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateTempFileTaskRequest(TeaModel):
    def __init__(
        self,
        gmt_expired_time: str = None,
    ):
        self.gmt_expired_time = gmt_expired_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.gmt_expired_time is not None:
            result['GmtExpiredTime'] = self.gmt_expired_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GmtExpiredTime') is not None:
            self.gmt_expired_time = m.get('GmtExpiredTime')
        return self


class UpdateTempFileTaskResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        http_status_code: int = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
        temp_file_task_id: str = None,
    ):
        self.code = code
        self.http_status_code = http_status_code
        self.message = message
        self.request_id = request_id
        self.success = success
        self.temp_file_task_id = temp_file_task_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.temp_file_task_id is not None:
            result['TempFileTaskId'] = self.temp_file_task_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('TempFileTaskId') is not None:
            self.temp_file_task_id = m.get('TempFileTaskId')
        return self


class UpdateTempFileTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateTempFileTaskResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateTempFileTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


