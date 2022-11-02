# coding: utf-8

import os
import tempfile
from collections import namedtuple
from datetime import date

import six
from oss2.exceptions import NotFound, ServerError

from pai.common.oss_utils import is_oss_url
from pai.common.utils import (
    extract_file_name,
    file_checksum,
    tar_source_files,
    to_abs_path,
)
from pai.core.session import EnvType, Session, get_default_session
from pai.exception import PAIException
from pai.operator._container import (
    _PRE_PIP_INSTALL_TEMPLATE,
    ContainerOperator,
    _DefaultScriptOperatorImageLight,
    _DefaultScriptOperatorImagePublic,
)

PAI_SCRIPT_TEMPLATE_DEFAULT_COMMAND = "launch"
PAI_SOURCE_CODE_ENV_KEY = "PAI_SOURCE_CODE_URL"
PAI_PROGRAM_ENTRY_POINT_ENV_KEY = "PAI_PROGRAM_ENTRY_POINT"

ProgramSourceFiles = namedtuple("ProgramSourceFiles", ["entry_point", "source_files"])


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
        except NotFound:
            oss_bucket.put_object_from_file(object_key, src)
        except ServerError as e:
            if e.status == 403:
                raise PAIException(
                    "Permission denied, please check credentials for the OSS bucket: %s"
                    % oss_bucket.bucket_name
                )
            raise PAIException("Unexpected OSS server exception: %s" % e.__str__())

        oss_url = "oss://{bucket_name}/{oss_key}?endpoint={endpoint}".format(
            bucket_name=oss_bucket.bucket_name,
            oss_key=object_key,
            endpoint=oss_bucket.endpoint,
        )
        return oss_url

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
        **kwargs,
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
            image_uri = cls._get_default_image_uri()

        return ContainerOperator(
            inputs=inputs,
            outputs=outputs,
            image_uri=image_uri,
            command=commands,
            env=env,
            **kwargs,
        )

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
    def _get_default_image_uri(cls):
        session = get_default_session()
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
