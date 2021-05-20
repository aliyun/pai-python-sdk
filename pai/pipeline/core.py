from __future__ import absolute_import

import logging
from collections import defaultdict, Counter

from graphviz import Digraph

from .base import OperatorBase
from ..core.session import get_default_session
from .types.artifact import PipelineArtifact, PipelineArtifactElement
from .types.parameter import PipelineParameter
from .types.spec import OutputsSpec, InputsSpec


logger = logging.getLogger(__name__)


class Pipeline(OperatorBase):
    """Represents pipeline instance in PAI Machine Learning pipeline.

    Pipeline can be constructed from multiple pipeline steps, or single container implementation.
    It is shareable and reusable workflow, present as YAML format in backend pipeline service.

    """

    def __init__(self, steps=None, inputs=None, outputs=None, **kwargs):
        """Pipeline initializer."""

        self._steps, inputs, outputs = self._build_pipeline(steps, inputs, outputs)

        self._session = get_default_session()
        super(Pipeline, self).__init__(inputs=inputs, outputs=outputs, **kwargs)

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
        steps, inputs, _ = self._infer_pipeline_graph(steps, inputs, outputs)
        inputs_spec = InputsSpec(inputs) if isinstance(inputs, list) else inputs
        outputs_spec = OutputsSpec(self._build_outputs(outputs))

        self._update_steps(steps)

        return steps, inputs_spec, outputs_spec

    @classmethod
    def _infer_pipeline_inputs(cls, input):
        pipeline_inputs = set()
        if isinstance(input, PipelineArtifact):
            sources = []
            if input.repeated and input.value:
                sources = [item for item in input.value]
            elif not input.repeated and input.from_:
                sources = [input.from_]

            for item in sources:
                if isinstance(item, PipelineArtifact) and not item.parent:
                    pipeline_inputs.add(item)
                elif (
                    isinstance(item, PipelineArtifactElement)
                    and not item.artifact.parent
                ):
                    pipeline_inputs.add(item.artifact)
        elif input.from_ and not input.from_.parent:
            pipeline_inputs.add(input.from_)
        return pipeline_inputs

    @classmethod
    def _set_step_artifact_count(cls, steps):
        for step in steps:
            for input in step.inputs.artifacts:
                sources = []
                if input.repeated and input.value:
                    sources = input.value
                elif not input.repeated and input.from_:
                    sources = [input.from_]
                artifact_elements = [
                    i
                    for i in sources
                    if isinstance(i, PipelineArtifactElement) and i.artifact.parent
                ]

                for elem in artifact_elements:
                    if elem.artifact.count is None or elem.index >= elem.artifact.count:
                        elem.artifact.count = elem.index + 1

    @classmethod
    def _infer_pipeline_graph(cls, steps, inputs, outputs):
        inputs = inputs or []

        outputs = outputs or []
        if isinstance(outputs, dict):
            outputs = list(outputs.values())

        steps = steps or []
        visited_steps = set(
            steps + [output.parent for output in outputs if output.parent]
        )
        cur_steps = visited_steps.copy()
        while cur_steps:
            next_steps = set()
            for step in cur_steps:
                for output in step.outputs.artifacts:
                    if output.repeated:
                        output.reset_count()
                for depend in step.depends:
                    if depend not in visited_steps:
                        next_steps.add(depend)
                        visited_steps.add(depend)
            cur_steps = next_steps

        # infer the pipeline inputs from step inputs.
        infer_inputs = set()
        for step in visited_steps:
            for ipt in step.inputs:
                infer_inputs |= cls._infer_pipeline_inputs(ipt)

        cls._set_step_artifact_count(visited_steps)

        if inputs:
            if len(infer_inputs) != len(inputs):
                raise ValueError(
                    "Please provide complete pipeline inputs list: expected=%s, given=%s"
                    % (len(infer_inputs), len(inputs))
                )

            unexpected = [ipt.name for ipt in inputs if ipt not in infer_inputs]
            if unexpected:
                raise ValueError(
                    "Do not provide inputs which is not used in pipeline: %s" % unexpected
                )
        else:
            inputs = sorted(
                list(infer_inputs),
                key=lambda x: 0 if x.variable_category == "parameters" else 1,
            )
        sorted_steps = cls._topo_sort(visited_steps)
        cls._check_steps(steps)
        cls._check_inputs_outputs_name_conflict(inputs, outputs)

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
                results.append(
                    PipelineArtifact(
                        repeated=item.repeated,
                        name=name,
                        from_=item,
                        metadata=item.metadata,
                    )
                )
            elif isinstance(item, PipelineArtifactElement):
                results.append(
                    PipelineArtifact(
                        name=name,
                        from_=item,
                        metadata=item.artifact.metadata,
                    )
                )
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
            raise ValueError(
                "Given pipeline step name conflict:%s" % ",".join(conflicts)
            )

    @classmethod
    def _check_inputs_outputs_name_conflict(cls, inputs, outputs):
        names = [v.name for v in inputs + outputs]
        conflicts = [name for name, c in Counter(names).items() if c > 1]
        if conflicts:
            raise ValueError(
                "Given input/output variable name conflict:%s" % ",".join(conflicts)
            )

    def _update_steps(self, steps):
        """
        Set the name of step and bind the step to the pipeline.

        Args:
            steps: List of steps in pipeline.
        """
        used_names = set([s.name for s in steps])
        used_names = set(used_names)
        for step in steps:
            step.parent = self
            if not step.name:
                step.name = self._gen_step_name(
                    step, used_names=used_names, search_limit=len(steps)
                )
                used_names.add(step.name)

    @classmethod
    def _gen_step_name(cls, step, used_names, search_limit=100):
        for i in range(search_limit):
            candidate = "%s-%s" % (step.identifier, i)
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
