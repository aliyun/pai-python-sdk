# coding: utf-8
from __future__ import print_function

import json
import os
import tempfile

import logging
import shutil
import six
import uuid

from pai.common.utils import makedirs
from pai.core.session import get_default_session
from pai.operator._base import UnRegisteredOperator
from pai.operator.types import IO_TYPE_OUTPUTS
from pai.operator.types.variable import PipelineVariable

PAI_PROGRAM_ENTRY_POINT_ENV_KEY = "PAI_PROGRAM_ENTRY_POINT"
PAI_MANIFEST_SPEC_INPUTS_ENV_KEY = "PAI_MANIFEST_SPEC_INPUTS"
PAI_MANIFEST_SPEC_OUTPUTS_ENV_KEY = "PAI_MANIFEST_SPEC_OUTPUTS"
PAI_INPUTS_PARAMETERS_ENV_KEY = "PAI_INPUTS_PARAMETERS"

_logger = logging.getLogger(__name__)

_PIP_INSTALL_TEMPLATE = '''\
(PIP_DISABLE_PIP_VERSION_CHECK=1 python3 -m pip install --quiet {pkgs} \
|| PIP_DISABLE_PIP_VERSION_CHECK=1 python3 -m pip install --quiet \
 {pkgs} --user) && "$0" "$@"'''

_DOCKERFILE_TEMPLATE = """\
# Build an image that run in PAI.
FROM {base_image}

RUN mkdir -p /work/code/
COPY __source_dir/* /work/code/

WORKDIR /work/code
{install_packages_step}
{install_requirements_step}

"""


class ContainerOperator(UnRegisteredOperator):
    def __init__(
        self,
        image_uri,
        command,
        args=None,
        image_registry_config=None,
        inputs=None,
        outputs=None,
        env=None,
    ):
        self.image_uri = image_uri
        self.image_registry_config = image_registry_config
        self.command = command
        self.args = args
        self.env = env
        self._guid = uuid.uuid4().hex

        super(ContainerOperator, self).__init__(
            inputs=inputs,
            outputs=outputs,
        )

    @classmethod
    def _transform_env(cls, env):
        if not env:
            return dict()
        return {
            k: v.enclosed_fullname if isinstance(v, PipelineVariable) else str(v)
            for k, v in env.items()
        }

    @classmethod
    def _transform_commands(cls, commands):
        if isinstance(commands, six.string_types):
            return commands
        if not commands:
            return []

        return [
            c.enclosed_fullname if isinstance(c, PipelineVariable) else c
            for c in commands
        ]

    def to_dict(self):
        d = super(ContainerOperator, self).to_dict()
        d["spec"]["container"] = {
            "image": self.image_uri,
            "command": self._transform_commands(self.command),
        }
        d["spec"]["container"]["imageRegistryConfig"] = (
            self.image_registry_config or dict()
        )
        if self.env:
            d["spec"]["container"]["envs"] = self._transform_env(self.env or dict())

        if self.args:
            d["spec"]["container"]["args"] = self._transform_commands(self.args)
        return d

    def run(self, job_name, arguments=None, local_mode=False, **kwargs):
        if local_mode:
            return self._local_run(job_name, arguments=arguments)
        else:
            return super(ContainerOperator, self).run(
                job_name=job_name, arguments=arguments, **kwargs
            )

    @classmethod
    def get_default_image(cls):
        sess = get_default_session()
        if sess and sess._is_inner:
            return "reg.docker.alibaba-inc.com/pai-sdk/python:3.6"
        return "python:3"

    def _local_run(self, job_name, arguments=None):
        return LocalContainerRun(
            job_name=job_name,
            inputs=self.inputs,
            outputs=self.outputs,
            image_uri=self.image_uri,
            command=self.command,
            arguments=arguments,
            env=self.env.copy() if self.env else None,
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
        source_files=None,
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
        self.entry_point = entry_point
        self.source_files = source_files
        self.tmp_base_dir = None

    def prepare(self):
        self.tmp_base_dir = tempfile.mkdtemp()
        self._prepare_spec()
        self._prepare_parameters()
        self._prepare_artifacts()
        self._prepare_code()
        self.env["PYTHONUNBUFFERED"] = "1"

    def run(self):
        import docker

        print("Local container run start")
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
            print("Local container run exit, container_id=%s" % container.id)
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
        target_dir = "{0}/code/".format(self.tmp_base_dir)
        makedirs(target_dir)

        if self.source_files:
            for src in self.source_files:
                if os.path.isfile(src):
                    shutil.copy(src, target_dir)
                else:
                    shutil.copytree(src, target_dir)
        if self.entry_point:
            self.env.update(
                {
                    PAI_PROGRAM_ENTRY_POINT_ENV_KEY: self.entry_point,
                }
            )

    def _prepare_artifacts(self):
        artifact_path_format = "{0}/{1}/artifacts/{2}/data"
        for artifact in self.inputs.artifacts:
            if (
                artifact.name not in self.arguments
                or artifact.io_type == IO_TYPE_OUTPUTS
            ):
                continue

            artifact_arg = artifact.translate_argument(self.arguments[artifact.name])
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

    @classmethod
    def from_scripts(
        cls,
        source_dir,
        entry_file,
        inputs=None,
        outputs=None,
        image_uri=None,
        install_packages=None,
        base_image=None,
        **kwargs
    ):
        from pai.operator._script import ScriptOperator

        return ScriptOperator.create_with_image_snapshot(
            entry_file=entry_file,
            source_dir=source_dir,
            inputs=inputs,
            outputs=outputs,
            image_uri=image_uri,
            base_image=base_image,
            install_packages=install_packages,
            **kwargs
        )
