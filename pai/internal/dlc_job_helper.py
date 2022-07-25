import functools
import json
import time

import six

from six.moves.urllib import parse

from pai.api.common import DEFAULT_DATASET_MOUNT_PATH
from pai.api.common import (
    PAI_DLC_INTEGRATED_WITH_WORKSPACE_FEATURE,
    DataSourceType,
    ResourceAccessibility,
    FileProperty,
)
from pai.api.dlc import DlcClient
from pai.api.workspace import WorkspaceClient
from pai.common.oss_utils import parse_oss_url, compose_oss_url, parse_dataset_path

DLC_JOB_DETAIL_INNER_URL_PATTERN = "https://dlc.alibaba-inc.com/#/jobs/detail?jobId={0}"
DLC_JOB_DETAIL_PUBLIC_URL_PATTERN = (
    "https://pai-dlc.console.aliyun.com/#/jobs/detail?jobId={0}&regionId={1}"
)
DLC_JOB_IN_WORKSPACE_PUBLIC_URL_PATTERN = (
    "https://pai.console.aliyun.com/?regionId={0}&workspaceId={1}#/job/detail?jobId={2}"
)
import logging

logger = logging.getLogger(__name__)


class DlcJobStatus(object):
    """DLC Job status."""

    Succeeded = "Succeeded"
    Failed = "Failed"
    Stopped = "Stopped"

    @classmethod
    def is_succeed(cls, status):
        return status in [cls.Succeeded]

    @classmethod
    def is_failed(cls, status):
        return status in [cls.Failed, cls.Stopped]


class DlcJobHelper(object):
    """A helper class provide compatible API for AIWorkspace integrated PAI-DLC or legacy PAI-DLC."""

    def __init__(
        self,
        dlc_client,
        ws_client,
        is_inner,
        workspace_id,
        region_id,
        role_arn,
        oss_aliyun_uid=None,
        oss_role_arn=None,
    ):
        self.dlc_client = dlc_client  # type: DlcClient
        self.ws_client = ws_client  # type: WorkspaceClient
        self.is_inner = is_inner  # type: bool
        self.workspace_id = workspace_id  # type: str
        self.region_id = region_id  # type: str
        self.oss_aliyun_uid = oss_aliyun_uid
        self.oss_role_arn = oss_role_arn

    @classmethod
    def from_session(cls, session):
        return DlcJobHelper(
            dlc_client=session.dlc_client,
            ws_client=session.ws_client,
            is_inner=session.is_inner,
            workspace_id=session.workspace.id if session.workspace else None,
            region_id=session.region_id,
            role_arn=session._oss_role_arn,
            # GroupInner config requires by OSS dataset.
            oss_aliyun_uid=session._oss_aliyun_uid,
            oss_role_arn=session._oss_role_arn,
        )

    @functools.lru_cache()
    def is_use_aiworkspace(self):
        """Returns if current user use AIWorkspace integrated PAI-DLC or legacy PAI-DLC."""
        if not self.workspace_id:
            return False

        features = self.ws_client.list_feature(
            names=PAI_DLC_INTEGRATED_WITH_WORKSPACE_FEATURE
        )
        if not features:
            return False
        return any(
            x.lower() == PAI_DLC_INTEGRATED_WITH_WORKSPACE_FEATURE.lower()
            for x in features
        )

    def create_dataset(
        self,
        name,
        data_source_type,
        uri,
        endpoint=None,
        mount_path=None,
        file_system_id=None,
        options=None,
        description=None,
        role_arn=None,
    ):

        if self.is_use_aiworkspace():
            # AIWorkspace Datasource API use upper case `data_source_type`, such as OSS, NAS, etc.
            data_source_type = data_source_type.upper()

            options = self.patch_options(
                options,
                {
                    "mountPath": mount_path or DEFAULT_DATASET_MOUNT_PATH,
                },
            )
            if data_source_type.lower() == DataSourceType.OSS.lower():
                url = self._compose_oss_url(uri, endpoint)
                dataset_id = self.ws_client.create_dataset(
                    name=name,
                    accessibility=ResourceAccessibility.PRIVATE,
                    data_source_type=data_source_type,
                    description=description,
                    options=options,
                    workspace_id=self.workspace_id,
                    uri=url,
                    property=FileProperty.DIRECTORY,
                )

            else:
                url = self._compose_nas_url(file_system_id, self.region_id, uri)
                dataset_id = self.ws_client.create_dataset(
                    name=name,
                    accessibility=ResourceAccessibility.PRIVATE,
                    data_source_type=data_source_type,
                    description=description,
                    options=options,
                    workspace_id=self.workspace_id,
                    uri=url,
                    property=FileProperty.DIRECTORY,
                )
        else:
            if self.is_inner:
                options = self.patch_options(
                    options,
                    {"RoleARN": role_arn or self.oss_role_arn},
                )
                options = self.patch_aliyun_uid(options, uri)

            if DataSourceType.OSS.lower() == data_source_type.lower():
                parsed = parse_oss_url(uri)
                endpoint = endpoint or parsed.endpoint
                # ! OSS URL for Dataset in DLC Service should not contain endpoint.
                uri = self._compose_oss_url_without_endpoint(uri)

            dataset_id = self.dlc_client.create_data_source(
                # PAI-DLC Datasource API use lower case `data_source_type`
                data_source_type=data_source_type.lower(),
                description=description,
                name=name,
                endpoint=endpoint,
                file_system_id=file_system_id,
                mount_path=mount_path or DEFAULT_DATASET_MOUNT_PATH,
                options=options,
                path=uri,
            )
        return dataset_id

    def patch_aliyun_uid(self, options, uri):
        """Get AliyunUid from given uri query."""
        parsed_result = parse.urlparse(uri)
        query = parse.parse_qs(parsed_result.query)
        if "aliyunUid" in query:
            aliyun_uid = query.get("aliyunUid")[0]
        elif "aliyun_uid" in query:
            aliyun_uid = query.get("aliyun_uid")[0]
        else:
            aliyun_uid = self.oss_aliyun_uid
        if aliyun_uid:
            logger.info("Patch AliyunUid to Dataset options.")
            options = self.patch_options(options, {"aliyunID": aliyun_uid})

        return options

    @classmethod
    def patch_options(cls, options, patch):
        """Update the options with given key value dict."""
        options = options or dict()
        if isinstance(options, six.string_types):
            options = json.loads(options)

        options.update(patch)
        return json.dumps(options)

    @classmethod
    def _compose_oss_url(cls, url, endpoint=None):
        """Build a OSS directory URI for Dataset."""
        bucket_name, obj_key, endpoint_in_url, _ = parse_oss_url(url)
        _, dir_path, _ = parse_dataset_path(obj_key)
        endpoint = endpoint or endpoint_in_url

        return compose_oss_url(bucket_name, dir_path, endpoint)

    @classmethod
    def _compose_oss_url_without_endpoint(cls, url):
        bucket_name, obj_key, _, _ = parse_oss_url(url)
        _, dir_path, _ = parse_dataset_path(obj_key)
        url = "oss://{0}/{1}".format(bucket_name, dir_path.lstrip("/"))
        return url

    @classmethod
    def _compose_nas_url(cls, file_system_id, region_id, path=None):
        path = path or "/"
        _, dir_path, _ = parse_dataset_path(path)
        return "nas://{0}.{1}{2}".format(file_system_id, region_id, path)

    def job_url(self, job_id):
        """Make a Job Dashboard Uri."""
        if self.is_inner:
            return DLC_JOB_DETAIL_INNER_URL_PATTERN.format(job_id)
        elif self.is_use_aiworkspace():
            return DLC_JOB_IN_WORKSPACE_PUBLIC_URL_PATTERN.format(
                self.region_id, self.workspace_id, job_id
            )
        else:
            return DLC_JOB_DETAIL_PUBLIC_URL_PATTERN.format(job_id, self.region_id)

    def wait_for_completion(self, job_id, interval=10):
        """Wait utils job is completed.

        Args:
            interval: Watch interval.
            job_id: Job Id.

        Raises:
            Throws RuntimeError if job is failed or stopper.

        """

        while True:
            resp = self.dlc_client.get_job(job_id)
            print("Job status: ", resp["Status"])
            if DlcJobStatus.is_succeed(resp["Status"]):
                break
            elif DlcJobStatus.is_failed(resp["Status"]):
                raise RuntimeError(
                    "Dlc Job failed: status={} reason_code={} reason_message={}".format(
                        resp["Status"], resp["ReasonCode"], resp["ReasonMessage"]
                    )
                )
            time.sleep(interval)
