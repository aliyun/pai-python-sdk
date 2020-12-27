# coding: utf-8
from collections import namedtuple

import os
import tempfile

from datetime import date

from pai.common.oss_utils import is_oss_url, OssNotFoundException
from pai.common.utils import (
    tar_source_files,
    file_checksum,
    to_abs_path,
    extract_file_name,
)

from pai.core.session import get_default_session
from pai.pipeline.templates.container import ContainerTemplate, LocalContainerRun

ScriptTemplateImage = "registry.{region_id}.aliyuncs.com/paiflow-core/base:1.0.0"

PAI_SCRIPT_TEMPLATE_DEFAULT_COMMAND = "launch"
PAI_SOURCE_CODE_ENV_KEY = "PAI_SOURCE_CODE_URL"
PAI_PROGRAM_ENTRY_POINT_ENV_KEY = "PAI_PROGRAM_ENTRY_POINT"

ProgramSourceFiles = namedtuple("ProgramSourceFiles", ["entry_point", "source_files"])


class ScriptTemplate(ContainerTemplate):
    """Build component run with script files.

    ScriptTemplate defines a PAI pipeline service component run with provided script. The Source files
    could be local files or remote files in OSS service.

    """

    def __init__(
        self,
        entry_file,
        source_dir=None,
        inputs=None,
        outputs=None,
        command=None,
        image_uri=None,
        **kwargs
    ):
        """Constructor of ScriptTemplate.

        Args:
            entry_file: Entry point script file, could be OSS file url or local file.
            source_dir: Directory of the source files, could be an OSS path or local directory.
            image_uri: The container imager used while run the component.
            inputs: The inputs definition of the component.
            outputs: Tht output definition of the component.
        """

        self.check_source_file(entry_file, source_dir)
        self._entry_file = entry_file
        self._source_dir = self._format_source_dir(source_dir)
        self._program_files = None
        super(ScriptTemplate, self).__init__(
            inputs=inputs,
            outputs=outputs,
            image_uri=image_uri or self._get_default_image_uri(),
            command=command or self._get_default_command(),
            **kwargs
        )

    @property
    def entry_file(self):
        return self._entry_file

    @property
    def source_dir(self):
        return self._source_dir

    def _is_remote_source_files(self):
        return is_oss_url(self.entry_file) or is_oss_url(self.source_dir)

    @classmethod
    def _format_source_dir(cls, source_dir):
        if not source_dir:
            return source_dir
        elif is_oss_url(source_dir):
            return source_dir
        else:
            return to_abs_path(source_dir)

    @classmethod
    def check_source_file(cls, entry_file, source_dir):
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
        return ScriptTemplateImage.format(region_id=region_id)

    def get_oss_bucket(self):
        session = get_default_session()
        return session.oss_bucket

    def upload_source_files(self):
        if is_oss_url(self._source_dir):
            return self._source_dir
        elif is_oss_url(self._entry_file):
            return self._entry_file
        elif not self._source_dir:
            if is_oss_url(self._entry_file):
                return self._entry_file
            else:
                source_files = [to_abs_path(self._entry_file)]
        else:
            source_files = [
                os.path.join(self._source_dir, name)
                for name in os.listdir(self._source_dir)
            ]

        tar_result = tempfile.mktemp()
        try:
            tar_source_files(source_files=source_files, target=tar_result)
            checksum = file_checksum(tar_result)
            object_key = "pai/script_template/{date}/{checksum}/source.gz.tar".format(
                date=date.today().isoformat(), checksum=checksum
            )
            oss_url = self._put_source_if_not_exists(
                src=tar_result, object_key=object_key
            )
            return oss_url
        finally:
            os.remove(tar_result)

    def download_source_files(self):
        pass

    def _put_source_if_not_exists(self, src, object_key):
        oss_bucket = self.get_oss_bucket()
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

    def prepare(self):
        entry_point = extract_file_name(self._entry_file)
        source_code_url = self.upload_source_files()
        self._program_files = ProgramSourceFiles(
            entry_point=entry_point, source_files=source_code_url
        )

    def save(self, identifier, version):
        self.prepare()
        return super(ScriptTemplate, self).save(identifier=identifier, version=version)

    def run(self, job_name, arguments=None, local_mode=False, **kwargs):
        if not local_mode:
            self.prepare()
        return super(ScriptTemplate, self).run(
            job_name=job_name, arguments=arguments, local_mode=local_mode, **kwargs
        )

    def to_dict(self):
        manifest = super(ScriptTemplate, self).to_dict()
        if self._program_files:
            manifest["spec"]["container"]["envs"].update(
                {
                    PAI_PROGRAM_ENTRY_POINT_ENV_KEY: self._program_files.entry_point,
                    PAI_SOURCE_CODE_ENV_KEY: self._program_files.source_files,
                }
            )
        return manifest

    def _local_run(self, job_name, arguments=None):
        if self._is_remote_source_files():
            raise ValueError(
                "ScriptTemplate do not support local run on remote source files."
            )
        entry_point = extract_file_name(self._entry_file)
        if not self._source_dir:
            source_files = [to_abs_path(self._entry_file)]
        else:
            source_files = [
                os.path.join(self._source_dir, fname)
                for fname in os.listdir(to_abs_path(self._source_dir))
            ]

        LocalContainerRun(
            job_name=job_name,
            inputs=self.inputs,
            outputs=self.outputs,
            image_uri=self.image_uri,
            command=self.command,
            arguments=arguments,
            entry_point=entry_point,
            source_files=source_files,
            env=self.env.copy() if self.env else None,
        ).run()
