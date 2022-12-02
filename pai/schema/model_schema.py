from marshmallow import EXCLUDE, fields, post_load

from pai.schema.base import BaseAPIResourceSchema, ListOfKVField


class ModelSchema(BaseAPIResourceSchema):
    class Meta(object):
        unknown = EXCLUDE

    FieldNameMapping = {
        "GmtCreateTime": "create_time",
        "GmtModifiedTime": "modified_time",
        "ModelName": "name",
    }

    name = fields.Str()
    labels = ListOfKVField()
    workspace_id = fields.Str()
    accessibility = fields.Str(required=True)

    # Load only fields
    model_id = fields.Str(load_only=True)
    create_time = fields.DateTime(load_only=True)
    modified_time = fields.DateTime(load_only=True)

    @post_load
    def _make(self, data, **kwargs):
        from pai.model import Model

        return self.make_or_reload(Model, data)


class ModelVersionSchema(BaseAPIResourceSchema):
    class Meta(object):
        unknown = EXCLUDE

    FieldNameMapping = {
        "GmtCreateTime": "create_time",
        "GmtModifiedTime": "modified_time",
        "VersionName": "version",
        "FormatType": "model_format",
        "FrameworkType": "framework",
    }

    name = fields.Str()
    workspace_id = fields.Str()
    model_id = fields.Str()

    model = fields.Nested(ModelSchema)

    version = fields.Str()
    description = fields.Str()
    uri = fields.Str()
    labels = ListOfKVField()
    model_format = fields.Str()
    framework = fields.Str()
    inference_spec = fields.Dict()

    # Load only fields
    create_time = fields.DateTime(load_only=True)
    modified_time = fields.DateTime(load_only=True)

    @post_load
    def _make(self, data, **kwargs):
        from pai.model import ModelVersion

        return self.make_or_reload(ModelVersion, data)
