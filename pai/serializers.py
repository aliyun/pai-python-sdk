import json
from typing import Any, Dict, List, Tuple, Union

import numpy
import numpy as np
import six
from eas_prediction import TFRequest, TFResponse, TorchRequest
from eas_prediction import pytorch_predict_pb2 as pt_pb
from eas_prediction import tf_request_pb2 as tf_pb


class TensorFlowIOSpec(object):
    def __init__(self, name: str, shape, data_type):
        self.name = name
        self.shape = shape
        self.data_type = data_type


class TorchIOSpec(object):
    def __init__(self, shape=None, data_type=None, index=0):
        self.index = index
        self.shape = shape
        self.data_type = data_type or TorchSerializer.DT_FLOAT

    @classmethod
    def from_dict(cls, data: Dict):
        """Initialize a PyTorchIoSpec from dict.

        Args:
            data: PyTorchIoSpec in dict.

        Returns:
            TorchIOSpec:
        """
        index = data["index"]
        shape = data.get("shape")
        data_type = data.get("data_type")
        return cls(
            index=index,
            shape=shape,
            data_type=data_type,
        )


class BaseSerializer(object):
    def serialize(self, data):
        if isinstance(data, six.string_types):
            return data
        return json.dumps(data)

    def deserialize(self, data):
        return data


class JsonSerializer(BaseSerializer):
    def serialize(self, data):
        if isinstance(data, six.string_types):
            return data
        return json.dumps(data)

    def deserialize(self, data):
        return json.loads(data)


class TensorFlowSerializer(BaseSerializer):

    DT_FLOAT = tf_pb.DT_FLOAT
    DT_DOUBLE = tf_pb.DT_DOUBLE
    DT_INT8 = tf_pb.DT_INT8
    DT_INT16 = tf_pb.DT_INT16
    DT_INT32 = tf_pb.DT_INT32
    DT_INT64 = tf_pb.DT_INT64
    DT_UINT8 = tf_pb.DT_UINT8
    DT_UINT16 = tf_pb.DT_UINT16
    DT_QINT8 = tf_pb.DT_QINT8
    DT_QUINT8 = tf_pb.DT_QUINT8
    DT_QINT16 = tf_pb.DT_QINT16
    DT_QUINT16 = tf_pb.DT_QUINT16
    DT_QINT32 = tf_pb.DT_QINT32
    DT_STRING = tf_pb.DT_STRING
    DT_BOOL = tf_pb.DT_BOOL

    def __init__(
        self,
        input_specs: Union[List[TensorFlowIOSpec], Dict[str, Any]] = None,
        output_fileter: List[str] = None,
        signature_name: str = None,
    ):
        """
        tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY = "serving_default"

        Args:
            pass

        """

        self.input_specs = input_specs
        self.output_fileter = output_fileter or []
        self.signature_name = signature_name

    def serialize(self, data):
        tf_request = TFRequest(signature_name=self.signature_name)
        if isinstance(data, dict):
            for input_spec in self.input_specs:
                tf_request.add_feed(
                    input_spec.name,
                    input_spec.shape,
                    input_spec.data_type,
                    np.ravel(data[input_spec.name]),
                )
        elif len(self.input_specs) == 1:
            tf_request.add_feed(
                self.input_specs[0].name,
                self.input_specs[0].shape,
                self.input_specs[0].data_type,
                np.ravel(data),
            )
        else:
            raise ValueError("Requires to input name for TensorFlow request.")
        if self.output_fileter:
            for name in self.output_fileter:
                tf_request.add_fetch(name)
        return tf_request

    @classmethod
    def from_signature_def(cls, signature_def):
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

        return cls(
            input_specs=input_specs,
            output_fileter=[spec.name for spec in output_specs],
            signature_name=signature_def_key,
        )

    def deserialize(self, response: TFResponse):
        if self.output_fileter:
            output_names = self.output_fileter
        else:
            output_names = response.response.outputs.keys()
        results = {}
        for name in output_names:
            tensor_shape = response.get_tensor_shape(name)
            values = response.get_values(name)
            results[name] = np.reshape(values, tensor_shape)

        return results


class TorchSerializer(BaseSerializer):

    DT_FLOAT = pt_pb.DT_FLOAT
    DT_DOUBLE = pt_pb.DT_DOUBLE
    DT_UINT8 = pt_pb.DT_UINT8
    DT_INT8 = pt_pb.DT_INT8
    DT_INT16 = pt_pb.DT_INT16
    DT_INT32 = pt_pb.DT_INT32
    DT_INT64 = pt_pb.DT_INT64

    def __init__(
        self,
        input_specs: Union[TorchIOSpec, List[TorchIOSpec], Dict] = None,
        output_filter: Union[int, List[int], Tuple[int]] = None,
    ):
        self.input_specs = self._build_input_specs(input_specs)
        self.output_filter = output_filter

    @classmethod
    def _build_input_specs(cls, input_specs):
        if isinstance(input_specs, (TorchIOSpec, Dict)):
            input_specs = [input_specs]
        if not input_specs:
            return []
        results = []
        for s in input_specs:
            if isinstance(s, TorchIOSpec):
                results.append(s)
            elif isinstance(s, Dict):
                results.append(TorchIOSpec.from_dict(s))
            else:
                raise ValueError(
                    "Requires type PyTorchIoSpec or dict for input_specs, but given: {}".format(
                        type(s)
                    )
                )
        return results

    def serialize(self, data):
        request = TorchRequest()

        if not self.input_specs:
            input_spec = TorchIOSpec(
                index=0,
                shape=None,
                data_type=TorchSerializer.DT_FLOAT,
            )
            self._add_input(request, input_spec, data)
        elif len(self.input_specs) == 1:
            self._add_input(request, self.input_specs[0], data)
        else:
            for idx, item in enumerate(data):
                spec = self.input_specs[idx]
                self._add_input(request, spec, item)

        if self.output_filter:
            for idx in self.output_filter:
                request.add_fetch(idx)
        return request

    @classmethod
    def _add_input(cls, request: TorchRequest, spec: TorchIOSpec, data):
        request.add_feed(
            index=spec.index,
            shape=spec.shape or numpy.shape(data),
            content_type=spec.data_type,
            content=np.ravel(data),
        )

    def deserialize(self, data: TFResponse):
        if len(data.response.outputs) > 1:
            results = []
            for idx in range(data.response.outputs):
                tensor_shape = data.get_tensor_shape(idx)
                values = data.get_values(idx)
                results.append(np.reshape(values, tensor_shape))
            return numpy.asarray(results)
        elif len(data.response.outputs) == 1:
            tensor_shape = data.get_tensor_shape(0)
            values = data.get_values(0)
            return np.reshape(values, tensor_shape)
