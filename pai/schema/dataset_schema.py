import json
import logging

import six
from marshmallow import EXCLUDE, Schema, fields, post_load

from .base import BaseAPIResourceSchema, ListOfKVField

logger = logging.getLogger(__name__)


class DatasetSchema(BaseAPIResourceSchema):
    """Dataset schema."""

    class Meta(object):
        unknown = EXCLUDE

    FieldNameMapping = {
        "GmtCreateTime": "create_time",
        "GmtModifiedTime": "modified_time",
    }

    data_source_type = fields.Str()
    data_type = fields.Str()
    description = fields.Str()
    name = fields.Str()
    options = fields.Str()
    property = fields.Str()
    source_id = fields.Str()
    source_type = fields.Str()
    uri = fields.Str()
    workspace_id = fields.Str()
    accessibility = fields.Str()
    labels = ListOfKVField()

    # Load only fields.
    mount_path = fields.Str()
    dataset_id = fields.Str(load_only=True)
    create_time = fields.DateTime(load_only=True)
    modified_time = fields.DateTime(load_only=True)
    owner_id = fields.Str(load_only=True)

    @post_load
    def _make(self, data, **kwargs):
        from pai.entity import Dataset

        mount_path = self._get_mount_path_from_options(data)
        if mount_path:
            data.update({"mount_path": mount_path})

        return self.make_or_reload(instance_cls=Dataset, data=data)

    @classmethod
    def _get_mount_path_from_options(cls, data):
        options = data.get("options", None)
        if not options:
            return
        if not isinstance(options, dict):
            try:
                options = json.loads(options)
            except json.JSONDecodeError as e:
                logger.warning(
                    "Unexpected options value for Dataset: JSONDecodeError={0} options={1}".format(
                        e, options
                    )
                )
                return

        return options.get("mountPath")
