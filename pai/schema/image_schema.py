from marshmallow import EXCLUDE, fields, post_load

from pai.schema.base import BaseAPIResourceSchema

from .base import ListOfKVField


class ImageSchema(BaseAPIResourceSchema):
    """Image schema."""

    class Meta(object):
        unknown = EXCLUDE

    FieldNameMapping = {
        "GmtCreateTime": "create_time",
        "GmtModifiedTime": "modified_time",
    }

    name = fields.Str()
    workspace_id = fields.Str()
    description = fields.Str()
    accessibility = fields.Str(required=True)
    labels = ListOfKVField()
    image_uri = fields.Str()

    # Load only fields.
    image_id = fields.Str(load_only=True)
    create_time = fields.DateTime(load_only=True)
    modified_time = fields.DateTime(load_only=True)

    @post_load
    def _make(self, data, **kwargs):
        from pai.entity import Image

        return Image(**data)
