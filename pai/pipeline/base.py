from __future__ import absolute_import

import itertools
import uuid

import logging
import string

import random

import six
from abc import ABCMeta

from pai.core.session import get_default_session
from pai.pipeline.consts import DEFAULT_PIPELINE_API_VERSION
from pai.pipeline.run import PipelineRun
from pai.pipeline.types import (
    PipelineParameter,
    InputsSpec,
    OutputsSpec,
    PipelineArtifact,
    IO_TYPE_OUTPUTS,
    IO_TYPE_INPUTS,
)

logger = logging.getLogger(__name__)


_DEFAULT_VERSION = "v1"


class OperatorBase(six.with_metaclass(ABCMeta, object)):
    def __init__(
        self,
        inputs,
        outputs,
        identifier=None,
        version=None,
        provider=None,
    ):

        session = get_default_session()
        self._identifier = identifier or self._gen_identifier()
        self._version = version or _DEFAULT_VERSION
        self._provider = provider or session.provider
        self._initialize_io_spec(inputs, outputs)
        self._repeated_artifact_config = {}

    def _initialize_io_spec(self, inputs, outputs):
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

    def __repr__(self):
        return "%s:{Identifier:%s, Provider:%s, Version:%s}" % (
            type(self).__name__,
            self.identifier,
            self.provider,
            self.version,
        )

    @classmethod
    def _get_service_client(cls):
        return get_default_session().paiflow_client

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

    @classmethod
    def current_provider(cls):
        return get_default_session().provider

    @property
    def metadata(self):
        return {
            "identifier": self.identifier,
            "provider": self.provider,
            "version": self.version,
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
        from pai.operator import SavedOperator

        session = get_default_session()
        provider = session.provider

        identifier = identifier or self._identifier
        version = version or self._version

        if not identifier or not version:
            raise ValueError(
                "Please provide the identifier and version for the operator."
            )

        manifest = self.to_dict()

        manifest["metadata"]["provider"] = provider
        manifest["metadata"]["identifier"] = identifier
        manifest["metadata"]["version"] = version
        id = session.create_pipeline(manifest, workspace=session.workspace)

        return SavedOperator.get(id)

    @classmethod
    def _gen_job_name(cls, prefix="job_"):
        if prefix:
            return prefix + "".join(
                [random.choice(string.ascii_letters) for _ in range(8)]
            )
        return

    @classmethod
    def _gen_identifier(cls):
        return "tmp-" + "".join(
            [random.choice(string.ascii_letters) for _ in range(16)]
        )

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
            value = variable.to_argument(arg)

            if variable.variable_category == "artifacts":
                artifacts.append(value)
            else:
                parameters.append(value)

        for name, count in self._repeated_artifact_config:
            if name not in args:
                artifacts.append({"name": name, "value": [None for _ in range(count)]})

        return parameters, artifacts

    def _submit(self, job_name, args):
        session = get_default_session()
        manifest = self.to_dict()
        run_id = session.create_run(
            job_name,
            args,
            no_confirm_required=True,
            manifest=manifest,
            workspace=session.workspace,
        )
        return run_id

    def add_artifact_config(self, artifact_name, count):
        """
        Set the count of repeated artifact in operator run.

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
        self._repeated_artifact_config[artifact_name] = count
        return self

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
        session = get_default_session()
        parameters, artifacts = self.translate_arguments(arguments)
        pipeline_args = {
            "parameters": parameters,
            "artifacts": artifacts,
        }

        manifest = self.to_dict()
        manifest["metadata"]["identifier"] = "tmp-%s" % uuid.uuid4().hex
        manifest["metadata"]["version"] = "v0"

        run_id = self._submit(job_name=job_name, args=pipeline_args)
        run_instance = PipelineRun(
            run_id=run_id,
            name=job_name,
            workspace_id=session.workspace.id if session.workspace else None,
        )
        if not wait:
            return run_instance
        run_instance.wait_for_completion(show_outputs=show_outputs)
        return run_instance

    def spec_to_dict(self):
        spec = {"inputs": self.inputs.to_dict(), "outputs": self.outputs.to_dict()}
        return spec

    def to_dict(self):
        data = {
            "apiVersion": DEFAULT_PIPELINE_API_VERSION,
            "metadata": self.metadata,
            "spec": self.spec_to_dict(),
        }
        return data
