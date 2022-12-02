from marshmallow import fields, post_load

from pai.schema.base import BaseAPIResourceSchema


class HyperparameterDefinitionSchema(BaseAPIResourceSchema):
    default_value = fields.Str()
    description = fields.Str()
    name = fields.Str()
    required = fields.Bool()
    type = fields.Str()

    @post_load
    def _make(self, data, **kwargs):
        from pai.algorithm import HyperparameterDefinition

        return HyperparameterDefinition(**data)


class MetricDefinitionSchema(BaseAPIResourceSchema):
    description = fields.Str()
    name = fields.Str()
    regex = fields.Str()

    @post_load
    def _make(self, data, **kwargs):
        from pai.algorithm import MetricDefinition

        return MetricDefinition(**data)


class ChannelDefinitionSchema(BaseAPIResourceSchema):
    description = fields.Str()
    name = fields.Str()
    properties = fields.List(fields.Dict)
    required = fields.Bool()
    supported_channel_types = fields.List(fields.Str)

    @post_load
    def _make(self, data, **kwargs):
        from pai.algorithm import ChannelDefinition

        return ChannelDefinition(**data)


class AlgorithmSpecSchema(BaseAPIResourceSchema):

    command = fields.List(fields.Str)
    hyperparameters = fields.List(fields.Nested(HyperparameterDefinitionSchema))
    image = fields.Str()
    input_channels = fields.List(fields.Nested(ChannelDefinitionSchema))
    output_channels = fields.List(fields.Nested(ChannelDefinitionSchema))
    job_type = fields.Str()
    metric_definitions = fields.List(fields.Nested(MetricDefinitionSchema))
    supported_instance_types = fields.List(fields.Str)
    supported_distributed_training = fields.Bool()

    @post_load
    def _make(self, data, **kwargs):
        from pai.algorithm import AlgorithmSpec

        return AlgorithmSpec(**data)


class AlgorithmVersionSchema(BaseAPIResourceSchema):

    algorithm_spec = fields.Nested(AlgorithmSpecSchema)
    algorithm_name = fields.Str()
    algorithm_version = fields.Str()

    # load only
    algorithm_provider = fields.Str(load_only=True)
    algorithm_id = fields.Str(load_only=True)
    tenant_id = fields.Str(load_only=True)
    user_id = fields.Str(load_only=True)

    @post_load
    def _make(self, data, **kwargs):
        from pai.algorithm import AlgorithmVersion

        return self.make_or_reload(AlgorithmVersion, data)


class AlgorithmSchema(BaseAPIResourceSchema):

    algorithm_description = fields.Str()
    algorithm_name = fields.Str()
    workspace_id = fields.Str()

    # load only
    algorithm_provider = fields.Str(load_only=True)
    algorithm_id = fields.Str(load_only=True)
    create_time = fields.DateTime(load_only=True)
    modified_time = fields.DateTime(load_only=True)
    tenant_id = fields.Str(load_only=True)
    user_id = fields.Str(load_only=True)

    @post_load
    def _make(self, data, **kwargs):
        from pai.algorithm import Algorithm

        return self.make_or_reload(Algorithm, data)
