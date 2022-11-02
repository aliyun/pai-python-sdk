import typing
from typing import List, Optional

from pai.common.consts import WorkerType

if typing.TYPE_CHECKING:
    from pai.entity.job import JobSpec


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
        from pai.entity.job import JobSpec

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


class DataSourceConfig(object):
    """DataSource Configuration using in PAI DLC Job."""

    def __init__(self, dataset_id: str, mount_path: Optional[str] = None) -> None:
        self.dataset_id = dataset_id
        self.mount_path = mount_path

    def __str__(self):
        return "DataSourceConfig:dataset_id={0} mount_path={1}".format(
            self.dataset_id, self.mount_path
        )

    def __repr__(self):
        return self.__str__()


class CodeSourceConfig(object):
    """Job input config."""

    def __init__(self, code_source_id, branch=None, commit=None, mount_path=None):
        self.code_source_id = code_source_id
        self.branch = branch
        self.commit = commit
        self.mount_path = mount_path

    def __str__(self):
        return "CodeSourceConfig: id={0} mount_path={1}".format(
            self.code_source_id, self.mount_path
        )


class GitConfig(object):
    """Configuration represent a Git repository using in PAI DLC Job."""

    def __init__(self, repo, branch, user_name=None, access_token=None):
        self.repo = repo
        self.branch = branch
        self.user_name = user_name
        self.access_token = access_token
