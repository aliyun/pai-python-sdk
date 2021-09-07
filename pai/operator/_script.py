# coding: utf-8

import os
import shlex
import subprocess
import tempfile
from collections import namedtuple

import shutil
import six
from datetime import date

from pai.common.oss_utils import is_oss_url, OssNotFoundException
from pai.common.utils import (
    tar_source_files,
    file_checksum,
    to_abs_path,
    extract_file_name,
)
from pai.core.session import get_default_session
from pai.operator._container import ContainerOperator
from pai.operator.types import PipelineParameter

ScriptOperatorImage = "registry.{region_id}.aliyuncs.com/paiflow-public/python3:v1.0.0"

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


class ScriptOperator(ContainerOperator):
    """Build component run with script files.

    ScriptTemplate defines a PAI pipeline service component run with provided script. The Source files
    could be local files or remote files in OSS service.

    """

    @classmethod
    def _normalize_source_dir(cls, source_dir):
        if not source_dir:
            return source_dir
        elif is_oss_url(source_dir):
            return source_dir
        else:
            return to_abs_path(source_dir)

    @classmethod
    def _check_source_file(cls, entry_file, source_dir):
        if not extract_file_name(entry_file):
            raise ValueError("entry_file should not be a directory path.")

        if is_oss_url(entry_file) and source_dir:
            raise ValueError("source_dir is not used if entry_file is an OSS file.")

        if source_dir and extract_file_name(entry_file) != entry_file:
            raise ValueError(
                "entry_file should be in the top-level directory of source files."
            )

    @classmethod
    def _get_default_command(cls):
        return [PAI_SCRIPT_TEMPLATE_DEFAULT_COMMAND]

    @classmethod
    def _get_default_image_uri(cls):
        region_id = get_default_session().region_id
        return ScriptOperatorImage.format(region_id=region_id)

    @classmethod
    def _get_oss_bucket(cls):
        session = get_default_session()
        return session.oss_bucket

    @classmethod
    def upload_source_files(cls, source_dir, entry_file):
        # source_dir or entry_file is OSS resource URL, do not require upload.
        if is_oss_url(source_dir):
            return source_dir
        elif is_oss_url(entry_file):
            return entry_file

        elif not source_dir:
            if is_oss_url(entry_file):
                return entry_file
            else:
                source_files = [to_abs_path(entry_file)]
        else:
            source_files = [
                os.path.join(source_dir, name) for name in os.listdir(source_dir)
            ]

        tar_result = tempfile.mktemp()
        try:
            tar_source_files(source_files=source_files, target=tar_result)
            checksum = file_checksum(tar_result)
            object_key = "pai/script_operator/{date}/{checksum}/source.gz.tar".format(
                date=date.today().isoformat(), checksum=checksum
            )
            oss_url = cls._put_source_if_not_exists(
                src=tar_result, object_key=object_key
            )
            return oss_url
        finally:
            os.remove(tar_result)

    def download_source_files(self):
        pass

    @classmethod
    def _put_source_if_not_exists(cls, src, object_key):
        oss_bucket = cls._get_oss_bucket()
        try:
            oss_bucket.head_object(object_key)
        except OssNotFoundException:
            oss_bucket.put_object_from_file(object_key, src)

        oss_url = "oss://{bucket_name}/{oss_key}?endpoint={endpoint}".format(
            bucket_name=oss_bucket.bucket_name,
            oss_key=object_key,
            endpoint=oss_bucket.endpoint,
        )
        return oss_url

    @classmethod
    def _build_pre_install_package_command(cls, install_packages, pip_index_url=None):
        install_packages = (
            [install_packages]
            if isinstance(install_packages, six.string_types)
            else install_packages
        )

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
        return commands

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
            pip_index_url=None,
            image_uri=image_uri,
        )
        cls._push_image(image_uri)

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
            install_packages_step=cls._get_install_packages_step(install_packages),
            install_requirements_step=cls._get_install_requirements_step(
                tmp_source_dir
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
    def _create_oss_code_snapshot(cls, source_dir, entry_file):
        entry_point = extract_file_name(entry_file)
        source_code_url = cls.upload_source_files(source_dir, entry_file)
        return entry_point, source_code_url

    @classmethod
    def create_with_oss_snapshot(
        cls,
        entry_file,
        source_dir=None,
        inputs=None,
        outputs=None,
        image_uri=None,
        install_packages=None,
        pip_index_url=None,
        env=None,
        **kwargs
    ):

        """Construct Operator that uses snapshot code in OSS.

        Args:
            entry_file: Entry point script file, could be OSS file url or local file.
            source_dir: Directory of the source files, could be an OSS path or local directory.
            image_uri: The container imager used while run the component.
            inputs: The inputs definition of the operator.
            outputs: The output definition of the operator.
            install_packages:
            env:

        Returns:
            ContainerOperator:

        """

        cls._check_source_file(entry_file, source_dir)
        entry_point, source_code_url = cls._create_oss_code_snapshot(
            source_dir, entry_file
        )
        env = env or {}
        env.update(
            {
                PAI_PROGRAM_ENTRY_POINT_ENV_KEY: entry_point,
                PAI_SOURCE_CODE_ENV_KEY: source_code_url,
            }
        )

        commands = cls._build_pre_install_package_command(
            install_packages=install_packages,
            pip_index_url=pip_index_url,
        )

        commands.extend(
            [
                PAI_SCRIPT_TEMPLATE_DEFAULT_COMMAND,
            ]
        )

        if not image_uri:
            # sess = get_default_session()
            image_uri = ScriptOperatorImage.format(region_id="cn-hangzhou")

        return ContainerOperator(
            inputs=inputs,
            outputs=outputs,
            image_uri=image_uri,
            command=commands,
            env=env,
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
            base_image=base_image or cls.get_default_image(),
            image_uri=image_uri,
            install_packages=install_packages,
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
            image_uri=image_uri or cls.get_default_image(),
            inputs=inputs,
            outputs=outputs,
            command=commands,
            args=args,
            **kwargs
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

        if ext == ".sh":
            run_commands = ["sh", "-ec", source]
        else:
            run_commands = ["python", "-u", "-c", source]

        commands.extend(run_commands)
        args = []
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
    def _get_install_requirements_step(cls, source_dir):
        requirement_file = os.path.join(source_dir, "requirements.txt")
        if not os.path.isfile(requirement_file):
            return ""
        return "RUN python -m pip install -r requirements.txt"
