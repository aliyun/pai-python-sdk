from __future__ import absolute_import

import json
import logging
import os.path
from enum import Enum

import oss2
import six
from six.moves.urllib import parse

from pai.api.client_factory import ClientFactory
from pai.common.consts import INNER_REGION_IDS
from pai.common.utils import makedirs
from pai.common.yaml_utils import dump as yaml_dump
from pai.decorator import cached_property

from ._resource_api import ResourceAPIsContainerMixin

logger = logging.getLogger(__name__)


# Environment variable indicates where config path located.
# If not present, "~/.pai/config.json" is used as default config path.
ENV_PAI_CONFIG_PATH = "PAI_CONFIG_PATH"

_default_session = None


class EnvType(Enum):
    PublicCloud = "PublicCloud"
    Light = "Light"


def setup_light_default_session(
    access_key_id,
    access_key_secret,
    endpoint,
    protocol="http",
):
    """

    Args:
        access_key_id:
        access_key_secret:
        endpoint:
        protocol:

    Returns:

    """

    sess = LightSession(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint=endpoint,
        protocol=protocol,
    )

    Session.set_default_session(sess)
    return sess


def setup_default_session(
    access_key_id,
    access_key_secret,
    region_id,
    oss_bucket_name=None,
    oss_endpoint=None,
    workspace_id=None,
    workspace_name=None,
    **kwargs,
):
    """Setup the default session used by the program.

    The function setup the default region of PAI service, workspace, and credentials of
     default the session.

    Args:
        access_key_id (str): Alibaba Cloud access key id.
        access_key_secret (str): Alibaba Cloud access key secret.
        region_id (str): Alibaba Cloud region id, Please visit below url to view the detail:
             https://help.aliyun.com/document_detail/40654.html
        oss_bucket_name: OSS bucket name.
        oss_endpoint (str): Endpoint for the OSS bucket.
        workspace_id: Id of workspace use in the default session.
        workspace_name: Name of workspace in the default session.
        **kwargs:

    Returns:
        pai.core.session.Session: Initialized default session.

    """
    session = Session(
        access_key_id,
        access_key_secret,
        region_id,
        oss_bucket_name=oss_bucket_name,
        oss_endpoint=oss_endpoint,
        workspace_id=workspace_id,
        workspace_name=workspace_name,
        **kwargs,
    )

    Session.set_default_session(session)
    return session


def get_default_session(config_path=None):
    global _default_session
    if not _default_session:
        _default_session = Session.from_config(config_path=config_path)
    return _default_session


class Session(ResourceAPIsContainerMixin):
    """Wrap functionality provided by Alibaba Cloud PAI services

    This class encapsulates convenient methods to access PAI services, currently focus
    on PAI pipeline service(PAIFlow). Other service provided by PAI, such as EAS inference service,
    Model optimize, etc, will be included soon.

    """

    _default_session = None
    _session_stack = []

    env_type = EnvType.PublicCloud

    def __init__(
        self,
        access_key_id,
        access_key_secret,
        region_id,
        security_token=None,
        oss_bucket_name=None,
        oss_endpoint=None,
        workspace_id=None,
        workspace_name=None,
        **kwargs,
    ):
        """PAI Session Initializer.

        Args:
            access_key_id (str): Alibaba Cloud access key id.
            access_key_secret (str): Alibaba Cloud access key secret.
            region_id (str): Alibaba Cloud region id, Please visit below url to explore the detail:
                 https://help.aliyun.com/document_detail/40654.html
        """

        if not access_key_id or not access_key_secret:
            raise ValueError("Please provide access_key, access_secret and region")

        self._region_id = region_id
        self._access_key_id = access_key_id
        self._access_key_secret = access_key_secret
        self._security_token = security_token
        self._workspace_id = workspace_id

        self._init_clients(access_key_id, access_key_secret, region_id, **kwargs)
        self._init_oss_bucket(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            region_id=region_id,
            oss_bucket_name=oss_bucket_name,
            oss_endpoint=oss_endpoint,
            **kwargs,
        )
        super(Session, self).__init__()

        self._init_workspace(workspace_id, workspace_name)

    def _init_workspace(self, workspace_id, workspace_name):
        from ..workspace import Workspace

        """Init workspace instance for the session using given workspace_id/workspace_name."""
        if workspace_name and workspace_id:
            raise ValueError(
                "both workspace_name and workspace_id are provided, only one is required."
            )
        if workspace_id:
            workspace = Workspace.get(workspace_id, session=self)
            if not workspace:
                raise ValueError("Workspace not found, workspace_id=%s" % workspace_id)
        elif workspace_name:
            workspace = Workspace.get_by_name(name=workspace_name)
            if not workspace:
                raise ValueError(
                    "Workspace not found, workspace_name=%s" % workspace_name
                )
        else:
            workspace = None
        self._workspace = workspace

    def _init_oss_bucket(
        self,
        access_key_id,
        access_key_secret,
        region_id,
        oss_bucket_name,
        oss_endpoint=None,
        **kwargs,
    ):
        """Initialize an OSS bucket instance."""
        oss_bucket = None
        if oss_bucket_name and not oss_endpoint:
            oss_endpoint = "oss-{}.aliyuncs.com".format(region_id)
            logger.info(
                "Note: OSS endpoint not given, use default endpoint of the region: oss_endpoint=%s",
                oss_endpoint,
            )
        if oss_bucket_name and oss_endpoint:
            # Use specific credential for OSS bucket if it is provided.
            if "oss_access_key_id" in kwargs and "oss_access_key_secret" in kwargs:
                access_key_id = kwargs.pop("oss_access_key_id", None) or access_key_id
                access_key_secret = (
                    kwargs.pop("oss_access_key_secret", None) or access_key_secret
                )
                self._oss_access_key_id = access_key_id
                self._oss_access_key_secret = access_key_secret
            else:
                self._oss_access_key_id = None
                self._oss_access_key_secret = None

            # Group-inner job requires oss_role_arn to support mount OSS.
            self._oss_role_arn = kwargs.pop("oss_role_arn", None)
            self._oss_aliyun_uid = kwargs.pop("oss_aliyun_uid", None)

            auth = oss2.Auth(
                access_key_id=access_key_id, access_key_secret=access_key_secret
            )
            oss_bucket = oss2.Bucket(
                auth=auth, endpoint=oss_endpoint, bucket_name=oss_bucket_name
            )
        self._oss_bucket = oss_bucket

    def _init_clients(self, ak, ak_secret, region_id, **kwargs):
        endpoint = kwargs.pop("endpoint", None)
        protocol = kwargs.pop("protocol", None)

        self.paiflow_client = ClientFactory.create_paiflow_client(
            access_key_id=ak,
            access_key_secret=ak_secret,
            region_id=region_id,
            endpoint=endpoint,
            protocol=protocol,
        )

    def __enter__(self):
        Session.push_session_stack(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Session.pop_session_stack()

    @classmethod
    def from_config(cls, config_path=None):
        """Initialize session from config file.

        If config_path is not given, "~/.pai/config" is used as the default.

        Args:
            config_path:

        Returns:
            Session:

        """
        return cls._init_from_file_config(config_path=config_path)

    @classmethod
    def current(cls):
        """Read get current active PAI session."""
        if cls._session_stack:
            return cls._session_stack[-1]
        elif cls._default_session:
            return cls._default_session
        else:
            # try to load config file and init a default session
            cls._default_session = cls._init_from_file_config()
            return cls._default_session

    def save_config(self, config_path=None):
        """Persist configuration used by the session"""
        if not config_path:
            default_config_path = os.path.join(
                os.path.expanduser("~"), ".pai", "config.json"
            )
            config_path = os.environ.get(ENV_PAI_CONFIG_PATH, default_config_path)
        config = {
            "access_key_id": self._access_key_id,
            "access_key_secret": self._access_key_secret,
            "region_id": self._region_id,
        }

        if self._oss_bucket:
            config.update(
                {
                    "oss_bucket_name": self._oss_bucket.bucket_name,
                    "oss_endpoint": self._oss_bucket.endpoint,
                }
            )

        if self._workspace:
            config.update(
                {
                    "workspace_id": self.workspace.id,
                }
            )

        # Support specific OSS credentials.
        if self._oss_access_key_id and self._oss_access_key_secret:
            config.update(
                {
                    "oss_access_key_id": self._oss_access_key_id,
                    "oss_access_key_secret": self._oss_access_key_secret,
                }
            )
        # Support OSS RoleARN config which is required by OSS mount in group inner.
        if self._oss_role_arn:
            config.update(
                {
                    "oss_role_arn": self._oss_role_arn,
                }
            )

        # OSS Dataset in GroupInner requires.
        if self._oss_aliyun_uid:
            config.update(
                {
                    "oss_aliyun_uid": self._oss_aliyun_uid,
                }
            )

        makedirs(os.path.dirname(config_path))

        with open(config_path, "w") as f:
            f.write(json.dumps(config, indent=4))
        print("Write config succeed: config_path=%s" % config_path)

    @classmethod
    def _init_from_file_config(cls, config_path=None):
        """Read config file and construct a default session.

        Returns:
            Session: Session instance init from config file.
        """
        if not config_path:
            default_config_path = os.path.join(
                os.path.expanduser("~"), ".pai", "config.json"
            )
            config_path = os.environ.get(ENV_PAI_CONFIG_PATH, default_config_path)
        # Lookup config path silently, not raise exception if default config path is not exists.
        if not os.path.exists(config_path):
            raise ValueError("Config file not exists: %s", config_path)

        logger.debug("Reading config from file: %s", config_path)
        with open(config_path, "r") as f:
            config = json.load(f)

        sess = Session(**config)

        return sess

    @classmethod
    def set_default_session(cls, s):
        """Set default session"""

        global _default_session
        _default_session = s

    @classmethod
    def push_session_stack(cls, sess):
        """Push a session to stack top."""
        cls._session_stack.append(sess)

    @classmethod
    def pop_session_stack(cls):
        """Pop a session from stack"""
        if len(cls._session_stack) == 0:
            raise ValueError("Session stack is empty")
        return cls._session_stack.pop(-1)

    @property
    def region_id(self):
        return self._region_id

    @classmethod
    def _is_inner_region(cls, region_id):
        return region_id in INNER_REGION_IDS

    @property
    def is_inner(self):
        return self._region_id in INNER_REGION_IDS

    @property
    def workspace(self):
        """Workspace current session work in."""
        return self._workspace

    @property
    def workspace_name(self):
        return self._workspace.name

    def set_workspace(self, workspace):
        from ..workspace import Workspace

        if isinstance(workspace, six.string_types):
            workspace = Workspace.get_by_name(workspace)
        if not isinstance(workspace, Workspace):
            raise ValueError(
                "Parameter workspace should be Workspace instance or workspace name"
            )
        self._workspace = workspace

    @property
    def oss_bucket(self):
        if not self._oss_bucket:
            raise ValueError("Default OSS bucket not provided")
        return self._oss_bucket

    @property
    def workspace_id(self):
        return self._workspace_id

    @property
    def console_url(self):
        if self.is_inner:
            return "https://pai-next.alibaba-inc.com"
        else:
            return "https://pai.console.aliyun.com/console"

    @cached_property
    def provider(self):
        return six.ensure_str(self.paiflow_client.get_caller_provider())

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

        pipeline_info, _ = self.paiflow_client.list_pipeline(
            identifier=identifier,
            provider=provider,
            version=version,
            page_size=1,
        )
        if not pipeline_info:
            return
        return self.paiflow_client.get_pipeline_schema(pipeline_info[0]["PipelineId"])

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
        return self.paiflow_client.get_pipeline_schema(pipeline_id=pipeline_id)

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
            manifest = yaml_dump(pipeline_def)
        elif isinstance(pipeline_def, Pipeline):
            manifest = yaml_dump(pipeline_def.to_dict())
        elif isinstance(pipeline_def, six.string_types):
            manifest = pipeline_def
        else:
            raise ValueError(
                "Not support argument `pipeline_def` type %s, expected dict, Pipeline or str."
            )

        pipeline_id = self.paiflow_client.create_pipeline(
            manifest=manifest, workspace_id=workspace.id if workspace else None
        )
        return pipeline_id

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
        return self.paiflow_client.update_pipeline_privilege(pipeline_id, user_ids)[
            "Data"
        ]

    def list_pipeline_privilege(self, pipeline_id):
        return self.paiflow_client.list_pipeline_privilege(pipeline_id)["Data"]

    def create_run(
        self,
        name,
        arguments,
        env=None,
        pipeline_id=None,
        manifest=None,
        no_confirm_required=True,
        workspace=None,
    ):
        """Submit a pipeline run with pipeline operator and run arguments.

        If pipeline_id is supplied, remote pipeline manifest is used as workflow template.


        Args:
            name (str): Run instance name of the submit job.
            arguments (dict): Run arguments required by pipeline manifest.
            env (list): Environment arguments of run.
            pipeline_id (str): Pipeline
            manifest (str or dict): Pipeline manifest of the run workflow.
            no_confirm_required (bool): Run workflow start immediately if true
                else start_run service call if required to start the workflow.

        Returns:
            str:run id if run workflow init success.

        """
        run_args = {"arguments": arguments, "env": env}

        if workspace:
            workspace_id = workspace.id
        elif self.env_type == EnvType.Light:
            workspace_id = 0
        else:
            workspace_id = 0

        run_id = self.paiflow_client.create_run(
            name,
            run_args,
            pipeline_id=pipeline_id,
            manifest=manifest,
            no_confirm_required=no_confirm_required,
            workspace_id=workspace_id,
        )

        print(
            "Create pipeline run success (run_id: {run_id}), please visit the link below to"
            " view the run detail.".format(run_id=run_id)
        )
        print(self.run_detail_url(run_id, pipeline_id=pipeline_id))

        return run_id

    def list_run(
        self,
        name=None,
        run_id=None,
        pipeline_id=None,
        status=None,
        sorted_by=None,
        sorted_sequence=None,
        workspace=None,
    ):
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
        return self.paiflow_client.list_run(
            name=name,
            run_id=run_id,
            pipeline_id=pipeline_id,
            status=status,
            sorted_by=sorted_by,
            sorted_sequence=sorted_sequence,
            workspace_id=workspace.id if workspace else None,
        )

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

    def get_run_log(
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

    def list_run_outputs(
        self,
        run_id,
        node_id,
        depth=1,
        name=None,
        sorted_by=None,
        sorted_sequence=None,
        typ=None,
        page_number=1,
        page_size=50,
    ):
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

    def run_detail_url(self, run_id, pipeline_id=None):
        if self.env_type == EnvType.Light:
            return (
                "{console_host}/#/pipeline/detail/{pipeline_id}#runId={run_id}".format(
                    console_host=self.console_url,
                    pipeline_id=pipeline_id or 0,
                    run_id=run_id,
                )
            )

        if self.env_type == EnvType.PublicCloud:
            if not self.is_inner:
                return "{console_host}?regionId={region_id}#/studio/task/detail/{run_id}".format(
                    console_host=self.console_url,
                    region_id=self.region_id,
                    run_id=run_id,
                )
            return "{console_host}/#/studio/task/detail/{run_id}".format(
                console_host=self.console_url, run_id=run_id
            )


class LightSession(Session):
    env_type = EnvType.Light

    def __init__(self, access_key_id, access_key_secret, endpoint=None, protocol=None):
        prs = parse.urlparse(endpoint)
        if prs.scheme and protocol is None:
            protocol = prs.scheme
            endpoint = prs.netloc

        self.protocol = protocol
        self.endpoint = endpoint
        super(LightSession, self).__init__(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            region_id=None,
        )

    def _init_clients(self, ak, ak_secret, region_id, **kwargs):
        self.paiflow_client = ClientFactory.create_paiflow_client(
            access_key_id=ak,
            access_key_secret=ak_secret,
            endpoint=self.endpoint,
            protocol=self.protocol,
        )

    def _build_console_endpoint(self):
        s = self.endpoint.split(".")
        s[0] = "pai-console"
        return ".".join(s)

    @property
    def console_url(self):
        return "http://{0}".format(self._build_console_endpoint())

    def run_detail_url(self, run_id, pipeline_id=None):
        return "{console_host}/#/pipeline/detail/{pipeline_id}?runId={run_id}".format(
            console_host=self.console_url,
            pipeline_id=pipeline_id or 0,
            run_id=run_id,
        )
