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

import itertools
import uuid
from abc import ABCMeta, abstractmethod

import six

from ...common.logging import get_logger
from ...common.utils import random_str
from ...common.yaml_utils import dump as yaml_dump
from ...common.yaml_utils import dump_all as yaml_dump_all
from ...session import get_default_session
from ..types import IO_TYPE_INPUTS, IO_TYPE_OUTPUTS, InputsSpec, OutputsSpec

logger = get_logger(__name__)


DEFAULT_PIPELINE_API_VERSION = "core/v1"


class ComponentBase(six.with_metaclass(ABCMeta, object)):
    def __init__(
        self,
        inputs,
        outputs,
    ):
        self._inputs = (
            inputs if isinstance(inputs, InputsSpec) else InputsSpec(inputs or [])
        )
        for input in self._inputs:
            input.bind(self, IO_TYPE_INPUTS)
        self._outputs = (
            outputs if isinstance(outputs, OutputsSpec) else OutputsSpec(outputs or [])
        )
        for output in self._outputs:
            output.bind(self, IO_TYPE_OUTPUTS)

    @property
    def inputs(self):
        """Inputs Spec of the operator.

        Returns:
            pai.pipeline.types.spec.InputsSpec: Inputs of the operator.

        """
        return self._inputs

    @property
    def outputs(self):
        """Outputs Spec of the operator.

        Returns:
            pai.pipeline.types.spec.OutputsSpec: Outputs of the operator

        """
        return self._outputs

    def translate_arguments(self, args):
        parameters, artifacts = [], []
        if not args:
            return parameters, artifacts

        requires = set([af.name for af in self.inputs.artifacts if af.required])
        not_supply = requires - set(args.keys())
        if len(not_supply) > 0:
            raise ValueError(
                "Required arguments is not supplied:%s" % ",".join(not_supply)
            )

        name_var_mapping = {
            item.name: item for item in itertools.chain(self.inputs, self.outputs)
        }

        for name, arg in args.items():
            if name not in name_var_mapping:
                logger.error(
                    "Provider useless argument:%s, it is not require by the pipeline manifest spec."
                    % name
                )
                raise ValueError("provided argument is not required:%s" % name)

            variable = name_var_mapping[name]
            value = variable.translate_argument(arg)

            if variable.variable_category == "artifacts":
                artifacts.append(value)
            else:
                parameters.append(value)

        repeated_artifacts = [
            af
            for af in itertools.chain(self.inputs.artifacts, self.outputs.artifacts)
            if af.repeated and af.count
        ]
        for af in repeated_artifacts:
            if af.name not in args:
                artifacts.append({"name": af.name, "value": [None] * af.count})

        return parameters, artifacts

    def set_artifact_count(self, artifact_name, count):
        """Set the count of repeated artifact in operator run.

        Args:
            artifact_name: output repeated artifact name.
            count:
        """
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

    def spec_to_dict(self):
        spec = {"inputs": self.inputs.to_dict(), "outputs": self.outputs.to_dict()}
        return spec

    def to_dict(self):
        data = {
            "apiVersion": DEFAULT_PIPELINE_API_VERSION,
            "metadata": self.metadata_to_dict(),
            "spec": self.spec_to_dict(),
        }
        return data

    def run(
        self, job_name=None, wait=True, arguments=None, show_outputs=True, **kwargs
    ):
        """Run the operator using the definition in SavedOperator and given arguments.

        Args:
            job_name (str): Name of the submit pipeline run job.
            arguments (dict): Inputs arguments used in the run workflow.
            wait (bool): Wait util the job stop(succeed or failed or terminated).
            show_outputs (bool): Show the outputs of the job.

        Returns:
            pai.pipeline.run.PipelineRun: PipelineRun instance of the submit job.

        """
        from pai.pipeline import PipelineRun

        parameters, artifacts = self.translate_arguments(arguments)
        pipeline_args = {
            "parameters": parameters,
            "artifacts": artifacts,
        }

        run_id = self._submit(job_name=job_name, args=pipeline_args)

        run_instance = PipelineRun.get(run_id=run_id)
        if not wait:
            return run_instance
        run_instance.wait_for_completion(show_outputs=show_outputs)
        return run_instance

    def as_step(self, name=None, inputs=None, depends=None):
        """Create a PipelineStep instance using the operator."""
        from pai.pipeline import PipelineStep

        return PipelineStep(
            inputs=inputs,
            component=self,
            name=name,
            depends=depends,
        )

    def as_loop_step(self, name, items, parallelism=None, inputs=None, depends=None):
        """Create a LoopStep instance using the operator."""
        from pai.pipeline.step import LoopStep

        return LoopStep(
            component=self,
            name=name,
            parallelism=parallelism,
            items=items,
            inputs=inputs,
            depends=depends,
        )

    def as_condition_step(self, name, condition, inputs=None, depends=None):
        """Create a conditional step using the operator."""
        from pai.pipeline.step import ConditionStep

        return ConditionStep(
            component=self,
            name=name,
            condition=condition,
            inputs=inputs,
            depends=depends,
        )


class UnRegisteredComponent(six.with_metaclass(ABCMeta, ComponentBase)):
    def __init__(self, inputs, outputs):
        super(UnRegisteredComponent, self).__init__(inputs=inputs, outputs=outputs)
        self._guid = uuid.uuid4().hex
        self._name = "tmp-{}".format(random_str(16))

    @property
    def guid(self):
        return self._guid

    def metadata_to_dict(self):
        # Hack: PAIFlow Service require field name in metadata dict
        return {
            "name": self._name,
            "guid": self._guid,
        }

    @property
    def name(self):
        return self._name

    def save(self, identifier, version):
        """Save the Pipeline in PAI service for reuse or share it with others.

        By specific the identifier, version and upload the manifest, the PipelineTemplate instance
        is store into the remote service and return the pipeline_id of the saved PipelineTemplate.
        Account UID in Alibaba Cloud is use as the provider of the saved operator by default.
        Saved PipelineTemplate could be fetch using the pipeline_id or the specific
        identifier-provider-version.

        Args:
            identifier (str): The identifier of the saved pipeline.
            version (str): Version of the saved pipeline.

        Returns:
            pai.pipeline.SavedTemplate: Saved PipelineTemplate instance
            (with pipeline_id generate by remote service).

        """
        from pai.pipeline.component import RegisteredComponent

        if not identifier or not version:
            raise ValueError(
                "Please provide the identifier and version for the operator."
            )

        manifest = self.to_manifest(identifier=identifier, version=version)

        session = get_default_session()
        pipeline_id = session.pipeline_api.create(manifest)
        return RegisteredComponent.get(pipeline_id)

    @classmethod
    def _patch_metadata(cls, pipeline_spec):
        if isinstance(pipeline_spec, dict):
            pipeline_spec["metadata"]["identifier"] = "tmp-%s" % random_str(16)
            pipeline_spec["metadata"]["version"] = "v0"
        elif isinstance(pipeline_spec, list):
            pipeline_spec[-1]["metadata"]["identifier"] = "tmp-%s" % random_str(16)
            pipeline_spec[-1]["metadata"]["version"] = "v0"
        return pipeline_spec

    def _submit(self, job_name, args):
        from pai.pipeline.run import PipelineRun

        session = get_default_session()
        pipeline_spec = self._patch_metadata(self.to_dict())
        if isinstance(pipeline_spec, dict):
            manifest = yaml_dump(pipeline_spec)
        # A Pipeline spec may contain unregistered operators. Such a pipeline spec is a list format.
        elif isinstance(pipeline_spec, list):
            manifest = yaml_dump_all(pipeline_spec)
        else:
            raise ValueError(
                "No support pipeline spec value type: %s" % (type(pipeline_spec))
            )

        run_id = PipelineRun.run(
            job_name,
            args,
            no_confirm_required=True,
            manifest=manifest,
            session=session,
        )
        return run_id

    def io_spec_to_dict(self):
        return {
            "inputs": self.inputs.to_dict(),
            "outputs": self.outputs.to_dict(),
        }

    @abstractmethod
    def to_manifest(self, identifier, version):
        pass

    def export_manifest(self, file_path, identifier, version):
        manifest = self.to_manifest(identifier=identifier, version=version)
        with open(file_path, "w") as f:
            f.write(manifest)
