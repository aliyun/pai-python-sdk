import json
import logging
from datetime import datetime
from typing import Optional

from six.moves.urllib import parse

from pai.base import EntityBaseMixin
from pai.common.consts import (
    DatasetSourceType,
    DataSourceType,
    DataType,
    FileProperty,
    ResourceAccessibility,
)
from pai.common.utils import random_str
from pai.decorator import config_default_session
from pai.schema import DatasetSchema
from pai.session import Session

logger = logging.getLogger(__name__)


class DataSourceConfig(object):
    """DataSource Configuration using in PAI DLC Job."""

    def __init__(self, dataset_id: str, mount_path: Optional[str] = None) -> None:
        self.dataset_id = dataset_id
        self.mount_path = mount_path

    def __str__(self):
        return "DataSourceConfig:dataset_id={0} mount_path={1}".format(
            self.dataset_id, self.mount_path
        )

    def __repr__(self):
        return self.__str__()


class Dataset(EntityBaseMixin):
    """Class represent Dataset resource."""

    _schema_cls = DatasetSchema

    RESOURCE_SERVICE_NAME = "workspace"

    _DEFAULT_PAGE_SIZE = 20

    _DEFAULT_PAGE_NUMBER = 1

    _list_method = "list_datasets_with_options"
    _get_method = "get_dataset_with_options"
    _delete_method = "delete_dataset_with_options"

    @config_default_session
    def __init__(
        self,
        uri,
        name=None,
        data_source_type=None,
        workspace_id=None,
        options=None,
        description=None,
        labels=None,
        mount_path="/mnt/data/",
        data_type=DataType.COMMON,
        accessibility=ResourceAccessibility.PUBLIC,
        property=FileProperty.DIRECTORY,
        source_type=DatasetSourceType.USER,
        session=None,
        **kwargs,
    ):
        super(Dataset, self).__init__(session=session)
        self.name = name or self._generate_name()
        self.data_type = data_type
        self.workspace_id = workspace_id
        self.accessibility = accessibility
        self.labels = labels
        self.uri = uri
        self.description = description
        self.source_type = source_type
        self.data_source_type = data_source_type or self._get_data_source_type_from_uri(
            uri
        )
        self.property = property or self._get_dataset_property_from_uri(uri)
        self.options = self._patch_options(options, mount_path=mount_path)
        self._mount_path = mount_path

        # ReadOnly Fields.
        self._dataset_id = kwargs.pop("dataset_id", None)
        self._create_time = kwargs.pop("create_time", None)
        self._modified_time = kwargs.pop("modified_time", None)

    @classmethod
    @config_default_session
    def upload(
        cls,
        source,
        name,
        options=None,
        description=None,
        labels=None,
        mount_path="/mnt/data/",
        session=None,
        data_source_type="OSS",
        **kwargs,
    ) -> "Dataset":
        dataset_id = session.dataset_api.create(
            data_source_type=data_source_type,
            uri=source,
            name=name,
            options=options,
            description=description,
            labels=labels,
            mount_path=mount_path,
            **kwargs,
        )
        return cls.get(dataset_id, session=session)

    @classmethod
    @config_default_session
    def get(cls, id, session=None):
        return cls.from_api_object(session.dataset_api.get(id), session=session)

    @classmethod
    def get_by_name(cls, name, session=None):
        pass

    @property
    def mount_path(self):
        """Dataset mount path."""
        return self._mount_path

    @mount_path.setter
    def mount_path(self, val):
        """Dataset mount path setter."""
        self._mount_path = val
        self.options = self._patch_options(self.options, mount_path=val)

    @property
    def id(self):
        """Id of the dataset"""
        return self._dataset_id

    @property
    def create_time(self):
        """Dataset create time."""
        return self._create_time

    @property
    def modified_time(self):
        """Dataset modified time."""
        return self._modified_time

    def _generate_name(self):
        return "{}-{}-{}".format(
            type(self).__name__,
            random_str(6),
            datetime.now().isoformat(sep="-", timespec="seconds"),
        )

    @classmethod
    def _get_data_source_type_from_uri(cls, dataset_uri):
        parsed_result = parse.urlparse(dataset_uri)
        scheme = parsed_result.scheme.lower()
        if scheme.lower() == DataSourceType.OSS.lower():
            return DataSourceType.OSS
        elif scheme.lower() == DataSourceType.NAS.lower():
            return DataSourceType.NAS
        else:
            logger.warning(
                "Failed to get DataSourceType from Dataset uri: {}".format(dataset_uri)
            )

    @classmethod
    def _get_dataset_property_from_uri(cls, dataset_uri):
        if dataset_uri.strip().endswith("/"):
            return FileProperty.DIRECTORY
        else:
            return FileProperty.FILE

    @classmethod
    def _patch_options(cls, options, mount_path):
        if not mount_path:
            return options
        options = options or dict()
        if not isinstance(options, dict):
            options = json.loads(options)

        options.update({"mountPath": mount_path})

        return json.dumps(options)

    def mount(self, mount_path=None):
        """Make a InputDataConfig using the Dataset for the DLCJob."""
        return DataSourceConfig(
            dataset_id=self.id,
            mount_path=mount_path,
        )

    @classmethod
    @config_default_session
    def list(
        cls,
        session: Session = None,
        page_size=10,
        page_number=10,
        data_source_type=None,
        name=None,
    ):
        """

        Args:
            session:
            page_size:
            page_number:
            data_source_type:
            name:

        Returns:

        """
        res = session.dataset_api.list(
            page_size=page_size,
            page_number=page_number,
            data_source_type=data_source_type,
            name=name,
        )
        return [cls.from_api_object(item, session=session) for item in res.items]

    def delete(self):
        self.session.dataset_api.delete(self.id)
