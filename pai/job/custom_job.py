import os
import shlex
import shutil
import tempfile
from datetime import datetime

import odps.dbapi
import oss2
import six
from oss2.exceptions import NotFound, ServerError
from six.moves.urllib import parse

from pai.api.common import DataSourceType
from pai.api.dlc import DlcClient
from pai.common.oss_utils import parse_oss_url, parse_dataset_path
from pai.common.utils import (
    random_str,
    to_abs_path,
    tar_file,
    makedirs,
)
from pai.core.session import Session
from pai.exception import PAIException
from pai.internal.dlc_job_helper import DlcJobHelper
from pai.job.common import JobConfig
from pai.job.common import JobType, GitConfig


class CustomJob(object):
    """Class to submit a Custom Job to PAI-DLC using script."""

    def __init__(
        self,
        image_uri=None,
        source_code=None,
        entry_point=None,
        parameters=None,
        base_dir=None,
        work_dir=None,
        job_type=None,
        code_path=None,
    ):
        """Construct a CustomJob.

        CustomJob helps to run script in PAI-DLC Job with specific image. User scripts is
        uploaded to OSS bucket specific in the session.

        Args:
            image_uri (str): Image uri using by the job.
            entry_point (str): Entry point of the job, could be .py or .sh file.
            parameters (dict): Parameters for the job, passing to job script as double-dash argument.
            base_dir (str): Base directory of the job, using /ml as default.
            work_dir (str): Working directory for the job script.
            job_type (str): Job type, could be TFJob, PyTorchJob or XGBoostJob.
            code_path (str): The OSS prefix path where the code is uploaded.
        """
        self.image_uri = image_uri
        self.entry_point = entry_point
        self.source_code = source_code
        self.parameters = parameters or dict()
        self.base_dir = base_dir or "/ml"
        self.work_dir = work_dir or os.path.join(self.base_dir, "code")
        self.job_type = JobType(job_type) if job_type else JobType.TFJob
        self.code_path = code_path
        self._job_id = None
        self._check()

        session = Session.current()
        self._job_helper = DlcJobHelper.from_session(session)
        self._session = session  # type: Session
        self._client = session.dlc_client  # type: DlcClient
        self._upload_source_files = None

        # OSS Dataset for inner PAI-DLC requires OSS RoleARN
        if session._oss_role_arn and session.is_inner:
            self._oss_role_arn = session._oss_role_arn
        else:
            self._oss_role_arn = None

    def _check(self):
        """Check the custom job spec."""
        if not self.image_uri:
            raise ValueError("Please provide image_uri for the job.")
        if not self.entry_point:
            raise ValueError("Please provide entry_point of the job.")
        if self.job_type not in JobType:
            raise ValueError("No supported job type: %s", self.job_type)

    def _put_source_if_not_exists(self, src, object_key):
        oss_bucket = self._session.oss_bucket  # type: oss2.Bucket
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

        # endpoint property of OSS bucket contains HTTP schema.
        endpoint = parse.urlparse(oss_bucket.endpoint).hostname
        oss_url = "oss://{bucket_name}.{endpoint}/{oss_key}".format(
            bucket_name=oss_bucket.bucket_name,
            oss_key=object_key,
            endpoint=endpoint,
        )
        return oss_url

    def _prepare_source_files(self):
        """Upload local source files to OSS."""
        if not self.source_code:
            return

        # TODO: support GitConfig.
        if isinstance(self.source_code, GitConfig):
            raise NotImplementedError("Not supported.")

        if not isinstance(self.source_code, six.string_types):
            raise ValueError(
                "Unsupported source_files type, expected string or GitConfig, but given %s",
                type(self.source_code),
            )
        if self.source_code.startswith("oss://"):
            self._upload_source_files = self.source_code
        else:

            source_dir = to_abs_path(self.source_code)
            tar_result = tar_file(source_file=source_dir)
            if not self.code_path:
                code_path = ""
            else:
                code_path = self.code_path.rstrip("/") + "/"

            object_key = "{code_path}pai/custom_job/{ts}/source.tar.gz".format(
                code_path=code_path,
                ts=datetime.now().isoformat(sep="-", timespec="milliseconds"),
            )
            self._upload_source_files = self._put_source_if_not_exists(
                src=tar_result, object_key=object_key
            )

        return self._upload_source_files

    def run(self, name, job_config, output_path=None, inputs=None, wait=True):
        """Submit the custom job to PAI-DLC.

        Args:
            name (str): Name of the job.
            output_path (str): Job output path.
            inputs (dict): Inputs for the job.
            job_config (JobConfig):
        """

        if self._job_id:
            raise RuntimeError("Job is submitted: job_id=%s" % self._job_id)

        dataset_ids = self._prepare_dataset_and_code_source(
            inputs, job_name=name, output_path=output_path
        )
        job_command = self._gen_job_command(inputs)

        # Group inner use PAI-DSW workgroup.
        if self._session.is_inner and job_config.workspace_id:
            workspace_id = job_config.workspace_id
        else:
            workspace_id = (
                self._job_helper.workspace_id
                if self._job_helper.is_use_aiworkspace()
                else None
            )

        for w in job_config.job_specs:
            w.image_uri = self.image_uri

        job_id = self._client.create_job(
            name=name,
            job_type=self.job_type,
            worker_specs=job_config.job_specs,
            resource_id=job_config.resource_id,
            data_source_ids=dataset_ids,
            user_command=job_command,
            workspace_id=workspace_id,
            envs={},
        )

        print("Job Url: {}".format(self._job_helper.job_url(job_id)))

        self._job_id = job_id

        if wait:
            self._job_helper.wait_for_completion(self._job_id)

        return self

    def _gen_job_command(self, inputs):
        """Generate command for the job."""
        prepare_cmd = self._code_prepare_command()

        if self.entry_point.endswith(".py"):
            exec_command = prepare_cmd + " ".join(
                ["python", self.entry_point] + self._build_job_command_args(inputs)
            )
        elif self.entry_point.endswith(".sh"):
            exec_command = prepare_cmd + " ".join(
                ["bash", self.entry_point] + self._build_job_command_args(inputs)
            )
        else:
            exec_command = prepare_cmd + " ".join(
                [self.entry_point] + self._build_job_command_args(inputs)
            )
        return exec_command

    def _code_prepare_command(self):
        """Build bash used for prepare code."""
        work_dir = shlex.quote(self.work_dir)
        prepare_sh = "mkdir -p {0} && cd {0} ".format(work_dir)

        # tar.gz source files in OSS will be mounted in path {base_dir}/mount/code/
        if self._upload_source_files:
            parsed = parse_oss_url(self._upload_source_files)
            is_dir, dir_path, file_name = parse_dataset_path(parsed.object_key)
            source_file_path = os.path.join(self.base_dir, "mount", "code", file_name)
            dest_path = os.path.join(self.base_dir, "code")
            prepare_sh += " && tar -xvzf {1} -C {0} ".format(
                dest_path,
                source_file_path,
            )
        return prepare_sh + " && "

    def _build_job_command_args(self, inputs):
        """Generate command arguments with component arguments.

        Returns:
            list: Returns `--arg1 v1 --arg2 va2` style arguments for execute program.
        """
        args = []
        # build argument list for user parameters.
        for name, v in self.parameters.items():
            args.append("--{}".format(shlex.quote(name)))
            args.append(shlex.quote(str(v)))

        # build arguments list for input artifact/data.
        for name, url in inputs.items():
            args.append("--{}".format(shlex.quote(name)))
            _, file_path = self._get_mount_path_for_channel(name, url)
            args.append(file_path)

        return args

    def _prepare_dataset_and_code_source(self, inputs, job_name, output_path):
        """Create Dataset/CodeSource to represent the input data and source files."""
        dataset_ids = self._create_dataset_for_channel_io(inputs, output_path)
        upload_source_files = self._prepare_source_files()
        if upload_source_files:
            dataset_ids.append(
                self._create_dataset_for_code(upload_source_files, job_name)
            )
        return dataset_ids

    def _get_output_mount_path(self):
        return "{}/output".format(self.base_dir)

    def _create_dataset_for_channel_io(self, inputs, output_path):
        """Create Datasets used in the job."""
        dataset_ids = []

        # Create dataset for input data.
        for name, url in inputs.items():
            mount_path, _ = self._get_mount_path_for_channel(name, url)
            dataset_id = self._job_helper.create_dataset(
                name="tmp-{}-{}".format(name, random_str(10)),
                data_source_type=DataSourceType.OSS,
                uri=url,
                mount_path=mount_path,
                role_arn=self._oss_role_arn,
            )
            dataset_ids.append(dataset_id)

        # Create dataset for training output.
        if output_path:
            dataset_id = self._job_helper.create_dataset(
                name="tmp-output-{}".format(random_str(10)),
                data_source_type=DataSourceType.OSS,
                uri=output_path,
                mount_path=self._get_output_mount_path(),
                role_arn=self._oss_role_arn,
            )
            dataset_ids.append(dataset_id)
        return dataset_ids

    @classmethod
    def _gen_dataset_name(cls, name):
        return "tmp-{}-{}".format(name, random_str(10))

    def _create_dataset_for_code(self, upload_source_files, job_name):
        """Create dataset using for mount input code."""
        if not upload_source_files:
            return
        parsed = parse_oss_url(upload_source_files)
        is_dir, dir_path, file_name = parse_dataset_path(parsed.object_key)

        uri = "oss://{bucket_name}.{endpoint}/{key}".format(
            bucket_name=parsed.bucket_name,
            endpoint=parsed.endpoint,
            key=dir_path.lstrip("/"),
        )
        # if source_file is tar.gz file in OSS, it should be mount
        # in {base_path}/mount/code and decompressed to {base_path}/code/
        if file_name.endswith(".tar.gz"):
            mount_path = f"{self.base_dir}/mount/code"
        else:
            mount_path = f"{self.base_dir}/code"

        dataset_id = self._job_helper.create_dataset(
            name="tmp-{}-sourcefile-{}".format(job_name, random_str(10)),
            uri=uri,
            mount_path=mount_path,
            data_source_type=DataSourceType.OSS,
            role_arn=self._oss_role_arn,
        )
        return dataset_id

    def _get_mount_path_for_channel(self, name, url):
        """Get channel mount path and file path."""
        parsed_oss = parse_oss_url(url)
        is_dir, dirname, filename = parse_dataset_path(parsed_oss.object_key)
        if is_dir:
            mount_path = f"{self.base_dir}/input/data/{name}"
            return mount_path, mount_path
        else:
            mount_path = f"{self.base_dir}/input/data/{name}"
            file_path = os.path.join(mount_path, filename)
            return mount_path, file_path

    def as_component(self, inputs=None, outputs=None):
        """Build a CustomJobOperator using the spec of the job.

        Args:
            inputs: Operator input definitions.
            outputs: Operator output definitions.

        Returns:
            CustomJobOperator: Operator response to submit CustomJob in workflow.

        """
        from pai.operator import CustomJobOperator

        return CustomJobOperator(
            entry_point=self.entry_point,
            image_uri=self.image_uri,
            parameters=self.parameters,
            source_code=self.source_code,
            job_type=self.job_type,
            base_dir=self.base_dir,
            work_dir=self.work_dir,
            code_path=self.code_path,
            outputs=outputs,
            inputs=inputs,
        )

    def local_run(self, inputs, output_path=None):
        """Run CustomJob in local with docker.

        Args:
            inputs: Inputs for the job, should be local file path.
            output_path: Output path of the job.

        Returns:
            LocalCustomJob:
        """
        job = LocalCustomJob(
            image_uri=self.image_uri,
            entry_point=self.entry_point,
            source_code=self.source_code,
            parameters=self.parameters,
            base_dir=self.base_dir,
        )

        job.run(inputs=inputs, output_path=output_path)


class LocalCustomJob(object):
    """Run CustomJob in local mode."""

    def __init__(self, image_uri, entry_point, source_code, parameters, base_dir):
        self.image_uri = image_uri
        self.entry_point = entry_point
        self.source_code = source_code
        self.parameters = parameters
        self.base_dir = base_dir
        self.local_base_dir = tempfile.mkdtemp()

    def _prepare_volumes(self, inputs, output_path):
        """Prepare input dataset

        Args:
            inputs: Input files for the job.
            output_path: Job output path.

        Returns:

        """

        volumes = {}

        # mount output path to container job output.
        if output_path:
            if not os.path.isabs(output_path):
                output_path = os.path.abspath(output_path)
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            if not os.path.isdir(output_path):
                raise ValueError("Output path should be a directory.")
            volumes[output_path] = {
                "bind": "{}/output/".format(self.base_dir),
                "mode": "rw",
            }

        # CustomJob requires channel name from inputs.
        input_configs = self._transform_inputs(inputs)

        # Mount directory of the input source file to job container.
        for config in input_configs:
            channel_dir = "{base_dir}/input/data/{channel_name}/".format(
                base_dir=self.base_dir,
                channel_name=config["name"],
            )
            volumes[config["dir_path"]] = {
                "bind": channel_dir,
                "mode": "rw",
            }

        # Mount source code to /ml/code/:
        source_code = os.path.realpath(os.path.expanduser(self.source_code))
        if os.path.isdir(source_code):
            code_dir = source_code
        else:
            code_dir = os.path.dirname(source_code)

        volumes[code_dir] = {
            "bind": "{}/code/".format(self.base_dir),
            "mode": "rw",
        }
        return volumes

    @classmethod
    def _transform_inputs(cls, inputs):
        """Transform inputs to a list of input config."""
        # CustomJob requires channel name to organize the directory structure of inputs.
        if isinstance(inputs, (list, tuple)):
            inputs = {"input_{0}".format(idx): item for idx, item in enumerate(inputs)}

        input_configs = []
        for name, value in inputs.items():
            if not os.path.isabs(value):
                source_path = os.path.realpath(value)
            else:
                source_path = value
            if not os.path.exists(source_path):
                raise ValueError("Input file path not exists: %s" % value)
            if os.path.isdir(source_path):
                dir_path = source_path
                is_dir = True
                file_name = None
            else:
                dir_path = os.path.dirname(source_path)
                is_dir = False
                file_name = os.path.basename(source_path)
            input_configs.append(
                {
                    "name": name,
                    "dir_path": dir_path,
                    "file_name": file_name,
                    "is_dir": is_dir,
                }
            )
        return input_configs

    def _gen_command(self, inputs, output_path):
        """Generate command using in local job run."""
        command = []
        if self.entry_point.endswith(".py"):
            command.extend(
                [
                    "python",
                    "-u",
                    shlex.quote(self.entry_point),
                ]
            )
        else:
            raise ValueError(
                "Not supported entry point file type: %s", self.entry_point
            )

        input_configs = self._transform_inputs(inputs)

        for name, v in self.parameters.items():
            command.append("--{}".format(shlex.quote(name)))
            command.append(shlex.quote(str(v)))

        for config in input_configs:
            command.append("--{}".format(shlex.quote(config["name"])))
            channel_dir = "{base_dir}/input/data/{channel_name}/".format(
                base_dir=self.base_dir, channel_name=config["name"]
            )
            if config["is_dir"]:
                command.append(shlex.quote(channel_dir))
            else:
                command.append(
                    shlex.quote(os.path.join(channel_dir, config["file_name"]))
                )

        return command

    def run(self, inputs, output_path=None):
        """

        Args:
            inputs:
            output_path:

        Returns:

        """
        import docker

        volumes = self._prepare_volumes(inputs=inputs, output_path=output_path)
        command = self._gen_command(inputs, output_path)
        docker_client = docker.from_env()

        container = docker_client.containers.run(
            image=self.image_uri,
            command=command,
            volumes=volumes,
            detach=True,
            working_dir="/ml/code/",
        )

        log_iterator = container.logs(stream=True)
        for log in log_iterator:
            print(log.decode("utf-8"), end="")
        print("Local container run exit, container_id=%s" % container.id)
        return docker_client.containers.get(container_id=container.id)
