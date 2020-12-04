# coding: utf-8
import os
import tempfile
from oss2.exceptions import NotFound

from datetime import date

from pai.common.utils import tar_source_files, file_checksum
from pai.core.session import get_default_session
from pai.pipeline.templates.container import ContainerTemplate

ScriptTemplateImage = "registry.{region_id}.aliyuncs.com/paiflow-core/base:0.1.0"

PAI_SCRIPT_TEMPLATE_DEFAULT_COMMAND = "launch"
PAI_SOURCE_CODE_ENV_KEY = "PAI_SOURCE_CODE_URL"
PAI_PROGRAM_ENTRY_POINT_ENV_KEY = "PAI_PROGRAM_ENTRY_POINT"


class ScriptTemplate(ContainerTemplate):
    def __init__(
        self,
        entry_point,
        source_dir=None,
        inputs=None,
        outputs=None,
        command=None,
        image_uri=None,
        **kwargs
    ):
        """

        Args:
            entry_point: Entry point script name.
            source_dir: Directory of the source code.
            code_location: Location of the uploaded code in OSS path.
            image_uri:
            inputs:
            outputs:
            session:
        """
        self.source_dir = source_dir
        self.entry_point = entry_point

        if self.source_dir.startswith("oss://"):
            self._code_url = source_dir
        else:
            self._code_url = None
        command = command or [PAI_SCRIPT_TEMPLATE_DEFAULT_COMMAND]
        super(ScriptTemplate, self).__init__(
            inputs=inputs,
            outputs=outputs,
            image_uri=image_uri or self.get_image_uri(),
            command=command,
            **kwargs
        )

    def get_oss_bucket(self):
        session = get_default_session()
        return session.oss_bucket

    @property
    def source_dir(self):
        if hasattr(self, "_source_dir"):
            return self._source_dir
        self._source_dir = None
        return self._source_dir

    @source_dir.setter
    def source_dir(self, src_dir):
        if os.path.isabs(src_dir):
            self._source_dir = src_dir
        else:
            cwd = os.getcwd()
            src_dir = os.path.join(cwd, src_dir)
            self._source_dir = src_dir

    def _upload_source_files(self):
        if self.source_dir.startswith("oss://"):
            self._code_url = self.source_dir
            return

        if not self.source_dir:
            source_files = [self.entry_point]
        else:
            source_files = [
                os.path.join(self.source_dir, name)
                for name in os.listdir(self.source_dir)
            ]

        tar_result = tempfile.mktemp()
        try:
            tar_source_files(source_files=source_files, target=tar_result)
            checksum = file_checksum(tar_result)
            object_key = "pai/script_template/{date}/{checksum}/source.gz.tar".format(
                date=date.today().isoformat(), checksum=checksum
            )
            oss_url = self.put_if_not_exists(src=tar_result, object_key=object_key)
            self._code_url = oss_url
            return self._code_url
        finally:
            os.remove(tar_result)

    def put_if_not_exists(self, src, object_key):
        oss_bucket = self.get_oss_bucket()
        try:
            oss_bucket.head_object(object_key)
        except NotFound:
            oss_bucket.put_object_from_file(object_key, src)

        oss_url = "oss://{bucket_name}/{oss_key}?endpoint={endpoint}".format(
            bucket_name=oss_bucket.bucket_name,
            oss_key=object_key,
            endpoint=oss_bucket.endpoint,
        )
        return oss_url

    def get_image_uri(self):
        region_id = get_default_session().region_id
        return ScriptTemplateImage.format(region_id=region_id)

    def prepare(self):
        self._upload_source_files()

    def save(self, identifier, version):
        self.prepare()
        return super(ScriptTemplate, self).save(identifier=identifier, version=version)

    def run(self, job_name, arguments=None, local_mode=False, **kwargs):
        if not local_mode:
            self.prepare()
        return super(ScriptTemplate, self).run(
            job_name=job_name, arguments=arguments, **kwargs
        )

    def to_dict(self):
        if self.env:
            self.env.update({PAI_PROGRAM_ENTRY_POINT_ENV_KEY: self.entry_point})
        else:
            self.env = {PAI_PROGRAM_ENTRY_POINT_ENV_KEY: self.entry_point}
        if self._code_url:
            self.env.update({PAI_SOURCE_CODE_ENV_KEY: self._code_url})

        return super(ScriptTemplate, self).to_dict()
