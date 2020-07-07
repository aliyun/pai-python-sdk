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
