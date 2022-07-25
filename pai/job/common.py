from enum import Enum


class JobType(str, Enum):
    TFJob = "TFJob"
    PyTorchJob = "PyTorchJob"
    XGBoostJob = "XGBoostJob"
    MPIJob = "MPIJob"


class GitConfig(object):
    def __init__(self, repo, branch, user_name=None, access_token=None):
        self.repo = repo
        self.branch = branch
        self.user_name = user_name
        self.access_token = access_token


class WorkerType(str, Enum):
    """Supported worker types in PAI-DLC."""

    PS = "PS"
    WORKER = "Worker"
    MASTER = "Master"
    EVALUATOR = "Evaluator"


class JobSpec(object):
    def __init__(
        self, type, count, instance_type=None, resource_config=None, image_uri=None
    ):
        self.type = type
        self.count = count
        self.instance_type = instance_type
        self.resource_config = resource_config
        self.image_uri = image_uri

    def to_dict(self):

        d = {
            "Type": self.type.value if isinstance(self.type, WorkerType) else self.type,
            "PodCount": self.count,
            "EcsSpec": self.instance_type,
            "ImageUri": self.image_uri,
        }
        return d


class JobConfig(object):
    """JobConfig represent resource, distribution, network config of PAI-DLC job."""

    def __init__(
        self, job_specs, resource_id=None, user_vpc=None, priority=None, **kwargs
    ):
        self.job_specs = job_specs
        self.resource_id = resource_id
        self.user_vpc = user_vpc
        self.priority = priority
        self.workspace_id = kwargs.get("workspace_id")

    def to_dict(self):
        d = {
            "JobSpecs": [worker.to_dict() for worker in self.job_specs],
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
    def create(
        cls,
        worker_count=None,
        worker_instance_type=None,
        # worker_resource_config=None,
        ps_count=None,
        ps_instance_type=None,
        # ps_resource_config=None,
        master_count=None,
        master_instance_type=None,
        # master_resource_config=None,
        resource_id=None,
        user_vpc=None,
        priority=None,
        workspace_id=None,
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
        job_specs = []
        if worker_count:
            job_specs.append(
                JobSpec(
                    instance_type=worker_instance_type,
                    type=WorkerType.WORKER,
                    count=worker_count,
                    # resource_config=worker_resource_config,
                )
            )
        if ps_count:
            job_specs.append(
                JobSpec(
                    instance_type=ps_instance_type,
                    type=WorkerType.PS,
                    count=ps_count,
                    # resource_config=ps_resource_config,
                )
            )

        if master_count:
            job_specs.append(
                JobSpec(
                    instance_type=master_instance_type,
                    type=WorkerType.MASTER,
                    count=master_count,
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
            workspace_id=workspace_id,
        )

        return job_config
