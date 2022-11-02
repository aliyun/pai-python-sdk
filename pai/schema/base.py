from marshmallow import EXCLUDE, Schema, fields, post_dump, pre_load

from pai.common.utils import camel_to_snake, snake_to_camel


class EntitySchema(Schema):
    def __init__(self, instance=None, **kwargs):
        super(EntitySchema, self).__init__(**kwargs)
        self.instance = instance


class BaseAPIResourceSchema(Schema):
    """Base schema using in API object serialization and deserialization."""

    class Meta(object):
        unknown = EXCLUDE

    _DefaultFieldsNameMapping = {
        "GmtCreateTime": "create_time",
        "GmtModifiedTime": "modified_time",
    }

    # Mapping API object field name to Python Object/Schema field name..
    FieldNameMapping = {}

    def __init__(self, instance=None, session=None, **kwargs):
        super(BaseAPIResourceSchema, self).__init__(**kwargs)
        self.instance = instance
        self.session = session

    @pre_load
    def _filed_name_load_preprocess(self, data, **kwargs):
        """Input API object preprocess.

        Transform the input data key to entity filed name.
        """
        result = dict()
        for name, value in data.items():
            if name in self.FieldNameMapping:
                result[self.FieldNameMapping[name]] = value
            else:
                result[camel_to_snake(name)] = value
        return result

    @post_dump
    def _filed_name_dump_postprocess(self, data, **kwargs):
        """Transform output field name to camel case."""
        filed_name_mapping = self._DefaultFieldsNameMapping.copy()
        filed_name_mapping.update(self.FieldNameMapping)

        field_mapping_rev = {value: key for key, value in filed_name_mapping.items()}
        result = dict()
        for key, value in data.items():
            if value is None:
                continue
            if key in field_mapping_rev:
                result[field_mapping_rev[key]] = value
            else:
                result[snake_to_camel(key)] = value
        return result

    def make_or_reload(self, instance_cls, data):
        """Make an instance or reload the instance."""
        if self.instance:
            self.instance.__init__(**data)
            return self.instance
        else:
            return instance_cls(session=self.session, **data)


class ListOfKVField(fields.Field):
    """Mapping a List of key, value to a Dict."""

    def _serialize(self, value, attr, obj, **kwargs):
        res = []
        if not value:
            return res
        for k, v in value.items():
            res.append(
                {
                    "Key": k,
                    "Value": v,
                }
            )
        return res

    def _deserialize(self, value, attr, data, **kwargs):
        res = dict()
        if not value:
            return res
        for item in value:
            res[item["Key"]] = item["Value"]
        return res
