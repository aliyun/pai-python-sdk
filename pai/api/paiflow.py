from __future__ import absolute_import

from functools import wraps

import six

from pai.common.yaml_utils import dump as yaml_dump
from pai.api.base import BaseTeaClient
from pai.libs.alibabacloud_paiflow20210202.client import Client
from pai.libs.alibabacloud_paiflow20210202.models import (
    GetNodeRequest,
    CreatePipelineRequest,
    CreateRunRequest,
    ListPipelinesRequest,
    ListRunsRequest,
    ListNodeLogsRequest,
    ListNodeOutputsRequest,
    UpdatePipelineRequest,
    UpdateRunRequest,
    UpdatePipelinePrivilegesRequest,
)


def require_workspace(f):
    @wraps(f)
    def _(self, *args, **kwargs):
        if not kwargs.get("workspace_id", None) and self.is_workspace_required:
            raise ValueError("Please provide WorkspaceId")

        return f(self, *args, **kwargs)

    return _


class PAIFlowClient(BaseTeaClient):
    _ENV_SERVICE_ENDPOINT_KEY = "PAI_PAIFLOW_SERVICE_ENDPOINT"

    _PRODUCT_NAME = "paiflow"

    def __init__(
        self, access_key_id, access_key_secret, region_id=None, endpoint=None, **kwargs
    ):
        """Class to wrap APIs provided by PaiFlow pipeline service.

        Args:
            base_client (pai.libs.alibabacloud_paiflow20210202.client.Client):
        """
        super(PAIFlowClient, self).__init__(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            region_id=region_id,
            client_cls=Client,
            endpoint=endpoint,
        )
        self.base_client = Client(config=self.build_client_config(**kwargs))

    def get_pipeline_schema(self, pipeline_id):
        resp = self._call_service_with_exception(
            self.base_client.get_pipeline_schema_with_options,
            pipeline_id=pipeline_id,
            headers=self._get_headers(),
            runtime=self._get_runtime(),
        )
        return resp.to_map()

    def list_pipeline(
        self,
        identifier=None,
        provider=None,
        workspace_id=None,
        version=None,
        page_number=None,
        page_size=None,
    ):
        request = ListPipelinesRequest(
            page_number=page_number,
            page_size=page_size,
            pipeline_provider=provider,
            pipeline_version=version,
            pipeline_identifier=identifier,
            workspace_id=workspace_id,
        )

        resp = self._call_service_with_exception(
            self.base_client.list_pipelines_with_options,
            request=request,
            headers=self._get_headers(),
            runtime=self._get_runtime(),
        ).to_map()
        total_count, pipelines = resp["TotalCount"], resp["Pipelines"]
        return pipelines, total_count

    def list_pipeline_generator(self, **kwargs):
        return type(self).to_generator(self.list_pipeline)(**kwargs)

    def create_pipeline(self, manifest, workspace_id=None):
        request = CreatePipelineRequest(manifest=manifest, workspace_id=workspace_id)
        resp = self._call_service_with_exception(
            self.base_client.create_pipeline_with_options,
            request=request,
            headers=self._get_headers(),
            runtime=self._get_runtime(),
        )
        return resp.pipeline_id

    def delete_pipeline(self, pipeline_id):
        self._call_service_with_exception(
            self.base_client.delete_pipeline_with_options,
            pipeline_id=pipeline_id,
            headers=self._get_headers(),
            runtime=self._get_runtime(),
        )
        return

    def update_pipeline(self, pipeline_id, manifest):
        request = UpdatePipelineRequest(
            manifest=manifest,
        )
        self._call_service_with_exception(
            self.base_client.update_pipeline_with_options,
            pipeline_id=pipeline_id,
            request=request,
            headers=self._get_headers(),
            runtime=self._get_runtime(),
        )
        return

    def get_pipeline(self, pipeline_id):
        resp = self._call_service_with_exception(
            self.base_client.get_pipeline_with_options,
            pipeline_id=pipeline_id,
            headers=self._get_headers(),
            runtime=self._get_runtime(),
        )
        return resp.to_map()

    def update_pipeline_privilege(self, pipeline_id, user_ids):
        if isinstance(user_ids, six.string_types):
            user_ids = user_ids.split(",")
        if not isinstance(user_ids, (list, tuple)):
            raise ValueError("Please provide user_ids as list or tuple")
        request = UpdatePipelinePrivilegesRequest(users=user_ids)
        self._call_service_with_exception(
            self.base_client.update_pipeline_privileges_with_options,
            pipeline_id=pipeline_id,
            request=request,
            headers=self._get_headers(),
            runtime=self._get_runtime(),
        )
        return

    def list_pipeline_privilege(self, pipeline_id):
        resp = self._call_service_with_exception(
            self.base_client.list_pipeline_privileges_with_options,
            pipeline_id=pipeline_id,
            headers=self._get_headers(),
            runtime=self._get_runtime(),
        )
        return resp.to_map()

    def create_run(
        self,
        name,
        arguments,
        pipeline_id=None,
        manifest=None,
        no_confirm_required=False,
        workspace_id=None,
        source="SDK",
    ):

        if not pipeline_id and not manifest:
            raise ValueError(
                "Create pipeline run require either pipeline_id or manifest."
            )
        if pipeline_id and manifest:
            raise ValueError(
                "Both pipeline_id and manifest are provide, create_run need only one."
            )
        if not name:
            raise ValueError("Pipeline run instance need a name.")

        if isinstance(arguments, dict):
            arguments = yaml_dump(arguments)

        request = CreateRunRequest(
            pipeline_id=pipeline_id,
            name=name,
            pipeline_manifest=manifest,
            arguments=arguments,
            no_confirm_required=no_confirm_required,
            workspace_id=workspace_id,
            source=source,
        )
        resp = self._call_service_with_exception(
            self.base_client.create_run_with_options,
            request=request,
            headers=self._get_headers(),
            runtime=self._get_runtime(),
        )
        return resp.run_id

    def list_run(
        self,
        name=None,
        run_id=None,
        pipeline_id=None,
        status=None,
        sort_by=None,
        order=None,
        workspace_id=None,
        page_number=None,
        page_size=None,
        experiment_id=None,
        source=None,
    ):
        request = ListRunsRequest(
            page_number=page_number,
            page_size=page_size,
            experiment_id=experiment_id,
            name=name,
            pipeline_id=pipeline_id,
            run_id=run_id,
            sort_by=sort_by,
            order=order,
            source=source,
            status=status,
            workspace_id=workspace_id,
        )
        resp = self._call_service_with_exception(
            self.base_client.list_runs_with_options,
            request=request,
            headers=self._get_headers(),
            runtime=self._get_runtime(),
        ).to_map()
        runs, total_count = resp["Runs"], resp["TotalCount"]
        return runs, total_count

    def list_run_generator(self, **kwargs):
        return type(self).to_generator(self.list_run)(**kwargs)

    def get_run(self, run_id):
        resp = self._call_service_with_exception(
            self.base_client.get_run_with_options,
            run_id=run_id,
            headers=self._get_headers(),
            runtime=self._get_runtime(),
        )
        return resp.to_map()

    def start_run(self, run_id):
        self._call_service_with_exception(
            self.base_client.start_run_with_options,
            run_id=run_id,
            headers=self._get_headers(),
            runtime=self._get_runtime(),
        )
        return

    def terminate_run(self, run_id):
        self._call_service_with_exception(
            self.base_client.terminate_run_with_options,
            run_id=run_id,
            headers=self._get_headers(),
            runtime=self._get_runtime(),
        )
        return

    def update_run(self, run_id, name):
        request = UpdateRunRequest(name=name)
        self._call_service_with_exception(
            self.base_client.update_run_with_options,
            run_id=run_id,
            request=request,
            headers=self._get_headers(),
            runtime=self._get_runtime(),
        )
        return

    def get_node(self, run_id, node_id, depth=2):
        request = GetNodeRequest(depth=depth)
        resp = self._call_service_with_exception(
            self.base_client.get_node_with_options,
            run_id=run_id,
            node_id=node_id,
            request=request,
            headers=self._get_headers(),
            runtime=self._get_runtime(),
        )
        return resp.to_map()

    def list_node_logs(
        self,
        run_id,
        node_id,
        from_time=None,
        to_time=None,
        keyword=None,
        reverse=False,
        page_offset=0,
        page_size=100,
    ):
        request = ListNodeLogsRequest(
            offset=page_offset,
            page_size=page_size,
            from_time_in_seconds=from_time,
            to_time_in_seconds=to_time,
            keyword=keyword,
            reverse=reverse,
        )

        resp = self._call_service_with_exception(
            self.base_client.list_node_logs_with_options,
            run_id=run_id,
            node_id=node_id,
            request=request,
            headers=self._get_headers(),
            runtime=self._get_runtime(),
        ).to_map()

        logs, total_count = resp["Logs"], resp["TotalCount"]
        return logs, total_count

    def list_node_logs_generator(self, **kwargs):
        def f(**kwargs):
            page_offset = kwargs.pop("page_offset", 0)
            page_size = kwargs.pop("page_size", 1)

            while True:
                entities, _ = self.list_node_logs(
                    page_offset=page_offset, page_size=page_size, **kwargs
                )
                if not entities:
                    return
                for entity in entities:
                    yield entity
                page_offset = page_size + page_offset

        return f(**kwargs)

    def list_node_outputs(
        self,
        run_id,
        node_id,
        depth=2,
        name=None,
        sort_by=None,
        order=None,
        type=None,
        page_number=1,
        page_size=50,
    ):
        request = ListNodeOutputsRequest(
            name=name,
            depth=depth,
            page_number=page_number,
            page_size=page_size,
            sort_by=sort_by,
            order=order,
            type=type,
        )

        resp = self._call_service_with_exception(
            self.base_client.list_node_outputs_with_options,
            run_id=run_id,
            node_id=node_id,
            request=request,
            headers=self._get_headers(),
            runtime=self._get_runtime(),
        ).to_map()

        outputs, total_count = resp["Outputs"], resp["TotalCount"]
        return outputs, total_count

    def list_node_outputs_generator(self, **kwargs):
        return type(self).to_generator(self.list_node_outputs)(**kwargs)

    def get_caller_provider(self):
        resp = self._call_service_with_exception(
            self.base_client.get_caller_provider_with_options,
            headers=self._get_headers(),
            runtime=self._get_runtime(),
        )
        return resp.provider
