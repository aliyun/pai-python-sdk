from marshmallow import EXCLUDE, fields, post_load, validate

from .base import BaseAPIResourceSchema


class CodeSourceSchema(BaseAPIResourceSchema):
    """CodeSource schema."""

    class Meta(object):
        unknown = EXCLUDE

    FieldNameMapping = {
        "GmtCreateTime": "create_time",
        "GmtModifyTime": "modified_time",
    }

    code_branch = fields.Str()
    code_repo = fields.Str(validate=validate.URL(), required=True)
    code_repo_access_token = fields.Str()
    code_repo_user_name = fields.Str()

    description = fields.Str()
    display_name = fields.Str()
    mount_path = fields.Str()
    workspace_id = fields.Str()
    accessibility = fields.Str()

    # Load only fields.
    code_source_id = fields.Str(load_only=True)
    create_time = fields.DateTime(load_only=True)
    modified_time = fields.DateTime(load_only=True)

    @post_load
    def _make(self, data, **kwargs):
        from pai.entity import CodeSource

        return self.make_or_reload(instance_cls=CodeSource, data=data)
