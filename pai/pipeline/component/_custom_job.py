import os
import shlex
from datetime import datetime
from typing import List

import oss2
import six
from oss2.exceptions import NotFound, ServerError
from six.moves.urllib import parse

from pai.code_source import GitConfig
from pai.common.consts import JobType, WorkerType
from pai.common.image_utils import retrieve_executor_image
from pai.common.utils import tar_file, to_abs_path
from pai.exception import PAIException
from pai.job import JobSpec
from pai.pipeline.component import ContainerComponent
from pai.pipeline.types import (
    ArtifactMetadataUtils,
    PipelineArtifact,
    PipelineParameter,
)
from pai.session import get_default_session


class JobConfig(object):
    """JobConfig represent resource, distribution, network config of PAI-DLC job."""

    def __init__(
        self,
        job_specs: List["JobSpec"],
        resource_id: str = None,
        user_vpc=None,
        priority: int = None,
        **kwargs,
    ):
        self.job_specs = job_specs
        self.resource_id = resource_id
        self.user_vpc = user_vpc
        self.priority = priority
        self.workspace_id = kwargs.get("workspace_id")

    def to_dict(self):
        d = {
            "JobSpecs": [worker.to_api_object() for worker in self.job_specs],
        }

        if self.resource_id is not None:
            d["ResourceId"] = self.resource_id
        if self.workspace_id is not None:
            d["WorkspaceId"] = self.workspace_id
        if self.priority is not None:
            d["Priority"] = self.priority
        if self.user_vpc is not None:
            d["UserVPC"] = self.user_vpc

        return d

    @classmethod
    def from_instance_type(
        cls,
        worker_count=None,
        worker_instance_type=None,
        ps_count=None,
        ps_instance_type=None,
        master_count=None,
        master_instance_type=None,
        resource_id=None,
        user_vpc=None,
        priority=None,
        **kwargs,
    ):
        """

        Args:
            worker_count:
            worker_instance_type:
            ps_count:
            ps_instance_type:
            master_count:
            master_instance_type:
            resource_id:
            user_vpc:
            priority:

        Returns:

        """
        from pai.job import JobSpec

        job_specs = []
        if worker_count:
            job_specs.append(
                JobSpec(
                    ecs_spec=worker_instance_type,
                    type=WorkerType.WORKER,
                    pod_count=worker_count,
                    # resource_config=worker_resource_config,
                )
            )
        if ps_count:
            job_specs.append(
                JobSpec(
                    ecs_spec=ps_instance_type,
                    type=WorkerType.PS,
                    pod_count=ps_count,
                    # resource_config=ps_resource_config,
                )
            )

        if master_count:
            job_specs.append(
                JobSpec(
                    ecs_spec=master_instance_type,
                    type=WorkerType.MASTER,
                    pod_count=master_count,
                    # resource_config=master_resource_config,
                )
            )

        if not job_specs:
            raise ValueError(
                "Please provide at least one of worker/ps/master for job config."
            )
        job_config = cls(
            job_specs=job_specs,
            resource_id=resource_id,
            user_vpc=user_vpc,
            priority=priority,
            **kwargs,
        )

        return job_config


class _CustomJobEnv(object):
    ENV_CUSTOM_JOB_MODE = "CUSTOM_JOB_MODE"
    ENV_CUSTOM_JOB_IMAGE_URI = "CUSTOM_JOB_IMAGE_URI"
    ENV_CUSTOM_JOB_TYPE = "CUSTOM_JOB_TYPE"
    ENV_CUSTOM_JOB_SOURCE_FILE = "CUSTOM_JOB_SOURCE_FILE"
    ENV_CUSTOM_JOB_ENTRY_POINT = "CUSTOM_JOB_ENTRY_POINT"
    ENV_CUSTOM_JOB_COMMAND = "CUSTOM_JOB_COMMAND"
    ENV_CUSTOM_JOB_ARGUMENTS = "CUSTOM_JOB_ARGUMENTS"
    ENV_CUSTOM_JOB_BASE_PATH = "CUSTOM_JOB_BASE_PATH"
    ENV_CUSTOM_JOB_WORK_DIR = "CUSTOM_JOB_WORK_DIR"
    ENV_CUSTOM_JOB_BASE_JOB_NAME = "CUSTOM_JOB_BASE_JOB_NAME"
    ENV_CUSTOM_JOB_RESOURCE_NO_DESTRUCTION = "CUSTOM_JOB_NO_DESTRUCTION"
    ENV_CUSTOM_JOB_OSS_ROLE_ARN = "CUSTOM_JOB_OSS_ROLE_ARN"
    ENV_CUSTOM_JOB_OSS_ALIYUN_UID = "CUSTOM_JOB_OSS_ALIYUN_UID"


class _DefaultOperatorParameters(object):
    JOB_CONFIG = "job_config"
    OUTPUT_PATH = "output_path"


class CustomJobComponent(ContainerComponent):
    """CustomJobOperator response for submit a custom job to PAI-DLC."""

    ExecutorType = "dlc-executor-v2"
    ExecutorVersion = "v1.0.4"

    def __init__(
        self,
        entry_point=None,
        command=None,
        image_uri=None,
        source_code=None,
        parameters=None,
        base_dir=None,
        work_dir=None,
        job_type=None,
        code_path=None,
        base_job_name=None,
        inputs=None,
        outputs=None,
    ):
        """Construct a CustomJobOperator instance.

        CustomJobOperator response for submit a CustomJob to PAI-DLC with specific image.

        Args:
            image_uri: Image uri for custom job.
            entry_point: Entrypoint for the job.
            source_code: Source code used by the job.
            parameters: Parameters for the job, it is passing to the job in
            base_dir: Base directory for custom job, job inputs and outputs will
            work_dir: Work directory for the job program.
            job_type: PAI-DLC job type, using TFJob as default.
            base_job_name: Base name used for generate the display name of the submitted PAI-DLC job.
        """

        self.job_image_uri = image_uri
        self.job_source_code = source_code
        self.job_entry_point = entry_point
        self.job_command = command
        self.job_parameters = parameters or dict()
        self.job_base_dir = base_dir or "/ml"
        self.job_work_dir = work_dir or os.path.join(self.job_base_dir, "code")
        self.job_type = job_type if job_type else JobType.TFJob
        self.job_code_path = code_path
        self.job_input_defs = inputs
        self.job_output_defs = outputs
        self.base_job_name = base_job_name or "custom_job_"
        self._session = get_default_session()

        self._source_file = self._prepare_source_files()

        env = self._gen_component_env(
            job_image_uri=self.job_image_uri,
            entry_point=self.job_entry_point,
            command=self.job_command,
            job_type=self.job_type,
            base_dir=self.job_base_dir,
            work_dir=self.job_work_dir,
            source_file=self.source_file,
        )

        # Image and command using in PAIFlow component spec.
        image_uri, command = self.get_executor_image_command(self._session.region_id)
        super().__init__(
            image_uri=image_uri,
            command=command,
            inputs=self._build_component_inputs(),
            outputs=outputs,
            env=env,
        )

        self._check()

    @property
    def source_file(self):
        """Uploaded source code url.

        Returns:
            str: A OSS URL which contains source code of the job.
        """
        return self._source_file

    def _check(self):
        """Check given parameters for the component."""
        if not self.job_image_uri:
            raise ValueError("Please provide image_uri for the job.")
        if not self.job_entry_point and not self.job_command:
            raise ValueError("Please provide either one of entry_point or command.")
        if self.job_type not in JobType.SUPPORTED_JOB_TYPEs:
            raise ValueError("No supported job type: %s", self.job_type)

        preset_params = set([p.name for p in self._get_default_parameters()])

        conflict_keys = [k for k in self.job_parameters.keys() if k in preset_params]
        if conflict_keys:
            raise ValueError(
                "Given parameter name conflict with preset parameters: %s",
                ",".join(conflict_keys),
            )

    def _prepare_source_files(self):
        """Prepare source code by uploading to OSS."""
        if not self.job_source_code:
            return

        # TODO: support GitConfig.
        if isinstance(self.job_source_code, GitConfig):
            raise NotImplementedError("Not supported.")

        if not isinstance(self.job_source_code, six.string_types):
            raise ValueError(
                "Unsupported source_files type, expected string or GitConfig, but given %s",
                type(self.job_source_code),
            )
        if self.job_source_code.startswith("oss://"):
            self._upload_source_files = self.job_source_code
        else:
            source_dir = to_abs_path(self.job_source_code)
            tar_result = tar_file(source_file=source_dir)

            if not self.job_code_path:
                code_path = ""
            elif not self.job_code_path.endswith("/"):
                code_path = self.job_code_path + "/"
            else:
                code_path = self.job_code_path

            object_key = "{code_path}pai/custom_job/{date}/source.tar.gz".format(
                code_path=code_path,
                date=datetime.now().strftime("%Y%m%d-%H:%M:%S"),
            )
            self._upload_source_files = self._put_source_if_not_exists(
                src=tar_result, object_key=object_key
            )

        return self._upload_source_files

    def _put_source_if_not_exists(self, src, object_key):
        """Upload source files to OSS."""
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

        # endpoint of OSS bucket contains HTTP schema.
        endpoint = parse.urlparse(oss_bucket.endpoint).hostname
        oss_url = "oss://{bucket_name}.{endpoint}/{oss_key}".format(
            bucket_name=oss_bucket.bucket_name,
            oss_key=object_key,
            endpoint=endpoint,
        )
        return oss_url

    def _build_component_inputs(self, inputs=None):
        """Update component input definitions with actual inputs."""
        parameters = self._gen_parameters()
        input_defs = self.job_input_defs or []
        input_defs = parameters + input_defs

        if not inputs:
            return input_defs
        input_names = set([item.name for item in input_defs])
        # TODO(LiangQuan): support MaxComputeTable input in uri format.
        for name, value in inputs.items():
            if name in input_names:
                continue
            input_defs.append(
                PipelineArtifact(
                    name=name,
                    metadata=ArtifactMetadataUtils.oss_dataset(),
                )
            )
        return input_defs

    def _config_component_inputs(self, inputs=None):
        """Config the component input definitions with given inputs."""
        from pai.pipeline.types.spec import InputsSpec

        input_defs = self._build_component_inputs(inputs=inputs)
        self._inputs = InputsSpec(input_defs)

    def run(
        self, inputs=None, job_name=None, job_config=None, output_path=None, **kwargs
    ):
        """

        Args:
            inputs:
            job_name:
            job_config:
            output_path:
            **kwargs:

        Returns:

        """
        self._config_component_inputs(inputs)
        args = self._get_run_arguments(
            inputs=inputs, output_path=output_path, job_config=job_config
        )
        return super(CustomJobComponent, self).run(
            job_name=job_name, arguments=args, **kwargs
        )

    def _get_run_arguments(self, inputs, job_config, output_path=None):

        arguments = self.job_parameters.copy()
        if inputs:
            arguments.update(inputs)
        if not job_config:
            raise ValueError("JobConfig is required to submit a job.")

        arguments.update(
            {
                _DefaultOperatorParameters.JOB_CONFIG: job_config.to_dict()
                if isinstance(job_config, JobConfig)
                else job_config
            }
        )

        if output_path:
            arguments.update(
                {
                    _DefaultOperatorParameters.OUTPUT_PATH: output_path,
                }
            )
        return arguments

    @classmethod
    def _gen_component_env(
        cls,
        job_image_uri,
        job_type,
        entry_point=None,
        command=None,
        base_dir=None,
        work_dir=None,
        source_file=None,
    ):
        env = {
            _CustomJobEnv.ENV_CUSTOM_JOB_MODE: "1",
            _CustomJobEnv.ENV_CUSTOM_JOB_IMAGE_URI: job_image_uri,
            _CustomJobEnv.ENV_CUSTOM_JOB_ENTRY_POINT: entry_point,
            _CustomJobEnv.ENV_CUSTOM_JOB_TYPE: job_type.value
            if isinstance(job_type, JobType)
            else job_type,
            _CustomJobEnv.ENV_CUSTOM_JOB_BASE_PATH: base_dir or "/ml",
            _CustomJobEnv.ENV_CUSTOM_JOB_WORK_DIR: work_dir or "/ml/code",
        }

        if command:

            if isinstance(command, (list, tuple)):
                command = " ".join([shlex.quote(c) for c in command])
            env.update(
                {
                    _CustomJobEnv.ENV_CUSTOM_JOB_COMMAND: command,
                }
            )
        elif entry_point:
            env.update(
                {
                    _CustomJobEnv.ENV_CUSTOM_JOB_ENTRY_POINT: entry_point,
                }
            )
        else:
            raise ValueError("Please provide either one of entry_point and command.")

        if source_file:
            env.update({_CustomJobEnv.ENV_CUSTOM_JOB_SOURCE_FILE: source_file})

        sess = get_default_session()
        if sess.is_inner:
            env.update(
                {
                    _CustomJobEnv.ENV_CUSTOM_JOB_OSS_ROLE_ARN: sess._oss_role_arn,
                    _CustomJobEnv.ENV_CUSTOM_JOB_OSS_ALIYUN_UID: sess._oss_aliyun_uid,
                }
            )

        return env

    @classmethod
    def _get_default_parameters(cls):
        params = [
            PipelineParameter(
                name=_DefaultOperatorParameters.JOB_CONFIG,
                typ=dict,
                desc="PAI-DLC job config, including worker spec, resource spec, etc.",
            ),
            PipelineParameter(
                name=_DefaultOperatorParameters.OUTPUT_PATH,
                typ=str,
                default="",
                desc="Job output path, could be OSS url or NAS url.",
            ),
        ]
        return params

    def _gen_parameters(self):
        params = self._get_default_parameters()
        for pname, pvalue in self.job_parameters.items():
            param = PipelineParameter(
                name=pname,
                typ=type(pvalue),
                default=pvalue,
            )

            params.append(param)

        return params

    @classmethod
    def get_executor_image_command(cls, region_id):
        """Get CustomJobExecutor image and command for the executor."""
        image_uri = retrieve_executor_image(
            region_id=region_id,
            version=cls.ExecutorVersion,
            executor_type=cls.ExecutorType,
        )

        command = [
            "python",
            "-um",
            "pai_running.cmd.custom_job_submit",
        ]
        return image_uri, command
