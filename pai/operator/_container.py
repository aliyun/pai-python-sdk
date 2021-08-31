# coding: utf-8
from __future__ import print_function

import logging
import json
import os
import shlex
import subprocess
import tempfile
import textwrap

import uuid

import shutil

from pai.common.utils import makedirs
from pai.operator._base import UnRegisteredOperator
from pai.operator.types import IO_TYPE_OUTPUTS
from pai.operator.types.variable import PipelineVariable

PAI_PROGRAM_ENTRY_POINT_ENV_KEY = "PAI_PROGRAM_ENTRY_POINT"
PAI_MANIFEST_SPEC_INPUTS_ENV_KEY = "PAI_MANIFEST_SPEC_INPUTS"
PAI_MANIFEST_SPEC_OUTPUTS_ENV_KEY = "PAI_MANIFEST_SPEC_OUTPUTS"
PAI_INPUTS_PARAMETERS_ENV_KEY = "PAI_INPUTS_PARAMETERS"

_logger = logging.getLogger(__name__)


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
            k: v.fullname if isinstance(v, PipelineVariable) else str(v)
            for k, v in env.items()
        }

    @classmethod
    def _transform_commands(cls, commands):
        if not commands:
            return []

        return [c.fullname if isinstance(c, PipelineVariable) else c for c in commands]

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
    def from_scripts(
        cls,
        source_dir,
        entry_file,
        inputs,
        outputs,
        image_uri,
        base_image=None,
        install_packages=None,
    ):
        """Build image

        Args:
            source_dir: Source script files use in Operator run.
            entry_file:
            inputs:
            outputs:
            image_uri: Image tag for the output image.
            base_image: Base image used to build the image use in Operator.
            install_packages: Required packages that will be installed in the image.

        Returns:
            ContainerOperator:
        """
        cls.build_and_push_image(
            source_dir,
            base_image=base_image or cls.get_default_image(),
            image_uri=image_uri,
            install_packages=install_packages,
            entry_file=entry_file,
        )

        return cls(
            image_uri=image_uri,
            command=shlex.split("python {}".format(entry_file)),
            inputs=inputs,
            outputs=outputs,
        )

    @classmethod
    def get_default_image(cls):
        return "python:3"

    @classmethod
    def build_and_push_image(
        cls, source_dir, entry_file, base_image, image_uri, install_packages=None
    ):
        """Build a docker image that contains the script file and install the required packages.

        Args:
            source_dir: source script files use in Operator run.
            base_image: Base image used to build the image use in Operator.
            image_uri: Image tag for the output image.
            install_packages: Required packages that will be installed in the image.
        """
        cls._build_image(
            source_dir,
            entry_file,
            base_image,
            install_packages=install_packages,
            image_uri=image_uri,
        )
        cls._push_image(image_uri)

    @classmethod
    def _build_image(
        cls, source_dir, entry_file, base_image, install_packages, image_uri
    ):
        build_dir = tempfile.mkdtemp()
        tmp_source_dir = os.path.join(build_dir, "__source_dir")
        shutil.copytree(source_dir, tmp_source_dir)
        install_packages = install_packages or []

        # append pip requirements read from file.
        requirement_file = os.path.join(tmp_source_dir, "requirements.txt")
        if os.path.isfile(requirement_file):
            with open(requirement_file, "r") as f:
                install_packages.extend(f.readlines())

        dockerfile = textwrap.dedent(
            """\
        # Build an image that run in PAI.
        FROM {base_image}

        RUN mkdir -p /work/code/
        COPY __source_dir/* /work/code/

        {install_packages}
        {entry_point}
        """
        ).format(
            base_image=base_image,
            install_packages=cls._get_install_packages_step(install_packages),
            entry_point=cls._get_entry_point(entry_file),
        )

        with open(os.path.join(build_dir, "Dockerfile"), "w") as f:
            f.write(dockerfile)

        command = "docker build . -t {}".format(image_uri)

        subprocess.check_call(shlex.split(command), cwd=build_dir, env=os.environ)

    @classmethod
    def _push_image(cls, image_uri):
        command = "docker push {}".format(image_uri)
        subprocess.check_call(shlex.split(command))

    @classmethod
    def _get_install_packages_step(cls, install_packages):
        if not install_packages:
            return ""
        packages = " ".join(install_packages)
        return "RUN PIP_DISABLE_PIP_VERSION_CHECK=1 python -m pip --quiet install {0}".format(
            packages
        )

    @classmethod
    def _get_entry_point(cls, entry_file):
        return "ENTRYPOINT {0}".format(json.dumps(["python", entry_file]))

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
