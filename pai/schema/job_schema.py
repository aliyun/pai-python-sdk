from marshmallow import EXCLUDE, fields, post_load, validate

from pai.common.consts import JobType

from .base import BaseAPIResourceSchema


class JobResourceConfigSchema(BaseAPIResourceSchema):
    """Schema for PAI DLC Job resource config"""

    FieldNameMapping = {
        "CPU": "cpu",
        "GPU": "gpu",
        "GPUType": "gpu_type",
        "Memory": "memory",
    }

    class Meta(object):
        unknown = EXCLUDE

    cpu = fields.Str()
    memory = fields.Str()
    gpu = fields.Str()
    gpu_type = fields.Str()
    shared_memory = fields.Str()

    @post_load
    def _make(self, data, **kwargs):
        from ..entity.job import ResourceConfig

        return ResourceConfig(**data)


class JobSpecSchema(BaseAPIResourceSchema):
    """Schema for DLC Job Spec."""

    class Meta(object):
        unknown = EXCLUDE

    pod_count = fields.Int()
    use_spot_instance = fields.Bool()
    ecs_spec = fields.Str()
    image = fields.Str()
    type = fields.Str()
    resource_config = fields.Nested(JobResourceConfigSchema)

    @post_load
    def _make(self, data, **kwargs):
        from ..entity.job import JobSpec

        return JobSpec(**data)


class JobDataSourceSchema(BaseAPIResourceSchema):
    """Input data config schema of DLC job."""

    dataset_id = fields.Str(required=True)
    mount_path = fields.Str()

    FieldNameMapping = {
        "DataSourceId": "dataset_id",
    }

    @post_load
    def _make(self, data, **kwargs):
        from ..entity.common import DataSourceConfig

        return DataSourceConfig(**data)


class JobCodeSourceSchema(BaseAPIResourceSchema):
    """Input code config schema of DLC job."""

    code_source_id = fields.Str(required=True)
    mount_path = fields.Str()
    branch = fields.Str()
    commit = fields.Str()

    @post_load
    def _make(self, data, **kwargs):
        from ..entity.common import CodeSourceConfig

        # Backend Service may return CodeSource struct with empty code_source_id.
        if data.get("code_source_id"):
            return CodeSourceConfig(**data)


class JobPodSchema(BaseAPIResourceSchema):
    """Schema of DlcJob Pod."""

    class Meta(object):
        unknown = EXCLUDE

    FieldNameMapping = {
        "GmtCreateTime": "create_time",
        "GmtStartTime": "start_time",
        "GmtFinishTime": "finish_time",
    }

    create_time = fields.DateTime()
    start_time = fields.DateTime()
    finish_time = fields.DateTime()
    pod_id = fields.Str()
    pod_uid = fields.Str()
    status = fields.Str()
    type = fields.Str()
    ip = fields.Str()

    @post_load()
    def _make(self, data, **kwargs):
        from pai.entity.job import JobPod

        return JobPod(**data)


class JobSchema(BaseAPIResourceSchema):
    """Schema of DLC job."""

    display_name = fields.Str()
    job_type = fields.Str(
        default=JobType.TFJob,
        validate=validate.OneOf(
            [JobType.TFJob, JobType.XGBoostJob, JobType.MPIJob, JobType.PyTorchJob]
        ),
    )
    workspace_id = fields.Str()
    job_specs = fields.List(fields.Nested(JobSpecSchema), required=True)
    data_sources = fields.List(fields.Nested(JobDataSourceSchema))
    code_source = fields.Nested(JobCodeSourceSchema)
    third_party_lib_dir = fields.Str()
    third_party_libs = fields.List(fields.Str)
    user_command = fields.Str(required=True)
    max_running_time_minutes = fields.Int()
    resource_id = fields.Str()

    # Load only fields
    job_id = fields.Str(load_only=True)
    status = fields.Str(load_only=True)
    create_time = fields.DateTime(load_only=True)
    reason_code = fields.Str(load_only=True)
    reason_message = fields.Str(load_only=True)
    pods = fields.List(fields.Nested(JobPodSchema), load_only=True)

    FieldNameMapping = {
        "ThirdpartyLibs": "third_party_libs",
        "ThirdpartyLibDir": "third_party_lib_dir",
        "JobMaxRunningTimeMiniutes": "max_running_time_miniutes",
        "GmtCreateTime": "create_time",
    }

    @post_load
    def _make(self, data, **kwargs):
        from pai.entity.job import Job

        return self.make_or_reload(Job, data=data)
