from marshmallow import EXCLUDE, fields, post_load

from pai.schema.base import BaseAPIResourceSchema


class EcsSpecSchema(BaseAPIResourceSchema):
    """EcsSpec schema."""

    class Meta(object):
        unknown = EXCLUDE

    accelerator_type = fields.Str()
    cpu = fields.Int()
    gpu = fields.Int()
    gpu_type = fields.Str()
    instance_type = fields.Str()
    memory = fields.Int()

    @post_load
    def _make(self, data, **kwargs):
        from pai.job import EcsSpec

        return EcsSpec(**data)
