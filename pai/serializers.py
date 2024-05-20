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

import json
import urllib.request
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.error import HTTPError

import backoff
import numpy
import numpy as np
import six
from eas_prediction import pytorch_predict_pb2 as pt_pb
from eas_prediction import tf_request_pb2 as tf_pb

from .common.logging import get_logger
from .session import Session, get_default_session

logger = get_logger(__name__)


def _is_pil_image(data) -> bool:
    try:
        from PIL import Image

        return isinstance(data, Image.Image)
    except ImportError:
        return False


def _is_numpy_ndarray(data) -> bool:
    try:
        import numpy

        return isinstance(data, numpy.ndarray)
    except ImportError:
        return False


def _is_pandas_dataframe(data) -> bool:
    try:
        import pandas

        return isinstance(data, pandas.DataFrame)
    except ImportError:
        return False


class TensorFlowIOSpec(object):
    def __init__(self, name: str, shape: Tuple, data_type: tf_pb.ArrayDataType):
        """A class represents TensorFlow inputs/outputs spec.

        Args:
            name (str): Name for the spec.
            shape (Tuple): The shape of the input/output value.
            data_type (tf_pb.ArrayDataType): Data type of the value.
        """
        self.name = name
        self.shape = shape
        self.data_type = data_type


class SerializerBase(ABC):
    """Abstract class for creating a Serializer class for predictor."""

    @abstractmethod
    def serialize(self, data) -> bytes:
        """Serialize the input data to bytes for transmitting."""

    @abstractmethod
    def deserialize(self, data: bytes):
        """Deserialize the data from raw bytes to Python object ."""

    def inspect_from_service(
        self, service_name: str, *, session: Optional[Session] = None
    ):
        """Inspect the online prediction service to complete the serializer instance
        initialization.

        The implementation of the `inspect_from_service` method is optional. You only
        need to implement it if your serializer requires additional information from
        service metadata or if it needs to send a request to the service in order to
        be initialized.

        """


class BytesSerializer(SerializerBase):
    """A Serializer object that serialize input data into bytes format and deserialize
    bytes formatted data into python object."""

    def serialize(self, data) -> bytes:
        if isinstance(data, (dict, list, tuple)):
            return json.dumps(data).encode()
        elif isinstance(data, str):
            return data.encode()
        elif isinstance(data, bytes):
            return data
        else:
            return str(data).encode()

    def deserialize(self, data: bytes):
        return data


class JsonSerializer(SerializerBase):
    """A Serializer object that serialize input data into JSON format and deserialize
    JSON formatted data into python object."""

    def serialize(self, data) -> bytes:
        if isinstance(data, six.string_types):
            return data

        if _is_pandas_dataframe(data):
            data = data.to_numpy().tolist()
        elif _is_numpy_ndarray(data):
            data = data.tolist()
        return json.dumps(data).encode()

    def deserialize(self, data):
        return json.loads(data)


class TensorFlowSerializer(SerializerBase):
    """A Serializer class that responsible for transforming input/output data for
    TensorFlow processor service."""

    NUMPY_DATA_TYPE_MAPPING = {
        "DT_FLOAT": np.float32,
        "DT_DOUBLE": np.float64,
        "DT_INT8": np.int8,
        "DT_INT16": np.int16,
        "DT_INT32": np.int32,
        "DT_INT64": np.int64,
        "DT_UINT8": np.uint8,
        "DT_UINT16": np.uint16,
        "DT_BOOL": np.bool_,
        "DT_STRING": np.str_,
    }

    def __init__(
        self,
    ):
        """TensorflowSerializer initializer."""

        self._input_specs = []
        self._output_filter = []
        self._signature_name = None
        super(TensorFlowSerializer, self).__init__()

    def inspect_from_service(
        self, service_name: str, *, session: Optional[Session] = None
    ):
        """Inspect the service to complete serializer instance initialization.

        Args:
            service_name (str): Name of the online prediction service.
            session (:class:`pai.session.Session`):  A PAI session instance used for
                communicating with PAI services.

        """
        session = session or get_default_session()
        sig_def = self.inspect_model_signature_def(service_name, session=session)
        self._init_from_signature_def(sig_def)

    @classmethod
    def inspect_model_signature_def(
        cls, service_name: str, *, session: Session = None
    ) -> Dict[str, Any]:
        """Inspect the TensorFlow serving model signature by sending a request to
        the service.

        TensorFlow processor creates a prediction service and exposes an HTTP API for
        model signature definition.

        Example API returns::

            {
                "signature_name": "serving_default",
                "inputs": [
                    {
                        "name": "flatten_input",
                        "shape": [
                            -1,
                            28,
                            28
                        ],
                        "type": "DT_FLOAT"
                    }
                ],
                "outputs": [
                    {
                        "name": "dense_1",
                        "shape": [
                            -1,
                            10
                        ],
                        "type": "DT_FLOAT"
                    }
                ]
            }

        Returns:
            A dictionary that represents the model signature definition.

        """
        from pai.predictor import ServiceStatus

        session = session or get_default_session()

        service_api_object = session.service_api.get(service_name)
        if service_api_object["Status"] != ServiceStatus.Running:
            raise RuntimeError(
                f"Service is not ready, cannot send request to the service to inspect "
                f"model signature definition: "
                f"name={service_api_object['ServiceName']} "
                f"status={service_api_object['Status']} "
                f"reason={service_api_object['Reason']} "
                f"message={service_api_object['Message']}."
            )

        @backoff.on_exception(
            backoff.expo,
            exception=HTTPError,
            max_tries=3,
            max_time=10,
        )
        def _send_request():
            request = urllib.request.Request(
                url=service_api_object["InternetEndpoint"],
                headers={
                    "Authorization": service_api_object["AccessToken"],
                },
            )
            resp = urllib.request.urlopen(request)
            return resp

        resp = _send_request()
        signature_def = json.load(resp)
        return signature_def

    def serialize(self, data: Union[Dict[str, Any], tf_pb.PredictRequest]) -> bytes:

        if isinstance(data, tf_pb.PredictRequest):
            return data.SerializeToString()

        request = tf_pb.PredictRequest()
        if self._output_filter:
            for output_name in self._output_filter:
                request.output_filter.append(output_name)

        if not isinstance(data, dict):
            if not self._input_specs or len(self._input_specs) > 1:
                raise ValueError(
                    "TensorFlowSerializer accepts a dictionary as input data, "
                    "with each input value having a name."
                )
            else:
                # TensorFlow Processor expects key-value pairs for input data. However,
                # if the input data is not a dictionary and the deployed model accepts
                # exactly one input (by model signature), the key will be inferred
                # from model signature and the current input data will be taken as
                # value.
                value = numpy.asarray(data)
                input_spec = self._input_specs[0]
                if (
                    input_spec.shape
                    and len([dim for dim in input_spec.shape if dim == -1]) == 1
                ):
                    value = value.reshape(input_spec.shape)
                data_type = (
                    input_spec.data_type
                    if input_spec and input_spec.data_type is not None
                    else self._np_dtype_to_tf_dtype(value.dtype.type)
                )
                self._put_value(
                    request=request,
                    name=input_spec.name,
                    data_type=data_type,
                    shape=value.shape,
                    data=np.ravel(value).tolist(),
                )
        else:
            input_specs_dict = (
                {input_spec.name: input_spec for input_spec in self._input_specs}
                if self._input_specs
                else {}
            )
            for name, value in data.items():
                input_spec = input_specs_dict.get(name)
                if not isinstance(value, np.ndarray):
                    value = np.asarray(value)
                data_type = (
                    input_spec.data_type
                    if input_spec and input_spec.data_type is not None
                    else self._np_dtype_to_tf_dtype(value.dtype.type)
                )

                if (
                    input_spec
                    and input_spec.shape
                    and len([dim for dim in input_spec.shape if dim == -1]) == 1
                ):
                    value = value.reshape(input_spec.shape)
                self._put_value(
                    request=request,
                    name=input_spec.name,
                    data_type=data_type,
                    shape=value.shape,
                    data=np.ravel(value).tolist(),
                )

        return request.SerializeToString()

    def _init_from_signature_def(self, signature_def):
        """Build TensorFlowSerializer from signature def.

        Args:
            signature_def: Signature def returns from PAI-EAS tensorflow processor.

        Returns:
            TensorFlowSerializer:
        """
        inputs = signature_def["inputs"]
        signature_def_key = signature_def["signature_name"]
        input_specs = []
        output_specs = []
        for input_def in inputs:
            data_type = tf_pb.ArrayDataType.Value(input_def["type"])
            input_spec = TensorFlowIOSpec(
                name=input_def["name"],
                data_type=data_type,
                # use batch_size=1
                shape=input_def["shape"][1:],
            )
            input_specs.append(input_spec)

        for output_def in signature_def["outputs"]:
            data_type = tf_pb.ArrayDataType.Value(output_def["type"])
            output_spec = TensorFlowIOSpec(
                name=output_def["name"],
                data_type=data_type,
                shape=output_def["shape"],
            )
            output_specs.append(output_spec)

        if not self._signature_name:
            self._signature_name = signature_def_key

        if not self._input_specs:
            self._input_specs = input_specs
        if not self._output_filter:
            self._output_filter = [spec.name for spec in output_specs]

    def deserialize(self, data: bytes):
        response = tf_pb.PredictResponse()
        response.ParseFromString(data)
        output_names = response.outputs.keys()
        results = {}
        for name in output_names:
            results[name] = self._get_value(
                response=response,
                name=name,
            )
        return results

    def _np_dtype_to_tf_dtype(self, np_dtype):
        rev_map = {value: key for key, value in self.NUMPY_DATA_TYPE_MAPPING.items()}
        if np_dtype not in rev_map:
            raise ValueError(
                f"Numpy dtype {np_dtype} is not supported in TensorFlowSerializer."
            )

        return tf_pb.ArrayDataType.Value(rev_map[np_dtype])

    def _tf_dtype_to_np_dtype(self, data_type):
        data_type_name = tf_pb.ArrayDataType.Name(data_type)
        if data_type_name not in self.NUMPY_DATA_TYPE_MAPPING:
            raise ValueError(
                f"Data type {data_type_name} is not supported in TensorFlowSerializer."
            )
        return self.NUMPY_DATA_TYPE_MAPPING.get(data_type_name)

    def _put_value(
        self, request: tf_pb.PredictRequest, name: str, data_type, shape, data
    ):
        request.inputs[name].dtype = data_type
        request.inputs[name].array_shape.dim.extend(shape)

        integer_types = [
            tf_pb.DT_INT8,
            tf_pb.DT_INT16,
            tf_pb.DT_INT32,
            tf_pb.DT_UINT8,
            tf_pb.DT_UINT16,
            tf_pb.DT_QINT8,
            tf_pb.DT_QINT16,
            tf_pb.DT_QINT32,
            tf_pb.DT_QUINT8,
            tf_pb.DT_QUINT16,
        ]
        if data_type == tf_pb.DT_FLOAT:
            request.inputs[name].float_val.extend(data)
        elif data_type == tf_pb.DT_DOUBLE:
            request.inputs[name].double_val.extend(data)
        elif data_type in integer_types:
            request.inputs[name].int_val.extend(data)
        elif data_type == tf_pb.DT_INT64:
            request.inputs[name].int64_val.extend(data)
        elif data_type == tf_pb.DT_BOOL:
            request.inputs[name].bool_val.extend(data)
        elif data_type == tf_pb.DT_STRING:
            request.inputs[name].string_val.extend(data)
        else:
            raise ValueError(
                f"Not supported input data type for TensorFlow PredictRequest: {data_type}"
            )

    def _get_value(self, response: tf_pb.PredictResponse, name):
        output = response.outputs[name]

        if (
            name not in response.outputs
            or tf_pb.DT_INVALID == response.outputs[name].dtype
        ):
            return
        np_dtype = self._tf_dtype_to_np_dtype(response.outputs[name].dtype)
        shape = list(output.array_shape.dim)

        if output.dtype == tf_pb.DT_FLOAT:
            return np.asarray(output.float_val, np_dtype).reshape(shape)
        elif output.dtype in (tf_pb.DT_INT8, tf_pb.DT_INT16, tf_pb.DT_INT32):
            return np.asarray(output.int_val, np_dtype).reshape(shape)
        elif output.dtype == tf_pb.DT_INT64:
            return np.asarray(output.int64_val, np_dtype).reshape(shape)
        elif output.dtype == tf_pb.DT_DOUBLE:
            return np.asarray(output.double_val, np_dtype).reshape(shape)
        elif output.dtype == tf_pb.DT_STRING:
            return np.asarray(output.string_val, np_dtype).reshape(shape)
        elif output.dtype == tf_pb.DT_BOOL:
            return np.asarray(output.bool_val, np_dtype).reshape(shape)
        else:
            raise ValueError(f"Not support data_type: {output.dtype}")


class PyTorchSerializer(SerializerBase):
    """A serializer responsible for transforming input/output data for PyTorch
    processor service.

    """

    NUMPY_DATA_TYPE_MAPPING = {
        "DT_FLOAT": np.float32,
        "DT_DOUBLE": np.float64,
        "DT_INT8": np.int8,
        "DT_INT16": np.int16,
        "DT_INT32": np.int32,
        "DT_INT64": np.int64,
        "DT_UINT8": np.uint8,
        "DT_UINT16": np.uint16,
        "DT_BOOL": np.bool_,
        "DT_STRING": np.str_,
    }

    def __init__(
        self,
    ):
        self._output_filter = []

    def _np_dtype_to_torch_dtype(self, np_dtype):
        """Get PredictRequest data_type from dtype of input np.ndarray."""
        rev_map = {value: key for key, value in self.NUMPY_DATA_TYPE_MAPPING.items()}
        if np_dtype not in rev_map:
            raise ValueError(
                f"Numpy dtype {np_dtype} is not supported in PyTorchSerializer."
            )
        return pt_pb.ArrayDataType.Value(rev_map[np_dtype])

    def _torch_dtype_to_numpy_dtype(self, data_type):
        data_type_name = pt_pb.ArrayDataType.Name(data_type)
        if data_type_name not in self.NUMPY_DATA_TYPE_MAPPING:
            raise ValueError(
                f"Data type {data_type_name} is not supported in PyTorchSerializer."
            )
        return self.NUMPY_DATA_TYPE_MAPPING.get(data_type_name)

    def serialize(self, data: Union[np.ndarray, List, Tuple]) -> bytes:
        request = pt_pb.PredictRequest()
        if _is_pil_image(data):
            data = np.asarray(data)
        elif isinstance(data, (bytes, str)):
            data = np.asarray(data)

        if isinstance(data, np.ndarray):
            # if input data type is np.ndarray, we assume there is only one input data
            # for the prediction request.
            self._put_value(
                request,
                index=0,
                shape=data.shape,
                data_type=self._np_dtype_to_torch_dtype(data.dtype.type),
                data=np.ravel(data).tolist(),
            )
        elif isinstance(data, (List, Tuple)):
            # if input data type is List or Tuple, we assume there is multi input data.
            # for the prediction request.
            for idx, item in enumerate(data):
                if not isinstance(item, np.ndarray):
                    item = np.asarray(item)
                if not item:
                    continue
                self._put_value(
                    request,
                    index=0,
                    shape=item.shape,
                    data_type=self._np_dtype_to_torch_dtype(item.dtype.type),
                    data=np.ravel(item).tolist(),
                )
        else:
            raise ValueError(
                "PyTorchSerializer accept List, Tuple as input request data."
            )
        return request.SerializeToString()

    def deserialize(self, data: bytes):
        resp = pt_pb.PredictResponse()
        resp.ParseFromString(data)
        if len(resp.outputs) > 1:
            results = []
            for idx in range(resp.outputs):
                results.append(self._get_value(resp, idx))
            return results
        elif len(resp.outputs) == 1:
            return self._get_value(resp, index=0)

    def _put_value(
        self, request: pt_pb.PredictRequest, index: int, shape, data_type, data
    ):
        while len(request.inputs) < index + 1:
            request.inputs.add()
        request.inputs[index].dtype = data_type
        request.inputs[index].array_shape.dim.extend(shape)
        if data_type == pt_pb.DT_FLOAT:
            request.inputs[index].float_val.extend(data)
        elif data_type == pt_pb.DT_DOUBLE:
            request.inputs[index].double_val.extend(data)
        elif data_type in (
            pt_pb.DT_INT8,
            pt_pb.DT_INT16,
            pt_pb.DT_INT32,
            pt_pb.DT_UINT8,
        ):
            request.inputs[index].int_val.extend(data)
        elif data_type == pt_pb.DT_INT64:
            request.inputs[index].int64_val.extend(data)
        else:
            raise ValueError(f"Not supported PyTorch request data type: {data_type}")

    def _get_value(self, response: pt_pb.PredictResponse, index: int):
        output = response.outputs[index]
        if output.dtype == pt_pb.DT_INVALID:
            return

        np_dtype = self._torch_dtype_to_numpy_dtype(output.dtype)
        shape = list(output.array_shape.dim)
        if output.dtype == pt_pb.DT_FLOAT:
            return np.asarray(output.float_val, np_dtype).reshape(shape)
        elif output.dtype in (
            pt_pb.DT_INT8,
            pt_pb.DT_INT16,
            pt_pb.DT_INT32,
            pt_pb.DT_UINT8,
        ):
            return np.asarray(output.int_val, np_dtype).reshape(shape)
        elif output.dtype == pt_pb.DT_INT64:
            return np.asarray(output.int64_val, np_dtype).reshape(shape)
        elif output.dtype == pt_pb.DT_DOUBLE:
            return np.asarray(output.double_val, np_dtype).reshape(shape)
        else:
            raise ValueError(
                f"Not supported PyTorch response data type: {output.dtype}"
            )
