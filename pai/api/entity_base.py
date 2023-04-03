from typing import Any, Dict, Optional, Type

from pai.schema.base import BaseAPIResourceSchema
from pai.session import Session, config_default_session, get_default_session


class EntityBaseMixin(object):

    _schema_cls: Type[BaseAPIResourceSchema]
    resource_type: str

    def __init__(self, session: Optional[Session] = None, **kwargs) -> None:
        super(EntityBaseMixin, self).__init__()
        self._session = session or get_default_session()

    @property
    def session(self) -> Session:
        return self._session

    @classmethod
    @config_default_session
    def from_api_object(cls, obj_dict: Dict[str, Any], session: Session = None):
        """Construct an entity representing the API resource from response.

        Args:
            session: Session for the instance.
            obj_dict: Response in json

        Returns:
            An entity representing the resource.
        """
        return cls._schema_cls(session=session).load(obj_dict)

    def to_api_object(self) -> Dict[str, Any]:
        """Convert the current instance to a dictionary representing an API object.

        Returns:
            dict: a dictionary representing the API object.
        """
        return self._schema_cls().dump(self)

    def patch_from_api_object(self, api_obj: Dict[str, Any]):
        if not api_obj:
            raise ValueError("REST API object should not be empty.")

        return self._schema_cls(instance=self).load(api_obj)

    def __repr__(self):
        return "{}:{}".format(type(self).__name__, self.id)

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def resource_api(self):
        return self._session.get_api_by_resource(self.resource_type)
