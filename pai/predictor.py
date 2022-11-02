import abc
from typing import Any

from eas_prediction import PredictClient, StringRequest, StringResponse
from eas_prediction.request import Request

from pai.core.session import Session

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
    def __init__(
        self,
        service_name,
        access_token,
        endpoint,
        endpoint_type=ENDPOINT_TYPE_DEFAULT,
        serializer=None,
        session: Session = None,
    ):
        self.service_name = service_name
        self.endpoint_type = endpoint_type
        self.endpoint = endpoint
        self.access_token = access_token
        self.serializer = serializer

        self.client = self._init_client()

    def _init_client(self):
        client = PredictClient(self.endpoint, service_name=self.service_name)
        client.set_endpoint_type(self.endpoint_type)
        client.set_token(self.access_token)
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


class ServiceGroupPredictor(object):
    pass


class AsyncPredictor(object):
    pass
