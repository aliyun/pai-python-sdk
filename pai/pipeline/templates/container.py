# coding: utf-8
from __future__ import print_function

import six
import tempfile

import docker
import json
import os
import shutil

from pai.pipeline.base import TemplateSpecBase
from pai.pipeline.types.artifact import PipelineArtifact
from pai.pipeline.types.spec import IO_TYPE_OUTPUTS

PAI_BASE_DIR_ENV_KEY = "PAI_BASE_DIR"
PAI_PROGRAM_ENTRY_POINT_ENV_KEY = "PAI_PROGRAM_ENTRY_POINT"
PAI_CREDENTIAL_ACCESS_KEY_ENV_KEY = "paiflow.aliyun.com-access-key"
PAI_CREDENTIAL_ACCESS_SECRET_ENV_KEY = "paiflow.aliyun.com-access-secret"

PAI_MANIFEST_SPEC_INPUTS_ENV_KEY = "paiflow.aliyun.com-manifest_spec_inputs"
PAI_MANIFEST_SPEC_OUTPUTS_ENV_KEY = "paiflow.aliyun.com-manifest_spec_outputs"
PAI_INPUTS_PARAMETERS_ENV_KEY = "paiflow.aliyun.com-inputs_parameters"

PAI_RAW_ARTIFACT_METADATA_ENV_KEY_FORMAT = (
    "paiflow.aliyun.com-{0}-artifacts-{1}-metadata"
)
PAI_RAW_ARTIFACT_VALUE_ENV_KEY_FORMAT = "paiflow.aliyun.com-{0}-artifacts-{1}-value"


class ContainerTemplate(TemplateSpecBase):

    default_identifier = "container_template"

    def __init__(
        self,
        image_uri,
        command,
        image_registry_config=None,
        inputs=None,
        outputs=None,
        env=None,
        identifier=None,
        version=None,
        provider=None,
    ):
        self.image_uri = image_uri
        self.image_registry_config = image_registry_config
        self.command = command
        self.env = env

        super(ContainerTemplate, self).__init__(
            inputs=inputs,
            outputs=outputs,
            identifier=identifier,
            version=version,
            provider=provider,
        )

    def to_dict(self):
        d = super(ContainerTemplate, self).to_dict()
        d["spec"]["execution"] = {
            "image": self.image_uri,
            "command": self.command,
        }

        if self.image_registry_config:
            d["spec"]["execution"]["imageRegistryConfig"] = self.image_registry_config

        if self.env:
            d["spec"]["execution"]["env"] = self.env
        return d

    def run(self, job_name, arguments=None, local_mode=False, **kwargs):
        if local_mode:
            self.local_run(job_name, arguments=arguments)
        else:
            return super(ContainerTemplate, self).run(
                job_name=job_name, arguments=arguments, **kwargs
            )

    def local_run(self, job_name, arguments=None):
        source_dir = self.source_dir if hasattr(self, "source_dir") else None
        entry_point = self.entry_point if hasattr(self, "entry_point") else None
        return LocalContainerRun(
            job_name=job_name,
            inputs=self.inputs,
            outputs=self.outputs,
            image_uri=self.image_uri,
            command=self.command,
            arguments=arguments,
            env=self.env.copy() if self.env else None,
            source_dir=source_dir,
            entry_point=entry_point,
        ).run()


class LocalContainerRun(object):
    BASE_WORKSPACE_DIR = "/work"

    def __init__(
        self,
        job_name,
        inputs,
        outputs,
        image_uri,
        command,
        arguments,
        env=None,
        container_base_dir=None,
        source_dir=None,
        entry_point=None,
    ):
        """

        Args:
            inputs (pai.pipeline.types.InputsSpec):
            outputs (pai.pipeline.types.OutputsSpec):
            command:
            arguments:
            env:
            source_dir:
            entry_point:
        """
        self.job_name = job_name
        self.inputs = inputs
        self.outputs = outputs
        self.image_uri = image_uri
        self.env = env or dict()
        self.command = command
        self.arguments = arguments
        self.container_base_dir = container_base_dir or type(self).BASE_WORKSPACE_DIR
        self.source_dir = source_dir
        self.entry_point = entry_point
        self.tmp_base_dir = None

    def prepare(self):
        self.tmp_base_dir = tempfile.mkdtemp()
        self._prepare_spec()
        self._prepare_parameters()
        self._prepare_artifacts()
        self._prepare_code()
        self.env["PYTHONUNBUFFERED"] = "1"

    def run(self):
        self.prepare()
        try:
            docker_client = docker.from_env()
            volumes = {
                self.tmp_base_dir: {
                    "bind": self.container_base_dir,
                    "mode": "rw",
                }
            }

            container = docker_client.containers.run(
                image=self.image_uri,
                command=self.command,
                environment=self.env,
                volumes=volumes,
                detach=True,
            )

            log_iterator = container.logs(stream=True)
            for log in log_iterator:
                print(log.decode("utf-8"), end="")
            return docker_client.containers.get(container_id=container.id)
        finally:
            shutil.rmtree(self.tmp_base_dir)
            self.tmp_base_dir = None

    def on_finish(self):
        pass

    def _prepare_spec(self):
        inputs_spec = self.inputs.to_dict()
        output_spec = self.outputs.to_dict()
        self.env.update(
            {
                PAI_MANIFEST_SPEC_INPUTS_ENV_KEY: json.dumps(inputs_spec),
                PAI_MANIFEST_SPEC_OUTPUTS_ENV_KEY: json.dumps(output_spec),
            }
        )

    def _prepare_code(self):
        source_dir = (
            self.source_dir
            if hasattr(self, "source_dir") and self.source_dir
            else os.path.dirname(self.entry_point)
        )

        target_dir = "{0}/code/".format(self.tmp_base_dir)
        shutil.copytree(source_dir, target_dir)
        self.env.update(
            {
                PAI_PROGRAM_ENTRY_POINT_ENV_KEY: self.entry_point,
            }
        )

    def _prepare_artifacts(self):
        artifact_path_format = "{0}/{1}/artifacts/{2}/data"

        def patch_path_for_metadata(af):
            container_artifact_path = artifact_path_format.format(
                self.container_base_dir, artifact.kind, af.name
            )
            artifact_metadata = af.metadata.to_dict()
            artifact_metadata["path"] = container_artifact_path
            return artifact_metadata

        for artifact in self.inputs.artifacts + self.outputs.artifacts:
            self.env.update(
                {
                    PAI_RAW_ARTIFACT_METADATA_ENV_KEY_FORMAT.format(
                        artifact.kind,
                        artifact.name,
                    ): json.dumps(patch_path_for_metadata(artifact))
                }
            )
            if artifact.name not in self.arguments or artifact.kind == IO_TYPE_OUTPUTS:
                continue
            artifact_arg = PipelineArtifact.to_argument_by_spec(
                self.arguments[artifact.name], artifact.to_dict()
            )
            artifact_raw_value = artifact_arg["value"]
            local_artifact_path = artifact_path_format.format(
                self.tmp_base_dir, "inputs", artifact.name
            )
            os.makedirs(os.path.dirname(local_artifact_path))
            with open(local_artifact_path, "w") as f:
                f.write(artifact_raw_value)

    def _prepare_parameters(self):
        parameters_spec = self.inputs.parameters
        names = [param_spec.name for param_spec in parameters_spec]

        def parameter_transform(arg):
            if isinstance(arg, (bool, int, float)):
                return str(arg)
            elif isinstance(arg, dict):
                return json.dumps(arg)
            else:
                return arg

        parameter_arguments = [
            {
                "name": name,
                "value": parameter_transform(arg),
            }
            for name, arg in self.arguments.items()
            if name in names
        ]
        self.env.update(
            {PAI_INPUTS_PARAMETERS_ENV_KEY: json.dumps(parameter_arguments)}
        )
