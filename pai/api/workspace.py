from __future__ import absolute_import

import json
from alibabacloud_tea_util import models as util_models

from pai.api.base import BaseTeaClient
from pai.api.common import DataType, DatasetSourceType
from pai.libs.alibabacloud_aiworkspace20210204.client import Client
from pai.libs.alibabacloud_aiworkspace20210204.models import (
    ListWorkspacesRequest,
    CreateWorkspaceRequest,
    GetWorkspaceRequest,
    ListFeaturesRequest,
    CreateDatasetRequest,
    DatasetLabel,
    CreateCodeSourceRequest,
)


class WorkspaceClient(BaseTeaClient):
    _ENV_SERVICE_ENDPOINT_KEY = "PAI_AIWORKSPACE_SERVICE_ENDPOINT"
    _PRODUCT_NAME = "aiworkspace"

    def __init__(self, access_key_id, access_key_secret, region_id=None, endpoint=None):
        super(WorkspaceClient, self).__init__(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            region_id=region_id,
            client_cls=Client,
            endpoint=endpoint,
        )
        self.base_client = Client(config=self.build_client_config())

    @classmethod
    def _get_default_request_header_runtime(cls):
        """Returns default (header, runtime) tuple for POP SDK API.

        Returns:
            A (header, runtime) tuple.
        """
        runtime = util_models.RuntimeOptions()
        headers = {}

        return headers, runtime

    def list_workspace(
        self,
        page_number=None,
        page_size=None,
        sort_by=None,
        order=None,
        workspace_name=None,
        module_list=None,
        status=None,
        option=None,
        verbose=None,
    ):
        request = ListWorkspacesRequest(
            page_number=page_number,
            page_size=page_size,
            sort_by=sort_by,
            order=order,
            workspace_name=workspace_name,
            module_list=module_list,
            status=status,
            option=option,
            verbose=verbose,
        )

        resp = self._call_service_with_exception(
            self.base_client.list_workspaces, request=request
        ).to_map()

        workspaces, total_count = resp["Workspaces"], resp["TotalCount"]
        return workspaces, total_count

    def list_workspace_generator(
        self,
        page_number=None,
        page_size=None,
        sort_by=None,
        order=None,
        workspace_name=None,
        module_list=None,
        status=None,
        option=None,
        verbose=None,
    ):
        return type(self).to_generator(self.list_workspace)(
            page_number=page_number,
            page_size=page_size,
            sort_by=sort_by,
            order=order,
            workspace_name=workspace_name,
            module_list=module_list,
            status=status,
            option=option,
            verbose=verbose,
        )

    def create(self, name, display_name=None, description=None, env_types=None):
        request = CreateWorkspaceRequest(
            workspace_name=name,
            description=description,
            display_name=display_name,
            env_types=None,
        )

        resp = self._call_service_with_exception(
            self.base_client.create_workspace, request=request
        )
        return resp.to_map()

    def get_workspace(self, workspace_id, verbose=False):
        resp = self.base_client.get_workspace(
            workspace_id, request=GetWorkspaceRequest(verbose=verbose)
        )
        return resp.body.to_map()

    def list_feature(self, names=None):
        if isinstance(names, (list, tuple)):
            names = ",".join(names)
        resp = self._call_service_with_exception(
            self.base_client.list_features,
            request=ListFeaturesRequest(
                names=names,
            ),
        )
        return resp.features

    def create_dataset(
        self,
        name,
        data_source_type,
        property,
        workspace_id,
        uri,
        data_type=None,
        accessibility=None,
        description=None,
        labels=None,
        options=None,
        source_id=None,
        source_type=None,
    ):
        """Create Dataset resource, return dataset_id.

        Args:
            name (str): Name for the dataset.
            data_source_type (str): Storage used by the dataset, could be NAS, OSS, etc.
            property (str): Dataset file property, could be File, Directory, or Tabular.
            workspace_id (str): Workspace the created dataset belongs to.
            uri (str): URI where the dataset is stored, it can be NAS URI or OSS URI.
            data_type (str): Type of the dataset, could be PIC, TEXT, VIDEO, AUDIO, or COMMON.
            accessibility (str): Accessibility property of the dataset for users in Workspace, could be PRIVATE or PUBLIC.
            description (str): Description of the dataset.
            labels (dict): Labels on the dataset.
            options (str or dict): Config for mount, such as mount path, mount options, etc.
            source_type (str): Source of the dataset, it can be USER, ITAG, or PAI_PUBLIC_DATASET.
            source_id (str): Identifier of the source.

        Returns:
            str: dataset_id of the created dataset.

        """
        data_type = data_type or DataType.COMMON
        source_type = source_type or DatasetSourceType.USER
        labels = labels or dict()
        labels = [DatasetLabel(key=k, value=v) for k, v in labels.items()]

        options = options or dict()
        if isinstance(options, dict):
            options = json.dumps(options)

        request = CreateDatasetRequest(
            accessibility=accessibility,
            data_source_type=data_source_type.upper(),
            data_type=data_type,
            description=description,
            labels=labels,
            name=name,
            options=options,
            property=property,
            source_id=source_id,
            source_type=source_type,
            uri=uri,
            workspace_id=workspace_id,
        )

        resp = self._call_service_with_exception(
            self.base_client.create_dataset,
            request=request,
        )
        return resp.dataset_id

    def delete_dataset(self, dataset_id):
        self._call_service_with_exception(
            self.base_client.delete_dataset, dataset_id=dataset_id
        )

    def create_code_source(
        self,
        code_repo,
        workspace_id,
        display_name,
        accessibility=None,
        code_branch=None,
        code_repo_access_token=None,
        code_repo_user_name=None,
        description=None,
        mount_path=None,
    ):
        request = CreateCodeSourceRequest(
            accessibility=accessibility,
            code_branch=code_branch,
            code_repo=code_repo,
            code_repo_access_token=code_repo_access_token,
            code_repo_user_name=code_repo_user_name,
            description=description,
            display_name=display_name,
            mount_path=mount_path,
            workspace_id=workspace_id,
        )
        resp = self._call_service_with_exception(
            self.base_client.create_code_source,
            request=request,
        )
        return resp.body.code_source_id

    def delete_code_source(self, code_source_id):
        self._call_service_with_exception(
            self.base_client.delete_code_source, code_source_id=code_source_id
        )

    def update(self, workspace_id, name):
        raise NotImplementedError

    def delete_member(self, workspace_id, delete_member_ids):
        raise NotImplementedError

    def add_member(self, workspace_id, member):
        raise NotImplementedError

    def list_member(self, workspace_id, name=None, role=None):
        raise NotImplementedError

    def list_sub_users(self, exclude_workspace_id=None):
        raise NotImplementedError

    def list_permissions(self, workspace_id):
        raise NotImplementedError

    def get_permission(self, workspace_id, permission_code):
        raise NotImplementedError

    def create_tenant(self):
        raise NotImplementedError

    def get_tenant(self):
        raise NotImplementedError

    def add_compute_engine(self, workspace_id):
        raise NotImplementedError

    def list_compute_engines(self, name, workspace_id, engine_type="PAI", **kwargs):
        raise NotImplementedError

    def list_resource_groups(self, tenant_id):
        raise NotImplementedError

    def list_commodities(self):
        raise NotImplementedError
