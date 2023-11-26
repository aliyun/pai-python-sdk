#  Copyright 2023 Alibaba, Inc. or its affiliates.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import copy
from abc import ABCMeta, abstractmethod
from collections import Counter

import six

from .artifact import LocationArtifactMetadata, PipelineArtifact
from .parameter import PipelineParameter

IO_TYPE_INPUTS = "inputs"
IO_TYPE_OUTPUTS = "outputs"


def sort_variable_by_category(items):
    """Sort variables by category."""
    if not items:
        return [], [], []
    counter = Counter((item.name for item in items))
    conflicts = {key for key, count in counter.items() if count > 1}
    if conflicts:
        raise ValueError("Parameter/Artifact names conflict:%s" % (",".join(conflicts)))

    arts = [item for item in items if item.variable_category == "artifacts"]
    params = [item for item in items if item.variable_category == "parameters"]
    return params, arts, params + arts


class IndexedItemMixin(six.with_metaclass(ABCMeta, object)):
    def __init__(self, items):
        self._items = items
        self._indexer = {self.index_key(item): idx for idx, item in enumerate(items)}

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

    @abstractmethod
    def index_key(self, item):
        pass


class IOSpecBase(IndexedItemMixin):
    """Inputs/Outputs spec base."""

    def __init__(self, items):
        parameter_items, artifact_items, items = sort_variable_by_category(items)
        self._parameters = Parameters(parameter_items)
        self._artifacts = Artifacts(artifact_items)
        super(IOSpecBase, self).__init__(items)

    @staticmethod
    def sort_items(items):
        # ensure parameters is prior to artifacts
        # `sorted` in Python is stable sort.
        return sorted(items, key=lambda x: 0 if isinstance(x, PipelineParameter) else 1)

    @property
    def items(self):
        return self._items

    @property
    def artifacts(self):
        return self._artifacts

    @property
    def parameters(self):
        return self._parameters

    def __repr__(self):
        return "%s:\n%s" % (
            type(self).__name__,
            "\n".join(["\t" + str(item) for item in self._items]),
        )

    def to_dict(self):
        af_pos = next(
            (
                idx
                for idx, item in enumerate(self._items)
                if item.variable_category == "artifacts"
            ),
            len(self._items),
        )

        d = {
            "parameters": [param.to_dict() for param in self._items[:af_pos]],
            "artifacts": [af.to_dict() for af in self._items[af_pos:]],
        }
        return d

    def index_key(self, item):
        return item.name


class InputsSpec(IOSpecBase):
    """Inputs spec for"""

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
                "Unexpected input_args type:%s, required list or dict"
                % type(inputs_args)
            )
        return assign_items


class OutputsSpec(IOSpecBase):
    def __init__(self, outputs):
        super(OutputsSpec, self).__init__(items=outputs)
        for item in self.items:
            item.kind = IO_TYPE_OUTPUTS


class Parameters(IndexedItemMixin):
    def index_key(self, item):
        return item.name


class Artifacts(IndexedItemMixin):
    def index_key(self, item):
        return item.name


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


def _load_parameter_spec(p, param_spec, io_type):
    typ = param_spec.pop("type", None)
    name = param_spec.pop("name")
    from_ = param_spec.pop("from", None)
    feasible = param_spec.pop("feasible", None)
    value = param_spec.pop("value", None)
    desc = param_spec.pop("desc", None)

    param = PipelineParameter(
        name=name,
        typ=typ,
        default=value,
        desc=desc,
        io_type=io_type,
        from_=from_,
        parent=p,
        feasible=feasible,
    )
    return param


def _load_artifact_spec(p, artifact_spec, io_type):
    assert io_type in ("inputs", "outputs")
    metadata = LocationArtifactMetadata.from_dict(artifact_spec.get("metadata", None))

    name = artifact_spec.get("name", None)
    from_ = artifact_spec.get("from", None)
    value = artifact_spec.get("value", None)
    desc = artifact_spec.get("desc", None)
    required = artifact_spec.get("required", False)
    repeated = artifact_spec.get("repeated", False)

    af = PipelineArtifact(
        name=name,
        metadata=metadata,
        io_type=io_type,
        parent=p,
        from_=from_,
        value=value,
        desc=desc,
        required=required,
        repeated=repeated,
    )
    return af
