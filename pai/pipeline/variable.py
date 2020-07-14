from __future__ import absolute_import

from abc import ABCMeta, abstractmethod

from six import with_metaclass


class PipelineVariable(with_metaclass(ABCMeta, object)):
    """Base class of Artifact and PipelineParameter."""

    variable_category = None

    def __init__(self, name, typ, desc=None, kind="inputs", value=None, from_=None, required=None,
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

        assert kind in ("inputs", "outputs")

        self.name = name
        self.kind = kind
        self.typ = typ
        self.desc = desc
        self.value = value
        self.from_ = from_
        self.required = required
        self.parent = parent
        self.validator = validator
        self._is_assigned = False

    @abstractmethod
    def validate_value(self, val):
        pass

    def validate_from(self, arg):
        if not isinstance(arg, PipelineVariable):
            raise ValueError("arg is expected to be type of 'PipelineVariable' "
                             "but was actually of type '%s'" % type(arg))

        if arg.typ is not None and self.typ is not None and arg.typ != self.typ:
            return False

        if arg.variable_category != self.variable_category:
            return False

        return True

    def assign(self, arg):
        if self._is_assigned:
            raise ValueError("Input:%s has been assigned." % self.name)

        if not isinstance(arg, PipelineVariable):
            if not self.validate_value(arg):
                raise ValueError("Arg:%s is invalid value for %s" % (arg, self))
            self.value = arg
        elif arg.parent is None:
            if not self.validate_value(arg.value):
                raise ValueError("Value(%s) is invalid value for %s" % (arg.value, self))
            self.value = arg.value
        else:
            if not self.validate_from(arg):
                raise ValueError(
                    "invalid assignment. %s left: %s, right: %s" % (
                        self.fullname, self.typ, arg.typ))
            self.from_ = arg
        self._is_assigned = True

    @property
    def is_assigned(self):
        return self._is_assigned

    @property
    def fullname(self):
        """Unique identifier in pipeline manifest for PipelineVariable"""
        return ".".join(
            filter(None, [self.parent.ref_name, self.kind, self.variable_category, self.name]))

    def __str__(self):
        return "{name}:{kind}:{variable_category}:{typ}".format(
            name=self.name,
            kind=self.kind,
            variable_category=self.variable_category,
            typ=self.typ
        )

    def to_argument(self):
        arguments = {
            "name": self.name
        }

        if self.from_ is not None:
            if isinstance(self.from_, PipelineVariable):
                arguments["from"] = "{{%s}}" % self.from_.fullname
            else:
                arguments["from"] = self.from_
        elif self.value is not None:
            arguments["value"] = self.value
        return arguments

    def to_dict(self):
        d = {
            "name": self.name,
        }

        if self.typ:
            d["type"] = self.typ
        if self.required:
            d["required"] = self.required
        if self.validator:
            d["feasible"] = self.validator.to_dict()

        if self.value is not None:
            d["value"] = self.value
        elif self.from_ is not None:
            if isinstance(self.from_, PipelineVariable):
                d["from"] = "{{%s}}" % self.from_.fullname
            else:
                d["from"] = self.from_

        return d
