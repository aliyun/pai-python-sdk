import functools
import logging
import os.path
import shlex
import time
from datetime import datetime
from typing import Callable, List, Optional, Union

import six
from six.moves.urllib import parse

from pai.common.consts import (
    DEFAULT_PAGE_SIZE,
    DEFAULT_WORKER_ECS_SPEC,
    DataSourceType,
    JobType,
    WorkerType,
)
from pai.common.oss_utils import (
    join_endpoint,
    parse_dataset_path,
    parse_oss_url,
    upload_to_oss,
)
from pai.common.utils import random_str, tar_file, to_abs_path
from pai.core import Session
from pai.decorator import config_default_session
from pai.entity.base import EntityBaseMixin
from pai.entity.common import CodeSourceConfig, DataSourceConfig
from pai.entity.dataset import Dataset
from pai.schema.job_schema import JobSchema, JobSpecSchema

logger = logging.getLogger(__name__)

_DEFAULT_JOB_WATCH_INTERVAL = 10

PAI_JOB_CONSOLE_URL_PATTERN = (
    "https://pai.console.aliyun.com/?regionId={0}&workspaceId={1}#/job/detail?jobId={2}"
)


class ResourceConfig(object):
    def __init__(self, cpu, memory, gpu=None, shared_memory=None, gpu_type=None):
        self.cpu = str(cpu)
        self.memory = self._append_memory_unit(memory=memory)
        self.gpu = str(gpu) if gpu else None
        self.shared_memory = self._append_memory_unit(memory=shared_memory)
        self.gpu_type = gpu_type

    @classmethod
    def _append_memory_unit(cls, memory):
        if not memory:
            return

        if isinstance(memory, six.string_types):
            memory = memory.strip()
            if memory.endswith("Gi"):
                return memory
        memory = int(memory)
        return "{}Gi".format(memory)


class JobSpec(object):
    def __init__(
        self,
        pod_count: int,
        image: Optional[str] = None,
        ecs_spec: Optional[str] = None,
        resource_config: Optional[ResourceConfig] = None,
        type: str = WorkerType.WORKER,
        use_spot_instance: bool = False,
    ) -> None:
        self.ecs_spec = ecs_spec
        self.type = type
        self.pod_count = pod_count
        self.resource_config = resource_config
        self.image = image
        self.use_spot_instance = use_spot_instance

    @classmethod
    def from_resource_config(
        cls,
        worker_cpu,
        worker_memory,
        worker_count,
        worker_image,
        worker_gpu=0,
        worker_shared_memory=None,
        ps_count=0,
        ps_cpu=None,
        ps_memory=None,
        ps_image=None,
        ps_gpu=None,
        ps_shared_memory=None,
    ):
        specs = []
        if worker_count > 0:
            worker_spec = JobSpec(
                pod_count=worker_count,
                type=WorkerType.WORKER,
                resource_config=ResourceConfig(
                    cpu=worker_cpu,
                    memory=worker_memory,
                    gpu=worker_gpu,
                    shared_memory=worker_shared_memory,
                ),
                image=worker_image,
            )
            specs.append(worker_spec)

        if ps_count > 0:
            ps_spec = JobSpec(
                pod_count=ps_count,
                type=WorkerType.PS,
                resource_config=ResourceConfig(
                    cpu=ps_cpu,
                    memory=ps_memory,
                    gpu=ps_gpu,
                    shared_memory=ps_shared_memory,
                ),
                image=ps_image,
            )
            specs.append(ps_spec)

        return specs

    @classmethod
    def from_instance_type(
        cls,
        worker_count=1,
        worker_instance_type=DEFAULT_WORKER_ECS_SPEC,
        worker_image=None,
        ps_image=None,
        ps_count=None,
        ps_instance_type=None,
        master_image=None,
        master_count=None,
        master_instance_type=None,
    ) -> List["JobSpec"]:
        job_specs = []
        if worker_count and worker_count > 0:
            job_specs.append(
                JobSpec(
                    ecs_spec=worker_instance_type,
                    type=WorkerType.WORKER,
                    pod_count=worker_count,
                    image=worker_image,
                ),
            )

        if ps_count:
            job_specs.append(
                JobSpec(
                    ecs_spec=ps_instance_type,
                    type=WorkerType.PS,
                    pod_count=ps_count,
                    image=ps_image,
                ),
            )

        if master_count:
            job_specs.append(
                JobSpec(
                    ecs_spec=master_instance_type,
                    type=WorkerType.MASTER,
                    pod_count=master_count,
                    image=master_image,
                )
            )

        return job_specs

    def to_api_object(self):
        return JobSpecSchema().dump(self)

    def to_dict(self):
        return self.to_api_object()


class JobStatus(object):
    """Represent PAI-DLC Job status"""

    Creating = "Creating"
    Queuing = "Queuing"
    Dequeued = "Dequeued"
    Running = "Running"
    Restarting = "Restarting"
    Succeeded = "Succeeded"
    Failed = "Failed"
    Stopping = "Stopping"
    Stopped = "Stopped"

    CompletedJobStatusList = [
        Succeeded,
        Failed,
        Stopped,
    ]
    ErrorJobStatusList = [
        Failed,
        Stopped,
    ]


def require_submitted(f: Callable) -> Callable:
    """Decorator on job method that requires job has been submitted."""

    @functools.wraps(f)
    def _(self, *args, **kwargs):
        if not self.id:
            raise ValueError("Job is not submitted.")

        return f(self, *args, **kwargs)

    return _


class JobPod(EntityBaseMixin):
    """Class that represent Job Pod."""

    def __init__(
        self,
        pod_id: str,
        status: str,
        type: str,
        pod_uid: Optional[str] = None,
        ip: Optional[str] = None,
        create_time: datetime = None,
        start_time: datetime = None,
        finish_time: datetime = None,
    ):
        super(JobPod, self).__init__()
        self.create_time = create_time
        self.finish_time = finish_time
        self.start_time = start_time
        self.ip = ip  # type: str
        self.pod_id = pod_id  # type: str
        self.pod_uid = pod_uid  # type: str
        self.status = status  # type: str
        self.type = type  # type: str

    @property
    def id(self):
        return self.pod_id

    def __repr__(self):
        return "Pod:type={} id={} status={}".format(self.type, self.id, self.status)


class Job(EntityBaseMixin):
    """PAI-DLC Job specs"""

    _schema_cls = JobSchema

    @config_default_session
    def __init__(
        self,
        user_command=None,
        display_name=None,
        description=None,
        envs=None,
        max_running_time_minutes=None,
        job_specs=None,
        job_type=JobType.TFJob,
        resource_id=None,
        priority=None,
        workspace_id=None,
        third_party_libs=None,
        third_party_lib_dir=None,
        data_sources: List[DataSourceConfig] = None,
        code_source: CodeSourceConfig = None,
        session=None,
        **kwargs,
    ):
        """Construct a Job.

        Args:
            user_command:
            display_name:
            description:
            envs:
            max_running_time_minutes:
            job_specs:
            job_type:
            resource_id:
            priority:
            workspace_id:
            third_party_libs:
            third_party_lib_dir:
            data_sources:
            code_source:
            **kwargs:
        """
        self.data_sources = data_sources or []
        self.code_source = code_source
        self.display_name = display_name
        self.envs = envs
        self.max_running_time_minutes = max_running_time_minutes
        self.job_specs = job_specs
        self.job_type = job_type
        self.resource_id = resource_id
        self.priority = priority
        self.user_command = (
            self._make_user_command(user_command)
            if isinstance(user_command, (list, tuple))
            else user_command
        )
        self.workspace_id = workspace_id
        self.third_party_libs = third_party_libs
        self.third_party_lib_dir = third_party_lib_dir
        self.description = description

        self._session = session

        # Read only fields from API response.
        self._job_id = kwargs.pop("job_id", None)
        self._create_time = kwargs.pop("create_time", None)
        self._status = kwargs.pop("status", None)
        self._reason_code = kwargs.pop("reason_code", None)
        self._reason_message = kwargs.pop("reason_message", None)
        self._pods = kwargs.pop("pods", None)

        # self.user_vpc = user_vpc
        # self.debug_config = debugger_config
        # self.elastic_spec = elastic_spec
        # self.job_settings = job_settings

    @property
    def id(self) -> str:
        return self._job_id

    def __str__(self):
        return self.__repr__()

    def __repr__(self) -> str:
        return "{}:{}".format(
            type(self).__name__, self.id if self.id else "<NotSubmitted>"
        )

    @classmethod
    def _make_user_command(cls, command_in_list):
        return " ".join([shlex.quote(cmd) for cmd in command_in_list])

    @property
    def create_time(self):
        """Create time of the job"""
        return self._create_time

    @property
    @require_submitted
    def status(self) -> str:
        """Status of the submitted job."""
        return self._status

    @property
    @require_submitted
    def reason_code(self):
        """Reason code for the job status."""
        return self._reason_code

    @property
    @require_submitted
    def reason_message(self):
        """Reason message for the job status."""
        return self._reason_message

    @property
    @require_submitted
    def pods(self):
        """Returns job pods."""
        return self._pods

    @property
    def job_apis(self):
        return self.session.job_api

    def run(self, wait=False):
        """Submit the DLC Job to run

        Args:
            wait:
        """
        job_id = self.job_apis.create(
            display_name=self.display_name,
            job_specs=self.job_specs,
            job_type=self.job_type,
            code_source_config=self.code_source,
            data_source_configs=self.data_sources,
            environment_variables=self.envs,
            max_running_time_minutes=self.max_running_time_minutes,
            resource_id=self.resource_id,
            priority=self.priority,
            thirdparty_lib_dir=self.third_party_lib_dir,
            thirdparty_libs=self.third_party_libs,
            user_command=self.user_command,
            # user_vpc=self.,
        )

        self.session.job_api.refresh_entity(entity=self, id_=job_id)

        print(
            "View the job detail by accessing the console URI: {}".format(
                self.console_uri
            )
        )
        if wait:
            self.wait_for_completion()

    @property
    def _job_apis(self):
        """Return JobAPI instance."""
        return self.session.job_api

    @require_submitted
    def wait_for_completion(self, interval=_DEFAULT_JOB_WATCH_INTERVAL):
        """Block until job completed."""
        while True:
            self.session.job_api.refresh_entity(self.id, self)
            if self.status in JobStatus.ErrorJobStatusList:
                raise RuntimeError(
                    "Job completed in error: id={} status={} reason_code={} reason_message={}".format(
                        self.id, self.status, self.reason_code, self.reason_message
                    )
                )
            elif self.status in JobStatus.CompletedJobStatusList:
                break
            time.sleep(interval)

    @property
    @require_submitted
    def console_uri(self):
        """Returns the dashboard uri of the resource."""
        return PAI_JOB_CONSOLE_URL_PATTERN.format(
            self.session.region_id, self.session.workspace.id, self._job_id
        )

    @require_submitted
    def stop(self):
        if not self.id:
            raise ValueError("Job is not submitted.")
        self._job_apis.stop(self.id)

    @require_submitted
    def list_events(self, start_time=None, end_time=None, max_events_num=2000):
        """Get Events of the DLC Job.

        Args:
            start_time: Start time of job events range.
            end_time: End time of job events range.
            max_events_num: Max event number return from the response.

        Returns:
            List[str]: List of job events.

        """

        return self._job_apis.list_events(
            self.id,
            start_time=start_time,
            end_time=end_time,
            max_events_num=max_events_num,
        )

    @require_submitted
    def list_pod_logs(
        self,
        pod_id,
        end_time=None,
        max_lines=None,
        pod_uid=None,
        start_time=None,
    ):
        """Get logs of a specific pod.

        Args:
            pod_id:
            end_time:
            max_lines:
            pod_uid:
            start_time:

        Returns:

        """
        return self._job_apis.list_pod_logs(
            job_id=self.id,
            pod_id=pod_id,
            end_time=end_time,
            max_lines=max_lines,
            pod_uid=pod_uid,
            start_time=start_time,
        )

    @classmethod
    @config_default_session
    def list(
        cls,
        display_name=None,
        start_time=None,
        end_time=None,
        resource_id=None,
        sort_by=None,
        order=None,
        status=None,
        tags=None,
        workspace_id=None,
        page_number=1,
        page_size=DEFAULT_PAGE_SIZE,
        session: Session = None,
    ) -> List["Job"]:
        result = session.job_api.list(
            display_name=display_name,
            start_time=start_time,
            end_time=end_time,
            resource_id=resource_id,
            sort_by=sort_by,
            order=order,
            status=status,
            tags=tags,
            workspace_id=workspace_id,
            page_number=page_number,
            page_size=page_size,
        )

        return [cls.from_api_object(obj, session=session) for obj in result.items]

    @classmethod
    @config_default_session
    def get(cls, id: str, session: Session = None) -> "Job":
        return cls.from_api_object(session.job_api.get(id), session=session)

    def delete(self) -> None:
        self.session.job_api.delete(self.id)

    @classmethod
    @config_default_session
    def from_script(
        cls,
        source_dir,
        entry_point,
        parameters=None,
        output_path=None,
        display_name=None,
        job_specs=None,
        envs=None,
        max_running_time_minutes=None,
        job_type: str = JobType.TFJob,
        resource_id: str = None,
        priority: int = None,
        third_party_libs=None,
        data_sources: List[Union[DataSourceConfig]] = None,
        session=None,
    ):
        job_name = display_name or cls.gen_script_job_name()
        data_source_for_code, upload_oss_url = cls._prepare_dataset_for_code(
            source_dir=source_dir,
            job_name=job_name,
            session=session,
        )
        data_sources = data_sources or []
        data_sources.append(data_source_for_code)
        if output_path:
            data_sources.append(cls._prepare_output_data_source(output_path, session))

        command = cls._build_script_job_command(
            entry_point=entry_point,
            oss_file_url=upload_oss_url,
            parameters=parameters,
            output_path=output_path,
        )

        job = cls(
            user_command=command,
            display_name=job_name,
            # description=d,
            envs=envs,
            max_running_time_minutes=max_running_time_minutes,
            job_specs=job_specs,
            job_type=job_type,
            resource_id=resource_id,
            priority=priority,
            third_party_libs=third_party_libs,
            data_sources=data_sources,
            session=session,
        )
        return job

    @classmethod
    def gen_script_job_name(cls):
        return "ScriptJob-{}".format(
            datetime.now().isoformat(sep="-", timespec="seconds")
        )

    @classmethod
    def _prepare_dataset_for_code(
        cls, source_dir: str, job_name: str, session: Session
    ):
        """Create dataset using for mount input code."""

        # tar the source files and upload to OSS bucket of the session.
        oss_file_url = upload_to_oss(
            source_path=tar_file(source_file=to_abs_path(source_dir)),
            oss_path="pai/dlc_job/{ts}/source.tar.gz".format(
                ts=datetime.now().isoformat(sep="-", timespec="milliseconds")
            ),
            oss_bucket=session.oss_bucket,
        )

        # Append endpoint to OSS URL.
        oss_file_url = join_endpoint(
            oss_file_url, parse.urlparse(session.oss_bucket.endpoint).hostname
        )

        # if source_file is tar.gz file in OSS, it should be mount
        # in {base_path}/mount/code and decompressed to {base_path}/code/
        mount_path = "/ml/mount/code"
        dataset = Dataset.upload(
            source=oss_file_url,
            name="tmp-sourcefile-{}".format(random_str(12)),
            mount_path=mount_path,
            data_source_type=DataSourceType.OSS,
        )
        return dataset.mount(mount_path=mount_path)

    @classmethod
    def _build_script_job_command(
        cls,
        entry_point,
        oss_file_url,
        base_dir="/ml",
        parameters=None,
        output_path=None,
    ):
        """Build command for script job."""

        # Prepare source code: decompress the mounted source code to working dir.
        work_dir = os.path.join(base_dir, "code")
        prepare_cmd = "mkdir -p {0} && cd {0} ".format(work_dir)
        parsed = parse_oss_url(oss_file_url)
        is_dir, dir_path, file_name = parse_dataset_path(parsed.object_key)
        source_file_path = os.path.join(base_dir, "mount", "code", file_name)
        prepare_cmd += " && tar -xvzf {0} -C {1} && ".format(
            source_file_path,
            work_dir,
        )

        # Generate arguments for the script.
        parameters = parameters or dict()
        args = []
        for name, v in parameters.items():
            args.append("--{}".format(shlex.quote(name)))
            args.append(shlex.quote(str(v)))
        if output_path:
            args.append("--output_path")
            args.append("/ml/output")

        if entry_point.endswith(".py"):
            exec_command = prepare_cmd + " ".join(["python", entry_point] + args)
        elif entry_point.endswith(".sh"):
            exec_command = prepare_cmd + " ".join(["bash", entry_point] + args)
        else:
            exec_command = prepare_cmd + " ".join([entry_point] + args)
        return exec_command

    @classmethod
    def _prepare_output_data_source(cls, output_path, session):
        parsed = parse_oss_url(output_path)
        uri = "oss://{bucket_name}.{endpoint}/{key}".format(
            bucket_name=parsed.bucket_name,
            endpoint=parsed.endpoint,
            key=parsed.object_key,
        )
        mount_path = "/ml/output/"
        dataset = Dataset.upload(
            source=uri,
            name="tmp-sourcefile-{}".format(random_str(12)),
            mount_path=mount_path,
            data_source_type=DataSourceType.OSS,
        )
        return dataset.mount(mount_path=mount_path)
