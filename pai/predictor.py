import json
import logging
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from urllib import parse

import docker
import requests
from eas_prediction import ENDPOINT_TYPE_DEFAULT, PredictClient
from eas_prediction import PredictException as EasPredictionException
from eas_prediction import StringRequest, StringResponse

from .common.consts import FrameworkTypes
from .common.docker_utils import ContainerRun
from .exception import PredictionException
from .serializers import (
    BytesSerializer,
    JsonSerializer,
    PyTorchSerializer,
    SerializerBase,
    TensorFlowSerializer,
)
from .session import Session, config_default_session

logger = logging.getLogger(__name__)

_PAI_SERVICE_CONSOLE_URI_PATTERN = (
    "https://pai.console.aliyun.com/?regionId={region_id}#"
    "/eas/serviceDetail/{service_name}/detail"
)


class ServiceStatus(object):
    """All EAS inference service status."""

    Running = "Running"
    Waiting = "Waiting"
    Scaling = "Scaling"
    Stopped = "Stopped"
    Failed = "Failed"
    DeleteFailed = "DeleteFailed"

    @classmethod
    def completed_status(cls):
        return [
            cls.Running,
            cls.Stopped,
            cls.Failed,
            cls.DeleteFailed,
        ]


class EndpointType(object):

    # Public Internet Endpoint
    INTERNET = "INTERNET"

    # VPC Endpoint
    INTRANET = "INTRANET"


class PredictorBase(ABC):
    @abstractmethod
    def predict(self, data) -> Any:
        """Perform inference on the provided data and return a prediction."""


class Predictor(PredictorBase):
    """Predictor is responsible for making prediction to an online service.

    The `predictor.predict` method sends the input data to the online prediction service
    and returns the prediction result. The serializer object of the predictor is
    responsible for data transformation when the `predict` method is invoked. The input
    data is serialized using the `serializer.serialize` method before it is sent, and
    the response is deserialized using the `serializer.deserialize` method before the
    prediction result returns.

    Examples::

        # Initialize a predictor object from an existing service using PyTorch
        # processor.
        torch_predictor = Predictor(service_name="example_torch_service")
        result = torch_predictor.predict(numpy.asarray([[22,33,44], [19,22,33]]))
        assert isinstance(result, numpy.ndarray)

    """

    @config_default_session
    def __init__(
        self,
        service_name: str,
        endpoint_type: str = EndpointType.INTERNET,
        serializer: Optional[SerializerBase] = None,
        session: Optional[Session] = None,
        **kwargs,
    ):
        """Construct a `Predictor` object using an existing prediction service.

        Args:
            service_name (str): Name of the existing prediction service.
            endpoint_type (str): Selects the endpoint used by the predictor, which
                should be one of `INTERNET` or `INTRANET`. The `INTERNET` endpoint type
                means that the predictor calls the service over a public endpoint, while
                the `INTRANET` endpoint type is over a VPC endpoint.
            serializer (SerializerBase, optional): A serializer object that transforms
                the input Python object for data transmission and deserialize the
                response data to Python object.
            session (Session, optional): A PAI session object used for communicating
                with PAI service.
        """
        self.session = session

        self._service_name = service_name
        self._endpoint_type = endpoint_type
        self._service_api_object = self.describe_service()
        self._client = None
        self._client_kwargs = kwargs or dict()
        self._serializer = serializer or self._get_default_serializer()

        self._check()

    @property
    def service_name(self):
        return self._service_name

    @property
    def endpoint_type(self):
        return self._endpoint_type

    @property
    def serializer(self):
        return self._serializer

    @serializer.setter
    def serializer(self, value):
        if not isinstance(value, SerializerBase):
            raise ValueError(
                f"Type of serializer should be a subclass of 'SerializerBase'. "
                f"Received: {type(value)}"
            )

        self._serializer = value
        self._post_init_serializer(force=True)

    @property
    def service_status(self):
        """Returns the status of the service."""
        return self.describe_service()["Status"]

    @property
    def console_uri(self):
        """Returns the console URI of the service."""
        return _PAI_SERVICE_CONSOLE_URI_PATTERN.format(
            region_id=self.session.region_id,
            service_name=self.service_name,
        )

    def _check(self):
        """Check parameters for the predictor"""
        if self._endpoint_type.upper() not in [
            EndpointType.INTERNET,
            EndpointType.INTRANET,
        ]:
            raise ValueError(
                "Parameter 'endpoint_type' for the predictor should be one of"
                " 'INTERNET' or 'INTRANET'."
            )

    def _post_init(self):
        """Post-initialize the serializer and client."""
        self._post_init_client()
        self._post_init_serializer()

    def _post_init_serializer(self, force=False):
        """Post-initialize the serializer by invoking serializer.inspect_from_service"""
        if not hasattr(self, "__post_init_serializer_flag") or force:
            if hasattr(self._serializer, "inspect_from_service"):
                self._serializer.inspect_from_service(
                    self.service_name, session=self.session
                )
            setattr(self, "__post_init_serializer_flag", 1)

    def _post_init_client(self):
        """Construct the client used to call the prediction service."""
        if self._client is None:
            self._client = self._init_client()

    def _init_client(self):
        if self.endpoint_type.upper() == EndpointType.INTERNET:
            endpoint_url = self._service_api_object["InternetEndpoint"]
        else:
            endpoint_url = self._service_api_object["IntranetEndpoint"]
        parsed = parse.urlparse(endpoint_url)
        client = PredictClient(
            "{}://{}".format(parsed.scheme, parsed.hostname),
            service_name=self.service_name,
        )
        timeout = self._client_kwargs.get("timeout", None)

        if timeout:
            client.set_timeout(timeout)
        client.set_endpoint_type(ENDPOINT_TYPE_DEFAULT)
        client.set_token(self._service_api_object["AccessToken"])
        client.init()
        return client

    def __del__(self):
        if hasattr(self, "_client") and self._client:
            self._client.destroy()
            self._client = None

    def _get_default_serializer(self):
        """Get default serializer for the predictor by inspecting the service config."""
        from pai.model import _BuiltinProcessor

        service_config = json.loads(self._service_api_object["ServiceConfig"])
        processor_code = service_config.get("processor")

        # if the service serving with custom processor or custom container,
        # use JsonSerializer as default serializer.
        if not processor_code:
            return JsonSerializer()
        if processor_code in (
            _BuiltinProcessor.PMML,
            _BuiltinProcessor.XGBoost,
        ):
            return JsonSerializer()
        elif processor_code.startswith(FrameworkTypes.TensorFlow.lower()):
            serializer = TensorFlowSerializer()
            return serializer
        elif processor_code.startswith(FrameworkTypes.PyTorch.lower()):
            return PyTorchSerializer()
        else:
            return JsonSerializer()

    def _send_request(self, request):
        if not self._client:
            self._client = self._init_client()

        try:
            return self._client.predict(request)
        except EasPredictionException as e:
            raise PredictionException(e.code, e.message)

    def predict(self, data):
        """Make a prediction with the online prediction service.

        The serializer object for the predictor is responsible for data transformation
        when the 'predict' method is invoked. The input data is serialized using the
        `serializer.serialize` method before it is sent, and the response is
        deserialized using the `serializer.deserialize` method before the prediction
        result returns.

        Args:
            data: The input data for the prediction. It will be serialized using the
                serializer of the predictor before transmitted to the prediction
                service.

        Returns:
            object: Prediction result.

        Raises:
            PredictionException: Raise if status code of the prediction response does
                not equal 200.
        """

        self._post_init()

        data = self._serializer.serialize(data)

        resp: StringResponse = self._send_request(StringRequest(data))
        return self._serializer.deserialize(resp.response_data)

    def raw_predict(self, data: bytes) -> bytes:
        """Send the serialized data in bytes to the service and returns the
        prediction in raw bytes.

        Args:
            data (bytes): Input data that is serialized to bytes for transmission.

        Returns:
            bytes: Prediction result in bytes returned by the service.

        Raises:
            PredictionException: Raise if status code of the prediction response does
                not equal 200.
        """
        resp: StringResponse = self._send_request(StringRequest(data))
        return resp.response_data

    def inspect_model_signature_def(self):
        """Get SignatureDef of the serving model.

        .. note::

            Only the service using the TensorFlow processor supports getting the
            model signature_definition.

        Returns:
            Dict[str, Any]: A dictionary representing the signature definition of the
                serving model.

        """
        service_config = json.loads(self._service_api_object["ServiceConfig"])
        processor_code = service_config.get("processor")

        if processor_code and processor_code.startswith("tensorflow"):
            return TensorFlowSerializer.inspect_model_signature_def(
                self.service_name, session=self.session
            )
        raise RuntimeError(
            "Only the online prediction service using the TensorFlow processor supports"
            " getting the signature_definition"
        )

    def describe_service(self) -> Dict[str, Any]:
        """Describe the service that referred by the predictor.

        Returns:
            Dict[str, Any]: Response from PAI API service.

        """
        return self.session.service_api.get(self.service_name)

    def start_service(self, wait=True):
        """Start the stopped service."""
        self.session.service_api.start(name=self.service_name)
        if wait:
            status = ServiceStatus.Running
            unexpected_status = ServiceStatus.completed_status()
            unexpected_status.remove(status)
            type(self)._wait_for_status(
                service_name=self.service_name,
                status=status,
                unexpected_status=unexpected_status,
                session=self.session,
            )

    def stop_service(self, wait=True):
        """Stop the running service."""
        self.session.service_api.stop(name=self.service_name)
        if wait:
            status = ServiceStatus.Stopped
            unexpected_status = ServiceStatus.completed_status()
            unexpected_status.remove(status)
            unexpected_status.remove(ServiceStatus.Running)

            type(self)._wait_for_status(
                service_name=self.service_name,
                status=status,
                unexpected_status=unexpected_status,
                session=self.session,
            )

    def delete_service(self):
        """Delete the service."""
        self.session.service_api.delete(name=self._service_name)

    def wait_for_ready(self):
        """Wait until the service enter running status."""

        logger.info(
            "Service waiting for ready: service_name={}".format(self.service_name)
        )
        unexpected_status = ServiceStatus.completed_status()
        unexpected_status.remove(ServiceStatus.Running)

        type(self)._wait_for_status(
            service_name=self.service_name,
            status=ServiceStatus.Running,
            unexpected_status=unexpected_status,
            session=self.session,
        )

    @classmethod
    @config_default_session
    def _wait_for_status(
        cls,
        service_name: str,
        status: str,
        unexpected_status: List[str],
        interval: int = 3,
        session: Optional[Session] = None,
    ):
        service_api_object = session.service_api.get(service_name)
        last_status = service_api_object["Status"]
        last_msg = service_api_object["Message"]
        time.sleep(interval)

        while True:
            service_api_object = session.service_api.get(service_name)
            # Check the service status
            cur_status = service_api_object["Status"]
            if cur_status == status:
                return status
            elif unexpected_status and cur_status in unexpected_status:
                # Unexpected terminated status
                raise RuntimeError(
                    f"The Service terminated unexpectedly: "
                    f"name={service_api_object['ServiceName']} "
                    f"status={service_api_object['Status']} "
                    f"reason={service_api_object['Reason']} "
                    f"message={service_api_object['Message']}."
                )
            elif (
                last_status == cur_status and service_api_object["Message"] == last_msg
            ) and cur_status != ServiceStatus.Waiting:
                # If service.status and service.message have not changed and
                # service.status is not 'Waiting', do not print the service
                # status/message.
                pass
            else:
                logger.info(
                    f"Refresh Service status: "
                    f"name={service_api_object['ServiceName']} "
                    f"id={service_api_object['ServiceId']} "
                    f"status={service_api_object['Status']} "
                    f"reason={service_api_object['Reason']} "
                    f"message={service_api_object['Message']}."
                )

            last_status = service_api_object["Status"]
            last_msg = service_api_object["Message"]
            time.sleep(interval)

    def switch_version(self, version: int):
        """Switch service to target version.

        Args:
            version (int): Target version

        """
        service_api_object = self.describe_service()

        current_version = service_api_object["CurrentVersion"]
        latest_version = service_api_object["LatestVersion"]
        if current_version == version:
            raise ValueError("Target version equals to current version.")

        if version > latest_version:
            raise ValueError("Target version greater than latest version.")
        self.session.service_api.update_version(self.service_name, version=version)

    @classmethod
    @config_default_session
    def deploy(
        cls,
        config: Dict[str, Any],
        session: Optional[Session] = None,
        endpoint_type: str = EndpointType.INTERNET,
        serializer: Optional[SerializerBase] = None,
        wait: bool = True,
    ):
        """Deploy an online prediction service using given configuration.

        Args:
            config (Dict[str, Any]): A dictionary of service configuration.
            session (:class:`pai.session.Session`, optional): An optional
                session object. If not provided, a default session will be used.
            serializer: An optional serializer object. If not provided, a
                default serializer will be used.
            endpoint_type: The type of endpoint to use.
            wait: Whether to wait for the service to be ready before returning.

        Returns:
            :class:`pai.predictor.Predictor`: A Predictor object for the deployed
                online prediction service.

        """
        name = session.service_api.create(config=config)

        if wait:
            # Wait until the service is ready
            unexpected_status = ServiceStatus.completed_status()
            unexpected_status.remove(ServiceStatus.Running)
            Predictor._wait_for_status(
                service_name=name,
                status=ServiceStatus.Running,
                unexpected_status=unexpected_status,
                session=session,
            )

        p = Predictor(
            service_name=name,
            endpoint_type=endpoint_type,
            serializer=serializer,
        )
        return p


class LocalPredictor(PredictorBase):
    """Perform prediction to a local service running with docker."""

    def __init__(
        self,
        port: int,
        container_id: str = None,
        serializer: SerializerBase = None,
        prediction_route: str = None,
    ):
        """LocalPredictor initializer.

        Args:
            port (int): The port of the local service.
            container_id (str, optional): The container id of the local service.
            serializer (SerializerBase, optional): A serializer object that transforms.
            prediction_route (str, optional): The route of the prediction endpoint.

        """
        self.container_id = container_id
        self.port = port
        self.serializer = serializer or BytesSerializer()
        self.prediction_route = prediction_route.lstrip("/") if prediction_route else ""
        self._container_run = (
            self._build_container_run(container_id, port=port)
            if self.container_id
            else None
        )

    @classmethod
    def _build_container_run(cls, container_id, port):
        client = docker.from_env()
        container = client.containers.get(container_id)

        return ContainerRun(container=container, port=port)

    def predict(self, data) -> Any:
        """Perform prediction with the given data.

        Args:
            data: The data to be predicted.
        """
        request_data = self.serializer.serialize(data=data)
        response = requests.post(
            url="http://127.0.0.1:{port}/{prediction_route}".format(
                port=self._container_run.port, prediction_route=self.prediction_route
            ),
            data=request_data,
        )

        if response.status_code != 200:
            raise PredictionException(
                code=response.status_code,
                message=response.content,
            )

        return self.serializer.deserialize(response.content)

    def raw_predict(self, data: bytes) -> bytes:
        """Perform prediction with the given data in bytes.

        Args:
            data (bytes): The data to be predicted.

        Returns:
            bytes: The prediction result in bytes.

        """
        response = requests.post(
            url="http://127.0.0.1:{port}/{prediction_route}".format(
                port=self.port, prediction_route=self.prediction_route
            ),
            data=data,
        )

        if response.status_code != 200:
            raise PredictionException(
                code=response.status_code,
                message=response.content,
            )

        return response.content

    def __enter__(self):
        if not self._container_run:
            raise RuntimeError("No container id is provided for the predictor.")
        elif not self._container_run.is_running():
            self._container_run.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._container_run:
            self._container_run.stop()

    def __del__(self):
        """Stops the container when the instance is about to be destroyed."""
        if self._container_run:
            self._container_run.stop()

    def delete_service(self):
        """Delete the docker container that running the service."""
        if self._container_run:
            self._container_run.stop()
