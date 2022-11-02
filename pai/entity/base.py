from typing import Any, Callable, Dict, Optional, Type

from pai.common.consts import DEFAULT_PAGE_SIZE
from pai.core.session import Session, get_default_session
from pai.decorator import config_default_session
from pai.schema.base import BaseAPIResourceSchema


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
        """Construct a DLC Job from response.

        Args:
            session: Session for the instance.
            obj_dict: Response in json

        Returns:
            DlcJob: A DlcJob instance.
        """
        return cls._schema_cls(session=session).load(obj_dict)

    def to_api_object(self) -> Dict[str, Any]:
        """Dump current instance to API object in dict.

        Returns:
            dict: API object.
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


def make_resource_iterator(method: Callable, **kwargs):
    """Wrap resource list method as a iterator.

    Args:
        method: Resource List method.
        **kwargs: arguments for the method.

    Returns:
        A resource iterator.
    """

    page_number = kwargs.get("page_number", 1)
    page_size = kwargs.get("page_size", DEFAULT_PAGE_SIZE)

    while True:
        kwargs.update(page_number=page_number, page_size=page_size)
        results = method(**kwargs)

        for item in results:
            yield item

        if len(results) == 0 or len(results) <= page_size:
            return
        page_number += 1
