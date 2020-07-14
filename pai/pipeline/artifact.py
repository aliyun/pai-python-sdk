from __future__ import absolute_import

from pai.pipeline.variable import PipelineVariable
from pai.pipeline.base import ArtifactModelType, ArtifactLocationType, ArtifactDataType


class PipelineArtifact(PipelineVariable):
    variable_category = "artifacts"

    def __init__(self, name, typ, desc=None, kind="input", value=None, from_=None, required=None, parent=None):
        super(PipelineArtifact, self).__init__(name=name, typ=typ, desc=desc, kind=kind, value=value, from_=from_,
                                               required=required, parent=parent)

    # TODO: value format of artifact is not set down.
    def validate_value(self, val):
        return True

    # TODO: Artifact Value and Type Refactor
    @classmethod
    def to_argument_by_spec(cls, val, af_spec, kind="inputs"):
        af_spec = af_spec.copy()

        name = af_spec.pop("name")
        typ = af_spec.pop("type")
        desc = af_spec.pop("desc")
        value = af_spec.pop("value")
        from_ = af_spec.pop("from")
        required = af_spec.pop("required")

        param = create_artifact(name=name, typ=typ, kind=kind, from_=from_, required=required, value=value,
                                desc=desc)
        if not param.validate_value(val):
            raise ValueError("Not Validate value for Parameter %s, value(%s:%s)" % (name, type(val), val))
        param.value = val
        return param.to_argument()

    def to_dict(self):
        d = super(PipelineArtifact, self).to_dict()
        if isinstance(self.typ, ArtifactType):
            d["type"] = self.typ.to_dict()

        return d


def create_artifact(name, typ, kind, desc=None, required=None, value=None, from_=None, parent=None):
    return PipelineArtifact(name=name, typ=typ, kind=kind, desc=desc, required=required, value=value,
                            parent=parent, from_=from_)


class ArtifactType(object):

    def __init__(self, data_type, location_type, model_type=None):
        self.data_type = data_type
        self.location_type = location_type
        self.model_type = model_type

    def __str__(self):
        return '{%s}:{locationType:%s, modelType:%s}' % (self.data_type, self.location_type, self.model_type)

    def to_dict(self):
        d = {
            self.data_type.value: {
                "locationType": self.location_type.value,
            }
        }

        if self.model_type is not None:
            d[self.data_type.value]["modelType"] = self.model_type.value

        return d

    def __eq__(self, other):

        if isinstance(other, ArtifactType):
            return self.data_type == other.data_type and self.location_type == other.location_type \
                   and self.model_type == other.model_type
        elif isinstance(other, dict):
            other = self.from_dict(other)
            return self.data_type == other.data_type and self.location_type == other.location_type \
                   and self.model_type == other.model_type
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def from_dict(cls, d):
        data_type = ArtifactDataType(list(d.keys())[0])
        location_type = ArtifactLocationType(d[data_type.value]["locationType"])
        model_type = None
        if "modelType" in d[data_type.value]:
            model_type = ArtifactModelType(d[data_type.value]["modelType"])

        return cls(data_type=data_type, location_type=location_type, model_type=model_type)


class ArtifactValue(object):
    def __init__(self):
        pass


class MaxComputeTableArtifact(ArtifactValue):

    def __init__(self, table, project, endpoint, owner, rolearn):
        super(MaxComputeTableArtifact, self).__init__()
        self.project = project
        self.endpoint = endpoint
        self.owner = owner
        self.rolearn = rolearn
        self.table = table


class MaxComputeOfflineModelArtifact(ArtifactValue):

    def __init__(self, name, endpoint, project, rolearn):
        super(MaxComputeOfflineModelArtifact, self).__init__()
        self.project = project
        self.endpoint = endpoint
        self.rolearn = rolearn
        self.name = name


class OSSArtifact(ArtifactValue):

    def __init__(self, bucket, key, endpoint, rolearn):
        super(OSSArtifact, self).__init__()
        self.bucket = bucket
        self.endpoint = endpoint
        self.rolearn = rolearn
        self.key = key
