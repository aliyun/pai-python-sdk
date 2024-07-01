#  Copyright 2023 Alibaba, Inc. or its affiliates.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import asyncio
import base64
import functools
import json
import posixpath
import time
from abc import ABC, abstractmethod
from concurrent.futures import Future, ThreadPoolExecutor
from io import IOBase
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from urllib.parse import urlencode

import aiohttp
import requests

from .common.consts import FrameworkTypes
from .common.docker_utils import ContainerRun
from .common.logging import get_logger
from .common.utils import http_user_agent, is_package_available
from .exception import PredictionException
from .serializers import (
    JsonSerializer,
    PyTorchSerializer,
    SerializerBase,
    TensorFlowSerializer,
)
from .session import Session, get_default_session

if is_package_available("openai"):
    from openai import OpenAI


logger = get_logger(__name__)

_PAI_SERVICE_CONSOLE_URI_PATTERN = (
    "https://pai.console.aliyun.com/?regionId={region_id}&workspaceId={workspace_id}#"
    "/eas/serviceDetail/{service_name}/detail"
)

_QUEUE_SERVICE_REQUEST_ID_HEADER = "X-Eas-Queueservice-Request-Id"
_QUEUE_SERVICE_SINK_PATH = "sink"
_DEFAULT_ASYNC_WORKER_COUNT = 30


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


class ServiceType(object):
    Standard = "Standard"
    Async = "Async"


class PredictorBase(ABC):
    @abstractmethod
    def predict(self, *args, **kwargs) -> Any:
        """Perform inference on the provided data and return prediction result."""

    @abstractmethod
    def raw_predict(
        self,
        data: Any = None,
        path: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        method: str = "POST",
        timeout: Optional[Union[float, Tuple[float, float]]] = None,
        **kwargs,
    ):
        pass


class RawResponse(object):
    """Response object returned by the predictor.raw_predict."""

    def __init__(self, status_code: int, headers: Dict[str, str], content: bytes):
        """Initialize a RawResponse object.

        Args:
            status_code (int):
            headers (dict):
            content (bytes):
        """
        self.status_code = status_code
        self.headers = headers
        self.content = content

    def json(self):
        """Returns the json-encoded content of a response

        Returns:
            Dict[str, Any]: The json-encoded content of a response.

        """
        return json.loads(self.content)


class _ServicePredictorMixin(object):
    def __init__(
        self,
        service_name: str,
        session: Optional[Session] = None,
        endpoint_type: str = EndpointType.INTERNET,
        serializer: Optional[SerializerBase] = None,
    ):
        self.service_name = service_name
        self.session = session or get_default_session()
        self._service_api_object = self.describe_service()
        self.endpoint_type = endpoint_type
        self.serializer = serializer or self._get_default_serializer()
        self._request_session = requests.Session()

    def __repr__(self):
        return "{}(service_name={}, endpoint_type={})".format(
            type(self).__name__,
            self.service_name,
            self.endpoint_type,
        )

    def __del__(self):
        self._request_session.close()

    def refresh(self):
        self._service_api_object = self.describe_service()

    @property
    def endpoint(self):
        if self.endpoint_type == EndpointType.INTRANET:
            return self._service_api_object["IntranetEndpoint"]
        else:
            return self._service_api_object["InternetEndpoint"]

    @property
    def intranet_endpoint(self):
        return self._service_api_object["IntranetEndpoint"]

    @property
    def internet_endpoint(self):
        return self._service_api_object["InternetEndpoint"]

    @property
    def service_status(self):
        """Returns the status of the service."""
        return self._service_api_object["Status"]

    @property
    def access_token(self) -> str:
        """Access token of the service."""
        return self._service_api_object["AccessToken"]

    @property
    def labels(self) -> Dict[str, str]:
        """Labels of the service."""
        labels = {
            item["LabelKey"]: item["LabelValue"]
            for item in self._service_api_object.get("Labels", [])
        }
        return labels

    @property
    def console_uri(self):
        """Returns the console URI of the service."""
        return _PAI_SERVICE_CONSOLE_URI_PATTERN.format(
            workspace_id=self.session.workspace_id,
            region_id=self.session.region_id,
            service_name=self.service_name,
        )

    def _get_default_serializer(self):
        """Get default serializer for the predictor by inspecting the service config."""
        from pai.model._model import _BuiltinProcessor

        service_config = json.loads(self._service_api_object["ServiceConfig"])
        processor_code = service_config.get("processor")

        # If the prediction service is serving with custom processor or custom
        # container, use JsonSerializer as default serializer.
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

    def _post_init_serializer(self):
        """Post-initialize the serializer by invoking serializer.inspect_from_service"""
        if not hasattr(self.serializer, "__post_init_serializer_flag") and hasattr(
            self.serializer, "inspect_from_service"
        ):
            self.serializer.inspect_from_service(
                self.service_name, session=self.session
            )
            setattr(self.serializer, "__post_init_serializer_flag", 1)

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
        self.refresh()

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
        self.refresh()

    def delete_service(self):
        """Delete the service."""
        self.session.service_api.delete(name=self.service_name)

    def wait_for_ready(self):
        """Wait until the service enter running status.

        Raises:
            RuntimeError: Raise if the service terminated unexpectedly.

        """
        if self.service_status == ServiceStatus.Running:
            return

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

        # hack: PAI-EAS gateway may not be ready when the service is ready.
        self._wait_for_gateway_ready()
        self.refresh()

    def wait(self):
        """Wait for the service to be ready."""
        return self.wait_for_ready()

    def _wait_for_gateway_ready(self, attempts: int = 60, interval: int = 2):
        """Hacky way to wait for the service gateway to be ready.

        Args:
            attempts (int): Number of attempts to wait for the service gateway to be
                ready.
            interval (int): Interval between each attempt.
        """

        def _is_gateway_ready():
            # can't use HEAD method to check gateway status because the service will
            # block the request until timeout.
            resp = self._send_request(method="GET")
            logger.debug(
                "Check gateway status result: status_code=%s content=%s",
                resp.status_code,
                resp.content,
            )
            res = not (
                # following status code and content indicates the gateway is not ready
                (
                    resp.status_code == 503
                    and (b"no healthy upstream" in resp.content or not resp.content)
                )
                or (resp.status_code == 404 and not resp.content)
            )
            return res

        err_count_threshold = 3
        err_count = 0
        while attempts > 0:
            attempts -= 1
            try:
                if _is_gateway_ready():
                    break
            except requests.exceptions.RequestException as e:
                err_count += 1
                if err_count >= err_count_threshold:
                    logger.warning("Failed to check gateway status: %s", e)
                    break
            time.sleep(interval)
        else:
            logger.warning("Timeout waiting for gateway to be ready.")

    @classmethod
    def _wait_for_status(
        cls,
        service_name: str,
        status: str,
        unexpected_status: List[str],
        interval: int = 3,
        session: Optional[Session] = None,
    ):
        session = session or get_default_session()
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
    def deploy(
        cls,
        config: Dict[str, Any],
        session: Optional[Session] = None,
        endpoint_type: str = EndpointType.INTERNET,
        serializer: Optional[SerializerBase] = None,
        wait: bool = True,
    ) -> PredictorBase:
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
            :class:`pai.predictor.PredictorBase`: A Predictor object for the deployed
                online prediction service.

        """
        session = session or get_default_session()
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

        service_api_obj = session.service_api.get(name)

        if service_api_obj["ServiceType"] == ServiceType.Async:
            p = AsyncPredictor(
                service_name=name,
                endpoint_type=endpoint_type,
                serializer=serializer,
            )
        else:
            p = Predictor(
                service_name=name,
                endpoint_type=endpoint_type,
                serializer=serializer,
            )

        return p

    def _build_url(
        self, path: Optional[str] = None, params: Dict[str, str] = None
    ) -> str:
        url = self.endpoint
        if path:
            if path.startswith("/"):
                path = path[1:]
            url = posixpath.join(url, path)

        # Add params to URL
        url = url + "?" + urlencode(params) if params else url
        return url

    def _build_headers(self, headers: Dict[str, str] = None) -> Dict[str, str]:
        headers = headers or dict()
        headers["Authorization"] = self.access_token
        headers["User-Agent"] = http_user_agent(headers.get("User-Agent"))
        return headers

    def _handle_input(self, data):
        return self.serializer.serialize(data) if self.serializer else data

    def _handle_output(self, content: bytes):
        return self.serializer.deserialize(content) if self.serializer else content

    def _handle_raw_input(self, data):
        if isinstance(data, (IOBase, bytes, str)):
            # if data is a file-like object, bytes, or string, it will be sent as
            # request body
            json_data, data = None, data
        else:
            # otherwise, it will be treated as a JSON serializable object and sent as
            # JSON.
            json_data, data = data, None

        return json_data, data

    def _handle_raw_output(self, status_code: int, headers: dict, content: bytes):
        return RawResponse(status_code, headers, content)

    def _send_request(
        self,
        data=None,
        path=None,
        method="POST",
        json=None,
        headers=None,
        params=None,
        **kwargs,
    ):
        url = self._build_url(path)
        resp = self._request_session.request(
            url=url,
            json=json,
            data=data,
            headers=self._build_headers(headers),
            method=method,
            params=params,
            **kwargs,
        )
        return resp

    async def _send_request_async(
        self,
        data=None,
        path=None,
        method="POST",
        json=None,
        headers=None,
        params=None,
        **kwargs,
    ):
        url = self._build_url(path=path, params=params)
        headers = self._build_headers(headers)
        async with aiohttp.ClientSession() as session:
            return await session.request(
                method=method,
                url=url,
                headers=headers,
                data=data,
                json=json,
                **kwargs,
            )


class Predictor(PredictorBase, _ServicePredictorMixin):
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

    def __init__(
        self,
        service_name: str,
        endpoint_type: str = EndpointType.INTERNET,
        serializer: Optional[SerializerBase] = None,
        session: Optional[Session] = None,
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
        super(Predictor, self).__init__(
            service_name=service_name,
            session=session or get_default_session(),
            endpoint_type=endpoint_type,
            serializer=serializer,
        )
        self._check()

    def _check(self):
        config = json.loads(self._service_api_object["ServiceConfig"])
        if config.get("metadata", {}).get("type") == ServiceType.Async:
            logger.warning(
                "Predictor is not recommended to make prediction to a async"
                " prediction service."
            )

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
                not equal 2xx.
        """
        self._post_init_serializer()
        data = self._handle_input(data)
        resp = self._send_request(
            data,
        )
        if resp.status_code // 100 != 2:
            raise PredictionException(resp.status_code, resp.content)
        return self._handle_output(
            resp.content,
        )

    def raw_predict(
        self,
        data: Any = None,
        path: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        method: str = "POST",
        timeout: Optional[Union[float, Tuple[float, float]]] = None,
        **kwargs,
    ) -> RawResponse:
        """Make a prediction with the online prediction service.

        Args:
            data (Any): Input data to be sent to the prediction service. If it is a
                file-like object, bytes, or string, it will be sent as the request body.
                Otherwise, it will be treated as a JSON serializable object and sent as
                JSON.
            path (str, optional): Path for the request to be sent to. If it is provided,
                it will be appended to the endpoint URL (Default None).
            headers (dict, optional): Request headers.
            method (str, optional): Request method, default to 'POST'.
            timeout(float, tuple(float, float), optional): Timeout setting for the
                request (Default 10).
            **kwargs: Additional keyword arguments for the request.
        Returns:
            RawResponse: Prediction response from the service.

        Raises:
            PredictionException: Raise if status code of the prediction response does
                not equal 2xx.
        """
        json_data, data = self._handle_raw_input(data)
        resp = self._send_request(
            data=data,
            json=json_data,
            method=method,
            path=path,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )
        if resp.status_code // 100 != 2:
            raise PredictionException(resp.status_code, resp.content)

        resp = RawResponse(
            status_code=resp.status_code,
            content=resp.content,
            headers=dict(resp.headers),
        )
        return resp

    def openai(self, url_suffix: str = "v1", **kwargs) -> "OpenAI":
        """Initialize an OpenAI client from the predictor.

        Only used for OpenAI API compatible services, such as Large Language Model
        service from PAI QuickStart.

        Args:
            url_suffix (str, optional): URL suffix that will be appended to the
                EAS service endpoint to form the base URL for the OpenAI client.
                (Default "v1").
            **kwargs: Additional keyword arguments for the OpenAI client.

        Returns:
            OpenAI: An OpenAI client object.
        """

        if not is_package_available("openai"):
            raise ImportError(
                "openai package is not installed, install it with `pip install openai`."
            )

        if url_suffix.startswith("/"):
            default_base_url = posixpath.join(self.endpoint, url_suffix[1:])
        else:
            default_base_url = posixpath.join(self.endpoint, url_suffix)
        base_url = kwargs.pop("base_url", default_base_url)
        api_key = kwargs.pop("api_key", self.access_token)

        return OpenAI(base_url=base_url, api_key=api_key, **kwargs)


class WaitConfig(object):
    """WaitConfig is used to set polling configurations for waiting for asynchronous
    requests to complete."""

    def __init__(self, max_attempts: int = 0, interval: int = 5):
        if interval <= 0:
            raise ValueError("interval must be positive integer.")
        self.max_attempts = max_attempts
        self.interval = interval


class AsyncTask(object):
    """AsyncTask is a wrapper class for `concurrent.futures.Future` object that represents
    a prediction call submitted to an async prediction service.
    """

    def __init__(
        self,
        future: Future,
    ):
        self.future = future
        super(AsyncTask, self).__init__()

    def result(self, timeout: Optional[float] = None):
        """
        Returns the prediction result of the call.

        Args:
            timeout (float, optional): Timeout setting  (Default None).

        Returns:
            The result of the prediction call.

        """
        return self.future.result(timeout=timeout)

    def done(self):
        return self.future.done()

    def exception(self, timeout: Optional[float] = None) -> Optional[Exception]:
        return self.future.exception()

    def running(self):
        return self.future.running()

    def cancel(self):
        return self.future.cancel()

    def cancelled(self):
        return self.future.cancelled()


class AsyncPredictor(PredictorBase, _ServicePredictorMixin):
    """A class that facilitates making predictions to asynchronous prediction service.

    Examples::

        # Initialize an AsyncPredictor object using the name of a running service.
        async_predictor = AsyncPredictor(service_name="example_service")

        # Make a prediction with the service and get the prediction result.
        resp = async_predictor.predict(data="YourPredictionData")
        result = resp.wait()

        # Make a prediction with async API.
        import asyncio
        result = asyncio.run(async_predictor.predict_async(data="YourPredictionData"))

    """

    def __init__(
        self,
        service_name: str,
        max_workers: Optional[int] = None,
        endpoint_type: str = EndpointType.INTERNET,
        serializer: Optional[SerializerBase] = None,
        session: Optional[Session] = None,
    ):
        """Construct a `AsyncPredictor` object using an existing async prediction service.

        Args:
            service_name (str): Name of the existing prediction service.
            max_workers (int): The maximum number of threads that can be used to
                execute the given prediction calls.
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

        super(AsyncPredictor, self).__init__(
            service_name=service_name,
            session=session or get_default_session(),
            endpoint_type=endpoint_type,
            serializer=serializer,
        )
        self._max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=self._max_workers)
        self._check()

    @property
    def max_workers(self):
        return self._max_workers

    @max_workers.setter
    def max_workers(self, n: int):
        if hasattr(self, "executor"):
            logger.info("Waiting for all submitted tasks in the queue to complete...")
            self.executor.shutdown()
        self._max_workers = n
        self.executor = ThreadPoolExecutor(max_workers=self._max_workers)

    def __del__(self):
        """wait for all pending tasks to complete before exit."""
        if hasattr(self, "executor"):
            logger.info("Waiting for all pending tasks to complete...")
            self.executor.shutdown()
        super(AsyncPredictor, self).__del__()

    def _check(self):
        config = json.loads(self._service_api_object["ServiceConfig"])
        if config.get("metadata", {}).get("type") != ServiceType.Async:
            logger.warning(
                "AsyncPredictor is not recommended to make prediction to a standard "
                " prediction service."
            )

    def _get_result(
        self, request_id: str
    ) -> Optional[Tuple[int, Dict[str, str], bytes]]:
        resp = self._send_request(
            method="GET",
            path=_QUEUE_SERVICE_SINK_PATH,
            params={
                "requestId": request_id,
                # _raw_ is false because we want to get the encapsulated prediction
                # result in response body.
                "_raw_": "false",
            },
        )
        logger.debug(
            "Poll prediction result: request_id=%s status_code=%s, content=%s",
            request_id,
            resp.status_code,
            resp.content,
        )
        if resp.status_code == 204:
            # Status code 204 means could not find prediction response for the specific
            # request id.
            return

        # Raise exception if status code is not 2xx.
        if resp.status_code // 100 != 2:
            raise RuntimeError(
                "Pulling prediction result failed: status_code={} content={}".format(
                    resp.status_code, resp.content.decode("utf-8")
                )
            )
        return self._parse_encapsulated_response(resp.json()[0])

    def _parse_encapsulated_response(self, data) -> Tuple[int, Dict[str, str], bytes]:
        tags = data["tags"]
        # If the status code from prediction service is not 200, a tag with
        # key 'lastCode' will be added to the tags in response.
        status_code = int(tags.get("lastCode", 200))
        data = base64.b64decode(data["data"])
        # currently, headers are not supported in async prediction service.
        headers = dict()
        return status_code, headers, data

    async def _get_result_async(
        self, request_id: str
    ) -> Optional[Tuple[int, Dict[str, str], bytes]]:
        resp = await self._send_request_async(
            method="GET",
            path=_QUEUE_SERVICE_SINK_PATH,
            params={
                "requestId": request_id,
                # _raw_ is false because we want to get the encapsulated prediction
                # result in response body.
                "_raw_": "false",
            },
        )
        status_code = resp.status
        content = await resp.read()
        logger.debug(
            "Get prediction result: request_id=%s status_code=%s, content=%s",
            request_id,
            status_code,
            content,
        )
        if status_code == 204:
            # Status code 204 means could not find prediction response for the specific
            # request id.
            return
        if status_code // 100 != 2:
            raise RuntimeError(
                "Pulling prediction result failed: status_code={} content={}".format(
                    status_code, content.decode("utf-8")
                )
            )
        data = (await resp.json())[0]
        return self._parse_encapsulated_response(data)

    def _poll_result(
        self, request_id: str, wait_config: WaitConfig
    ) -> Tuple[int, Dict[str, str], bytes]:
        # if max_attempts is negative or zero, then wait forever
        attempts = -1 if wait_config.max_attempts <= 0 else wait_config.max_attempts
        while attempts != 0:
            attempts -= 1
            result = self._get_result(request_id=request_id)
            if not result:
                time.sleep(wait_config.interval)
                continue
            status_code, headers, content = result
            # check real prediction response
            if status_code // 100 != 2:
                raise PredictionException(
                    code=status_code,
                    message=f"Prediction failed: status_code={status_code}"
                    f" content={content.decode()}",
                )
            return status_code, headers, content

        # Polling prediction result timeout.
        raise RuntimeError(
            f"Polling prediction result timeout: request_id={request_id}, "
            f"total_time={wait_config.max_attempts * wait_config.interval}"
        )

    async def _poll_result_async(
        self, request_id, wait_config: WaitConfig
    ) -> Tuple[int, Dict[str, str], bytes]:
        # if max_attempts is negative or zero, then wait forever
        attempts = -1 if wait_config.max_attempts <= 0 else wait_config.max_attempts
        while attempts != 0:
            attempts -= 1
            result = await self._get_result_async(request_id)
            if not result:
                await asyncio.sleep(wait_config.interval)
                continue
            status_code, headers, content = result
            # check real prediction response
            if status_code // 100 != 2:
                raise PredictionException(
                    f"Prediction failed: status_code={status_code} content={content.decode()}"
                )
            return status_code, headers, content

        # Polling prediction result timeout.
        raise RuntimeError(
            f"Polling prediction result timeout: request_id={request_id}, "
            f"total_time={wait_config.max_attempts * wait_config.interval}"
        )

    def _get_request_id(self, resp: requests.models.Response) -> str:
        if resp.status_code // 100 != 2:
            raise RuntimeError(
                f"Send prediction request failed. status_code={resp.status_code} "
                f"message={resp.text}"
            )

        if _QUEUE_SERVICE_REQUEST_ID_HEADER not in resp.headers:
            logger.error(
                f"Send prediction request failed. Missing request id."
                f" status_code={resp.status_code} content={resp.text}"
            )
            raise RuntimeError("Missing request id in response header.")

        request_id = resp.headers[_QUEUE_SERVICE_REQUEST_ID_HEADER]
        logger.debug(
            f"Send prediction request successfully. request_id={request_id}"
            f" status_code={resp.status_code}",
        )
        return request_id

    async def _get_request_id_async(self, resp: aiohttp.ClientResponse) -> str:
        content = await resp.read()
        if resp.status != 200:
            raise RuntimeError(
                "Send request to async prediction service failed: status_code={} "
                "content={}".format(resp.status, content.decode("utf-8"))
            )

        if _QUEUE_SERVICE_REQUEST_ID_HEADER not in resp.headers:
            logger.error(
                f"Send prediction request failed. Missing request id."
                f" status_code={resp.status} content={content.decode()}"
            )
            raise RuntimeError("Missing request id in response header.")
        request_id = resp.headers[_QUEUE_SERVICE_REQUEST_ID_HEADER]
        logger.debug(
            f"Send prediction request successfully. request_id={request_id}"
            f" status_code={resp.status}",
        )
        return request_id

    def _predict_fn(
        self,
        data,
    ):
        """Make a prediction with the async prediction service."""
        # serialize input data
        data = self._handle_input(data)
        resp = self._send_request(data=data)
        request_id = self._get_request_id(resp)
        logger.debug("Async prediction RequestId: ", request_id)
        # poll prediction result
        status, headers, content = self._poll_result(
            request_id=request_id, wait_config=WaitConfig()
        )

        return self._handle_output(content)

    def _wrap_callback_fn(self, cb: Callable):
        """Wrap the callback function to handle the prediction result."""

        @functools.wraps(cb)
        def _(future: Future):
            return cb(future.result())

        return _

    def predict(
        self,
        data,
        callback: Optional[Union[Callable, List[Callable]]] = None,
    ):
        """Make a prediction with the async prediction service.

        The input data is serialized using the `serializer.serialize` method before it
        is sent, and the response body is deserialized using the
        `serializer.deserialize` method the prediction result returns.

        Args:
            data: The input data for the prediction. It will be serialized using the
                serializer of the predictor before transmitted to the prediction
                service.
            callback (Union[Callable, List[Callable]], optional): A Callback function,
                or a list of callback functions used to process the prediction result.

        Returns:
            AsyncTask: The task object that can be used to retrieve the prediction
                result.
        """
        self._post_init_serializer()
        future = self.executor.submit(self._predict_fn, data)

        if isinstance(callback, Callable):
            callback = [callback]

        if callback:
            for cb in callback:
                future.add_done_callback(self._wrap_callback_fn(cb))

        return AsyncTask(future=future)

    async def predict_async(self, data, wait_config: WaitConfig = WaitConfig()):
        """Make a prediction with the async prediction service.

        The serializer object for the predictor is responsible for data transformation
        when the 'predict' method is invoked. The input data is serialized using the
        `serializer.serialize` method before it is sent, and the response is
        deserialized using the `serializer.deserialize` method before the prediction
        result returns.

        Args:
            data: The input data for the prediction. It will be serialized using the
                serializer of the predictor before transmitted to the prediction
                service.
            wait_config (WaitConfig): A config object that controls the behavior of
                polling the prediction result.

        Returns:
            Prediction result.

        """
        self._post_init_serializer()
        data = self._handle_input(data)
        resp = await self._send_request_async(data=data)
        request_id = await self._get_request_id_async(resp)

        status_code, headers, content = await self._poll_result_async(
            request_id=request_id, wait_config=wait_config
        )
        return self._handle_output(content)

    def _raw_predict_fn(self, data, method, path, headers, **kwargs):
        json_data, data = self._handle_raw_input(data)
        resp = self._send_request(
            path=path,
            json=json_data,
            data=data,
            headers=self._build_headers(headers),
            method=method,
            **kwargs,
        )
        request_id = self._get_request_id(resp)
        status, headers, content = self._poll_result(
            request_id, wait_config=WaitConfig()
        )
        return RawResponse(status, headers, content)

    def raw_predict(
        self,
        data: Any = None,
        callback: Optional[Union[Callable, List[Callable], None]] = None,
        method: str = "POST",
        path: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> AsyncTask:
        """Make a prediction with the online prediction service.

        Args:
            data (Any): Input data to be sent to the prediction service. If it is a
                file-like object, bytes, or string, it will be sent as the request body.
                Otherwise, it will be treated as a JSON serializable object and sent as
                JSON.
            callback (Union[Callable, List[Callable]], optional): A Callback function,
                or a list of callback functions used to process the prediction result.
            path (str, optional): Path for the request to be sent to. If it is provided,
                it will be appended to the endpoint URL (Default None).
            headers (dict, optional): Request headers.
            method (str, optional): Request method, default to 'POST'.
            **kwargs: Additional keyword arguments for the request.
        Returns:
            AsyncTask: The task object that can be used to retrieve the prediction
                result.

        Examples:

            from pai.predictor import AsyncPredictor, AsyncTask

            predictor = AsyncPredictor()
            task: AsyncTask = predictor.raw_predict(data="YourPredictionData")
            print(task.result())

        """

        future = self.executor.submit(
            self._raw_predict_fn, data, method, path, headers, **kwargs
        )
        cbs = [callback] if isinstance(callback, Callable) else callback
        if cbs:
            for cb in cbs:
                future.add_done_callback(self._wrap_callback_fn(cb))

        return AsyncTask(future=future)

    async def raw_predict_async(
        self,
        data,
        wait_config: WaitConfig = WaitConfig(),
        method: str = "POST",
        headers: Optional[Dict[str, str]] = None,
        path: Optional[str] = None,
        **kwargs,
    ) -> RawResponse:
        """Make a prediction with the online prediction service.

        Args:
            data (Any): Input data to be sent to the prediction service. If it is a
                file-like object, bytes, or string, it will be sent as the request body.
                Otherwise, it will be treated as a JSON serializable object and sent as
                JSON.
            wait_config (WaitConfig): A config object that controls the behavior of
                polling the prediction result.
            path (str, optional): Path for the request to be sent to. If it is provided,
                it will be appended to the endpoint URL (Default None).
            headers (dict, optional): Request headers.
            method (str, optional): Request method, default to 'POST'.
            **kwargs: Additional keyword arguments for the request.
        Returns:
            RawResponse: Prediction result.

        """
        if self.service_status not in ServiceStatus.completed_status():
            self.wait_for_ready()
        json_data, data = self._handle_raw_input(data)

        resp = await self._send_request_async(
            data=data,
            method=method,
            json=json_data,
            path=path,
            headers=headers,
            **kwargs,
        )
        request_id = await self._get_request_id_async(resp)
        # Polling the prediction result.
        status_code, headers, content = await self._poll_result_async(
            request_id=request_id, wait_config=wait_config
        )
        return self._handle_raw_output(status_code, headers, content)


class LocalPredictor(PredictorBase):
    """Perform prediction to a local service running with docker."""

    def __init__(
        self,
        port: int,
        container_id: Optional[str] = None,
        serializer: Optional[SerializerBase] = None,
    ):
        """LocalPredictor initializer.

        Args:
            port (int): The port of the local service.
            container_id (str, optional): The container id of the local service.
            serializer (SerializerBase, optional): A serializer object that transforms.
        """
        self.container_id = container_id
        self.port = port
        self.serializer = serializer or JsonSerializer()
        self._container_run = (
            self._build_container_run(container_id, port=port)
            if self.container_id
            else None
        )

    @classmethod
    def _build_container_run(cls, container_id, port):
        try:
            import docker
        except ImportError:
            raise ImportError("Please install docker first: pip install docker")
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
            url="http://127.0.0.1:{port}/".format(port=self._container_run.port),
            data=request_data,
        )

        if response.status_code // 100 != 2:
            raise PredictionException(
                code=response.status_code,
                message=response.content,
            )

        return self.serializer.deserialize(response.content)

    def _build_headers(
        self, headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, str]:
        headers = headers or dict()
        headers["User-Agent"] = http_user_agent(headers.get("User-Agent"))
        return headers

    def _build_url(self, path: Optional[str] = None):
        url = "http://127.0.0.1:{}".format(self.port)
        if path:
            if path.startswith("/"):
                path = path[1:]
            url = posixpath.join(url, path)
        return url

    def raw_predict(
        self,
        data: Any = None,
        path: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        method: str = "POST",
        timeout: Optional[Union[float, Tuple[float, float]]] = None,
        **kwargs,
    ) -> RawResponse:
        """Make a prediction with the online prediction service.

        Args:
            data (Any): Input data to be sent to the prediction service. If it is a
                file-like object, bytes, or string, it will be sent as the request body.
                Otherwise, it will be treated as a JSON serializable object and sent as
                JSON.
            path (str, optional): Path for the request to be sent to. If it is provided,
                it will be appended to the endpoint URL (Default None).
            headers (dict, optional): Request headers.
            method (str, optional): Request method, default to 'POST'.
            timeout(float, tuple(float, float), optional): Timeout setting for the
                request (Default 10).
        Returns:
            RawResponse: Prediction response from the service.

        Raises:
            PredictionException: Raise if status code of the prediction response does
                not equal 2xx.
        """
        if isinstance(data, (IOBase, bytes, str)):
            # if data is a file-like object, bytes, or string, it will be sent as
            # request body
            json_data, data = None, data
        else:
            # otherwise, it will be treated as a JSON serializable object and sent as
            # JSON.
            json_data, data = data, None
        header = self._build_headers(headers=headers)
        url = self._build_url(path)
        resp = requests.request(
            url=url,
            json=json_data,
            data=data,
            headers=header,
            method=method,
            timeout=timeout,
            **kwargs,
        )
        resp = RawResponse(
            status_code=resp.status_code,
            content=resp.content,
            headers=dict(resp.headers),
        )
        if resp.status_code // 100 != 2:
            raise PredictionException(resp.status_code, resp.content)
        return resp

    def delete_service(self):
        """Delete the docker container that running the service."""
        if self._container_run:
            self._container_run.stop()

    def wait_for_ready(self):
        self._container_run.wait_for_ready()
        # ensure the server is ready.
        self._wait_local_server_ready()
        time.sleep(5)

    def wait(self):
        return self.wait_for_ready()

    def _wait_local_server_ready(
        self,
        interval: int = 5,
    ):
        """Wait for the local model server to be ready."""
        container_run = self._container_run
        while True:
            try:
                # Check whether the container is still running.
                if not container_run.is_running():
                    raise RuntimeError(
                        "Container exited unexpectedly, status: {}".format(
                            container_run.status
                        )
                    )

                # Make a HEAD request to the server, just test for connection.
                requests.head(
                    f"http://127.0.0.1:{container_run.port}/",
                )
                break
            except requests.ConnectionError:
                # ConnectionError means server is not ready.
                logger.debug("Waiting for the container to be ready...")
                time.sleep(interval)
                continue
