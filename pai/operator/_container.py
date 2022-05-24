# coding: utf-8
from __future__ import print_function

import shlex
from collections import namedtuple

import json
import logging
import os
import shutil
import six
import subprocess
import tempfile
import uuid

from pai.common.utils import makedirs
from pai.common.yaml_utils import dump as yaml_dump
from pai.core.session import Session, EnvType
from pai.operator._base import UnRegisteredOperator
from pai.operator.types import IO_TYPE_OUTPUTS, PipelineParameter
from pai.operator.types.variable import PipelineVariable

PAI_MANIFEST_SPEC_INPUTS_ENV_KEY = "PAI_MANIFEST_SPEC_INPUTS"
PAI_MANIFEST_SPEC_OUTPUTS_ENV_KEY = "PAI_MANIFEST_SPEC_OUTPUTS"
PAI_INPUTS_PARAMETERS_ENV_KEY = "PAI_INPUTS_PARAMETERS"

_logger = logging.getLogger(__name__)

_PIP_INSTALL_TEMPLATE = '''\
(PIP_DISABLE_PIP_VERSION_CHECK=1 python3 -m pip install --quiet {pkgs} \
|| PIP_DISABLE_PIP_VERSION_CHECK=1 python3 -m pip install --quiet \
 {pkgs} --user) && "$0" "$@"'''


_DefaultScriptOperatorImagePublic = (
    "registry.{region_id}.aliyuncs.com/paiflow-public/python3:v1.0.0"
)
_DefaultScriptOperatorImageLight = "master0:5000/eflops/python3:v0.1.0"


PAI_SCRIPT_TEMPLATE_DEFAULT_COMMAND = "launch"
PAI_SOURCE_CODE_ENV_KEY = "PAI_SOURCE_CODE_URL"
PAI_PROGRAM_ENTRY_POINT_ENV_KEY = "PAI_PROGRAM_ENTRY_POINT"

ProgramSourceFiles = namedtuple("ProgramSourceFiles", ["entry_point", "source_files"])


_PRE_PIP_INSTALL_TEMPLATE = '''\
(PIP_DISABLE_PIP_VERSION_CHECK=1 {pip_index_url_env} python3 -m pip install --quiet {pkgs} \
|| PIP_DISABLE_PIP_VERSION_CHECK=1 {pip_index_url_env} python3 -m pip install --quiet \
 {pkgs} --user) && "$0" "$@"'''

_DEFAULT_PIP_INDEX_URL = "https://mirrors.aliyun.com/pypi/simple/"

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
            return [commands]
        if not commands:
            return []

        return [
            c.enclosed_fullname if isinstance(c, PipelineVariable) else c
            for c in commands
        ]

    def to_dict(self, identifier=None, version=None):
        d = super(ContainerOperator, self).to_dict()

        if identifier is not None:
            d["metadata"]["identifier"] = identifier
        if version is not None:
            d["metadata"]["version"] = version

        if Session.current():
            d["metadata"]["provider"] = Session.current().provider

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

    def to_manifest(self, identifier, version):
        return yaml_dump(self.to_dict(identifier=identifier, version=version))

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

    @classmethod
    def create_with_source_snapshot(
        cls,
        script_file,
        inputs=None,
        outputs=None,
        image_uri=None,
        install_packages=None,
        pip_index_url=_DEFAULT_PIP_INDEX_URL,
        **kwargs
    ):
        """Construct Operator that uses snapshot code in image.

        Given `script_file` will be passed to the command as literal source code and
        executed by Shell or Python.


        Args:
            script_file:
            image_uri:
            inputs:
            outputs:
            install_packages:
            pip_index_url:

        Returns:

        """

        commands, args = cls._build_script_commands(
            script_file=script_file,
            install_packages=install_packages,
            pip_index_url=pip_index_url,
            inputs=inputs,
        )

        return ContainerOperator(
            image_uri=image_uri or cls._get_default_image_uri(),
            inputs=inputs,
            outputs=outputs,
            command=commands,
            args=args,
            **kwargs
        )

    @classmethod
    def create_with_image_snapshot(
        cls,
        entry_file,
        source_dir,
        image_uri,
        inputs=None,
        outputs=None,
        base_image=None,
        install_packages=None,
        pip_index_url=_DEFAULT_PIP_INDEX_URL,
        **kwargs
    ):
        """Construct Operator that uses snapshot code in image.

        The method will build a new docker image using the docker cli tool. Files in source_dir
        will be added to the image at "/work/code" and the required pip packages will be installed.
        Operator use the new image to run the job.

        Args:
            source_dir: Source script files use in Operator run.
            entry_file: Entry point file use in Operator run.
            inputs: Inputs spec of the Operator.
            outputs: Outputs spec of the Operator.
            image_uri: Image tag for the output image.
            base_image: Base image used to build the image use in Operator.
            install_packages: Required packages that will be installed in the image.
            pip_index_url:

        Returns:
            ContainerOperator:
        """

        cls._build_and_push_image(
            source_dir,
            base_image=base_image or cls._get_default_image_uri(),
            image_uri=image_uri,
            install_packages=install_packages,
            pip_index_url=pip_index_url,
        )

        commands, args = cls._build_commands_for_image_snapshot(entry_file, inputs)

        return ContainerOperator(
            image_uri=image_uri,
            command=commands,
            args=args,
            inputs=inputs,
            outputs=outputs,
            **kwargs
        )

    @classmethod
    def _get_default_image_uri(cls):
        session = Session.current()
        if session.env_type == EnvType.Light:
            return _DefaultScriptOperatorImageLight
        else:
            return (
                _DefaultScriptOperatorImagePublic
                if session.is_inner
                else _DefaultScriptOperatorImagePublic.format(
                    region_id=session.region_id
                )
            )

    @classmethod
    def _build_script_commands(
        cls, script_file, install_packages, inputs, pip_index_url=None
    ):
        install_packages = (
            [install_packages]
            if isinstance(install_packages, six.string_types)
            else install_packages
        )

        _, ext = os.path.splitext(script_file)
        if ext not in [".py", ".sh"]:
            raise ValueError(
                "Not support script file, please provide Shell(.sh) or Python(.py) script."
            )
        with open(script_file, "r") as f:
            source = f.read()

        pip_index_url_env = (
            "PIP_INDEX_URL={}".format(pip_index_url) if pip_index_url else ""
        )
        commands = (
            [
                "sh",
                "-c",
                _PRE_PIP_INSTALL_TEMPLATE.format(
                    pkgs="".join(["'%s'" % p for p in install_packages]),
                    pip_index_url_env=pip_index_url_env,
                ),
            ]
            if install_packages
            else []
        )
        args = []

        if ext == ".sh":
            run_commands = ["sh", "-ec", source]
            args.append("--")
        else:
            run_commands = ["python", "-u", "-c", source]

        commands.extend(run_commands)
        if not inputs:
            return commands, args

        for p in inputs:
            if isinstance(p, PipelineParameter):
                args.append("--%s" % p.name)
                args.append(p)
        return commands, args

    @classmethod
    def _get_install_packages_step(cls, install_packages, pip_index_url=None):
        if not install_packages:
            return ""
        packages = " ".join(install_packages)
        if not pip_index_url:
            return "RUN python -m pip install {0}".format(packages)
        return "RUN PIP_INDEX_URL={0} python -m pip install {1}".format(
            pip_index_url, packages
        )

    @classmethod
    def _get_install_requirements_step(cls, source_dir, pip_index_url=None):
        requirement_file = os.path.join(source_dir, "requirements.txt")
        if not os.path.isfile(requirement_file):
            return ""
        if not pip_index_url:
            return "RUN  python -m pip install -r requirements.txt"
        return "RUN PIP_INDEX_URL={0} python -m pip install -r requirements.txt".format(
            pip_index_url
        )

    @classmethod
    def _build_image(
        cls, source_dir, base_image, install_packages, image_uri, pip_index_url=None
    ):
        build_dir = tempfile.mkdtemp()
        tmp_source_dir = os.path.join(build_dir, "__source_dir")
        shutil.copytree(source_dir, tmp_source_dir)
        install_packages = install_packages or []

        dockerfile = _DOCKERFILE_TEMPLATE.format(
            base_image=base_image,
            install_packages_step=cls._get_install_packages_step(
                install_packages, pip_index_url
            ),
            install_requirements_step=cls._get_install_requirements_step(
                tmp_source_dir,
                pip_index_url,
            ),
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
    def _build_commands_for_image_snapshot(cls, entry_file, inputs):
        filename, file_extension = os.path.splitext(entry_file)
        if file_extension == ".py":
            commands = ["python", entry_file]
        elif file_extension == ".sh":
            commands = ["sh", entry_file]
        else:
            commands = ["./%s" % entry_file]

        if not inputs:
            return commands

        args = []
        for p in inputs:
            if isinstance(p, PipelineParameter):
                args.append("--%s" % p.name)
                args.append(p)
        return commands, args

    @classmethod
    def _build_and_push_image(
        cls,
        source_dir,
        base_image,
        image_uri,
        install_packages=None,
        pip_index_url=None,
    ):
        """Build a docker image that contains the script file and install the required packages.

        Args:
            source_dir: source script files use in Operator run.
            base_image: Base image used to build the image use in Operator.
            image_uri: Image tag for the output image.
            install_packages: Required packages that will be installed in the image.
        """
        print("build and push image: %s" % image_uri)
        cls._build_image(
            source_dir,
            base_image,
            install_packages=install_packages,
            pip_index_url=pip_index_url,
            image_uri=image_uri,
        )
        cls._push_image(image_uri)


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
