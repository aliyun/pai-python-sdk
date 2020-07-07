from __future__ import absolute_import

from pai.pipeline.pipeline_variable import PipelineVariable
from enum import Enum


class ArtifactDataType(Enum):
    DataSet = "DataSet"
    Model = "Model"


class ArtifactLocationType(Enum):
    MaxComputeTable = "MaxComputeTable"
    MaxComputeVolume = "MaxComputeVolume"


class ArtifactModelType(Enum):
    OfflineModel = "OfflineModel"
    PMML = "PMML"


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
    def to_argument_by_spec(cls, val, af_spec):
        name = af_spec.pop("name")
        typ = af_spec.pop("type")
        kind = "inputs"
        from_ = af_spec.pop("from", None)
        param = create_artifact(name=name, typ=typ, kind=kind, from_=from_, **af_spec)
        if not param.validate_value(val):
            raise ValueError("Not Validate value for Parameter %s, value(%s:%s)" % (name, type(val), val))
        param.value = val
        return param.to_argument()


def create_artifact(name, typ, kind, desc=None, required=None, value=None, from_=None, parent=None):
    return PipelineArtifact(name=name, typ=typ, kind=kind, desc=desc, required=required, value=value,
                            parent=parent, from_=from_)


class ArtifactType(object):

    def __init__(self, data_type, location_type, model_type=None):
        self.data_type = data_type
        self.location_type = location_type
        self.model_type = model_type

    def to_dict(self):
        d = {
            self.data_type.value: {
                "locationType": self.location_type.value,
            }
        }

        if self.model_type is not None:
            d[self.data_type.value]["modelType"] = self.model_type.value

        return d

    @classmethod
    def from_dict(cls, d):
        data_type = ArtifactDataType(d.keys()[0])
        location_type = ArtifactLocationType(d[data_type.value]["locationType"])
        model_type = None
        if "modelType" in d[data_type.value]:
            model_type = ArtifactModelType(d[data_type.value]["modelType"])

        return cls(data_type=data_type, location_type=location_type, model_type=model_type)

