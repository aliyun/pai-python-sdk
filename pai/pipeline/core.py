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

from __future__ import absolute_import

from collections import Counter, defaultdict

from ..common.logging import get_logger
from ..common.yaml_utils import dump as yaml_dump
from ..common.yaml_utils import dump_all as yaml_dump_all
from ..session import get_default_session
from .component._base import UnRegisteredComponent
from .types import InputsSpec, OutputsSpec, PipelineParameter, PipelineVariable
from .types.artifact import PipelineArtifact, PipelineArtifactElement

logger = get_logger(__name__)


class Pipeline(UnRegisteredComponent):
    """Represents pipeline instance in PAI Machine Learning pipeliner service.

    Pipeline can be constructed from multiple pipeline steps, or single container implementation.
    It is shareable and reusable workflow, present as YAML format in backend pipeline service.

    """

    def __init__(self, steps, inputs=None, outputs=None, **kwargs):
        """Pipeline initializer."""
        from pai.pipeline import PipelineStep

        # check parameter steps.
        if not steps:
            raise ValueError("Required at least one step in the pipeline")
        if not isinstance(steps, list) or any(
            x for x in steps if not isinstance(x, PipelineStep)
        ):
            raise ValueError(
                "Parameter steps must be a list of PipelineStep instances."
            )

        steps, inputs, outputs, unregistered_ops = self._build_pipeline(
            steps, inputs, outputs
        )

        self._steps = steps
        self._unregistered_components = unregistered_ops
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

        self._check_inputs_outputs_name_conflict(
            inputs_spec=inputs_spec, outputs_spec=outputs_spec
        )
        unregistered_ops = self._get_unregistered_components(steps)

        self._update_steps(steps)

        return (
            steps,
            inputs_spec,
            outputs_spec,
            unregistered_ops,
        )

    @classmethod
    def _get_unregistered_components(cls, steps):
        """Get the unregistered components used by the step in the pipeline.

        Args:
            steps: Steps in the pipeline.

        Returns:
            List[OperatorBase]: Return unregistered components using in the pipeline.
        """

        unregistered_ops = [
            step.component for step in steps if not step.is_component_registered
        ]
        seen = set()
        return [
            op
            for op in unregistered_ops
            if op.guid not in seen and not seen.add(op.guid)
        ]

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
        elif (
            input.from_
            and isinstance(input.from_, PipelineVariable)
            and not input.from_.parent
        ):
            pipeline_inputs.add(input.from_)
        return pipeline_inputs

    @classmethod
    def _set_step_artifact_count(cls, steps):
        """The expanded count of the repeated artifact should be fixed while using in the pipeline.

        Args:
            steps: All the steps used in the pipeline.
        """
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
        """Inference the DAG graph of pipeline by pipelines inputs, steps and outputs. The
         function walks through the pipeline graph bottom-up from outputs and steps,
          finding out all the required steps and inputs of the pipeline.

        Args:
            steps: steps used in the pipeline graph.
            inputs: inputs used in the pipeline.
            outputs: outputs definition of the pipeline.

        Returns:
            Tuple: Returns all the required steps, inputs and outputs.

        """
        inputs = inputs or []

        outputs = outputs or []
        if isinstance(outputs, dict):
            outputs = list(outputs.values())

        # find out all steps in the pipeline by topological sort.
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
                    "Do not provide inputs which is not used in pipeline: %s"
                    % unexpected
                )
        else:
            inputs = sorted(
                list(infer_inputs),
                key=lambda x: 0 if x.variable_category == "parameters" else 1,
            )
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
            raise ValueError("Require list or dict, unexpected type:%s" % type(outputs))

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
            raise ValueError("Pipeline step has been used")

        step_names = [step.name for step in steps if step.name]
        conflicts = [k for k, v in Counter(step_names).items() if v > 1]
        if conflicts:
            raise ValueError(
                "Given pipeline step name conflict:%s" % ",".join(conflicts)
            )

    @classmethod
    def _check_inputs_outputs_name_conflict(cls, inputs_spec, outputs_spec):
        names = [v.name for v in inputs_spec.items + outputs_spec.items]
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
            candidate = "%s-%s" % (step.gen_name_prefix(), i)
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
        try:
            from graphviz import Digraph
        except ImportError:
            raise ImportError(
                "Unable to display pipeline, install graphviz first: "
                "pip install graphviz"
            )

        graph = Digraph()
        for step in self.steps:
            graph.node(step.name)
            for head in step.depends:
                graph.edge(head.name, step.name)
        return graph

    def to_dict(self, identifier=None, version=None):
        entrypoint = super(Pipeline, self).to_dict()

        if identifier is not None:
            entrypoint["metadata"]["identifier"] = identifier
        if version is not None:
            entrypoint["metadata"]["version"] = version
        if get_default_session():
            entrypoint["metadata"]["provider"] = get_default_session().provider

        entrypoint["spec"]["pipelines"] = [step.to_dict() for step in self.steps]
        if not self._unregistered_components:
            return entrypoint

        res = [op.to_dict() for op in self._unregistered_components]
        res.append(entrypoint)

        return res

    def to_manifest(self, identifier, version):
        d = self.to_dict(identifier, version)
        if isinstance(d, list):
            return yaml_dump_all(d)
        return yaml_dump(d)
