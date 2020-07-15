from __future__ import absolute_import

import itertools

import six
from enum import Enum

PyParameterTypes = tuple(itertools.chain(six.integer_types, six.string_types, [dict, list, bool]))


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
