from __future__ import absolute_import

import logging
from abc import ABCMeta
from collections import defaultdict, Counter

import six
from graphviz import Digraph

from ..core.session import get_default_session
from .types.artifact import PipelineArtifact
from .types.parameter import PipelineParameter
from .types.spec import OutputsSpec, InputsSpec

DEFAULT_PIPELINE_API_VERSION = "core/v1"

logger = logging.getLogger(__name__)


class PipelineBase(six.with_metaclass(ABCMeta, object)):

    def __init__(self, inputs, outputs, identifier=None, provider=None, version=None,
                 pipeline_id=None):
        self._identifier = identifier
        self._provider = provider
        self._version = version
        self._pipeline_id = pipeline_id
        self._inputs = inputs if isinstance(inputs, InputsSpec) else InputsSpec(inputs)
        self._outputs = outputs if isinstance(outputs, OutputsSpec) else OutputsSpec(outputs)

    def __repr__(self):
        return '%s:{PipelineId:%s, Identifier:%s, Provider:%s, Version:%s}' % (
            type(self).__name__, self._pipeline_id, self.identifier, self.provider, self.version)

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self._outputs

    @property
    def metadata(self):
        return {
            "identifier": self._identifier,
            "provider": self._provider,
            "version": self._version,
        }

    @property
    def identifier(self):
        return self._identifier

    @property
    def provider(self):
        return self._provider

    @property
    def version(self):
        return self._version

    @property
    def _template(self):
        from .template import PipelineTemplate
        manifest = self.to_dict()
        return PipelineTemplate(manifest=manifest, pipeline_id=self.pipeline_id)

    @property
    def pipeline_id(self):
        return self._pipeline_id

    @property
    def is_saved(self):
        return bool(self.pipeline_id)

    def save(self, identifier=None, version=None):
        templ = self._template.save(identifier=identifier, version=version)
        self._identifier = templ.identifier
        self._version = templ.version
        self._provider = templ.provider
        self._pipeline_id = templ.pipeline_id
        return self

    def to_estimator(self, parameters):
        from pai.core.estimator import PipelineEstimator
        return PipelineEstimator(pipeline_id=self._template.pipeline_id,
                                 manifest=self._template.manifest,
                                 parameters=parameters)

    def to_transformer(self, parameters=None):
        from pai.core.transformer import PipelineTransformer
        return PipelineTransformer(pipeline_id=self._template.pipeline_id,
                                   manifest=self._template.manifest,
                                   parameters=parameters)

    def run(self, job_name, arguments=None, **kwargs):
        return self._template.run(job_name=job_name, arguments=arguments,
                                  **kwargs)

    def _spec_to_dict(self):
        spec = {"inputs": self.inputs.to_dict(), "outputs": self.outputs.to_dict()}
        return spec

    def to_dict(self):
        manifest = {
            "apiVersion": DEFAULT_PIPELINE_API_VERSION,
            "metadata": self.metadata,
            "spec": self._spec_to_dict()
        }
        return manifest


class ContainerComponent(PipelineBase):

    def __init__(self, image_uri, inputs, outputs, command, image_registry_config=None,
                 identifier=None, provider=None, version=None, pipeline_id=None):
        self.image_uri = image_uri
        self.image_registry_config = image_registry_config
        self.command = command or []
        super(ContainerComponent, self).__init__(inputs=inputs, outputs=outputs, provider=provider,
                                                 version=version, identifier=identifier,
                                                 pipeline_id=pipeline_id)

    def to_dict(self):
        d = super(ContainerComponent, self).to_dict()
        d["spec"]["execution"] = {
            "image": self.image_uri,
            "command": self.command,
        }

        if self.image_registry_config:
            d["spec"]["execution"]["imageRegistryConfig"] = self.image_registry_config

        return d


class Pipeline(PipelineBase):
    """Represents pipeline instance in PAI Machine Learning pipeline.

    Pipeline can be constructed from multiple pipeline steps, or single container implementation.
    It is shareable and reusable workflow, present as YAML format in backend pipeline service.

    """

    def __init__(self, steps=None, inputs=None, outputs=None, identifier=None, version=None,
                 provider=None):
        """Pipeline initializer.

        """

        self._steps, inputs, outputs = self._build_pipeline(steps, inputs, outputs)

        self._session = get_default_session()
        super(Pipeline, self).__init__(inputs=inputs,
                                       outputs=outputs,
                                       identifier=identifier,
                                       provider=provider,
                                       version=version)

    @property
    def steps(self):
        return self._steps

    def _build_pipeline(self, steps, inputs, outputs):
        """

        Args:
            steps:
            outputs:
            inputs:

        Returns:

        """
        steps, inputs, _ = self._infer_pipeline(steps, inputs, outputs)
        inputs_spec = InputsSpec(inputs) if isinstance(inputs, list) else inputs
        outputs_spec = OutputsSpec(self._build_outputs(outputs))

        self._update_steps(steps)

        return steps, inputs_spec, outputs_spec

    @classmethod
    def _infer_pipeline(cls, steps, inputs, outputs):
        inputs = inputs or []

        outputs = outputs or []
        if isinstance(outputs, dict):
            outputs = outputs.values()

        steps = steps or []
        visited_steps = set(steps + [output.parent for output in outputs if output.parent])
        infer_inputs = set()
        cur_steps = visited_steps.copy()
        while cur_steps:
            next_steps = set()
            for step in cur_steps:
                for ipt in step.inputs:
                    if ipt.from_ and not ipt.from_.parent:
                        infer_inputs.add(ipt.from_)
                for depend in step.depends:
                    if depend not in visited_steps:
                        next_steps.add(depend)
                        visited_steps.add(depend)
            cur_steps = next_steps

        if inputs:
            if len(infer_inputs) != len(inputs) or any(
                    ipt for ipt in inputs if ipt not in infer_inputs):
                raise ValueError("Require complete pipeline inputs list")
        else:
            inputs = sorted(list(infer_inputs),
                            key=lambda x: 0 if x.variable_category == "parameters" else 1)
        sorted_steps = cls._topo_sort(visited_steps)
        cls._check_steps(steps)

        return sorted_steps, inputs, outputs

    @classmethod
    def _build_outputs(cls, outputs):
        outputs = outputs or []
        if isinstance(outputs, dict):
            items = outputs.items()
        elif isinstance(outputs, (list, OutputsSpec)):
            items = [(item.name, item) for item in outputs]
        else:
            raise ValueError("Require list or dict, unexpect type:%s" % type(outputs))

        results = []
        for name, item in items:
            if isinstance(item, PipelineArtifact):
                results.append(PipelineArtifact(
                    name=name,
                    from_=item,
                    metadata=item.metadata,
                ))
            elif isinstance(item, PipelineParameter):
                results.append(PipelineParameter(name=name, typ=item.typ, from_=item))
            else:
                raise ValueError("Unexpected output type: %s", type(item))
        return results

    @classmethod
    def _topo_sort(cls, steps):
        rev_depends = defaultdict(set)
        for step in steps:
            for depend_step in step.depends:
                rev_depends[depend_step].add(step)
        # entry steps
        visited_steps = [step for step in steps if not step.depends]

        cur_steps = visited_steps
        while cur_steps:
            next_steps = []
            for step in cur_steps:
                for candidate_step in rev_depends[step]:
                    if candidate_step in next_steps or candidate_step in visited_steps:
                        continue
                    if all(s in visited_steps for s in candidate_step.depends):
                        next_steps.append(candidate_step)
            visited_steps.extend(next_steps)
            cur_steps = next_steps

        if len(visited_steps) != len(steps):
            raise ValueError("Cycle dependency detected, please check the input steps")

        return visited_steps

    @classmethod
    def _check_steps(cls, steps):
        """
        1. check if cycle dependency exists in pipeline DAG.
        2. check if step name conflict.
        3. naming the unnamed step.

        Args:
            steps:
        """

        if any(step.parent for step in steps):
            raise ValueError("Pipeline step has been")

        step_names = [step.name for step in steps if step.name]
        conflicts = [k for k, v in Counter(step_names).items() if v > 1]
        if conflicts:
            raise ValueError("Given pipeline step name conflict:%s" % ','.join(conflicts))

    def _update_steps(self, steps):
        used_names = set([s.name for s in steps])
        used_names = set(used_names)
        for step in steps:
            step.parent = self
            if not step.name:
                step.name = self._make_step_name(step, used_names=used_names,
                                                 search_limit=len(steps))
                used_names.add(step.name)

    @classmethod
    def _make_step_name(cls, step, used_names, search_limit=100):
        for i in range(search_limit):
            candidate = '%s-%s' % (step.identifier, i)
            if candidate not in used_names:
                return candidate
        raise ValueError("No available name for the step")

    @property
    def ref_name(self):
        return ""

    def validate_step_name(self, name):
        if name in self.steps:
            raise ValueError("Pipeline step name conflict: %s" % name)
        return name

    @property
    def input_parameters_spec(self):
        return {ipt.name: ipt.to_dict() for ipt in self.inputs if
                ipt.variable_category == "parameters"}

    @property
    def input_artifacts_spec(self):
        return {ipt.name: ipt.to_dict() for ipt in self.inputs if
                ipt.variable_category == "artifacts"}

    def dot(self):
        graph = Digraph()
        for step in self.steps:
            graph.node(step.name)
            for head in step.depends:
                graph.edge(head.name, step.name)
        return graph

    def to_dict(self):
        d = super(Pipeline, self).to_dict()
        d["spec"]["pipelines"] = [step.to_dict() for step in self.steps]
        return d
