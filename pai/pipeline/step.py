import copy
import uuid
from collections import OrderedDict

import six
import yaml

from .types.spec import load_input_output_spec
from .store import PAIFlowPipelineStore
from .types.variable import PipelineVariable


class PipelineStep(object):
    """ Represents an execution step in PAI pipeline.

    Pipeline steps can be configured together to construct a Pipeline, which is present as workflow
    in PAI ML pipeline service.

    """

    def __init__(self, identifier, provider=None, version="v1", inputs=None, name=None,
                 depends=None):
        self._depends = depends or set()
        manifest = self.get_manifest(identifier=identifier, provider=provider, version=version)
        self._metadata = copy.copy(manifest["metadata"])
        self._metadata["name"] = name

        inputs_spec, outputs_spec, = load_input_output_spec(self, manifest["spec"])
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
        self.inputs.assign(inputs)
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
        return self._metadata.get("name")

    @name.setter
    def name(self, value):
        self._metadata["name"] = value

    @classmethod
    def get_manifest(cls, identifier, provider, version):
        manifest_store = PAIFlowPipelineStore()
        return manifest_store.get(identifier=identifier, provider=provider, version=version)

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
        spec = {
            "arguments": self.inputs.to_dict(),
        }

        if self._depends:
            spec["dependencies"] = [step.name for step in self.depends]
        return spec

    def to_dict(self):
        d = {
            "metadata": self.metadata,
            "spec": self._convert_spec_to_json(),
        }
        return d
