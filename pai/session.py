from __future__ import absolute_import

import logging

import six
import yaml
from aliyunsdkcore.client import AcsClient
from odps import ODPS
import oss2

from pai.api.client_factory import ClientFactory
from pai.utils import run_detail_url

logger = logging.getLogger(__name__)


class Session(object):
    """Wrap functionality provided by Alibaba Cloud PAI services

    This class encapsulates convenient methods to access PAI services, currently focus
    on Pipeline service, future include EAS inference service, Model optimize, etc.

    """

    def __init__(self, access_key_id, access_key_secret, region_id,
                 odps_project=None, odps_endpoint=None):
        """ PAI Session constructor.

        Args:
            access_key_id (str): Alibaba Cloud access key id.
            access_key_secret (str): Alibaba Cloud access key secret.
            region_id (str): Alibaba Cloud region id
            odps_project (str): Default MaxCompute(ODPS) project used for session.
            odps_endpoint (str): Endpoint for entry
        """

        if not access_key_id or not access_key_secret or not region_id:
            raise ValueError("Please provide access_key, access_secret and region")

        self.region_id = region_id

        self._init_clients(access_key_id, access_key_secret, region_id,
                           odps_project=odps_project, odps_endpoint=odps_endpoint)

    def _init_clients(self, access_key, access_secret, region, odps_project=None,
                      odps_endpoint=None):

        self._acs_client = AcsClient(ak=access_key, secret=access_secret, region_id=region)
        self.paiflow_client = ClientFactory.create_paiflow_client(self._acs_client)

        self.sts_client = ClientFactory.create_sts_client(self._acs_client)
        self.odps_client = ODPS(access_id=access_key, secret_access_key=access_secret,
                                project=odps_project,
                                endpoint=odps_endpoint)
        self._oss_auth = oss2.Auth(access_key_id=access_key, access_key_secret=access_secret)
        self._init_account()

    def get_oss_bucket(self, endpoint, bucket):
        return oss2.Bucket(self._oss_auth, endpoint=endpoint, bucket_name=bucket)

    @property
    def account_id(self):
        """int: Alibaba account ID of specific access key in constructor."""
        return self._account_id

    @property
    def user_id(self):
        """int: Owner user id (Alibaba UserId) of session."""
        return self._user_id

    def _init_account(self):
        caller_identity = self.sts_client.get_caller_identity()
        self._account_id = int(caller_identity["AccountId"])
        self._user_id = int(caller_identity["UserId"])
        self._arn = caller_identity["Arn"]

    @property
    def odps_project(self):
        """int: Default MaxCompute project use by session."""
        return self.odps_client.project

    def get_pipeline(self, identifier, provider, version):
        """Get information of pipeline by identifier, provider and version.

        User should has `GetPipeline` privilege to access the pipeline.

        Args:
            identifier (str): Identifier of pipeline.
            provider (str): Provider of pipeline, it is supplied as Account UID of the creator
             of pipeline.
            version (str): version of the pipeline. default

        Returns:
            dict: Information of pipeline, including pipeline_id and manifest.

        Raises:
            ServiceCallException: Raise if the pipeline not exists.
        """
        pipeline_info = self.paiflow_client.get_pipeline(identifier=identifier,
                                                         provider=provider,
                                                         version=version)["Data"]
        return pipeline_info

    def get_pipeline_by_id(self, pipeline_id):
        """Get information of pipeline by pipelineId.

        User should has `GetPipeline` privilege to access the pipeline.

        Args:
            pipeline_id: Unique Id of the pipeline.

        Returns:
            dict: Information of pipeline, including pipeline_id and manifest.
        Raises:
            ServiceCallException: Raise if the pipeline not exists.

        """
        return self.paiflow_client.get_pipeline(pipeline_id=pipeline_id)["Data"]

    def list_pipeline(self, identifier=None, provider=None, fuzzy=None, version=None,
                      page_num=1, page_size=50):
        """List metadata information of pipelines using supplied query filter.

        The query filters (identifier, provider, version) are None by default. Pipeline service
        return the pipelines where user has been granted with GetPipeline privilege.

        Args:
            identifier (str): Filter by identifier.
            provider (str): Filter by pipeline provider
            fuzzy (bool): Use fuzzy match search with provide identifier if been assign as true.
            version (str): Filter by version
            page_num (int): Return specific page number of results.
            page_size (int): Maximum size of return results.

        Returns:
            :obj:`list` of :obj:`dict`: List of pipeline metadata.

        """
        resp = self.paiflow_client.list_pipeline(
            identifier=identifier,
            provider=provider,
            fuzzy=fuzzy,
            version=version,
            page_num=page_num,
            page_size=page_size,
        )
        total_count = resp["TotalCount"]
        pipeline_infos = resp["Data"]
        return pipeline_infos, total_count

    def create_pipeline(self, pipeline_def):
        """Create new pipeline by push the definition to PAI pipeline service.

        create_pipeline submit pipeline manifest to PAI pipeline service. Identifier-provider-version
         triple in metadata of manifest is unique identifier of the Pipeline. The same triple
          combination will result overwrite of original pipeline.

        Args:
            pipeline_def (dict or str): pipeline definition manifest, support types Pipeline,

        Returns:
            str: pipeline_id: ID of pipeline in pipeline service.
        """
        from pai.pipeline import Pipeline

        if isinstance(pipeline_def, dict):
            manifest = yaml.dump(pipeline_def)
        elif isinstance(pipeline_def, Pipeline):
            manifest = yaml.dump(pipeline_def.to_dict())
        elif not isinstance(pipeline_def, six.string_types):
            raise ValueError(
                "Not support argument `pipeline_def` type %s, expected dict, Pipeline or str.")
        resp = self.paiflow_client.create_pipeline(manifest=manifest)
        return resp["Data"]["PipelineId"]

    def describe_pipeline(self, pipeline_id):
        """Get detail information of pipeline by pipelineId.


        Args:
            pipeline_id:

        Returns:

        """
        return self.paiflow_client.describe_pipeline(pipeline_id)

    def update_pipeline_privilege(self, pipeline_id, user_ids):
        return self.paiflow_client.update_pipeline_privilege(pipeline_id, user_ids)["Data"]

    def list_pipeline_privilege(self, pipeline_id):
        return self.paiflow_client.list_pipeline_privilege(pipeline_id)["Data"]

    def create_run(self, name, arguments, env=None, pipeline_id=None, manifest=None,
                   no_confirm_required=True):
        arguments = {
            "arguments": arguments,
            "env": env
        }

        resp = self.paiflow_client.create_run(name, arguments, pipeline_id=pipeline_id,
                                              manifest=manifest,
                                              no_confirm_required=no_confirm_required)

        run_id = resp["Data"]["RunId"]

        print("Create pipeline run success (run_id: {run_id}), please visit the link below to view"
              " the run detail.".format(run_id=run_id))
        print(run_detail_url(run_id, self.region_id))

        return run_id

    def list_run(self, name=None, run_id=None, pipeline_id=None, status=None,
                 sorted_by=None, sorted_sequences=None, page_num=1, page_size=50):
        kwargs = locals()
        kwargs.pop("self")
        run_infos = self.paiflow_client.list_run(**kwargs)
        return run_infos

    def delete_pipeline(self, pipeline_id):
        _ = self.paiflow_client.delete_pipeline(pipeline_id)
        return True

    def get_run_detail(self, run_id, node_id, depth=2):
        run_info = self.paiflow_client.get_run_detail(run_id, node_id, depth=depth)
        return run_info["Data"]

    def get_run_log(self, run_id, node_id, from_time=None, to_time=None,
                    keyword=None, reverse=False, page_offset=0, page_size=100):
        kwargs = locals()
        kwargs.pop("self")
        logs = self.paiflow_client.list_node_log(**kwargs)
        return logs["Data"]

    def list_run_outputs(self, run_id, node_id, depth=1, name=None, sorted_by=None,
                         sorted_sequence=None, typ=None, page_number=1, page_size=50):
        outputs = self.paiflow_client.list_run_outputs(
            run_id=run_id,
            node_id=node_id,
            depth=depth,
            name=name,
            sorted_by=sorted_by,
            sorted_sequence=sorted_sequence,
            typ=typ,
            page_number=page_number,
            page_size=page_size,
        )["Data"]
        return outputs

    def get_run(self, run_id):
        run_info = self.paiflow_client.get_run(run_id)
        return run_info["Data"]

    def terminate_run(self, run_id):
        resp = self.paiflow_client.terminate_run(run_id)
        return resp["Data"]["runId"] == run_id

    def suspend_run(self, run_id):
        resp = self.paiflow_client.suspend_run(run_id)
        return resp["Data"]

    def retry_run(self, run_id):
        resp = self.paiflow_client.retry_run(run_id)
        return resp["Data"]["runId"] == run_id

    def resume_run(self, run_id):
        resp = self.paiflow_client.resume_run(run_id)
        return resp["Data"]

    def start_run(self, run_id):
        resp = self.paiflow_client.start_run(run_id)
        return resp["Data"]
