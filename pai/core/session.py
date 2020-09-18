from __future__ import absolute_import

import logging

import six
import yaml
from aliyunsdkcore.client import AcsClient

from pai.api.client_factory import ClientFactory
from pai.core.workspace import Workspace
from pai.decorator import cached_property

logger = logging.getLogger(__name__)


def setup_default_session(access_key_id=None, access_key_secret=None, region_id=None,
                          oss_bucket=None, **kwargs):
    """Setup the default session used by the program.

    The function setup the default region of PAI service, workspace, and credentials of
     default the session.

    Args:
        access_key_id (str): Alibaba Cloud access key id.
        access_key_secret (str): Alibaba Cloud access key secret.
        region_id (str): Alibaba Cloud region id, Please visit below url to view the detail:
             https://help.aliyun.com/document_detail/40654.html
        oss_bucket (oss2.Bucket): oss2.Bucket object.
        **kwargs:

    Returns:
        pai.core.session.Session: Initialized default session.

    """

    session = Session(access_key_id, access_key_secret, region_id, oss_bucket=oss_bucket,
                      **kwargs)
    Session._default_session = session

    if not session._is_inner:
        workspace = Workspace.get_or_create_default_workspace()
        session.set_workspace(workspace=workspace)
    return session


def get_default_session():
    """Get the default session.

    Returns:
        pai.core.session.Session: Default session used by program.

    """
    return Session.get_default_session()


class Session(object):
    """Wrap functionality provided by Alibaba Cloud PAI services

    This class encapsulates convenient methods to access PAI services, currently focus
    on PAI pipeline service(PAIFlow). Other service provided by PAI, such as EAS inference service,
    Model optimize, etc, will be included soon.

    """

    _default_session = None
    _inner_region_ids = ["center"]

    def __init__(self, access_key_id=None, access_key_secret=None, region_id=None, oss_bucket=None,
                 workspace=None, **kwargs):
        """ PAI Session Initializer.

        Args:
            access_key_id (str): Alibaba Cloud access key id.
            access_key_secret (str): Alibaba Cloud access key secret.
            region_id (str): Alibaba Cloud region id, Please visit below url to explore the detail:
                 https://help.aliyun.com/document_detail/40654.html
        """

        if not access_key_id or not access_key_secret or not region_id:
            raise ValueError("Please provide access_key, access_secret and region")

        self._init_clients(access_key_id, access_key_secret, region_id)

        self._region_id = region_id
        self._oss_bucket = oss_bucket
        self._workspace = workspace

    def _init_clients(self, ak, ak_secret, region_id):
        _acs_client = AcsClient(ak=ak, secret=ak_secret,
                                region_id=region_id)
        self.paiflow_client = ClientFactory.create_paiflow_client(
            _acs_client, _is_inner=self._is_inner_region(region_id))
        self.ws_client = ClientFactory.create_workspace_client(_acs_client)

    @classmethod
    def get_default_session(cls):
        return cls._default_session

    @property
    def region_id(self):
        return self._region_id

    @classmethod
    def _is_inner_region(cls, region_id):
        return region_id in cls._inner_region_ids

    @property
    def _is_inner(self):
        return self._region_id in self._inner_region_ids

    @property
    def workspace(self):
        return self._workspace

    @property
    def workspace_name(self):
        return self._workspace.name

    def set_workspace(self, workspace):
        if isinstance(workspace, six.string_types):
            workspace = Workspace.get_by_name(workspace)
        if not isinstance(workspace, Workspace):
            raise ValueError("Parameter workspace should be Workspace instance or workspace name")
        self._workspace = workspace

    @property
    def oss_bucket(self):
        if not self._oss_bucket:
            raise ValueError("Default OSS bucket not provided")
        return self._oss_bucket

    @property
    def console_host(self):
        return 'https://pai.data.aliyun.com/console'

    @cached_property
    def provider(self):
        return six.ensure_str(self.paiflow_client.get_my_provider()["Data"]["Provider"])

    def get_pipeline(self, identifier, provider=None, version="v1"):
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

        provider = provider or self.provider
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

    def list_pipeline(self, identifier=None, provider=None, fuzzy=None, version=None):
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
        return self.paiflow_client.list_pipeline(
            identifier=identifier,
            provider=provider,
            fuzzy=fuzzy,
            version=version,
        )

    def create_pipeline(self, pipeline_def, workspace=None):
        """Create new pipeline instance.

        Create_pipeline submit pipeline manifest to PAI pipeline service. Identifier-
        provider-version triple in metadata of manifest is unique identifier of the Pipeline.
         The same triple combination will result overwrite of original pipeline.

        Args:
            pipeline_def (dict or str): pipeline definition manifest, support types Pipeline,
            workspace:

        Returns:
            str: pipeline_id, ID of pipeline in pipeline service.
        """
        from pai.pipeline import Pipeline

        if isinstance(pipeline_def, dict):
            manifest = yaml.dump(pipeline_def)
        elif isinstance(pipeline_def, Pipeline):
            manifest = yaml.dump(pipeline_def.to_dict())
        elif isinstance(pipeline_def, six.string_types):
            manifest = pipeline_def
        else:
            raise ValueError(
                "Not support argument `pipeline_def` type %s, expected dict, Pipeline or str.")

        resp = self.paiflow_client.create_pipeline(manifest=manifest,
                                                   workspace_id=workspace.id if workspace else None)
        return resp["Data"]["PipelineId"]

    def describe_pipeline(self, pipeline_id):
        """Get detail information of pipeline by pipelineId.

        User should been granted with DescribePipeline privilege on the pipeline_id to use this
        API. Manifest in response include the detail implementation of the pipeline.

        Args:
            pipeline_id (str):  ID of pipeline in pipeline service

        Returns:
            dict: Including metadata and full manifest of the pipeline.

        """
        return self.paiflow_client.describe_pipeline(pipeline_id)["Data"]

    def update_pipeline_privilege(self, pipeline_id, user_ids):
        return self.paiflow_client.update_pipeline_privilege(pipeline_id, user_ids)["Data"]

    def list_pipeline_privilege(self, pipeline_id):
        return self.paiflow_client.list_pipeline_privilege(pipeline_id)["Data"]

    def create_run(self, name, arguments, env=None, pipeline_id=None, manifest=None,
                   no_confirm_required=True, workspace=None):
        """Submit a pipeline run with pipeline _template and run arguments.

        If pipeline_id is supplied, remote pipeline manifest is used as workflow _template.


        Args:
            name (str): Run instance name of the submit job.
            arguments (list): Run arguments required by pipeline manifest.
            env (list): Environment arguments of run.
            pipeline_id (str): Pipeline
            manifest (str): Pipeline manifest of the run workflow.
            no_confirm_required (bool): Run workflow start immediately if true
                else start_run service call if required to start the workflow.

        Returns:
            str:run id if run workflow init success.

        """
        run_args = {
            "arguments": arguments,
            "env": env
        }

        resp = self.paiflow_client.create_run(name, run_args, pipeline_id=pipeline_id,
                                              manifest=manifest,
                                              no_confirm_required=no_confirm_required,
                                              workspace_id=workspace.id if workspace else None)

        run_id = resp["Data"]["RunId"]

        if not self._is_inner:
            print(
                "Create pipeline run success (run_id: {run_id}), please visit the link below to"
                " view the run detail.".format(run_id=run_id))
            print(self.run_detail_url(run_id))
        else:
            print("Create pipeline run success (run_id: {run_id})".format(run_id=run_id))

        return run_id

    def list_run(self, name=None, run_id=None, pipeline_id=None, status=None,
                 sorted_by=None, sorted_sequence=None, workspace=None):
        """List submit pipeline run infos.

        List run infos by specific filter, return the outline information of the run, the detail
        information of the run could be achieve from session.get_run_detail.

        Args:
            name (str): List run infos with the specific name.
            run_id (str): List run of specific run_id.
            pipeline_id (str): Filter the run infos using pipeline_id.
            status (str): Status of the run, could be one of Init, Running, Suspended, Succeeded,
                Terminated, Unknown, Skipped, Failed.
            sorted_by (str): Order key of the run_infos, could be one of 'pipelineId', 'userId',
                'parentUserId', 'startedAt', 'finishedAt', 'workflowServiceId'.
            sorted_sequence (str): Order sequence by order key, either asc or desc.
            workspace:

        Returns:
            List of Dict:  Run Information as dict.
        """
        return self.paiflow_client.list_run(name=name,
                                            run_id=run_id,
                                            pipeline_id=pipeline_id,
                                            status=status,
                                            sorted_by=sorted_by,
                                            sorted_sequence=sorted_sequence,
                                            workspace_id=workspace.id if workspace else None)

    def delete_pipeline(self, pipeline_id):
        """Delete the pipeline using pipeline_id, return True if success.

        Args:
            pipeline_id: Pipeline Id

        """
        _ = self.paiflow_client.delete_pipeline(pipeline_id)
        return True

    def get_run_detail(self, run_id, node_id, depth=2):
        """Get Run detail information of specific node.

        Get detail run information, including node status, node start time, finished time.
        If node is implementation as composite pipeline and parameter depth > 1, sub-pipeline
        information of the node will provided.

        Args:
            run_id (str): Run instance id.
            node_id (str): Node identifier in run workflow.
            depth (int): if the running node is composite pipeline, depth > 1 will provide
             the sub-pipeline information.

        Returns:
            dict: Detail information of node in workflow.

        """
        run_info = self.paiflow_client.get_run_detail(run_id, node_id, depth=depth)
        return run_info["Data"]

    def get_run_log(self, run_id, node_id, from_time=None, to_time=None,
                    keyword=None, reverse=False, page_offset=0, page_size=100):
        """Get log information of pipeline run.

        Args:
            run_id (str): Run instance id.
            node_id (str): Node identifier in run workflow.
            from_time (datetime or int):
            to_time (datetime or int):
            keyword (str):
            reverse (bool):
            page_offset (int):
            page_size (int):

        Returns:
            list: Logs are return as list of string.

        """
        kwargs = locals()
        kwargs.pop("self")
        logs = self.paiflow_client.list_node_log(**kwargs)
        return logs["Data"]

    def list_run_outputs(self, run_id, node_id, depth=1, name=None, sorted_by=None,
                         sorted_sequence=None, typ=None, page_number=1, page_size=50):
        """Get pipeline run outputs.

        Args:
            run_id (str): Run instance id.
            node_id (str): Node identifier in run workflow.
            depth (int): Get output at specific depth of nested pipeline.
            name (str): Filter by output name.
            sorted_by (str): Order key of outputs.
            sorted_sequence (str): Order sequence, either asc or desc.
            typ (str): Filter by outputs type.
            page_number (int): Return specific page number of results.
            page_size (int): Maximum size of return results.

        Returns:
            List of dict: Outputs of run instance in json.

        """
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
        """Return outline run information.

        Args:
            run_id (str): Run instance id.

        """
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

    def run_detail_url(self, run_id):
        return "{console_host}?regionId={region_id}#/studio2/task/detail/{run_id}".format(
            console_host=self.console_host, region_id=self.region_id, run_id=run_id)
