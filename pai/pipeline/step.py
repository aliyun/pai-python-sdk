import copy

import six

from .types.spec import load_input_output_spec
from .types.variable import PipelineVariable


class PipelineStep(object):
    """ Represents an execution step in PAI pipeline.

    Pipeline steps can be configured together to construct a Pipeline, which is present as workflow
    in PAI ML pipeline service.

    """

    def __init__(self, identifier, provider=None, version="v1", inputs=None, name=None,
                 depends=None):
        self._depends = depends or set()
        self._assigned = set()
        template = self.get_template(identifier=identifier, provider=provider, version=version)
        self._metadata = copy.copy(template.manifest["metadata"])
        self._name = name

        inputs_spec, outputs_spec, = load_input_output_spec(self, template.manifest["spec"])
        self.parent = None
        self.inputs = inputs_spec
        self.outputs = outputs_spec

        self.assign_inputs(inputs)

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
        steps = set(
            [ipt.parent for ipt in inputs if isinstance(ipt, PipelineVariable) and ipt.parent])
        self._depends = steps.union(self._depends)

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
    def get_template(cls, identifier, provider, version):
        from .template import PipelineTemplate
        template = PipelineTemplate.get_by_identifier(identifier=identifier, provider=provider,
                                                      version=version)
        return template

    def after(self, *steps):
        if self.parent or any(step for step in steps if step.parent):
            raise ValueError("Not allow operation, pipeline step has been included in a pipeline")
        for step in steps:
            if step not in self._depends:
                self._depends.add(step)

    @property
    def ref_name(self):
        return "pipelines.{}".format(self.name)

    def _convert_spec_to_json(self):
        assigned_inputs = [ipt for ipt in self.inputs if ipt.name in self._assigned]

        spec = {
            "arguments": {
                "parameters": [ipt.to_dict() for ipt in assigned_inputs if
                               ipt.variable_category == "parameters"],
                "artifacts": [ipt.to_dict() for ipt in assigned_inputs if
                              ipt.variable_category == "artifacts"],
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
