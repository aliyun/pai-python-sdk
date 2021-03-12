# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel
from Tea.converter import TeaConverter


class CreatePipelineRequest(TeaModel):
    def __init__(self, workspace_id=None, manifest=None):
        self.workspace_id = TeaConverter.to_unicode(workspace_id)  # type: unicode
        self.manifest = TeaConverter.to_unicode(manifest)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        if self.manifest is not None:
            result['Manifest'] = self.manifest
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        if m.get('Manifest') is not None:
            self.manifest = m.get('Manifest')
        return self


class CreatePipelineResponseBody(TeaModel):
    def __init__(self, request_id=None, pipeline_id=None):
        # Id of the request
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        self.pipeline_id = TeaConverter.to_unicode(pipeline_id)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.pipeline_id is not None:
            result['PipelineId'] = self.pipeline_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PipelineId') is not None:
            self.pipeline_id = m.get('PipelineId')
        return self


class CreatePipelineResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: CreatePipelineResponseBody

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
            temp_model = CreatePipelineResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreatePipelineReleaseRequest(TeaModel):
    def __init__(self, target_pipeline_provider=None):
        self.target_pipeline_provider = TeaConverter.to_unicode(target_pipeline_provider)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.target_pipeline_provider is not None:
            result['TargetPipelineProvider'] = self.target_pipeline_provider
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('TargetPipelineProvider') is not None:
            self.target_pipeline_provider = m.get('TargetPipelineProvider')
        return self


class CreatePipelineReleaseResponseBody(TeaModel):
    def __init__(self, request_id=None, pipeline_id=None):
        # Id of the request
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        self.pipeline_id = TeaConverter.to_unicode(pipeline_id)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.pipeline_id is not None:
            result['PipelineId'] = self.pipeline_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PipelineId') is not None:
            self.pipeline_id = m.get('PipelineId')
        return self


class CreatePipelineReleaseResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: CreatePipelineReleaseResponseBody

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
            temp_model = CreatePipelineReleaseResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateRunRequest(TeaModel):
    def __init__(self, pipeline_id=None, name=None, pipeline_manifest=None, arguments=None,
                 no_confirm_required=None, workspace_id=None, source=None):
        self.pipeline_id = TeaConverter.to_unicode(pipeline_id)  # type: unicode
        self.name = TeaConverter.to_unicode(name)  # type: unicode
        self.pipeline_manifest = TeaConverter.to_unicode(pipeline_manifest)  # type: unicode
        self.arguments = TeaConverter.to_unicode(arguments)  # type: unicode
        self.no_confirm_required = no_confirm_required  # type: bool
        self.workspace_id = TeaConverter.to_unicode(workspace_id)  # type: unicode
        self.source = TeaConverter.to_unicode(source)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.pipeline_id is not None:
            result['PipelineId'] = self.pipeline_id
        if self.name is not None:
            result['Name'] = self.name
        if self.pipeline_manifest is not None:
            result['PipelineManifest'] = self.pipeline_manifest
        if self.arguments is not None:
            result['Arguments'] = self.arguments
        if self.no_confirm_required is not None:
            result['NoConfirmRequired'] = self.no_confirm_required
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        if self.source is not None:
            result['Source'] = self.source
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('PipelineId') is not None:
            self.pipeline_id = m.get('PipelineId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('PipelineManifest') is not None:
            self.pipeline_manifest = m.get('PipelineManifest')
        if m.get('Arguments') is not None:
            self.arguments = m.get('Arguments')
        if m.get('NoConfirmRequired') is not None:
            self.no_confirm_required = m.get('NoConfirmRequired')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        if m.get('Source') is not None:
            self.source = m.get('Source')
        return self


class CreateRunResponseBody(TeaModel):
    def __init__(self, request_id=None, run_id=None):
        # Id of the request
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        self.run_id = TeaConverter.to_unicode(run_id)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.run_id is not None:
            result['RunId'] = self.run_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('RunId') is not None:
            self.run_id = m.get('RunId')
        return self


class CreateRunResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: CreateRunResponseBody

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
            temp_model = CreateRunResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeletePipelineResponseBody(TeaModel):
    def __init__(self, request_id=None):
        # Id of the request
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


class DeletePipelineResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: DeletePipelineResponseBody

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
            temp_model = DeletePipelineResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetCallerProviderResponseBody(TeaModel):
    def __init__(self, request_id=None, provider=None):
        # Id of the request
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        self.provider = TeaConverter.to_unicode(provider)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.provider is not None:
            result['Provider'] = self.provider
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Provider') is not None:
            self.provider = m.get('Provider')
        return self


class GetCallerProviderResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: GetCallerProviderResponseBody

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
            temp_model = GetCallerProviderResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetNodeRequest(TeaModel):
    def __init__(self, depth=None):
        self.depth = depth  # type: int

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.depth is not None:
            result['Depth'] = self.depth
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Depth') is not None:
            self.depth = m.get('Depth')
        return self


class GetNodeResponseBodyMetadata(TeaModel):
    def __init__(self, identifier=None, name=None, provider=None, node_id=None, version=None):
        # 标识符
        self.identifier = TeaConverter.to_unicode(identifier)  # type: unicode
        # 名字
        self.name = TeaConverter.to_unicode(name)  # type: unicode
        # 提供方
        self.provider = TeaConverter.to_unicode(provider)  # type: unicode
        # 节点id
        self.node_id = TeaConverter.to_unicode(node_id)  # type: unicode
        # 版本
        self.version = TeaConverter.to_unicode(version)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.identifier is not None:
            result['Identifier'] = self.identifier
        if self.name is not None:
            result['Name'] = self.name
        if self.provider is not None:
            result['Provider'] = self.provider
        if self.node_id is not None:
            result['NodeId'] = self.node_id
        if self.version is not None:
            result['Version'] = self.version
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Identifier') is not None:
            self.identifier = m.get('Identifier')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Provider') is not None:
            self.provider = m.get('Provider')
        if m.get('NodeId') is not None:
            self.node_id = m.get('NodeId')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        return self


class GetNodeResponseBodySpecInputs(TeaModel):
    def __init__(self, artifacts=None, parameters=None):
        # artifacts
        self.artifacts = artifacts  # type: list[dict[unicode, any]]
        # 参数
        self.parameters = parameters  # type: list[dict[unicode, any]]

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.artifacts is not None:
            result['Artifacts'] = self.artifacts
        if self.parameters is not None:
            result['Parameters'] = self.parameters
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Artifacts') is not None:
            self.artifacts = m.get('Artifacts')
        if m.get('Parameters') is not None:
            self.parameters = m.get('Parameters')
        return self


class GetNodeResponseBodySpecOutputs(TeaModel):
    def __init__(self, artifacts=None, parameters=None):
        # artifacts
        self.artifacts = artifacts  # type: list[dict[unicode, any]]
        # 参数
        self.parameters = parameters  # type: list[dict[unicode, any]]

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.artifacts is not None:
            result['Artifacts'] = self.artifacts
        if self.parameters is not None:
            result['Parameters'] = self.parameters
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Artifacts') is not None:
            self.artifacts = m.get('Artifacts')
        if m.get('Parameters') is not None:
            self.parameters = m.get('Parameters')
        return self


class GetNodeResponseBodySpec(TeaModel):
    def __init__(self, has_pipelines=None, dependencies=None, pipelines=None, inputs=None, outputs=None):
        # 是否有pipeline
        self.has_pipelines = has_pipelines  # type: bool
        # 依赖列表
        self.dependencies = dependencies  # type: list[unicode]
        # pipeline列表
        self.pipelines = pipelines  # type: list[dict[unicode, any]]
        # 输入
        self.inputs = inputs  # type: GetNodeResponseBodySpecInputs
        # 输出
        self.outputs = outputs  # type: GetNodeResponseBodySpecOutputs

    def validate(self):
        if self.inputs:
            self.inputs.validate()
        if self.outputs:
            self.outputs.validate()

    def to_map(self):
        result = dict()
        if self.has_pipelines is not None:
            result['HasPipelines'] = self.has_pipelines
        if self.dependencies is not None:
            result['Dependencies'] = self.dependencies
        if self.pipelines is not None:
            result['Pipelines'] = self.pipelines
        if self.inputs is not None:
            result['Inputs'] = self.inputs.to_map()
        if self.outputs is not None:
            result['Outputs'] = self.outputs.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('HasPipelines') is not None:
            self.has_pipelines = m.get('HasPipelines')
        if m.get('Dependencies') is not None:
            self.dependencies = m.get('Dependencies')
        if m.get('Pipelines') is not None:
            self.pipelines = m.get('Pipelines')
        if m.get('Inputs') is not None:
            temp_model = GetNodeResponseBodySpecInputs()
            self.inputs = temp_model.from_map(m['Inputs'])
        if m.get('Outputs') is not None:
            temp_model = GetNodeResponseBodySpecOutputs()
            self.outputs = temp_model.from_map(m['Outputs'])
        return self


class GetNodeResponseBodyStatusInfo(TeaModel):
    def __init__(self, finished_at=None, started_at=None, status=None):
        # 结束时间
        self.finished_at = TeaConverter.to_unicode(finished_at)  # type: unicode
        # 开始时间
        self.started_at = TeaConverter.to_unicode(started_at)  # type: unicode
        # 状态
        self.status = TeaConverter.to_unicode(status)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.finished_at is not None:
            result['FinishedAt'] = self.finished_at
        if self.started_at is not None:
            result['StartedAt'] = self.started_at
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('FinishedAt') is not None:
            self.finished_at = m.get('FinishedAt')
        if m.get('StartedAt') is not None:
            self.started_at = m.get('StartedAt')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class GetNodeResponseBody(TeaModel):
    def __init__(self, request_id=None, api_version=None, metadata=None, spec=None, status_info=None):
        # Id of the request
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        self.api_version = TeaConverter.to_unicode(api_version)  # type: unicode
        self.metadata = metadata  # type: GetNodeResponseBodyMetadata
        # 算法体
        self.spec = spec  # type: GetNodeResponseBodySpec
        # 状态
        self.status_info = status_info  # type: GetNodeResponseBodyStatusInfo

    def validate(self):
        if self.metadata:
            self.metadata.validate()
        if self.spec:
            self.spec.validate()
        if self.status_info:
            self.status_info.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.api_version is not None:
            result['ApiVersion'] = self.api_version
        if self.metadata is not None:
            result['Metadata'] = self.metadata.to_map()
        if self.spec is not None:
            result['Spec'] = self.spec.to_map()
        if self.status_info is not None:
            result['StatusInfo'] = self.status_info.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ApiVersion') is not None:
            self.api_version = m.get('ApiVersion')
        if m.get('Metadata') is not None:
            temp_model = GetNodeResponseBodyMetadata()
            self.metadata = temp_model.from_map(m['Metadata'])
        if m.get('Spec') is not None:
            temp_model = GetNodeResponseBodySpec()
            self.spec = temp_model.from_map(m['Spec'])
        if m.get('StatusInfo') is not None:
            temp_model = GetNodeResponseBodyStatusInfo()
            self.status_info = temp_model.from_map(m['StatusInfo'])
        return self


class GetNodeResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: GetNodeResponseBody

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
            temp_model = GetNodeResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetPipelineResponseBody(TeaModel):
    def __init__(self, request_id=None, pipeline_id=None, provider=None, identifier=None, version=None,
                 manifest=None, gmt_create_time=None, gmt_modified_time=None, uuid=None, workspace_id=None):
        # Id of the request
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        self.pipeline_id = TeaConverter.to_unicode(pipeline_id)  # type: unicode
        self.provider = TeaConverter.to_unicode(provider)  # type: unicode
        self.identifier = TeaConverter.to_unicode(identifier)  # type: unicode
        self.version = TeaConverter.to_unicode(version)  # type: unicode
        self.manifest = TeaConverter.to_unicode(manifest)  # type: unicode
        self.gmt_create_time = TeaConverter.to_unicode(gmt_create_time)  # type: unicode
        self.gmt_modified_time = TeaConverter.to_unicode(gmt_modified_time)  # type: unicode
        self.uuid = TeaConverter.to_unicode(uuid)  # type: unicode
        self.workspace_id = TeaConverter.to_unicode(workspace_id)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.pipeline_id is not None:
            result['PipelineId'] = self.pipeline_id
        if self.provider is not None:
            result['Provider'] = self.provider
        if self.identifier is not None:
            result['Identifier'] = self.identifier
        if self.version is not None:
            result['Version'] = self.version
        if self.manifest is not None:
            result['Manifest'] = self.manifest
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.uuid is not None:
            result['Uuid'] = self.uuid
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PipelineId') is not None:
            self.pipeline_id = m.get('PipelineId')
        if m.get('Provider') is not None:
            self.provider = m.get('Provider')
        if m.get('Identifier') is not None:
            self.identifier = m.get('Identifier')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        if m.get('Manifest') is not None:
            self.manifest = m.get('Manifest')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('Uuid') is not None:
            self.uuid = m.get('Uuid')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class GetPipelineResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: GetPipelineResponseBody

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
            temp_model = GetPipelineResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetPipelineSchemaResponseBody(TeaModel):
    def __init__(self, request_id=None, pipeline_id=None, provider=None, identifier=None, version=None,
                 manifest=None, gmt_create_time=None, gmt_modified_time=None, uuid=None, workspace_id=None):
        # Id of the request
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        self.pipeline_id = TeaConverter.to_unicode(pipeline_id)  # type: unicode
        self.provider = TeaConverter.to_unicode(provider)  # type: unicode
        self.identifier = TeaConverter.to_unicode(identifier)  # type: unicode
        self.version = TeaConverter.to_unicode(version)  # type: unicode
        self.manifest = TeaConverter.to_unicode(manifest)  # type: unicode
        self.gmt_create_time = TeaConverter.to_unicode(gmt_create_time)  # type: unicode
        self.gmt_modified_time = TeaConverter.to_unicode(gmt_modified_time)  # type: unicode
        self.uuid = TeaConverter.to_unicode(uuid)  # type: unicode
        self.workspace_id = TeaConverter.to_unicode(workspace_id)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.pipeline_id is not None:
            result['PipelineId'] = self.pipeline_id
        if self.provider is not None:
            result['Provider'] = self.provider
        if self.identifier is not None:
            result['Identifier'] = self.identifier
        if self.version is not None:
            result['Version'] = self.version
        if self.manifest is not None:
            result['Manifest'] = self.manifest
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.uuid is not None:
            result['Uuid'] = self.uuid
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PipelineId') is not None:
            self.pipeline_id = m.get('PipelineId')
        if m.get('Provider') is not None:
            self.provider = m.get('Provider')
        if m.get('Identifier') is not None:
            self.identifier = m.get('Identifier')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        if m.get('Manifest') is not None:
            self.manifest = m.get('Manifest')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('Uuid') is not None:
            self.uuid = m.get('Uuid')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class GetPipelineSchemaResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: GetPipelineSchemaResponseBody

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
            temp_model = GetPipelineSchemaResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetRunResponseBody(TeaModel):
    def __init__(self, request_id=None, pipeline_id=None, run_id=None, name=None, status=None, manifest=None,
                 arguments=None, user_id=None, parent_user_id=None, started_at=None, finished_at=None, node_id=None,
                 duration=None, workspace_id=None, message=None, source=None, experiment_id=None):
        # Id of the request
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        self.pipeline_id = TeaConverter.to_unicode(pipeline_id)  # type: unicode
        self.run_id = TeaConverter.to_unicode(run_id)  # type: unicode
        self.name = TeaConverter.to_unicode(name)  # type: unicode
        self.status = TeaConverter.to_unicode(status)  # type: unicode
        self.manifest = TeaConverter.to_unicode(manifest)  # type: unicode
        self.arguments = TeaConverter.to_unicode(arguments)  # type: unicode
        self.user_id = TeaConverter.to_unicode(user_id)  # type: unicode
        self.parent_user_id = TeaConverter.to_unicode(parent_user_id)  # type: unicode
        self.started_at = TeaConverter.to_unicode(started_at)  # type: unicode
        self.finished_at = TeaConverter.to_unicode(finished_at)  # type: unicode
        self.node_id = TeaConverter.to_unicode(node_id)  # type: unicode
        self.duration = duration  # type: long
        self.workspace_id = TeaConverter.to_unicode(workspace_id)  # type: unicode
        self.message = TeaConverter.to_unicode(message)  # type: unicode
        self.source = TeaConverter.to_unicode(source)  # type: unicode
        self.experiment_id = TeaConverter.to_unicode(experiment_id)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.pipeline_id is not None:
            result['PipelineId'] = self.pipeline_id
        if self.run_id is not None:
            result['RunId'] = self.run_id
        if self.name is not None:
            result['Name'] = self.name
        if self.status is not None:
            result['Status'] = self.status
        if self.manifest is not None:
            result['Manifest'] = self.manifest
        if self.arguments is not None:
            result['Arguments'] = self.arguments
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.parent_user_id is not None:
            result['ParentUserId'] = self.parent_user_id
        if self.started_at is not None:
            result['StartedAt'] = self.started_at
        if self.finished_at is not None:
            result['FinishedAt'] = self.finished_at
        if self.node_id is not None:
            result['NodeId'] = self.node_id
        if self.duration is not None:
            result['Duration'] = self.duration
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        if self.message is not None:
            result['Message'] = self.message
        if self.source is not None:
            result['Source'] = self.source
        if self.experiment_id is not None:
            result['ExperimentId'] = self.experiment_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PipelineId') is not None:
            self.pipeline_id = m.get('PipelineId')
        if m.get('RunId') is not None:
            self.run_id = m.get('RunId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('Manifest') is not None:
            self.manifest = m.get('Manifest')
        if m.get('Arguments') is not None:
            self.arguments = m.get('Arguments')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('ParentUserId') is not None:
            self.parent_user_id = m.get('ParentUserId')
        if m.get('StartedAt') is not None:
            self.started_at = m.get('StartedAt')
        if m.get('FinishedAt') is not None:
            self.finished_at = m.get('FinishedAt')
        if m.get('NodeId') is not None:
            self.node_id = m.get('NodeId')
        if m.get('Duration') is not None:
            self.duration = m.get('Duration')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('Source') is not None:
            self.source = m.get('Source')
        if m.get('ExperimentId') is not None:
            self.experiment_id = m.get('ExperimentId')
        return self


class GetRunResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: GetRunResponseBody

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
            temp_model = GetRunResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListNodeLogsRequest(TeaModel):
    def __init__(self, offset=None, page_size=None, from_time_in_seconds=None, keyword=None, reverse=None,
                 to_time_in_seconds=None):
        # 当前偏移量
        self.offset = offset  # type: int
        # 每页返回的log数目
        self.page_size = page_size  # type: int
        # 开始时间
        self.from_time_in_seconds = from_time_in_seconds  # type: long
        # 搜索词
        self.keyword = TeaConverter.to_unicode(keyword)  # type: unicode
        # 是否倒排
        self.reverse = reverse  # type: bool
        # 结束时间
        self.to_time_in_seconds = to_time_in_seconds  # type: long

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.offset is not None:
            result['Offset'] = self.offset
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.from_time_in_seconds is not None:
            result['FromTimeInSeconds'] = self.from_time_in_seconds
        if self.keyword is not None:
            result['Keyword'] = self.keyword
        if self.reverse is not None:
            result['Reverse'] = self.reverse
        if self.to_time_in_seconds is not None:
            result['ToTimeInSeconds'] = self.to_time_in_seconds
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Offset') is not None:
            self.offset = m.get('Offset')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('FromTimeInSeconds') is not None:
            self.from_time_in_seconds = m.get('FromTimeInSeconds')
        if m.get('Keyword') is not None:
            self.keyword = m.get('Keyword')
        if m.get('Reverse') is not None:
            self.reverse = m.get('Reverse')
        if m.get('ToTimeInSeconds') is not None:
            self.to_time_in_seconds = m.get('ToTimeInSeconds')
        return self


class ListNodeLogsResponseBody(TeaModel):
    def __init__(self, request_id=None, total_count=None, logs=None):
        # 请求 ID
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        # 符合过滤条件的作业数量
        self.total_count = total_count  # type: long
        # 日志列表
        self.logs = logs  # type: list[unicode]

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.logs is not None:
            result['Logs'] = self.logs
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('Logs') is not None:
            self.logs = m.get('Logs')
        return self


class ListNodeLogsResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: ListNodeLogsResponseBody

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
            temp_model = ListNodeLogsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListNodeOutputsRequest(TeaModel):
    def __init__(self, depth=None, name=None, page_number=None, page_size=None, sort_by=None, order=None, type=None):
        # 节点往下拿多少层子节点
        self.depth = depth  # type: int
        # 节点名字
        self.name = TeaConverter.to_unicode(name)  # type: unicode
        # 当前页，页码从1开始
        self.page_number = page_number  # type: int
        # 每页返回的输出数目
        self.page_size = page_size  # type: int
        # 排序字段
        self.sort_by = TeaConverter.to_unicode(sort_by)  # type: unicode
        # 排序顺序， 顺序：ASC，倒序：DESC
        self.order = TeaConverter.to_unicode(order)  # type: unicode
        # artifact 类型
        self.type = TeaConverter.to_unicode(type)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.depth is not None:
            result['Depth'] = self.depth
        if self.name is not None:
            result['Name'] = self.name
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.order is not None:
            result['Order'] = self.order
        if self.type is not None:
            result['Type'] = self.type
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Depth') is not None:
            self.depth = m.get('Depth')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        return self


class ListNodeOutputsResponseBodyOutputs(TeaModel):
    def __init__(self, name=None, type=None, gmt_create_time=None, id=None, node_id=None, value=None,
                 expanded_artifact_index=None, expandable_artifact_name=None, info=None, producer=None):
        # 名字
        self.name = TeaConverter.to_unicode(name)  # type: unicode
        # 类型
        self.type = TeaConverter.to_unicode(type)  # type: unicode
        # 创建时间
        self.gmt_create_time = TeaConverter.to_unicode(gmt_create_time)  # type: unicode
        self.id = TeaConverter.to_unicode(id)  # type: unicode
        # 输出所属节点 id
        self.node_id = TeaConverter.to_unicode(node_id)  # type: unicode
        # 输出内容
        self.value = TeaConverter.to_unicode(value)  # type: unicode
        # 被扩展artifact的索引号，以0开始
        self.expanded_artifact_index = expanded_artifact_index  # type: long
        # 可扩展artifact的名字
        self.expandable_artifact_name = TeaConverter.to_unicode(expandable_artifact_name)  # type: unicode
        # artifact内容
        self.info = info  # type: dict[unicode, any]
        # rtifact生产者
        self.producer = TeaConverter.to_unicode(producer)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.type is not None:
            result['Type'] = self.type
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.id is not None:
            result['Id'] = self.id
        if self.node_id is not None:
            result['NodeId'] = self.node_id
        if self.value is not None:
            result['Value'] = self.value
        if self.expanded_artifact_index is not None:
            result['ExpandedArtifactIndex'] = self.expanded_artifact_index
        if self.expandable_artifact_name is not None:
            result['ExpandableArtifactName'] = self.expandable_artifact_name
        if self.info is not None:
            result['Info'] = self.info
        if self.producer is not None:
            result['Producer'] = self.producer
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('NodeId') is not None:
            self.node_id = m.get('NodeId')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('ExpandedArtifactIndex') is not None:
            self.expanded_artifact_index = m.get('ExpandedArtifactIndex')
        if m.get('ExpandableArtifactName') is not None:
            self.expandable_artifact_name = m.get('ExpandableArtifactName')
        if m.get('Info') is not None:
            self.info = m.get('Info')
        if m.get('Producer') is not None:
            self.producer = m.get('Producer')
        return self


class ListNodeOutputsResponseBody(TeaModel):
    def __init__(self, request_id=None, total_count=None, outputs=None):
        # 请求ID
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        # 符合过滤条件的作业数量
        self.total_count = total_count  # type: long
        # 输出列表
        self.outputs = outputs  # type: list[ListNodeOutputsResponseBodyOutputs]

    def validate(self):
        if self.outputs:
            for k in self.outputs:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        result['Outputs'] = []
        if self.outputs is not None:
            for k in self.outputs:
                result['Outputs'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        self.outputs = []
        if m.get('Outputs') is not None:
            for k in m.get('Outputs'):
                temp_model = ListNodeOutputsResponseBodyOutputs()
                self.outputs.append(temp_model.from_map(k))
        return self


class ListNodeOutputsResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: ListNodeOutputsResponseBody

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
            temp_model = ListNodeOutputsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListPipelinePrivilegesResponseBody(TeaModel):
    def __init__(self, request_id=None, pipeline_id=None, users=None, actions=None):
        # Id of the request
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        self.pipeline_id = TeaConverter.to_unicode(pipeline_id)  # type: unicode
        # [ "*" ]
        self.users = users  # type: list[unicode]
        # [     "DescribeRun",     "PutRun",     "ListPipeline",     "GetPipeline"  ]
        self.actions = actions  # type: list[unicode]

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.pipeline_id is not None:
            result['PipelineId'] = self.pipeline_id
        if self.users is not None:
            result['Users'] = self.users
        if self.actions is not None:
            result['Actions'] = self.actions
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PipelineId') is not None:
            self.pipeline_id = m.get('PipelineId')
        if m.get('Users') is not None:
            self.users = m.get('Users')
        if m.get('Actions') is not None:
            self.actions = m.get('Actions')
        return self


class ListPipelinePrivilegesResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: ListPipelinePrivilegesResponseBody

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
            temp_model = ListPipelinePrivilegesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListPipelinesRequest(TeaModel):
    def __init__(self, page_number=None, page_size=None, pipeline_identifier=None, pipeline_provider=None,
                 pipeline_version=None, workspace_id=None):
        self.page_number = page_number  # type: int
        self.page_size = page_size  # type: int
        self.pipeline_identifier = TeaConverter.to_unicode(pipeline_identifier)  # type: unicode
        self.pipeline_provider = TeaConverter.to_unicode(pipeline_provider)  # type: unicode
        self.pipeline_version = TeaConverter.to_unicode(pipeline_version)  # type: unicode
        self.workspace_id = TeaConverter.to_unicode(workspace_id)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.pipeline_identifier is not None:
            result['PipelineIdentifier'] = self.pipeline_identifier
        if self.pipeline_provider is not None:
            result['PipelineProvider'] = self.pipeline_provider
        if self.pipeline_version is not None:
            result['PipelineVersion'] = self.pipeline_version
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('PipelineIdentifier') is not None:
            self.pipeline_identifier = m.get('PipelineIdentifier')
        if m.get('PipelineProvider') is not None:
            self.pipeline_provider = m.get('PipelineProvider')
        if m.get('PipelineVersion') is not None:
            self.pipeline_version = m.get('PipelineVersion')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class ListPipelinesResponseBodyPipelines(TeaModel):
    def __init__(self, pipeline_id=None, gmt_create_time=None, gmt_modified_time=None, provider=None,
                 identifier=None, version=None, uuid=None, workspace_id=None):
        self.pipeline_id = TeaConverter.to_unicode(pipeline_id)  # type: unicode
        self.gmt_create_time = TeaConverter.to_unicode(gmt_create_time)  # type: unicode
        self.gmt_modified_time = TeaConverter.to_unicode(gmt_modified_time)  # type: unicode
        self.provider = TeaConverter.to_unicode(provider)  # type: unicode
        self.identifier = TeaConverter.to_unicode(identifier)  # type: unicode
        self.version = TeaConverter.to_unicode(version)  # type: unicode
        self.uuid = TeaConverter.to_unicode(uuid)  # type: unicode
        self.workspace_id = TeaConverter.to_unicode(workspace_id)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.pipeline_id is not None:
            result['PipelineId'] = self.pipeline_id
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.provider is not None:
            result['Provider'] = self.provider
        if self.identifier is not None:
            result['Identifier'] = self.identifier
        if self.version is not None:
            result['Version'] = self.version
        if self.uuid is not None:
            result['Uuid'] = self.uuid
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('PipelineId') is not None:
            self.pipeline_id = m.get('PipelineId')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('Provider') is not None:
            self.provider = m.get('Provider')
        if m.get('Identifier') is not None:
            self.identifier = m.get('Identifier')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        if m.get('Uuid') is not None:
            self.uuid = m.get('Uuid')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class ListPipelinesResponseBody(TeaModel):
    def __init__(self, request_id=None, pipelines=None, total_count=None):
        # Id of the request
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        self.pipelines = pipelines  # type: list[ListPipelinesResponseBodyPipelines]
        self.total_count = total_count  # type: long

    def validate(self):
        if self.pipelines:
            for k in self.pipelines:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Pipelines'] = []
        if self.pipelines is not None:
            for k in self.pipelines:
                result['Pipelines'].append(k.to_map() if k else None)
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.pipelines = []
        if m.get('Pipelines') is not None:
            for k in m.get('Pipelines'):
                temp_model = ListPipelinesResponseBodyPipelines()
                self.pipelines.append(temp_model.from_map(k))
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListPipelinesResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: ListPipelinesResponseBody

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
            temp_model = ListPipelinesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListRunsRequest(TeaModel):
    def __init__(self, page_number=None, page_size=None, experiment_id=None, name=None, pipeline_id=None,
                 run_id=None, sort_by=None, order=None, source=None, status=None, workspace_id=None):
        self.page_number = page_number  # type: int
        self.page_size = page_size  # type: int
        self.experiment_id = TeaConverter.to_unicode(experiment_id)  # type: unicode
        self.name = TeaConverter.to_unicode(name)  # type: unicode
        self.pipeline_id = TeaConverter.to_unicode(pipeline_id)  # type: unicode
        self.run_id = TeaConverter.to_unicode(run_id)  # type: unicode
        self.sort_by = TeaConverter.to_unicode(sort_by)  # type: unicode
        self.order = TeaConverter.to_unicode(order)  # type: unicode
        self.source = TeaConverter.to_unicode(source)  # type: unicode
        self.status = TeaConverter.to_unicode(status)  # type: unicode
        self.workspace_id = TeaConverter.to_unicode(workspace_id)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.experiment_id is not None:
            result['ExperimentId'] = self.experiment_id
        if self.name is not None:
            result['Name'] = self.name
        if self.pipeline_id is not None:
            result['PipelineId'] = self.pipeline_id
        if self.run_id is not None:
            result['RunId'] = self.run_id
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.order is not None:
            result['Order'] = self.order
        if self.source is not None:
            result['Source'] = self.source
        if self.status is not None:
            result['Status'] = self.status
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('ExperimentId') is not None:
            self.experiment_id = m.get('ExperimentId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('PipelineId') is not None:
            self.pipeline_id = m.get('PipelineId')
        if m.get('RunId') is not None:
            self.run_id = m.get('RunId')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('Source') is not None:
            self.source = m.get('Source')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class ListRunsResponseBodyRuns(TeaModel):
    def __init__(self, run_id=None, name=None, status=None, user_id=None, parent_user_id=None, started_at=None,
                 finished_at=None, node_id=None, duration=None, workspace_id=None, message=None, source=None, experiment_id=None):
        self.run_id = TeaConverter.to_unicode(run_id)  # type: unicode
        self.name = TeaConverter.to_unicode(name)  # type: unicode
        self.status = TeaConverter.to_unicode(status)  # type: unicode
        self.user_id = TeaConverter.to_unicode(user_id)  # type: unicode
        self.parent_user_id = TeaConverter.to_unicode(parent_user_id)  # type: unicode
        self.started_at = TeaConverter.to_unicode(started_at)  # type: unicode
        self.finished_at = TeaConverter.to_unicode(finished_at)  # type: unicode
        self.node_id = TeaConverter.to_unicode(node_id)  # type: unicode
        self.duration = duration  # type: long
        self.workspace_id = TeaConverter.to_unicode(workspace_id)  # type: unicode
        self.message = TeaConverter.to_unicode(message)  # type: unicode
        self.source = TeaConverter.to_unicode(source)  # type: unicode
        self.experiment_id = TeaConverter.to_unicode(experiment_id)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.run_id is not None:
            result['RunId'] = self.run_id
        if self.name is not None:
            result['Name'] = self.name
        if self.status is not None:
            result['Status'] = self.status
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.parent_user_id is not None:
            result['ParentUserId'] = self.parent_user_id
        if self.started_at is not None:
            result['StartedAt'] = self.started_at
        if self.finished_at is not None:
            result['FinishedAt'] = self.finished_at
        if self.node_id is not None:
            result['NodeId'] = self.node_id
        if self.duration is not None:
            result['Duration'] = self.duration
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        if self.message is not None:
            result['Message'] = self.message
        if self.source is not None:
            result['Source'] = self.source
        if self.experiment_id is not None:
            result['ExperimentId'] = self.experiment_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RunId') is not None:
            self.run_id = m.get('RunId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('ParentUserId') is not None:
            self.parent_user_id = m.get('ParentUserId')
        if m.get('StartedAt') is not None:
            self.started_at = m.get('StartedAt')
        if m.get('FinishedAt') is not None:
            self.finished_at = m.get('FinishedAt')
        if m.get('NodeId') is not None:
            self.node_id = m.get('NodeId')
        if m.get('Duration') is not None:
            self.duration = m.get('Duration')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('Source') is not None:
            self.source = m.get('Source')
        if m.get('ExperimentId') is not None:
            self.experiment_id = m.get('ExperimentId')
        return self


class ListRunsResponseBody(TeaModel):
    def __init__(self, request_id=None, runs=None, total_count=None):
        # Id of the request
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        self.runs = runs  # type: list[ListRunsResponseBodyRuns]
        self.total_count = total_count  # type: long

    def validate(self):
        if self.runs:
            for k in self.runs:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Runs'] = []
        if self.runs is not None:
            for k in self.runs:
                result['Runs'].append(k.to_map() if k else None)
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.runs = []
        if m.get('Runs') is not None:
            for k in m.get('Runs'):
                temp_model = ListRunsResponseBodyRuns()
                self.runs.append(temp_model.from_map(k))
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListRunsResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: ListRunsResponseBody

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
            temp_model = ListRunsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListRunsStatusRequestNodeInfos(TeaModel):
    def __init__(self, run_id=None, node_id=None):
        self.run_id = TeaConverter.to_unicode(run_id)  # type: unicode
        self.node_id = TeaConverter.to_unicode(node_id)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.run_id is not None:
            result['RunId'] = self.run_id
        if self.node_id is not None:
            result['NodeId'] = self.node_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RunId') is not None:
            self.run_id = m.get('RunId')
        if m.get('NodeId') is not None:
            self.node_id = m.get('NodeId')
        return self


class ListRunsStatusRequest(TeaModel):
    def __init__(self, run_ids=None, node_infos=None):
        self.run_ids = run_ids  # type: list[unicode]
        self.node_infos = node_infos  # type: list[ListRunsStatusRequestNodeInfos]

    def validate(self):
        if self.node_infos:
            for k in self.node_infos:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.run_ids is not None:
            result['RunIds'] = self.run_ids
        result['NodeInfos'] = []
        if self.node_infos is not None:
            for k in self.node_infos:
                result['NodeInfos'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RunIds') is not None:
            self.run_ids = m.get('RunIds')
        self.node_infos = []
        if m.get('NodeInfos') is not None:
            for k in m.get('NodeInfos'):
                temp_model = ListRunsStatusRequestNodeInfos()
                self.node_infos.append(temp_model.from_map(k))
        return self


class ListRunsStatusResponseBodyRunsInfos(TeaModel):
    def __init__(self, run_id=None, status=None):
        self.run_id = TeaConverter.to_unicode(run_id)  # type: unicode
        self.status = TeaConverter.to_unicode(status)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.run_id is not None:
            result['RunId'] = self.run_id
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RunId') is not None:
            self.run_id = m.get('RunId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class ListRunsStatusResponseBodyNodeInfos(TeaModel):
    def __init__(self, run_id=None, node_id=None, status=None, input_artifact_archived=None,
                 output_artifact_archived=None):
        self.run_id = TeaConverter.to_unicode(run_id)  # type: unicode
        self.node_id = TeaConverter.to_unicode(node_id)  # type: unicode
        self.status = TeaConverter.to_unicode(status)  # type: unicode
        self.input_artifact_archived = input_artifact_archived  # type: bool
        self.output_artifact_archived = output_artifact_archived  # type: bool

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.run_id is not None:
            result['RunId'] = self.run_id
        if self.node_id is not None:
            result['NodeId'] = self.node_id
        if self.status is not None:
            result['Status'] = self.status
        if self.input_artifact_archived is not None:
            result['InputArtifactArchived'] = self.input_artifact_archived
        if self.output_artifact_archived is not None:
            result['OutputArtifactArchived'] = self.output_artifact_archived
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RunId') is not None:
            self.run_id = m.get('RunId')
        if m.get('NodeId') is not None:
            self.node_id = m.get('NodeId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('InputArtifactArchived') is not None:
            self.input_artifact_archived = m.get('InputArtifactArchived')
        if m.get('OutputArtifactArchived') is not None:
            self.output_artifact_archived = m.get('OutputArtifactArchived')
        return self


class ListRunsStatusResponseBody(TeaModel):
    def __init__(self, request_id=None, runs_infos=None, node_infos=None):
        # Id of the request
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode
        self.runs_infos = runs_infos  # type: list[ListRunsStatusResponseBodyRunsInfos]
        self.node_infos = node_infos  # type: list[ListRunsStatusResponseBodyNodeInfos]

    def validate(self):
        if self.runs_infos:
            for k in self.runs_infos:
                if k:
                    k.validate()
        if self.node_infos:
            for k in self.node_infos:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['RunsInfos'] = []
        if self.runs_infos is not None:
            for k in self.runs_infos:
                result['RunsInfos'].append(k.to_map() if k else None)
        result['NodeInfos'] = []
        if self.node_infos is not None:
            for k in self.node_infos:
                result['NodeInfos'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.runs_infos = []
        if m.get('RunsInfos') is not None:
            for k in m.get('RunsInfos'):
                temp_model = ListRunsStatusResponseBodyRunsInfos()
                self.runs_infos.append(temp_model.from_map(k))
        self.node_infos = []
        if m.get('NodeInfos') is not None:
            for k in m.get('NodeInfos'):
                temp_model = ListRunsStatusResponseBodyNodeInfos()
                self.node_infos.append(temp_model.from_map(k))
        return self


class ListRunsStatusResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: ListRunsStatusResponseBody

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
            temp_model = ListRunsStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StartRunResponseBody(TeaModel):
    def __init__(self, request_id=None):
        # Id of the request
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


class StartRunResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: StartRunResponseBody

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
            temp_model = StartRunResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class TerminateRunResponseBody(TeaModel):
    def __init__(self, request_id=None):
        # Id of the request
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


class TerminateRunResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: TerminateRunResponseBody

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
            temp_model = TerminateRunResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdatePipelineRequest(TeaModel):
    def __init__(self, manifest=None):
        self.manifest = TeaConverter.to_unicode(manifest)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.manifest is not None:
            result['Manifest'] = self.manifest
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Manifest') is not None:
            self.manifest = m.get('Manifest')
        return self


class UpdatePipelineResponseBody(TeaModel):
    def __init__(self, request_id=None):
        # Id of the request
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


class UpdatePipelineResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: UpdatePipelineResponseBody

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
            temp_model = UpdatePipelineResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdatePipelinePrivilegesRequest(TeaModel):
    def __init__(self, users=None):
        self.users = users  # type: list[unicode]

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.users is not None:
            result['Users'] = self.users
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Users') is not None:
            self.users = m.get('Users')
        return self


class UpdatePipelinePrivilegesResponseBody(TeaModel):
    def __init__(self, request_id=None):
        # Id of the request
        self.request_id = TeaConverter.to_unicode(request_id)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class UpdatePipelinePrivilegesResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: UpdatePipelinePrivilegesResponseBody

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
            temp_model = UpdatePipelinePrivilegesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateRunRequest(TeaModel):
    def __init__(self, name=None):
        self.name = TeaConverter.to_unicode(name)  # type: unicode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class UpdateRunResponseBody(TeaModel):
    def __init__(self, request_id=None):
        # Id of the request
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


class UpdateRunResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers  # type: dict[unicode, unicode]
        self.body = body  # type: UpdateRunResponseBody

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
            temp_model = UpdateRunResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


