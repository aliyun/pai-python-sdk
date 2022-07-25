from __future__ import absolute_import

from pai.api.base import BaseTeaClient
from pai.libs.alibabacloud_pai_dlc20201203.client import Client
from pai.libs.alibabacloud_pai_dlc20201203.models import (
    CreateDataSourceRequest,
    CreateCodeSourceRequest,
    CreateJobRequest,
    CreateJobRequestCodeSource,
    CreateJobRequestDataSources,
    JobSpec,
)


class DlcClient(BaseTeaClient):
    _ENV_SERVICE_ENDPOINT_KEY = "PAI_DLC_SERVICE_ENDPOINT"
    _PRODUCT_NAME = "pai-dlc"

    def __init__(self, access_key_id, access_key_secret, region_id=None, endpoint=None):
        super(DlcClient, self).__init__(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            region_id=region_id,
            client_cls=Client,
            endpoint=endpoint,
        )
        self.base_client = Client(config=self.build_client_config())  # type: Client

    @classmethod
    def _construct_endpoint_by_region(cls, region_id):
        """Construct Product endpoint with given region_id"""
        if region_id == cls._inner_region_id:
            return "{}-share.aliyuncs.com".format(cls._PRODUCT_NAME)
        return "{}.{}.aliyuncs.com".format(cls._PRODUCT_NAME.lower(), region_id)

    def create_data_source(
        self,
        name,
        data_source_type,
        path,
        mount_path,
        endpoint=None,
        file_system_id=None,
        is_proxy=None,
        options=None,
        description=None,
    ):
        request = CreateDataSourceRequest(
            data_source_type=data_source_type.lower(),
            description=description,
            display_name=name,
            endpoint=endpoint,
            file_system_id=file_system_id,
            is_proxy=is_proxy,
            mount_path=mount_path,
            options=options,
            path=path,
        )

        resp_body = self._call_service_with_exception(
            self.base_client.create_data_source, request=request
        )
        return resp_body.data_source_id

    def delete_data_source(self, data_source_id):
        self._call_service_with_exception(
            self.base_client.delete_data_source, data_source_id=data_source_id
        )

    def create_code_source(
        self,
        code_repo,
        name,
        code_branch=None,
        code_repo_access_token=None,
        code_repo_user_name=None,
        description=None,
        mount_path=None,
    ):
        request = CreateCodeSourceRequest(
            code_repo=code_repo,
            code_branch=code_branch,
            code_repo_access_token=code_repo_access_token,
            code_repo_user_name=code_repo_user_name,
            description=description,
            display_name=name,
            mount_path=mount_path,
        )
        resp_body = self._call_service_with_exception(
            self.base_client.create_code_source, request=request
        )
        return resp_body.code_source_id

    def delete_code_source(self, code_source_id):
        self._call_service_with_exception(
            self.base_client.delete_code_source, code_source_id=code_source_id
        )

    @classmethod
    def to_job_spec_item(cls, item):
        from pai.job.common import JobSpec as WorkerSpec

        if isinstance(item, JobSpec):
            return item
        elif isinstance(item, dict):
            return JobSpec().from_map(item)
        elif isinstance(item, WorkerSpec):
            return JobSpec(
                type=item.type,
                pod_count=item.count,
                ecs_spec=item.instance_type,
                image=item.image_uri,
            )
        else:
            raise ValueError("Not supported job spec type: %s" % type(item))

    def create_job(
        self,
        name,
        user_command,
        job_type,
        worker_specs,
        workspace_id=None,
        code_source_id=None,
        data_source_ids=None,
        envs=None,
        priority=None,
        job_max_running_time_minutes=None,
        resource_id=None,
        thirdparty_lib_dir=None,
        thirdparty_libs=None,
        user_vpc=None,
    ):

        code_source = (
            CreateJobRequestCodeSource(code_source_id=code_source_id)
            if code_source_id
            else None
        )
        data_sources = (
            [CreateJobRequestDataSources(data_source_id=_id) for _id in data_source_ids]
            if data_source_ids
            else None
        )

        if not isinstance(worker_specs, (tuple, list)):
            raise ValueError(
                "job_specs type error: expected list but given %s" % type(worker_specs)
            )

        worker_specs = [self.to_job_spec_item(j) for j in worker_specs]

        request = CreateJobRequest(
            code_source=code_source,
            data_sources=data_sources,
            display_name=name,
            envs=envs,
            job_specs=worker_specs,
            job_type=job_type,
            priority=priority,
            resource_id=resource_id,
            job_max_running_time_minutes=job_max_running_time_minutes,
            thirdparty_lib_dir=thirdparty_lib_dir,
            thirdparty_libs=thirdparty_libs,
            user_command=user_command,
            user_vpc=user_vpc,
            workspace_id=workspace_id,
            debugger_config_content=None,
            elastic_spec=None,
            settings=None,
        )

        resp_body = self._call_service_with_exception(
            self.base_client.create_job, request=request
        )
        return resp_body.job_id

    def get_job(self, job_id):
        """Get Job resource with the job id."""
        resp_body = self._call_service_with_exception(
            self.base_client.get_job, job_id=job_id
        )
        return resp_body.to_map()
