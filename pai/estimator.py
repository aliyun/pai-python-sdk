import json
import logging
import os
import posixpath
import shlex
import tempfile
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

import oss2
import six
from oss2.exceptions import NotFound
from six.moves.urllib import parse

from pai.common.consts import DataSourceType, JobType
from pai.common.oss_utils import parse_dataset_path, parse_oss_url
from pai.common.utils import random_str, tar_file, to_abs_path
from pai.core.session import Session, get_default_session
from pai.entity.common import DataSourceConfig, GitConfig
from pai.entity.job import Job, JobSpec
from pai.entity.service import Service, ServiceConfig
from pai.predictor import Predictor

logger = logging.getLogger(__name__)


class DataConfigBase(object):
    def __init__(
        self, name=None, dataset_id=None, uri=None, mount_path=None, data_path=None
    ):
        self.name = name
        self.dataset_id = dataset_id
        self.uri = uri
        self.mount_path = mount_path
        self.data_path = data_path

    def to_dict(self):
        d = {
            "DatasetId": self.dataset_id,
            "Name": self.name,
            "URI": self.uri,
            "MountPath": self.mount_path,
            "DataPath": self.data_path,
        }
        return d


class InputDataConfig(DataConfigBase):
    def to_dict(self):
        d = super(InputDataConfig, self).to_dict()
        d.update({"IOType": "inputs"})
        return d


class OutputDataConfig(DataConfigBase):
    def to_dict(self):
        d = super(OutputDataConfig, self).to_dict()
        d.update({"IOType": "outputs"})
        return d


class EstimatorTrainingJobEnvironment(object):
    PAI_INPUT_DATA_CONFIG = "PAI_INPUT_DATA_CONFIG"
    PAI_OUTPUT_DATA_CONFIG = "PAI_OUTPUT_DATA_CONFIG"
    PAI_USER_ENTRY_POINT = "PAI_USER_ENTRY_POINT"
    PAI_USER_PROGRAM = "PAI_USER_PROGRAM"


class InputCodeConfig(object):
    def __init__(self, dataset_id, uri, mount_path):
        self.dataset_id = dataset_id
        self.uri = uri
        self.mount_path = mount_path

    def to_dict(self):
        return {
            "DatasetId": self.dataset_id,
            "URI": self.uri,
            "MountPath": self.mount_path,
        }


class Estimator(object):
    """Class to submit a Training Job to PAI-DLC with script."""

    def __init__(
        self,
        image_uri: str = None,
        source_code: str = None,
        entry_point: str = None,
        hyperparameters: Dict[str, Any] = None,
        base_dir: str = "/ml/",
        work_dir: str = "/ml/code/",
        base_job_name=None,
        environment_variables: Dict[str, str] = None,
        job_type: str = "TFJob",
        job_specs: List[JobSpec] = None,
        vpc_config: Dict[str, str] = None,
        third_party_libs: List[str] = None,
        output_path: str = None,
        session: Session = None,
        code_path=None,
        **kwargs,
    ):
        """Construct an Estimator to submit a training job.

        EstimatorV1 helps to run script in PAI-DLC Job with specific image. User scripts is
        uploaded to OSS bucket specific in the session.

        Args:
            image_uri (str): Image uri using by the job.
            entry_point (str): Entry point of the job, could be .py or .sh file.
            hyperparameters (dict): Parameters for the job, passing to job script as double-dash argument.
            base_dir (str): Base directory of the job, using /ml as default.
            work_dir (str): Working directory for the job script.
            job_type (str): Job type, could be TFJob, PyTorchJob or XGBoostJob.
            code_path (str): The OSS prefix path where the code is uploaded.
        """
        self.image_uri = image_uri
        self.entry_point = entry_point
        self.source_code = source_code
        self.hyperparameters = hyperparameters or dict()
        self.job_specs = job_specs
        self.base_dir = base_dir or "/ml"
        self.work_dir = work_dir or posixpath.join(self.base_dir, "code")
        self.job_type = job_type if job_type else JobType.TFJob
        self.code_path = code_path
        self.base_job_name = base_job_name
        self.output_path = output_path
        self.environment_variables = environment_variables or dict()
        self.vpc_config = vpc_config
        self._latest_job = None

        self._session = session or get_default_session()
        if not self._session:
            raise ValueError("Estimator requires a valid session.")
        self.__uploaded_source_files = None

    def gen_job_display_name(self, job_name=None):
        """Generate job display name."""
        if job_name:
            return job_name

        return "{}_{}".format(
            self.base_job_name or "job_", datetime.now().isoformat(sep=" ")
        )

    def _check(self):
        """Check the custom job spec."""
        if not self.image_uri:
            raise ValueError("Please provide image_uri for the job.")
        if not self.entry_point:
            raise ValueError("Please provide entry_point of the job.")

    def _put_source_if_not_exists(self, src, object_key):
        oss_bucket = self._session.oss_bucket  # type: oss2.Bucket
        try:
            oss_bucket.head_object(object_key)
        except NotFound:
            oss_bucket.put_object_from_file(object_key, src)

        # endpoint property of OSS bucket contains HTTP schema.
        endpoint = parse.urlparse(oss_bucket.endpoint).hostname
        oss_url = "oss://{bucket_name}.{endpoint}/{oss_key}".format(
            bucket_name=oss_bucket.bucket_name,
            oss_key=object_key,
            endpoint=endpoint,
        )
        return oss_url

    def _upload_source_files(self):
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
            self.__uploaded_source_files = self.source_code
        else:
            source_dir = to_abs_path(self.source_code)
            tar_result = tar_file(source_file=source_dir)
            if not self.code_path:
                code_path = ""
            else:
                code_path = self.code_path.rstrip("/") + "/"

            object_key = "{code_path}pai/job-sources-code/{ts}/source.tar.gz".format(
                code_path=code_path,
                ts=datetime.now().isoformat(sep="-", timespec="milliseconds"),
            )
            self.__uploaded_source_files = self._put_source_if_not_exists(
                src=tar_result, object_key=object_key
            )

        return self.__uploaded_source_files

    def fit(self, inputs=None, wait=True, job_name=None):
        job_name = self.gen_job_display_name(job_name=job_name)
        (
            input_data_configs,
            output_data_configs,
        ) = self._make_data_config_for_input_output(
            inputs, output_path=self.output_path
        )

        input_code_config = self._make_source_code_input(job_name)
        command = self._make_job_command(input_data_configs=input_data_configs)
        for job_spec in self.job_specs:
            if job_spec.image is None:
                job_spec.image = self.image_uri
        job_id = self._session.job_api.create(
            display_name=job_name,
            job_type=self.job_type,
            job_specs=self.job_specs,
            # code_source_config=None,
            data_source_configs=self._make_data_source_config(
                input_data_configs,
                output_data_configs,
                input_code_config,
            ),
            environment_variables=self._make_environment_variables(
                input_data_configs=input_data_configs,
                output_data_configs=output_data_configs,
            ),
            # max_running_time_minutes=None,
            # # options=None,
            # resource_id=None,
            # priority=None,
            # thirdparty_lib_dir=None,
            # thirdparty_libs=None,
            user_command=command,
            user_vpc=self.vpc_config,
        )
        self._latest_job = Job.get(job_id)

        print(
            "View the job detail by accessing the console URI: {}".format(
                self._latest_job.console_uri
            )
        )

        if wait:
            self._latest_job.wait_for_completion()

    def deploy(
        self,
        model_file_name=None,
        service_config: Union[Dict[str, Any], ServiceConfig] = None,
        serializer=None,
    ) -> Predictor:
        if model_file_name:
            model_path = posixpath.join(self.output_path, model_file_name)
        else:
            model_path = self.output_path

        if isinstance(service_config, dict):
            service_config["model_path"] = model_path
        else:
            service_config.model_path = model_path
        service = Service.deploy_by_config(
            config=service_config,
            session=self._session,
        )
        return service.get_predictor(serializer=serializer)

    def _make_job_command(self, input_data_configs: List[DataConfigBase]) -> str:
        """Generate command for the job."""

        # Make code prepare command.
        prepare_cmd = ["mkdir", "-p", self.work_dir, "&&", "cd", self.work_dir]
        # tar.gz source files in OSS will be mounted in path {base_dir}/mount/code/
        if self.__uploaded_source_files:
            parsed = parse_oss_url(self.__uploaded_source_files)
            is_dir, dir_path, file_name = parse_dataset_path(parsed.object_key)
            source_file_path = posixpath.join(self.base_dir, "mount", "code", file_name)
            dest_path = posixpath.join(self.base_dir, "code")
            prepare_cmd += ["&&", "tar", "-xvzf", source_file_path, "-C", dest_path]
        prepare_cmd.append("&&")

        if self.entry_point.endswith(".py"):
            exec_command = (
                prepare_cmd
                + ["python", self.entry_point]
                + self._make_job_command_args(input_data_configs)
            )
        elif self.entry_point.endswith(".sh"):
            exec_command = (
                prepare_cmd
                + ["bash", self.entry_point]
                + self._make_job_command_args(input_data_configs)
            )
        else:
            exec_command = (
                prepare_cmd
                + [self.entry_point]
                + self._make_job_command_args(input_data_configs)
            )

        return " ".join(exec_command)

    def _make_job_command_args(
        self, input_data_config: List[DataConfigBase]
    ) -> List[str]:
        """Generate command arguments with component arguments.

        Returns:
            list: Returns `--arg1 v1 --arg2 va2` style arguments for execute program.
        """
        args = []
        # build argument list for user parameters.
        for name, v in self.hyperparameters.items():
            args.append("--{}".format(shlex.quote(name)))
            args.append(shlex.quote(str(v)))

        # build arguments list for input artifact/data.

        for data_config in input_data_config:
            args.append("--{}".format(shlex.quote(data_config.name)))
            args.append(data_config.data_path)

        return args

    def _make_source_code_input(self, job_name) -> Optional[InputCodeConfig]:
        """Create Dataset/CodeSource to represent the input data and source files."""
        upload_source_files = self._upload_source_files()
        if not upload_source_files:
            return
        return self._create_dataset_for_oss_code(upload_source_files, job_name)

    def _get_output_mount_path(self):
        return posixpath.join(self.base_dir, "output/")

    def _get_input_mount_path(self, name):
        return posixpath.join(self.base_dir, "input/data", name)

    def _make_data_config_for_input_output(self, inputs, output_path):
        """Create Datasets used in the job."""

        input_data_configs = []
        output_data_configs = []

        # Create dataset for input data.
        for name, uri in inputs.items():
            source_uri, mount_path, local_path = self._get_mount_config_for_input(
                name, uri
            )
            dataset_id = self._session.dataset_api.create(
                name="tmp-{}-{}".format(name, random_str(10)),
                data_source_type=DataSourceType.OSS,
                uri=source_uri,
                mount_path=self._get_input_mount_path(name),
            )

            input_data_configs.append(
                InputDataConfig(
                    name=name,
                    uri=uri,
                    dataset_id=dataset_id,
                    mount_path=mount_path,
                    data_path=local_path,
                )
            )

        # Create dataset for training output.
        if output_path:
            mount_path = self._get_output_mount_path()
            dataset_id = self._session.dataset_api.create(
                name="tmp-output-{}".format(random_str(10)),
                data_source_type=DataSourceType.OSS,
                uri=output_path,
                mount_path=mount_path,
            )

            output_data_configs.append(
                OutputDataConfig(
                    name="output",
                    uri=output_path,
                    dataset_id=dataset_id,
                    mount_path=mount_path,
                    data_path=mount_path,
                )
            )

        return input_data_configs, output_data_configs

    def _make_data_source_config(
        self,
        input_data_config: List[InputDataConfig],
        output_data_config: List[OutputDataConfig],
        input_code_config: InputCodeConfig,
    ) -> List[DataSourceConfig]:
        data_source_configs = [
            DataSourceConfig(
                dataset_id=input.dataset_id,
                mount_path=input.mount_path,
            )
            for input in input_data_config
        ] + [
            DataSourceConfig(
                dataset_id=output.dataset_id,
                mount_path=output.mount_path,
            )
            for output in output_data_config
        ]

        if input_code_config:
            data_source_configs.append(
                DataSourceConfig(
                    dataset_id=input_code_config.dataset_id,
                    mount_path=input_code_config.mount_path,
                )
            )

        return data_source_configs

    @classmethod
    def _gen_dataset_name(cls, name):
        return "tmp-{}-{}".format(name, random_str(10))

    def _create_dataset_for_oss_code(
        self, upload_source_files, job_name
    ) -> Optional[InputCodeConfig]:
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
        dataset_id = self._session.dataset_api.create(
            name="tmp-{}-sourcefile-{}".format(job_name, random_str(10)),
            uri=uri,
            mount_path=mount_path,
            data_source_type=DataSourceType.OSS,
        )
        return InputCodeConfig(
            dataset_id=dataset_id,
            uri=uri,
            mount_path=mount_path,
        )

    def _get_mount_config_for_input(self, name, url):
        """Get channel mount path and file path."""
        parsed_oss = parse_oss_url(url)
        is_dir, dirname, filename = parse_dataset_path(parsed_oss.object_key)
        source_uri = "oss://{}.{}{}".format(
            parsed_oss.bucket_name, parsed_oss.endpoint, dirname
        )
        if is_dir:
            mount_path = f"{self.base_dir}/input/data/{name}"
            return source_uri, mount_path, mount_path
        else:
            mount_path = f"{self.base_dir}/input/data/{name}"
            file_path = posixpath.join(mount_path, filename)
            return source_uri, mount_path, file_path

    def _make_environment_variables(
        self,
        input_data_configs: List[InputDataConfig],
        output_data_configs: List[OutputDataConfig],
    ) -> Dict[str, str]:
        env = self.environment_variables.copy() or {}
        env.update(
            {
                EstimatorTrainingJobEnvironment.PAI_INPUT_DATA_CONFIG: json.dumps(
                    [input.to_dict() for input in input_data_configs]
                ),
                EstimatorTrainingJobEnvironment.PAI_OUTPUT_DATA_CONFIG: json.dumps(
                    [output.to_dict() for output in output_data_configs]
                ),
                EstimatorTrainingJobEnvironment.PAI_USER_ENTRY_POINT: self.entry_point,
            }
        )
        if self.__uploaded_source_files:
            env.update(
                {
                    EstimatorTrainingJobEnvironment.PAI_USER_PROGRAM: self.__uploaded_source_files,
                }
            )
        return env

    def local_run(self, inputs, output_path=None):
        """Run estimator job in local with docker.

        Args:
            inputs: Inputs for the job, should be local file path.
            output_path: Output path of the job.

        Returns:
            _LocalRunJob:
        """
        if not output_path:
            output_path = tempfile.mkdtemp()
            logger.info("Local run job temporary output path: {}".format(output_path))

        output_path = output_path or tempfile.mkdtemp()
        job = _LocalContainerJob(
            image_uri=self.image_uri,
            entry_point=self.entry_point,
            source_code=self.source_code,
            hyperparameters=self.hyperparameters,
            environment_variables=self.environment_variables,
            base_dir=self.base_dir,
            work_dir=self.work_dir,
        )

        job.run(inputs=inputs, output_path=output_path)


class _LocalContainerJob(object):
    """Run estimator job in local mode."""

    def __init__(
        self,
        image_uri: str,
        entry_point: str,
        source_code: str,
        hyperparameters: Dict[str, Any],
        base_dir: str,
        work_dir: str,
        environment_variables: Dict[str, str] = None,
        host_base_dir=None,
    ):
        self.image_uri = image_uri
        self.entry_point = entry_point
        self.source_code = source_code
        self.hyperparameters = hyperparameters
        self.base_dir = base_dir
        self.work_dir = work_dir
        self.environment_variables = environment_variables or dict()
        self.host_base_dir = host_base_dir, tempfile.mkdtemp()

    def _make_input_data_config(self, inputs) -> List[InputDataConfig]:
        """Transform inputs to a list of input config."""
        # Estimator requires names of input to organize the directory structure of inputs.
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
            mount_path = posixpath.join(self.base_dir, "input/data", name)
            if os.path.isdir(source_path):
                dir_path = source_path
                data_path = mount_path
            else:
                dir_path = os.path.dirname(source_path)
                file_name = os.path.basename(source_path)
                data_path = posixpath.join(mount_path, file_name)
            input_configs.append(
                InputDataConfig(
                    name=name,
                    dataset_id=None,
                    uri=dir_path,
                    mount_path=mount_path,
                    data_path=data_path,
                )
            )
        return input_configs

    def _make_data_config(
        self, inputs, output_path
    ) -> Tuple[List[InputDataConfig], List[OutputDataConfig]]:
        # mount output path to container job output.
        if not os.path.isabs(output_path):
            output_path = os.path.abspath(output_path)
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        if not os.path.isdir(output_path):
            raise ValueError("Output path should be a directory.")

        mount_path = posixpath.join(self.base_dir, "output")
        output_data_config = [
            OutputDataConfig(
                name="output",
                uri=output_path,
                mount_path=mount_path,
                data_path=mount_path,
            )
        ]
        # Estimator job requires channel name from inputs.
        input_data_configs = self._make_input_data_config(inputs)

        return input_data_configs, output_data_config

    def _prepare_volumes(
        self,
        input_data_configs: List[InputDataConfig],
        output_data_configs: List[OutputDataConfig],
    ) -> Dict[str, Any]:
        """Prepare input/output as docker volumes.

        Args:
            inputs: Input files for the job.
            output_path: Job output path.

        Returns:

        """

        volumes = {}
        for output in output_data_configs:
            volumes[output.uri] = {
                "bind": output.mount_path,
                "mode": "rw",
            }
        # Mount directory of the input source file to job container.
        for config in input_data_configs:
            volumes[config.uri] = {
                "bind": config.mount_path,
                "mode": "rw",
            }
        # Mount source code to /ml/code/:
        source_code = os.path.realpath(os.path.expanduser(self.source_code))
        if os.path.isdir(source_code):
            code_dir = source_code
        else:
            code_dir = os.path.dirname(source_code)
        volumes[code_dir] = {
            "bind": posixpath.join(self.base_dir, "code/"),
            "mode": "rw",
        }
        return volumes

    @classmethod
    def _transform_input_config(cls, inputs):
        # Estimator requires names of input to organize the directory structure of inputs.
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

            input_configs.append(
                InputDataConfig(
                    name=name,
                    dataset_id=None,
                    uri=None,
                    mount_path=None,
                    data_path=None,
                )
            )

        return input_configs

    def _make_command(
        self,
        input_data_configs: List[InputDataConfig],
    ):
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

        for name, value in self.hyperparameters.items():
            command.append("--{}".format(shlex.quote(name)))
            command.append(shlex.quote(str(value)))

        for input_config in input_data_configs:
            command.append("--{}".format(shlex.quote(input_config.name)))
            command.append(shlex.quote(shlex.quote(input_config.data_path)))
        return command

    def run(self, inputs, output_path=None):
        """

        Args:
            inputs:
            output_path:

        Returns:

        """
        import docker

        # if shutil.which("docker") is None:
        #     raise ValueError(
        #         "Program 'docker' is not found, could not run the job in local mode."
        #     )

        input_data_configs, output_data_configs = self._make_data_config(
            inputs, output_path
        )
        volumes = self._prepare_volumes(input_data_configs, output_data_configs)
        command = self._make_command(input_data_configs=input_data_configs)

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
