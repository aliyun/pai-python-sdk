from __future__ import absolute_import

import re
from decimal import Decimal

import six
from enum import Enum

from pai.pipeline.variable import PipelineVariable

StringType = six.string_types

int_float_types = tuple(list(six.integer_types) + list([float]))

_PRIMITIVE_TYPE_MAP = {
    "Int": six.integer_types,
    "Double": int_float_types,
    "Bool": bool,
    "Str": six.string_types
}

NEGATIVE_INFINITY = Decimal("-infinity")
POSITIVE_INFINITY = Decimal("infinity")


class PipelineParameter(PipelineVariable):
    variable_category = "parameters"

    def __init__(self, name, typ, **kwargs):
        super(PipelineParameter, self).__init__(name=name, typ=typ, **kwargs)

    def validate_value(self, val):
        if self.typ in _PRIMITIVE_TYPE_MAP:
            # error hint because of pycharm bug
            # https://stackoverflow.com/questions/56493140/parameterized-generics-cannot-be-used-with-class-or-instance-checks
            if not isinstance(val, _PRIMITIVE_TYPE_MAP[self.typ]):
                return False
        if self.validator and not self.validator.validate(val):
            return False
        return True

    @classmethod
    def to_argument_by_spec(cls, val, param_spec):
        param_spec = param_spec.copy()

        typ = param_spec.pop("type", None)
        name = param_spec.pop("name")
        kind = "inputs"
        from_ = param_spec.pop("from", None)
        feasible = param_spec.pop("feasible", None)
        value = param_spec.pop("value", None)
        desc = param_spec.pop("desc", None)
        required = param_spec.pop("required", False)

        param = create_pipeline_parameter(name=name, typ=typ, kind=kind, from_=from_, value=value,
                                          desc=desc,
                                          required=required, feasible=feasible)
        if not param.validate_value(val):
            raise ValueError(
                "Not Validate value for Parameter %s, value(%s:%s)" % (name, type(val), val))
        param.value = val
        return param.to_argument()


class ParameterValidator(object):
    def __init__(self, interval=None):
        self.interval = interval

    @classmethod
    def load(cls, feasible):
        validator = cls()
        if "range" in feasible:
            validator.interval = Interval.load(feasible["range"])
        return validator

    def validate(self, value):
        if self.interval and not self.interval.validate(value):
            return False
        return True

    def to_dict(self):
        return {
            "range": str(self.interval),
        }


class Interval(object):
    """Range validator of pipeline parameter."""

    _NUMBER_REGEXP = r"(-?(?:(?:[\d]+(\.[\d]*)?)|INF))"
    INTERVAL_PATTERN = re.compile(
        r"^([(\[])\s*{number_pattern}\s*,\s*{number_pattern}([)\]])$".format(
            number_pattern=_NUMBER_REGEXP))

    def __init__(self, min_, max_, min_inclusive, max_inclusive):
        self.min_ = min_
        self.max_ = max_
        self.min_inclusive = min_inclusive
        self.max_inclusive = max_inclusive

    def __str__(self):
        return "{left}{min_}, {max_}{right}".format(
            left="[" if self.min_inclusive else "(",
            min_=self.value_str(self.min_),
            max_=self.value_str(self.max_),
            right="]" if self.max_inclusive else "[",
        )

    @staticmethod
    def value_str(val):
        if val == POSITIVE_INFINITY:
            return "INF"
        elif val == NEGATIVE_INFINITY:
            return "-INF"
        else:
            return str(val)

    @classmethod
    def load(cls, feasible):
        m = cls.INTERVAL_PATTERN.match(feasible)
        if not m:
            raise ValueError("parameter feasible %s not match pattern" % feasible)

        left, min_, min_fraction, max_, max_fraction, right = m.groups()
        if min_fraction:
            min_ = Decimal(min_)
        elif min_ not in ("-INF", "INF"):
            min_ = int(min_)
        else:
            min_ = Decimal(min_)

        if max_fraction:
            max_ = Decimal(max_)
        elif max_ not in ("-INF", "INF"):
            max_ = int(max_)
        else:
            max_ = Decimal(max_)

        interval = Interval(min_, max_, left == "[", right == "]")
        if not interval._validate_bound():
            raise ValueError("invalid range: lower bound greater than upper bound is not allowed")
        return interval

    def _validate_bound(self):
        if Decimal(self.min_) > Decimal(self.max_):
            return False

        if self.min_ == self.max_ and not (self.min_inclusive or self.max_inclusive):
            return False
        return True

    def validate(self, val):
        if self.min_ < val < self.max_:
            return True

        if self.min_ == val and self.min_inclusive:
            return True
        if self.max_ == val and self.max_inclusive:
            return True

        return False


ParameterTypeMapping = {
    "long": "Int",
    "integer": "Int",
    "int": "Int",
    "double": "Double",
    "float": "Double",
    "string": "String",
    "str": "String",
    "bool": "Bool",
    "boolean": "Bool",
    "map": "Map",
    "dict": "Map",
    "array": "Array",
    "list": "Array"
}


class ParameterType(Enum):
    String = "String"
    Integer = "Int"
    Double = "Double"
    Bool = "Bool"
    Map = "Map"
    Array = "Array"

    @classmethod
    def normalize_typ(cls, typ_instance):
        if isinstance(typ_instance, type):
            type_name = typ_instance.__name__.lower()
        elif isinstance(typ_instance, six.string_types):
            type_name = typ_instance.lower()
        elif isinstance(typ_instance, cls):
            return typ_instance
        else:
            raise ValueError("Not Supported PipelineParameter Type: {typ}".format(typ=typ_instance))
        return ParameterType(ParameterTypeMapping[type_name])


def create_pipeline_parameter(name, typ, kind, desc=None, required=False, value=None,
                              parent=None, from_=None, **kwargs):
    typ = ParameterType.normalize_typ(typ)
    validator = None
    feasible = kwargs.get("feasible", None)

    if feasible:
        validator = ParameterValidator.load(feasible)

    return PipelineParameter(name=name, typ=typ, kind=kind, desc=desc, required=required,
                             value=value, from_=from_, parent=parent, validator=validator)
