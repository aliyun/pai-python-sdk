import abc
from typing import Any, Dict

from eas_prediction import PredictClient, StringRequest, StringResponse
from eas_prediction.request import Request
from six.moves.urllib import parse

from pai.decorator import config_default_session
from pai.predictor.service import Service
from pai.session import Session

ENDPOINT_TYPE_DIRECT = "DIRECT"
ENDPOINT_TYPE_VIPSERVER = "VIPSERVER"
ENDPOINT_TYPE_DEFAULT = "DEFAULT"


class PredictorBase(object):
    @abc.abstractmethod
    def predict(self, *args, **kwargs) -> Any:
        """Perform inference on the provided data and return a prediction."""

    @abc.abstractmethod
    def delete_predictor(self, *args, **kwargs) -> None:
        """Destroy resources associated with this predictor."""


class Predictor(object):
    @config_default_session
    def __init__(
        self,
        service_name: str,
        network_type="internet",
        serializer=None,
        session: Session = None,
    ):
        self.service_name = service_name
        self.network_type = network_type
        self.serializer = serializer
        self.session = session

        self.service: Service = Service.get(self.service_name)
        self.client = self._init_client()

    @classmethod
    @config_default_session
    def deploy(cls, service_config: Dict[str, Any], session: Session = None):
        service_name = session.service_api.create(service_config)

        return Predictor(
            service_name=service_name,
            session=session,
        )

    @property
    def service_config(self):
        return self.service.config

    def _init_client(self):
        if self.network_type == "internet":
            endpoint_url = self.service.internet_endpoint
        else:
            endpoint_url = self.service.intranet_endpoint
        parsed = parse.urlparse(endpoint_url)

        name = parsed.path.lstrip("/api/predict/")
        client = PredictClient(
            "{}://{}".format(parsed.scheme, parsed.hostname),
            service_name=name,
        )
        client.set_endpoint_type(ENDPOINT_TYPE_DEFAULT)
        client.set_token(self.service.access_token)
        client.init()
        return client

    def predict(self, data):
        data = self.serializer.serialize(data)
        if not isinstance(data, Request):
            data = StringRequest(data)
        resp = self.client.predict(data)
        if isinstance(resp, StringResponse):
            return self.serializer.deserialize(resp.response_data)
        return self.serializer.deserialize(resp)

    def destruct(self):
        self.client.destroy()
