========================
调用模型服务
========================

模型推理服务支持通过API的方式调用，获得模型预测结果。

本文档介绍了如何使用PAI Python SDK提供的API调用模型推理服务。

调用服务
******************

:class:`~pai.predictor.Predictor` 对象，指向一个已经存在的推理服务，可以用于操作推理服务，向推理服务发送预测请求。

通过创建新的推理服务，或是使用已有的推理服务的名称，可以获得一个 ``Predictor`` 对象。

.. code-block:: python
    :caption: predict.py

    from pai.predictor import Predictor, EndpointType, RawResponse

    # 部署模型服务，获得一个Predictor对象
    predictor = model.deploy(
        service_name="example_xgb_service",
        instance_type="ecs.c6.xlarge",
    )

    # 使用已有的推理服务
    predictor = Predictor(
        service_name="example_xgb_service",
        # 默认使用公网网络(EndpointType.INTERNET)访问，用户可以配置使用VPC的网络(EndpointType.INTRANET)
        # endpoint_type=EndpointType.INTRANET,
    )

    # 获取推理服务的Endpoint
    print(predictor.endpoint)

    # 获取推理的access_token
    print(predictor.access_token)

    # 停止推理服务
    predictor.stop_service()
    # 开始推理服务
    predictor.start_service()
    # 删除推理服务
    predictor.delete_service()


:class:`~pai.predictor.Predictor` 实例支持向推理服务发送预测请求：

.. code-block:: python

    # predict 方法向对应服务发送数据请求，拿到相应结果。
    # predictor 默认使用JsonSerializer，使用json.dump 序列化预测数据，使用json.load反序列化响应的预测结果。
    res = predictor.predict(data_in_nested_list)
    print(res)

    # raw_predict 方法，提供与 Python requests相似的接口
    # 接收bytes, file-like object，或是其他可以被JSON序列化的对象，作为数据请求，通过HTTP，发送给到预测服务。
    # 返回RawResponse对象，包含HTTP响应的状态码，响应头，响应体等信息。
    response: RawResponse = predictor.raw_predict(
        # 如果输入数据是bytes，或是file-like object，请求数据直接在HTTP请求体内传递。否则则会经过一次JSON序列化，然后放在HTTP请求体内传递。
        data=data_in_nested_list
        # path="predict"            # 如果服务请求是在监听 /predict，则可以通过path参数指定发送给该请求路径
        # headers=dict(),
        # method="POST"
        # timeout=30,
    )
    print(response.status_code)
    print(response.headers)
    print(response.content)
    print(response.json())


使用Serializer处理推理服务的输入和输出
******************************************

当使用 :class:`pai.predictor.Predictor` 请求推理服务，需要将输入的Python的数据结构序列化，转换为服务能够支持的数据格式进行传输。服务响应返回的数据也同样需要做一次反序列化转为可读，或是可以操作的Python对象。SDK通过 ``Serializer`` 的抽象处理请求和响应数据的序列化以及反序列化。

.. note::

    SDK里提供的 ``Serializer`` 运行在客户端。当用户需要自定义推理服务的数据预处理和预测结果后处理，并且支持不同的客户端调用时，需要依赖于推理服务的代码完成推理请求的前后处理。

SDK提供了一些预置的 ``Serializer``，支持常见的数据的序列化处理，以及PAI内置的深度学习Processor的输入输出数据处理。

``JsonSerializer``
------------------------------------------


:class:`pai.serializers.JsonSerializer` 支持 ``JSON`` 数据的序列化和反序列化。用户通过 :meth:`pai.predictor.Predictor.predict` 方法传递的 ``data``，可以是 ``numpy.ndarray``，或是一个 ``List``，``JsonSerializer.serialize`` 负责将对应的数组序列化为 ``JSON`` 字符串，``JsonSerializer.deserialize`` 则负责将返回的JSON字符串反序列化为一个Python对象。


PAI提供的预置的XGBoost Processor、PMML Processor等默认使用 ``JSON`` 格式接收数据和响应结果。``Predictor`` 默认使用 ``JsonSerializer`` 处理这些processor创建的服务的输入输出数据。

.. code-block:: python

    from pai.serializers import JsonSerializer

    # 在`.deploy`方法指定返回的predictor使用的serializer
    p = Model(
        inference_spec=InferenceSpec(processor="xgboost"),
        model_data="oss://<YourOssBucket>/path-to-xgboost-model"
    ).deploy(
        instance_type="ecs.c6.xlarge",
        # 可选: 使用 XGBoost processor 的 service 默认使用 JsonSerializer
        serializer=JsonSerializer()
    )

    # 或是直接创建Predictor时指定对应的 serializer
    p = Predictor(
        service_name="example_xgb_service"
        serializer=JsonSerializer(),
    )

    # 预测的返回结果也是一个list
    res = p.predict([[2,3,4], [4,5,6]])


``TensorFlowSerializer``
-----------------------------

PAI提供了 `TensorFlow Processor <https://help.aliyun.com/document_detail/468737.html>`_ ，支持用户将 ``TensorFlow SavedModel`` 格式的模型直接部署到PAI创建推理服务。对应的服务的输入输出消息格式是Protocol Buffers，具体格式可以见定义文件 `tf_predict.proto <https://github.com/pai-eas/eas-golang-sdk/blob/master/eas/types/tf_predict_protos/tf_predict.proto>`_ 。

SDK预置了 :class:`pai.serializers.TensorFlowSerializer` ，支持用户通过传递 ``numpy.ndarray`` 的方式发送请求给到 ``TensorFlow Processor`` 的推理服务， ``Serializer`` 负责使用对应的 ``numpy.ndarray`` 生成对应的Protocol Buffers消息，并将接收的Protocol Buffers消息反序列化为 ``numpy.ndarray`` 。


.. code-block:: python

        # 创建一个TensorFlow processor 服务.
        tf_predictor = Model(
            inference_spec=InferenceSpec(processor="tensorflow_cpu_2.7"),
            model_data="oss://<YourOssBucket>/path-to-tensorflow-saved-model"
        ).deploy(
            instance_type="ecs.c6.xlarge",
            # 可选: 使用 TensorFlow processor 的 service 默认使用 TensorFlowSerializer
            # serializer=TensorFlowSerializer(),
        )

        # 使用TensorFlow processor启动的服务，支持用户通过API获取模型的服务签名
        print(tf_predictor.inspect_signature_def())

        # TensorFlow processor的输入要求一个Dict，Key是模型输入签名的名称，Value是具体的输入数据。
        tf_result = tf_predictor.predict(data={
            "flatten_input": numpy.zeros(28*28*2).reshape((-1, 28, 28))
        })

        assert result["dense_1"].shape == (2, 10)

``PyTorchSerializer``
---------------------------

PAI提供了预置的 `PyTorch Processor <https://help.aliyun.com/document_detail/470458.html>`_ ，支持用户将使用 `TorchScript 格式 <https://pytorch.org/docs/stable/jit.html>`_ 的模型部署推理服务。使用PyTorch Processor启动的推理服务的输入输出使用Protocol Buffers传递数据，具体的proto文件格式见链接: `pytorch_predict_proto <https://github.com/pai-eas/eas-golang-sdk/blob/master/eas/types/torch_predict_protos/pytorch_predict.proto>`_ 。


SDK提供了预置的 :class:`pai.serializers.PyTorchSerializer` ，支持用户使用 ``numpy.ndarray`` 发送请求，并将预测结果转换为 ``numpy.ndarray`` ，由 ``PyTorchSerializer`` 负责Protocol Buffers消息和 ``numpy.ndarray`` 的转换。

.. code-block:: python


        # 创建一个使用 PyTorch processor 服务.
        torch_predictor = Model(
            inference_spec=InferenceSpec(processor="pytorch_cpu_1.10"),
            model_data="oss://<YourOssBucket>/path-to-torch_script-model"
        ).deploy(
            instance_type="ecs.c6.xlarge",
            # 可选: 使用 PyTorch processor 的 service 默认使用 PyTorchSerializer
            # serializer=PyTorchSerializer(),
        )

        # 1. 用户需要注意将对应的输入数据 reshape 成模型支持的形状。
        # 2. 如果有多个输入数据，则需要使用List/Tuple传递，列表中的每一项是numpy.ndarray
        torch_result = torch_predictor.predict(data=numpy.zeros(28 * 28 * 2).reshape((-1, 28, 28)))
        assert torch_result.shape == (2, 10)


自定义Serializer
------------------
用户可以根据推理服务支持的数据格式,实现所需 Serializer Class，仅需继承 :class:`pai.serializers.SerializerBase` ，实现 ``serialize`` 和 ``deserialize`` 方法。

以下示例是一个自定义的 NumpySerializer，当predict被调用时，整体的链路如下:

1. 客户端： 用户传递 ``numpy.ndarray``, 或是 ``pandas.DataFrame`` ，作为predict的输入，调用 ``NumpySerializer.serializer`` 序列化为 ``npy format``，发送给到服务端。
2. 服务端： 推理服务接收的 ``npy`` 格式数据，反序列化数据，获得推理结果，然后接输出的结果，序列化为 ``npy`` 格式返回。
3. 客户端： 接收到 ``npy`` 格式返回，通过 ``NumpySerializer.deserialize`` 反序列化为 ``numpy.ndarray``。


.. code-block:: python

    import pandas as pd
    import numpy as np
    import io

    class NumpySerializer(SerializerBase):

        def serialize(self, data: Union[np.ndarray, pd.DataFrame, bytes]) -> bytes:
            """Serialize input python object to npy format"""
            if isinstance(data, bytes):
                return data
            elif isinstance(data, str):
                return data.encode()
            elif isinstance(data, pd.DataFrame):
                data = data.to_numpy()

            res = io.BytesIO()
            np.save(res, data)
            res.seek(0)
            return res.read()

        def deserialize(self, data: bytes) -> np.ndarray:
            """Deserialize prediction response to numpy.ndarray"""
            f = io.BytesIO(data)
            return np.load(f)


    # 创建一个使用 PyTorch processor 服务.
    predictor = Model(
        inference_spec=infer_spec,
        model_data="oss://<YourOssBucket>/path-to-torch_script-model"
    ).deploy(
        instance_type="ecs.c6.xlarge",

        # 使用自定义的serializer
        serializer=NumpySerializer(),
    )

    res: predictor.predict(data=input_data)

    assert isinstance(input_data, numpy.ndarray)
    assert isinstance(res, numpy.ndarray)
