import copy

import six

from collections import Counter
from .artifact import ArtifactMetadata, PipelineArtifact
from .parameter import PipelineParameter


def validate_spec(items):
    if not items:
        return
    counter = Counter((item.name for item in items))
    conflicts = {key for key, count in counter.items() if count > 1}
    if conflicts:
        raise ValueError("Parameter/Artifact names conflict:%s" % (','.join(conflicts)))

    # ensure parameters is prior to artifacts in list
    af_pos = next((idx for idx, item in enumerate(items) if item.variable_category == "artifacts"),
                  len(items))

    idx = next(
        (idx for idx in range(af_pos, len(items)) if items[idx].variable_category == "parameters"),
        len(items))
    if idx != len(items):
        raise ValueError("Please ensure parameters is prior to artifacts in the spec list")


class SpecBase(object):

    def __init__(self, items):
        self._items = items
        self._indexer = {item.name: idx for idx, item in enumerate(items)}
        validate_spec(items)

    @property
    def items(self):
        return self._items

    def __repr__(self):
        return '%s:\n%s' % (
            type(self).__name__, '\n'.join(['\t' + str(item) for item in self._items]))

    def _repr_html(self):
        pass

    def __getitem__(self, key):
        if isinstance(key, six.integer_types):
            return self._items[key]
        elif isinstance(key, six.string_types):
            return self._items[self._indexer[key]]
        elif isinstance(key, slice):
            return self._items.__getitem__(key)

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def to_dict(self):
        af_pos = next(
            (idx for idx, item in enumerate(self._items) if item.variable_category == "artifacts"),
            len(self._items))

        d = {
            "parameters": [param.to_dict() for param in self._items[:af_pos]],
            "artifacts": [af.to_dict() for af in self._items[af_pos:]]
        }
        return d


class InputsSpec(SpecBase):

    def __init__(self, inputs):
        super(InputsSpec, self).__init__(items=inputs)

    def assign(self, inputs_args):
        """

        Args:
            inputs_args:
        """
        assign_items = []
        if isinstance(inputs_args, list):
            for idx, arg in enumerate(inputs_args):
                self._items[idx].assign(arg)
                assign_items.append(self.items[idx])
        elif isinstance(inputs_args, dict):
            for k, v in inputs_args.items():
                self._items[self._indexer[k]].assign(v)
                assign_items.append(self._items[self._indexer[k]])
        else:
            raise ValueError(
                "Unexpected input_args type:%s, required list or dict" % type(inputs_args))
        return assign_items


class OutputsSpec(SpecBase):

    def __init__(self, outputs):
        super(OutputsSpec, self).__init__(items=outputs)


def load_input_output_spec(p, spec):
    inputs = []
    outputs = []
    spec = copy.deepcopy(spec)
    for param in spec["inputs"].get("parameters", []):
        inputs.append(_load_parameter_spec(p, param.copy(), "inputs"))

    for af in spec["inputs"].get("artifacts", []):
        inputs.append(_load_artifact_spec(p, af, "inputs"))

    for param in spec["outputs"].get("parameters", []):
        outputs.append(_load_parameter_spec(p, param, "outputs"))

    for af in spec["outputs"].get("artifacts", []):
        outputs.append(_load_artifact_spec(p, af, "outputs"))
    return InputsSpec(inputs), OutputsSpec(outputs)


def _load_parameter_spec(p, param_spec, kind):
    typ = param_spec.pop("type", None)
    name = param_spec.pop("name")
    from_ = param_spec.pop("from", None)
    feasible = param_spec.pop("feasible", None)
    value = param_spec.pop("value", None)
    desc = param_spec.pop("desc", None)

    param = PipelineParameter(name=name, typ=typ, default=value, desc=desc, kind=kind, from_=from_,
                              parent=p, feasible=feasible)
    return param


def _load_artifact_spec(p, artifact_spec, kind):
    assert kind in ("inputs", "outputs")
    metadata = ArtifactMetadata.from_dict(artifact_spec.get("metadata", None))
    name = artifact_spec.get("name", None)
    from_ = artifact_spec.get("from", None)
    value = artifact_spec.get("value", None)
    desc = artifact_spec.get("desc", None)
    required = artifact_spec.get("required", False)

    af = PipelineArtifact(name=name, metadata=metadata, kind=kind, parent=p, from_=from_,
                          default=value, desc=desc, required=required)
    return af
