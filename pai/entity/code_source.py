import logging

from pai.common.consts import ResourceAccessibility
from pai.core.session import Session, get_default_session
from pai.decorator import config_default_session
from pai.entity.base import EntityBaseMixin
from pai.entity.common import CodeSourceConfig
from pai.schema import CodeSourceSchema

logger = logging.getLogger(__name__)


class CodeSource(EntityBaseMixin):
    """Class represent a CodeSource resource."""

    _schema_cls = CodeSourceSchema

    @config_default_session
    def __init__(
        self,
        code_repo,
        display_name,
        description=None,
        workspace_id=None,
        accessibility=ResourceAccessibility.PRIVATE,
        code_branch=None,
        code_commit=None,
        mount_path="/root/code",
        code_repo_user_name=None,
        code_repo_access_token=None,
        session=None,
        **kwargs,
    ):
        super(CodeSource, self).__init__(session=session)
        self.code_repo = code_repo
        self.display_name = display_name
        self.description = description
        self.workspace_id = workspace_id
        self.accessibility = accessibility
        self.code_branch = code_branch
        self.code_commit = code_commit
        self.mount_path = mount_path
        self.code_repo_access_token = code_repo_access_token
        self.code_repo_user_name = code_repo_user_name

        self._session = session

        # ReadOnly Fields.
        self._code_source_id = kwargs.pop("code_source_id", None)
        self._create_time = kwargs.pop("create_time", None)
        self._modified_time = kwargs.pop("modified_time", None)

    @classmethod
    @config_default_session
    def get(cls, id: str, session: Session = None) -> "CodeSource":
        return cls.from_api_object(session.code_source_api.get(id), session=session)

    def register(self):
        if self.id:
            raise ValueError("API Resource has been created.")
        code_source_id = self.session.code_source_api.create(code_source=self)
        self.session.code_source_api.refresh_entity(entity=self, id_=code_source_id)

    @property
    def id(self):
        return self._code_source_id

    @property
    def create_time(self):
        """CodeSource create time."""
        return self._create_time

    @property
    def modified_time(self):
        """CodeSource Modified time."""
        return self._modified_time

    def mount(self, mount_path=None, branch=None, commit=None):
        """Make a InputCodeConfig for DlcJob."""
        return CodeSourceConfig(
            code_source_id=self.id,
            mount_path=mount_path,
            branch=branch,
            commit=commit,
        )

    @classmethod
    @config_default_session
    def list(cls, session=None):
        result = session.code_source_api.list()
        return [cls.from_api_object(item, session=session) for item in result.items]

    def delete(self):
        self.session.code_source_api.delete(self.id)
