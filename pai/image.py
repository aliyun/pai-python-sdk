from pai.base import EntityBaseMixin
from pai.common.consts import ResourceAccessibility
from pai.decorator import config_default_session
from pai.schema import ImageSchema


class Image(EntityBaseMixin):
    """Image entity."""

    _schema_cls = ImageSchema

    # Default List image label filter.
    _LIST_IMAGE_DEFAULT_LABEL_FILTER = "system.official=false"
    _LIST_IMAGE_PAI_LABEL_FILTER = (
        "system.origin=PAI,system.official=true,system.supported.dlc=true"
    )
    _LIST_IMAGE_COMMUNITY_LABEL_FILTER = "system.origin=Community,system.official=true"

    def __init__(
        self,
        name,
        image_uri,
        accessibility=ResourceAccessibility.PUBLIC,
        description=None,
        labels=None,
        workspace_id=None,
        session=None,
        **kwargs,
    ):
        super(Image, self).__init__(session=session)
        self.accessibility = accessibility
        self.description = description
        self.image_uri = image_uri
        self.labels = labels
        self.name = name
        self.workspace_id = workspace_id

        # ReadOnly Fields.
        self._image_id = kwargs.pop("image_id", None)
        self._create_time = kwargs.pop("gmt_create_time", None)
        self._modified_time = kwargs.pop("gmt_modify_time", None)

    @property
    def id(self):
        """Id of the Image"""
        return self._image_id

    @property
    def create_time(self):
        """Image create time."""
        return self._create_time

    @property
    def modified_time(self):
        """Image modified time."""
        return self._modified_time

    @classmethod
    @config_default_session
    def list_community_images(cls, session=None):
        return [
            cls.from_api_object(item, session=session)
            for item in session.image_api.list_community_images().items
        ]

    @classmethod
    @config_default_session
    def list_pai_images(cls, session=None):
        return [
            cls.from_api_object(item, session=session)
            for item in session.image_api.list_pai_images().items
        ]
