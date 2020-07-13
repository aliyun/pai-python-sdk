from __future__ import absolute_import
import six

import itertools
from enum import Enum

PyParameterTypes = tuple(itertools.chain(six.integer_types, six.string_types, [dict, list, bool]))


class ParameterType(Enum):
    String = "String"
    Integer = "Integer"
    Double = "Double"
    Bool = "Bool"
    Map = "Map"


class ArtifactDataType(Enum):
    DataSet = "DataSet"
    Model = "Model"
    ModelEvaluation = "ModelEvaluation"


class ArtifactLocationType(Enum):
    MaxComputeTable = "MaxComputeTable"
    MaxComputeVolume = "MaxComputeVolume"
    MaxComputeOfflineModel = "MaxComputeOfflineModel"


class ArtifactModelType(Enum):
    OfflineModel = "OfflineModel"
    PMML = "PMML"
