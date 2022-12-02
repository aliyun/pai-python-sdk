from __future__ import absolute_import

import json
import logging
import os.path
from enum import Enum

import oss2
import six

from pai.api._resource_api import ResourceAPIsContainerMixin
from pai.common.consts import INNER_REGION_IDS
from pai.common.utils import makedirs
from pai.decorator import cached_property

logger = logging.getLogger(__name__)


# Environment variable indicates where config path located.
# If not present, "~/.pai/config.json" is used as default config path.
ENV_PAI_CONFIG_PATH = "PAI_CONFIG_PATH"

_default_session = None


class EnvType(Enum):
    PublicCloud = "PublicCloud"
    Light = "Light"


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
        pai.session.Session: Initialized default session.

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
        """Init workspace instance for the session using given workspace_id/workspace_name."""
        from pai.workspace import Workspace

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

            auth = oss2.Auth(
                access_key_id=access_key_id, access_key_secret=access_key_secret
            )
            oss_bucket = oss2.Bucket(
                auth=auth, endpoint=oss_endpoint, bucket_name=oss_bucket_name
            )
        self._oss_bucket = oss_bucket

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
        from pai.workspace import Workspace

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
        return self.pipeline_api.get_caller_provider()

    def create_run(
        self,
        name,
        arguments,
        env=None,
        pipeline_id=None,
        manifest=None,
        no_confirm_required=True,
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
        run_id = self.pipeline_run_api.create(
            name=name,
            arguments=arguments,
            env=env,
            manifest=manifest,
            pipeline_id=pipeline_id,
            no_confirm_required=no_confirm_required,
        )

        print(
            "Create pipeline run success (run_id: {run_id}), please visit the link below to"
            " view the run detail.".format(run_id=run_id)
        )
        print(self.run_detail_url(run_id, pipeline_id=pipeline_id))

        return run_id

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
