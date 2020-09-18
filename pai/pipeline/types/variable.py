from __future__ import absolute_import

from abc import ABCMeta, abstractmethod

from six import with_metaclass


class PipelineVariable(with_metaclass(ABCMeta, object)):
    """Base class of Artifact and PipelineParameter."""

    variable_category = None

    def __init__(self, name, desc=None, kind="inputs", value=None, from_=None, required=None,
                 parent=None, validator=None):
        """

        Args:
            name: name of parameter.
            desc: parameter description.
            kind: usage of PipelineParameter in pipeline, either "input" or "output"
            value: default value of parameter
            from_:
            required:
            validator: parameter value validator.
            parent:
        """
        self.name = name
        self.kind = kind
        self.desc = desc
        self.value = value
        self.from_ = from_
        self.required = required
        self.parent = parent
        self.validator = validator

    # TODO: validate if pipeline variable attribute is legal
    def _validate_spec(self):
        pass

    @abstractmethod
    def validate_value(self, val):
        pass

    def assign(self, arg):
        if not isinstance(arg, PipelineVariable):
            if not self.validate_value(arg):
                raise ValueError("Arg:%s is invalid value for %s" % (arg, self))
            self.value = arg
        elif arg.parent is None:
            if not self.validate_value(arg.value):
                raise ValueError("Value(%s) is invalid value for %s" % (arg.value, self))
            self.value = arg.value
            self.from_ = arg
        else:
            if not self.validate_from(arg):
                raise ValueError(
                    "invalid assignment. %s left: %s, right: %s" % (
                        self.fullname, self.typ, arg.typ))
            self.from_ = arg

    @property
    def is_assigned(self):
        return self._is_assigned

    @property
    def fullname(self):
        """Unique identifier in pipeline manifest for PipelineVariable"""
        if self.parent:
            return ".".join(
                [self.parent.ref_name, self.kind, self.variable_category, self.name])
        else:
            return ".".join([self.kind, self.variable_category, self.name])

    @property
    def enclosed_fullname(self):
        return "{{%s}}" % self.fullname

    def __repr__(self):
        return "%s:{Name:%s, Kind:%s, Required:%s, Value:%s, Desc:%s}" % (
            type(self).__name__,
            self.name,
            self.kind,
            self.required,
            self.value,
            self.desc,
        )

    def to_argument(self):
        arguments = {
            "name": self.name
        }

        if self.from_ is not None:
            if isinstance(self.from_, PipelineVariable):
                arguments["from"] = self.enclosed_fullname
            else:
                arguments["from"] = self.from_
        elif self.value is not None:
            arguments["value"] = self.value
        return arguments

    def to_dict(self):
        d = {
            "name": self.name,
        }

        if self.validator:
            d["feasible"] = self.validator.to_dict()

        elif self.from_ is not None:
            if isinstance(self.from_, PipelineVariable):
                d["from"] = "{{%s}}" % self.from_.fullname
            else:
                d["from"] = self.from_

        return d
