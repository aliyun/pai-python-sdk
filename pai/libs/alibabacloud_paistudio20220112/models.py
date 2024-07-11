# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel
from typing import List, Dict, Any


class ACS(TeaModel):
    def __init__(
        self,
        acsquota_id: str = None,
        associated_products: List[str] = None,
    ):
        self.acsquota_id = acsquota_id
        self.associated_products = associated_products

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.acsquota_id is not None:
            result['ACSQuotaId'] = self.acsquota_id
        if self.associated_products is not None:
            result['AssociatedProducts'] = self.associated_products
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ACSQuotaId') is not None:
            self.acsquota_id = m.get('ACSQuotaId')
        if m.get('AssociatedProducts') is not None:
            self.associated_products = m.get('AssociatedProducts')
        return self


class AlgorithmSpecComputeResourcePolicy(TeaModel):
    def __init__(
        self,
        value: str = None,
        version: str = None,
    ):
        # This parameter is required.
        self.value = value
        # This parameter is required.
        self.version = version

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.value is not None:
            result['Value'] = self.value
        if self.version is not None:
            result['Version'] = self.version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        return self


class AlgorithmSpecComputeResource(TeaModel):
    def __init__(
        self,
        policy: AlgorithmSpecComputeResourcePolicy = None,
    ):
        # This parameter is required.
        self.policy = policy

    def validate(self):
        if self.policy:
            self.policy.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.policy is not None:
            result['Policy'] = self.policy.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Policy') is not None:
            temp_model = AlgorithmSpecComputeResourcePolicy()
            self.policy = temp_model.from_map(m['Policy'])
        return self


class AlgorithmSpecCustomization(TeaModel):
    def __init__(
        self,
        code_dir: bool = None,
    ):
        self.code_dir = code_dir

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code_dir is not None:
            result['CodeDir'] = self.code_dir
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CodeDir') is not None:
            self.code_dir = m.get('CodeDir')
        return self


class AlgorithmSpecProgressDefinitionsOverallProgress(TeaModel):
    def __init__(
        self,
        description: str = None,
        regex: str = None,
    ):
        self.description = description
        self.regex = regex

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.description is not None:
            result['Description'] = self.description
        if self.regex is not None:
            result['Regex'] = self.regex
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Regex') is not None:
            self.regex = m.get('Regex')
        return self


class AlgorithmSpecProgressDefinitionsRemainingTime(TeaModel):
    def __init__(
        self,
        description: str = None,
        regex: str = None,
    ):
        self.description = description
        self.regex = regex

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.description is not None:
            result['Description'] = self.description
        if self.regex is not None:
            result['Regex'] = self.regex
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Regex') is not None:
            self.regex = m.get('Regex')
        return self


class AlgorithmSpecProgressDefinitions(TeaModel):
    def __init__(
        self,
        overall_progress: AlgorithmSpecProgressDefinitionsOverallProgress = None,
        remaining_time: AlgorithmSpecProgressDefinitionsRemainingTime = None,
    ):
        self.overall_progress = overall_progress
        self.remaining_time = remaining_time

    def validate(self):
        if self.overall_progress:
            self.overall_progress.validate()
        if self.remaining_time:
            self.remaining_time.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.overall_progress is not None:
            result['OverallProgress'] = self.overall_progress.to_map()
        if self.remaining_time is not None:
            result['RemainingTime'] = self.remaining_time.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('OverallProgress') is not None:
            temp_model = AlgorithmSpecProgressDefinitionsOverallProgress()
            self.overall_progress = temp_model.from_map(m['OverallProgress'])
        if m.get('RemainingTime') is not None:
            temp_model = AlgorithmSpecProgressDefinitionsRemainingTime()
            self.remaining_time = temp_model.from_map(m['RemainingTime'])
        return self


class Location(TeaModel):
    def __init__(
        self,
        location_type: str = None,
        location_value: Dict[str, Any] = None,
    ):
        self.location_type = location_type
        self.location_value = location_value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.location_type is not None:
            result['LocationType'] = self.location_type
        if self.location_value is not None:
            result['LocationValue'] = self.location_value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LocationType') is not None:
            self.location_type = m.get('LocationType')
        if m.get('LocationValue') is not None:
            self.location_value = m.get('LocationValue')
        return self


class HyperParameterRange(TeaModel):
    def __init__(
        self,
        enum: List[str] = None,
        exclusive_maximum: bool = None,
        exclusive_minimum: bool = None,
        max_length: int = None,
        maximum: str = None,
        min_length: int = None,
        minimum: str = None,
        pattern: str = None,
    ):
        self.enum = enum
        self.exclusive_maximum = exclusive_maximum
        self.exclusive_minimum = exclusive_minimum
        self.max_length = max_length
        self.maximum = maximum
        self.min_length = min_length
        self.minimum = minimum
        self.pattern = pattern

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.enum is not None:
            result['Enum'] = self.enum
        if self.exclusive_maximum is not None:
            result['ExclusiveMaximum'] = self.exclusive_maximum
        if self.exclusive_minimum is not None:
            result['ExclusiveMinimum'] = self.exclusive_minimum
        if self.max_length is not None:
            result['MaxLength'] = self.max_length
        if self.maximum is not None:
            result['Maximum'] = self.maximum
        if self.min_length is not None:
            result['MinLength'] = self.min_length
        if self.minimum is not None:
            result['Minimum'] = self.minimum
        if self.pattern is not None:
            result['Pattern'] = self.pattern
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Enum') is not None:
            self.enum = m.get('Enum')
        if m.get('ExclusiveMaximum') is not None:
            self.exclusive_maximum = m.get('ExclusiveMaximum')
        if m.get('ExclusiveMinimum') is not None:
            self.exclusive_minimum = m.get('ExclusiveMinimum')
        if m.get('MaxLength') is not None:
            self.max_length = m.get('MaxLength')
        if m.get('Maximum') is not None:
            self.maximum = m.get('Maximum')
        if m.get('MinLength') is not None:
            self.min_length = m.get('MinLength')
        if m.get('Minimum') is not None:
            self.minimum = m.get('Minimum')
        if m.get('Pattern') is not None:
            self.pattern = m.get('Pattern')
        return self


class HyperParameterDefinition(TeaModel):
    def __init__(
        self,
        default_value: str = None,
        description: str = None,
        display_name: str = None,
        name: str = None,
        range: HyperParameterRange = None,
        required: bool = None,
        type: str = None,
    ):
        self.default_value = default_value
        self.description = description
        self.display_name = display_name
        # This parameter is required.
        self.name = name
        self.range = range
        self.required = required
        # This parameter is required.
        self.type = type

    def validate(self):
        if self.range:
            self.range.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.default_value is not None:
            result['DefaultValue'] = self.default_value
        if self.description is not None:
            result['Description'] = self.description
        if self.display_name is not None:
            result['DisplayName'] = self.display_name
        if self.name is not None:
            result['Name'] = self.name
        if self.range is not None:
            result['Range'] = self.range.to_map()
        if self.required is not None:
            result['Required'] = self.required
        if self.type is not None:
            result['Type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DefaultValue') is not None:
            self.default_value = m.get('DefaultValue')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('DisplayName') is not None:
            self.display_name = m.get('DisplayName')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Range') is not None:
            temp_model = HyperParameterRange()
            self.range = temp_model.from_map(m['Range'])
        if m.get('Required') is not None:
            self.required = m.get('Required')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        return self


class Channel(TeaModel):
    def __init__(
        self,
        description: str = None,
        name: str = None,
        properties: Dict[str, Any] = None,
        required: bool = None,
        supported_channel_types: List[str] = None,
    ):
        self.description = description
        # This parameter is required.
        self.name = name
        self.properties = properties
        self.required = required
        self.supported_channel_types = supported_channel_types

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.description is not None:
            result['Description'] = self.description
        if self.name is not None:
            result['Name'] = self.name
        if self.properties is not None:
            result['Properties'] = self.properties
        if self.required is not None:
            result['Required'] = self.required
        if self.supported_channel_types is not None:
            result['SupportedChannelTypes'] = self.supported_channel_types
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Properties') is not None:
            self.properties = m.get('Properties')
        if m.get('Required') is not None:
            self.required = m.get('Required')
        if m.get('SupportedChannelTypes') is not None:
            self.supported_channel_types = m.get('SupportedChannelTypes')
        return self


class MetricDefinition(TeaModel):
    def __init__(
        self,
        description: str = None,
        name: str = None,
        regex: str = None,
    ):
        self.description = description
        # This parameter is required.
        self.name = name
        # This parameter is required.
        self.regex = regex

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.description is not None:
            result['Description'] = self.description
        if self.name is not None:
            result['Name'] = self.name
        if self.regex is not None:
            result['Regex'] = self.regex
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Regex') is not None:
            self.regex = m.get('Regex')
        return self


class ConditionExpression(TeaModel):
    def __init__(
        self,
        key: str = None,
        operator: str = None,
        values: List[str] = None,
    ):
        # This parameter is required.
        self.key = key
        # This parameter is required.
        self.operator = operator
        # This parameter is required.
        self.values = values

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.operator is not None:
            result['Operator'] = self.operator
        if self.values is not None:
            result['Values'] = self.values
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Operator') is not None:
            self.operator = m.get('Operator')
        if m.get('Values') is not None:
            self.values = m.get('Values')
        return self


class AlgorithmSpec(TeaModel):
    def __init__(
        self,
        code_dir: Location = None,
        command: List[str] = None,
        compute_resource: AlgorithmSpecComputeResource = None,
        customization: AlgorithmSpecCustomization = None,
        hyper_parameters: List[HyperParameterDefinition] = None,
        image: str = None,
        input_channels: List[Channel] = None,
        job_type: str = None,
        metric_definitions: List[MetricDefinition] = None,
        output_channels: List[Channel] = None,
        progress_definitions: AlgorithmSpecProgressDefinitions = None,
        resource_requirements: List[ConditionExpression] = None,
        supported_instance_types: List[str] = None,
        supports_distributed_training: bool = None,
    ):
        self.code_dir = code_dir
        # This parameter is required.
        self.command = command
        self.compute_resource = compute_resource
        self.customization = customization
        self.hyper_parameters = hyper_parameters
        # This parameter is required.
        self.image = image
        self.input_channels = input_channels
        # This parameter is required.
        self.job_type = job_type
        self.metric_definitions = metric_definitions
        self.output_channels = output_channels
        self.progress_definitions = progress_definitions
        self.resource_requirements = resource_requirements
        self.supported_instance_types = supported_instance_types
        self.supports_distributed_training = supports_distributed_training

    def validate(self):
        if self.code_dir:
            self.code_dir.validate()
        if self.compute_resource:
            self.compute_resource.validate()
        if self.customization:
            self.customization.validate()
        if self.hyper_parameters:
            for k in self.hyper_parameters:
                if k:
                    k.validate()
        if self.input_channels:
            for k in self.input_channels:
                if k:
                    k.validate()
        if self.metric_definitions:
            for k in self.metric_definitions:
                if k:
                    k.validate()
        if self.output_channels:
            for k in self.output_channels:
                if k:
                    k.validate()
        if self.progress_definitions:
            self.progress_definitions.validate()
        if self.resource_requirements:
            for k in self.resource_requirements:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code_dir is not None:
            result['CodeDir'] = self.code_dir.to_map()
        if self.command is not None:
            result['Command'] = self.command
        if self.compute_resource is not None:
            result['ComputeResource'] = self.compute_resource.to_map()
        if self.customization is not None:
            result['Customization'] = self.customization.to_map()
        result['HyperParameters'] = []
        if self.hyper_parameters is not None:
            for k in self.hyper_parameters:
                result['HyperParameters'].append(k.to_map() if k else None)
        if self.image is not None:
            result['Image'] = self.image
        result['InputChannels'] = []
        if self.input_channels is not None:
            for k in self.input_channels:
                result['InputChannels'].append(k.to_map() if k else None)
        if self.job_type is not None:
            result['JobType'] = self.job_type
        result['MetricDefinitions'] = []
        if self.metric_definitions is not None:
            for k in self.metric_definitions:
                result['MetricDefinitions'].append(k.to_map() if k else None)
        result['OutputChannels'] = []
        if self.output_channels is not None:
            for k in self.output_channels:
                result['OutputChannels'].append(k.to_map() if k else None)
        if self.progress_definitions is not None:
            result['ProgressDefinitions'] = self.progress_definitions.to_map()
        result['ResourceRequirements'] = []
        if self.resource_requirements is not None:
            for k in self.resource_requirements:
                result['ResourceRequirements'].append(k.to_map() if k else None)
        if self.supported_instance_types is not None:
            result['SupportedInstanceTypes'] = self.supported_instance_types
        if self.supports_distributed_training is not None:
            result['SupportsDistributedTraining'] = self.supports_distributed_training
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CodeDir') is not None:
            temp_model = Location()
            self.code_dir = temp_model.from_map(m['CodeDir'])
        if m.get('Command') is not None:
            self.command = m.get('Command')
        if m.get('ComputeResource') is not None:
            temp_model = AlgorithmSpecComputeResource()
            self.compute_resource = temp_model.from_map(m['ComputeResource'])
        if m.get('Customization') is not None:
            temp_model = AlgorithmSpecCustomization()
            self.customization = temp_model.from_map(m['Customization'])
        self.hyper_parameters = []
        if m.get('HyperParameters') is not None:
            for k in m.get('HyperParameters'):
                temp_model = HyperParameterDefinition()
                self.hyper_parameters.append(temp_model.from_map(k))
        if m.get('Image') is not None:
            self.image = m.get('Image')
        self.input_channels = []
        if m.get('InputChannels') is not None:
            for k in m.get('InputChannels'):
                temp_model = Channel()
                self.input_channels.append(temp_model.from_map(k))
        if m.get('JobType') is not None:
            self.job_type = m.get('JobType')
        self.metric_definitions = []
        if m.get('MetricDefinitions') is not None:
            for k in m.get('MetricDefinitions'):
                temp_model = MetricDefinition()
                self.metric_definitions.append(temp_model.from_map(k))
        self.output_channels = []
        if m.get('OutputChannels') is not None:
            for k in m.get('OutputChannels'):
                temp_model = Channel()
                self.output_channels.append(temp_model.from_map(k))
        if m.get('ProgressDefinitions') is not None:
            temp_model = AlgorithmSpecProgressDefinitions()
            self.progress_definitions = temp_model.from_map(m['ProgressDefinitions'])
        self.resource_requirements = []
        if m.get('ResourceRequirements') is not None:
            for k in m.get('ResourceRequirements'):
                temp_model = ConditionExpression()
                self.resource_requirements.append(temp_model.from_map(k))
        if m.get('SupportedInstanceTypes') is not None:
            self.supported_instance_types = m.get('SupportedInstanceTypes')
        if m.get('SupportsDistributedTraining') is not None:
            self.supports_distributed_training = m.get('SupportsDistributedTraining')
        return self


class NodeSpec(TeaModel):
    def __init__(
        self,
        count: int = None,
        type: str = None,
    ):
        self.count = count
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.count is not None:
            result['Count'] = self.count
        if self.type is not None:
            result['Type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Count') is not None:
            self.count = m.get('Count')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        return self


class AllocateStrategySpec(TeaModel):
    def __init__(
        self,
        node_specs: List[NodeSpec] = None,
    ):
        self.node_specs = node_specs

    def validate(self):
        if self.node_specs:
            for k in self.node_specs:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['NodeSpecs'] = []
        if self.node_specs is not None:
            for k in self.node_specs:
                result['NodeSpecs'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.node_specs = []
        if m.get('NodeSpecs') is not None:
            for k in m.get('NodeSpecs'):
                temp_model = NodeSpec()
                self.node_specs.append(temp_model.from_map(k))
        return self


class ChannelProperty(TeaModel):
    def __init__(
        self,
        name: str = None,
        value: str = None,
    ):
        # This parameter is required.
        self.name = name
        # This parameter is required.
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class ComponentSpec(TeaModel):
    def __init__(
        self,
        code_dir: Location = None,
        command: str = None,
        hyper_parameters: List[HyperParameterDefinition] = None,
        image: str = None,
        input_channels: List[Channel] = None,
        job_type: str = None,
        metric_definitions: List[MetricDefinition] = None,
        output_channels: List[Channel] = None,
        resource_requirements: List[ConditionExpression] = None,
    ):
        self.code_dir = code_dir
        # This parameter is required.
        self.command = command
        self.hyper_parameters = hyper_parameters
        # This parameter is required.
        self.image = image
        self.input_channels = input_channels
        # This parameter is required.
        self.job_type = job_type
        self.metric_definitions = metric_definitions
        self.output_channels = output_channels
        self.resource_requirements = resource_requirements

    def validate(self):
        if self.code_dir:
            self.code_dir.validate()
        if self.hyper_parameters:
            for k in self.hyper_parameters:
                if k:
                    k.validate()
        if self.input_channels:
            for k in self.input_channels:
                if k:
                    k.validate()
        if self.metric_definitions:
            for k in self.metric_definitions:
                if k:
                    k.validate()
        if self.output_channels:
            for k in self.output_channels:
                if k:
                    k.validate()
        if self.resource_requirements:
            for k in self.resource_requirements:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code_dir is not None:
            result['CodeDir'] = self.code_dir.to_map()
        if self.command is not None:
            result['Command'] = self.command
        result['HyperParameters'] = []
        if self.hyper_parameters is not None:
            for k in self.hyper_parameters:
                result['HyperParameters'].append(k.to_map() if k else None)
        if self.image is not None:
            result['Image'] = self.image
        result['InputChannels'] = []
        if self.input_channels is not None:
            for k in self.input_channels:
                result['InputChannels'].append(k.to_map() if k else None)
        if self.job_type is not None:
            result['JobType'] = self.job_type
        result['MetricDefinitions'] = []
        if self.metric_definitions is not None:
            for k in self.metric_definitions:
                result['MetricDefinitions'].append(k.to_map() if k else None)
        result['OutputChannels'] = []
        if self.output_channels is not None:
            for k in self.output_channels:
                result['OutputChannels'].append(k.to_map() if k else None)
        result['ResourceRequirements'] = []
        if self.resource_requirements is not None:
            for k in self.resource_requirements:
                result['ResourceRequirements'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CodeDir') is not None:
            temp_model = Location()
            self.code_dir = temp_model.from_map(m['CodeDir'])
        if m.get('Command') is not None:
            self.command = m.get('Command')
        self.hyper_parameters = []
        if m.get('HyperParameters') is not None:
            for k in m.get('HyperParameters'):
                temp_model = HyperParameterDefinition()
                self.hyper_parameters.append(temp_model.from_map(k))
        if m.get('Image') is not None:
            self.image = m.get('Image')
        self.input_channels = []
        if m.get('InputChannels') is not None:
            for k in m.get('InputChannels'):
                temp_model = Channel()
                self.input_channels.append(temp_model.from_map(k))
        if m.get('JobType') is not None:
            self.job_type = m.get('JobType')
        self.metric_definitions = []
        if m.get('MetricDefinitions') is not None:
            for k in m.get('MetricDefinitions'):
                temp_model = MetricDefinition()
                self.metric_definitions.append(temp_model.from_map(k))
        self.output_channels = []
        if m.get('OutputChannels') is not None:
            for k in m.get('OutputChannels'):
                temp_model = Channel()
                self.output_channels.append(temp_model.from_map(k))
        self.resource_requirements = []
        if m.get('ResourceRequirements') is not None:
            for k in m.get('ResourceRequirements'):
                temp_model = ConditionExpression()
                self.resource_requirements.append(temp_model.from_map(k))
        return self


class FeaturesQuota(TeaModel):
    def __init__(
        self,
        is_enabled: bool = None,
    ):
        self.is_enabled = is_enabled

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.is_enabled is not None:
            result['IsEnabled'] = self.is_enabled
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('IsEnabled') is not None:
            self.is_enabled = m.get('IsEnabled')
        return self


class Features(TeaModel):
    def __init__(
        self,
        quota: FeaturesQuota = None,
    ):
        self.quota = quota

    def validate(self):
        if self.quota:
            self.quota.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.quota is not None:
            result['Quota'] = self.quota.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Quota') is not None:
            temp_model = FeaturesQuota()
            self.quota = temp_model.from_map(m['Quota'])
        return self


class GPUInfo(TeaModel):
    def __init__(
        self,
        count: int = None,
        type: str = None,
    ):
        self.count = count
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.count is not None:
            result['count'] = self.count
        if self.type is not None:
            result['type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('count') is not None:
            self.count = m.get('count')
        if m.get('type') is not None:
            self.type = m.get('type')
        return self


class GPUMetric(TeaModel):
    def __init__(
        self,
        index: int = None,
        model: str = None,
        status: int = None,
        usage_rate: float = None,
    ):
        self.index = index
        self.model = model
        self.status = status
        self.usage_rate = usage_rate

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.index is not None:
            result['Index'] = self.index
        if self.model is not None:
            result['Model'] = self.model
        if self.status is not None:
            result['Status'] = self.status
        if self.usage_rate is not None:
            result['UsageRate'] = self.usage_rate
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Index') is not None:
            self.index = m.get('Index')
        if m.get('Model') is not None:
            self.model = m.get('Model')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('UsageRate') is not None:
            self.usage_rate = m.get('UsageRate')
        return self


class JobViewMetric(TeaModel):
    def __init__(
        self,
        cpuusage_rate: str = None,
        disk_read_rate: str = None,
        disk_write_rate: str = None,
        gpuusage_rate: str = None,
        job_id: str = None,
        job_type: str = None,
        memory_usage_rate: str = None,
        network_input_rate: str = None,
        network_output_rate: str = None,
        node_names: List[str] = None,
        request_cpu: int = None,
        request_gpu: int = None,
        request_memory: int = None,
        resource_group_id: str = None,
        total_cpu: int = None,
        total_gpu: int = None,
        total_memory: int = None,
        user_id: str = None,
    ):
        self.cpuusage_rate = cpuusage_rate
        self.disk_read_rate = disk_read_rate
        self.disk_write_rate = disk_write_rate
        self.gpuusage_rate = gpuusage_rate
        self.job_id = job_id
        self.job_type = job_type
        self.memory_usage_rate = memory_usage_rate
        self.network_input_rate = network_input_rate
        self.network_output_rate = network_output_rate
        self.node_names = node_names
        self.request_cpu = request_cpu
        self.request_gpu = request_gpu
        self.request_memory = request_memory
        self.resource_group_id = resource_group_id
        self.total_cpu = total_cpu
        self.total_gpu = total_gpu
        self.total_memory = total_memory
        self.user_id = user_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cpuusage_rate is not None:
            result['CPUUsageRate'] = self.cpuusage_rate
        if self.disk_read_rate is not None:
            result['DiskReadRate'] = self.disk_read_rate
        if self.disk_write_rate is not None:
            result['DiskWriteRate'] = self.disk_write_rate
        if self.gpuusage_rate is not None:
            result['GPUUsageRate'] = self.gpuusage_rate
        if self.job_id is not None:
            result['JobId'] = self.job_id
        if self.job_type is not None:
            result['JobType'] = self.job_type
        if self.memory_usage_rate is not None:
            result['MemoryUsageRate'] = self.memory_usage_rate
        if self.network_input_rate is not None:
            result['NetworkInputRate'] = self.network_input_rate
        if self.network_output_rate is not None:
            result['NetworkOutputRate'] = self.network_output_rate
        if self.node_names is not None:
            result['NodeNames'] = self.node_names
        if self.request_cpu is not None:
            result['RequestCPU'] = self.request_cpu
        if self.request_gpu is not None:
            result['RequestGPU'] = self.request_gpu
        if self.request_memory is not None:
            result['RequestMemory'] = self.request_memory
        if self.resource_group_id is not None:
            result['ResourceGroupID'] = self.resource_group_id
        if self.total_cpu is not None:
            result['TotalCPU'] = self.total_cpu
        if self.total_gpu is not None:
            result['TotalGPU'] = self.total_gpu
        if self.total_memory is not None:
            result['TotalMemory'] = self.total_memory
        if self.user_id is not None:
            result['UserId'] = self.user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CPUUsageRate') is not None:
            self.cpuusage_rate = m.get('CPUUsageRate')
        if m.get('DiskReadRate') is not None:
            self.disk_read_rate = m.get('DiskReadRate')
        if m.get('DiskWriteRate') is not None:
            self.disk_write_rate = m.get('DiskWriteRate')
        if m.get('GPUUsageRate') is not None:
            self.gpuusage_rate = m.get('GPUUsageRate')
        if m.get('JobId') is not None:
            self.job_id = m.get('JobId')
        if m.get('JobType') is not None:
            self.job_type = m.get('JobType')
        if m.get('MemoryUsageRate') is not None:
            self.memory_usage_rate = m.get('MemoryUsageRate')
        if m.get('NetworkInputRate') is not None:
            self.network_input_rate = m.get('NetworkInputRate')
        if m.get('NetworkOutputRate') is not None:
            self.network_output_rate = m.get('NetworkOutputRate')
        if m.get('NodeNames') is not None:
            self.node_names = m.get('NodeNames')
        if m.get('RequestCPU') is not None:
            self.request_cpu = m.get('RequestCPU')
        if m.get('RequestGPU') is not None:
            self.request_gpu = m.get('RequestGPU')
        if m.get('RequestMemory') is not None:
            self.request_memory = m.get('RequestMemory')
        if m.get('ResourceGroupID') is not None:
            self.resource_group_id = m.get('ResourceGroupID')
        if m.get('TotalCPU') is not None:
            self.total_cpu = m.get('TotalCPU')
        if m.get('TotalGPU') is not None:
            self.total_gpu = m.get('TotalGPU')
        if m.get('TotalMemory') is not None:
            self.total_memory = m.get('TotalMemory')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        return self


class Label(TeaModel):
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


class MachineGroup(TeaModel):
    def __init__(
        self,
        creator_id: str = None,
        default_driver: str = None,
        ecs_count: int = None,
        ecs_spec: str = None,
        gmt_created_time: str = None,
        gmt_expired_time: str = None,
        gmt_modified_time: str = None,
        gmt_started_time: str = None,
        machine_group_id: str = None,
        order_instance_id: str = None,
        payment_duration: str = None,
        payment_duration_unit: str = None,
        payment_type: str = None,
        reason_code: str = None,
        reason_message: str = None,
        resource_group_id: str = None,
        status: str = None,
        supported_drivers: List[str] = None,
    ):
        self.creator_id = creator_id
        self.default_driver = default_driver
        self.ecs_count = ecs_count
        self.ecs_spec = ecs_spec
        self.gmt_created_time = gmt_created_time
        self.gmt_expired_time = gmt_expired_time
        self.gmt_modified_time = gmt_modified_time
        self.gmt_started_time = gmt_started_time
        self.machine_group_id = machine_group_id
        self.order_instance_id = order_instance_id
        self.payment_duration = payment_duration
        self.payment_duration_unit = payment_duration_unit
        self.payment_type = payment_type
        self.reason_code = reason_code
        self.reason_message = reason_message
        self.resource_group_id = resource_group_id
        self.status = status
        self.supported_drivers = supported_drivers

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.creator_id is not None:
            result['CreatorID'] = self.creator_id
        if self.default_driver is not None:
            result['DefaultDriver'] = self.default_driver
        if self.ecs_count is not None:
            result['EcsCount'] = self.ecs_count
        if self.ecs_spec is not None:
            result['EcsSpec'] = self.ecs_spec
        if self.gmt_created_time is not None:
            result['GmtCreatedTime'] = self.gmt_created_time
        if self.gmt_expired_time is not None:
            result['GmtExpiredTime'] = self.gmt_expired_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.gmt_started_time is not None:
            result['GmtStartedTime'] = self.gmt_started_time
        if self.machine_group_id is not None:
            result['MachineGroupID'] = self.machine_group_id
        if self.order_instance_id is not None:
            result['OrderInstanceId'] = self.order_instance_id
        if self.payment_duration is not None:
            result['PaymentDuration'] = self.payment_duration
        if self.payment_duration_unit is not None:
            result['PaymentDurationUnit'] = self.payment_duration_unit
        if self.payment_type is not None:
            result['PaymentType'] = self.payment_type
        if self.reason_code is not None:
            result['ReasonCode'] = self.reason_code
        if self.reason_message is not None:
            result['ReasonMessage'] = self.reason_message
        if self.resource_group_id is not None:
            result['ResourceGroupID'] = self.resource_group_id
        if self.status is not None:
            result['Status'] = self.status
        if self.supported_drivers is not None:
            result['SupportedDrivers'] = self.supported_drivers
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CreatorID') is not None:
            self.creator_id = m.get('CreatorID')
        if m.get('DefaultDriver') is not None:
            self.default_driver = m.get('DefaultDriver')
        if m.get('EcsCount') is not None:
            self.ecs_count = m.get('EcsCount')
        if m.get('EcsSpec') is not None:
            self.ecs_spec = m.get('EcsSpec')
        if m.get('GmtCreatedTime') is not None:
            self.gmt_created_time = m.get('GmtCreatedTime')
        if m.get('GmtExpiredTime') is not None:
            self.gmt_expired_time = m.get('GmtExpiredTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('GmtStartedTime') is not None:
            self.gmt_started_time = m.get('GmtStartedTime')
        if m.get('MachineGroupID') is not None:
            self.machine_group_id = m.get('MachineGroupID')
        if m.get('OrderInstanceId') is not None:
            self.order_instance_id = m.get('OrderInstanceId')
        if m.get('PaymentDuration') is not None:
            self.payment_duration = m.get('PaymentDuration')
        if m.get('PaymentDurationUnit') is not None:
            self.payment_duration_unit = m.get('PaymentDurationUnit')
        if m.get('PaymentType') is not None:
            self.payment_type = m.get('PaymentType')
        if m.get('ReasonCode') is not None:
            self.reason_code = m.get('ReasonCode')
        if m.get('ReasonMessage') is not None:
            self.reason_message = m.get('ReasonMessage')
        if m.get('ResourceGroupID') is not None:
            self.resource_group_id = m.get('ResourceGroupID')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('SupportedDrivers') is not None:
            self.supported_drivers = m.get('SupportedDrivers')
        return self


class Metric(TeaModel):
    def __init__(
        self,
        time: int = None,
        value: str = None,
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


class QuotaIdName(TeaModel):
    def __init__(
        self,
        quota_id: str = None,
        quota_name: str = None,
    ):
        self.quota_id = quota_id
        self.quota_name = quota_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.quota_id is not None:
            result['QuotaId'] = self.quota_id
        if self.quota_name is not None:
            result['QuotaName'] = self.quota_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('QuotaId') is not None:
            self.quota_id = m.get('QuotaId')
        if m.get('QuotaName') is not None:
            self.quota_name = m.get('QuotaName')
        return self


class UserInfo(TeaModel):
    def __init__(
        self,
        user_id: str = None,
        user_name: str = None,
    ):
        self.user_id = user_id
        self.user_name = user_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.user_name is not None:
            result['UserName'] = self.user_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('UserName') is not None:
            self.user_name = m.get('UserName')
        return self


class Node(TeaModel):
    def __init__(
        self,
        accelerator_type: str = None,
        bound_quotas: List[QuotaIdName] = None,
        cpu: str = None,
        creator_id: str = None,
        gpu: str = None,
        gputype: str = None,
        gmt_create_time: str = None,
        gmt_expired_time: str = None,
        gmt_modified_time: str = None,
        is_bound: bool = None,
        limit_cpu: str = None,
        limit_gpu: str = None,
        limit_memory: str = None,
        machine_group_id: str = None,
        memory: str = None,
        node_name: str = None,
        node_status: str = None,
        node_type: str = None,
        order_status: str = None,
        pod_num: int = None,
        reason_code: str = None,
        reason_message: str = None,
        request_cpu: str = None,
        request_gpu: str = None,
        request_memory: str = None,
        resource_group_id: str = None,
        resource_group_name: str = None,
        users: List[UserInfo] = None,
        workload_num: int = None,
    ):
        self.accelerator_type = accelerator_type
        self.bound_quotas = bound_quotas
        self.cpu = cpu
        self.creator_id = creator_id
        self.gpu = gpu
        self.gputype = gputype
        self.gmt_create_time = gmt_create_time
        self.gmt_expired_time = gmt_expired_time
        self.gmt_modified_time = gmt_modified_time
        self.is_bound = is_bound
        self.limit_cpu = limit_cpu
        self.limit_gpu = limit_gpu
        self.limit_memory = limit_memory
        self.machine_group_id = machine_group_id
        self.memory = memory
        self.node_name = node_name
        self.node_status = node_status
        self.node_type = node_type
        self.order_status = order_status
        self.pod_num = pod_num
        self.reason_code = reason_code
        self.reason_message = reason_message
        self.request_cpu = request_cpu
        self.request_gpu = request_gpu
        self.request_memory = request_memory
        self.resource_group_id = resource_group_id
        self.resource_group_name = resource_group_name
        self.users = users
        self.workload_num = workload_num

    def validate(self):
        if self.bound_quotas:
            for k in self.bound_quotas:
                if k:
                    k.validate()
        if self.users:
            for k in self.users:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.accelerator_type is not None:
            result['AcceleratorType'] = self.accelerator_type
        result['BoundQuotas'] = []
        if self.bound_quotas is not None:
            for k in self.bound_quotas:
                result['BoundQuotas'].append(k.to_map() if k else None)
        if self.cpu is not None:
            result['CPU'] = self.cpu
        if self.creator_id is not None:
            result['CreatorId'] = self.creator_id
        if self.gpu is not None:
            result['GPU'] = self.gpu
        if self.gputype is not None:
            result['GPUType'] = self.gputype
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_expired_time is not None:
            result['GmtExpiredTime'] = self.gmt_expired_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.is_bound is not None:
            result['IsBound'] = self.is_bound
        if self.limit_cpu is not None:
            result['LimitCPU'] = self.limit_cpu
        if self.limit_gpu is not None:
            result['LimitGPU'] = self.limit_gpu
        if self.limit_memory is not None:
            result['LimitMemory'] = self.limit_memory
        if self.machine_group_id is not None:
            result['MachineGroupId'] = self.machine_group_id
        if self.memory is not None:
            result['Memory'] = self.memory
        if self.node_name is not None:
            result['NodeName'] = self.node_name
        if self.node_status is not None:
            result['NodeStatus'] = self.node_status
        if self.node_type is not None:
            result['NodeType'] = self.node_type
        if self.order_status is not None:
            result['OrderStatus'] = self.order_status
        if self.pod_num is not None:
            result['PodNum'] = self.pod_num
        if self.reason_code is not None:
            result['ReasonCode'] = self.reason_code
        if self.reason_message is not None:
            result['ReasonMessage'] = self.reason_message
        if self.request_cpu is not None:
            result['RequestCPU'] = self.request_cpu
        if self.request_gpu is not None:
            result['RequestGPU'] = self.request_gpu
        if self.request_memory is not None:
            result['RequestMemory'] = self.request_memory
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.resource_group_name is not None:
            result['ResourceGroupName'] = self.resource_group_name
        result['Users'] = []
        if self.users is not None:
            for k in self.users:
                result['Users'].append(k.to_map() if k else None)
        if self.workload_num is not None:
            result['WorkloadNum'] = self.workload_num
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AcceleratorType') is not None:
            self.accelerator_type = m.get('AcceleratorType')
        self.bound_quotas = []
        if m.get('BoundQuotas') is not None:
            for k in m.get('BoundQuotas'):
                temp_model = QuotaIdName()
                self.bound_quotas.append(temp_model.from_map(k))
        if m.get('CPU') is not None:
            self.cpu = m.get('CPU')
        if m.get('CreatorId') is not None:
            self.creator_id = m.get('CreatorId')
        if m.get('GPU') is not None:
            self.gpu = m.get('GPU')
        if m.get('GPUType') is not None:
            self.gputype = m.get('GPUType')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtExpiredTime') is not None:
            self.gmt_expired_time = m.get('GmtExpiredTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('IsBound') is not None:
            self.is_bound = m.get('IsBound')
        if m.get('LimitCPU') is not None:
            self.limit_cpu = m.get('LimitCPU')
        if m.get('LimitGPU') is not None:
            self.limit_gpu = m.get('LimitGPU')
        if m.get('LimitMemory') is not None:
            self.limit_memory = m.get('LimitMemory')
        if m.get('MachineGroupId') is not None:
            self.machine_group_id = m.get('MachineGroupId')
        if m.get('Memory') is not None:
            self.memory = m.get('Memory')
        if m.get('NodeName') is not None:
            self.node_name = m.get('NodeName')
        if m.get('NodeStatus') is not None:
            self.node_status = m.get('NodeStatus')
        if m.get('NodeType') is not None:
            self.node_type = m.get('NodeType')
        if m.get('OrderStatus') is not None:
            self.order_status = m.get('OrderStatus')
        if m.get('PodNum') is not None:
            self.pod_num = m.get('PodNum')
        if m.get('ReasonCode') is not None:
            self.reason_code = m.get('ReasonCode')
        if m.get('ReasonMessage') is not None:
            self.reason_message = m.get('ReasonMessage')
        if m.get('RequestCPU') is not None:
            self.request_cpu = m.get('RequestCPU')
        if m.get('RequestGPU') is not None:
            self.request_gpu = m.get('RequestGPU')
        if m.get('RequestMemory') is not None:
            self.request_memory = m.get('RequestMemory')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('ResourceGroupName') is not None:
            self.resource_group_name = m.get('ResourceGroupName')
        self.users = []
        if m.get('Users') is not None:
            for k in m.get('Users'):
                temp_model = UserInfo()
                self.users.append(temp_model.from_map(k))
        if m.get('WorkloadNum') is not None:
            self.workload_num = m.get('WorkloadNum')
        return self


class NodeGPUMetric(TeaModel):
    def __init__(
        self,
        accelerator_type: str = None,
        gpucount: int = None,
        gpumetrics: List[GPUMetric] = None,
        gputype: str = None,
        memory_util: float = None,
        node_id: str = None,
        node_type: str = None,
        total_memory: float = None,
        used_memory: float = None,
    ):
        self.accelerator_type = accelerator_type
        self.gpucount = gpucount
        self.gpumetrics = gpumetrics
        self.gputype = gputype
        self.memory_util = memory_util
        self.node_id = node_id
        self.node_type = node_type
        self.total_memory = total_memory
        self.used_memory = used_memory

    def validate(self):
        if self.gpumetrics:
            for k in self.gpumetrics:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.accelerator_type is not None:
            result['AcceleratorType'] = self.accelerator_type
        if self.gpucount is not None:
            result['GPUCount'] = self.gpucount
        result['GPUMetrics'] = []
        if self.gpumetrics is not None:
            for k in self.gpumetrics:
                result['GPUMetrics'].append(k.to_map() if k else None)
        if self.gputype is not None:
            result['GPUType'] = self.gputype
        if self.memory_util is not None:
            result['MemoryUtil'] = self.memory_util
        if self.node_id is not None:
            result['NodeId'] = self.node_id
        if self.node_type is not None:
            result['NodeType'] = self.node_type
        if self.total_memory is not None:
            result['TotalMemory'] = self.total_memory
        if self.used_memory is not None:
            result['UsedMemory'] = self.used_memory
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AcceleratorType') is not None:
            self.accelerator_type = m.get('AcceleratorType')
        if m.get('GPUCount') is not None:
            self.gpucount = m.get('GPUCount')
        self.gpumetrics = []
        if m.get('GPUMetrics') is not None:
            for k in m.get('GPUMetrics'):
                temp_model = GPUMetric()
                self.gpumetrics.append(temp_model.from_map(k))
        if m.get('GPUType') is not None:
            self.gputype = m.get('GPUType')
        if m.get('MemoryUtil') is not None:
            self.memory_util = m.get('MemoryUtil')
        if m.get('NodeId') is not None:
            self.node_id = m.get('NodeId')
        if m.get('NodeType') is not None:
            self.node_type = m.get('NodeType')
        if m.get('TotalMemory') is not None:
            self.total_memory = m.get('TotalMemory')
        if m.get('UsedMemory') is not None:
            self.used_memory = m.get('UsedMemory')
        return self


class NodeMetric(TeaModel):
    def __init__(
        self,
        gputype: str = None,
        metrics: List[Metric] = None,
        node_id: str = None,
    ):
        self.gputype = gputype
        self.metrics = metrics
        self.node_id = node_id

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
        if self.gputype is not None:
            result['GPUType'] = self.gputype
        result['Metrics'] = []
        if self.metrics is not None:
            for k in self.metrics:
                result['Metrics'].append(k.to_map() if k else None)
        if self.node_id is not None:
            result['NodeID'] = self.node_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GPUType') is not None:
            self.gputype = m.get('GPUType')
        self.metrics = []
        if m.get('Metrics') is not None:
            for k in m.get('Metrics'):
                temp_model = Metric()
                self.metrics.append(temp_model.from_map(k))
        if m.get('NodeID') is not None:
            self.node_id = m.get('NodeID')
        return self


class ResourceAmount(TeaModel):
    def __init__(
        self,
        cpu: str = None,
        gpu: str = None,
        gputype: str = None,
        memory: str = None,
    ):
        self.cpu = cpu
        self.gpu = gpu
        self.gputype = gputype
        self.memory = memory

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
        return self


class NodePodInfo(TeaModel):
    def __init__(
        self,
        phase: str = None,
        pod_ip: str = None,
        pod_name: str = None,
        pod_namespace: str = None,
        resource_spec: ResourceAmount = None,
        workload_id: str = None,
        workload_type: str = None,
    ):
        self.phase = phase
        self.pod_ip = pod_ip
        self.pod_name = pod_name
        self.pod_namespace = pod_namespace
        self.resource_spec = resource_spec
        self.workload_id = workload_id
        self.workload_type = workload_type

    def validate(self):
        if self.resource_spec:
            self.resource_spec.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.phase is not None:
            result['Phase'] = self.phase
        if self.pod_ip is not None:
            result['PodIP'] = self.pod_ip
        if self.pod_name is not None:
            result['PodName'] = self.pod_name
        if self.pod_namespace is not None:
            result['PodNamespace'] = self.pod_namespace
        if self.resource_spec is not None:
            result['ResourceSpec'] = self.resource_spec.to_map()
        if self.workload_id is not None:
            result['WorkloadId'] = self.workload_id
        if self.workload_type is not None:
            result['WorkloadType'] = self.workload_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Phase') is not None:
            self.phase = m.get('Phase')
        if m.get('PodIP') is not None:
            self.pod_ip = m.get('PodIP')
        if m.get('PodName') is not None:
            self.pod_name = m.get('PodName')
        if m.get('PodNamespace') is not None:
            self.pod_namespace = m.get('PodNamespace')
        if m.get('ResourceSpec') is not None:
            temp_model = ResourceAmount()
            self.resource_spec = temp_model.from_map(m['ResourceSpec'])
        if m.get('WorkloadId') is not None:
            self.workload_id = m.get('WorkloadId')
        if m.get('WorkloadType') is not None:
            self.workload_type = m.get('WorkloadType')
        return self


class NodeType(TeaModel):
    def __init__(
        self,
        accelerator_type: str = None,
        cpu: str = None,
        gpu: str = None,
        gputype: str = None,
        memory: str = None,
        node_type: str = None,
    ):
        self.accelerator_type = accelerator_type
        self.cpu = cpu
        self.gpu = gpu
        self.gputype = gputype
        self.memory = memory
        self.node_type = node_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.accelerator_type is not None:
            result['AcceleratorType'] = self.accelerator_type
        if self.cpu is not None:
            result['CPU'] = self.cpu
        if self.gpu is not None:
            result['GPU'] = self.gpu
        if self.gputype is not None:
            result['GPUType'] = self.gputype
        if self.memory is not None:
            result['Memory'] = self.memory
        if self.node_type is not None:
            result['NodeType'] = self.node_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AcceleratorType') is not None:
            self.accelerator_type = m.get('AcceleratorType')
        if m.get('CPU') is not None:
            self.cpu = m.get('CPU')
        if m.get('GPU') is not None:
            self.gpu = m.get('GPU')
        if m.get('GPUType') is not None:
            self.gputype = m.get('GPUType')
        if m.get('Memory') is not None:
            self.memory = m.get('Memory')
        if m.get('NodeType') is not None:
            self.node_type = m.get('NodeType')
        return self


class NodeTypeStatistic(TeaModel):
    def __init__(
        self,
        can_be_bound_count: int = None,
        node_type: str = None,
        total_count: int = None,
    ):
        self.can_be_bound_count = can_be_bound_count
        self.node_type = node_type
        self.total_count = total_count

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.can_be_bound_count is not None:
            result['CanBeBoundCount'] = self.can_be_bound_count
        if self.node_type is not None:
            result['NodeType'] = self.node_type
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CanBeBoundCount') is not None:
            self.can_be_bound_count = m.get('CanBeBoundCount')
        if m.get('NodeType') is not None:
            self.node_type = m.get('NodeType')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class NodeViewMetric(TeaModel):
    def __init__(
        self,
        cpuusage_rate: str = None,
        created_time: str = None,
        disk_read_rate: str = None,
        disk_write_rate: str = None,
        gputype: str = None,
        machine_group_id: str = None,
        memory_usage_rate: str = None,
        network_input_rate: str = None,
        network_output_rate: str = None,
        node_id: str = None,
        node_status: str = None,
        node_type: str = None,
        request_cpu: int = None,
        request_gpu: int = None,
        request_memory: int = None,
        task_id_map: Dict[str, Any] = None,
        total_cpu: int = None,
        total_gpu: int = None,
        total_memory: int = None,
        total_tasks: int = None,
        user_ids: List[str] = None,
        user_number: str = None,
    ):
        self.cpuusage_rate = cpuusage_rate
        self.created_time = created_time
        self.disk_read_rate = disk_read_rate
        self.disk_write_rate = disk_write_rate
        self.gputype = gputype
        self.machine_group_id = machine_group_id
        self.memory_usage_rate = memory_usage_rate
        self.network_input_rate = network_input_rate
        self.network_output_rate = network_output_rate
        self.node_id = node_id
        self.node_status = node_status
        self.node_type = node_type
        self.request_cpu = request_cpu
        self.request_gpu = request_gpu
        self.request_memory = request_memory
        self.task_id_map = task_id_map
        self.total_cpu = total_cpu
        self.total_gpu = total_gpu
        self.total_memory = total_memory
        self.total_tasks = total_tasks
        self.user_ids = user_ids
        self.user_number = user_number

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cpuusage_rate is not None:
            result['CPUUsageRate'] = self.cpuusage_rate
        if self.created_time is not None:
            result['CreatedTime'] = self.created_time
        if self.disk_read_rate is not None:
            result['DiskReadRate'] = self.disk_read_rate
        if self.disk_write_rate is not None:
            result['DiskWriteRate'] = self.disk_write_rate
        if self.gputype is not None:
            result['GPUType'] = self.gputype
        if self.machine_group_id is not None:
            result['MachineGroupID'] = self.machine_group_id
        if self.memory_usage_rate is not None:
            result['MemoryUsageRate'] = self.memory_usage_rate
        if self.network_input_rate is not None:
            result['NetworkInputRate'] = self.network_input_rate
        if self.network_output_rate is not None:
            result['NetworkOutputRate'] = self.network_output_rate
        if self.node_id is not None:
            result['NodeID'] = self.node_id
        if self.node_status is not None:
            result['NodeStatus'] = self.node_status
        if self.node_type is not None:
            result['NodeType'] = self.node_type
        if self.request_cpu is not None:
            result['RequestCPU'] = self.request_cpu
        if self.request_gpu is not None:
            result['RequestGPU'] = self.request_gpu
        if self.request_memory is not None:
            result['RequestMemory'] = self.request_memory
        if self.task_id_map is not None:
            result['TaskIdMap'] = self.task_id_map
        if self.total_cpu is not None:
            result['TotalCPU'] = self.total_cpu
        if self.total_gpu is not None:
            result['TotalGPU'] = self.total_gpu
        if self.total_memory is not None:
            result['TotalMemory'] = self.total_memory
        if self.total_tasks is not None:
            result['TotalTasks'] = self.total_tasks
        if self.user_ids is not None:
            result['UserIDs'] = self.user_ids
        if self.user_number is not None:
            result['UserNumber'] = self.user_number
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CPUUsageRate') is not None:
            self.cpuusage_rate = m.get('CPUUsageRate')
        if m.get('CreatedTime') is not None:
            self.created_time = m.get('CreatedTime')
        if m.get('DiskReadRate') is not None:
            self.disk_read_rate = m.get('DiskReadRate')
        if m.get('DiskWriteRate') is not None:
            self.disk_write_rate = m.get('DiskWriteRate')
        if m.get('GPUType') is not None:
            self.gputype = m.get('GPUType')
        if m.get('MachineGroupID') is not None:
            self.machine_group_id = m.get('MachineGroupID')
        if m.get('MemoryUsageRate') is not None:
            self.memory_usage_rate = m.get('MemoryUsageRate')
        if m.get('NetworkInputRate') is not None:
            self.network_input_rate = m.get('NetworkInputRate')
        if m.get('NetworkOutputRate') is not None:
            self.network_output_rate = m.get('NetworkOutputRate')
        if m.get('NodeID') is not None:
            self.node_id = m.get('NodeID')
        if m.get('NodeStatus') is not None:
            self.node_status = m.get('NodeStatus')
        if m.get('NodeType') is not None:
            self.node_type = m.get('NodeType')
        if m.get('RequestCPU') is not None:
            self.request_cpu = m.get('RequestCPU')
        if m.get('RequestGPU') is not None:
            self.request_gpu = m.get('RequestGPU')
        if m.get('RequestMemory') is not None:
            self.request_memory = m.get('RequestMemory')
        if m.get('TaskIdMap') is not None:
            self.task_id_map = m.get('TaskIdMap')
        if m.get('TotalCPU') is not None:
            self.total_cpu = m.get('TotalCPU')
        if m.get('TotalGPU') is not None:
            self.total_gpu = m.get('TotalGPU')
        if m.get('TotalMemory') is not None:
            self.total_memory = m.get('TotalMemory')
        if m.get('TotalTasks') is not None:
            self.total_tasks = m.get('TotalTasks')
        if m.get('UserIDs') is not None:
            self.user_ids = m.get('UserIDs')
        if m.get('UserNumber') is not None:
            self.user_number = m.get('UserNumber')
        return self


class Permission(TeaModel):
    def __init__(
        self,
        is_enabled: bool = None,
        resource_type: str = None,
    ):
        self.is_enabled = is_enabled
        self.resource_type = resource_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.is_enabled is not None:
            result['IsEnabled'] = self.is_enabled
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('IsEnabled') is not None:
            self.is_enabled = m.get('IsEnabled')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        return self


class QueueInfo(TeaModel):
    def __init__(
        self,
        code: str = None,
        code_type: str = None,
        gmt_created_time: str = None,
        gmt_dequeued_time: str = None,
        gmt_enqueued_time: str = None,
        gmt_position_modified_time: str = None,
        name: str = None,
        position: int = None,
        priority: int = None,
        queue_strategy: str = None,
        quota_id: str = None,
        reason: str = None,
        resource: ResourceAmount = None,
        status: str = None,
        sub_status: str = None,
        user_id: str = None,
        user_name: str = None,
        workload_id: str = None,
        workload_name: str = None,
        workload_type: str = None,
        workspace_id: str = None,
    ):
        self.code = code
        self.code_type = code_type
        self.gmt_created_time = gmt_created_time
        self.gmt_dequeued_time = gmt_dequeued_time
        self.gmt_enqueued_time = gmt_enqueued_time
        self.gmt_position_modified_time = gmt_position_modified_time
        self.name = name
        self.position = position
        self.priority = priority
        self.queue_strategy = queue_strategy
        self.quota_id = quota_id
        self.reason = reason
        self.resource = resource
        self.status = status
        self.sub_status = sub_status
        self.user_id = user_id
        self.user_name = user_name
        self.workload_id = workload_id
        self.workload_name = workload_name
        self.workload_type = workload_type
        self.workspace_id = workspace_id

    def validate(self):
        if self.resource:
            self.resource.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.code_type is not None:
            result['CodeType'] = self.code_type
        if self.gmt_created_time is not None:
            result['GmtCreatedTime'] = self.gmt_created_time
        if self.gmt_dequeued_time is not None:
            result['GmtDequeuedTime'] = self.gmt_dequeued_time
        if self.gmt_enqueued_time is not None:
            result['GmtEnqueuedTime'] = self.gmt_enqueued_time
        if self.gmt_position_modified_time is not None:
            result['GmtPositionModifiedTime'] = self.gmt_position_modified_time
        if self.name is not None:
            result['Name'] = self.name
        if self.position is not None:
            result['Position'] = self.position
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.queue_strategy is not None:
            result['QueueStrategy'] = self.queue_strategy
        if self.quota_id is not None:
            result['QuotaId'] = self.quota_id
        if self.reason is not None:
            result['Reason'] = self.reason
        if self.resource is not None:
            result['Resource'] = self.resource.to_map()
        if self.status is not None:
            result['Status'] = self.status
        if self.sub_status is not None:
            result['SubStatus'] = self.sub_status
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.user_name is not None:
            result['UserName'] = self.user_name
        if self.workload_id is not None:
            result['WorkloadId'] = self.workload_id
        if self.workload_name is not None:
            result['WorkloadName'] = self.workload_name
        if self.workload_type is not None:
            result['WorkloadType'] = self.workload_type
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('CodeType') is not None:
            self.code_type = m.get('CodeType')
        if m.get('GmtCreatedTime') is not None:
            self.gmt_created_time = m.get('GmtCreatedTime')
        if m.get('GmtDequeuedTime') is not None:
            self.gmt_dequeued_time = m.get('GmtDequeuedTime')
        if m.get('GmtEnqueuedTime') is not None:
            self.gmt_enqueued_time = m.get('GmtEnqueuedTime')
        if m.get('GmtPositionModifiedTime') is not None:
            self.gmt_position_modified_time = m.get('GmtPositionModifiedTime')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Position') is not None:
            self.position = m.get('Position')
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('QueueStrategy') is not None:
            self.queue_strategy = m.get('QueueStrategy')
        if m.get('QuotaId') is not None:
            self.quota_id = m.get('QuotaId')
        if m.get('Reason') is not None:
            self.reason = m.get('Reason')
        if m.get('Resource') is not None:
            temp_model = ResourceAmount()
            self.resource = temp_model.from_map(m['Resource'])
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('SubStatus') is not None:
            self.sub_status = m.get('SubStatus')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('UserName') is not None:
            self.user_name = m.get('UserName')
        if m.get('WorkloadId') is not None:
            self.workload_id = m.get('WorkloadId')
        if m.get('WorkloadName') is not None:
            self.workload_name = m.get('WorkloadName')
        if m.get('WorkloadType') is not None:
            self.workload_type = m.get('WorkloadType')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class ResourceSpec(TeaModel):
    def __init__(
        self,
        node_specs: List[NodeSpec] = None,
    ):
        self.node_specs = node_specs

    def validate(self):
        if self.node_specs:
            for k in self.node_specs:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['NodeSpecs'] = []
        if self.node_specs is not None:
            for k in self.node_specs:
                result['NodeSpecs'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.node_specs = []
        if m.get('NodeSpecs') is not None:
            for k in m.get('NodeSpecs'):
                temp_model = NodeSpec()
                self.node_specs.append(temp_model.from_map(k))
        return self


class WorkspaceSpec(TeaModel):
    def __init__(
        self,
        code: str = None,
        code_type: str = None,
        is_guaranteed_valid: bool = None,
        is_over_sold_valid: bool = None,
        reason: str = None,
        spec: ResourceAmount = None,
        spec_name: str = None,
    ):
        self.code = code
        self.code_type = code_type
        self.is_guaranteed_valid = is_guaranteed_valid
        self.is_over_sold_valid = is_over_sold_valid
        self.reason = reason
        self.spec = spec
        self.spec_name = spec_name

    def validate(self):
        if self.spec:
            self.spec.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.code_type is not None:
            result['CodeType'] = self.code_type
        if self.is_guaranteed_valid is not None:
            result['IsGuaranteedValid'] = self.is_guaranteed_valid
        if self.is_over_sold_valid is not None:
            result['IsOverSoldValid'] = self.is_over_sold_valid
        if self.reason is not None:
            result['Reason'] = self.reason
        if self.spec is not None:
            result['Spec'] = self.spec.to_map()
        if self.spec_name is not None:
            result['SpecName'] = self.spec_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('CodeType') is not None:
            self.code_type = m.get('CodeType')
        if m.get('IsGuaranteedValid') is not None:
            self.is_guaranteed_valid = m.get('IsGuaranteedValid')
        if m.get('IsOverSoldValid') is not None:
            self.is_over_sold_valid = m.get('IsOverSoldValid')
        if m.get('Reason') is not None:
            self.reason = m.get('Reason')
        if m.get('Spec') is not None:
            temp_model = ResourceAmount()
            self.spec = temp_model.from_map(m['Spec'])
        if m.get('SpecName') is not None:
            self.spec_name = m.get('SpecName')
        return self


class WorkspaceSpecs(TeaModel):
    def __init__(
        self,
        product: str = None,
        specs: List[WorkspaceSpec] = None,
        workspace_id: str = None,
    ):
        self.product = product
        self.specs = specs
        self.workspace_id = workspace_id

    def validate(self):
        if self.specs:
            for k in self.specs:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.product is not None:
            result['Product'] = self.product
        result['Specs'] = []
        if self.specs is not None:
            for k in self.specs:
                result['Specs'].append(k.to_map() if k else None)
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Product') is not None:
            self.product = m.get('Product')
        self.specs = []
        if m.get('Specs') is not None:
            for k in m.get('Specs'):
                temp_model = WorkspaceSpec()
                self.specs.append(temp_model.from_map(k))
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class UserVpc(TeaModel):
    def __init__(
        self,
        default_route: str = None,
        extended_cidrs: List[str] = None,
        role_arn: str = None,
        security_group_id: str = None,
        switch_id: str = None,
        vpc_id: str = None,
    ):
        self.default_route = default_route
        self.extended_cidrs = extended_cidrs
        self.role_arn = role_arn
        self.security_group_id = security_group_id
        self.switch_id = switch_id
        self.vpc_id = vpc_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.default_route is not None:
            result['DefaultRoute'] = self.default_route
        if self.extended_cidrs is not None:
            result['ExtendedCIDRs'] = self.extended_cidrs
        if self.role_arn is not None:
            result['RoleArn'] = self.role_arn
        if self.security_group_id is not None:
            result['SecurityGroupId'] = self.security_group_id
        if self.switch_id is not None:
            result['SwitchId'] = self.switch_id
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DefaultRoute') is not None:
            self.default_route = m.get('DefaultRoute')
        if m.get('ExtendedCIDRs') is not None:
            self.extended_cidrs = m.get('ExtendedCIDRs')
        if m.get('RoleArn') is not None:
            self.role_arn = m.get('RoleArn')
        if m.get('SecurityGroupId') is not None:
            self.security_group_id = m.get('SecurityGroupId')
        if m.get('SwitchId') is not None:
            self.switch_id = m.get('SwitchId')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        return self


class QuotaConfig(TeaModel):
    def __init__(
        self,
        acs: ACS = None,
        cluster_id: str = None,
        default_gpudriver: str = None,
        enable_preempt_subquota_workloads: bool = None,
        resource_specs: List[WorkspaceSpecs] = None,
        support_gpudrivers: List[str] = None,
        support_rdma: bool = None,
        user_vpc: UserVpc = None,
    ):
        self.acs = acs
        self.cluster_id = cluster_id
        self.default_gpudriver = default_gpudriver
        self.enable_preempt_subquota_workloads = enable_preempt_subquota_workloads
        self.resource_specs = resource_specs
        self.support_gpudrivers = support_gpudrivers
        self.support_rdma = support_rdma
        self.user_vpc = user_vpc

    def validate(self):
        if self.acs:
            self.acs.validate()
        if self.resource_specs:
            for k in self.resource_specs:
                if k:
                    k.validate()
        if self.user_vpc:
            self.user_vpc.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.acs is not None:
            result['ACS'] = self.acs.to_map()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.default_gpudriver is not None:
            result['DefaultGPUDriver'] = self.default_gpudriver
        if self.enable_preempt_subquota_workloads is not None:
            result['EnablePreemptSubquotaWorkloads'] = self.enable_preempt_subquota_workloads
        result['ResourceSpecs'] = []
        if self.resource_specs is not None:
            for k in self.resource_specs:
                result['ResourceSpecs'].append(k.to_map() if k else None)
        if self.support_gpudrivers is not None:
            result['SupportGPUDrivers'] = self.support_gpudrivers
        if self.support_rdma is not None:
            result['SupportRDMA'] = self.support_rdma
        if self.user_vpc is not None:
            result['UserVpc'] = self.user_vpc.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ACS') is not None:
            temp_model = ACS()
            self.acs = temp_model.from_map(m['ACS'])
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('DefaultGPUDriver') is not None:
            self.default_gpudriver = m.get('DefaultGPUDriver')
        if m.get('EnablePreemptSubquotaWorkloads') is not None:
            self.enable_preempt_subquota_workloads = m.get('EnablePreemptSubquotaWorkloads')
        self.resource_specs = []
        if m.get('ResourceSpecs') is not None:
            for k in m.get('ResourceSpecs'):
                temp_model = WorkspaceSpecs()
                self.resource_specs.append(temp_model.from_map(k))
        if m.get('SupportGPUDrivers') is not None:
            self.support_gpudrivers = m.get('SupportGPUDrivers')
        if m.get('SupportRDMA') is not None:
            self.support_rdma = m.get('SupportRDMA')
        if m.get('UserVpc') is not None:
            temp_model = UserVpc()
            self.user_vpc = temp_model.from_map(m['UserVpc'])
        return self


class QuotaDetails(TeaModel):
    def __init__(
        self,
        actual_min_quota: ResourceAmount = None,
        desired_min_quota: ResourceAmount = None,
        requested_quota: ResourceAmount = None,
        used_quota: ResourceAmount = None,
    ):
        self.actual_min_quota = actual_min_quota
        self.desired_min_quota = desired_min_quota
        self.requested_quota = requested_quota
        self.used_quota = used_quota

    def validate(self):
        if self.actual_min_quota:
            self.actual_min_quota.validate()
        if self.desired_min_quota:
            self.desired_min_quota.validate()
        if self.requested_quota:
            self.requested_quota.validate()
        if self.used_quota:
            self.used_quota.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.actual_min_quota is not None:
            result['ActualMinQuota'] = self.actual_min_quota.to_map()
        if self.desired_min_quota is not None:
            result['DesiredMinQuota'] = self.desired_min_quota.to_map()
        if self.requested_quota is not None:
            result['RequestedQuota'] = self.requested_quota.to_map()
        if self.used_quota is not None:
            result['UsedQuota'] = self.used_quota.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ActualMinQuota') is not None:
            temp_model = ResourceAmount()
            self.actual_min_quota = temp_model.from_map(m['ActualMinQuota'])
        if m.get('DesiredMinQuota') is not None:
            temp_model = ResourceAmount()
            self.desired_min_quota = temp_model.from_map(m['DesiredMinQuota'])
        if m.get('RequestedQuota') is not None:
            temp_model = ResourceAmount()
            self.requested_quota = temp_model.from_map(m['RequestedQuota'])
        if m.get('UsedQuota') is not None:
            temp_model = ResourceAmount()
            self.used_quota = temp_model.from_map(m['UsedQuota'])
        return self


class WorkspaceIdName(TeaModel):
    def __init__(
        self,
        workspace_id: str = None,
    ):
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class Quota(TeaModel):
    def __init__(
        self,
        allocate_strategy: str = None,
        creator_id: str = None,
        description: str = None,
        gmt_created_time: str = None,
        gmt_modified_time: str = None,
        labels: List[Label] = None,
        latest_operation_id: str = None,
        min: ResourceSpec = None,
        parent_quota_id: str = None,
        queue_strategy: str = None,
        quota_config: QuotaConfig = None,
        quota_details: QuotaDetails = None,
        quota_id: str = None,
        quota_name: str = None,
        reason_code: str = None,
        reason_message: str = None,
        resource_group_ids: List[str] = None,
        resource_type: str = None,
        status: str = None,
        sub_quotas: List[QuotaIdName] = None,
        workspaces: List[WorkspaceIdName] = None,
    ):
        self.allocate_strategy = allocate_strategy
        self.creator_id = creator_id
        self.description = description
        self.gmt_created_time = gmt_created_time
        self.gmt_modified_time = gmt_modified_time
        self.labels = labels
        self.latest_operation_id = latest_operation_id
        self.min = min
        self.parent_quota_id = parent_quota_id
        self.queue_strategy = queue_strategy
        self.quota_config = quota_config
        self.quota_details = quota_details
        self.quota_id = quota_id
        self.quota_name = quota_name
        self.reason_code = reason_code
        self.reason_message = reason_message
        self.resource_group_ids = resource_group_ids
        self.resource_type = resource_type
        self.status = status
        self.sub_quotas = sub_quotas
        self.workspaces = workspaces

    def validate(self):
        if self.labels:
            for k in self.labels:
                if k:
                    k.validate()
        if self.min:
            self.min.validate()
        if self.quota_config:
            self.quota_config.validate()
        if self.quota_details:
            self.quota_details.validate()
        if self.sub_quotas:
            for k in self.sub_quotas:
                if k:
                    k.validate()
        if self.workspaces:
            for k in self.workspaces:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.allocate_strategy is not None:
            result['AllocateStrategy'] = self.allocate_strategy
        if self.creator_id is not None:
            result['CreatorId'] = self.creator_id
        if self.description is not None:
            result['Description'] = self.description
        if self.gmt_created_time is not None:
            result['GmtCreatedTime'] = self.gmt_created_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        if self.latest_operation_id is not None:
            result['LatestOperationId'] = self.latest_operation_id
        if self.min is not None:
            result['Min'] = self.min.to_map()
        if self.parent_quota_id is not None:
            result['ParentQuotaId'] = self.parent_quota_id
        if self.queue_strategy is not None:
            result['QueueStrategy'] = self.queue_strategy
        if self.quota_config is not None:
            result['QuotaConfig'] = self.quota_config.to_map()
        if self.quota_details is not None:
            result['QuotaDetails'] = self.quota_details.to_map()
        if self.quota_id is not None:
            result['QuotaId'] = self.quota_id
        if self.quota_name is not None:
            result['QuotaName'] = self.quota_name
        if self.reason_code is not None:
            result['ReasonCode'] = self.reason_code
        if self.reason_message is not None:
            result['ReasonMessage'] = self.reason_message
        if self.resource_group_ids is not None:
            result['ResourceGroupIds'] = self.resource_group_ids
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.status is not None:
            result['Status'] = self.status
        result['SubQuotas'] = []
        if self.sub_quotas is not None:
            for k in self.sub_quotas:
                result['SubQuotas'].append(k.to_map() if k else None)
        result['Workspaces'] = []
        if self.workspaces is not None:
            for k in self.workspaces:
                result['Workspaces'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AllocateStrategy') is not None:
            self.allocate_strategy = m.get('AllocateStrategy')
        if m.get('CreatorId') is not None:
            self.creator_id = m.get('CreatorId')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('GmtCreatedTime') is not None:
            self.gmt_created_time = m.get('GmtCreatedTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = Label()
                self.labels.append(temp_model.from_map(k))
        if m.get('LatestOperationId') is not None:
            self.latest_operation_id = m.get('LatestOperationId')
        if m.get('Min') is not None:
            temp_model = ResourceSpec()
            self.min = temp_model.from_map(m['Min'])
        if m.get('ParentQuotaId') is not None:
            self.parent_quota_id = m.get('ParentQuotaId')
        if m.get('QueueStrategy') is not None:
            self.queue_strategy = m.get('QueueStrategy')
        if m.get('QuotaConfig') is not None:
            temp_model = QuotaConfig()
            self.quota_config = temp_model.from_map(m['QuotaConfig'])
        if m.get('QuotaDetails') is not None:
            temp_model = QuotaDetails()
            self.quota_details = temp_model.from_map(m['QuotaDetails'])
        if m.get('QuotaId') is not None:
            self.quota_id = m.get('QuotaId')
        if m.get('QuotaName') is not None:
            self.quota_name = m.get('QuotaName')
        if m.get('ReasonCode') is not None:
            self.reason_code = m.get('ReasonCode')
        if m.get('ReasonMessage') is not None:
            self.reason_message = m.get('ReasonMessage')
        if m.get('ResourceGroupIds') is not None:
            self.resource_group_ids = m.get('ResourceGroupIds')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        self.sub_quotas = []
        if m.get('SubQuotas') is not None:
            for k in m.get('SubQuotas'):
                temp_model = QuotaIdName()
                self.sub_quotas.append(temp_model.from_map(k))
        self.workspaces = []
        if m.get('Workspaces') is not None:
            for k in m.get('Workspaces'):
                temp_model = WorkspaceIdName()
                self.workspaces.append(temp_model.from_map(k))
        return self


class QuotaJob(TeaModel):
    def __init__(
        self,
        queuing: int = None,
        running: int = None,
        total: int = None,
    ):
        self.queuing = queuing
        self.running = running
        self.total = total

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.queuing is not None:
            result['Queuing'] = self.queuing
        if self.running is not None:
            result['Running'] = self.running
        if self.total is not None:
            result['Total'] = self.total
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Queuing') is not None:
            self.queuing = m.get('Queuing')
        if m.get('Running') is not None:
            self.running = m.get('Running')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        return self


class QuotaJobViewMetric(TeaModel):
    def __init__(
        self,
        cpuusage_rate: str = None,
        disk_read_rate: str = None,
        disk_write_rate: str = None,
        gpuusage_rate: str = None,
        job_id: str = None,
        job_type: str = None,
        memory_usage_rate: str = None,
        network_input_rate: str = None,
        network_output_rate: str = None,
        node_names: List[str] = None,
        request_cpu: int = None,
        request_gpu: int = None,
        request_memory: int = None,
        total_cpu: int = None,
        total_gpu: int = None,
        total_memory: int = None,
        user_id: str = None,
    ):
        self.cpuusage_rate = cpuusage_rate
        self.disk_read_rate = disk_read_rate
        self.disk_write_rate = disk_write_rate
        self.gpuusage_rate = gpuusage_rate
        self.job_id = job_id
        self.job_type = job_type
        self.memory_usage_rate = memory_usage_rate
        self.network_input_rate = network_input_rate
        self.network_output_rate = network_output_rate
        self.node_names = node_names
        self.request_cpu = request_cpu
        self.request_gpu = request_gpu
        self.request_memory = request_memory
        self.total_cpu = total_cpu
        self.total_gpu = total_gpu
        self.total_memory = total_memory
        self.user_id = user_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cpuusage_rate is not None:
            result['CPUUsageRate'] = self.cpuusage_rate
        if self.disk_read_rate is not None:
            result['DiskReadRate'] = self.disk_read_rate
        if self.disk_write_rate is not None:
            result['DiskWriteRate'] = self.disk_write_rate
        if self.gpuusage_rate is not None:
            result['GPUUsageRate'] = self.gpuusage_rate
        if self.job_id is not None:
            result['JobId'] = self.job_id
        if self.job_type is not None:
            result['JobType'] = self.job_type
        if self.memory_usage_rate is not None:
            result['MemoryUsageRate'] = self.memory_usage_rate
        if self.network_input_rate is not None:
            result['NetworkInputRate'] = self.network_input_rate
        if self.network_output_rate is not None:
            result['NetworkOutputRate'] = self.network_output_rate
        if self.node_names is not None:
            result['NodeNames'] = self.node_names
        if self.request_cpu is not None:
            result['RequestCPU'] = self.request_cpu
        if self.request_gpu is not None:
            result['RequestGPU'] = self.request_gpu
        if self.request_memory is not None:
            result['RequestMemory'] = self.request_memory
        if self.total_cpu is not None:
            result['TotalCPU'] = self.total_cpu
        if self.total_gpu is not None:
            result['TotalGPU'] = self.total_gpu
        if self.total_memory is not None:
            result['TotalMemory'] = self.total_memory
        if self.user_id is not None:
            result['UserId'] = self.user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CPUUsageRate') is not None:
            self.cpuusage_rate = m.get('CPUUsageRate')
        if m.get('DiskReadRate') is not None:
            self.disk_read_rate = m.get('DiskReadRate')
        if m.get('DiskWriteRate') is not None:
            self.disk_write_rate = m.get('DiskWriteRate')
        if m.get('GPUUsageRate') is not None:
            self.gpuusage_rate = m.get('GPUUsageRate')
        if m.get('JobId') is not None:
            self.job_id = m.get('JobId')
        if m.get('JobType') is not None:
            self.job_type = m.get('JobType')
        if m.get('MemoryUsageRate') is not None:
            self.memory_usage_rate = m.get('MemoryUsageRate')
        if m.get('NetworkInputRate') is not None:
            self.network_input_rate = m.get('NetworkInputRate')
        if m.get('NetworkOutputRate') is not None:
            self.network_output_rate = m.get('NetworkOutputRate')
        if m.get('NodeNames') is not None:
            self.node_names = m.get('NodeNames')
        if m.get('RequestCPU') is not None:
            self.request_cpu = m.get('RequestCPU')
        if m.get('RequestGPU') is not None:
            self.request_gpu = m.get('RequestGPU')
        if m.get('RequestMemory') is not None:
            self.request_memory = m.get('RequestMemory')
        if m.get('TotalCPU') is not None:
            self.total_cpu = m.get('TotalCPU')
        if m.get('TotalGPU') is not None:
            self.total_gpu = m.get('TotalGPU')
        if m.get('TotalMemory') is not None:
            self.total_memory = m.get('TotalMemory')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        return self


class QuotaMetric(TeaModel):
    def __init__(
        self,
        gputype: str = None,
        metrics: List[Metric] = None,
    ):
        self.gputype = gputype
        self.metrics = metrics

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
        if self.gputype is not None:
            result['GPUType'] = self.gputype
        result['Metrics'] = []
        if self.metrics is not None:
            for k in self.metrics:
                result['Metrics'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GPUType') is not None:
            self.gputype = m.get('GPUType')
        self.metrics = []
        if m.get('Metrics') is not None:
            for k in m.get('Metrics'):
                temp_model = Metric()
                self.metrics.append(temp_model.from_map(k))
        return self


class QuotaNodeViewMetric(TeaModel):
    def __init__(
        self,
        cpuusage_rate: str = None,
        created_time: str = None,
        disk_read_rate: str = None,
        disk_write_rate: str = None,
        gputype: str = None,
        memory_usage_rate: str = None,
        network_input_rate: str = None,
        network_output_rate: str = None,
        node_id: str = None,
        node_status: str = None,
        node_type: str = None,
        quota_id: str = None,
        request_cpu: int = None,
        request_gpu: int = None,
        request_memory: int = None,
        task_id_map: Dict[str, Any] = None,
        total_cpu: int = None,
        total_gpu: int = None,
        total_memory: int = None,
        total_tasks: int = None,
        user_ids: List[str] = None,
        user_number: str = None,
    ):
        self.cpuusage_rate = cpuusage_rate
        self.created_time = created_time
        self.disk_read_rate = disk_read_rate
        self.disk_write_rate = disk_write_rate
        self.gputype = gputype
        self.memory_usage_rate = memory_usage_rate
        self.network_input_rate = network_input_rate
        self.network_output_rate = network_output_rate
        self.node_id = node_id
        self.node_status = node_status
        self.node_type = node_type
        self.quota_id = quota_id
        self.request_cpu = request_cpu
        self.request_gpu = request_gpu
        self.request_memory = request_memory
        self.task_id_map = task_id_map
        self.total_cpu = total_cpu
        self.total_gpu = total_gpu
        self.total_memory = total_memory
        self.total_tasks = total_tasks
        self.user_ids = user_ids
        self.user_number = user_number

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cpuusage_rate is not None:
            result['CPUUsageRate'] = self.cpuusage_rate
        if self.created_time is not None:
            result['CreatedTime'] = self.created_time
        if self.disk_read_rate is not None:
            result['DiskReadRate'] = self.disk_read_rate
        if self.disk_write_rate is not None:
            result['DiskWriteRate'] = self.disk_write_rate
        if self.gputype is not None:
            result['GPUType'] = self.gputype
        if self.memory_usage_rate is not None:
            result['MemoryUsageRate'] = self.memory_usage_rate
        if self.network_input_rate is not None:
            result['NetworkInputRate'] = self.network_input_rate
        if self.network_output_rate is not None:
            result['NetworkOutputRate'] = self.network_output_rate
        if self.node_id is not None:
            result['NodeID'] = self.node_id
        if self.node_status is not None:
            result['NodeStatus'] = self.node_status
        if self.node_type is not None:
            result['NodeType'] = self.node_type
        if self.quota_id is not None:
            result['QuotaId'] = self.quota_id
        if self.request_cpu is not None:
            result['RequestCPU'] = self.request_cpu
        if self.request_gpu is not None:
            result['RequestGPU'] = self.request_gpu
        if self.request_memory is not None:
            result['RequestMemory'] = self.request_memory
        if self.task_id_map is not None:
            result['TaskIdMap'] = self.task_id_map
        if self.total_cpu is not None:
            result['TotalCPU'] = self.total_cpu
        if self.total_gpu is not None:
            result['TotalGPU'] = self.total_gpu
        if self.total_memory is not None:
            result['TotalMemory'] = self.total_memory
        if self.total_tasks is not None:
            result['TotalTasks'] = self.total_tasks
        if self.user_ids is not None:
            result['UserIDs'] = self.user_ids
        if self.user_number is not None:
            result['UserNumber'] = self.user_number
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CPUUsageRate') is not None:
            self.cpuusage_rate = m.get('CPUUsageRate')
        if m.get('CreatedTime') is not None:
            self.created_time = m.get('CreatedTime')
        if m.get('DiskReadRate') is not None:
            self.disk_read_rate = m.get('DiskReadRate')
        if m.get('DiskWriteRate') is not None:
            self.disk_write_rate = m.get('DiskWriteRate')
        if m.get('GPUType') is not None:
            self.gputype = m.get('GPUType')
        if m.get('MemoryUsageRate') is not None:
            self.memory_usage_rate = m.get('MemoryUsageRate')
        if m.get('NetworkInputRate') is not None:
            self.network_input_rate = m.get('NetworkInputRate')
        if m.get('NetworkOutputRate') is not None:
            self.network_output_rate = m.get('NetworkOutputRate')
        if m.get('NodeID') is not None:
            self.node_id = m.get('NodeID')
        if m.get('NodeStatus') is not None:
            self.node_status = m.get('NodeStatus')
        if m.get('NodeType') is not None:
            self.node_type = m.get('NodeType')
        if m.get('QuotaId') is not None:
            self.quota_id = m.get('QuotaId')
        if m.get('RequestCPU') is not None:
            self.request_cpu = m.get('RequestCPU')
        if m.get('RequestGPU') is not None:
            self.request_gpu = m.get('RequestGPU')
        if m.get('RequestMemory') is not None:
            self.request_memory = m.get('RequestMemory')
        if m.get('TaskIdMap') is not None:
            self.task_id_map = m.get('TaskIdMap')
        if m.get('TotalCPU') is not None:
            self.total_cpu = m.get('TotalCPU')
        if m.get('TotalGPU') is not None:
            self.total_gpu = m.get('TotalGPU')
        if m.get('TotalMemory') is not None:
            self.total_memory = m.get('TotalMemory')
        if m.get('TotalTasks') is not None:
            self.total_tasks = m.get('TotalTasks')
        if m.get('UserIDs') is not None:
            self.user_ids = m.get('UserIDs')
        if m.get('UserNumber') is not None:
            self.user_number = m.get('UserNumber')
        return self


class WorkloadDetails(TeaModel):
    def __init__(
        self,
        dlc: QuotaJob = None,
        dsw: QuotaJob = None,
        eas: QuotaJob = None,
        summary: QuotaJob = None,
    ):
        self.dlc = dlc
        self.dsw = dsw
        self.eas = eas
        self.summary = summary

    def validate(self):
        if self.dlc:
            self.dlc.validate()
        if self.dsw:
            self.dsw.validate()
        if self.eas:
            self.eas.validate()
        if self.summary:
            self.summary.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.dlc is not None:
            result['DLC'] = self.dlc.to_map()
        if self.dsw is not None:
            result['DSW'] = self.dsw.to_map()
        if self.eas is not None:
            result['EAS'] = self.eas.to_map()
        if self.summary is not None:
            result['Summary'] = self.summary.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DLC') is not None:
            temp_model = QuotaJob()
            self.dlc = temp_model.from_map(m['DLC'])
        if m.get('DSW') is not None:
            temp_model = QuotaJob()
            self.dsw = temp_model.from_map(m['DSW'])
        if m.get('EAS') is not None:
            temp_model = QuotaJob()
            self.eas = temp_model.from_map(m['EAS'])
        if m.get('Summary') is not None:
            temp_model = QuotaJob()
            self.summary = temp_model.from_map(m['Summary'])
        return self


class QuotaTopo(TeaModel):
    def __init__(
        self,
        depth: str = None,
        parent_quota_id: str = None,
        quota_details: QuotaDetails = None,
        quota_id: str = None,
        quota_name: str = None,
        resource_type: str = None,
        workload_details: WorkloadDetails = None,
    ):
        self.depth = depth
        self.parent_quota_id = parent_quota_id
        self.quota_details = quota_details
        self.quota_id = quota_id
        self.quota_name = quota_name
        self.resource_type = resource_type
        self.workload_details = workload_details

    def validate(self):
        if self.quota_details:
            self.quota_details.validate()
        if self.workload_details:
            self.workload_details.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.depth is not None:
            result['Depth'] = self.depth
        if self.parent_quota_id is not None:
            result['ParentQuotaId'] = self.parent_quota_id
        if self.quota_details is not None:
            result['QuotaDetails'] = self.quota_details.to_map()
        if self.quota_id is not None:
            result['QuotaId'] = self.quota_id
        if self.quota_name is not None:
            result['QuotaName'] = self.quota_name
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.workload_details is not None:
            result['WorkloadDetails'] = self.workload_details.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Depth') is not None:
            self.depth = m.get('Depth')
        if m.get('ParentQuotaId') is not None:
            self.parent_quota_id = m.get('ParentQuotaId')
        if m.get('QuotaDetails') is not None:
            temp_model = QuotaDetails()
            self.quota_details = temp_model.from_map(m['QuotaDetails'])
        if m.get('QuotaId') is not None:
            self.quota_id = m.get('QuotaId')
        if m.get('QuotaName') is not None:
            self.quota_name = m.get('QuotaName')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('WorkloadDetails') is not None:
            temp_model = WorkloadDetails()
            self.workload_details = temp_model.from_map(m['WorkloadDetails'])
        return self


class QuotaUserResources(TeaModel):
    def __init__(
        self,
        submitted: ResourceAmount = None,
        used: ResourceAmount = None,
    ):
        self.submitted = submitted
        self.used = used

    def validate(self):
        if self.submitted:
            self.submitted.validate()
        if self.used:
            self.used.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.submitted is not None:
            result['Submitted'] = self.submitted.to_map()
        if self.used is not None:
            result['Used'] = self.used.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Submitted') is not None:
            temp_model = ResourceAmount()
            self.submitted = temp_model.from_map(m['Submitted'])
        if m.get('Used') is not None:
            temp_model = ResourceAmount()
            self.used = temp_model.from_map(m['Used'])
        return self


class QuotaUser(TeaModel):
    def __init__(
        self,
        resources: QuotaUserResources = None,
        user_id: str = None,
        username: str = None,
        workload_count: int = None,
    ):
        self.resources = resources
        self.user_id = user_id
        self.username = username
        self.workload_count = workload_count

    def validate(self):
        if self.resources:
            self.resources.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.resources is not None:
            result['Resources'] = self.resources.to_map()
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.username is not None:
            result['Username'] = self.username
        if self.workload_count is not None:
            result['WorkloadCount'] = self.workload_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Resources') is not None:
            temp_model = QuotaUserResources()
            self.resources = temp_model.from_map(m['Resources'])
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('Username') is not None:
            self.username = m.get('Username')
        if m.get('WorkloadCount') is not None:
            self.workload_count = m.get('WorkloadCount')
        return self


class QuotaUserViewMetric(TeaModel):
    def __init__(
        self,
        cpunode_number: int = None,
        cpuusage_rate: str = None,
        cpu_job_names: List[str] = None,
        cpu_node_names: List[str] = None,
        disk_read_rate: str = None,
        disk_write_rate: str = None,
        gpunode_number: int = None,
        gpuusage_rate: str = None,
        gpu_job_names: List[str] = None,
        gpu_node_names: List[str] = None,
        job_type: str = None,
        memory_usage_rate: str = None,
        network_input_rate: str = None,
        network_output_rate: str = None,
        node_names: List[str] = None,
        request_cpu: int = None,
        request_gpu: int = None,
        request_memory: int = None,
        total_cpu: int = None,
        total_gpu: int = None,
        total_memory: int = None,
        user_id: str = None,
    ):
        self.cpunode_number = cpunode_number
        self.cpuusage_rate = cpuusage_rate
        self.cpu_job_names = cpu_job_names
        self.cpu_node_names = cpu_node_names
        self.disk_read_rate = disk_read_rate
        self.disk_write_rate = disk_write_rate
        self.gpunode_number = gpunode_number
        self.gpuusage_rate = gpuusage_rate
        self.gpu_job_names = gpu_job_names
        self.gpu_node_names = gpu_node_names
        self.job_type = job_type
        self.memory_usage_rate = memory_usage_rate
        self.network_input_rate = network_input_rate
        self.network_output_rate = network_output_rate
        self.node_names = node_names
        self.request_cpu = request_cpu
        self.request_gpu = request_gpu
        self.request_memory = request_memory
        self.total_cpu = total_cpu
        self.total_gpu = total_gpu
        self.total_memory = total_memory
        self.user_id = user_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cpunode_number is not None:
            result['CPUNodeNumber'] = self.cpunode_number
        if self.cpuusage_rate is not None:
            result['CPUUsageRate'] = self.cpuusage_rate
        if self.cpu_job_names is not None:
            result['CpuJobNames'] = self.cpu_job_names
        if self.cpu_node_names is not None:
            result['CpuNodeNames'] = self.cpu_node_names
        if self.disk_read_rate is not None:
            result['DiskReadRate'] = self.disk_read_rate
        if self.disk_write_rate is not None:
            result['DiskWriteRate'] = self.disk_write_rate
        if self.gpunode_number is not None:
            result['GPUNodeNumber'] = self.gpunode_number
        if self.gpuusage_rate is not None:
            result['GPUUsageRate'] = self.gpuusage_rate
        if self.gpu_job_names is not None:
            result['GpuJobNames'] = self.gpu_job_names
        if self.gpu_node_names is not None:
            result['GpuNodeNames'] = self.gpu_node_names
        if self.job_type is not None:
            result['JobType'] = self.job_type
        if self.memory_usage_rate is not None:
            result['MemoryUsageRate'] = self.memory_usage_rate
        if self.network_input_rate is not None:
            result['NetworkInputRate'] = self.network_input_rate
        if self.network_output_rate is not None:
            result['NetworkOutputRate'] = self.network_output_rate
        if self.node_names is not None:
            result['NodeNames'] = self.node_names
        if self.request_cpu is not None:
            result['RequestCPU'] = self.request_cpu
        if self.request_gpu is not None:
            result['RequestGPU'] = self.request_gpu
        if self.request_memory is not None:
            result['RequestMemory'] = self.request_memory
        if self.total_cpu is not None:
            result['TotalCPU'] = self.total_cpu
        if self.total_gpu is not None:
            result['TotalGPU'] = self.total_gpu
        if self.total_memory is not None:
            result['TotalMemory'] = self.total_memory
        if self.user_id is not None:
            result['UserId'] = self.user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CPUNodeNumber') is not None:
            self.cpunode_number = m.get('CPUNodeNumber')
        if m.get('CPUUsageRate') is not None:
            self.cpuusage_rate = m.get('CPUUsageRate')
        if m.get('CpuJobNames') is not None:
            self.cpu_job_names = m.get('CpuJobNames')
        if m.get('CpuNodeNames') is not None:
            self.cpu_node_names = m.get('CpuNodeNames')
        if m.get('DiskReadRate') is not None:
            self.disk_read_rate = m.get('DiskReadRate')
        if m.get('DiskWriteRate') is not None:
            self.disk_write_rate = m.get('DiskWriteRate')
        if m.get('GPUNodeNumber') is not None:
            self.gpunode_number = m.get('GPUNodeNumber')
        if m.get('GPUUsageRate') is not None:
            self.gpuusage_rate = m.get('GPUUsageRate')
        if m.get('GpuJobNames') is not None:
            self.gpu_job_names = m.get('GpuJobNames')
        if m.get('GpuNodeNames') is not None:
            self.gpu_node_names = m.get('GpuNodeNames')
        if m.get('JobType') is not None:
            self.job_type = m.get('JobType')
        if m.get('MemoryUsageRate') is not None:
            self.memory_usage_rate = m.get('MemoryUsageRate')
        if m.get('NetworkInputRate') is not None:
            self.network_input_rate = m.get('NetworkInputRate')
        if m.get('NetworkOutputRate') is not None:
            self.network_output_rate = m.get('NetworkOutputRate')
        if m.get('NodeNames') is not None:
            self.node_names = m.get('NodeNames')
        if m.get('RequestCPU') is not None:
            self.request_cpu = m.get('RequestCPU')
        if m.get('RequestGPU') is not None:
            self.request_gpu = m.get('RequestGPU')
        if m.get('RequestMemory') is not None:
            self.request_memory = m.get('RequestMemory')
        if m.get('TotalCPU') is not None:
            self.total_cpu = m.get('TotalCPU')
        if m.get('TotalGPU') is not None:
            self.total_gpu = m.get('TotalGPU')
        if m.get('TotalMemory') is not None:
            self.total_memory = m.get('TotalMemory')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        return self


class ResourceGroup(TeaModel):
    def __init__(
        self,
        creator_id: str = None,
        gmt_created_time: str = None,
        gmt_modified_time: str = None,
        name: str = None,
        node_count: int = None,
        resource_group_id: str = None,
        user_vpc: UserVpc = None,
        workspace_id: str = None,
    ):
        self.creator_id = creator_id
        self.gmt_created_time = gmt_created_time
        self.gmt_modified_time = gmt_modified_time
        self.name = name
        self.node_count = node_count
        self.resource_group_id = resource_group_id
        self.user_vpc = user_vpc
        self.workspace_id = workspace_id

    def validate(self):
        if self.user_vpc:
            self.user_vpc.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.creator_id is not None:
            result['CreatorID'] = self.creator_id
        if self.gmt_created_time is not None:
            result['GmtCreatedTime'] = self.gmt_created_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.name is not None:
            result['Name'] = self.name
        if self.node_count is not None:
            result['NodeCount'] = self.node_count
        if self.resource_group_id is not None:
            result['ResourceGroupID'] = self.resource_group_id
        if self.user_vpc is not None:
            result['UserVpc'] = self.user_vpc.to_map()
        if self.workspace_id is not None:
            result['WorkspaceID'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CreatorID') is not None:
            self.creator_id = m.get('CreatorID')
        if m.get('GmtCreatedTime') is not None:
            self.gmt_created_time = m.get('GmtCreatedTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('NodeCount') is not None:
            self.node_count = m.get('NodeCount')
        if m.get('ResourceGroupID') is not None:
            self.resource_group_id = m.get('ResourceGroupID')
        if m.get('UserVpc') is not None:
            temp_model = UserVpc()
            self.user_vpc = temp_model.from_map(m['UserVpc'])
        if m.get('WorkspaceID') is not None:
            self.workspace_id = m.get('WorkspaceID')
        return self


class ResourceGroupMetric(TeaModel):
    def __init__(
        self,
        gpu_type: str = None,
        metrics: List[Metric] = None,
        resource_group_id: str = None,
    ):
        self.gpu_type = gpu_type
        self.metrics = metrics
        self.resource_group_id = resource_group_id

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
        if self.gpu_type is not None:
            result['GpuType'] = self.gpu_type
        result['Metrics'] = []
        if self.metrics is not None:
            for k in self.metrics:
                result['Metrics'].append(k.to_map() if k else None)
        if self.resource_group_id is not None:
            result['ResourceGroupID'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GpuType') is not None:
            self.gpu_type = m.get('GpuType')
        self.metrics = []
        if m.get('Metrics') is not None:
            for k in m.get('Metrics'):
                temp_model = Metric()
                self.metrics.append(temp_model.from_map(k))
        if m.get('ResourceGroupID') is not None:
            self.resource_group_id = m.get('ResourceGroupID')
        return self


class ResourceOperation(TeaModel):
    def __init__(
        self,
        creator_id: str = None,
        gmt_created_time: str = None,
        gmt_end_time: str = None,
        gmt_modified_time: str = None,
        gmt_start_time: str = None,
        object_id: str = None,
        object_type: str = None,
        operation_description: str = None,
        operation_id: str = None,
        operation_spec_json: str = None,
        operation_type: str = None,
        reason_code: str = None,
        reason_message: str = None,
        status: str = None,
    ):
        self.creator_id = creator_id
        self.gmt_created_time = gmt_created_time
        self.gmt_end_time = gmt_end_time
        self.gmt_modified_time = gmt_modified_time
        self.gmt_start_time = gmt_start_time
        self.object_id = object_id
        self.object_type = object_type
        self.operation_description = operation_description
        self.operation_id = operation_id
        self.operation_spec_json = operation_spec_json
        self.operation_type = operation_type
        self.reason_code = reason_code
        self.reason_message = reason_message
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.creator_id is not None:
            result['CreatorId'] = self.creator_id
        if self.gmt_created_time is not None:
            result['GmtCreatedTime'] = self.gmt_created_time
        if self.gmt_end_time is not None:
            result['GmtEndTime'] = self.gmt_end_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.gmt_start_time is not None:
            result['GmtStartTime'] = self.gmt_start_time
        if self.object_id is not None:
            result['ObjectId'] = self.object_id
        if self.object_type is not None:
            result['ObjectType'] = self.object_type
        if self.operation_description is not None:
            result['OperationDescription'] = self.operation_description
        if self.operation_id is not None:
            result['OperationId'] = self.operation_id
        if self.operation_spec_json is not None:
            result['OperationSpecJson'] = self.operation_spec_json
        if self.operation_type is not None:
            result['OperationType'] = self.operation_type
        if self.reason_code is not None:
            result['ReasonCode'] = self.reason_code
        if self.reason_message is not None:
            result['ReasonMessage'] = self.reason_message
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CreatorId') is not None:
            self.creator_id = m.get('CreatorId')
        if m.get('GmtCreatedTime') is not None:
            self.gmt_created_time = m.get('GmtCreatedTime')
        if m.get('GmtEndTime') is not None:
            self.gmt_end_time = m.get('GmtEndTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('GmtStartTime') is not None:
            self.gmt_start_time = m.get('GmtStartTime')
        if m.get('ObjectId') is not None:
            self.object_id = m.get('ObjectId')
        if m.get('ObjectType') is not None:
            self.object_type = m.get('ObjectType')
        if m.get('OperationDescription') is not None:
            self.operation_description = m.get('OperationDescription')
        if m.get('OperationId') is not None:
            self.operation_id = m.get('OperationId')
        if m.get('OperationSpecJson') is not None:
            self.operation_spec_json = m.get('OperationSpecJson')
        if m.get('OperationType') is not None:
            self.operation_type = m.get('OperationType')
        if m.get('ReasonCode') is not None:
            self.reason_code = m.get('ReasonCode')
        if m.get('ReasonMessage') is not None:
            self.reason_message = m.get('ReasonMessage')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class SpotPriceItem(TeaModel):
    def __init__(
        self,
        instance_type: str = None,
        spot_discount: float = None,
        timestamp: str = None,
        zone_id: str = None,
    ):
        self.instance_type = instance_type
        self.spot_discount = spot_discount
        self.timestamp = timestamp
        self.zone_id = zone_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        if self.spot_discount is not None:
            result['SpotDiscount'] = self.spot_discount
        if self.timestamp is not None:
            result['Timestamp'] = self.timestamp
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        if m.get('SpotDiscount') is not None:
            self.spot_discount = m.get('SpotDiscount')
        if m.get('Timestamp') is not None:
            self.timestamp = m.get('Timestamp')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        return self


class SpotStockPreview(TeaModel):
    def __init__(
        self,
        instance_type: str = None,
        spot_discount: float = None,
        stock_status: str = None,
    ):
        self.instance_type = instance_type
        self.spot_discount = spot_discount
        self.stock_status = stock_status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        if self.spot_discount is not None:
            result['SpotDiscount'] = self.spot_discount
        if self.stock_status is not None:
            result['StockStatus'] = self.stock_status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        if m.get('SpotDiscount') is not None:
            self.spot_discount = m.get('SpotDiscount')
        if m.get('StockStatus') is not None:
            self.stock_status = m.get('StockStatus')
        return self


class TimeRangeFilter(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        start_time: str = None,
    ):
        self.end_time = end_time
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
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        return self


class UserViewMetric(TeaModel):
    def __init__(
        self,
        cpunode_number: int = None,
        cpuusage_rate: str = None,
        cpu_job_names: List[str] = None,
        cpu_node_names: List[str] = None,
        disk_read_rate: str = None,
        disk_write_rate: str = None,
        gpunode_number: int = None,
        gpuusage_rate: str = None,
        gpu_job_names: List[str] = None,
        gpu_node_names: List[str] = None,
        job_type: str = None,
        memory_usage_rate: str = None,
        network_input_rate: str = None,
        network_output_rate: str = None,
        node_names: List[str] = None,
        request_cpu: int = None,
        request_gpu: int = None,
        request_memory: int = None,
        resource_group_id: str = None,
        total_cpu: int = None,
        total_gpu: int = None,
        total_memory: int = None,
        user_id: str = None,
    ):
        self.cpunode_number = cpunode_number
        self.cpuusage_rate = cpuusage_rate
        self.cpu_job_names = cpu_job_names
        self.cpu_node_names = cpu_node_names
        self.disk_read_rate = disk_read_rate
        self.disk_write_rate = disk_write_rate
        self.gpunode_number = gpunode_number
        self.gpuusage_rate = gpuusage_rate
        self.gpu_job_names = gpu_job_names
        self.gpu_node_names = gpu_node_names
        self.job_type = job_type
        self.memory_usage_rate = memory_usage_rate
        self.network_input_rate = network_input_rate
        self.network_output_rate = network_output_rate
        self.node_names = node_names
        self.request_cpu = request_cpu
        self.request_gpu = request_gpu
        self.request_memory = request_memory
        self.resource_group_id = resource_group_id
        self.total_cpu = total_cpu
        self.total_gpu = total_gpu
        self.total_memory = total_memory
        self.user_id = user_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cpunode_number is not None:
            result['CPUNodeNumber'] = self.cpunode_number
        if self.cpuusage_rate is not None:
            result['CPUUsageRate'] = self.cpuusage_rate
        if self.cpu_job_names is not None:
            result['CpuJobNames'] = self.cpu_job_names
        if self.cpu_node_names is not None:
            result['CpuNodeNames'] = self.cpu_node_names
        if self.disk_read_rate is not None:
            result['DiskReadRate'] = self.disk_read_rate
        if self.disk_write_rate is not None:
            result['DiskWriteRate'] = self.disk_write_rate
        if self.gpunode_number is not None:
            result['GPUNodeNumber'] = self.gpunode_number
        if self.gpuusage_rate is not None:
            result['GPUUsageRate'] = self.gpuusage_rate
        if self.gpu_job_names is not None:
            result['GpuJobNames'] = self.gpu_job_names
        if self.gpu_node_names is not None:
            result['GpuNodeNames'] = self.gpu_node_names
        if self.job_type is not None:
            result['JobType'] = self.job_type
        if self.memory_usage_rate is not None:
            result['MemoryUsageRate'] = self.memory_usage_rate
        if self.network_input_rate is not None:
            result['NetworkInputRate'] = self.network_input_rate
        if self.network_output_rate is not None:
            result['NetworkOutputRate'] = self.network_output_rate
        if self.node_names is not None:
            result['NodeNames'] = self.node_names
        if self.request_cpu is not None:
            result['RequestCPU'] = self.request_cpu
        if self.request_gpu is not None:
            result['RequestGPU'] = self.request_gpu
        if self.request_memory is not None:
            result['RequestMemory'] = self.request_memory
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.total_cpu is not None:
            result['TotalCPU'] = self.total_cpu
        if self.total_gpu is not None:
            result['TotalGPU'] = self.total_gpu
        if self.total_memory is not None:
            result['TotalMemory'] = self.total_memory
        if self.user_id is not None:
            result['UserId'] = self.user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CPUNodeNumber') is not None:
            self.cpunode_number = m.get('CPUNodeNumber')
        if m.get('CPUUsageRate') is not None:
            self.cpuusage_rate = m.get('CPUUsageRate')
        if m.get('CpuJobNames') is not None:
            self.cpu_job_names = m.get('CpuJobNames')
        if m.get('CpuNodeNames') is not None:
            self.cpu_node_names = m.get('CpuNodeNames')
        if m.get('DiskReadRate') is not None:
            self.disk_read_rate = m.get('DiskReadRate')
        if m.get('DiskWriteRate') is not None:
            self.disk_write_rate = m.get('DiskWriteRate')
        if m.get('GPUNodeNumber') is not None:
            self.gpunode_number = m.get('GPUNodeNumber')
        if m.get('GPUUsageRate') is not None:
            self.gpuusage_rate = m.get('GPUUsageRate')
        if m.get('GpuJobNames') is not None:
            self.gpu_job_names = m.get('GpuJobNames')
        if m.get('GpuNodeNames') is not None:
            self.gpu_node_names = m.get('GpuNodeNames')
        if m.get('JobType') is not None:
            self.job_type = m.get('JobType')
        if m.get('MemoryUsageRate') is not None:
            self.memory_usage_rate = m.get('MemoryUsageRate')
        if m.get('NetworkInputRate') is not None:
            self.network_input_rate = m.get('NetworkInputRate')
        if m.get('NetworkOutputRate') is not None:
            self.network_output_rate = m.get('NetworkOutputRate')
        if m.get('NodeNames') is not None:
            self.node_names = m.get('NodeNames')
        if m.get('RequestCPU') is not None:
            self.request_cpu = m.get('RequestCPU')
        if m.get('RequestGPU') is not None:
            self.request_gpu = m.get('RequestGPU')
        if m.get('RequestMemory') is not None:
            self.request_memory = m.get('RequestMemory')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('TotalCPU') is not None:
            self.total_cpu = m.get('TotalCPU')
        if m.get('TotalGPU') is not None:
            self.total_gpu = m.get('TotalGPU')
        if m.get('TotalMemory') is not None:
            self.total_memory = m.get('TotalMemory')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        return self


class CheckInstanceWebTerminalRequest(TeaModel):
    def __init__(
        self,
        check_info: str = None,
    ):
        self.check_info = check_info

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.check_info is not None:
            result['CheckInfo'] = self.check_info
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CheckInfo') is not None:
            self.check_info = m.get('CheckInfo')
        return self


class CheckInstanceWebTerminalResponseBody(TeaModel):
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


class CheckInstanceWebTerminalResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CheckInstanceWebTerminalResponseBody = None,
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
            temp_model = CheckInstanceWebTerminalResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateAI4DDefaultBucketResponseBody(TeaModel):
    def __init__(
        self,
        extranet_endpoint: str = None,
        intranet_endpoint: str = None,
        name: str = None,
        request_id: str = None,
    ):
        self.extranet_endpoint = extranet_endpoint
        self.intranet_endpoint = intranet_endpoint
        self.name = name
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.extranet_endpoint is not None:
            result['ExtranetEndpoint'] = self.extranet_endpoint
        if self.intranet_endpoint is not None:
            result['IntranetEndpoint'] = self.intranet_endpoint
        if self.name is not None:
            result['Name'] = self.name
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ExtranetEndpoint') is not None:
            self.extranet_endpoint = m.get('ExtranetEndpoint')
        if m.get('IntranetEndpoint') is not None:
            self.intranet_endpoint = m.get('IntranetEndpoint')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class CreateAI4DDefaultBucketResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateAI4DDefaultBucketResponseBody = None,
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
            temp_model = CreateAI4DDefaultBucketResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateAI4DSerivceRequest(TeaModel):
    def __init__(
        self,
        inference_spec: Dict[str, Any] = None,
        service_type: str = None,
        workspace_id: str = None,
    ):
        self.inference_spec = inference_spec
        # This parameter is required.
        self.service_type = service_type
        # This parameter is required.
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.inference_spec is not None:
            result['InferenceSpec'] = self.inference_spec
        if self.service_type is not None:
            result['ServiceType'] = self.service_type
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InferenceSpec') is not None:
            self.inference_spec = m.get('InferenceSpec')
        if m.get('ServiceType') is not None:
            self.service_type = m.get('ServiceType')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class CreateAI4DSerivceResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        service_name: str = None,
    ):
        self.request_id = request_id
        self.service_name = service_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.service_name is not None:
            result['ServiceName'] = self.service_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ServiceName') is not None:
            self.service_name = m.get('ServiceName')
        return self


class CreateAI4DSerivceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateAI4DSerivceResponseBody = None,
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
            temp_model = CreateAI4DSerivceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateAlgorithmRequest(TeaModel):
    def __init__(
        self,
        algorithm_description: str = None,
        algorithm_name: str = None,
        display_name: str = None,
        workspace_id: str = None,
    ):
        self.algorithm_description = algorithm_description
        self.algorithm_name = algorithm_name
        self.display_name = display_name
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.algorithm_description is not None:
            result['AlgorithmDescription'] = self.algorithm_description
        if self.algorithm_name is not None:
            result['AlgorithmName'] = self.algorithm_name
        if self.display_name is not None:
            result['DisplayName'] = self.display_name
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AlgorithmDescription') is not None:
            self.algorithm_description = m.get('AlgorithmDescription')
        if m.get('AlgorithmName') is not None:
            self.algorithm_name = m.get('AlgorithmName')
        if m.get('DisplayName') is not None:
            self.display_name = m.get('DisplayName')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class CreateAlgorithmResponseBody(TeaModel):
    def __init__(
        self,
        algorithm_id: str = None,
        request_id: str = None,
    ):
        self.algorithm_id = algorithm_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.algorithm_id is not None:
            result['AlgorithmId'] = self.algorithm_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AlgorithmId') is not None:
            self.algorithm_id = m.get('AlgorithmId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class CreateAlgorithmResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateAlgorithmResponseBody = None,
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
            temp_model = CreateAlgorithmResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateAlgorithmVersionRequest(TeaModel):
    def __init__(
        self,
        algorithm_spec: AlgorithmSpec = None,
    ):
        self.algorithm_spec = algorithm_spec

    def validate(self):
        if self.algorithm_spec:
            self.algorithm_spec.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.algorithm_spec is not None:
            result['AlgorithmSpec'] = self.algorithm_spec.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AlgorithmSpec') is not None:
            temp_model = AlgorithmSpec()
            self.algorithm_spec = temp_model.from_map(m['AlgorithmSpec'])
        return self


class CreateAlgorithmVersionShrinkRequest(TeaModel):
    def __init__(
        self,
        algorithm_spec_shrink: str = None,
    ):
        self.algorithm_spec_shrink = algorithm_spec_shrink

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.algorithm_spec_shrink is not None:
            result['AlgorithmSpec'] = self.algorithm_spec_shrink
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AlgorithmSpec') is not None:
            self.algorithm_spec_shrink = m.get('AlgorithmSpec')
        return self


class CreateAlgorithmVersionResponseBody(TeaModel):
    def __init__(
        self,
        algorithm_id: str = None,
        algorithm_version: str = None,
    ):
        self.algorithm_id = algorithm_id
        self.algorithm_version = algorithm_version

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.algorithm_id is not None:
            result['AlgorithmId'] = self.algorithm_id
        if self.algorithm_version is not None:
            result['AlgorithmVersion'] = self.algorithm_version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AlgorithmId') is not None:
            self.algorithm_id = m.get('AlgorithmId')
        if m.get('AlgorithmVersion') is not None:
            self.algorithm_version = m.get('AlgorithmVersion')
        return self


class CreateAlgorithmVersionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateAlgorithmVersionResponseBody = None,
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
            temp_model = CreateAlgorithmVersionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateComponentRequest(TeaModel):
    def __init__(
        self,
        description: str = None,
        display_name: str = None,
        labels: List[Label] = None,
        name: str = None,
        workspace_id: str = None,
    ):
        # This parameter is required.
        self.description = description
        self.display_name = display_name
        self.labels = labels
        # This parameter is required.
        self.name = name
        # This parameter is required.
        self.workspace_id = workspace_id

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
        if self.description is not None:
            result['Description'] = self.description
        if self.display_name is not None:
            result['DisplayName'] = self.display_name
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        if self.name is not None:
            result['Name'] = self.name
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('DisplayName') is not None:
            self.display_name = m.get('DisplayName')
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = Label()
                self.labels.append(temp_model.from_map(k))
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class CreateComponentResponseBody(TeaModel):
    def __init__(
        self,
        component_id: str = None,
        request_id: str = None,
    ):
        self.component_id = component_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.component_id is not None:
            result['ComponentId'] = self.component_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComponentId') is not None:
            self.component_id = m.get('ComponentId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class CreateComponentResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateComponentResponseBody = None,
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
            temp_model = CreateComponentResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateComponentVersionRequestLabels(TeaModel):
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


class CreateComponentVersionRequest(TeaModel):
    def __init__(
        self,
        config_dir: Location = None,
        description: str = None,
        labels: List[CreateComponentVersionRequestLabels] = None,
        spec: ComponentSpec = None,
        version: str = None,
    ):
        self.config_dir = config_dir
        self.description = description
        self.labels = labels
        self.spec = spec
        self.version = version

    def validate(self):
        if self.config_dir:
            self.config_dir.validate()
        if self.labels:
            for k in self.labels:
                if k:
                    k.validate()
        if self.spec:
            self.spec.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_dir is not None:
            result['ConfigDir'] = self.config_dir.to_map()
        if self.description is not None:
            result['Description'] = self.description
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        if self.spec is not None:
            result['Spec'] = self.spec.to_map()
        if self.version is not None:
            result['Version'] = self.version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConfigDir') is not None:
            temp_model = Location()
            self.config_dir = temp_model.from_map(m['ConfigDir'])
        if m.get('Description') is not None:
            self.description = m.get('Description')
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = CreateComponentVersionRequestLabels()
                self.labels.append(temp_model.from_map(k))
        if m.get('Spec') is not None:
            temp_model = ComponentSpec()
            self.spec = temp_model.from_map(m['Spec'])
        if m.get('Version') is not None:
            self.version = m.get('Version')
        return self


class CreateComponentVersionResponseBody(TeaModel):
    def __init__(
        self,
        instance_job_id: str = None,
        request_id: str = None,
    ):
        self.instance_job_id = instance_job_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instance_job_id is not None:
            result['InstanceJobId'] = self.instance_job_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceJobId') is not None:
            self.instance_job_id = m.get('InstanceJobId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class CreateComponentVersionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateComponentVersionResponseBody = None,
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
            temp_model = CreateComponentVersionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateInstanceWebTerminalResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        web_terminal_id: str = None,
    ):
        self.request_id = request_id
        self.web_terminal_id = web_terminal_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.web_terminal_id is not None:
            result['WebTerminalId'] = self.web_terminal_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('WebTerminalId') is not None:
            self.web_terminal_id = m.get('WebTerminalId')
        return self


class CreateInstanceWebTerminalResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateInstanceWebTerminalResponseBody = None,
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
            temp_model = CreateInstanceWebTerminalResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateQuotaRequest(TeaModel):
    def __init__(
        self,
        allocate_strategy: str = None,
        description: str = None,
        labels: List[Label] = None,
        min: ResourceSpec = None,
        parent_quota_id: str = None,
        queue_strategy: str = None,
        quota_config: QuotaConfig = None,
        quota_name: str = None,
        resource_group_ids: List[str] = None,
        resource_type: str = None,
    ):
        self.allocate_strategy = allocate_strategy
        self.description = description
        self.labels = labels
        self.min = min
        self.parent_quota_id = parent_quota_id
        self.queue_strategy = queue_strategy
        self.quota_config = quota_config
        self.quota_name = quota_name
        self.resource_group_ids = resource_group_ids
        self.resource_type = resource_type

    def validate(self):
        if self.labels:
            for k in self.labels:
                if k:
                    k.validate()
        if self.min:
            self.min.validate()
        if self.quota_config:
            self.quota_config.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.allocate_strategy is not None:
            result['AllocateStrategy'] = self.allocate_strategy
        if self.description is not None:
            result['Description'] = self.description
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        if self.min is not None:
            result['Min'] = self.min.to_map()
        if self.parent_quota_id is not None:
            result['ParentQuotaId'] = self.parent_quota_id
        if self.queue_strategy is not None:
            result['QueueStrategy'] = self.queue_strategy
        if self.quota_config is not None:
            result['QuotaConfig'] = self.quota_config.to_map()
        if self.quota_name is not None:
            result['QuotaName'] = self.quota_name
        if self.resource_group_ids is not None:
            result['ResourceGroupIds'] = self.resource_group_ids
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AllocateStrategy') is not None:
            self.allocate_strategy = m.get('AllocateStrategy')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = Label()
                self.labels.append(temp_model.from_map(k))
        if m.get('Min') is not None:
            temp_model = ResourceSpec()
            self.min = temp_model.from_map(m['Min'])
        if m.get('ParentQuotaId') is not None:
            self.parent_quota_id = m.get('ParentQuotaId')
        if m.get('QueueStrategy') is not None:
            self.queue_strategy = m.get('QueueStrategy')
        if m.get('QuotaConfig') is not None:
            temp_model = QuotaConfig()
            self.quota_config = temp_model.from_map(m['QuotaConfig'])
        if m.get('QuotaName') is not None:
            self.quota_name = m.get('QuotaName')
        if m.get('ResourceGroupIds') is not None:
            self.resource_group_ids = m.get('ResourceGroupIds')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        return self


class CreateQuotaResponseBody(TeaModel):
    def __init__(
        self,
        quota_id: str = None,
        request_id: str = None,
    ):
        # Quota Id
        self.quota_id = quota_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.quota_id is not None:
            result['QuotaId'] = self.quota_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('QuotaId') is not None:
            self.quota_id = m.get('QuotaId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class CreateQuotaResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateQuotaResponseBody = None,
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
            temp_model = CreateQuotaResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateResourceGroupRequestTag(TeaModel):
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


class CreateResourceGroupRequest(TeaModel):
    def __init__(
        self,
        computing_resource_provider: str = None,
        description: str = None,
        name: str = None,
        resource_type: str = None,
        tag: List[CreateResourceGroupRequestTag] = None,
        user_vpc: UserVpc = None,
    ):
        self.computing_resource_provider = computing_resource_provider
        self.description = description
        self.name = name
        self.resource_type = resource_type
        self.tag = tag
        self.user_vpc = user_vpc

    def validate(self):
        if self.tag:
            for k in self.tag:
                if k:
                    k.validate()
        if self.user_vpc:
            self.user_vpc.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.computing_resource_provider is not None:
            result['ComputingResourceProvider'] = self.computing_resource_provider
        if self.description is not None:
            result['Description'] = self.description
        if self.name is not None:
            result['Name'] = self.name
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        result['Tag'] = []
        if self.tag is not None:
            for k in self.tag:
                result['Tag'].append(k.to_map() if k else None)
        if self.user_vpc is not None:
            result['UserVpc'] = self.user_vpc.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComputingResourceProvider') is not None:
            self.computing_resource_provider = m.get('ComputingResourceProvider')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        self.tag = []
        if m.get('Tag') is not None:
            for k in m.get('Tag'):
                temp_model = CreateResourceGroupRequestTag()
                self.tag.append(temp_model.from_map(k))
        if m.get('UserVpc') is not None:
            temp_model = UserVpc()
            self.user_vpc = temp_model.from_map(m['UserVpc'])
        return self


class CreateResourceGroupResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        resource_group_id: str = None,
    ):
        self.request_id = request_id
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.resource_group_id is not None:
            result['ResourceGroupID'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ResourceGroupID') is not None:
            self.resource_group_id = m.get('ResourceGroupID')
        return self


class CreateResourceGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateResourceGroupResponseBody = None,
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
            temp_model = CreateResourceGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateResourceGroupMachineGroupRequestTag(TeaModel):
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


class CreateResourceGroupMachineGroupRequest(TeaModel):
    def __init__(
        self,
        ecs_count: int = None,
        ecs_spec: str = None,
        name: str = None,
        payment_duration: str = None,
        payment_duration_unit: str = None,
        payment_type: str = None,
        tag: List[CreateResourceGroupMachineGroupRequestTag] = None,
    ):
        self.ecs_count = ecs_count
        self.ecs_spec = ecs_spec
        self.name = name
        self.payment_duration = payment_duration
        self.payment_duration_unit = payment_duration_unit
        self.payment_type = payment_type
        self.tag = tag

    def validate(self):
        if self.tag:
            for k in self.tag:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.ecs_count is not None:
            result['EcsCount'] = self.ecs_count
        if self.ecs_spec is not None:
            result['EcsSpec'] = self.ecs_spec
        if self.name is not None:
            result['Name'] = self.name
        if self.payment_duration is not None:
            result['PaymentDuration'] = self.payment_duration
        if self.payment_duration_unit is not None:
            result['PaymentDurationUnit'] = self.payment_duration_unit
        if self.payment_type is not None:
            result['PaymentType'] = self.payment_type
        result['Tag'] = []
        if self.tag is not None:
            for k in self.tag:
                result['Tag'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EcsCount') is not None:
            self.ecs_count = m.get('EcsCount')
        if m.get('EcsSpec') is not None:
            self.ecs_spec = m.get('EcsSpec')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('PaymentDuration') is not None:
            self.payment_duration = m.get('PaymentDuration')
        if m.get('PaymentDurationUnit') is not None:
            self.payment_duration_unit = m.get('PaymentDurationUnit')
        if m.get('PaymentType') is not None:
            self.payment_type = m.get('PaymentType')
        self.tag = []
        if m.get('Tag') is not None:
            for k in m.get('Tag'):
                temp_model = CreateResourceGroupMachineGroupRequestTag()
                self.tag.append(temp_model.from_map(k))
        return self


class CreateResourceGroupMachineGroupResponseBody(TeaModel):
    def __init__(
        self,
        machine_group_id: str = None,
        request_id: str = None,
    ):
        self.machine_group_id = machine_group_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.machine_group_id is not None:
            result['MachineGroupID'] = self.machine_group_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MachineGroupID') is not None:
            self.machine_group_id = m.get('MachineGroupID')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class CreateResourceGroupMachineGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateResourceGroupMachineGroupResponseBody = None,
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
            temp_model = CreateResourceGroupMachineGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateServiceIdentityRoleRequest(TeaModel):
    def __init__(
        self,
        role_name: str = None,
    ):
        self.role_name = role_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.role_name is not None:
            result['RoleName'] = self.role_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RoleName') is not None:
            self.role_name = m.get('RoleName')
        return self


class CreateServiceIdentityRoleResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        role_name: str = None,
    ):
        self.request_id = request_id
        self.role_name = role_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.role_name is not None:
            result['RoleName'] = self.role_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('RoleName') is not None:
            self.role_name = m.get('RoleName')
        return self


class CreateServiceIdentityRoleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateServiceIdentityRoleResponseBody = None,
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
            temp_model = CreateServiceIdentityRoleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateTrainingJobRequestComputeResourceInstanceSpec(TeaModel):
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


class CreateTrainingJobRequestComputeResourceSpotSpec(TeaModel):
    def __init__(
        self,
        spot_discount_limit: float = None,
        spot_strategy: str = None,
    ):
        self.spot_discount_limit = spot_discount_limit
        self.spot_strategy = spot_strategy

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.spot_discount_limit is not None:
            result['SpotDiscountLimit'] = self.spot_discount_limit
        if self.spot_strategy is not None:
            result['SpotStrategy'] = self.spot_strategy
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SpotDiscountLimit') is not None:
            self.spot_discount_limit = m.get('SpotDiscountLimit')
        if m.get('SpotStrategy') is not None:
            self.spot_strategy = m.get('SpotStrategy')
        return self


class CreateTrainingJobRequestComputeResource(TeaModel):
    def __init__(
        self,
        ecs_count: int = None,
        ecs_spec: str = None,
        instance_count: int = None,
        instance_spec: CreateTrainingJobRequestComputeResourceInstanceSpec = None,
        resource_id: str = None,
        spot_spec: CreateTrainingJobRequestComputeResourceSpotSpec = None,
        use_spot_instance: bool = None,
    ):
        self.ecs_count = ecs_count
        self.ecs_spec = ecs_spec
        self.instance_count = instance_count
        self.instance_spec = instance_spec
        self.resource_id = resource_id
        self.spot_spec = spot_spec
        self.use_spot_instance = use_spot_instance

    def validate(self):
        if self.instance_spec:
            self.instance_spec.validate()
        if self.spot_spec:
            self.spot_spec.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.ecs_count is not None:
            result['EcsCount'] = self.ecs_count
        if self.ecs_spec is not None:
            result['EcsSpec'] = self.ecs_spec
        if self.instance_count is not None:
            result['InstanceCount'] = self.instance_count
        if self.instance_spec is not None:
            result['InstanceSpec'] = self.instance_spec.to_map()
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.spot_spec is not None:
            result['SpotSpec'] = self.spot_spec.to_map()
        if self.use_spot_instance is not None:
            result['UseSpotInstance'] = self.use_spot_instance
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EcsCount') is not None:
            self.ecs_count = m.get('EcsCount')
        if m.get('EcsSpec') is not None:
            self.ecs_spec = m.get('EcsSpec')
        if m.get('InstanceCount') is not None:
            self.instance_count = m.get('InstanceCount')
        if m.get('InstanceSpec') is not None:
            temp_model = CreateTrainingJobRequestComputeResourceInstanceSpec()
            self.instance_spec = temp_model.from_map(m['InstanceSpec'])
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('SpotSpec') is not None:
            temp_model = CreateTrainingJobRequestComputeResourceSpotSpec()
            self.spot_spec = temp_model.from_map(m['SpotSpec'])
        if m.get('UseSpotInstance') is not None:
            self.use_spot_instance = m.get('UseSpotInstance')
        return self


class CreateTrainingJobRequestExperimentConfig(TeaModel):
    def __init__(
        self,
        experiment_id: str = None,
    ):
        self.experiment_id = experiment_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.experiment_id is not None:
            result['ExperimentId'] = self.experiment_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ExperimentId') is not None:
            self.experiment_id = m.get('ExperimentId')
        return self


class CreateTrainingJobRequestHyperParameters(TeaModel):
    def __init__(
        self,
        name: str = None,
        value: str = None,
    ):
        self.name = name
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class CreateTrainingJobRequestInputChannels(TeaModel):
    def __init__(
        self,
        dataset_id: str = None,
        input_uri: str = None,
        name: str = None,
    ):
        self.dataset_id = dataset_id
        self.input_uri = input_uri
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.dataset_id is not None:
            result['DatasetId'] = self.dataset_id
        if self.input_uri is not None:
            result['InputUri'] = self.input_uri
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DatasetId') is not None:
            self.dataset_id = m.get('DatasetId')
        if m.get('InputUri') is not None:
            self.input_uri = m.get('InputUri')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class CreateTrainingJobRequestLabels(TeaModel):
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


class CreateTrainingJobRequestOutputChannels(TeaModel):
    def __init__(
        self,
        dataset_id: str = None,
        name: str = None,
        output_uri: str = None,
    ):
        self.dataset_id = dataset_id
        self.name = name
        self.output_uri = output_uri

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.dataset_id is not None:
            result['DatasetId'] = self.dataset_id
        if self.name is not None:
            result['Name'] = self.name
        if self.output_uri is not None:
            result['OutputUri'] = self.output_uri
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DatasetId') is not None:
            self.dataset_id = m.get('DatasetId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('OutputUri') is not None:
            self.output_uri = m.get('OutputUri')
        return self


class CreateTrainingJobRequestScheduler(TeaModel):
    def __init__(
        self,
        max_running_time_in_seconds: int = None,
    ):
        self.max_running_time_in_seconds = max_running_time_in_seconds

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.max_running_time_in_seconds is not None:
            result['MaxRunningTimeInSeconds'] = self.max_running_time_in_seconds
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MaxRunningTimeInSeconds') is not None:
            self.max_running_time_in_seconds = m.get('MaxRunningTimeInSeconds')
        return self


class CreateTrainingJobRequestSettings(TeaModel):
    def __init__(
        self,
        aimaster_type: str = None,
        enable_error_monitoring_in_aimaster: bool = None,
        error_monitoring_args: str = None,
        priority: int = None,
    ):
        self.aimaster_type = aimaster_type
        self.enable_error_monitoring_in_aimaster = enable_error_monitoring_in_aimaster
        self.error_monitoring_args = error_monitoring_args
        self.priority = priority

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.aimaster_type is not None:
            result['AIMasterType'] = self.aimaster_type
        if self.enable_error_monitoring_in_aimaster is not None:
            result['EnableErrorMonitoringInAIMaster'] = self.enable_error_monitoring_in_aimaster
        if self.error_monitoring_args is not None:
            result['ErrorMonitoringArgs'] = self.error_monitoring_args
        if self.priority is not None:
            result['Priority'] = self.priority
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AIMasterType') is not None:
            self.aimaster_type = m.get('AIMasterType')
        if m.get('EnableErrorMonitoringInAIMaster') is not None:
            self.enable_error_monitoring_in_aimaster = m.get('EnableErrorMonitoringInAIMaster')
        if m.get('ErrorMonitoringArgs') is not None:
            self.error_monitoring_args = m.get('ErrorMonitoringArgs')
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        return self


class CreateTrainingJobRequestUserVpc(TeaModel):
    def __init__(
        self,
        default_route: str = None,
        extended_cidrs: List[str] = None,
        security_group_id: str = None,
        switch_id: str = None,
        vpc_id: str = None,
    ):
        self.default_route = default_route
        self.extended_cidrs = extended_cidrs
        self.security_group_id = security_group_id
        self.switch_id = switch_id
        self.vpc_id = vpc_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.default_route is not None:
            result['DefaultRoute'] = self.default_route
        if self.extended_cidrs is not None:
            result['ExtendedCIDRs'] = self.extended_cidrs
        if self.security_group_id is not None:
            result['SecurityGroupId'] = self.security_group_id
        if self.switch_id is not None:
            result['SwitchId'] = self.switch_id
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DefaultRoute') is not None:
            self.default_route = m.get('DefaultRoute')
        if m.get('ExtendedCIDRs') is not None:
            self.extended_cidrs = m.get('ExtendedCIDRs')
        if m.get('SecurityGroupId') is not None:
            self.security_group_id = m.get('SecurityGroupId')
        if m.get('SwitchId') is not None:
            self.switch_id = m.get('SwitchId')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        return self


class CreateTrainingJobRequest(TeaModel):
    def __init__(
        self,
        algorithm_name: str = None,
        algorithm_provider: str = None,
        algorithm_spec: AlgorithmSpec = None,
        algorithm_version: str = None,
        code_dir: Location = None,
        compute_resource: CreateTrainingJobRequestComputeResource = None,
        environments: Dict[str, str] = None,
        experiment_config: CreateTrainingJobRequestExperimentConfig = None,
        hyper_parameters: List[CreateTrainingJobRequestHyperParameters] = None,
        input_channels: List[CreateTrainingJobRequestInputChannels] = None,
        labels: List[CreateTrainingJobRequestLabels] = None,
        output_channels: List[CreateTrainingJobRequestOutputChannels] = None,
        python_requirements: List[str] = None,
        role_arn: str = None,
        scheduler: CreateTrainingJobRequestScheduler = None,
        settings: CreateTrainingJobRequestSettings = None,
        training_job_description: str = None,
        training_job_name: str = None,
        user_vpc: CreateTrainingJobRequestUserVpc = None,
        workspace_id: str = None,
        resource_type: str = None,
    ):
        self.algorithm_name = algorithm_name
        self.algorithm_provider = algorithm_provider
        self.algorithm_spec = algorithm_spec
        self.algorithm_version = algorithm_version
        self.code_dir = code_dir
        self.compute_resource = compute_resource
        self.environments = environments
        self.experiment_config = experiment_config
        self.hyper_parameters = hyper_parameters
        self.input_channels = input_channels
        self.labels = labels
        self.output_channels = output_channels
        self.python_requirements = python_requirements
        self.role_arn = role_arn
        self.scheduler = scheduler
        self.settings = settings
        self.training_job_description = training_job_description
        # This parameter is required.
        self.training_job_name = training_job_name
        self.user_vpc = user_vpc
        # This parameter is required.
        self.workspace_id = workspace_id
        self.resource_type = resource_type

    def validate(self):
        if self.algorithm_spec:
            self.algorithm_spec.validate()
        if self.code_dir:
            self.code_dir.validate()
        if self.compute_resource:
            self.compute_resource.validate()
        if self.experiment_config:
            self.experiment_config.validate()
        if self.hyper_parameters:
            for k in self.hyper_parameters:
                if k:
                    k.validate()
        if self.input_channels:
            for k in self.input_channels:
                if k:
                    k.validate()
        if self.labels:
            for k in self.labels:
                if k:
                    k.validate()
        if self.output_channels:
            for k in self.output_channels:
                if k:
                    k.validate()
        if self.scheduler:
            self.scheduler.validate()
        if self.settings:
            self.settings.validate()
        if self.user_vpc:
            self.user_vpc.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.algorithm_name is not None:
            result['AlgorithmName'] = self.algorithm_name
        if self.algorithm_provider is not None:
            result['AlgorithmProvider'] = self.algorithm_provider
        if self.algorithm_spec is not None:
            result['AlgorithmSpec'] = self.algorithm_spec.to_map()
        if self.algorithm_version is not None:
            result['AlgorithmVersion'] = self.algorithm_version
        if self.code_dir is not None:
            result['CodeDir'] = self.code_dir.to_map()
        if self.compute_resource is not None:
            result['ComputeResource'] = self.compute_resource.to_map()
        if self.environments is not None:
            result['Environments'] = self.environments
        if self.experiment_config is not None:
            result['ExperimentConfig'] = self.experiment_config.to_map()
        result['HyperParameters'] = []
        if self.hyper_parameters is not None:
            for k in self.hyper_parameters:
                result['HyperParameters'].append(k.to_map() if k else None)
        result['InputChannels'] = []
        if self.input_channels is not None:
            for k in self.input_channels:
                result['InputChannels'].append(k.to_map() if k else None)
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        result['OutputChannels'] = []
        if self.output_channels is not None:
            for k in self.output_channels:
                result['OutputChannels'].append(k.to_map() if k else None)
        if self.python_requirements is not None:
            result['PythonRequirements'] = self.python_requirements
        if self.role_arn is not None:
            result['RoleArn'] = self.role_arn
        if self.scheduler is not None:
            result['Scheduler'] = self.scheduler.to_map()
        if self.settings is not None:
            result['Settings'] = self.settings.to_map()
        if self.training_job_description is not None:
            result['TrainingJobDescription'] = self.training_job_description
        if self.training_job_name is not None:
            result['TrainingJobName'] = self.training_job_name
        if self.user_vpc is not None:
            result['UserVpc'] = self.user_vpc.to_map()
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AlgorithmName') is not None:
            self.algorithm_name = m.get('AlgorithmName')
        if m.get('AlgorithmProvider') is not None:
            self.algorithm_provider = m.get('AlgorithmProvider')
        if m.get('AlgorithmSpec') is not None:
            temp_model = AlgorithmSpec()
            self.algorithm_spec = temp_model.from_map(m['AlgorithmSpec'])
        if m.get('AlgorithmVersion') is not None:
            self.algorithm_version = m.get('AlgorithmVersion')
        if m.get('CodeDir') is not None:
            temp_model = Location()
            self.code_dir = temp_model.from_map(m['CodeDir'])
        if m.get('ComputeResource') is not None:
            temp_model = CreateTrainingJobRequestComputeResource()
            self.compute_resource = temp_model.from_map(m['ComputeResource'])
        if m.get('Environments') is not None:
            self.environments = m.get('Environments')
        if m.get('ExperimentConfig') is not None:
            temp_model = CreateTrainingJobRequestExperimentConfig()
            self.experiment_config = temp_model.from_map(m['ExperimentConfig'])
        self.hyper_parameters = []
        if m.get('HyperParameters') is not None:
            for k in m.get('HyperParameters'):
                temp_model = CreateTrainingJobRequestHyperParameters()
                self.hyper_parameters.append(temp_model.from_map(k))
        self.input_channels = []
        if m.get('InputChannels') is not None:
            for k in m.get('InputChannels'):
                temp_model = CreateTrainingJobRequestInputChannels()
                self.input_channels.append(temp_model.from_map(k))
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = CreateTrainingJobRequestLabels()
                self.labels.append(temp_model.from_map(k))
        self.output_channels = []
        if m.get('OutputChannels') is not None:
            for k in m.get('OutputChannels'):
                temp_model = CreateTrainingJobRequestOutputChannels()
                self.output_channels.append(temp_model.from_map(k))
        if m.get('PythonRequirements') is not None:
            self.python_requirements = m.get('PythonRequirements')
        if m.get('RoleArn') is not None:
            self.role_arn = m.get('RoleArn')
        if m.get('Scheduler') is not None:
            temp_model = CreateTrainingJobRequestScheduler()
            self.scheduler = temp_model.from_map(m['Scheduler'])
        if m.get('Settings') is not None:
            temp_model = CreateTrainingJobRequestSettings()
            self.settings = temp_model.from_map(m['Settings'])
        if m.get('TrainingJobDescription') is not None:
            self.training_job_description = m.get('TrainingJobDescription')
        if m.get('TrainingJobName') is not None:
            self.training_job_name = m.get('TrainingJobName')
        if m.get('UserVpc') is not None:
            temp_model = CreateTrainingJobRequestUserVpc()
            self.user_vpc = temp_model.from_map(m['UserVpc'])
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        return self


class CreateTrainingJobResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        training_job_id: str = None,
    ):
        self.request_id = request_id
        self.training_job_id = training_job_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.training_job_id is not None:
            result['TrainingJobId'] = self.training_job_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TrainingJobId') is not None:
            self.training_job_id = m.get('TrainingJobId')
        return self


class CreateTrainingJobResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateTrainingJobResponseBody = None,
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
            temp_model = CreateTrainingJobResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteAlgorithmResponseBody(TeaModel):
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
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class DeleteAlgorithmResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteAlgorithmResponseBody = None,
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
            temp_model = DeleteAlgorithmResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteAlgorithmVersionResponseBody(TeaModel):
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


class DeleteAlgorithmVersionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteAlgorithmVersionResponseBody = None,
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
            temp_model = DeleteAlgorithmVersionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteComponentResponseBody(TeaModel):
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


class DeleteComponentResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteComponentResponseBody = None,
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
            temp_model = DeleteComponentResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteComponentVersionResponseBody(TeaModel):
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


class DeleteComponentVersionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteComponentVersionResponseBody = None,
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
            temp_model = DeleteComponentVersionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteComponentVersionSnapshotResponseBody(TeaModel):
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


class DeleteComponentVersionSnapshotResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteComponentVersionSnapshotResponseBody = None,
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
            temp_model = DeleteComponentVersionSnapshotResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteMachineGroupResponseBody(TeaModel):
    def __init__(
        self,
        machine_group_id: str = None,
        request_id: str = None,
    ):
        self.machine_group_id = machine_group_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.machine_group_id is not None:
            result['MachineGroupID'] = self.machine_group_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MachineGroupID') is not None:
            self.machine_group_id = m.get('MachineGroupID')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteMachineGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteMachineGroupResponseBody = None,
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
            temp_model = DeleteMachineGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteQuotaResponseBody(TeaModel):
    def __init__(
        self,
        quota_id: str = None,
        request_id: str = None,
    ):
        # Quota Id
        self.quota_id = quota_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.quota_id is not None:
            result['QuotaId'] = self.quota_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('QuotaId') is not None:
            self.quota_id = m.get('QuotaId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteQuotaResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteQuotaResponseBody = None,
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
            temp_model = DeleteQuotaResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteQuotaLabelsRequest(TeaModel):
    def __init__(
        self,
        keys: str = None,
    ):
        self.keys = keys

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.keys is not None:
            result['Keys'] = self.keys
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Keys') is not None:
            self.keys = m.get('Keys')
        return self


class DeleteQuotaLabelsResponseBody(TeaModel):
    def __init__(
        self,
        quota_id: str = None,
        request_id: str = None,
    ):
        self.quota_id = quota_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.quota_id is not None:
            result['QuotaId'] = self.quota_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('QuotaId') is not None:
            self.quota_id = m.get('QuotaId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteQuotaLabelsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteQuotaLabelsResponseBody = None,
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
            temp_model = DeleteQuotaLabelsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteResourceGroupResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        resource_group_id: str = None,
    ):
        self.request_id = request_id
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.resource_group_id is not None:
            result['ResourceGroupID'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ResourceGroupID') is not None:
            self.resource_group_id = m.get('ResourceGroupID')
        return self


class DeleteResourceGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteResourceGroupResponseBody = None,
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
            temp_model = DeleteResourceGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteResourceGroupMachineGroupResponseBody(TeaModel):
    def __init__(
        self,
        machine_group_id: str = None,
        request_id: str = None,
    ):
        self.machine_group_id = machine_group_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.machine_group_id is not None:
            result['MachineGroupID'] = self.machine_group_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MachineGroupID') is not None:
            self.machine_group_id = m.get('MachineGroupID')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteResourceGroupMachineGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteResourceGroupMachineGroupResponseBody = None,
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
            temp_model = DeleteResourceGroupMachineGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteTrainingJobResponseBody(TeaModel):
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


class DeleteTrainingJobResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteTrainingJobResponseBody = None,
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
            temp_model = DeleteTrainingJobResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteTrainingJobLabelsRequest(TeaModel):
    def __init__(
        self,
        keys: str = None,
    ):
        # This parameter is required.
        self.keys = keys

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.keys is not None:
            result['Keys'] = self.keys
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Keys') is not None:
            self.keys = m.get('Keys')
        return self


class DeleteTrainingJobLabelsResponseBody(TeaModel):
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


class DeleteTrainingJobLabelsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteTrainingJobLabelsResponseBody = None,
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
            temp_model = DeleteTrainingJobLabelsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetAI4DDefaultBucketResponseBody(TeaModel):
    def __init__(
        self,
        extranet_endpoint: str = None,
        intranet_endpoint: str = None,
        name: str = None,
        request_id: str = None,
    ):
        self.extranet_endpoint = extranet_endpoint
        self.intranet_endpoint = intranet_endpoint
        self.name = name
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.extranet_endpoint is not None:
            result['ExtranetEndpoint'] = self.extranet_endpoint
        if self.intranet_endpoint is not None:
            result['IntranetEndpoint'] = self.intranet_endpoint
        if self.name is not None:
            result['Name'] = self.name
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ExtranetEndpoint') is not None:
            self.extranet_endpoint = m.get('ExtranetEndpoint')
        if m.get('IntranetEndpoint') is not None:
            self.intranet_endpoint = m.get('IntranetEndpoint')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class GetAI4DDefaultBucketResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetAI4DDefaultBucketResponseBody = None,
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
            temp_model = GetAI4DDefaultBucketResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetAlgorithmResponseBody(TeaModel):
    def __init__(
        self,
        algorithm_description: str = None,
        algorithm_id: str = None,
        algorithm_name: str = None,
        algorithm_provider: str = None,
        display_name: str = None,
        gmt_create_time: str = None,
        gmt_modified_time: str = None,
        request_id: str = None,
        tenant_id: str = None,
        user_id: str = None,
        workspace_id: str = None,
    ):
        self.algorithm_description = algorithm_description
        self.algorithm_id = algorithm_id
        self.algorithm_name = algorithm_name
        self.algorithm_provider = algorithm_provider
        self.display_name = display_name
        self.gmt_create_time = gmt_create_time
        self.gmt_modified_time = gmt_modified_time
        self.request_id = request_id
        self.tenant_id = tenant_id
        self.user_id = user_id
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.algorithm_description is not None:
            result['AlgorithmDescription'] = self.algorithm_description
        if self.algorithm_id is not None:
            result['AlgorithmId'] = self.algorithm_id
        if self.algorithm_name is not None:
            result['AlgorithmName'] = self.algorithm_name
        if self.algorithm_provider is not None:
            result['AlgorithmProvider'] = self.algorithm_provider
        if self.display_name is not None:
            result['DisplayName'] = self.display_name
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.tenant_id is not None:
            result['TenantId'] = self.tenant_id
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AlgorithmDescription') is not None:
            self.algorithm_description = m.get('AlgorithmDescription')
        if m.get('AlgorithmId') is not None:
            self.algorithm_id = m.get('AlgorithmId')
        if m.get('AlgorithmName') is not None:
            self.algorithm_name = m.get('AlgorithmName')
        if m.get('AlgorithmProvider') is not None:
            self.algorithm_provider = m.get('AlgorithmProvider')
        if m.get('DisplayName') is not None:
            self.display_name = m.get('DisplayName')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TenantId') is not None:
            self.tenant_id = m.get('TenantId')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class GetAlgorithmResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetAlgorithmResponseBody = None,
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
            temp_model = GetAlgorithmResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetAlgorithmVersionResponseBody(TeaModel):
    def __init__(
        self,
        algorithm_id: str = None,
        algorithm_name: str = None,
        algorithm_provider: str = None,
        algorithm_spec: AlgorithmSpec = None,
        algorithm_version: str = None,
        gmt_create_time: str = None,
        gmt_modified_time: str = None,
        tenant_id: str = None,
        user_id: str = None,
    ):
        self.algorithm_id = algorithm_id
        self.algorithm_name = algorithm_name
        self.algorithm_provider = algorithm_provider
        self.algorithm_spec = algorithm_spec
        self.algorithm_version = algorithm_version
        self.gmt_create_time = gmt_create_time
        self.gmt_modified_time = gmt_modified_time
        self.tenant_id = tenant_id
        self.user_id = user_id

    def validate(self):
        if self.algorithm_spec:
            self.algorithm_spec.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.algorithm_id is not None:
            result['AlgorithmId'] = self.algorithm_id
        if self.algorithm_name is not None:
            result['AlgorithmName'] = self.algorithm_name
        if self.algorithm_provider is not None:
            result['AlgorithmProvider'] = self.algorithm_provider
        if self.algorithm_spec is not None:
            result['AlgorithmSpec'] = self.algorithm_spec.to_map()
        if self.algorithm_version is not None:
            result['AlgorithmVersion'] = self.algorithm_version
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.tenant_id is not None:
            result['TenantId'] = self.tenant_id
        if self.user_id is not None:
            result['UserId'] = self.user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AlgorithmId') is not None:
            self.algorithm_id = m.get('AlgorithmId')
        if m.get('AlgorithmName') is not None:
            self.algorithm_name = m.get('AlgorithmName')
        if m.get('AlgorithmProvider') is not None:
            self.algorithm_provider = m.get('AlgorithmProvider')
        if m.get('AlgorithmSpec') is not None:
            temp_model = AlgorithmSpec()
            self.algorithm_spec = temp_model.from_map(m['AlgorithmSpec'])
        if m.get('AlgorithmVersion') is not None:
            self.algorithm_version = m.get('AlgorithmVersion')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('TenantId') is not None:
            self.tenant_id = m.get('TenantId')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        return self


class GetAlgorithmVersionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetAlgorithmVersionResponseBody = None,
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
            temp_model = GetAlgorithmVersionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetComponentResponseBodyVersions(TeaModel):
    def __init__(
        self,
        gmt_create_time: str = None,
        snapshot_id: str = None,
        status: str = None,
        version: str = None,
    ):
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.gmt_create_time = gmt_create_time
        self.snapshot_id = snapshot_id
        self.status = status
        self.version = version

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.snapshot_id is not None:
            result['SnapshotId'] = self.snapshot_id
        if self.status is not None:
            result['Status'] = self.status
        if self.version is not None:
            result['Version'] = self.version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('SnapshotId') is not None:
            self.snapshot_id = m.get('SnapshotId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        return self


class GetComponentResponseBody(TeaModel):
    def __init__(
        self,
        component_id: str = None,
        description: str = None,
        display_name: str = None,
        gmt_create_time: str = None,
        gmt_modified_time: str = None,
        labels: List[Label] = None,
        name: str = None,
        provider: str = None,
        request_id: str = None,
        tenant_id: str = None,
        user_id: str = None,
        versions: List[GetComponentResponseBodyVersions] = None,
        workspace_id: str = None,
    ):
        self.component_id = component_id
        self.description = description
        self.display_name = display_name
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.gmt_create_time = gmt_create_time
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.gmt_modified_time = gmt_modified_time
        self.labels = labels
        self.name = name
        self.provider = provider
        self.request_id = request_id
        self.tenant_id = tenant_id
        self.user_id = user_id
        self.versions = versions
        self.workspace_id = workspace_id

    def validate(self):
        if self.labels:
            for k in self.labels:
                if k:
                    k.validate()
        if self.versions:
            for k in self.versions:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.component_id is not None:
            result['ComponentId'] = self.component_id
        if self.description is not None:
            result['Description'] = self.description
        if self.display_name is not None:
            result['DisplayName'] = self.display_name
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        if self.name is not None:
            result['Name'] = self.name
        if self.provider is not None:
            result['Provider'] = self.provider
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.tenant_id is not None:
            result['TenantId'] = self.tenant_id
        if self.user_id is not None:
            result['UserId'] = self.user_id
        result['Versions'] = []
        if self.versions is not None:
            for k in self.versions:
                result['Versions'].append(k.to_map() if k else None)
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComponentId') is not None:
            self.component_id = m.get('ComponentId')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('DisplayName') is not None:
            self.display_name = m.get('DisplayName')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = Label()
                self.labels.append(temp_model.from_map(k))
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Provider') is not None:
            self.provider = m.get('Provider')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TenantId') is not None:
            self.tenant_id = m.get('TenantId')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        self.versions = []
        if m.get('Versions') is not None:
            for k in m.get('Versions'):
                temp_model = GetComponentResponseBodyVersions()
                self.versions.append(temp_model.from_map(k))
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class GetComponentResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetComponentResponseBody = None,
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
            temp_model = GetComponentResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetComponentVersionResponseBody(TeaModel):
    def __init__(
        self,
        description: str = None,
        gmt_create_time: str = None,
        gmt_modified_time: str = None,
        labels: List[Label] = None,
        name: str = None,
        provider: str = None,
        request_id: str = None,
        snapshot_id: str = None,
        spec: ComponentSpec = None,
        tenant_id: str = None,
        user_id: str = None,
        version: str = None,
        workspace_id: str = None,
    ):
        self.description = description
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.gmt_create_time = gmt_create_time
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.gmt_modified_time = gmt_modified_time
        self.labels = labels
        self.name = name
        self.provider = provider
        self.request_id = request_id
        self.snapshot_id = snapshot_id
        self.spec = spec
        self.tenant_id = tenant_id
        self.user_id = user_id
        self.version = version
        self.workspace_id = workspace_id

    def validate(self):
        if self.labels:
            for k in self.labels:
                if k:
                    k.validate()
        if self.spec:
            self.spec.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.description is not None:
            result['Description'] = self.description
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        if self.name is not None:
            result['Name'] = self.name
        if self.provider is not None:
            result['Provider'] = self.provider
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.snapshot_id is not None:
            result['SnapshotId'] = self.snapshot_id
        if self.spec is not None:
            result['Spec'] = self.spec.to_map()
        if self.tenant_id is not None:
            result['TenantId'] = self.tenant_id
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.version is not None:
            result['Version'] = self.version
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = Label()
                self.labels.append(temp_model.from_map(k))
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Provider') is not None:
            self.provider = m.get('Provider')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('SnapshotId') is not None:
            self.snapshot_id = m.get('SnapshotId')
        if m.get('Spec') is not None:
            temp_model = ComponentSpec()
            self.spec = temp_model.from_map(m['Spec'])
        if m.get('TenantId') is not None:
            self.tenant_id = m.get('TenantId')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class GetComponentVersionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetComponentVersionResponseBody = None,
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
            temp_model = GetComponentVersionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetComponentVersionSnapshotResponseBody(TeaModel):
    def __init__(
        self,
        component_id: str = None,
        gmt_create_time: str = None,
        gmt_modified_time: str = None,
        is_current_version: bool = None,
        request_id: str = None,
        snapshot_id: str = None,
        tenant_id: str = None,
        user_id: str = None,
        version: str = None,
        workspace_id: str = None,
    ):
        self.component_id = component_id
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.gmt_create_time = gmt_create_time
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.gmt_modified_time = gmt_modified_time
        self.is_current_version = is_current_version
        self.request_id = request_id
        self.snapshot_id = snapshot_id
        self.tenant_id = tenant_id
        self.user_id = user_id
        self.version = version
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.component_id is not None:
            result['ComponentId'] = self.component_id
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.is_current_version is not None:
            result['IsCurrentVersion'] = self.is_current_version
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.snapshot_id is not None:
            result['SnapshotId'] = self.snapshot_id
        if self.tenant_id is not None:
            result['TenantId'] = self.tenant_id
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.version is not None:
            result['Version'] = self.version
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComponentId') is not None:
            self.component_id = m.get('ComponentId')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('IsCurrentVersion') is not None:
            self.is_current_version = m.get('IsCurrentVersion')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('SnapshotId') is not None:
            self.snapshot_id = m.get('SnapshotId')
        if m.get('TenantId') is not None:
            self.tenant_id = m.get('TenantId')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class GetComponentVersionSnapshotResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetComponentVersionSnapshotResponseBody = None,
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
            temp_model = GetComponentVersionSnapshotResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetInstanceJobResponseBody(TeaModel):
    def __init__(
        self,
        creator: str = None,
        gmt_create_time: str = None,
        instance_id: str = None,
        instance_job_id: str = None,
        instance_job_type: str = None,
        reason_code: str = None,
        reason_message: str = None,
        request_id: str = None,
        status: str = None,
        workspace_id: str = None,
    ):
        self.creator = creator
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.gmt_create_time = gmt_create_time
        self.instance_id = instance_id
        self.instance_job_id = instance_job_id
        self.instance_job_type = instance_job_type
        self.reason_code = reason_code
        self.reason_message = reason_message
        self.request_id = request_id
        self.status = status
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.creator is not None:
            result['Creator'] = self.creator
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.instance_job_id is not None:
            result['InstanceJobId'] = self.instance_job_id
        if self.instance_job_type is not None:
            result['InstanceJobType'] = self.instance_job_type
        if self.reason_code is not None:
            result['ReasonCode'] = self.reason_code
        if self.reason_message is not None:
            result['ReasonMessage'] = self.reason_message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.status is not None:
            result['Status'] = self.status
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Creator') is not None:
            self.creator = m.get('Creator')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('InstanceJobId') is not None:
            self.instance_job_id = m.get('InstanceJobId')
        if m.get('InstanceJobType') is not None:
            self.instance_job_type = m.get('InstanceJobType')
        if m.get('ReasonCode') is not None:
            self.reason_code = m.get('ReasonCode')
        if m.get('ReasonMessage') is not None:
            self.reason_message = m.get('ReasonMessage')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class GetInstanceJobResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetInstanceJobResponseBody = None,
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
            temp_model = GetInstanceJobResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetJobViewMetricsRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        page_number: int = None,
        page_size: int = None,
        sort_by: str = None,
        start_time: str = None,
        time_step: str = None,
        workspace_id: str = None,
    ):
        self.end_time = end_time
        self.page_number = page_number
        self.page_size = page_size
        self.sort_by = sort_by
        self.start_time = start_time
        self.time_step = time_step
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.time_step is not None:
            result['TimeStep'] = self.time_step
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('TimeStep') is not None:
            self.time_step = m.get('TimeStep')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class GetJobViewMetricsResponseBody(TeaModel):
    def __init__(
        self,
        job_metrics: List[JobViewMetric] = None,
        request_id: str = None,
        summary: JobViewMetric = None,
        total: int = None,
    ):
        self.job_metrics = job_metrics
        self.request_id = request_id
        self.summary = summary
        self.total = total

    def validate(self):
        if self.job_metrics:
            for k in self.job_metrics:
                if k:
                    k.validate()
        if self.summary:
            self.summary.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['JobMetrics'] = []
        if self.job_metrics is not None:
            for k in self.job_metrics:
                result['JobMetrics'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.summary is not None:
            result['Summary'] = self.summary.to_map()
        if self.total is not None:
            result['Total'] = self.total
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.job_metrics = []
        if m.get('JobMetrics') is not None:
            for k in m.get('JobMetrics'):
                temp_model = JobViewMetric()
                self.job_metrics.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Summary') is not None:
            temp_model = JobViewMetric()
            self.summary = temp_model.from_map(m['Summary'])
        if m.get('Total') is not None:
            self.total = m.get('Total')
        return self


class GetJobViewMetricsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetJobViewMetricsResponseBody = None,
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
            temp_model = GetJobViewMetricsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetJobsStatisticsByQuotaRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        start_time: str = None,
        workspace_id: str = None,
    ):
        self.end_time = end_time
        self.start_time = start_time
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class GetJobsStatisticsByQuotaResponseBody(TeaModel):
    def __init__(
        self,
        quota_id: str = None,
        request_id: str = None,
        statistics: Dict[str, Any] = None,
    ):
        self.quota_id = quota_id
        self.request_id = request_id
        self.statistics = statistics

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.quota_id is not None:
            result['QuotaId'] = self.quota_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('QuotaId') is not None:
            self.quota_id = m.get('QuotaId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        return self


class GetJobsStatisticsByQuotaResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetJobsStatisticsByQuotaResponseBody = None,
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
            temp_model = GetJobsStatisticsByQuotaResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetJobsStatisticsByResourceGroupRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        start_time: str = None,
        workspace_id: str = None,
    ):
        self.end_time = end_time
        self.start_time = start_time
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.workspace_id is not None:
            result['WorkspaceID'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('WorkspaceID') is not None:
            self.workspace_id = m.get('WorkspaceID')
        return self


class GetJobsStatisticsByResourceGroupResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        statistics: Dict[str, Any] = None,
    ):
        self.request_id = request_id
        self.statistics = statistics

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        return self


class GetJobsStatisticsByResourceGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetJobsStatisticsByResourceGroupResponseBody = None,
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
            temp_model = GetJobsStatisticsByResourceGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetMachineGroupResponseBody(TeaModel):
    def __init__(
        self,
        count: int = None,
        default_driver: str = None,
        duration: str = None,
        ecs_type: str = None,
        gmt_created: str = None,
        gmt_expired: str = None,
        gmt_modified: str = None,
        gmt_started: str = None,
        machine_group_id: str = None,
        order_id: str = None,
        order_instance_id: str = None,
        pairesource_id: str = None,
        pay_type: str = None,
        pricing_cycle: str = None,
        region_id: str = None,
        request_id: str = None,
        status: str = None,
        supported_drivers: List[str] = None,
    ):
        self.count = count
        self.default_driver = default_driver
        self.duration = duration
        self.ecs_type = ecs_type
        self.gmt_created = gmt_created
        self.gmt_expired = gmt_expired
        self.gmt_modified = gmt_modified
        self.gmt_started = gmt_started
        self.machine_group_id = machine_group_id
        self.order_id = order_id
        self.order_instance_id = order_instance_id
        self.pairesource_id = pairesource_id
        self.pay_type = pay_type
        self.pricing_cycle = pricing_cycle
        self.region_id = region_id
        self.request_id = request_id
        self.status = status
        self.supported_drivers = supported_drivers

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.count is not None:
            result['Count'] = self.count
        if self.default_driver is not None:
            result['DefaultDriver'] = self.default_driver
        if self.duration is not None:
            result['Duration'] = self.duration
        if self.ecs_type is not None:
            result['EcsType'] = self.ecs_type
        if self.gmt_created is not None:
            result['GmtCreated'] = self.gmt_created
        if self.gmt_expired is not None:
            result['GmtExpired'] = self.gmt_expired
        if self.gmt_modified is not None:
            result['GmtModified'] = self.gmt_modified
        if self.gmt_started is not None:
            result['GmtStarted'] = self.gmt_started
        if self.machine_group_id is not None:
            result['MachineGroupID'] = self.machine_group_id
        if self.order_id is not None:
            result['OrderID'] = self.order_id
        if self.order_instance_id is not None:
            result['OrderInstanceId'] = self.order_instance_id
        if self.pairesource_id is not None:
            result['PAIResourceID'] = self.pairesource_id
        if self.pay_type is not None:
            result['PayType'] = self.pay_type
        if self.pricing_cycle is not None:
            result['PricingCycle'] = self.pricing_cycle
        if self.region_id is not None:
            result['RegionID'] = self.region_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.status is not None:
            result['Status'] = self.status
        if self.supported_drivers is not None:
            result['SupportedDrivers'] = self.supported_drivers
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Count') is not None:
            self.count = m.get('Count')
        if m.get('DefaultDriver') is not None:
            self.default_driver = m.get('DefaultDriver')
        if m.get('Duration') is not None:
            self.duration = m.get('Duration')
        if m.get('EcsType') is not None:
            self.ecs_type = m.get('EcsType')
        if m.get('GmtCreated') is not None:
            self.gmt_created = m.get('GmtCreated')
        if m.get('GmtExpired') is not None:
            self.gmt_expired = m.get('GmtExpired')
        if m.get('GmtModified') is not None:
            self.gmt_modified = m.get('GmtModified')
        if m.get('GmtStarted') is not None:
            self.gmt_started = m.get('GmtStarted')
        if m.get('MachineGroupID') is not None:
            self.machine_group_id = m.get('MachineGroupID')
        if m.get('OrderID') is not None:
            self.order_id = m.get('OrderID')
        if m.get('OrderInstanceId') is not None:
            self.order_instance_id = m.get('OrderInstanceId')
        if m.get('PAIResourceID') is not None:
            self.pairesource_id = m.get('PAIResourceID')
        if m.get('PayType') is not None:
            self.pay_type = m.get('PayType')
        if m.get('PricingCycle') is not None:
            self.pricing_cycle = m.get('PricingCycle')
        if m.get('RegionID') is not None:
            self.region_id = m.get('RegionID')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('SupportedDrivers') is not None:
            self.supported_drivers = m.get('SupportedDrivers')
        return self


class GetMachineGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetMachineGroupResponseBody = None,
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
            temp_model = GetMachineGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetMetricsRequest(TeaModel):
    def __init__(
        self,
        dimensions: str = None,
        end_time: str = None,
        express: str = None,
        length: str = None,
        metric_name: str = None,
        namespace: str = None,
        next_token: str = None,
        period: str = None,
        start_time: str = None,
    ):
        # This parameter is required.
        self.dimensions = dimensions
        self.end_time = end_time
        self.express = express
        self.length = length
        # This parameter is required.
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
        if self.express is not None:
            result['Express'] = self.express
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
        if m.get('Express') is not None:
            self.express = m.get('Express')
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


class GetNodeGPUMetricsRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        metric_type: str = None,
        quota_id: str = None,
        start_time: str = None,
    ):
        self.end_time = end_time
        # This parameter is required.
        self.metric_type = metric_type
        # This parameter is required.
        self.quota_id = quota_id
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
        if self.metric_type is not None:
            result['MetricType'] = self.metric_type
        if self.quota_id is not None:
            result['QuotaId'] = self.quota_id
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('MetricType') is not None:
            self.metric_type = m.get('MetricType')
        if m.get('QuotaId') is not None:
            self.quota_id = m.get('QuotaId')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        return self


class GetNodeGPUMetricsResponseBody(TeaModel):
    def __init__(
        self,
        metric_type: str = None,
        node_gpumetric: NodeGPUMetric = None,
        request_id: str = None,
    ):
        self.metric_type = metric_type
        self.node_gpumetric = node_gpumetric
        self.request_id = request_id

    def validate(self):
        if self.node_gpumetric:
            self.node_gpumetric.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.metric_type is not None:
            result['MetricType'] = self.metric_type
        if self.node_gpumetric is not None:
            result['NodeGPUMetric'] = self.node_gpumetric.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MetricType') is not None:
            self.metric_type = m.get('MetricType')
        if m.get('NodeGPUMetric') is not None:
            temp_model = NodeGPUMetric()
            self.node_gpumetric = temp_model.from_map(m['NodeGPUMetric'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetNodeGPUMetricsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetNodeGPUMetricsResponseBody = None,
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
            temp_model = GetNodeGPUMetricsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetNodeMetricsRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        gputype: str = None,
        start_time: str = None,
        time_step: str = None,
        verbose: bool = None,
    ):
        self.end_time = end_time
        self.gputype = gputype
        self.start_time = start_time
        self.time_step = time_step
        self.verbose = verbose

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.gputype is not None:
            result['GPUType'] = self.gputype
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.time_step is not None:
            result['TimeStep'] = self.time_step
        if self.verbose is not None:
            result['Verbose'] = self.verbose
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('GPUType') is not None:
            self.gputype = m.get('GPUType')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('TimeStep') is not None:
            self.time_step = m.get('TimeStep')
        if m.get('Verbose') is not None:
            self.verbose = m.get('Verbose')
        return self


class GetNodeMetricsResponseBody(TeaModel):
    def __init__(
        self,
        metric_type: str = None,
        nodes_metrics: List[NodeMetric] = None,
        resource_group_id: str = None,
    ):
        self.metric_type = metric_type
        self.nodes_metrics = nodes_metrics
        self.resource_group_id = resource_group_id

    def validate(self):
        if self.nodes_metrics:
            for k in self.nodes_metrics:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.metric_type is not None:
            result['MetricType'] = self.metric_type
        result['NodesMetrics'] = []
        if self.nodes_metrics is not None:
            for k in self.nodes_metrics:
                result['NodesMetrics'].append(k.to_map() if k else None)
        if self.resource_group_id is not None:
            result['ResourceGroupID'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MetricType') is not None:
            self.metric_type = m.get('MetricType')
        self.nodes_metrics = []
        if m.get('NodesMetrics') is not None:
            for k in m.get('NodesMetrics'):
                temp_model = NodeMetric()
                self.nodes_metrics.append(temp_model.from_map(k))
        if m.get('ResourceGroupID') is not None:
            self.resource_group_id = m.get('ResourceGroupID')
        return self


class GetNodeMetricsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetNodeMetricsResponseBody = None,
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
            temp_model = GetNodeMetricsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetNodeViewMetricsRequest(TeaModel):
    def __init__(
        self,
        node_id: str = None,
        page_number: int = None,
        page_size: int = None,
        time_step: str = None,
        workspace_id: str = None,
    ):
        self.node_id = node_id
        # This parameter is required.
        self.page_number = page_number
        # This parameter is required.
        self.page_size = page_size
        self.time_step = time_step
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.node_id is not None:
            result['NodeId'] = self.node_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.time_step is not None:
            result['TimeStep'] = self.time_step
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NodeId') is not None:
            self.node_id = m.get('NodeId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('TimeStep') is not None:
            self.time_step = m.get('TimeStep')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class GetNodeViewMetricsResponseBody(TeaModel):
    def __init__(
        self,
        node_metrics: List[NodeViewMetric] = None,
        total: int = None,
    ):
        self.node_metrics = node_metrics
        self.total = total

    def validate(self):
        if self.node_metrics:
            for k in self.node_metrics:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['NodeMetrics'] = []
        if self.node_metrics is not None:
            for k in self.node_metrics:
                result['NodeMetrics'].append(k.to_map() if k else None)
        if self.total is not None:
            result['Total'] = self.total
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.node_metrics = []
        if m.get('NodeMetrics') is not None:
            for k in m.get('NodeMetrics'):
                temp_model = NodeViewMetric()
                self.node_metrics.append(temp_model.from_map(k))
        if m.get('Total') is not None:
            self.total = m.get('Total')
        return self


class GetNodeViewMetricsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetNodeViewMetricsResponseBody = None,
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
            temp_model = GetNodeViewMetricsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetOperationResponseBody(TeaModel):
    def __init__(
        self,
        creator_id: str = None,
        gmt_created_time: str = None,
        gmt_end_time: str = None,
        gmt_modified_time: str = None,
        gmt_start_time: str = None,
        object_id: str = None,
        object_type: str = None,
        operation_description: str = None,
        operation_id: str = None,
        operation_spec_json: str = None,
        operation_type: str = None,
        reason_code: str = None,
        reason_message: str = None,
        request_id: str = None,
        status: str = None,
    ):
        self.creator_id = creator_id
        self.gmt_created_time = gmt_created_time
        self.gmt_end_time = gmt_end_time
        self.gmt_modified_time = gmt_modified_time
        self.gmt_start_time = gmt_start_time
        self.object_id = object_id
        self.object_type = object_type
        self.operation_description = operation_description
        self.operation_id = operation_id
        self.operation_spec_json = operation_spec_json
        self.operation_type = operation_type
        self.reason_code = reason_code
        self.reason_message = reason_message
        self.request_id = request_id
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.creator_id is not None:
            result['CreatorId'] = self.creator_id
        if self.gmt_created_time is not None:
            result['GmtCreatedTime'] = self.gmt_created_time
        if self.gmt_end_time is not None:
            result['GmtEndTime'] = self.gmt_end_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.gmt_start_time is not None:
            result['GmtStartTime'] = self.gmt_start_time
        if self.object_id is not None:
            result['ObjectId'] = self.object_id
        if self.object_type is not None:
            result['ObjectType'] = self.object_type
        if self.operation_description is not None:
            result['OperationDescription'] = self.operation_description
        if self.operation_id is not None:
            result['OperationId'] = self.operation_id
        if self.operation_spec_json is not None:
            result['OperationSpecJson'] = self.operation_spec_json
        if self.operation_type is not None:
            result['OperationType'] = self.operation_type
        if self.reason_code is not None:
            result['ReasonCode'] = self.reason_code
        if self.reason_message is not None:
            result['ReasonMessage'] = self.reason_message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CreatorId') is not None:
            self.creator_id = m.get('CreatorId')
        if m.get('GmtCreatedTime') is not None:
            self.gmt_created_time = m.get('GmtCreatedTime')
        if m.get('GmtEndTime') is not None:
            self.gmt_end_time = m.get('GmtEndTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('GmtStartTime') is not None:
            self.gmt_start_time = m.get('GmtStartTime')
        if m.get('ObjectId') is not None:
            self.object_id = m.get('ObjectId')
        if m.get('ObjectType') is not None:
            self.object_type = m.get('ObjectType')
        if m.get('OperationDescription') is not None:
            self.operation_description = m.get('OperationDescription')
        if m.get('OperationId') is not None:
            self.operation_id = m.get('OperationId')
        if m.get('OperationSpecJson') is not None:
            self.operation_spec_json = m.get('OperationSpecJson')
        if m.get('OperationType') is not None:
            self.operation_type = m.get('OperationType')
        if m.get('ReasonCode') is not None:
            self.reason_code = m.get('ReasonCode')
        if m.get('ReasonMessage') is not None:
            self.reason_message = m.get('ReasonMessage')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class GetOperationResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetOperationResponseBody = None,
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
            temp_model = GetOperationResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetQueueInfosRequest(TeaModel):
    def __init__(
        self,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        quota_ids: str = None,
        sort_by: str = None,
        workload_ids: str = None,
        workload_type: str = None,
        workspace_ids: str = None,
    ):
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        self.quota_ids = quota_ids
        self.sort_by = sort_by
        self.workload_ids = workload_ids
        self.workload_type = workload_type
        self.workspace_ids = workspace_ids

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
        if self.quota_ids is not None:
            result['QuotaIds'] = self.quota_ids
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.workload_ids is not None:
            result['WorkloadIds'] = self.workload_ids
        if self.workload_type is not None:
            result['WorkloadType'] = self.workload_type
        if self.workspace_ids is not None:
            result['WorkspaceIds'] = self.workspace_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('QuotaIds') is not None:
            self.quota_ids = m.get('QuotaIds')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('WorkloadIds') is not None:
            self.workload_ids = m.get('WorkloadIds')
        if m.get('WorkloadType') is not None:
            self.workload_type = m.get('WorkloadType')
        if m.get('WorkspaceIds') is not None:
            self.workspace_ids = m.get('WorkspaceIds')
        return self


class GetQueueInfosResponseBody(TeaModel):
    def __init__(
        self,
        queue_infos: List[QueueInfo] = None,
        request_id: str = None,
        total_count: int = None,
    ):
        self.queue_infos = queue_infos
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.queue_infos:
            for k in self.queue_infos:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['QueueInfos'] = []
        if self.queue_infos is not None:
            for k in self.queue_infos:
                result['QueueInfos'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.queue_infos = []
        if m.get('QueueInfos') is not None:
            for k in m.get('QueueInfos'):
                temp_model = QueueInfo()
                self.queue_infos.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class GetQueueInfosResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetQueueInfosResponseBody = None,
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
            temp_model = GetQueueInfosResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetQuotaRequest(TeaModel):
    def __init__(
        self,
        verbose: bool = None,
    ):
        self.verbose = verbose

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.verbose is not None:
            result['Verbose'] = self.verbose
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Verbose') is not None:
            self.verbose = m.get('Verbose')
        return self


class GetQuotaResponseBody(TeaModel):
    def __init__(
        self,
        allocate_strategy: str = None,
        creator_id: str = None,
        description: str = None,
        gmt_created_time: str = None,
        gmt_modified_time: str = None,
        labels: List[Label] = None,
        latest_operation_id: str = None,
        min: ResourceSpec = None,
        parent_quota_id: str = None,
        queue_strategy: str = None,
        quota_config: QuotaConfig = None,
        quota_details: QuotaDetails = None,
        quota_id: str = None,
        quota_name: str = None,
        reason_code: str = None,
        reason_message: str = None,
        request_id: str = None,
        resource_group_ids: List[str] = None,
        resource_type: str = None,
        status: str = None,
        sub_quotas: List[QuotaIdName] = None,
        workspaces: List[WorkspaceIdName] = None,
    ):
        self.allocate_strategy = allocate_strategy
        self.creator_id = creator_id
        self.description = description
        self.gmt_created_time = gmt_created_time
        self.gmt_modified_time = gmt_modified_time
        self.labels = labels
        self.latest_operation_id = latest_operation_id
        self.min = min
        self.parent_quota_id = parent_quota_id
        self.queue_strategy = queue_strategy
        self.quota_config = quota_config
        self.quota_details = quota_details
        # Quota Id
        self.quota_id = quota_id
        self.quota_name = quota_name
        self.reason_code = reason_code
        self.reason_message = reason_message
        self.request_id = request_id
        self.resource_group_ids = resource_group_ids
        self.resource_type = resource_type
        self.status = status
        self.sub_quotas = sub_quotas
        self.workspaces = workspaces

    def validate(self):
        if self.labels:
            for k in self.labels:
                if k:
                    k.validate()
        if self.min:
            self.min.validate()
        if self.quota_config:
            self.quota_config.validate()
        if self.quota_details:
            self.quota_details.validate()
        if self.sub_quotas:
            for k in self.sub_quotas:
                if k:
                    k.validate()
        if self.workspaces:
            for k in self.workspaces:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.allocate_strategy is not None:
            result['AllocateStrategy'] = self.allocate_strategy
        if self.creator_id is not None:
            result['CreatorId'] = self.creator_id
        if self.description is not None:
            result['Description'] = self.description
        if self.gmt_created_time is not None:
            result['GmtCreatedTime'] = self.gmt_created_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        if self.latest_operation_id is not None:
            result['LatestOperationId'] = self.latest_operation_id
        if self.min is not None:
            result['Min'] = self.min.to_map()
        if self.parent_quota_id is not None:
            result['ParentQuotaId'] = self.parent_quota_id
        if self.queue_strategy is not None:
            result['QueueStrategy'] = self.queue_strategy
        if self.quota_config is not None:
            result['QuotaConfig'] = self.quota_config.to_map()
        if self.quota_details is not None:
            result['QuotaDetails'] = self.quota_details.to_map()
        if self.quota_id is not None:
            result['QuotaId'] = self.quota_id
        if self.quota_name is not None:
            result['QuotaName'] = self.quota_name
        if self.reason_code is not None:
            result['ReasonCode'] = self.reason_code
        if self.reason_message is not None:
            result['ReasonMessage'] = self.reason_message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.resource_group_ids is not None:
            result['ResourceGroupIds'] = self.resource_group_ids
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.status is not None:
            result['Status'] = self.status
        result['SubQuotas'] = []
        if self.sub_quotas is not None:
            for k in self.sub_quotas:
                result['SubQuotas'].append(k.to_map() if k else None)
        result['Workspaces'] = []
        if self.workspaces is not None:
            for k in self.workspaces:
                result['Workspaces'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AllocateStrategy') is not None:
            self.allocate_strategy = m.get('AllocateStrategy')
        if m.get('CreatorId') is not None:
            self.creator_id = m.get('CreatorId')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('GmtCreatedTime') is not None:
            self.gmt_created_time = m.get('GmtCreatedTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = Label()
                self.labels.append(temp_model.from_map(k))
        if m.get('LatestOperationId') is not None:
            self.latest_operation_id = m.get('LatestOperationId')
        if m.get('Min') is not None:
            temp_model = ResourceSpec()
            self.min = temp_model.from_map(m['Min'])
        if m.get('ParentQuotaId') is not None:
            self.parent_quota_id = m.get('ParentQuotaId')
        if m.get('QueueStrategy') is not None:
            self.queue_strategy = m.get('QueueStrategy')
        if m.get('QuotaConfig') is not None:
            temp_model = QuotaConfig()
            self.quota_config = temp_model.from_map(m['QuotaConfig'])
        if m.get('QuotaDetails') is not None:
            temp_model = QuotaDetails()
            self.quota_details = temp_model.from_map(m['QuotaDetails'])
        if m.get('QuotaId') is not None:
            self.quota_id = m.get('QuotaId')
        if m.get('QuotaName') is not None:
            self.quota_name = m.get('QuotaName')
        if m.get('ReasonCode') is not None:
            self.reason_code = m.get('ReasonCode')
        if m.get('ReasonMessage') is not None:
            self.reason_message = m.get('ReasonMessage')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ResourceGroupIds') is not None:
            self.resource_group_ids = m.get('ResourceGroupIds')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        self.sub_quotas = []
        if m.get('SubQuotas') is not None:
            for k in m.get('SubQuotas'):
                temp_model = QuotaIdName()
                self.sub_quotas.append(temp_model.from_map(k))
        self.workspaces = []
        if m.get('Workspaces') is not None:
            for k in m.get('Workspaces'):
                temp_model = WorkspaceIdName()
                self.workspaces.append(temp_model.from_map(k))
        return self


class GetQuotaResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetQuotaResponseBody = None,
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
            temp_model = GetQuotaResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetQuotaJobViewMetricsRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        sort_by: str = None,
        start_time: str = None,
        time_step: str = None,
        workspace_id: str = None,
    ):
        self.end_time = end_time
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        self.sort_by = sort_by
        self.start_time = start_time
        self.time_step = time_step
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.order is not None:
            result['Order'] = self.order
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.time_step is not None:
            result['TimeStep'] = self.time_step
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('TimeStep') is not None:
            self.time_step = m.get('TimeStep')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class GetQuotaJobViewMetricsResponseBody(TeaModel):
    def __init__(
        self,
        job_metrics: List[QuotaJobViewMetric] = None,
        quota_id: str = None,
        request_id: str = None,
        summary: QuotaJobViewMetric = None,
        total_count: int = None,
    ):
        self.job_metrics = job_metrics
        self.quota_id = quota_id
        self.request_id = request_id
        self.summary = summary
        self.total_count = total_count

    def validate(self):
        if self.job_metrics:
            for k in self.job_metrics:
                if k:
                    k.validate()
        if self.summary:
            self.summary.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['JobMetrics'] = []
        if self.job_metrics is not None:
            for k in self.job_metrics:
                result['JobMetrics'].append(k.to_map() if k else None)
        if self.quota_id is not None:
            result['QuotaId'] = self.quota_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.summary is not None:
            result['Summary'] = self.summary.to_map()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.job_metrics = []
        if m.get('JobMetrics') is not None:
            for k in m.get('JobMetrics'):
                temp_model = QuotaJobViewMetric()
                self.job_metrics.append(temp_model.from_map(k))
        if m.get('QuotaId') is not None:
            self.quota_id = m.get('QuotaId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Summary') is not None:
            temp_model = QuotaJobViewMetric()
            self.summary = temp_model.from_map(m['Summary'])
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class GetQuotaJobViewMetricsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetQuotaJobViewMetricsResponseBody = None,
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
            temp_model = GetQuotaJobViewMetricsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetQuotaMetricsRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        gputype: str = None,
        start_time: str = None,
        time_step: str = None,
    ):
        self.end_time = end_time
        self.gputype = gputype
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
        if self.gputype is not None:
            result['GPUType'] = self.gputype
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.time_step is not None:
            result['TimeStep'] = self.time_step
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('GPUType') is not None:
            self.gputype = m.get('GPUType')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('TimeStep') is not None:
            self.time_step = m.get('TimeStep')
        return self


class GetQuotaMetricsResponseBody(TeaModel):
    def __init__(
        self,
        quota_id: str = None,
        quota_metrics: List[QuotaMetric] = None,
        request_id: str = None,
    ):
        self.quota_id = quota_id
        self.quota_metrics = quota_metrics
        self.request_id = request_id

    def validate(self):
        if self.quota_metrics:
            for k in self.quota_metrics:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.quota_id is not None:
            result['QuotaId'] = self.quota_id
        result['QuotaMetrics'] = []
        if self.quota_metrics is not None:
            for k in self.quota_metrics:
                result['QuotaMetrics'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('QuotaId') is not None:
            self.quota_id = m.get('QuotaId')
        self.quota_metrics = []
        if m.get('QuotaMetrics') is not None:
            for k in m.get('QuotaMetrics'):
                temp_model = QuotaMetric()
                self.quota_metrics.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class GetQuotaMetricsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetQuotaMetricsResponseBody = None,
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
            temp_model = GetQuotaMetricsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetQuotaNodeMetricsRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        gputype: str = None,
        start_time: str = None,
        time_step: str = None,
        verbose: bool = None,
    ):
        self.end_time = end_time
        self.gputype = gputype
        self.start_time = start_time
        self.time_step = time_step
        self.verbose = verbose

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.gputype is not None:
            result['GPUType'] = self.gputype
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.time_step is not None:
            result['TimeStep'] = self.time_step
        if self.verbose is not None:
            result['Verbose'] = self.verbose
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('GPUType') is not None:
            self.gputype = m.get('GPUType')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('TimeStep') is not None:
            self.time_step = m.get('TimeStep')
        if m.get('Verbose') is not None:
            self.verbose = m.get('Verbose')
        return self


class GetQuotaNodeMetricsResponseBody(TeaModel):
    def __init__(
        self,
        metric_type: str = None,
        nodes_metrics: List[NodeMetric] = None,
        quota_id: str = None,
        request_id: str = None,
    ):
        self.metric_type = metric_type
        self.nodes_metrics = nodes_metrics
        self.quota_id = quota_id
        self.request_id = request_id

    def validate(self):
        if self.nodes_metrics:
            for k in self.nodes_metrics:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.metric_type is not None:
            result['MetricType'] = self.metric_type
        result['NodesMetrics'] = []
        if self.nodes_metrics is not None:
            for k in self.nodes_metrics:
                result['NodesMetrics'].append(k.to_map() if k else None)
        if self.quota_id is not None:
            result['QuotaId'] = self.quota_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MetricType') is not None:
            self.metric_type = m.get('MetricType')
        self.nodes_metrics = []
        if m.get('NodesMetrics') is not None:
            for k in m.get('NodesMetrics'):
                temp_model = NodeMetric()
                self.nodes_metrics.append(temp_model.from_map(k))
        if m.get('QuotaId') is not None:
            self.quota_id = m.get('QuotaId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class GetQuotaNodeMetricsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetQuotaNodeMetricsResponseBody = None,
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
            temp_model = GetQuotaNodeMetricsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetQuotaNodeViewMetricsRequest(TeaModel):
    def __init__(
        self,
        node_id: str = None,
        node_status: str = None,
        order: str = None,
        order_status: str = None,
        page_number: int = None,
        page_size: int = None,
        resource_group_id: str = None,
        self_only: bool = None,
        sort_by: str = None,
        time_step: str = None,
        workspace_id: str = None,
    ):
        self.node_id = node_id
        self.node_status = node_status
        self.order = order
        self.order_status = order_status
        self.page_number = page_number
        self.page_size = page_size
        self.resource_group_id = resource_group_id
        self.self_only = self_only
        self.sort_by = sort_by
        self.time_step = time_step
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.node_id is not None:
            result['NodeId'] = self.node_id
        if self.node_status is not None:
            result['NodeStatus'] = self.node_status
        if self.order is not None:
            result['Order'] = self.order
        if self.order_status is not None:
            result['OrderStatus'] = self.order_status
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.self_only is not None:
            result['SelfOnly'] = self.self_only
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.time_step is not None:
            result['TimeStep'] = self.time_step
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NodeId') is not None:
            self.node_id = m.get('NodeId')
        if m.get('NodeStatus') is not None:
            self.node_status = m.get('NodeStatus')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('OrderStatus') is not None:
            self.order_status = m.get('OrderStatus')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('SelfOnly') is not None:
            self.self_only = m.get('SelfOnly')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('TimeStep') is not None:
            self.time_step = m.get('TimeStep')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class GetQuotaNodeViewMetricsResponseBody(TeaModel):
    def __init__(
        self,
        node_metrics: List[QuotaNodeViewMetric] = None,
        quota_id: str = None,
        request_id: str = None,
        total_count: int = None,
    ):
        self.node_metrics = node_metrics
        self.quota_id = quota_id
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.node_metrics:
            for k in self.node_metrics:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['NodeMetrics'] = []
        if self.node_metrics is not None:
            for k in self.node_metrics:
                result['NodeMetrics'].append(k.to_map() if k else None)
        if self.quota_id is not None:
            result['QuotaId'] = self.quota_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.node_metrics = []
        if m.get('NodeMetrics') is not None:
            for k in m.get('NodeMetrics'):
                temp_model = QuotaNodeViewMetric()
                self.node_metrics.append(temp_model.from_map(k))
        if m.get('QuotaId') is not None:
            self.quota_id = m.get('QuotaId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class GetQuotaNodeViewMetricsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetQuotaNodeViewMetricsResponseBody = None,
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
            temp_model = GetQuotaNodeViewMetricsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetQuotaQueueInfoRequest(TeaModel):
    def __init__(
        self,
        before_workload_id: str = None,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        show_own: bool = None,
        sort_by: str = None,
        status: str = None,
        sub_quota_ids: str = None,
        workload_ids: str = None,
        workload_type: str = None,
        workspace_ids: str = None,
    ):
        self.before_workload_id = before_workload_id
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        self.show_own = show_own
        self.sort_by = sort_by
        self.status = status
        self.sub_quota_ids = sub_quota_ids
        self.workload_ids = workload_ids
        self.workload_type = workload_type
        self.workspace_ids = workspace_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.before_workload_id is not None:
            result['BeforeWorkloadId'] = self.before_workload_id
        if self.order is not None:
            result['Order'] = self.order
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.show_own is not None:
            result['ShowOwn'] = self.show_own
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.status is not None:
            result['Status'] = self.status
        if self.sub_quota_ids is not None:
            result['SubQuotaIds'] = self.sub_quota_ids
        if self.workload_ids is not None:
            result['WorkloadIds'] = self.workload_ids
        if self.workload_type is not None:
            result['WorkloadType'] = self.workload_type
        if self.workspace_ids is not None:
            result['WorkspaceIds'] = self.workspace_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BeforeWorkloadId') is not None:
            self.before_workload_id = m.get('BeforeWorkloadId')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('ShowOwn') is not None:
            self.show_own = m.get('ShowOwn')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('SubQuotaIds') is not None:
            self.sub_quota_ids = m.get('SubQuotaIds')
        if m.get('WorkloadIds') is not None:
            self.workload_ids = m.get('WorkloadIds')
        if m.get('WorkloadType') is not None:
            self.workload_type = m.get('WorkloadType')
        if m.get('WorkspaceIds') is not None:
            self.workspace_ids = m.get('WorkspaceIds')
        return self


class GetQuotaQueueInfoResponseBody(TeaModel):
    def __init__(
        self,
        queue_infos: List[QueueInfo] = None,
        request_id: str = None,
        total_count: int = None,
    ):
        self.queue_infos = queue_infos
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.queue_infos:
            for k in self.queue_infos:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['QueueInfos'] = []
        if self.queue_infos is not None:
            for k in self.queue_infos:
                result['QueueInfos'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.queue_infos = []
        if m.get('QueueInfos') is not None:
            for k in m.get('QueueInfos'):
                temp_model = QueueInfo()
                self.queue_infos.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class GetQuotaQueueInfoResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetQuotaQueueInfoResponseBody = None,
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
            temp_model = GetQuotaQueueInfoResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetQuotaRangeUserViewMetricsRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        sort_by: str = None,
        start_time: str = None,
        user_id: str = None,
        workspace_id: str = None,
    ):
        self.end_time = end_time
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        self.sort_by = sort_by
        self.start_time = start_time
        self.user_id = user_id
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.order is not None:
            result['Order'] = self.order
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class GetQuotaRangeUserViewMetricsResponseBody(TeaModel):
    def __init__(
        self,
        quota_id: str = None,
        request_id: str = None,
        summary: QuotaUserViewMetric = None,
        total_count: int = None,
        user_metrics: List[QuotaUserViewMetric] = None,
    ):
        self.quota_id = quota_id
        self.request_id = request_id
        self.summary = summary
        self.total_count = total_count
        self.user_metrics = user_metrics

    def validate(self):
        if self.summary:
            self.summary.validate()
        if self.user_metrics:
            for k in self.user_metrics:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.quota_id is not None:
            result['QuotaId'] = self.quota_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.summary is not None:
            result['Summary'] = self.summary.to_map()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        result['UserMetrics'] = []
        if self.user_metrics is not None:
            for k in self.user_metrics:
                result['UserMetrics'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('QuotaId') is not None:
            self.quota_id = m.get('QuotaId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Summary') is not None:
            temp_model = QuotaUserViewMetric()
            self.summary = temp_model.from_map(m['Summary'])
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        self.user_metrics = []
        if m.get('UserMetrics') is not None:
            for k in m.get('UserMetrics'):
                temp_model = QuotaUserViewMetric()
                self.user_metrics.append(temp_model.from_map(k))
        return self


class GetQuotaRangeUserViewMetricsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetQuotaRangeUserViewMetricsResponseBody = None,
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
            temp_model = GetQuotaRangeUserViewMetricsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetQuotaTopoRequest(TeaModel):
    def __init__(
        self,
        depth: int = None,
        show_own_workloads: bool = None,
        verbose: bool = None,
    ):
        self.depth = depth
        self.show_own_workloads = show_own_workloads
        self.verbose = verbose

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.depth is not None:
            result['Depth'] = self.depth
        if self.show_own_workloads is not None:
            result['ShowOwnWorkloads'] = self.show_own_workloads
        if self.verbose is not None:
            result['Verbose'] = self.verbose
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Depth') is not None:
            self.depth = m.get('Depth')
        if m.get('ShowOwnWorkloads') is not None:
            self.show_own_workloads = m.get('ShowOwnWorkloads')
        if m.get('Verbose') is not None:
            self.verbose = m.get('Verbose')
        return self


class GetQuotaTopoResponseBody(TeaModel):
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
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetQuotaTopoResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetQuotaTopoResponseBody = None,
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
            temp_model = GetQuotaTopoResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetQuotaUserViewMetricsRequest(TeaModel):
    def __init__(
        self,
        order: str = None,
        page_number: str = None,
        page_size: str = None,
        sort_by: str = None,
        time_step: str = None,
        user_id: str = None,
        workspace_id: str = None,
    ):
        self.order = order
        # This parameter is required.
        self.page_number = page_number
        # This parameter is required.
        self.page_size = page_size
        self.sort_by = sort_by
        self.time_step = time_step
        self.user_id = user_id
        self.workspace_id = workspace_id

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
        if self.time_step is not None:
            result['TimeStep'] = self.time_step
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
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
        if m.get('TimeStep') is not None:
            self.time_step = m.get('TimeStep')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class GetQuotaUserViewMetricsResponseBody(TeaModel):
    def __init__(
        self,
        quota_id: str = None,
        request_id: str = None,
        summary: QuotaUserViewMetric = None,
        total_count: int = None,
        user_metrics: List[QuotaUserViewMetric] = None,
    ):
        self.quota_id = quota_id
        self.request_id = request_id
        self.summary = summary
        self.total_count = total_count
        self.user_metrics = user_metrics

    def validate(self):
        if self.summary:
            self.summary.validate()
        if self.user_metrics:
            for k in self.user_metrics:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.quota_id is not None:
            result['QuotaId'] = self.quota_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.summary is not None:
            result['Summary'] = self.summary.to_map()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        result['UserMetrics'] = []
        if self.user_metrics is not None:
            for k in self.user_metrics:
                result['UserMetrics'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('QuotaId') is not None:
            self.quota_id = m.get('QuotaId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Summary') is not None:
            temp_model = QuotaUserViewMetric()
            self.summary = temp_model.from_map(m['Summary'])
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        self.user_metrics = []
        if m.get('UserMetrics') is not None:
            for k in m.get('UserMetrics'):
                temp_model = QuotaUserViewMetric()
                self.user_metrics.append(temp_model.from_map(k))
        return self


class GetQuotaUserViewMetricsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetQuotaUserViewMetricsResponseBody = None,
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
            temp_model = GetQuotaUserViewMetricsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetRangeUserViewMetricsRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        sort_by: str = None,
        start_time: str = None,
        user_id: str = None,
        workspace_id: str = None,
    ):
        self.end_time = end_time
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        self.sort_by = sort_by
        self.start_time = start_time
        self.user_id = user_id
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.order is not None:
            result['Order'] = self.order
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class GetRangeUserViewMetricsResponseBody(TeaModel):
    def __init__(
        self,
        summary: UserViewMetric = None,
        user_metrics: List[UserViewMetric] = None,
        request_id: str = None,
    ):
        self.summary = summary
        self.user_metrics = user_metrics
        self.request_id = request_id

    def validate(self):
        if self.summary:
            self.summary.validate()
        if self.user_metrics:
            for k in self.user_metrics:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.summary is not None:
            result['Summary'] = self.summary.to_map()
        result['UserMetrics'] = []
        if self.user_metrics is not None:
            for k in self.user_metrics:
                result['UserMetrics'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Summary') is not None:
            temp_model = UserViewMetric()
            self.summary = temp_model.from_map(m['Summary'])
        self.user_metrics = []
        if m.get('UserMetrics') is not None:
            for k in m.get('UserMetrics'):
                temp_model = UserViewMetric()
                self.user_metrics.append(temp_model.from_map(k))
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetRangeUserViewMetricsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetRangeUserViewMetricsResponseBody = None,
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
            temp_model = GetRangeUserViewMetricsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetResourceGroupRequestTag(TeaModel):
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


class GetResourceGroupRequest(TeaModel):
    def __init__(
        self,
        is_aiworkspace_data_enabled: bool = None,
        tag: List[GetResourceGroupRequestTag] = None,
    ):
        self.is_aiworkspace_data_enabled = is_aiworkspace_data_enabled
        self.tag = tag

    def validate(self):
        if self.tag:
            for k in self.tag:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.is_aiworkspace_data_enabled is not None:
            result['IsAIWorkspaceDataEnabled'] = self.is_aiworkspace_data_enabled
        result['Tag'] = []
        if self.tag is not None:
            for k in self.tag:
                result['Tag'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('IsAIWorkspaceDataEnabled') is not None:
            self.is_aiworkspace_data_enabled = m.get('IsAIWorkspaceDataEnabled')
        self.tag = []
        if m.get('Tag') is not None:
            for k in m.get('Tag'):
                temp_model = GetResourceGroupRequestTag()
                self.tag.append(temp_model.from_map(k))
        return self


class GetResourceGroupShrinkRequest(TeaModel):
    def __init__(
        self,
        is_aiworkspace_data_enabled: bool = None,
        tag_shrink: str = None,
    ):
        self.is_aiworkspace_data_enabled = is_aiworkspace_data_enabled
        self.tag_shrink = tag_shrink

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.is_aiworkspace_data_enabled is not None:
            result['IsAIWorkspaceDataEnabled'] = self.is_aiworkspace_data_enabled
        if self.tag_shrink is not None:
            result['Tag'] = self.tag_shrink
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('IsAIWorkspaceDataEnabled') is not None:
            self.is_aiworkspace_data_enabled = m.get('IsAIWorkspaceDataEnabled')
        if m.get('Tag') is not None:
            self.tag_shrink = m.get('Tag')
        return self


class GetResourceGroupResponseBodyTags(TeaModel):
    def __init__(
        self,
        tag_key: str = None,
        tag_value: str = None,
    ):
        self.tag_key = tag_key
        self.tag_value = tag_value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.tag_key is not None:
            result['TagKey'] = self.tag_key
        if self.tag_value is not None:
            result['TagValue'] = self.tag_value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TagKey') is not None:
            self.tag_key = m.get('TagKey')
        if m.get('TagValue') is not None:
            self.tag_value = m.get('TagValue')
        return self


class GetResourceGroupResponseBody(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        computing_resource_provider: str = None,
        creator_id: str = None,
        description: str = None,
        gmt_created_time: str = None,
        gmt_modified_time: str = None,
        name: str = None,
        request_id: str = None,
        resource_type: str = None,
        status: str = None,
        support_rdma: bool = None,
        tags: List[GetResourceGroupResponseBodyTags] = None,
        user_vpc: UserVpc = None,
        workspace_id: str = None,
    ):
        self.cluster_id = cluster_id
        self.computing_resource_provider = computing_resource_provider
        self.creator_id = creator_id
        self.description = description
        self.gmt_created_time = gmt_created_time
        self.gmt_modified_time = gmt_modified_time
        self.name = name
        self.request_id = request_id
        self.resource_type = resource_type
        self.status = status
        self.support_rdma = support_rdma
        self.tags = tags
        self.user_vpc = user_vpc
        self.workspace_id = workspace_id

    def validate(self):
        if self.tags:
            for k in self.tags:
                if k:
                    k.validate()
        if self.user_vpc:
            self.user_vpc.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cluster_id is not None:
            result['ClusterID'] = self.cluster_id
        if self.computing_resource_provider is not None:
            result['ComputingResourceProvider'] = self.computing_resource_provider
        if self.creator_id is not None:
            result['CreatorID'] = self.creator_id
        if self.description is not None:
            result['Description'] = self.description
        if self.gmt_created_time is not None:
            result['GmtCreatedTime'] = self.gmt_created_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.name is not None:
            result['Name'] = self.name
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.status is not None:
            result['Status'] = self.status
        if self.support_rdma is not None:
            result['SupportRDMA'] = self.support_rdma
        result['Tags'] = []
        if self.tags is not None:
            for k in self.tags:
                result['Tags'].append(k.to_map() if k else None)
        if self.user_vpc is not None:
            result['UserVpc'] = self.user_vpc.to_map()
        if self.workspace_id is not None:
            result['WorkspaceID'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterID') is not None:
            self.cluster_id = m.get('ClusterID')
        if m.get('ComputingResourceProvider') is not None:
            self.computing_resource_provider = m.get('ComputingResourceProvider')
        if m.get('CreatorID') is not None:
            self.creator_id = m.get('CreatorID')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('GmtCreatedTime') is not None:
            self.gmt_created_time = m.get('GmtCreatedTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('SupportRDMA') is not None:
            self.support_rdma = m.get('SupportRDMA')
        self.tags = []
        if m.get('Tags') is not None:
            for k in m.get('Tags'):
                temp_model = GetResourceGroupResponseBodyTags()
                self.tags.append(temp_model.from_map(k))
        if m.get('UserVpc') is not None:
            temp_model = UserVpc()
            self.user_vpc = temp_model.from_map(m['UserVpc'])
        if m.get('WorkspaceID') is not None:
            self.workspace_id = m.get('WorkspaceID')
        return self


class GetResourceGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetResourceGroupResponseBody = None,
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
            temp_model = GetResourceGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetResourceGroupMachineGroupRequestTag(TeaModel):
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


class GetResourceGroupMachineGroupRequest(TeaModel):
    def __init__(
        self,
        tag: List[GetResourceGroupMachineGroupRequestTag] = None,
    ):
        self.tag = tag

    def validate(self):
        if self.tag:
            for k in self.tag:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Tag'] = []
        if self.tag is not None:
            for k in self.tag:
                result['Tag'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.tag = []
        if m.get('Tag') is not None:
            for k in m.get('Tag'):
                temp_model = GetResourceGroupMachineGroupRequestTag()
                self.tag.append(temp_model.from_map(k))
        return self


class GetResourceGroupMachineGroupShrinkRequest(TeaModel):
    def __init__(
        self,
        tag_shrink: str = None,
    ):
        self.tag_shrink = tag_shrink

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.tag_shrink is not None:
            result['Tag'] = self.tag_shrink
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Tag') is not None:
            self.tag_shrink = m.get('Tag')
        return self


class GetResourceGroupMachineGroupResponseBodyTags(TeaModel):
    def __init__(
        self,
        tag_key: str = None,
        tag_value: str = None,
    ):
        self.tag_key = tag_key
        self.tag_value = tag_value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.tag_key is not None:
            result['TagKey'] = self.tag_key
        if self.tag_value is not None:
            result['TagValue'] = self.tag_value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TagKey') is not None:
            self.tag_key = m.get('TagKey')
        if m.get('TagValue') is not None:
            self.tag_value = m.get('TagValue')
        return self


class GetResourceGroupMachineGroupResponseBody(TeaModel):
    def __init__(
        self,
        cpu: str = None,
        default_driver: str = None,
        ecs_count: int = None,
        ecs_spec: str = None,
        gmt_created_time: str = None,
        gmt_expired_time: str = None,
        gmt_modified_time: str = None,
        gmt_started_time: str = None,
        gpu: str = None,
        gpu_type: str = None,
        machine_group_id: str = None,
        memory: str = None,
        name: str = None,
        payment_duration: str = None,
        payment_duration_unit: str = None,
        payment_type: str = None,
        request_id: str = None,
        resource_group_id: str = None,
        status: str = None,
        supported_drivers: List[str] = None,
        tags: List[GetResourceGroupMachineGroupResponseBodyTags] = None,
    ):
        self.cpu = cpu
        self.default_driver = default_driver
        self.ecs_count = ecs_count
        self.ecs_spec = ecs_spec
        self.gmt_created_time = gmt_created_time
        self.gmt_expired_time = gmt_expired_time
        self.gmt_modified_time = gmt_modified_time
        self.gmt_started_time = gmt_started_time
        self.gpu = gpu
        self.gpu_type = gpu_type
        self.machine_group_id = machine_group_id
        self.memory = memory
        self.name = name
        self.payment_duration = payment_duration
        self.payment_duration_unit = payment_duration_unit
        self.payment_type = payment_type
        self.request_id = request_id
        self.resource_group_id = resource_group_id
        self.status = status
        self.supported_drivers = supported_drivers
        self.tags = tags

    def validate(self):
        if self.tags:
            for k in self.tags:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cpu is not None:
            result['Cpu'] = self.cpu
        if self.default_driver is not None:
            result['DefaultDriver'] = self.default_driver
        if self.ecs_count is not None:
            result['EcsCount'] = self.ecs_count
        if self.ecs_spec is not None:
            result['EcsSpec'] = self.ecs_spec
        if self.gmt_created_time is not None:
            result['GmtCreatedTime'] = self.gmt_created_time
        if self.gmt_expired_time is not None:
            result['GmtExpiredTime'] = self.gmt_expired_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.gmt_started_time is not None:
            result['GmtStartedTime'] = self.gmt_started_time
        if self.gpu is not None:
            result['Gpu'] = self.gpu
        if self.gpu_type is not None:
            result['GpuType'] = self.gpu_type
        if self.machine_group_id is not None:
            result['MachineGroupID'] = self.machine_group_id
        if self.memory is not None:
            result['Memory'] = self.memory
        if self.name is not None:
            result['Name'] = self.name
        if self.payment_duration is not None:
            result['PaymentDuration'] = self.payment_duration
        if self.payment_duration_unit is not None:
            result['PaymentDurationUnit'] = self.payment_duration_unit
        if self.payment_type is not None:
            result['PaymentType'] = self.payment_type
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.resource_group_id is not None:
            result['ResourceGroupID'] = self.resource_group_id
        if self.status is not None:
            result['Status'] = self.status
        if self.supported_drivers is not None:
            result['SupportedDrivers'] = self.supported_drivers
        result['Tags'] = []
        if self.tags is not None:
            for k in self.tags:
                result['Tags'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Cpu') is not None:
            self.cpu = m.get('Cpu')
        if m.get('DefaultDriver') is not None:
            self.default_driver = m.get('DefaultDriver')
        if m.get('EcsCount') is not None:
            self.ecs_count = m.get('EcsCount')
        if m.get('EcsSpec') is not None:
            self.ecs_spec = m.get('EcsSpec')
        if m.get('GmtCreatedTime') is not None:
            self.gmt_created_time = m.get('GmtCreatedTime')
        if m.get('GmtExpiredTime') is not None:
            self.gmt_expired_time = m.get('GmtExpiredTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('GmtStartedTime') is not None:
            self.gmt_started_time = m.get('GmtStartedTime')
        if m.get('Gpu') is not None:
            self.gpu = m.get('Gpu')
        if m.get('GpuType') is not None:
            self.gpu_type = m.get('GpuType')
        if m.get('MachineGroupID') is not None:
            self.machine_group_id = m.get('MachineGroupID')
        if m.get('Memory') is not None:
            self.memory = m.get('Memory')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('PaymentDuration') is not None:
            self.payment_duration = m.get('PaymentDuration')
        if m.get('PaymentDurationUnit') is not None:
            self.payment_duration_unit = m.get('PaymentDurationUnit')
        if m.get('PaymentType') is not None:
            self.payment_type = m.get('PaymentType')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ResourceGroupID') is not None:
            self.resource_group_id = m.get('ResourceGroupID')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('SupportedDrivers') is not None:
            self.supported_drivers = m.get('SupportedDrivers')
        self.tags = []
        if m.get('Tags') is not None:
            for k in m.get('Tags'):
                temp_model = GetResourceGroupMachineGroupResponseBodyTags()
                self.tags.append(temp_model.from_map(k))
        return self


class GetResourceGroupMachineGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetResourceGroupMachineGroupResponseBody = None,
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
            temp_model = GetResourceGroupMachineGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetResourceGroupMetricsRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        gputype: str = None,
        start_time: str = None,
        time_step: str = None,
    ):
        self.end_time = end_time
        self.gputype = gputype
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
        if self.gputype is not None:
            result['GPUType'] = self.gputype
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.time_step is not None:
            result['TimeStep'] = self.time_step
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('GPUType') is not None:
            self.gputype = m.get('GPUType')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('TimeStep') is not None:
            self.time_step = m.get('TimeStep')
        return self


class GetResourceGroupMetricsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        resource_group_id: str = None,
        resource_group_metrics: List[ResourceGroupMetric] = None,
    ):
        self.request_id = request_id
        self.resource_group_id = resource_group_id
        self.resource_group_metrics = resource_group_metrics

    def validate(self):
        if self.resource_group_metrics:
            for k in self.resource_group_metrics:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.resource_group_id is not None:
            result['ResourceGroupID'] = self.resource_group_id
        result['ResourceGroupMetrics'] = []
        if self.resource_group_metrics is not None:
            for k in self.resource_group_metrics:
                result['ResourceGroupMetrics'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ResourceGroupID') is not None:
            self.resource_group_id = m.get('ResourceGroupID')
        self.resource_group_metrics = []
        if m.get('ResourceGroupMetrics') is not None:
            for k in m.get('ResourceGroupMetrics'):
                temp_model = ResourceGroupMetric()
                self.resource_group_metrics.append(temp_model.from_map(k))
        return self


class GetResourceGroupMetricsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetResourceGroupMetricsResponseBody = None,
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
            temp_model = GetResourceGroupMetricsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetResourceGroupRequestRequest(TeaModel):
    def __init__(
        self,
        pod_status: str = None,
        resource_group_id: str = None,
    ):
        self.pod_status = pod_status
        # This parameter is required.
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.pod_status is not None:
            result['PodStatus'] = self.pod_status
        if self.resource_group_id is not None:
            result['ResourceGroupID'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PodStatus') is not None:
            self.pod_status = m.get('PodStatus')
        if m.get('ResourceGroupID') is not None:
            self.resource_group_id = m.get('ResourceGroupID')
        return self


class GetResourceGroupRequestResponseBody(TeaModel):
    def __init__(
        self,
        request_cpu: int = None,
        request_gpu: int = None,
        request_gpuinfos: List[GPUInfo] = None,
        request_memory: int = None,
    ):
        self.request_cpu = request_cpu
        self.request_gpu = request_gpu
        self.request_gpuinfos = request_gpuinfos
        self.request_memory = request_memory

    def validate(self):
        if self.request_gpuinfos:
            for k in self.request_gpuinfos:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_cpu is not None:
            result['requestCPU'] = self.request_cpu
        if self.request_gpu is not None:
            result['requestGPU'] = self.request_gpu
        result['requestGPUInfos'] = []
        if self.request_gpuinfos is not None:
            for k in self.request_gpuinfos:
                result['requestGPUInfos'].append(k.to_map() if k else None)
        if self.request_memory is not None:
            result['requestMemory'] = self.request_memory
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestCPU') is not None:
            self.request_cpu = m.get('requestCPU')
        if m.get('requestGPU') is not None:
            self.request_gpu = m.get('requestGPU')
        self.request_gpuinfos = []
        if m.get('requestGPUInfos') is not None:
            for k in m.get('requestGPUInfos'):
                temp_model = GPUInfo()
                self.request_gpuinfos.append(temp_model.from_map(k))
        if m.get('requestMemory') is not None:
            self.request_memory = m.get('requestMemory')
        return self


class GetResourceGroupRequestResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetResourceGroupRequestResponseBody = None,
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
            temp_model = GetResourceGroupRequestResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetResourceGroupTotalRequest(TeaModel):
    def __init__(
        self,
        resource_group_id: str = None,
    ):
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.resource_group_id is not None:
            result['ResourceGroupID'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ResourceGroupID') is not None:
            self.resource_group_id = m.get('ResourceGroupID')
        return self


class GetResourceGroupTotalResponseBody(TeaModel):
    def __init__(
        self,
        total_cpu: int = None,
        total_gpu: int = None,
        total_gpuinfos: List[GPUInfo] = None,
        total_memory: int = None,
    ):
        self.total_cpu = total_cpu
        self.total_gpu = total_gpu
        self.total_gpuinfos = total_gpuinfos
        self.total_memory = total_memory

    def validate(self):
        if self.total_gpuinfos:
            for k in self.total_gpuinfos:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.total_cpu is not None:
            result['totalCPU'] = self.total_cpu
        if self.total_gpu is not None:
            result['totalGPU'] = self.total_gpu
        result['totalGPUInfos'] = []
        if self.total_gpuinfos is not None:
            for k in self.total_gpuinfos:
                result['totalGPUInfos'].append(k.to_map() if k else None)
        if self.total_memory is not None:
            result['totalMemory'] = self.total_memory
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('totalCPU') is not None:
            self.total_cpu = m.get('totalCPU')
        if m.get('totalGPU') is not None:
            self.total_gpu = m.get('totalGPU')
        self.total_gpuinfos = []
        if m.get('totalGPUInfos') is not None:
            for k in m.get('totalGPUInfos'):
                temp_model = GPUInfo()
                self.total_gpuinfos.append(temp_model.from_map(k))
        if m.get('totalMemory') is not None:
            self.total_memory = m.get('totalMemory')
        return self


class GetResourceGroupTotalResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetResourceGroupTotalResponseBody = None,
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
            temp_model = GetResourceGroupTotalResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetServiceIdentityRoleResponseBody(TeaModel):
    def __init__(
        self,
        exist: bool = None,
        request_id: str = None,
        role_name: str = None,
    ):
        self.exist = exist
        self.request_id = request_id
        self.role_name = role_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.exist is not None:
            result['Exist'] = self.exist
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.role_name is not None:
            result['RoleName'] = self.role_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Exist') is not None:
            self.exist = m.get('Exist')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('RoleName') is not None:
            self.role_name = m.get('RoleName')
        return self


class GetServiceIdentityRoleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetServiceIdentityRoleResponseBody = None,
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
            temp_model = GetServiceIdentityRoleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetSpotPriceHistoryRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        sort_by: str = None,
        start_time: str = None,
    ):
        self.end_time = end_time
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        self.sort_by = sort_by
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
        if self.order is not None:
            result['Order'] = self.order
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        return self


class GetSpotPriceHistoryResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        spot_price_history: List[SpotPriceItem] = None,
        total_count: int = None,
    ):
        self.request_id = request_id
        self.spot_price_history = spot_price_history
        self.total_count = total_count

    def validate(self):
        if self.spot_price_history:
            for k in self.spot_price_history:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['SpotPriceHistory'] = []
        if self.spot_price_history is not None:
            for k in self.spot_price_history:
                result['SpotPriceHistory'].append(k.to_map() if k else None)
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.spot_price_history = []
        if m.get('SpotPriceHistory') is not None:
            for k in m.get('SpotPriceHistory'):
                temp_model = SpotPriceItem()
                self.spot_price_history.append(temp_model.from_map(k))
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class GetSpotPriceHistoryResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetSpotPriceHistoryResponseBody = None,
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
            temp_model = GetSpotPriceHistoryResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetSpotStockPreviewResponseBody(TeaModel):
    def __init__(
        self,
        instance_type: str = None,
        request_id: str = None,
        stock_status: str = None,
    ):
        self.instance_type = instance_type
        self.request_id = request_id
        self.stock_status = stock_status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.stock_status is not None:
            result['StockStatus'] = self.stock_status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('StockStatus') is not None:
            self.stock_status = m.get('StockStatus')
        return self


class GetSpotStockPreviewResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetSpotStockPreviewResponseBody = None,
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
            temp_model = GetSpotStockPreviewResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetTokenRequest(TeaModel):
    def __init__(
        self,
        expire_time: int = None,
        training_job_id: str = None,
    ):
        self.expire_time = expire_time
        # This parameter is required.
        self.training_job_id = training_job_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.expire_time is not None:
            result['ExpireTime'] = self.expire_time
        if self.training_job_id is not None:
            result['TrainingJobId'] = self.training_job_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ExpireTime') is not None:
            self.expire_time = m.get('ExpireTime')
        if m.get('TrainingJobId') is not None:
            self.training_job_id = m.get('TrainingJobId')
        return self


class GetTokenResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        token: str = None,
    ):
        self.request_id = request_id
        self.token = token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.token is not None:
            result['Token'] = self.token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
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


class GetTrainingJobRequest(TeaModel):
    def __init__(
        self,
        token: str = None,
    ):
        self.token = token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.token is not None:
            result['Token'] = self.token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Token') is not None:
            self.token = m.get('Token')
        return self


class GetTrainingJobResponseBodyComputeResourceInstanceSpec(TeaModel):
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


class GetTrainingJobResponseBodyComputeResourceSpotSpec(TeaModel):
    def __init__(
        self,
        spot_discount_limit: float = None,
        spot_strategy: str = None,
    ):
        self.spot_discount_limit = spot_discount_limit
        self.spot_strategy = spot_strategy

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.spot_discount_limit is not None:
            result['SpotDiscountLimit'] = self.spot_discount_limit
        if self.spot_strategy is not None:
            result['SpotStrategy'] = self.spot_strategy
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SpotDiscountLimit') is not None:
            self.spot_discount_limit = m.get('SpotDiscountLimit')
        if m.get('SpotStrategy') is not None:
            self.spot_strategy = m.get('SpotStrategy')
        return self


class GetTrainingJobResponseBodyComputeResource(TeaModel):
    def __init__(
        self,
        ecs_count: int = None,
        ecs_spec: str = None,
        instance_count: int = None,
        instance_spec: GetTrainingJobResponseBodyComputeResourceInstanceSpec = None,
        resource_id: str = None,
        spot_spec: GetTrainingJobResponseBodyComputeResourceSpotSpec = None,
        use_spot_instance: bool = None,
    ):
        self.ecs_count = ecs_count
        self.ecs_spec = ecs_spec
        self.instance_count = instance_count
        self.instance_spec = instance_spec
        self.resource_id = resource_id
        self.spot_spec = spot_spec
        self.use_spot_instance = use_spot_instance

    def validate(self):
        if self.instance_spec:
            self.instance_spec.validate()
        if self.spot_spec:
            self.spot_spec.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.ecs_count is not None:
            result['EcsCount'] = self.ecs_count
        if self.ecs_spec is not None:
            result['EcsSpec'] = self.ecs_spec
        if self.instance_count is not None:
            result['InstanceCount'] = self.instance_count
        if self.instance_spec is not None:
            result['InstanceSpec'] = self.instance_spec.to_map()
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.spot_spec is not None:
            result['SpotSpec'] = self.spot_spec.to_map()
        if self.use_spot_instance is not None:
            result['UseSpotInstance'] = self.use_spot_instance
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EcsCount') is not None:
            self.ecs_count = m.get('EcsCount')
        if m.get('EcsSpec') is not None:
            self.ecs_spec = m.get('EcsSpec')
        if m.get('InstanceCount') is not None:
            self.instance_count = m.get('InstanceCount')
        if m.get('InstanceSpec') is not None:
            temp_model = GetTrainingJobResponseBodyComputeResourceInstanceSpec()
            self.instance_spec = temp_model.from_map(m['InstanceSpec'])
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('SpotSpec') is not None:
            temp_model = GetTrainingJobResponseBodyComputeResourceSpotSpec()
            self.spot_spec = temp_model.from_map(m['SpotSpec'])
        if m.get('UseSpotInstance') is not None:
            self.use_spot_instance = m.get('UseSpotInstance')
        return self


class GetTrainingJobResponseBodyExperimentConfig(TeaModel):
    def __init__(
        self,
        experiment_id: str = None,
        experiment_name: str = None,
    ):
        self.experiment_id = experiment_id
        self.experiment_name = experiment_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.experiment_id is not None:
            result['ExperimentId'] = self.experiment_id
        if self.experiment_name is not None:
            result['ExperimentName'] = self.experiment_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ExperimentId') is not None:
            self.experiment_id = m.get('ExperimentId')
        if m.get('ExperimentName') is not None:
            self.experiment_name = m.get('ExperimentName')
        return self


class GetTrainingJobResponseBodyHyperParameters(TeaModel):
    def __init__(
        self,
        name: str = None,
        value: str = None,
    ):
        self.name = name
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class GetTrainingJobResponseBodyInputChannels(TeaModel):
    def __init__(
        self,
        dataset_id: str = None,
        input_uri: str = None,
        name: str = None,
    ):
        self.dataset_id = dataset_id
        self.input_uri = input_uri
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.dataset_id is not None:
            result['DatasetId'] = self.dataset_id
        if self.input_uri is not None:
            result['InputUri'] = self.input_uri
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DatasetId') is not None:
            self.dataset_id = m.get('DatasetId')
        if m.get('InputUri') is not None:
            self.input_uri = m.get('InputUri')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class GetTrainingJobResponseBodyInstances(TeaModel):
    def __init__(
        self,
        name: str = None,
        role: str = None,
        status: str = None,
    ):
        self.name = name
        self.role = role
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.role is not None:
            result['Role'] = self.role
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Role') is not None:
            self.role = m.get('Role')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class GetTrainingJobResponseBodyLabels(TeaModel):
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


class GetTrainingJobResponseBodyLatestMetrics(TeaModel):
    def __init__(
        self,
        name: str = None,
        timestamp: str = None,
        value: float = None,
    ):
        self.name = name
        self.timestamp = timestamp
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.timestamp is not None:
            result['Timestamp'] = self.timestamp
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Timestamp') is not None:
            self.timestamp = m.get('Timestamp')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class GetTrainingJobResponseBodyLatestProgressOverallProgress(TeaModel):
    def __init__(
        self,
        timestamp: str = None,
        value: float = None,
    ):
        self.timestamp = timestamp
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.timestamp is not None:
            result['Timestamp'] = self.timestamp
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Timestamp') is not None:
            self.timestamp = m.get('Timestamp')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class GetTrainingJobResponseBodyLatestProgressRemainingTime(TeaModel):
    def __init__(
        self,
        timestamp: str = None,
        value: int = None,
    ):
        self.timestamp = timestamp
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.timestamp is not None:
            result['Timestamp'] = self.timestamp
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Timestamp') is not None:
            self.timestamp = m.get('Timestamp')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class GetTrainingJobResponseBodyLatestProgress(TeaModel):
    def __init__(
        self,
        overall_progress: GetTrainingJobResponseBodyLatestProgressOverallProgress = None,
        remaining_time: GetTrainingJobResponseBodyLatestProgressRemainingTime = None,
    ):
        self.overall_progress = overall_progress
        self.remaining_time = remaining_time

    def validate(self):
        if self.overall_progress:
            self.overall_progress.validate()
        if self.remaining_time:
            self.remaining_time.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.overall_progress is not None:
            result['OverallProgress'] = self.overall_progress.to_map()
        if self.remaining_time is not None:
            result['RemainingTime'] = self.remaining_time.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('OverallProgress') is not None:
            temp_model = GetTrainingJobResponseBodyLatestProgressOverallProgress()
            self.overall_progress = temp_model.from_map(m['OverallProgress'])
        if m.get('RemainingTime') is not None:
            temp_model = GetTrainingJobResponseBodyLatestProgressRemainingTime()
            self.remaining_time = temp_model.from_map(m['RemainingTime'])
        return self


class GetTrainingJobResponseBodyOutputChannels(TeaModel):
    def __init__(
        self,
        dataset_id: str = None,
        name: str = None,
        output_uri: str = None,
    ):
        self.dataset_id = dataset_id
        self.name = name
        self.output_uri = output_uri

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.dataset_id is not None:
            result['DatasetId'] = self.dataset_id
        if self.name is not None:
            result['Name'] = self.name
        if self.output_uri is not None:
            result['OutputUri'] = self.output_uri
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DatasetId') is not None:
            self.dataset_id = m.get('DatasetId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('OutputUri') is not None:
            self.output_uri = m.get('OutputUri')
        return self


class GetTrainingJobResponseBodyOutputModel(TeaModel):
    def __init__(
        self,
        output_channel_name: str = None,
        uri: str = None,
    ):
        self.output_channel_name = output_channel_name
        self.uri = uri

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.output_channel_name is not None:
            result['OutputChannelName'] = self.output_channel_name
        if self.uri is not None:
            result['Uri'] = self.uri
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('OutputChannelName') is not None:
            self.output_channel_name = m.get('OutputChannelName')
        if m.get('Uri') is not None:
            self.uri = m.get('Uri')
        return self


class GetTrainingJobResponseBodyScheduler(TeaModel):
    def __init__(
        self,
        max_running_time_in_seconds: int = None,
    ):
        self.max_running_time_in_seconds = max_running_time_in_seconds

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.max_running_time_in_seconds is not None:
            result['MaxRunningTimeInSeconds'] = self.max_running_time_in_seconds
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MaxRunningTimeInSeconds') is not None:
            self.max_running_time_in_seconds = m.get('MaxRunningTimeInSeconds')
        return self


class GetTrainingJobResponseBodySettings(TeaModel):
    def __init__(
        self,
        aimaster_type: str = None,
        enable_error_monitoring_in_aimaster: bool = None,
        error_monitoring_args: str = None,
        priority: int = None,
    ):
        self.aimaster_type = aimaster_type
        self.enable_error_monitoring_in_aimaster = enable_error_monitoring_in_aimaster
        self.error_monitoring_args = error_monitoring_args
        self.priority = priority

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.aimaster_type is not None:
            result['AIMasterType'] = self.aimaster_type
        if self.enable_error_monitoring_in_aimaster is not None:
            result['EnableErrorMonitoringInAIMaster'] = self.enable_error_monitoring_in_aimaster
        if self.error_monitoring_args is not None:
            result['ErrorMonitoringArgs'] = self.error_monitoring_args
        if self.priority is not None:
            result['Priority'] = self.priority
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AIMasterType') is not None:
            self.aimaster_type = m.get('AIMasterType')
        if m.get('EnableErrorMonitoringInAIMaster') is not None:
            self.enable_error_monitoring_in_aimaster = m.get('EnableErrorMonitoringInAIMaster')
        if m.get('ErrorMonitoringArgs') is not None:
            self.error_monitoring_args = m.get('ErrorMonitoringArgs')
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        return self


class GetTrainingJobResponseBodyStatusTransitions(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        reason_code: str = None,
        reason_message: str = None,
        start_time: str = None,
        status: str = None,
    ):
        self.end_time = end_time
        self.reason_code = reason_code
        self.reason_message = reason_message
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
        if self.reason_code is not None:
            result['ReasonCode'] = self.reason_code
        if self.reason_message is not None:
            result['ReasonMessage'] = self.reason_message
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('ReasonCode') is not None:
            self.reason_code = m.get('ReasonCode')
        if m.get('ReasonMessage') is not None:
            self.reason_message = m.get('ReasonMessage')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class GetTrainingJobResponseBodyUserVpc(TeaModel):
    def __init__(
        self,
        extended_cidrs: List[str] = None,
        security_group_id: str = None,
        switch_id: str = None,
        vpc_id: str = None,
    ):
        self.extended_cidrs = extended_cidrs
        self.security_group_id = security_group_id
        self.switch_id = switch_id
        self.vpc_id = vpc_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.extended_cidrs is not None:
            result['ExtendedCIDRs'] = self.extended_cidrs
        if self.security_group_id is not None:
            result['SecurityGroupId'] = self.security_group_id
        if self.switch_id is not None:
            result['SwitchId'] = self.switch_id
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ExtendedCIDRs') is not None:
            self.extended_cidrs = m.get('ExtendedCIDRs')
        if m.get('SecurityGroupId') is not None:
            self.security_group_id = m.get('SecurityGroupId')
        if m.get('SwitchId') is not None:
            self.switch_id = m.get('SwitchId')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        return self


class GetTrainingJobResponseBody(TeaModel):
    def __init__(
        self,
        algorithm_id: str = None,
        algorithm_name: str = None,
        algorithm_provider: str = None,
        algorithm_spec: AlgorithmSpec = None,
        algorithm_version: str = None,
        compute_resource: GetTrainingJobResponseBodyComputeResource = None,
        duration: int = None,
        environments: Dict[str, str] = None,
        experiment_config: GetTrainingJobResponseBodyExperimentConfig = None,
        gmt_create_time: str = None,
        gmt_modified_time: str = None,
        hyper_parameters: List[GetTrainingJobResponseBodyHyperParameters] = None,
        input_channels: List[GetTrainingJobResponseBodyInputChannels] = None,
        instances: List[GetTrainingJobResponseBodyInstances] = None,
        is_temp_algo: bool = None,
        labels: List[GetTrainingJobResponseBodyLabels] = None,
        latest_metrics: List[GetTrainingJobResponseBodyLatestMetrics] = None,
        latest_progress: GetTrainingJobResponseBodyLatestProgress = None,
        output_channels: List[GetTrainingJobResponseBodyOutputChannels] = None,
        output_model: GetTrainingJobResponseBodyOutputModel = None,
        python_requirements: List[str] = None,
        reason_code: str = None,
        reason_message: str = None,
        request_id: str = None,
        role_arn: str = None,
        scheduler: GetTrainingJobResponseBodyScheduler = None,
        settings: GetTrainingJobResponseBodySettings = None,
        status: str = None,
        status_transitions: List[GetTrainingJobResponseBodyStatusTransitions] = None,
        training_job_description: str = None,
        training_job_id: str = None,
        training_job_name: str = None,
        training_job_url: str = None,
        user_id: str = None,
        user_vpc: GetTrainingJobResponseBodyUserVpc = None,
        workspace_id: str = None,
    ):
        self.algorithm_id = algorithm_id
        self.algorithm_name = algorithm_name
        self.algorithm_provider = algorithm_provider
        self.algorithm_spec = algorithm_spec
        self.algorithm_version = algorithm_version
        self.compute_resource = compute_resource
        self.duration = duration
        self.environments = environments
        self.experiment_config = experiment_config
        self.gmt_create_time = gmt_create_time
        self.gmt_modified_time = gmt_modified_time
        self.hyper_parameters = hyper_parameters
        self.input_channels = input_channels
        self.instances = instances
        self.is_temp_algo = is_temp_algo
        self.labels = labels
        self.latest_metrics = latest_metrics
        self.latest_progress = latest_progress
        self.output_channels = output_channels
        self.output_model = output_model
        self.python_requirements = python_requirements
        self.reason_code = reason_code
        self.reason_message = reason_message
        self.request_id = request_id
        self.role_arn = role_arn
        self.scheduler = scheduler
        self.settings = settings
        self.status = status
        self.status_transitions = status_transitions
        self.training_job_description = training_job_description
        self.training_job_id = training_job_id
        self.training_job_name = training_job_name
        self.training_job_url = training_job_url
        self.user_id = user_id
        self.user_vpc = user_vpc
        self.workspace_id = workspace_id

    def validate(self):
        if self.algorithm_spec:
            self.algorithm_spec.validate()
        if self.compute_resource:
            self.compute_resource.validate()
        if self.experiment_config:
            self.experiment_config.validate()
        if self.hyper_parameters:
            for k in self.hyper_parameters:
                if k:
                    k.validate()
        if self.input_channels:
            for k in self.input_channels:
                if k:
                    k.validate()
        if self.instances:
            for k in self.instances:
                if k:
                    k.validate()
        if self.labels:
            for k in self.labels:
                if k:
                    k.validate()
        if self.latest_metrics:
            for k in self.latest_metrics:
                if k:
                    k.validate()
        if self.latest_progress:
            self.latest_progress.validate()
        if self.output_channels:
            for k in self.output_channels:
                if k:
                    k.validate()
        if self.output_model:
            self.output_model.validate()
        if self.scheduler:
            self.scheduler.validate()
        if self.settings:
            self.settings.validate()
        if self.status_transitions:
            for k in self.status_transitions:
                if k:
                    k.validate()
        if self.user_vpc:
            self.user_vpc.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.algorithm_id is not None:
            result['AlgorithmId'] = self.algorithm_id
        if self.algorithm_name is not None:
            result['AlgorithmName'] = self.algorithm_name
        if self.algorithm_provider is not None:
            result['AlgorithmProvider'] = self.algorithm_provider
        if self.algorithm_spec is not None:
            result['AlgorithmSpec'] = self.algorithm_spec.to_map()
        if self.algorithm_version is not None:
            result['AlgorithmVersion'] = self.algorithm_version
        if self.compute_resource is not None:
            result['ComputeResource'] = self.compute_resource.to_map()
        if self.duration is not None:
            result['Duration'] = self.duration
        if self.environments is not None:
            result['Environments'] = self.environments
        if self.experiment_config is not None:
            result['ExperimentConfig'] = self.experiment_config.to_map()
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        result['HyperParameters'] = []
        if self.hyper_parameters is not None:
            for k in self.hyper_parameters:
                result['HyperParameters'].append(k.to_map() if k else None)
        result['InputChannels'] = []
        if self.input_channels is not None:
            for k in self.input_channels:
                result['InputChannels'].append(k.to_map() if k else None)
        result['Instances'] = []
        if self.instances is not None:
            for k in self.instances:
                result['Instances'].append(k.to_map() if k else None)
        if self.is_temp_algo is not None:
            result['IsTempAlgo'] = self.is_temp_algo
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        result['LatestMetrics'] = []
        if self.latest_metrics is not None:
            for k in self.latest_metrics:
                result['LatestMetrics'].append(k.to_map() if k else None)
        if self.latest_progress is not None:
            result['LatestProgress'] = self.latest_progress.to_map()
        result['OutputChannels'] = []
        if self.output_channels is not None:
            for k in self.output_channels:
                result['OutputChannels'].append(k.to_map() if k else None)
        if self.output_model is not None:
            result['OutputModel'] = self.output_model.to_map()
        if self.python_requirements is not None:
            result['PythonRequirements'] = self.python_requirements
        if self.reason_code is not None:
            result['ReasonCode'] = self.reason_code
        if self.reason_message is not None:
            result['ReasonMessage'] = self.reason_message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.role_arn is not None:
            result['RoleArn'] = self.role_arn
        if self.scheduler is not None:
            result['Scheduler'] = self.scheduler.to_map()
        if self.settings is not None:
            result['Settings'] = self.settings.to_map()
        if self.status is not None:
            result['Status'] = self.status
        result['StatusTransitions'] = []
        if self.status_transitions is not None:
            for k in self.status_transitions:
                result['StatusTransitions'].append(k.to_map() if k else None)
        if self.training_job_description is not None:
            result['TrainingJobDescription'] = self.training_job_description
        if self.training_job_id is not None:
            result['TrainingJobId'] = self.training_job_id
        if self.training_job_name is not None:
            result['TrainingJobName'] = self.training_job_name
        if self.training_job_url is not None:
            result['TrainingJobUrl'] = self.training_job_url
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.user_vpc is not None:
            result['UserVpc'] = self.user_vpc.to_map()
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AlgorithmId') is not None:
            self.algorithm_id = m.get('AlgorithmId')
        if m.get('AlgorithmName') is not None:
            self.algorithm_name = m.get('AlgorithmName')
        if m.get('AlgorithmProvider') is not None:
            self.algorithm_provider = m.get('AlgorithmProvider')
        if m.get('AlgorithmSpec') is not None:
            temp_model = AlgorithmSpec()
            self.algorithm_spec = temp_model.from_map(m['AlgorithmSpec'])
        if m.get('AlgorithmVersion') is not None:
            self.algorithm_version = m.get('AlgorithmVersion')
        if m.get('ComputeResource') is not None:
            temp_model = GetTrainingJobResponseBodyComputeResource()
            self.compute_resource = temp_model.from_map(m['ComputeResource'])
        if m.get('Duration') is not None:
            self.duration = m.get('Duration')
        if m.get('Environments') is not None:
            self.environments = m.get('Environments')
        if m.get('ExperimentConfig') is not None:
            temp_model = GetTrainingJobResponseBodyExperimentConfig()
            self.experiment_config = temp_model.from_map(m['ExperimentConfig'])
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        self.hyper_parameters = []
        if m.get('HyperParameters') is not None:
            for k in m.get('HyperParameters'):
                temp_model = GetTrainingJobResponseBodyHyperParameters()
                self.hyper_parameters.append(temp_model.from_map(k))
        self.input_channels = []
        if m.get('InputChannels') is not None:
            for k in m.get('InputChannels'):
                temp_model = GetTrainingJobResponseBodyInputChannels()
                self.input_channels.append(temp_model.from_map(k))
        self.instances = []
        if m.get('Instances') is not None:
            for k in m.get('Instances'):
                temp_model = GetTrainingJobResponseBodyInstances()
                self.instances.append(temp_model.from_map(k))
        if m.get('IsTempAlgo') is not None:
            self.is_temp_algo = m.get('IsTempAlgo')
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = GetTrainingJobResponseBodyLabels()
                self.labels.append(temp_model.from_map(k))
        self.latest_metrics = []
        if m.get('LatestMetrics') is not None:
            for k in m.get('LatestMetrics'):
                temp_model = GetTrainingJobResponseBodyLatestMetrics()
                self.latest_metrics.append(temp_model.from_map(k))
        if m.get('LatestProgress') is not None:
            temp_model = GetTrainingJobResponseBodyLatestProgress()
            self.latest_progress = temp_model.from_map(m['LatestProgress'])
        self.output_channels = []
        if m.get('OutputChannels') is not None:
            for k in m.get('OutputChannels'):
                temp_model = GetTrainingJobResponseBodyOutputChannels()
                self.output_channels.append(temp_model.from_map(k))
        if m.get('OutputModel') is not None:
            temp_model = GetTrainingJobResponseBodyOutputModel()
            self.output_model = temp_model.from_map(m['OutputModel'])
        if m.get('PythonRequirements') is not None:
            self.python_requirements = m.get('PythonRequirements')
        if m.get('ReasonCode') is not None:
            self.reason_code = m.get('ReasonCode')
        if m.get('ReasonMessage') is not None:
            self.reason_message = m.get('ReasonMessage')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('RoleArn') is not None:
            self.role_arn = m.get('RoleArn')
        if m.get('Scheduler') is not None:
            temp_model = GetTrainingJobResponseBodyScheduler()
            self.scheduler = temp_model.from_map(m['Scheduler'])
        if m.get('Settings') is not None:
            temp_model = GetTrainingJobResponseBodySettings()
            self.settings = temp_model.from_map(m['Settings'])
        if m.get('Status') is not None:
            self.status = m.get('Status')
        self.status_transitions = []
        if m.get('StatusTransitions') is not None:
            for k in m.get('StatusTransitions'):
                temp_model = GetTrainingJobResponseBodyStatusTransitions()
                self.status_transitions.append(temp_model.from_map(k))
        if m.get('TrainingJobDescription') is not None:
            self.training_job_description = m.get('TrainingJobDescription')
        if m.get('TrainingJobId') is not None:
            self.training_job_id = m.get('TrainingJobId')
        if m.get('TrainingJobName') is not None:
            self.training_job_name = m.get('TrainingJobName')
        if m.get('TrainingJobUrl') is not None:
            self.training_job_url = m.get('TrainingJobUrl')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('UserVpc') is not None:
            temp_model = GetTrainingJobResponseBodyUserVpc()
            self.user_vpc = temp_model.from_map(m['UserVpc'])
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class GetTrainingJobResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetTrainingJobResponseBody = None,
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
            temp_model = GetTrainingJobResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetTrainingJobErrorInfoRequest(TeaModel):
    def __init__(
        self,
        token: str = None,
    ):
        self.token = token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.token is not None:
            result['Token'] = self.token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Token') is not None:
            self.token = m.get('Token')
        return self


class GetTrainingJobErrorInfoResponseBodyErrorInfo(TeaModel):
    def __init__(
        self,
        additional_info: str = None,
        code: str = None,
        message: str = None,
    ):
        self.additional_info = additional_info
        self.code = code
        self.message = message

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.additional_info is not None:
            result['AdditionalInfo'] = self.additional_info
        if self.code is not None:
            result['Code'] = self.code
        if self.message is not None:
            result['Message'] = self.message
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AdditionalInfo') is not None:
            self.additional_info = m.get('AdditionalInfo')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        return self


class GetTrainingJobErrorInfoResponseBody(TeaModel):
    def __init__(
        self,
        error_info: GetTrainingJobErrorInfoResponseBodyErrorInfo = None,
        request_id: str = None,
    ):
        self.error_info = error_info
        self.request_id = request_id

    def validate(self):
        if self.error_info:
            self.error_info.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.error_info is not None:
            result['ErrorInfo'] = self.error_info.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ErrorInfo') is not None:
            temp_model = GetTrainingJobErrorInfoResponseBodyErrorInfo()
            self.error_info = temp_model.from_map(m['ErrorInfo'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class GetTrainingJobErrorInfoResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetTrainingJobErrorInfoResponseBody = None,
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
            temp_model = GetTrainingJobErrorInfoResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetTrainingJobLatestMetricsRequest(TeaModel):
    def __init__(
        self,
        names: str = None,
        token: str = None,
    ):
        self.names = names
        self.token = token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.names is not None:
            result['Names'] = self.names
        if self.token is not None:
            result['Token'] = self.token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Names') is not None:
            self.names = m.get('Names')
        if m.get('Token') is not None:
            self.token = m.get('Token')
        return self


class GetTrainingJobLatestMetricsResponseBodyMetrics(TeaModel):
    def __init__(
        self,
        name: str = None,
        timestamp: str = None,
        value: float = None,
    ):
        self.name = name
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.timestamp = timestamp
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.timestamp is not None:
            result['Timestamp'] = self.timestamp
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Timestamp') is not None:
            self.timestamp = m.get('Timestamp')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class GetTrainingJobLatestMetricsResponseBody(TeaModel):
    def __init__(
        self,
        metrics: List[GetTrainingJobLatestMetricsResponseBodyMetrics] = None,
        request_id: str = None,
    ):
        self.metrics = metrics
        self.request_id = request_id

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
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.metrics = []
        if m.get('Metrics') is not None:
            for k in m.get('Metrics'):
                temp_model = GetTrainingJobLatestMetricsResponseBodyMetrics()
                self.metrics.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class GetTrainingJobLatestMetricsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetTrainingJobLatestMetricsResponseBody = None,
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
            temp_model = GetTrainingJobLatestMetricsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetUserViewMetricsRequest(TeaModel):
    def __init__(
        self,
        order: str = None,
        page_number: str = None,
        page_size: str = None,
        sort_by: str = None,
        time_step: str = None,
        user_id: str = None,
        workspace_id: str = None,
    ):
        self.order = order
        # This parameter is required.
        self.page_number = page_number
        # This parameter is required.
        self.page_size = page_size
        self.sort_by = sort_by
        self.time_step = time_step
        self.user_id = user_id
        self.workspace_id = workspace_id

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
        if self.time_step is not None:
            result['TimeStep'] = self.time_step
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
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
        if m.get('TimeStep') is not None:
            self.time_step = m.get('TimeStep')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class GetUserViewMetricsResponseBody(TeaModel):
    def __init__(
        self,
        resource_group_id: str = None,
        summary: UserViewMetric = None,
        total: int = None,
        user_metrics: List[UserViewMetric] = None,
    ):
        self.resource_group_id = resource_group_id
        self.summary = summary
        self.total = total
        self.user_metrics = user_metrics

    def validate(self):
        if self.summary:
            self.summary.validate()
        if self.user_metrics:
            for k in self.user_metrics:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.summary is not None:
            result['Summary'] = self.summary.to_map()
        if self.total is not None:
            result['Total'] = self.total
        result['UserMetrics'] = []
        if self.user_metrics is not None:
            for k in self.user_metrics:
                result['UserMetrics'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('Summary') is not None:
            temp_model = UserViewMetric()
            self.summary = temp_model.from_map(m['Summary'])
        if m.get('Total') is not None:
            self.total = m.get('Total')
        self.user_metrics = []
        if m.get('UserMetrics') is not None:
            for k in m.get('UserMetrics'):
                temp_model = UserViewMetric()
                self.user_metrics.append(temp_model.from_map(k))
        return self


class GetUserViewMetricsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetUserViewMetricsResponseBody = None,
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
            temp_model = GetUserViewMetricsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListAI4DSerivcesRequest(TeaModel):
    def __init__(
        self,
        service_type: str = None,
        workspace_id: str = None,
    ):
        self.service_type = service_type
        # This parameter is required.
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.service_type is not None:
            result['ServiceType'] = self.service_type
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ServiceType') is not None:
            self.service_type = m.get('ServiceType')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class ListAI4DSerivcesResponseBodyServices(TeaModel):
    def __init__(
        self,
        service_name: str = None,
        service_type: str = None,
    ):
        self.service_name = service_name
        self.service_type = service_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.service_name is not None:
            result['ServiceName'] = self.service_name
        if self.service_type is not None:
            result['ServiceType'] = self.service_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ServiceName') is not None:
            self.service_name = m.get('ServiceName')
        if m.get('ServiceType') is not None:
            self.service_type = m.get('ServiceType')
        return self


class ListAI4DSerivcesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        services: List[ListAI4DSerivcesResponseBodyServices] = None,
    ):
        self.request_id = request_id
        self.services = services

    def validate(self):
        if self.services:
            for k in self.services:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Services'] = []
        if self.services is not None:
            for k in self.services:
                result['Services'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.services = []
        if m.get('Services') is not None:
            for k in m.get('Services'):
                temp_model = ListAI4DSerivcesResponseBodyServices()
                self.services.append(temp_model.from_map(k))
        return self


class ListAI4DSerivcesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListAI4DSerivcesResponseBody = None,
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
            temp_model = ListAI4DSerivcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListAI4DServiceTemplatesRequest(TeaModel):
    def __init__(
        self,
        service_type: str = None,
        workspace_id: str = None,
    ):
        self.service_type = service_type
        # This parameter is required.
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.service_type is not None:
            result['ServiceType'] = self.service_type
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ServiceType') is not None:
            self.service_type = m.get('ServiceType')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class ListAI4DServiceTemplatesResponseBodyServiceTemplatesLabels(TeaModel):
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


class ListAI4DServiceTemplatesResponseBodyServiceTemplates(TeaModel):
    def __init__(
        self,
        inference_spec: Dict[str, Any] = None,
        labels: List[ListAI4DServiceTemplatesResponseBodyServiceTemplatesLabels] = None,
        service_template_description: str = None,
        service_template_doc: str = None,
        service_template_id: str = None,
        service_template_name: str = None,
    ):
        self.inference_spec = inference_spec
        self.labels = labels
        self.service_template_description = service_template_description
        self.service_template_doc = service_template_doc
        self.service_template_id = service_template_id
        self.service_template_name = service_template_name

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
        if self.inference_spec is not None:
            result['InferenceSpec'] = self.inference_spec
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        if self.service_template_description is not None:
            result['ServiceTemplateDescription'] = self.service_template_description
        if self.service_template_doc is not None:
            result['ServiceTemplateDoc'] = self.service_template_doc
        if self.service_template_id is not None:
            result['ServiceTemplateId'] = self.service_template_id
        if self.service_template_name is not None:
            result['ServiceTemplateName'] = self.service_template_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InferenceSpec') is not None:
            self.inference_spec = m.get('InferenceSpec')
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = ListAI4DServiceTemplatesResponseBodyServiceTemplatesLabels()
                self.labels.append(temp_model.from_map(k))
        if m.get('ServiceTemplateDescription') is not None:
            self.service_template_description = m.get('ServiceTemplateDescription')
        if m.get('ServiceTemplateDoc') is not None:
            self.service_template_doc = m.get('ServiceTemplateDoc')
        if m.get('ServiceTemplateId') is not None:
            self.service_template_id = m.get('ServiceTemplateId')
        if m.get('ServiceTemplateName') is not None:
            self.service_template_name = m.get('ServiceTemplateName')
        return self


class ListAI4DServiceTemplatesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        service_templates: List[ListAI4DServiceTemplatesResponseBodyServiceTemplates] = None,
    ):
        self.request_id = request_id
        self.service_templates = service_templates

    def validate(self):
        if self.service_templates:
            for k in self.service_templates:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['ServiceTemplates'] = []
        if self.service_templates is not None:
            for k in self.service_templates:
                result['ServiceTemplates'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.service_templates = []
        if m.get('ServiceTemplates') is not None:
            for k in m.get('ServiceTemplates'):
                temp_model = ListAI4DServiceTemplatesResponseBodyServiceTemplates()
                self.service_templates.append(temp_model.from_map(k))
        return self


class ListAI4DServiceTemplatesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListAI4DServiceTemplatesResponseBody = None,
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
            temp_model = ListAI4DServiceTemplatesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListAlgorithmVersionsRequest(TeaModel):
    def __init__(
        self,
        page_number: int = None,
        page_size: int = None,
    ):
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class ListAlgorithmVersionsResponseBodyAlgorithmVersions(TeaModel):
    def __init__(
        self,
        algorithm_id: str = None,
        algorithm_name: str = None,
        algorithm_provider: str = None,
        algorithm_version: str = None,
        gmt_create_time: str = None,
        gmt_modified_time: str = None,
        tenant_id: str = None,
        user_id: str = None,
    ):
        self.algorithm_id = algorithm_id
        self.algorithm_name = algorithm_name
        self.algorithm_provider = algorithm_provider
        self.algorithm_version = algorithm_version
        self.gmt_create_time = gmt_create_time
        self.gmt_modified_time = gmt_modified_time
        self.tenant_id = tenant_id
        self.user_id = user_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.algorithm_id is not None:
            result['AlgorithmId'] = self.algorithm_id
        if self.algorithm_name is not None:
            result['AlgorithmName'] = self.algorithm_name
        if self.algorithm_provider is not None:
            result['AlgorithmProvider'] = self.algorithm_provider
        if self.algorithm_version is not None:
            result['AlgorithmVersion'] = self.algorithm_version
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.tenant_id is not None:
            result['TenantId'] = self.tenant_id
        if self.user_id is not None:
            result['UserId'] = self.user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AlgorithmId') is not None:
            self.algorithm_id = m.get('AlgorithmId')
        if m.get('AlgorithmName') is not None:
            self.algorithm_name = m.get('AlgorithmName')
        if m.get('AlgorithmProvider') is not None:
            self.algorithm_provider = m.get('AlgorithmProvider')
        if m.get('AlgorithmVersion') is not None:
            self.algorithm_version = m.get('AlgorithmVersion')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('TenantId') is not None:
            self.tenant_id = m.get('TenantId')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        return self


class ListAlgorithmVersionsResponseBody(TeaModel):
    def __init__(
        self,
        algorithm_versions: List[ListAlgorithmVersionsResponseBodyAlgorithmVersions] = None,
        request_id: str = None,
        total_count: int = None,
    ):
        self.algorithm_versions = algorithm_versions
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.algorithm_versions:
            for k in self.algorithm_versions:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['AlgorithmVersions'] = []
        if self.algorithm_versions is not None:
            for k in self.algorithm_versions:
                result['AlgorithmVersions'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.algorithm_versions = []
        if m.get('AlgorithmVersions') is not None:
            for k in m.get('AlgorithmVersions'):
                temp_model = ListAlgorithmVersionsResponseBodyAlgorithmVersions()
                self.algorithm_versions.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListAlgorithmVersionsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListAlgorithmVersionsResponseBody = None,
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
            temp_model = ListAlgorithmVersionsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListAlgorithmsRequest(TeaModel):
    def __init__(
        self,
        algorithm_id: str = None,
        algorithm_name: str = None,
        algorithm_provider: str = None,
        page_number: int = None,
        page_size: int = None,
        workspace_id: str = None,
    ):
        self.algorithm_id = algorithm_id
        self.algorithm_name = algorithm_name
        self.algorithm_provider = algorithm_provider
        self.page_number = page_number
        self.page_size = page_size
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.algorithm_id is not None:
            result['AlgorithmId'] = self.algorithm_id
        if self.algorithm_name is not None:
            result['AlgorithmName'] = self.algorithm_name
        if self.algorithm_provider is not None:
            result['AlgorithmProvider'] = self.algorithm_provider
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AlgorithmId') is not None:
            self.algorithm_id = m.get('AlgorithmId')
        if m.get('AlgorithmName') is not None:
            self.algorithm_name = m.get('AlgorithmName')
        if m.get('AlgorithmProvider') is not None:
            self.algorithm_provider = m.get('AlgorithmProvider')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class ListAlgorithmsResponseBodyAlgorithms(TeaModel):
    def __init__(
        self,
        algorithm_description: str = None,
        algorithm_id: str = None,
        algorithm_name: str = None,
        algorithm_provider: str = None,
        display_name: str = None,
        gmt_create_time: str = None,
        gmt_modified_time: str = None,
        user_id: str = None,
        workspace_id: str = None,
    ):
        self.algorithm_description = algorithm_description
        self.algorithm_id = algorithm_id
        self.algorithm_name = algorithm_name
        self.algorithm_provider = algorithm_provider
        self.display_name = display_name
        self.gmt_create_time = gmt_create_time
        self.gmt_modified_time = gmt_modified_time
        self.user_id = user_id
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.algorithm_description is not None:
            result['AlgorithmDescription'] = self.algorithm_description
        if self.algorithm_id is not None:
            result['AlgorithmId'] = self.algorithm_id
        if self.algorithm_name is not None:
            result['AlgorithmName'] = self.algorithm_name
        if self.algorithm_provider is not None:
            result['AlgorithmProvider'] = self.algorithm_provider
        if self.display_name is not None:
            result['DisplayName'] = self.display_name
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AlgorithmDescription') is not None:
            self.algorithm_description = m.get('AlgorithmDescription')
        if m.get('AlgorithmId') is not None:
            self.algorithm_id = m.get('AlgorithmId')
        if m.get('AlgorithmName') is not None:
            self.algorithm_name = m.get('AlgorithmName')
        if m.get('AlgorithmProvider') is not None:
            self.algorithm_provider = m.get('AlgorithmProvider')
        if m.get('DisplayName') is not None:
            self.display_name = m.get('DisplayName')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class ListAlgorithmsResponseBody(TeaModel):
    def __init__(
        self,
        algorithms: List[ListAlgorithmsResponseBodyAlgorithms] = None,
        request_id: str = None,
        total_count: int = None,
    ):
        self.algorithms = algorithms
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.algorithms:
            for k in self.algorithms:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Algorithms'] = []
        if self.algorithms is not None:
            for k in self.algorithms:
                result['Algorithms'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.algorithms = []
        if m.get('Algorithms') is not None:
            for k in m.get('Algorithms'):
                temp_model = ListAlgorithmsResponseBodyAlgorithms()
                self.algorithms.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListAlgorithmsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListAlgorithmsResponseBody = None,
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
            temp_model = ListAlgorithmsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListComponentVersionSnapshotsRequest(TeaModel):
    def __init__(
        self,
        component_id: str = None,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        snapshot_id: str = None,
        sort_by: str = None,
        version: str = None,
    ):
        # This parameter is required.
        self.component_id = component_id
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        self.snapshot_id = snapshot_id
        self.sort_by = sort_by
        # This parameter is required.
        self.version = version

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.component_id is not None:
            result['ComponentId'] = self.component_id
        if self.order is not None:
            result['Order'] = self.order
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.snapshot_id is not None:
            result['SnapshotId'] = self.snapshot_id
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.version is not None:
            result['Version'] = self.version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComponentId') is not None:
            self.component_id = m.get('ComponentId')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('SnapshotId') is not None:
            self.snapshot_id = m.get('SnapshotId')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        return self


class ListComponentVersionSnapshotsResponseBodySnapshots(TeaModel):
    def __init__(
        self,
        component_id: str = None,
        description: str = None,
        is_current_version: bool = None,
        snapshot_id: str = None,
        tenant_id: str = None,
        user_id: str = None,
        version: str = None,
        workspace_id: str = None,
    ):
        self.component_id = component_id
        self.description = description
        self.is_current_version = is_current_version
        self.snapshot_id = snapshot_id
        self.tenant_id = tenant_id
        self.user_id = user_id
        self.version = version
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.component_id is not None:
            result['ComponentId'] = self.component_id
        if self.description is not None:
            result['Description'] = self.description
        if self.is_current_version is not None:
            result['IsCurrentVersion'] = self.is_current_version
        if self.snapshot_id is not None:
            result['SnapshotId'] = self.snapshot_id
        if self.tenant_id is not None:
            result['TenantId'] = self.tenant_id
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.version is not None:
            result['Version'] = self.version
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComponentId') is not None:
            self.component_id = m.get('ComponentId')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('IsCurrentVersion') is not None:
            self.is_current_version = m.get('IsCurrentVersion')
        if m.get('SnapshotId') is not None:
            self.snapshot_id = m.get('SnapshotId')
        if m.get('TenantId') is not None:
            self.tenant_id = m.get('TenantId')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class ListComponentVersionSnapshotsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        snapshots: List[ListComponentVersionSnapshotsResponseBodySnapshots] = None,
        total_count: int = None,
    ):
        self.request_id = request_id
        self.snapshots = snapshots
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
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Snapshots'] = []
        if self.snapshots is not None:
            for k in self.snapshots:
                result['Snapshots'].append(k.to_map() if k else None)
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.snapshots = []
        if m.get('Snapshots') is not None:
            for k in m.get('Snapshots'):
                temp_model = ListComponentVersionSnapshotsResponseBodySnapshots()
                self.snapshots.append(temp_model.from_map(k))
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListComponentVersionSnapshotsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListComponentVersionSnapshotsResponseBody = None,
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
            temp_model = ListComponentVersionSnapshotsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListComponentVersionsRequest(TeaModel):
    def __init__(
        self,
        labels: Dict[str, str] = None,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        sort_by: str = None,
        version: str = None,
    ):
        self.labels = labels
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        self.sort_by = sort_by
        self.version = version

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.labels is not None:
            result['Labels'] = self.labels
        if self.order is not None:
            result['Order'] = self.order
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.version is not None:
            result['Version'] = self.version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Labels') is not None:
            self.labels = m.get('Labels')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        return self


class ListComponentVersionsShrinkRequest(TeaModel):
    def __init__(
        self,
        labels_shrink: str = None,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        sort_by: str = None,
        version: str = None,
    ):
        self.labels_shrink = labels_shrink
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        self.sort_by = sort_by
        self.version = version

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.labels_shrink is not None:
            result['Labels'] = self.labels_shrink
        if self.order is not None:
            result['Order'] = self.order
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.version is not None:
            result['Version'] = self.version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Labels') is not None:
            self.labels_shrink = m.get('Labels')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        return self


class ListComponentVersionsResponseBodyComponentVersions(TeaModel):
    def __init__(
        self,
        component_id: str = None,
        gmt_create_time: str = None,
        gmt_modified_time: str = None,
        labels: List[Label] = None,
        name: str = None,
        provider: str = None,
        status: str = None,
        tenant_id: str = None,
        user_id: str = None,
        version: str = None,
        workspace_id: str = None,
    ):
        self.component_id = component_id
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.gmt_create_time = gmt_create_time
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.gmt_modified_time = gmt_modified_time
        self.labels = labels
        self.name = name
        self.provider = provider
        self.status = status
        self.tenant_id = tenant_id
        self.user_id = user_id
        self.version = version
        self.workspace_id = workspace_id

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
        if self.component_id is not None:
            result['ComponentId'] = self.component_id
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        if self.name is not None:
            result['Name'] = self.name
        if self.provider is not None:
            result['Provider'] = self.provider
        if self.status is not None:
            result['Status'] = self.status
        if self.tenant_id is not None:
            result['TenantId'] = self.tenant_id
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.version is not None:
            result['Version'] = self.version
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComponentId') is not None:
            self.component_id = m.get('ComponentId')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = Label()
                self.labels.append(temp_model.from_map(k))
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Provider') is not None:
            self.provider = m.get('Provider')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('TenantId') is not None:
            self.tenant_id = m.get('TenantId')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class ListComponentVersionsResponseBody(TeaModel):
    def __init__(
        self,
        component_versions: List[ListComponentVersionsResponseBodyComponentVersions] = None,
        request_id: str = None,
        total_count: int = None,
    ):
        self.component_versions = component_versions
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.component_versions:
            for k in self.component_versions:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['ComponentVersions'] = []
        if self.component_versions is not None:
            for k in self.component_versions:
                result['ComponentVersions'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.component_versions = []
        if m.get('ComponentVersions') is not None:
            for k in m.get('ComponentVersions'):
                temp_model = ListComponentVersionsResponseBodyComponentVersions()
                self.component_versions.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListComponentVersionsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListComponentVersionsResponseBody = None,
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
            temp_model = ListComponentVersionsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListComponentsRequest(TeaModel):
    def __init__(
        self,
        component_id: str = None,
        component_ids: str = None,
        labels: Dict[str, Any] = None,
        name: str = None,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        provider: str = None,
        sort_by: str = None,
        workspace_id: str = None,
    ):
        self.component_id = component_id
        self.component_ids = component_ids
        self.labels = labels
        self.name = name
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        self.provider = provider
        self.sort_by = sort_by
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.component_id is not None:
            result['ComponentId'] = self.component_id
        if self.component_ids is not None:
            result['ComponentIds'] = self.component_ids
        if self.labels is not None:
            result['Labels'] = self.labels
        if self.name is not None:
            result['Name'] = self.name
        if self.order is not None:
            result['Order'] = self.order
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.provider is not None:
            result['Provider'] = self.provider
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComponentId') is not None:
            self.component_id = m.get('ComponentId')
        if m.get('ComponentIds') is not None:
            self.component_ids = m.get('ComponentIds')
        if m.get('Labels') is not None:
            self.labels = m.get('Labels')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Provider') is not None:
            self.provider = m.get('Provider')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class ListComponentsShrinkRequest(TeaModel):
    def __init__(
        self,
        component_id: str = None,
        component_ids: str = None,
        labels_shrink: str = None,
        name: str = None,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        provider: str = None,
        sort_by: str = None,
        workspace_id: str = None,
    ):
        self.component_id = component_id
        self.component_ids = component_ids
        self.labels_shrink = labels_shrink
        self.name = name
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        self.provider = provider
        self.sort_by = sort_by
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.component_id is not None:
            result['ComponentId'] = self.component_id
        if self.component_ids is not None:
            result['ComponentIds'] = self.component_ids
        if self.labels_shrink is not None:
            result['Labels'] = self.labels_shrink
        if self.name is not None:
            result['Name'] = self.name
        if self.order is not None:
            result['Order'] = self.order
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.provider is not None:
            result['Provider'] = self.provider
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComponentId') is not None:
            self.component_id = m.get('ComponentId')
        if m.get('ComponentIds') is not None:
            self.component_ids = m.get('ComponentIds')
        if m.get('Labels') is not None:
            self.labels_shrink = m.get('Labels')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Provider') is not None:
            self.provider = m.get('Provider')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class ListComponentsResponseBodyComponentsVersions(TeaModel):
    def __init__(
        self,
        gmt_create_time: str = None,
        snapshot_id: str = None,
        status: str = None,
        version: str = None,
    ):
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.gmt_create_time = gmt_create_time
        self.snapshot_id = snapshot_id
        self.status = status
        self.version = version

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.snapshot_id is not None:
            result['SnapshotId'] = self.snapshot_id
        if self.status is not None:
            result['Status'] = self.status
        if self.version is not None:
            result['Version'] = self.version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('SnapshotId') is not None:
            self.snapshot_id = m.get('SnapshotId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        return self


class ListComponentsResponseBodyComponents(TeaModel):
    def __init__(
        self,
        component_id: str = None,
        description: str = None,
        display_name: str = None,
        gmt_create_time: str = None,
        gmt_modified_time: str = None,
        labels: List[Label] = None,
        name: str = None,
        provider: str = None,
        tenant_id: str = None,
        user_id: str = None,
        versions: List[ListComponentsResponseBodyComponentsVersions] = None,
        workspace_id: str = None,
    ):
        self.component_id = component_id
        self.description = description
        self.display_name = display_name
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.gmt_create_time = gmt_create_time
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.gmt_modified_time = gmt_modified_time
        self.labels = labels
        self.name = name
        self.provider = provider
        self.tenant_id = tenant_id
        self.user_id = user_id
        self.versions = versions
        self.workspace_id = workspace_id

    def validate(self):
        if self.labels:
            for k in self.labels:
                if k:
                    k.validate()
        if self.versions:
            for k in self.versions:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.component_id is not None:
            result['ComponentId'] = self.component_id
        if self.description is not None:
            result['Description'] = self.description
        if self.display_name is not None:
            result['DisplayName'] = self.display_name
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        if self.name is not None:
            result['Name'] = self.name
        if self.provider is not None:
            result['Provider'] = self.provider
        if self.tenant_id is not None:
            result['TenantId'] = self.tenant_id
        if self.user_id is not None:
            result['UserId'] = self.user_id
        result['Versions'] = []
        if self.versions is not None:
            for k in self.versions:
                result['Versions'].append(k.to_map() if k else None)
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComponentId') is not None:
            self.component_id = m.get('ComponentId')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('DisplayName') is not None:
            self.display_name = m.get('DisplayName')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = Label()
                self.labels.append(temp_model.from_map(k))
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Provider') is not None:
            self.provider = m.get('Provider')
        if m.get('TenantId') is not None:
            self.tenant_id = m.get('TenantId')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        self.versions = []
        if m.get('Versions') is not None:
            for k in m.get('Versions'):
                temp_model = ListComponentsResponseBodyComponentsVersions()
                self.versions.append(temp_model.from_map(k))
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class ListComponentsResponseBody(TeaModel):
    def __init__(
        self,
        components: List[ListComponentsResponseBodyComponents] = None,
        request_id: str = None,
        total_count: int = None,
    ):
        self.components = components
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.components:
            for k in self.components:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Components'] = []
        if self.components is not None:
            for k in self.components:
                result['Components'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.components = []
        if m.get('Components') is not None:
            for k in m.get('Components'):
                temp_model = ListComponentsResponseBodyComponents()
                self.components.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListComponentsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListComponentsResponseBody = None,
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
            temp_model = ListComponentsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListInstanceJobsRequest(TeaModel):
    def __init__(
        self,
        instance_job_type: str = None,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        sort_by: str = None,
        status: str = None,
    ):
        self.instance_job_type = instance_job_type
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        self.sort_by = sort_by
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instance_job_type is not None:
            result['InstanceJobType'] = self.instance_job_type
        if self.order is not None:
            result['Order'] = self.order
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceJobType') is not None:
            self.instance_job_type = m.get('InstanceJobType')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class ListInstanceJobsResponseBodyInstanceJobs(TeaModel):
    def __init__(
        self,
        creator: str = None,
        gmt_create_time: str = None,
        instance_id: str = None,
        instance_job_id: str = None,
        instance_job_type: str = None,
        reason_code: str = None,
        reason_message: str = None,
        status: str = None,
        workspace_id: str = None,
    ):
        self.creator = creator
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.gmt_create_time = gmt_create_time
        self.instance_id = instance_id
        self.instance_job_id = instance_job_id
        self.instance_job_type = instance_job_type
        self.reason_code = reason_code
        self.reason_message = reason_message
        self.status = status
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.creator is not None:
            result['Creator'] = self.creator
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.instance_job_id is not None:
            result['InstanceJobId'] = self.instance_job_id
        if self.instance_job_type is not None:
            result['InstanceJobType'] = self.instance_job_type
        if self.reason_code is not None:
            result['ReasonCode'] = self.reason_code
        if self.reason_message is not None:
            result['ReasonMessage'] = self.reason_message
        if self.status is not None:
            result['Status'] = self.status
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Creator') is not None:
            self.creator = m.get('Creator')
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('InstanceJobId') is not None:
            self.instance_job_id = m.get('InstanceJobId')
        if m.get('InstanceJobType') is not None:
            self.instance_job_type = m.get('InstanceJobType')
        if m.get('ReasonCode') is not None:
            self.reason_code = m.get('ReasonCode')
        if m.get('ReasonMessage') is not None:
            self.reason_message = m.get('ReasonMessage')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class ListInstanceJobsResponseBody(TeaModel):
    def __init__(
        self,
        instance_jobs: ListInstanceJobsResponseBodyInstanceJobs = None,
        request_id: str = None,
        total_count: int = None,
    ):
        self.instance_jobs = instance_jobs
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.instance_jobs:
            self.instance_jobs.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instance_jobs is not None:
            result['InstanceJobs'] = self.instance_jobs.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceJobs') is not None:
            temp_model = ListInstanceJobsResponseBodyInstanceJobs()
            self.instance_jobs = temp_model.from_map(m['InstanceJobs'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListInstanceJobsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListInstanceJobsResponseBody = None,
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
            temp_model = ListInstanceJobsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListNodeGPUMetricsRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        gputype: str = None,
        metric_type: str = None,
        node_type: str = None,
        start_time: str = None,
    ):
        self.end_time = end_time
        self.gputype = gputype
        # This parameter is required.
        self.metric_type = metric_type
        self.node_type = node_type
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
        if self.gputype is not None:
            result['GPUType'] = self.gputype
        if self.metric_type is not None:
            result['MetricType'] = self.metric_type
        if self.node_type is not None:
            result['NodeType'] = self.node_type
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('GPUType') is not None:
            self.gputype = m.get('GPUType')
        if m.get('MetricType') is not None:
            self.metric_type = m.get('MetricType')
        if m.get('NodeType') is not None:
            self.node_type = m.get('NodeType')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        return self


class ListNodeGPUMetricsResponseBody(TeaModel):
    def __init__(
        self,
        metric_type: str = None,
        node_gpumetrics: List[NodeGPUMetric] = None,
        quota_id: str = None,
    ):
        self.metric_type = metric_type
        self.node_gpumetrics = node_gpumetrics
        self.quota_id = quota_id

    def validate(self):
        if self.node_gpumetrics:
            for k in self.node_gpumetrics:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.metric_type is not None:
            result['MetricType'] = self.metric_type
        result['NodeGPUMetrics'] = []
        if self.node_gpumetrics is not None:
            for k in self.node_gpumetrics:
                result['NodeGPUMetrics'].append(k.to_map() if k else None)
        if self.quota_id is not None:
            result['QuotaId'] = self.quota_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MetricType') is not None:
            self.metric_type = m.get('MetricType')
        self.node_gpumetrics = []
        if m.get('NodeGPUMetrics') is not None:
            for k in m.get('NodeGPUMetrics'):
                temp_model = NodeGPUMetric()
                self.node_gpumetrics.append(temp_model.from_map(k))
        if m.get('QuotaId') is not None:
            self.quota_id = m.get('QuotaId')
        return self


class ListNodeGPUMetricsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListNodeGPUMetricsResponseBody = None,
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
            temp_model = ListNodeGPUMetricsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListNodePodsRequest(TeaModel):
    def __init__(
        self,
        resource_group_id: str = None,
    ):
        # This parameter is required.
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class ListNodePodsResponseBody(TeaModel):
    def __init__(
        self,
        node_pod_infos: List[NodePodInfo] = None,
        request_id: str = None,
    ):
        self.node_pod_infos = node_pod_infos
        self.request_id = request_id

    def validate(self):
        if self.node_pod_infos:
            for k in self.node_pod_infos:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['NodePodInfos'] = []
        if self.node_pod_infos is not None:
            for k in self.node_pod_infos:
                result['NodePodInfos'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.node_pod_infos = []
        if m.get('NodePodInfos') is not None:
            for k in m.get('NodePodInfos'):
                temp_model = NodePodInfo()
                self.node_pod_infos.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ListNodePodsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListNodePodsResponseBody = None,
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
            temp_model = ListNodePodsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListNodeTypesRequest(TeaModel):
    def __init__(
        self,
        accelerator_type: str = None,
        gputype: str = None,
        node_types: str = None,
        quota_id: str = None,
        resource_group_ids: str = None,
    ):
        self.accelerator_type = accelerator_type
        self.gputype = gputype
        self.node_types = node_types
        self.quota_id = quota_id
        self.resource_group_ids = resource_group_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.accelerator_type is not None:
            result['AcceleratorType'] = self.accelerator_type
        if self.gputype is not None:
            result['GPUType'] = self.gputype
        if self.node_types is not None:
            result['NodeTypes'] = self.node_types
        if self.quota_id is not None:
            result['QuotaId'] = self.quota_id
        if self.resource_group_ids is not None:
            result['ResourceGroupIds'] = self.resource_group_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AcceleratorType') is not None:
            self.accelerator_type = m.get('AcceleratorType')
        if m.get('GPUType') is not None:
            self.gputype = m.get('GPUType')
        if m.get('NodeTypes') is not None:
            self.node_types = m.get('NodeTypes')
        if m.get('QuotaId') is not None:
            self.quota_id = m.get('QuotaId')
        if m.get('ResourceGroupIds') is not None:
            self.resource_group_ids = m.get('ResourceGroupIds')
        return self


class ListNodeTypesResponseBody(TeaModel):
    def __init__(
        self,
        node_types: List[NodeType] = None,
        request_id: str = None,
        statistics: List[NodeTypeStatistic] = None,
    ):
        self.node_types = node_types
        self.request_id = request_id
        self.statistics = statistics

    def validate(self):
        if self.node_types:
            for k in self.node_types:
                if k:
                    k.validate()
        if self.statistics:
            for k in self.statistics:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['NodeTypes'] = []
        if self.node_types is not None:
            for k in self.node_types:
                result['NodeTypes'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Statistics'] = []
        if self.statistics is not None:
            for k in self.statistics:
                result['Statistics'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.node_types = []
        if m.get('NodeTypes') is not None:
            for k in m.get('NodeTypes'):
                temp_model = NodeType()
                self.node_types.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.statistics = []
        if m.get('Statistics') is not None:
            for k in m.get('Statistics'):
                temp_model = NodeTypeStatistic()
                self.statistics.append(temp_model.from_map(k))
        return self


class ListNodeTypesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListNodeTypesResponseBody = None,
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
            temp_model = ListNodeTypesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListNodesRequest(TeaModel):
    def __init__(
        self,
        accelerator_type: str = None,
        filter_by_quota_id: str = None,
        filter_by_resource_group_ids: str = None,
        gputype: str = None,
        node_names: str = None,
        node_statuses: str = None,
        node_types: str = None,
        order: str = None,
        order_statuses: str = None,
        page_number: int = None,
        page_size: int = None,
        quota_id: str = None,
        resource_group_ids: str = None,
        sort_by: str = None,
        verbose: bool = None,
    ):
        self.accelerator_type = accelerator_type
        self.filter_by_quota_id = filter_by_quota_id
        self.filter_by_resource_group_ids = filter_by_resource_group_ids
        self.gputype = gputype
        self.node_names = node_names
        self.node_statuses = node_statuses
        self.node_types = node_types
        self.order = order
        self.order_statuses = order_statuses
        self.page_number = page_number
        self.page_size = page_size
        self.quota_id = quota_id
        self.resource_group_ids = resource_group_ids
        self.sort_by = sort_by
        self.verbose = verbose

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.accelerator_type is not None:
            result['AcceleratorType'] = self.accelerator_type
        if self.filter_by_quota_id is not None:
            result['FilterByQuotaId'] = self.filter_by_quota_id
        if self.filter_by_resource_group_ids is not None:
            result['FilterByResourceGroupIds'] = self.filter_by_resource_group_ids
        if self.gputype is not None:
            result['GPUType'] = self.gputype
        if self.node_names is not None:
            result['NodeNames'] = self.node_names
        if self.node_statuses is not None:
            result['NodeStatuses'] = self.node_statuses
        if self.node_types is not None:
            result['NodeTypes'] = self.node_types
        if self.order is not None:
            result['Order'] = self.order
        if self.order_statuses is not None:
            result['OrderStatuses'] = self.order_statuses
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.quota_id is not None:
            result['QuotaId'] = self.quota_id
        if self.resource_group_ids is not None:
            result['ResourceGroupIds'] = self.resource_group_ids
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.verbose is not None:
            result['Verbose'] = self.verbose
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AcceleratorType') is not None:
            self.accelerator_type = m.get('AcceleratorType')
        if m.get('FilterByQuotaId') is not None:
            self.filter_by_quota_id = m.get('FilterByQuotaId')
        if m.get('FilterByResourceGroupIds') is not None:
            self.filter_by_resource_group_ids = m.get('FilterByResourceGroupIds')
        if m.get('GPUType') is not None:
            self.gputype = m.get('GPUType')
        if m.get('NodeNames') is not None:
            self.node_names = m.get('NodeNames')
        if m.get('NodeStatuses') is not None:
            self.node_statuses = m.get('NodeStatuses')
        if m.get('NodeTypes') is not None:
            self.node_types = m.get('NodeTypes')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('OrderStatuses') is not None:
            self.order_statuses = m.get('OrderStatuses')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('QuotaId') is not None:
            self.quota_id = m.get('QuotaId')
        if m.get('ResourceGroupIds') is not None:
            self.resource_group_ids = m.get('ResourceGroupIds')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('Verbose') is not None:
            self.verbose = m.get('Verbose')
        return self


class ListNodesResponseBody(TeaModel):
    def __init__(
        self,
        nodes: List[Node] = None,
        request_id: str = None,
        total_count: int = None,
    ):
        self.nodes = nodes
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.nodes:
            for k in self.nodes:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Nodes'] = []
        if self.nodes is not None:
            for k in self.nodes:
                result['Nodes'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.nodes = []
        if m.get('Nodes') is not None:
            for k in m.get('Nodes'):
                temp_model = Node()
                self.nodes.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListNodesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListNodesResponseBody = None,
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
            temp_model = ListNodesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListOperationsRequest(TeaModel):
    def __init__(
        self,
        object_id: str = None,
        object_type: str = None,
        operation_id: str = None,
        operation_type: str = None,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        sort_by: str = None,
        status: str = None,
    ):
        self.object_id = object_id
        self.object_type = object_type
        self.operation_id = operation_id
        self.operation_type = operation_type
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        self.sort_by = sort_by
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.object_id is not None:
            result['ObjectId'] = self.object_id
        if self.object_type is not None:
            result['ObjectType'] = self.object_type
        if self.operation_id is not None:
            result['OperationId'] = self.operation_id
        if self.operation_type is not None:
            result['OperationType'] = self.operation_type
        if self.order is not None:
            result['Order'] = self.order
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ObjectId') is not None:
            self.object_id = m.get('ObjectId')
        if m.get('ObjectType') is not None:
            self.object_type = m.get('ObjectType')
        if m.get('OperationId') is not None:
            self.operation_id = m.get('OperationId')
        if m.get('OperationType') is not None:
            self.operation_type = m.get('OperationType')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class ListOperationsResponseBody(TeaModel):
    def __init__(
        self,
        operations: List[ResourceOperation] = None,
        request_id: str = None,
    ):
        self.operations = operations
        self.request_id = request_id

    def validate(self):
        if self.operations:
            for k in self.operations:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Operations'] = []
        if self.operations is not None:
            for k in self.operations:
                result['Operations'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.operations = []
        if m.get('Operations') is not None:
            for k in m.get('Operations'):
                temp_model = ResourceOperation()
                self.operations.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ListOperationsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListOperationsResponseBody = None,
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
            temp_model = ListOperationsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListPermissionsResponseBody(TeaModel):
    def __init__(
        self,
        features: Features = None,
        permissions: List[Permission] = None,
        request_id: str = None,
    ):
        self.features = features
        self.permissions = permissions
        self.request_id = request_id

    def validate(self):
        if self.features:
            self.features.validate()
        if self.permissions:
            for k in self.permissions:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.features is not None:
            result['Features'] = self.features.to_map()
        result['Permissions'] = []
        if self.permissions is not None:
            for k in self.permissions:
                result['Permissions'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Features') is not None:
            temp_model = Features()
            self.features = temp_model.from_map(m['Features'])
        self.permissions = []
        if m.get('Permissions') is not None:
            for k in m.get('Permissions'):
                temp_model = Permission()
                self.permissions.append(temp_model.from_map(k))
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ListPermissionsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListPermissionsResponseBody = None,
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
            temp_model = ListPermissionsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListQuotaUsersRequest(TeaModel):
    def __init__(
        self,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        self_only: bool = None,
        sort_by: str = None,
        user_id: str = None,
        username: str = None,
        workspace_id: str = None,
    ):
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        self.self_only = self_only
        self.sort_by = sort_by
        self.user_id = user_id
        self.username = username
        self.workspace_id = workspace_id

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
        if self.self_only is not None:
            result['SelfOnly'] = self.self_only
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.username is not None:
            result['Username'] = self.username
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('SelfOnly') is not None:
            self.self_only = m.get('SelfOnly')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('Username') is not None:
            self.username = m.get('Username')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class ListQuotaUsersResponseBody(TeaModel):
    def __init__(
        self,
        quota_users: List[QuotaUser] = None,
        request_id: str = None,
        total_count: str = None,
    ):
        self.quota_users = quota_users
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.quota_users:
            for k in self.quota_users:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['QuotaUsers'] = []
        if self.quota_users is not None:
            for k in self.quota_users:
                result['QuotaUsers'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.quota_users = []
        if m.get('QuotaUsers') is not None:
            for k in m.get('QuotaUsers'):
                temp_model = QuotaUser()
                self.quota_users.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListQuotaUsersResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListQuotaUsersResponseBody = None,
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
            temp_model = ListQuotaUsersResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListQuotaWorkloadsRequest(TeaModel):
    def __init__(
        self,
        before_workload_id: str = None,
        node_name: str = None,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        show_own: bool = None,
        sort_by: str = None,
        status: str = None,
        sub_quota_ids: str = None,
        user_ids: str = None,
        workload_created_time_range: TimeRangeFilter = None,
        workload_ids: str = None,
        workload_type: str = None,
        workspace_ids: str = None,
    ):
        self.before_workload_id = before_workload_id
        self.node_name = node_name
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        self.show_own = show_own
        self.sort_by = sort_by
        self.status = status
        self.sub_quota_ids = sub_quota_ids
        self.user_ids = user_ids
        self.workload_created_time_range = workload_created_time_range
        self.workload_ids = workload_ids
        self.workload_type = workload_type
        self.workspace_ids = workspace_ids

    def validate(self):
        if self.workload_created_time_range:
            self.workload_created_time_range.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.before_workload_id is not None:
            result['BeforeWorkloadId'] = self.before_workload_id
        if self.node_name is not None:
            result['NodeName'] = self.node_name
        if self.order is not None:
            result['Order'] = self.order
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.show_own is not None:
            result['ShowOwn'] = self.show_own
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.status is not None:
            result['Status'] = self.status
        if self.sub_quota_ids is not None:
            result['SubQuotaIds'] = self.sub_quota_ids
        if self.user_ids is not None:
            result['UserIds'] = self.user_ids
        if self.workload_created_time_range is not None:
            result['WorkloadCreatedTimeRange'] = self.workload_created_time_range.to_map()
        if self.workload_ids is not None:
            result['WorkloadIds'] = self.workload_ids
        if self.workload_type is not None:
            result['WorkloadType'] = self.workload_type
        if self.workspace_ids is not None:
            result['WorkspaceIds'] = self.workspace_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BeforeWorkloadId') is not None:
            self.before_workload_id = m.get('BeforeWorkloadId')
        if m.get('NodeName') is not None:
            self.node_name = m.get('NodeName')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('ShowOwn') is not None:
            self.show_own = m.get('ShowOwn')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('SubQuotaIds') is not None:
            self.sub_quota_ids = m.get('SubQuotaIds')
        if m.get('UserIds') is not None:
            self.user_ids = m.get('UserIds')
        if m.get('WorkloadCreatedTimeRange') is not None:
            temp_model = TimeRangeFilter()
            self.workload_created_time_range = temp_model.from_map(m['WorkloadCreatedTimeRange'])
        if m.get('WorkloadIds') is not None:
            self.workload_ids = m.get('WorkloadIds')
        if m.get('WorkloadType') is not None:
            self.workload_type = m.get('WorkloadType')
        if m.get('WorkspaceIds') is not None:
            self.workspace_ids = m.get('WorkspaceIds')
        return self


class ListQuotaWorkloadsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        total_count: int = None,
        workloads: List[QueueInfo] = None,
    ):
        self.request_id = request_id
        self.total_count = total_count
        self.workloads = workloads

    def validate(self):
        if self.workloads:
            for k in self.workloads:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        result['Workloads'] = []
        if self.workloads is not None:
            for k in self.workloads:
                result['Workloads'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        self.workloads = []
        if m.get('Workloads') is not None:
            for k in m.get('Workloads'):
                temp_model = QueueInfo()
                self.workloads.append(temp_model.from_map(k))
        return self


class ListQuotaWorkloadsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListQuotaWorkloadsResponseBody = None,
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
            temp_model = ListQuotaWorkloadsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListQuotasRequest(TeaModel):
    def __init__(
        self,
        labels: str = None,
        layout_mode: str = None,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        parent_quota_id: str = None,
        quota_ids: str = None,
        quota_name: str = None,
        resource_type: str = None,
        sort_by: str = None,
        statuses: str = None,
        verbose: bool = None,
        workspace_ids: str = None,
    ):
        self.labels = labels
        self.layout_mode = layout_mode
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        self.parent_quota_id = parent_quota_id
        self.quota_ids = quota_ids
        self.quota_name = quota_name
        self.resource_type = resource_type
        self.sort_by = sort_by
        self.statuses = statuses
        self.verbose = verbose
        self.workspace_ids = workspace_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.labels is not None:
            result['Labels'] = self.labels
        if self.layout_mode is not None:
            result['LayoutMode'] = self.layout_mode
        if self.order is not None:
            result['Order'] = self.order
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.parent_quota_id is not None:
            result['ParentQuotaId'] = self.parent_quota_id
        if self.quota_ids is not None:
            result['QuotaIds'] = self.quota_ids
        if self.quota_name is not None:
            result['QuotaName'] = self.quota_name
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.statuses is not None:
            result['Statuses'] = self.statuses
        if self.verbose is not None:
            result['Verbose'] = self.verbose
        if self.workspace_ids is not None:
            result['WorkspaceIds'] = self.workspace_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Labels') is not None:
            self.labels = m.get('Labels')
        if m.get('LayoutMode') is not None:
            self.layout_mode = m.get('LayoutMode')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('ParentQuotaId') is not None:
            self.parent_quota_id = m.get('ParentQuotaId')
        if m.get('QuotaIds') is not None:
            self.quota_ids = m.get('QuotaIds')
        if m.get('QuotaName') is not None:
            self.quota_name = m.get('QuotaName')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('Statuses') is not None:
            self.statuses = m.get('Statuses')
        if m.get('Verbose') is not None:
            self.verbose = m.get('Verbose')
        if m.get('WorkspaceIds') is not None:
            self.workspace_ids = m.get('WorkspaceIds')
        return self


class ListQuotasResponseBody(TeaModel):
    def __init__(
        self,
        quotas: List[Quota] = None,
        request_id: str = None,
        total_count: int = None,
    ):
        self.quotas = quotas
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.quotas:
            for k in self.quotas:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Quotas'] = []
        if self.quotas is not None:
            for k in self.quotas:
                result['Quotas'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.quotas = []
        if m.get('Quotas') is not None:
            for k in m.get('Quotas'):
                temp_model = Quota()
                self.quotas.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListQuotasResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListQuotasResponseBody = None,
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
            temp_model = ListQuotasResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListResourceGroupMachineGroupsRequest(TeaModel):
    def __init__(
        self,
        creator_id: str = None,
        ecs_spec: str = None,
        name: str = None,
        order: str = None,
        order_instance_id: str = None,
        page_number: int = None,
        page_size: int = None,
        payment_duration: str = None,
        payment_duration_unit: str = None,
        payment_type: str = None,
        sort_by: str = None,
        status: str = None,
    ):
        self.creator_id = creator_id
        self.ecs_spec = ecs_spec
        self.name = name
        self.order = order
        self.order_instance_id = order_instance_id
        self.page_number = page_number
        self.page_size = page_size
        self.payment_duration = payment_duration
        self.payment_duration_unit = payment_duration_unit
        self.payment_type = payment_type
        self.sort_by = sort_by
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.creator_id is not None:
            result['CreatorID'] = self.creator_id
        if self.ecs_spec is not None:
            result['EcsSpec'] = self.ecs_spec
        if self.name is not None:
            result['Name'] = self.name
        if self.order is not None:
            result['Order'] = self.order
        if self.order_instance_id is not None:
            result['OrderInstanceId'] = self.order_instance_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.payment_duration is not None:
            result['PaymentDuration'] = self.payment_duration
        if self.payment_duration_unit is not None:
            result['PaymentDurationUnit'] = self.payment_duration_unit
        if self.payment_type is not None:
            result['PaymentType'] = self.payment_type
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CreatorID') is not None:
            self.creator_id = m.get('CreatorID')
        if m.get('EcsSpec') is not None:
            self.ecs_spec = m.get('EcsSpec')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('OrderInstanceId') is not None:
            self.order_instance_id = m.get('OrderInstanceId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('PaymentDuration') is not None:
            self.payment_duration = m.get('PaymentDuration')
        if m.get('PaymentDurationUnit') is not None:
            self.payment_duration_unit = m.get('PaymentDurationUnit')
        if m.get('PaymentType') is not None:
            self.payment_type = m.get('PaymentType')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class ListResourceGroupMachineGroupsResponseBody(TeaModel):
    def __init__(
        self,
        machine_groups: List[MachineGroup] = None,
        request_id: str = None,
        total_count: str = None,
    ):
        self.machine_groups = machine_groups
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.machine_groups:
            for k in self.machine_groups:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['MachineGroups'] = []
        if self.machine_groups is not None:
            for k in self.machine_groups:
                result['MachineGroups'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.machine_groups = []
        if m.get('MachineGroups') is not None:
            for k in m.get('MachineGroups'):
                temp_model = MachineGroup()
                self.machine_groups.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListResourceGroupMachineGroupsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListResourceGroupMachineGroupsResponseBody = None,
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
            temp_model = ListResourceGroupMachineGroupsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListResourceGroupsRequest(TeaModel):
    def __init__(
        self,
        computing_resource_provider: str = None,
        name: str = None,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        resource_type: str = None,
        show_all: bool = None,
        sort_by: str = None,
        status: str = None,
    ):
        self.computing_resource_provider = computing_resource_provider
        self.name = name
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        self.resource_type = resource_type
        self.show_all = show_all
        self.sort_by = sort_by
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.computing_resource_provider is not None:
            result['ComputingResourceProvider'] = self.computing_resource_provider
        if self.name is not None:
            result['Name'] = self.name
        if self.order is not None:
            result['Order'] = self.order
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.show_all is not None:
            result['ShowAll'] = self.show_all
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComputingResourceProvider') is not None:
            self.computing_resource_provider = m.get('ComputingResourceProvider')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('ShowAll') is not None:
            self.show_all = m.get('ShowAll')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class ListResourceGroupsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        resource_groups: List[ResourceGroup] = None,
        total_count: int = None,
    ):
        self.request_id = request_id
        self.resource_groups = resource_groups
        # This parameter is required.
        self.total_count = total_count

    def validate(self):
        if self.resource_groups:
            for k in self.resource_groups:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['ResourceGroups'] = []
        if self.resource_groups is not None:
            for k in self.resource_groups:
                result['ResourceGroups'].append(k.to_map() if k else None)
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.resource_groups = []
        if m.get('ResourceGroups') is not None:
            for k in m.get('ResourceGroups'):
                temp_model = ResourceGroup()
                self.resource_groups.append(temp_model.from_map(k))
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListResourceGroupsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListResourceGroupsResponseBody = None,
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
            temp_model = ListResourceGroupsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListSpotsStockPreviewRequest(TeaModel):
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


class ListSpotsStockPreviewResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        spots_stock_preview: List[SpotStockPreview] = None,
    ):
        self.request_id = request_id
        self.spots_stock_preview = spots_stock_preview

    def validate(self):
        if self.spots_stock_preview:
            for k in self.spots_stock_preview:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['SpotsStockPreview'] = []
        if self.spots_stock_preview is not None:
            for k in self.spots_stock_preview:
                result['SpotsStockPreview'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.spots_stock_preview = []
        if m.get('SpotsStockPreview') is not None:
            for k in m.get('SpotsStockPreview'):
                temp_model = SpotStockPreview()
                self.spots_stock_preview.append(temp_model.from_map(k))
        return self


class ListSpotsStockPreviewResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListSpotsStockPreviewResponseBody = None,
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
            temp_model = ListSpotsStockPreviewResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListTagResourcesRequestTag(TeaModel):
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


class ListTagResourcesRequest(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        region_id: str = None,
        resource_id: List[str] = None,
        resource_type: str = None,
        tag: List[ListTagResourcesRequestTag] = None,
    ):
        self.next_token = next_token
        # This parameter is required.
        self.region_id = region_id
        self.resource_id = resource_id
        # This parameter is required.
        self.resource_type = resource_type
        self.tag = tag

    def validate(self):
        if self.tag:
            for k in self.tag:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        result['Tag'] = []
        if self.tag is not None:
            for k in self.tag:
                result['Tag'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        self.tag = []
        if m.get('Tag') is not None:
            for k in m.get('Tag'):
                temp_model = ListTagResourcesRequestTag()
                self.tag.append(temp_model.from_map(k))
        return self


class ListTagResourcesShrinkRequest(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        region_id: str = None,
        resource_id_shrink: str = None,
        resource_type: str = None,
        tag_shrink: str = None,
    ):
        self.next_token = next_token
        # This parameter is required.
        self.region_id = region_id
        self.resource_id_shrink = resource_id_shrink
        # This parameter is required.
        self.resource_type = resource_type
        self.tag_shrink = tag_shrink

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.resource_id_shrink is not None:
            result['ResourceId'] = self.resource_id_shrink
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.tag_shrink is not None:
            result['Tag'] = self.tag_shrink
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ResourceId') is not None:
            self.resource_id_shrink = m.get('ResourceId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('Tag') is not None:
            self.tag_shrink = m.get('Tag')
        return self


class ListTagResourcesResponseBodyTagResources(TeaModel):
    def __init__(
        self,
        resource_id: str = None,
        resource_type: str = None,
        tag_key: str = None,
        tag_value: str = None,
    ):
        self.resource_id = resource_id
        self.resource_type = resource_type
        self.tag_key = tag_key
        self.tag_value = tag_value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.tag_key is not None:
            result['TagKey'] = self.tag_key
        if self.tag_value is not None:
            result['TagValue'] = self.tag_value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('TagKey') is not None:
            self.tag_key = m.get('TagKey')
        if m.get('TagValue') is not None:
            self.tag_value = m.get('TagValue')
        return self


class ListTagResourcesResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        tag_resources: List[ListTagResourcesResponseBodyTagResources] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.tag_resources = tag_resources

    def validate(self):
        if self.tag_resources:
            for k in self.tag_resources:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['TagResources'] = []
        if self.tag_resources is not None:
            for k in self.tag_resources:
                result['TagResources'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.tag_resources = []
        if m.get('TagResources') is not None:
            for k in m.get('TagResources'):
                temp_model = ListTagResourcesResponseBodyTagResources()
                self.tag_resources.append(temp_model.from_map(k))
        return self


class ListTagResourcesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListTagResourcesResponseBody = None,
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
            temp_model = ListTagResourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListTrainingJobEventsRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        page_number: int = None,
        page_size: int = None,
        start_time: str = None,
        token: str = None,
    ):
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.end_time = end_time
        self.page_number = page_number
        self.page_size = page_size
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.start_time = start_time
        self.token = token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.token is not None:
            result['Token'] = self.token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('Token') is not None:
            self.token = m.get('Token')
        return self


class ListTrainingJobEventsResponseBody(TeaModel):
    def __init__(
        self,
        events: List[str] = None,
        request_id: str = None,
        total_count: str = None,
    ):
        self.events = events
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.events is not None:
            result['Events'] = self.events
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Events') is not None:
            self.events = m.get('Events')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListTrainingJobEventsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListTrainingJobEventsResponseBody = None,
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
            temp_model = ListTrainingJobEventsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListTrainingJobInstanceEventsRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        page_number: int = None,
        page_size: int = None,
        start_time: str = None,
        token: str = None,
    ):
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.end_time = end_time
        self.page_number = page_number
        self.page_size = page_size
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.start_time = start_time
        self.token = token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.token is not None:
            result['Token'] = self.token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('Token') is not None:
            self.token = m.get('Token')
        return self


class ListTrainingJobInstanceEventsResponseBody(TeaModel):
    def __init__(
        self,
        events: List[str] = None,
        request_id: str = None,
        total_count: str = None,
    ):
        self.events = events
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.events is not None:
            result['Events'] = self.events
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Events') is not None:
            self.events = m.get('Events')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListTrainingJobInstanceEventsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListTrainingJobInstanceEventsResponseBody = None,
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
            temp_model = ListTrainingJobInstanceEventsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListTrainingJobInstanceMetricsRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        instance_id: str = None,
        metric_type: str = None,
        start_time: str = None,
        time_step: str = None,
        token: str = None,
    ):
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.end_time = end_time
        self.instance_id = instance_id
        # This parameter is required.
        self.metric_type = metric_type
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.start_time = start_time
        self.time_step = time_step
        self.token = token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.metric_type is not None:
            result['MetricType'] = self.metric_type
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.time_step is not None:
            result['TimeStep'] = self.time_step
        if self.token is not None:
            result['Token'] = self.token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('MetricType') is not None:
            self.metric_type = m.get('MetricType')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('TimeStep') is not None:
            self.time_step = m.get('TimeStep')
        if m.get('Token') is not None:
            self.token = m.get('Token')
        return self


class ListTrainingJobInstanceMetricsResponseBodyInstancemetricsMetrics(TeaModel):
    def __init__(
        self,
        time: str = None,
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


class ListTrainingJobInstanceMetricsResponseBodyInstancemetrics(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        metrics: List[ListTrainingJobInstanceMetricsResponseBodyInstancemetricsMetrics] = None,
        node_name: str = None,
    ):
        self.instance_id = instance_id
        self.metrics = metrics
        self.node_name = node_name

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
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        result['Metrics'] = []
        if self.metrics is not None:
            for k in self.metrics:
                result['Metrics'].append(k.to_map() if k else None)
        if self.node_name is not None:
            result['NodeName'] = self.node_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        self.metrics = []
        if m.get('Metrics') is not None:
            for k in m.get('Metrics'):
                temp_model = ListTrainingJobInstanceMetricsResponseBodyInstancemetricsMetrics()
                self.metrics.append(temp_model.from_map(k))
        if m.get('NodeName') is not None:
            self.node_name = m.get('NodeName')
        return self


class ListTrainingJobInstanceMetricsResponseBody(TeaModel):
    def __init__(
        self,
        instancemetrics: List[ListTrainingJobInstanceMetricsResponseBodyInstancemetrics] = None,
        request_id: str = None,
    ):
        self.instancemetrics = instancemetrics
        self.request_id = request_id

    def validate(self):
        if self.instancemetrics:
            for k in self.instancemetrics:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Instancemetrics'] = []
        if self.instancemetrics is not None:
            for k in self.instancemetrics:
                result['Instancemetrics'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.instancemetrics = []
        if m.get('Instancemetrics') is not None:
            for k in m.get('Instancemetrics'):
                temp_model = ListTrainingJobInstanceMetricsResponseBodyInstancemetrics()
                self.instancemetrics.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ListTrainingJobInstanceMetricsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListTrainingJobInstanceMetricsResponseBody = None,
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
            temp_model = ListTrainingJobInstanceMetricsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListTrainingJobLogsRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        instance_id: str = None,
        page_number: int = None,
        page_size: int = None,
        start_time: str = None,
        token: str = None,
        worker_id: str = None,
    ):
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.end_time = end_time
        self.instance_id = instance_id
        self.page_number = page_number
        self.page_size = page_size
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.start_time = start_time
        self.token = token
        self.worker_id = worker_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.token is not None:
            result['Token'] = self.token
        if self.worker_id is not None:
            result['WorkerId'] = self.worker_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('Token') is not None:
            self.token = m.get('Token')
        if m.get('WorkerId') is not None:
            self.worker_id = m.get('WorkerId')
        return self


class ListTrainingJobLogsResponseBody(TeaModel):
    def __init__(
        self,
        logs: List[str] = None,
        request_id: str = None,
        total_count: str = None,
    ):
        self.logs = logs
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.logs is not None:
            result['Logs'] = self.logs
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Logs') is not None:
            self.logs = m.get('Logs')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListTrainingJobLogsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListTrainingJobLogsResponseBody = None,
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
            temp_model = ListTrainingJobLogsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListTrainingJobMetricsRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        name: str = None,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        start_time: str = None,
        token: str = None,
    ):
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.end_time = end_time
        self.name = name
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.start_time = start_time
        self.token = token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.name is not None:
            result['Name'] = self.name
        if self.order is not None:
            result['Order'] = self.order
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.token is not None:
            result['Token'] = self.token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('Token') is not None:
            self.token = m.get('Token')
        return self


class ListTrainingJobMetricsResponseBodyMetrics(TeaModel):
    def __init__(
        self,
        name: str = None,
        timestamp: str = None,
        value: float = None,
    ):
        self.name = name
        # Use the UTC time format: yyyy-MM-ddTHH:mmZ
        self.timestamp = timestamp
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.timestamp is not None:
            result['Timestamp'] = self.timestamp
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Timestamp') is not None:
            self.timestamp = m.get('Timestamp')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class ListTrainingJobMetricsResponseBody(TeaModel):
    def __init__(
        self,
        metrics: List[ListTrainingJobMetricsResponseBodyMetrics] = None,
        request_id: str = None,
    ):
        self.metrics = metrics
        self.request_id = request_id

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
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.metrics = []
        if m.get('Metrics') is not None:
            for k in m.get('Metrics'):
                temp_model = ListTrainingJobMetricsResponseBodyMetrics()
                self.metrics.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ListTrainingJobMetricsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListTrainingJobMetricsResponseBody = None,
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
            temp_model = ListTrainingJobMetricsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListTrainingJobOutputModelsRequest(TeaModel):
    def __init__(
        self,
        token: str = None,
    ):
        self.token = token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.token is not None:
            result['Token'] = self.token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Token') is not None:
            self.token = m.get('Token')
        return self


class ListTrainingJobOutputModelsResponseBodyOutputModelsLabels(TeaModel):
    def __init__(
        self,
        name: str = None,
        value: str = None,
    ):
        self.name = name
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class ListTrainingJobOutputModelsResponseBodyOutputModels(TeaModel):
    def __init__(
        self,
        evaluation_spec: Dict[str, Any] = None,
        inference_spec: Dict[str, Any] = None,
        labels: List[ListTrainingJobOutputModelsResponseBodyOutputModelsLabels] = None,
        metrics: Dict[str, Any] = None,
        output_channel_name: str = None,
        source_id: str = None,
        source_type: str = None,
        training_spec: Dict[str, Any] = None,
        uri: str = None,
    ):
        self.evaluation_spec = evaluation_spec
        self.inference_spec = inference_spec
        self.labels = labels
        self.metrics = metrics
        self.output_channel_name = output_channel_name
        self.source_id = source_id
        self.source_type = source_type
        self.training_spec = training_spec
        self.uri = uri

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
        if self.evaluation_spec is not None:
            result['EvaluationSpec'] = self.evaluation_spec
        if self.inference_spec is not None:
            result['InferenceSpec'] = self.inference_spec
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        if self.metrics is not None:
            result['Metrics'] = self.metrics
        if self.output_channel_name is not None:
            result['OutputChannelName'] = self.output_channel_name
        if self.source_id is not None:
            result['SourceId'] = self.source_id
        if self.source_type is not None:
            result['SourceType'] = self.source_type
        if self.training_spec is not None:
            result['TrainingSpec'] = self.training_spec
        if self.uri is not None:
            result['Uri'] = self.uri
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EvaluationSpec') is not None:
            self.evaluation_spec = m.get('EvaluationSpec')
        if m.get('InferenceSpec') is not None:
            self.inference_spec = m.get('InferenceSpec')
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = ListTrainingJobOutputModelsResponseBodyOutputModelsLabels()
                self.labels.append(temp_model.from_map(k))
        if m.get('Metrics') is not None:
            self.metrics = m.get('Metrics')
        if m.get('OutputChannelName') is not None:
            self.output_channel_name = m.get('OutputChannelName')
        if m.get('SourceId') is not None:
            self.source_id = m.get('SourceId')
        if m.get('SourceType') is not None:
            self.source_type = m.get('SourceType')
        if m.get('TrainingSpec') is not None:
            self.training_spec = m.get('TrainingSpec')
        if m.get('Uri') is not None:
            self.uri = m.get('Uri')
        return self


class ListTrainingJobOutputModelsResponseBody(TeaModel):
    def __init__(
        self,
        output_models: List[ListTrainingJobOutputModelsResponseBodyOutputModels] = None,
    ):
        self.output_models = output_models

    def validate(self):
        if self.output_models:
            for k in self.output_models:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['OutputModels'] = []
        if self.output_models is not None:
            for k in self.output_models:
                result['OutputModels'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.output_models = []
        if m.get('OutputModels') is not None:
            for k in m.get('OutputModels'):
                temp_model = ListTrainingJobOutputModelsResponseBodyOutputModels()
                self.output_models.append(temp_model.from_map(k))
        return self


class ListTrainingJobOutputModelsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListTrainingJobOutputModelsResponseBody = None,
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
            temp_model = ListTrainingJobOutputModelsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListTrainingJobsRequest(TeaModel):
    def __init__(
        self,
        algorithm_name: str = None,
        algorithm_provider: str = None,
        end_time: str = None,
        is_temp_algo: bool = None,
        labels: Dict[str, Any] = None,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        sort_by: str = None,
        start_time: str = None,
        status: str = None,
        training_job_id: str = None,
        training_job_name: str = None,
        workspace_id: str = None,
    ):
        self.algorithm_name = algorithm_name
        self.algorithm_provider = algorithm_provider
        self.end_time = end_time
        self.is_temp_algo = is_temp_algo
        self.labels = labels
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        self.sort_by = sort_by
        self.start_time = start_time
        self.status = status
        self.training_job_id = training_job_id
        self.training_job_name = training_job_name
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.algorithm_name is not None:
            result['AlgorithmName'] = self.algorithm_name
        if self.algorithm_provider is not None:
            result['AlgorithmProvider'] = self.algorithm_provider
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.is_temp_algo is not None:
            result['IsTempAlgo'] = self.is_temp_algo
        if self.labels is not None:
            result['Labels'] = self.labels
        if self.order is not None:
            result['Order'] = self.order
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.status is not None:
            result['Status'] = self.status
        if self.training_job_id is not None:
            result['TrainingJobId'] = self.training_job_id
        if self.training_job_name is not None:
            result['TrainingJobName'] = self.training_job_name
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AlgorithmName') is not None:
            self.algorithm_name = m.get('AlgorithmName')
        if m.get('AlgorithmProvider') is not None:
            self.algorithm_provider = m.get('AlgorithmProvider')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('IsTempAlgo') is not None:
            self.is_temp_algo = m.get('IsTempAlgo')
        if m.get('Labels') is not None:
            self.labels = m.get('Labels')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('TrainingJobId') is not None:
            self.training_job_id = m.get('TrainingJobId')
        if m.get('TrainingJobName') is not None:
            self.training_job_name = m.get('TrainingJobName')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class ListTrainingJobsShrinkRequest(TeaModel):
    def __init__(
        self,
        algorithm_name: str = None,
        algorithm_provider: str = None,
        end_time: str = None,
        is_temp_algo: bool = None,
        labels_shrink: str = None,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        sort_by: str = None,
        start_time: str = None,
        status: str = None,
        training_job_id: str = None,
        training_job_name: str = None,
        workspace_id: str = None,
    ):
        self.algorithm_name = algorithm_name
        self.algorithm_provider = algorithm_provider
        self.end_time = end_time
        self.is_temp_algo = is_temp_algo
        self.labels_shrink = labels_shrink
        self.order = order
        self.page_number = page_number
        self.page_size = page_size
        self.sort_by = sort_by
        self.start_time = start_time
        self.status = status
        self.training_job_id = training_job_id
        self.training_job_name = training_job_name
        self.workspace_id = workspace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.algorithm_name is not None:
            result['AlgorithmName'] = self.algorithm_name
        if self.algorithm_provider is not None:
            result['AlgorithmProvider'] = self.algorithm_provider
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.is_temp_algo is not None:
            result['IsTempAlgo'] = self.is_temp_algo
        if self.labels_shrink is not None:
            result['Labels'] = self.labels_shrink
        if self.order is not None:
            result['Order'] = self.order
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.status is not None:
            result['Status'] = self.status
        if self.training_job_id is not None:
            result['TrainingJobId'] = self.training_job_id
        if self.training_job_name is not None:
            result['TrainingJobName'] = self.training_job_name
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AlgorithmName') is not None:
            self.algorithm_name = m.get('AlgorithmName')
        if m.get('AlgorithmProvider') is not None:
            self.algorithm_provider = m.get('AlgorithmProvider')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('IsTempAlgo') is not None:
            self.is_temp_algo = m.get('IsTempAlgo')
        if m.get('Labels') is not None:
            self.labels_shrink = m.get('Labels')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('TrainingJobId') is not None:
            self.training_job_id = m.get('TrainingJobId')
        if m.get('TrainingJobName') is not None:
            self.training_job_name = m.get('TrainingJobName')
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class ListTrainingJobsResponseBodyTrainingJobsComputeResourceInstanceSpec(TeaModel):
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


class ListTrainingJobsResponseBodyTrainingJobsComputeResource(TeaModel):
    def __init__(
        self,
        ecs_count: int = None,
        ecs_spec: str = None,
        instance_count: int = None,
        instance_spec: ListTrainingJobsResponseBodyTrainingJobsComputeResourceInstanceSpec = None,
        resource_id: str = None,
    ):
        self.ecs_count = ecs_count
        self.ecs_spec = ecs_spec
        self.instance_count = instance_count
        self.instance_spec = instance_spec
        self.resource_id = resource_id

    def validate(self):
        if self.instance_spec:
            self.instance_spec.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.ecs_count is not None:
            result['EcsCount'] = self.ecs_count
        if self.ecs_spec is not None:
            result['EcsSpec'] = self.ecs_spec
        if self.instance_count is not None:
            result['InstanceCount'] = self.instance_count
        if self.instance_spec is not None:
            result['InstanceSpec'] = self.instance_spec.to_map()
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EcsCount') is not None:
            self.ecs_count = m.get('EcsCount')
        if m.get('EcsSpec') is not None:
            self.ecs_spec = m.get('EcsSpec')
        if m.get('InstanceCount') is not None:
            self.instance_count = m.get('InstanceCount')
        if m.get('InstanceSpec') is not None:
            temp_model = ListTrainingJobsResponseBodyTrainingJobsComputeResourceInstanceSpec()
            self.instance_spec = temp_model.from_map(m['InstanceSpec'])
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        return self


class ListTrainingJobsResponseBodyTrainingJobsExperimentConfig(TeaModel):
    def __init__(
        self,
        experiment_id: str = None,
        experiment_name: str = None,
    ):
        self.experiment_id = experiment_id
        self.experiment_name = experiment_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.experiment_id is not None:
            result['ExperimentId'] = self.experiment_id
        if self.experiment_name is not None:
            result['ExperimentName'] = self.experiment_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ExperimentId') is not None:
            self.experiment_id = m.get('ExperimentId')
        if m.get('ExperimentName') is not None:
            self.experiment_name = m.get('ExperimentName')
        return self


class ListTrainingJobsResponseBodyTrainingJobsHyperParameters(TeaModel):
    def __init__(
        self,
        name: str = None,
        value: str = None,
    ):
        self.name = name
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class ListTrainingJobsResponseBodyTrainingJobsInputChannels(TeaModel):
    def __init__(
        self,
        dataset_id: str = None,
        input_uri: str = None,
        name: str = None,
    ):
        self.dataset_id = dataset_id
        self.input_uri = input_uri
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.dataset_id is not None:
            result['DatasetId'] = self.dataset_id
        if self.input_uri is not None:
            result['InputUri'] = self.input_uri
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DatasetId') is not None:
            self.dataset_id = m.get('DatasetId')
        if m.get('InputUri') is not None:
            self.input_uri = m.get('InputUri')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class ListTrainingJobsResponseBodyTrainingJobsLabels(TeaModel):
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


class ListTrainingJobsResponseBodyTrainingJobsOutputChannels(TeaModel):
    def __init__(
        self,
        dataset_id: str = None,
        name: str = None,
        output_uri: str = None,
    ):
        self.dataset_id = dataset_id
        self.name = name
        self.output_uri = output_uri

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.dataset_id is not None:
            result['DatasetId'] = self.dataset_id
        if self.name is not None:
            result['Name'] = self.name
        if self.output_uri is not None:
            result['OutputUri'] = self.output_uri
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DatasetId') is not None:
            self.dataset_id = m.get('DatasetId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('OutputUri') is not None:
            self.output_uri = m.get('OutputUri')
        return self


class ListTrainingJobsResponseBodyTrainingJobsScheduler(TeaModel):
    def __init__(
        self,
        max_running_time_in_seconds: int = None,
    ):
        self.max_running_time_in_seconds = max_running_time_in_seconds

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.max_running_time_in_seconds is not None:
            result['MaxRunningTimeInSeconds'] = self.max_running_time_in_seconds
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MaxRunningTimeInSeconds') is not None:
            self.max_running_time_in_seconds = m.get('MaxRunningTimeInSeconds')
        return self


class ListTrainingJobsResponseBodyTrainingJobsStatusTransitions(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        reason_code: str = None,
        reason_message: str = None,
        start_time: str = None,
        status: str = None,
    ):
        self.end_time = end_time
        self.reason_code = reason_code
        self.reason_message = reason_message
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
        if self.reason_code is not None:
            result['ReasonCode'] = self.reason_code
        if self.reason_message is not None:
            result['ReasonMessage'] = self.reason_message
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('ReasonCode') is not None:
            self.reason_code = m.get('ReasonCode')
        if m.get('ReasonMessage') is not None:
            self.reason_message = m.get('ReasonMessage')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class ListTrainingJobsResponseBodyTrainingJobsUserVpc(TeaModel):
    def __init__(
        self,
        default_route: str = None,
        extended_cidrs: List[str] = None,
        security_group_id: str = None,
        switch_id: str = None,
        vpc_id: str = None,
    ):
        self.default_route = default_route
        self.extended_cidrs = extended_cidrs
        self.security_group_id = security_group_id
        self.switch_id = switch_id
        self.vpc_id = vpc_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.default_route is not None:
            result['DefaultRoute'] = self.default_route
        if self.extended_cidrs is not None:
            result['ExtendedCIDRs'] = self.extended_cidrs
        if self.security_group_id is not None:
            result['SecurityGroupId'] = self.security_group_id
        if self.switch_id is not None:
            result['SwitchId'] = self.switch_id
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DefaultRoute') is not None:
            self.default_route = m.get('DefaultRoute')
        if m.get('ExtendedCIDRs') is not None:
            self.extended_cidrs = m.get('ExtendedCIDRs')
        if m.get('SecurityGroupId') is not None:
            self.security_group_id = m.get('SecurityGroupId')
        if m.get('SwitchId') is not None:
            self.switch_id = m.get('SwitchId')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        return self


class ListTrainingJobsResponseBodyTrainingJobs(TeaModel):
    def __init__(
        self,
        algorithm_name: str = None,
        algorithm_provider: str = None,
        algorithm_version: str = None,
        compute_resource: ListTrainingJobsResponseBodyTrainingJobsComputeResource = None,
        environments: Dict[str, str] = None,
        experiment_config: ListTrainingJobsResponseBodyTrainingJobsExperimentConfig = None,
        gmt_create_time: str = None,
        gmt_modified_time: str = None,
        hyper_parameters: List[ListTrainingJobsResponseBodyTrainingJobsHyperParameters] = None,
        input_channels: List[ListTrainingJobsResponseBodyTrainingJobsInputChannels] = None,
        is_temp_algo: bool = None,
        labels: List[ListTrainingJobsResponseBodyTrainingJobsLabels] = None,
        output_channels: List[ListTrainingJobsResponseBodyTrainingJobsOutputChannels] = None,
        python_requirements: List[str] = None,
        reason_code: str = None,
        reason_message: str = None,
        role_arn: str = None,
        scheduler: ListTrainingJobsResponseBodyTrainingJobsScheduler = None,
        status: str = None,
        status_transitions: List[ListTrainingJobsResponseBodyTrainingJobsStatusTransitions] = None,
        training_job_description: str = None,
        training_job_id: str = None,
        training_job_name: str = None,
        user_id: str = None,
        user_vpc: ListTrainingJobsResponseBodyTrainingJobsUserVpc = None,
        workspace_id: str = None,
    ):
        self.algorithm_name = algorithm_name
        self.algorithm_provider = algorithm_provider
        self.algorithm_version = algorithm_version
        self.compute_resource = compute_resource
        self.environments = environments
        self.experiment_config = experiment_config
        self.gmt_create_time = gmt_create_time
        self.gmt_modified_time = gmt_modified_time
        self.hyper_parameters = hyper_parameters
        self.input_channels = input_channels
        self.is_temp_algo = is_temp_algo
        self.labels = labels
        self.output_channels = output_channels
        self.python_requirements = python_requirements
        self.reason_code = reason_code
        self.reason_message = reason_message
        self.role_arn = role_arn
        self.scheduler = scheduler
        self.status = status
        self.status_transitions = status_transitions
        self.training_job_description = training_job_description
        self.training_job_id = training_job_id
        self.training_job_name = training_job_name
        self.user_id = user_id
        self.user_vpc = user_vpc
        self.workspace_id = workspace_id

    def validate(self):
        if self.compute_resource:
            self.compute_resource.validate()
        if self.experiment_config:
            self.experiment_config.validate()
        if self.hyper_parameters:
            for k in self.hyper_parameters:
                if k:
                    k.validate()
        if self.input_channels:
            for k in self.input_channels:
                if k:
                    k.validate()
        if self.labels:
            for k in self.labels:
                if k:
                    k.validate()
        if self.output_channels:
            for k in self.output_channels:
                if k:
                    k.validate()
        if self.scheduler:
            self.scheduler.validate()
        if self.status_transitions:
            for k in self.status_transitions:
                if k:
                    k.validate()
        if self.user_vpc:
            self.user_vpc.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.algorithm_name is not None:
            result['AlgorithmName'] = self.algorithm_name
        if self.algorithm_provider is not None:
            result['AlgorithmProvider'] = self.algorithm_provider
        if self.algorithm_version is not None:
            result['AlgorithmVersion'] = self.algorithm_version
        if self.compute_resource is not None:
            result['ComputeResource'] = self.compute_resource.to_map()
        if self.environments is not None:
            result['Environments'] = self.environments
        if self.experiment_config is not None:
            result['ExperimentConfig'] = self.experiment_config.to_map()
        if self.gmt_create_time is not None:
            result['GmtCreateTime'] = self.gmt_create_time
        if self.gmt_modified_time is not None:
            result['GmtModifiedTime'] = self.gmt_modified_time
        result['HyperParameters'] = []
        if self.hyper_parameters is not None:
            for k in self.hyper_parameters:
                result['HyperParameters'].append(k.to_map() if k else None)
        result['InputChannels'] = []
        if self.input_channels is not None:
            for k in self.input_channels:
                result['InputChannels'].append(k.to_map() if k else None)
        if self.is_temp_algo is not None:
            result['IsTempAlgo'] = self.is_temp_algo
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        result['OutputChannels'] = []
        if self.output_channels is not None:
            for k in self.output_channels:
                result['OutputChannels'].append(k.to_map() if k else None)
        if self.python_requirements is not None:
            result['PythonRequirements'] = self.python_requirements
        if self.reason_code is not None:
            result['ReasonCode'] = self.reason_code
        if self.reason_message is not None:
            result['ReasonMessage'] = self.reason_message
        if self.role_arn is not None:
            result['RoleArn'] = self.role_arn
        if self.scheduler is not None:
            result['Scheduler'] = self.scheduler.to_map()
        if self.status is not None:
            result['Status'] = self.status
        result['StatusTransitions'] = []
        if self.status_transitions is not None:
            for k in self.status_transitions:
                result['StatusTransitions'].append(k.to_map() if k else None)
        if self.training_job_description is not None:
            result['TrainingJobDescription'] = self.training_job_description
        if self.training_job_id is not None:
            result['TrainingJobId'] = self.training_job_id
        if self.training_job_name is not None:
            result['TrainingJobName'] = self.training_job_name
        if self.user_id is not None:
            result['UserId'] = self.user_id
        if self.user_vpc is not None:
            result['UserVpc'] = self.user_vpc.to_map()
        if self.workspace_id is not None:
            result['WorkspaceId'] = self.workspace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AlgorithmName') is not None:
            self.algorithm_name = m.get('AlgorithmName')
        if m.get('AlgorithmProvider') is not None:
            self.algorithm_provider = m.get('AlgorithmProvider')
        if m.get('AlgorithmVersion') is not None:
            self.algorithm_version = m.get('AlgorithmVersion')
        if m.get('ComputeResource') is not None:
            temp_model = ListTrainingJobsResponseBodyTrainingJobsComputeResource()
            self.compute_resource = temp_model.from_map(m['ComputeResource'])
        if m.get('Environments') is not None:
            self.environments = m.get('Environments')
        if m.get('ExperimentConfig') is not None:
            temp_model = ListTrainingJobsResponseBodyTrainingJobsExperimentConfig()
            self.experiment_config = temp_model.from_map(m['ExperimentConfig'])
        if m.get('GmtCreateTime') is not None:
            self.gmt_create_time = m.get('GmtCreateTime')
        if m.get('GmtModifiedTime') is not None:
            self.gmt_modified_time = m.get('GmtModifiedTime')
        self.hyper_parameters = []
        if m.get('HyperParameters') is not None:
            for k in m.get('HyperParameters'):
                temp_model = ListTrainingJobsResponseBodyTrainingJobsHyperParameters()
                self.hyper_parameters.append(temp_model.from_map(k))
        self.input_channels = []
        if m.get('InputChannels') is not None:
            for k in m.get('InputChannels'):
                temp_model = ListTrainingJobsResponseBodyTrainingJobsInputChannels()
                self.input_channels.append(temp_model.from_map(k))
        if m.get('IsTempAlgo') is not None:
            self.is_temp_algo = m.get('IsTempAlgo')
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = ListTrainingJobsResponseBodyTrainingJobsLabels()
                self.labels.append(temp_model.from_map(k))
        self.output_channels = []
        if m.get('OutputChannels') is not None:
            for k in m.get('OutputChannels'):
                temp_model = ListTrainingJobsResponseBodyTrainingJobsOutputChannels()
                self.output_channels.append(temp_model.from_map(k))
        if m.get('PythonRequirements') is not None:
            self.python_requirements = m.get('PythonRequirements')
        if m.get('ReasonCode') is not None:
            self.reason_code = m.get('ReasonCode')
        if m.get('ReasonMessage') is not None:
            self.reason_message = m.get('ReasonMessage')
        if m.get('RoleArn') is not None:
            self.role_arn = m.get('RoleArn')
        if m.get('Scheduler') is not None:
            temp_model = ListTrainingJobsResponseBodyTrainingJobsScheduler()
            self.scheduler = temp_model.from_map(m['Scheduler'])
        if m.get('Status') is not None:
            self.status = m.get('Status')
        self.status_transitions = []
        if m.get('StatusTransitions') is not None:
            for k in m.get('StatusTransitions'):
                temp_model = ListTrainingJobsResponseBodyTrainingJobsStatusTransitions()
                self.status_transitions.append(temp_model.from_map(k))
        if m.get('TrainingJobDescription') is not None:
            self.training_job_description = m.get('TrainingJobDescription')
        if m.get('TrainingJobId') is not None:
            self.training_job_id = m.get('TrainingJobId')
        if m.get('TrainingJobName') is not None:
            self.training_job_name = m.get('TrainingJobName')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        if m.get('UserVpc') is not None:
            temp_model = ListTrainingJobsResponseBodyTrainingJobsUserVpc()
            self.user_vpc = temp_model.from_map(m['UserVpc'])
        if m.get('WorkspaceId') is not None:
            self.workspace_id = m.get('WorkspaceId')
        return self


class ListTrainingJobsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        total_count: int = None,
        training_jobs: List[ListTrainingJobsResponseBodyTrainingJobs] = None,
    ):
        self.request_id = request_id
        self.total_count = total_count
        self.training_jobs = training_jobs

    def validate(self):
        if self.training_jobs:
            for k in self.training_jobs:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        result['TrainingJobs'] = []
        if self.training_jobs is not None:
            for k in self.training_jobs:
                result['TrainingJobs'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        self.training_jobs = []
        if m.get('TrainingJobs') is not None:
            for k in m.get('TrainingJobs'):
                temp_model = ListTrainingJobsResponseBodyTrainingJobs()
                self.training_jobs.append(temp_model.from_map(k))
        return self


class ListTrainingJobsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListTrainingJobsResponseBody = None,
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
            temp_model = ListTrainingJobsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class OperateNodeRequest(TeaModel):
    def __init__(
        self,
        operation: str = None,
        resource_group_id: str = None,
    ):
        # This parameter is required.
        self.operation = operation
        # This parameter is required.
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.operation is not None:
            result['Operation'] = self.operation
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Operation') is not None:
            self.operation = m.get('Operation')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class OperateNodeResponseBody(TeaModel):
    def __init__(
        self,
        node_id: str = None,
        request_id: str = None,
    ):
        self.node_id = node_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.node_id is not None:
            result['NodeId'] = self.node_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NodeId') is not None:
            self.node_id = m.get('NodeId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class OperateNodeResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: OperateNodeResponseBody = None,
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
            temp_model = OperateNodeResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ReleaseAlgorithmRequest(TeaModel):
    def __init__(
        self,
        target_algorithm_name: str = None,
        update_if_exists: bool = None,
    ):
        # This parameter is required.
        self.target_algorithm_name = target_algorithm_name
        self.update_if_exists = update_if_exists

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.target_algorithm_name is not None:
            result['TargetAlgorithmName'] = self.target_algorithm_name
        if self.update_if_exists is not None:
            result['UpdateIfExists'] = self.update_if_exists
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TargetAlgorithmName') is not None:
            self.target_algorithm_name = m.get('TargetAlgorithmName')
        if m.get('UpdateIfExists') is not None:
            self.update_if_exists = m.get('UpdateIfExists')
        return self


class ReleaseAlgorithmResponseBody(TeaModel):
    def __init__(
        self,
        algorithm_id: str = None,
        request_id: str = None,
    ):
        self.algorithm_id = algorithm_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.algorithm_id is not None:
            result['AlgorithmId'] = self.algorithm_id
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AlgorithmId') is not None:
            self.algorithm_id = m.get('AlgorithmId')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ReleaseAlgorithmResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ReleaseAlgorithmResponseBody = None,
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
            temp_model = ReleaseAlgorithmResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ReleaseAlgorithmVersionRequest(TeaModel):
    def __init__(
        self,
        target_algorithm_name: str = None,
        target_algorithm_version: str = None,
        update_if_exists: bool = None,
    ):
        # This parameter is required.
        self.target_algorithm_name = target_algorithm_name
        self.target_algorithm_version = target_algorithm_version
        self.update_if_exists = update_if_exists

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.target_algorithm_name is not None:
            result['TargetAlgorithmName'] = self.target_algorithm_name
        if self.target_algorithm_version is not None:
            result['TargetAlgorithmVersion'] = self.target_algorithm_version
        if self.update_if_exists is not None:
            result['UpdateIfExists'] = self.update_if_exists
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TargetAlgorithmName') is not None:
            self.target_algorithm_name = m.get('TargetAlgorithmName')
        if m.get('TargetAlgorithmVersion') is not None:
            self.target_algorithm_version = m.get('TargetAlgorithmVersion')
        if m.get('UpdateIfExists') is not None:
            self.update_if_exists = m.get('UpdateIfExists')
        return self


class ReleaseAlgorithmVersionResponseBody(TeaModel):
    def __init__(
        self,
        algorithm_id: str = None,
        algorithm_version: str = None,
        request_id: str = None,
    ):
        self.algorithm_id = algorithm_id
        self.algorithm_version = algorithm_version
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.algorithm_id is not None:
            result['AlgorithmId'] = self.algorithm_id
        if self.algorithm_version is not None:
            result['AlgorithmVersion'] = self.algorithm_version
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AlgorithmId') is not None:
            self.algorithm_id = m.get('AlgorithmId')
        if m.get('AlgorithmVersion') is not None:
            self.algorithm_version = m.get('AlgorithmVersion')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ReleaseAlgorithmVersionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ReleaseAlgorithmVersionResponseBody = None,
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
            temp_model = ReleaseAlgorithmVersionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ReleaseMachineGroupResponseBody(TeaModel):
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
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ReleaseMachineGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ReleaseMachineGroupResponseBody = None,
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
            temp_model = ReleaseMachineGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ScaleQuotaRequest(TeaModel):
    def __init__(
        self,
        min: ResourceSpec = None,
        resource_group_ids: List[str] = None,
    ):
        self.min = min
        self.resource_group_ids = resource_group_ids

    def validate(self):
        if self.min:
            self.min.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.min is not None:
            result['Min'] = self.min.to_map()
        if self.resource_group_ids is not None:
            result['ResourceGroupIds'] = self.resource_group_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Min') is not None:
            temp_model = ResourceSpec()
            self.min = temp_model.from_map(m['Min'])
        if m.get('ResourceGroupIds') is not None:
            self.resource_group_ids = m.get('ResourceGroupIds')
        return self


class ScaleQuotaResponseBody(TeaModel):
    def __init__(
        self,
        quota_id: str = None,
        request_id: str = None,
    ):
        # Quota Id
        self.quota_id = quota_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.quota_id is not None:
            result['QuotaId'] = self.quota_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('QuotaId') is not None:
            self.quota_id = m.get('QuotaId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ScaleQuotaResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ScaleQuotaResponseBody = None,
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
            temp_model = ScaleQuotaResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StopTrainingJobResponseBody(TeaModel):
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


class StopTrainingJobResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: StopTrainingJobResponseBody = None,
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
            temp_model = StopTrainingJobResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class TagResourcesRequestTag(TeaModel):
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


class TagResourcesRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        resource_id: List[str] = None,
        resource_type: str = None,
        tag: List[TagResourcesRequestTag] = None,
    ):
        self.region_id = region_id
        self.resource_id = resource_id
        self.resource_type = resource_type
        self.tag = tag

    def validate(self):
        if self.tag:
            for k in self.tag:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        result['Tag'] = []
        if self.tag is not None:
            for k in self.tag:
                result['Tag'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        self.tag = []
        if m.get('Tag') is not None:
            for k in m.get('Tag'):
                temp_model = TagResourcesRequestTag()
                self.tag.append(temp_model.from_map(k))
        return self


class TagResourcesResponseBody(TeaModel):
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


class TagResourcesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: TagResourcesResponseBody = None,
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
            temp_model = TagResourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UntagResourcesRequest(TeaModel):
    def __init__(
        self,
        all: bool = None,
        region_id: str = None,
        resource_id: List[str] = None,
        resource_type: str = None,
        tag_key: List[str] = None,
    ):
        self.all = all
        # This parameter is required.
        self.region_id = region_id
        # This parameter is required.
        self.resource_id = resource_id
        # This parameter is required.
        self.resource_type = resource_type
        self.tag_key = tag_key

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.all is not None:
            result['All'] = self.all
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.tag_key is not None:
            result['TagKey'] = self.tag_key
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('All') is not None:
            self.all = m.get('All')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('TagKey') is not None:
            self.tag_key = m.get('TagKey')
        return self


class UntagResourcesShrinkRequest(TeaModel):
    def __init__(
        self,
        all: bool = None,
        region_id: str = None,
        resource_id_shrink: str = None,
        resource_type: str = None,
        tag_key_shrink: str = None,
    ):
        self.all = all
        # This parameter is required.
        self.region_id = region_id
        # This parameter is required.
        self.resource_id_shrink = resource_id_shrink
        # This parameter is required.
        self.resource_type = resource_type
        self.tag_key_shrink = tag_key_shrink

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.all is not None:
            result['All'] = self.all
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.resource_id_shrink is not None:
            result['ResourceId'] = self.resource_id_shrink
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.tag_key_shrink is not None:
            result['TagKey'] = self.tag_key_shrink
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('All') is not None:
            self.all = m.get('All')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ResourceId') is not None:
            self.resource_id_shrink = m.get('ResourceId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('TagKey') is not None:
            self.tag_key_shrink = m.get('TagKey')
        return self


class UntagResourcesResponseBody(TeaModel):
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


class UntagResourcesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UntagResourcesResponseBody = None,
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
            temp_model = UntagResourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateAlgorithmRequest(TeaModel):
    def __init__(
        self,
        algorithm_description: str = None,
        display_name: str = None,
    ):
        self.algorithm_description = algorithm_description
        self.display_name = display_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.algorithm_description is not None:
            result['AlgorithmDescription'] = self.algorithm_description
        if self.display_name is not None:
            result['DisplayName'] = self.display_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AlgorithmDescription') is not None:
            self.algorithm_description = m.get('AlgorithmDescription')
        if m.get('DisplayName') is not None:
            self.display_name = m.get('DisplayName')
        return self


class UpdateAlgorithmResponseBody(TeaModel):
    def __init__(
        self,
        algorithm_id: str = None,
        request_id: str = None,
    ):
        self.algorithm_id = algorithm_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.algorithm_id is not None:
            result['AlgorithmId'] = self.algorithm_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AlgorithmId') is not None:
            self.algorithm_id = m.get('AlgorithmId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateAlgorithmResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateAlgorithmResponseBody = None,
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
            temp_model = UpdateAlgorithmResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateAlgorithmVersionRequest(TeaModel):
    def __init__(
        self,
        algorithm_spec: AlgorithmSpec = None,
    ):
        self.algorithm_spec = algorithm_spec

    def validate(self):
        if self.algorithm_spec:
            self.algorithm_spec.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.algorithm_spec is not None:
            result['AlgorithmSpec'] = self.algorithm_spec.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AlgorithmSpec') is not None:
            temp_model = AlgorithmSpec()
            self.algorithm_spec = temp_model.from_map(m['AlgorithmSpec'])
        return self


class UpdateAlgorithmVersionShrinkRequest(TeaModel):
    def __init__(
        self,
        algorithm_spec_shrink: str = None,
    ):
        self.algorithm_spec_shrink = algorithm_spec_shrink

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.algorithm_spec_shrink is not None:
            result['AlgorithmSpec'] = self.algorithm_spec_shrink
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AlgorithmSpec') is not None:
            self.algorithm_spec_shrink = m.get('AlgorithmSpec')
        return self


class UpdateAlgorithmVersionResponseBody(TeaModel):
    def __init__(
        self,
        algorithm_id: str = None,
        algorithm_version: str = None,
    ):
        self.algorithm_id = algorithm_id
        self.algorithm_version = algorithm_version

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.algorithm_id is not None:
            result['AlgorithmId'] = self.algorithm_id
        if self.algorithm_version is not None:
            result['AlgorithmVersion'] = self.algorithm_version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AlgorithmId') is not None:
            self.algorithm_id = m.get('AlgorithmId')
        if m.get('AlgorithmVersion') is not None:
            self.algorithm_version = m.get('AlgorithmVersion')
        return self


class UpdateAlgorithmVersionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateAlgorithmVersionResponseBody = None,
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
            temp_model = UpdateAlgorithmVersionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateComponentRequest(TeaModel):
    def __init__(
        self,
        description: str = None,
        display_name: str = None,
        labels: List[Label] = None,
    ):
        self.description = description
        self.display_name = display_name
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
        if self.description is not None:
            result['Description'] = self.description
        if self.display_name is not None:
            result['DisplayName'] = self.display_name
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('DisplayName') is not None:
            self.display_name = m.get('DisplayName')
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = Label()
                self.labels.append(temp_model.from_map(k))
        return self


class UpdateComponentResponseBody(TeaModel):
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


class UpdateComponentResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateComponentResponseBody = None,
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
            temp_model = UpdateComponentResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateComponentVersionRequest(TeaModel):
    def __init__(
        self,
        labels: str = None,
        spec: ComponentSpec = None,
    ):
        self.labels = labels
        self.spec = spec

    def validate(self):
        if self.spec:
            self.spec.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.labels is not None:
            result['Labels'] = self.labels
        if self.spec is not None:
            result['Spec'] = self.spec.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Labels') is not None:
            self.labels = m.get('Labels')
        if m.get('Spec') is not None:
            temp_model = ComponentSpec()
            self.spec = temp_model.from_map(m['Spec'])
        return self


class UpdateComponentVersionResponseBody(TeaModel):
    def __init__(
        self,
        instance_job_id: str = None,
        request_id: str = None,
    ):
        self.instance_job_id = instance_job_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instance_job_id is not None:
            result['InstanceJobId'] = self.instance_job_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceJobId') is not None:
            self.instance_job_id = m.get('InstanceJobId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateComponentVersionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateComponentVersionResponseBody = None,
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
            temp_model = UpdateComponentVersionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateComponentVersionSnapshotResponseBody(TeaModel):
    def __init__(
        self,
        description: str = None,
        request_id: str = None,
    ):
        self.description = description
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.description is not None:
            result['Description'] = self.description
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateComponentVersionSnapshotResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateComponentVersionSnapshotResponseBody = None,
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
            temp_model = UpdateComponentVersionSnapshotResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateQuotaRequest(TeaModel):
    def __init__(
        self,
        description: str = None,
        labels: List[Label] = None,
        queue_strategy: str = None,
        quota_config: QuotaConfig = None,
        quota_name: str = None,
    ):
        self.description = description
        self.labels = labels
        self.queue_strategy = queue_strategy
        self.quota_config = quota_config
        self.quota_name = quota_name

    def validate(self):
        if self.labels:
            for k in self.labels:
                if k:
                    k.validate()
        if self.quota_config:
            self.quota_config.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.description is not None:
            result['Description'] = self.description
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        if self.queue_strategy is not None:
            result['QueueStrategy'] = self.queue_strategy
        if self.quota_config is not None:
            result['QuotaConfig'] = self.quota_config.to_map()
        if self.quota_name is not None:
            result['QuotaName'] = self.quota_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Description') is not None:
            self.description = m.get('Description')
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = Label()
                self.labels.append(temp_model.from_map(k))
        if m.get('QueueStrategy') is not None:
            self.queue_strategy = m.get('QueueStrategy')
        if m.get('QuotaConfig') is not None:
            temp_model = QuotaConfig()
            self.quota_config = temp_model.from_map(m['QuotaConfig'])
        if m.get('QuotaName') is not None:
            self.quota_name = m.get('QuotaName')
        return self


class UpdateQuotaResponseBody(TeaModel):
    def __init__(
        self,
        quota_id: str = None,
        request_id: str = None,
    ):
        # Quota Id
        self.quota_id = quota_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.quota_id is not None:
            result['QuotaId'] = self.quota_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('QuotaId') is not None:
            self.quota_id = m.get('QuotaId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateQuotaResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateQuotaResponseBody = None,
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
            temp_model = UpdateQuotaResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateQuotaLabelsRequest(TeaModel):
    def __init__(
        self,
        labels: List[Label] = None,
    ):
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
                temp_model = Label()
                self.labels.append(temp_model.from_map(k))
        return self


class UpdateQuotaLabelsResponseBody(TeaModel):
    def __init__(
        self,
        quota_id: str = None,
        request_id: str = None,
    ):
        self.quota_id = quota_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.quota_id is not None:
            result['QuotaId'] = self.quota_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('QuotaId') is not None:
            self.quota_id = m.get('QuotaId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateQuotaLabelsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateQuotaLabelsResponseBody = None,
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
            temp_model = UpdateQuotaLabelsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateResourceGroupRequest(TeaModel):
    def __init__(
        self,
        description: str = None,
        name: str = None,
        unbind: bool = None,
        user_vpc: UserVpc = None,
    ):
        self.description = description
        self.name = name
        self.unbind = unbind
        self.user_vpc = user_vpc

    def validate(self):
        if self.user_vpc:
            self.user_vpc.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.description is not None:
            result['Description'] = self.description
        if self.name is not None:
            result['Name'] = self.name
        if self.unbind is not None:
            result['Unbind'] = self.unbind
        if self.user_vpc is not None:
            result['UserVpc'] = self.user_vpc.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Unbind') is not None:
            self.unbind = m.get('Unbind')
        if m.get('UserVpc') is not None:
            temp_model = UserVpc()
            self.user_vpc = temp_model.from_map(m['UserVpc'])
        return self


class UpdateResourceGroupResponseBody(TeaModel):
    def __init__(
        self,
        resource_group_id: str = None,
        request_id: str = None,
    ):
        self.resource_group_id = resource_group_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.resource_group_id is not None:
            result['ResourceGroupID'] = self.resource_group_id
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ResourceGroupID') is not None:
            self.resource_group_id = m.get('ResourceGroupID')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class UpdateResourceGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateResourceGroupResponseBody = None,
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
            temp_model = UpdateResourceGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateResourceGroupMachineGroupRequest(TeaModel):
    def __init__(
        self,
        name: str = None,
    ):
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class UpdateResourceGroupMachineGroupResponseBody(TeaModel):
    def __init__(
        self,
        machine_group_id: str = None,
        request_id: str = None,
    ):
        self.machine_group_id = machine_group_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.machine_group_id is not None:
            result['MachineGroupID'] = self.machine_group_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MachineGroupID') is not None:
            self.machine_group_id = m.get('MachineGroupID')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateResourceGroupMachineGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateResourceGroupMachineGroupResponseBody = None,
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
            temp_model = UpdateResourceGroupMachineGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateTrainingJobLabelsRequestLabels(TeaModel):
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


class UpdateTrainingJobLabelsRequest(TeaModel):
    def __init__(
        self,
        labels: List[UpdateTrainingJobLabelsRequestLabels] = None,
    ):
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
                temp_model = UpdateTrainingJobLabelsRequestLabels()
                self.labels.append(temp_model.from_map(k))
        return self


class UpdateTrainingJobLabelsResponseBody(TeaModel):
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


class UpdateTrainingJobLabelsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateTrainingJobLabelsResponseBody = None,
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
            temp_model = UpdateTrainingJobLabelsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


