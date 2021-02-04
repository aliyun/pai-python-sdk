import copy
import itertools

import six

from .types.spec import load_input_output_spec
from .types.variable import PipelineVariable
from ..common.utils import is_iterable


class PipelineStep(object):
    """Represents an execution step in PAI pipeline.

    Pipeline steps can be configured together to construct a Pipeline, which is present as workflow
    in PAI ML pipeline service.

    """

    def __init__(
        self,
        identifier,
        provider=None,
        version="v1",
        inputs=None,
        name=None,
        depends=None,
    ):
        self._depends = depends or set()
        self._assigned = set()
        operator = self.get_operator(
            identifier=identifier, provider=provider, version=version
        )
        self._metadata = self._parse_raw_metadata(operator.manifest["metadata"])
        self._name = name

        (
            inputs_spec,
            outputs_spec,
        ) = load_input_output_spec(self, operator.manifest["spec"])
        self.parent = None
        self.inputs = inputs_spec
        self.outputs = outputs_spec

        self.assign_inputs(inputs)
        self._repeated_artifact_config = {}

    @classmethod
    def _parse_raw_metadata(cls, raw_metadata):
        metadata = {
            "identifier": raw_metadata["identifier"],
            "provider": raw_metadata["provider"],
            "uuid": raw_metadata["uuid"],
            "version": raw_metadata["version"],
        }
        return metadata

    @property
    def repeated_io_config(self):
        return self._repeated_artifact_config

    def set_artifact_count(self, artifact_name, count):
        artifacts = {
            item.name: item
            for item in itertools.chain(self.outputs.artifacts, self.inputs.artifacts)
        }
        artifact = artifacts.get(artifact_name)
        if not artifact:
            raise ValueError("artifact is not exists: %s" % artifact_name)

        if not artifact.repeated:
            raise ValueError("artifact is not repeated: %s", artifact_name)
        artifact.count = count
        return self

    # TODO: Confirm pipeline step name restriction
    @classmethod
    def _validate_name(cls, name):
        if name is None:
            return
        if not isinstance(name, six.string_types):
            raise ValueError("PipelineStep name should be string type")
        if not name:
            raise ValueError("PipelineStep name should not be empty str")
        if len(name) > 30:
            raise ValueError("Given invalid pipeline step name.")

    def assign_inputs(self, inputs):
        if not inputs:
            return
        assign_items = self.inputs.assign(inputs)
        self._assigned = self._assigned.union(set(item.name for item in assign_items))

        if isinstance(inputs, dict):
            inputs = inputs.values()

        values = []
        for ipt in inputs:
            if isinstance(ipt, (list, tuple)):
                values.extend(ipt)
            else:
                values.append(ipt)

        def _depend_step(input):
            from pai.pipeline.types.artifact import PipelineArtifactElement

            if isinstance(input, PipelineVariable) and input.parent:
                return input.parent
            elif isinstance(input, PipelineArtifactElement) and input.artifact.parent:
                return input.artifact.parent

        input_steps = set(filter(None, [_depend_step(val) for val in values]))

        self._depends = input_steps.union(self._depends)

    @property
    def metadata(self):
        return self._metadata

    @property
    def identifier(self):
        return self._metadata["identifier"]

    @property
    def provider(self):
        return self._metadata["provider"]

    @property
    def depends(self):
        return list(self._depends)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @classmethod
    def get_operator(cls, identifier, provider, version):
        from pai.operator import SavedOperator

        operator = SavedOperator.get_by_identifier(
            identifier=identifier, provider=provider, version=version
        )
        return operator

    def after(self, *steps):
        if self.parent or any(step for step in steps if step.parent):
            raise ValueError(
                "Not allow operation, pipeline step has been included in a pipeline"
            )
        for step in steps:
            if step not in self._depends:
                self._depends.add(step)

    @property
    def ref_name(self):
        return "pipelines.{}".format(self.name)

    def _convert_spec_to_json(self):
        assigned_inputs = [ipt for ipt in self.inputs if ipt.name in self._assigned]

        repeated_artifact_config = [
            {
                "name": opt.name,
                "value": [None] * opt.count,
            }
            for opt in self.outputs.artifacts
            if opt.repeated and opt.count
        ]

        spec = {
            "arguments": {
                "parameters": [
                    ipt.to_argument()
                    for ipt in assigned_inputs
                    if ipt.variable_category == "parameters"
                ],
                "artifacts": [
                    ipt.to_argument()
                    for ipt in assigned_inputs
                    if ipt.variable_category == "artifacts"
                ]
                + repeated_artifact_config,
            }
        }

        if self._depends:
            spec["dependencies"] = [step.name for step in self.depends]
        return spec

    def to_dict(self):
        metadata = copy.copy(self._metadata)
        metadata["name"] = self.name
        d = {
            "metadata": metadata,
            "spec": self._convert_spec_to_json(),
        }
        return d
