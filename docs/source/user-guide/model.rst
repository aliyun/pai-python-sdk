======================
部署推理服务
======================

SDK 提供了 HighLevel API，:class:`pai.model.Model` 和 :class:`pai.predictor.Predictor` ，支持用户将模型部署到PAI，以及进行调用测试。

通过 SDK 创建推理服务的基本流程包括:

- 用户通过 :class:`pai.model.InferenceSpec` 描述模型的推理服务配置，包括使用的 Processor 或是镜像的信息。

- 使用 InferenceSpec 实例与待部署的模型文件创建一个 :class:`pai.model.Model` 对象。

- 通过 :meth:`pai.model.Model.deploy` 方法，指定服务使用的资源，服务名称等信息，在PAI创建一个推理服务。

- `deploy` 方法返回 :class:`pai.predictor.Predictor` 对象，提供了 `.predict` 方法向推理服务发送预测请求。

示例代码如下:

.. code-block:: python

    # 1. 使用InferenceSpec描述模型的推理配置信息
    inference_spec = InferenceSpec(
        processor="xgboost",
    )

    # 2. 构建Model对象，用于模型部署
    model = Model(
        # 使用OSS Bucket上的模型文件
        model_data="oss://<YourBucket>/path-to-model-data",
        inference_spec=inference_spec,
    )

    # 3. 部署模型到PAI-EAS，创建在线推理服务，返回Predictor对象
    predictor = m.deploy(
        service_name="example_xgb_service",
        instance_type="ecs.c6.xlarge",
    )

    # 4. 测试推理服务
    res = predictor.predict(data=data)


模型的 ``InferenceSpec``
****************************

`PAI-EAS <https://www.aliyun.com/activity/bigdata/pai/eas>`_ 是PAI提供模型推理服务产品，支持用户将模型部署到PAI创建推理服务。用户可以通过 `Processor <https://help.aliyun.com/document_detail/468735.html>`_  或是 `自定义镜像方式 <https://help.aliyun.com/document_detail/258246.html>`_ 部署推理服务。

SDK 通过 :class:`pai.model.InferenceSpec` 描述模型如何应用于推理的配置，例如使用 Processor 或是镜像部署，运行服务的存储配置，模型服务预热配置，服务的RPC Batch功能配置等， 构建的 `InferenceSpec` 最终会用于推理服务的创建。

使用预置 Processor
------------------------------------

Processor 是 PAI 对于推理服务程序包的抽象描述，它能够基于用户提供的模型，直接构建一个推理服务。PAI提供了预置的Processor，支持一系列常见的机器学习模型格式，包括 `Tensorflow SavedModel <https://www.tensorflow.org/guide/saved_model>`_ ，`PyTorch TorchScript <https://pytorch.org/docs/stable/jit.html>`_ ，`XGBoost <https://xgboost.readthedocs.io/en/stable/tutorials/saving_model.html>`_ ，`LightGBM <https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.Booster.html#lightgbm.Booster.save_model>`_ ，PMML等，完整的介绍请参考文档： `预置Processor使用说明 <https://help.aliyun.com/document_detail/111029.html>`_ 。

对于使用 Processor 方式部署模型，可以参考以下示例配置 InferenceSpec。

.. code-block:: python

    # 使用预置的TensorFlow Processor
    # 有关Tensorflow Processor的详细介绍，请见：https://help.aliyun.com/document_detail/468737.html
    tf_infer_spec = InferenceSpec(processor="tensorflow_cpu_2.3")


    # 使用预置的PyTorch Processor
    # 有关PyTorch Processor的详细介绍，请见：https://help.aliyun.com/document_detail/470458.html
    tf_infer_spec = InferenceSpec(processor="tensorflow_cpu_2.3")

    # 使用预置的XGBoost Processor
    # 相关文档: https://help.aliyun.com/document_detail/470490.html
    xgb_infer_spec = InferenceSpec(processor="xgboost")


用户可以在 InferenceSpec 实例上配置推理服务的更多功能，例如配置服务预热文件，或是服务的RPC配置等，完整的服务参数信息可以见 `服务模型所有相关参数说明文档 <https://help.aliyun.com/document_detail/450525.html>`_ 。

.. code-block:: python

    # 直接配置InferenceSpec的属性
    tf_infer_spec.warm_up_data_path = "oss://<YourOssBucket>/path/to/warmup-data" #  配置服务预热文件路径
    tf_infer_spec.metadata.rpc.keepalive  = 1000 # 配置请求链接的keepalive时长
    tf_infer_spec.model_config = "CustomModelConfig" # 是否开启服务batch功能

    print(tf_infer_spec.warm_up_data_path)
    print(tf_infer_spec.metadata.rpc.keepalive)


使用镜像部署
------------------------------------

使用 Processor 部署模型提供了易用性，但是无法支持用户灵活自定义的述求，例如模型或是推理服务程序有较为复杂的依赖。对于类似的场景，PAI 提供了镜像部署的方式，支持用户以更加灵活自定义的方式部署模型。

用户可以通过将模型服务的代码以及相关的依赖打包构建成一个Docker镜像，然后推送到 `阿里云 ACR 镜像仓库服务 <https://www.aliyun.com/product/acr>`_ ，然后基于以上的Docker镜像构建 InferenceSpec ，用于模型的部署。

.. code-block:: python

    from pai.model import InferenceSpec

    # 通过 `from_serving_container` 方法，用户可以构建一个使用镜像服务模型的InferenceSpec.
    container_infer_spec = InferenceSpec.from_serving_container(
        # 推理服务运行使用的镜像
        image_uri="<CustomImageUri>",
        # 运行在容器内的推理服务需要监听的端口, 用户发送的预测请求会被PAI转发到服务容器的该端口
        port=8000,
        environment_variables=environment_variables,
        # 推理服务的启动命令
        command=command,
        # 推理服务依赖的Python包。
        requirements=[
            "scikit-learn",
        ],
    )

    print(container_infer_spec.to_dict())

    m = Model(
        model_data="oss://<YourOssBucket>/path-to-tensorflow-saved-model",
        inference_spec=custom_container_infer_spec,
    )
    p = m.deploy(
        instance_type="ecs.c6.xlarge"
    )


当通过自定义镜像部署的方式部署模型，默认需要用户将推理服务运行所需的代码准备到运行容器，需要用户构建镜像，并推送到镜像仓库。SDK 提供便利方法，支持用户将本地的代码以及基础镜像的方式构建推理服务。通过调用，:meth:`pai.model.InferenceSpec.from_serving_script` ，用户的本地代码会被上传到OSS上，然后通过挂载的方式准备到运行容器中，用于运行对应的推理服务程序。


.. code-block:: python

    from pai.model import InferenceSpec

    inference_spec = InferenceSpec.from_serving_script(
        # 用户推理服务程序的使用脚本，会通过 python run.py 的方式运行在容器中。
        entry_point="run.py",
        # 用户推理程序所在的本地目录路径，会被上传到OSS Bucket，然后挂载到运行容器中。
        source_dir="./src",
        # 用户的推理服务程序，需要监听该端口。
        # port=8000
        image_uri="<ServingImageUri>",
        requirements=[]
    )
    print(inference_spec.to_dict())


部署在线推理服务
****************

用户使用 InferenceSpec 和模型数据地址 model_data, 构建一个模型对象 :class:`pai.model.Model`，然后通过调用 ``.deploy`` 方法部署模型。``model_data`` 可以是一个OSS URI，也可以是本地路径，对于本地路径的模型，相应的模型文件会被上传到OSS Bucket上，供对应的推理服务拉取使用。

当调用 ``.deploy`` 方法部署模型时，用户需要指定服务所需的资源配置，服务实例个数，服务名称等服务相关参数。

.. code-block:: python

    from pai.model import Model

    model = Model(
        # model_data 模型所在的路径，可以是OSS URI，或是是本地路径
        model_data="oss://<YourBucket>/path-to-model-data",
        inference_spec=inference_spec,
    )

    # 部署到PAI-EAS
    predictor = m.deploy(
        # 推理服务的名称
        service_name="example_xgb_service",
        # 服务使用的机器类型
        instance_type="ecs.c6.xlarge",
        # 机器实例/服务的个数
        instance_count=2,
        # 用户的专有资源组，可选，默认使用公共资源组
        # resource_id="<YOUR_EAS_RESOURCE_GROUP_ID>",
        # 一些高阶参数，详细请见服务参数文档：https://help.aliyun.com/document_detail/450525.html
        options={
            "metadata.rpc.batching": True,
            "metadata.rpc.keepalive": 50000,
            "metadata.rpc.max_batch_size": 16,
            "warm_up_data_path": "oss://<bucket-name>/path-to-warmup-data",
        },
    )

当用户需要根据服务使用的资源数量，例如 CPU，Memory 配置服务时，可以通过 :class:`pai.model.ResourceConfig` 配置每一个服务实例的申请的资源。

.. code-block:: python

    from pai.model import ResourceConfig

    predictor = m.deploy(
        service_name="dedicated_rg_service",
        # 指定单个服务实例使用的CPU和Memory资源
        # 当前示例中，每一个服务使用2个核的CPU，以及4000Mb的内存
        resource_config=ResourceConfig(
            cpu=2,
            memory=4000,
        ),
    )



对于通过 :class:`pai.estimator.Estimator` 训练输出的模型，用户可以直接调用 ``.deploy`` 部署推理服务。

.. code-block:: python

    # Estimator 默认等待到训练作业结束
    estimator.fit()

    # 训练任务结束之后，可以拿到输出模型所在的OSS地址
    print(estimator.model_data())

    # 使用训练作业的模型，构建一个Model
    model: Model = estimator.create_model(
        inference_spec=InferenceSpec(processor="xgboost"),
    )

    # 使用训练作业输出model直接部署。
    estimator.deploy(
        inference_spec=InferenceSpec(processor="xgboost"),
        instance_type="ecs.c6.xlarge",
        service_name="example_xgb_service",
    )



模型的注册和使用
*****************

PAI提供了模型仓库服务，它支持版本化的模型管理，用户可以将训练产出的模型，以及其推理配置信息注册到PAI进行管理。后续用户可以直接使用注册的模型( :class:`pai.model.RegisteredModel` )，填写服务的机器配置等信息，创建一个在线推理服务。

.. code-block:: python

    from pai.model import RegisteredModel

    m = Model(
        model_data = estimator.model_data()
        ## model_data="oss://<bucket-name>/path-to-model-data",
        inference_spec=InferenceSpec(processor="xgboost")
    )

    # 注册模型，保存模型地址以及推理服务配置到PAI模型仓库
    m.register(
        # 模型名称
        name="xgboost_rank_model",
        # 模型版本, 可选
        # 需要遵循语义化版本规则 https://semver.org/
        # 如果默认不填，则会在原先最新的版本基础上增加一个小版本
        version="v1.0.1",
        # 模型使用框架：可选
        framework="TensorFlow",
        # 模型保存的格式类型：可选
        model_format="SavedModel",
        # 模型标签: 可选
        labels={
            "CustomModelLabelKey": "CustomModelLabelValue",
        },
    )

    # 从模型仓库获取注册的模型
    reg_model: RegisteredModel = RegisteredModel(
        name="xgboost_rank_model",
        # 可选，在没有指定具体版本的情况下，则会比较当前模型的所有版本，选择使用最新的模型
        # model_version="v1.0.1",
    )

    # 部署已经注册的模型
    predictor = reg_model.deploy(
        instance_type="ecs.c6.xlarge",
        service_name="example_xgb_service",
    )


调用推理服务
******************

:meth:`pai.model.Model.deploy` 返回新创建的推理服务的 :class:`pai.predictor.Predictor` 对象，他提供了 :meth:`pai.predictor.Predictor.deploy` ，支持向推理服务发送预测请求。

.. code-block:: python

    from pai.predictor import Predictor, EndpointType

    # 创建一个新的推理服务
    predictor = model.deploy(
        instance_type="ecs.c6.xlarge",
        service_name="example_xgb_service",
    )

    # 使用已有的推理服务
    predictor = Predictor(
        service_name="example_xgb_service",
        # 默认使用 INTERNET 公网网络访问，用户可以配置使用 VPC 的网络(需要客户端代码运行在VPC环境下).
        # endpoint_type=EndpointType.INTRANET,
    )

    # .predict 向对应服务发送数据请求，拿到相应结果。输入数据和响应结果会经过serializer处理。
    res = predictor.predict(data_in_nested_list)

    # .raw_predict 接收bytes作为数据请求，通过HTTP POST请求，在Body内传递给到对应的服务，然后直接返回拿到HTTP响应的Body。
    res = predictor.raw_predict(json.dumps(data_in_nested_list))

    # 停止推理服务
    predictor.stop_service()
    # 开始推理服务
    predictor.start_service()
    # 删除推理服务
    predictor.delete_service()



处理推理的输入和输出
******************************************

当使用 SDK 请求推理服务，需要将输入的Python的数据结构序列化，转换为服务能够支持的数据格式进行传输。服务响应返回的数据也同样需要做一次反序列化转为可读，或是可以操作的Python对象。SDK通过 ``Serializer`` 的抽象处理请求和响应数据的序列化以及反序列化。

.. note::

    SDK 里提供的 Serializer 运行在客户端。当用户需要自定义推理服务的数据预处理和预测结果后处理，并且支持不同的客户端调用时，需要用户通过自定义Processor或是镜像部署的方式，自定义推理服务的前处理和后处理。

SDK 提供了一些预置的 Serializer，支持常见的数据的序列化处理，以及 PAI 内置的深度学习 Processor 的输入输出数据处理。

``JsonSerializer``
------------------------------------------

:class:`pai.serializers.JsonSerializer` 支持JSON数据的序列化和反序列化。用户通过 predict 方法传递的 data，可以是 numpy.ndarray，或是一个List，``JsonSerializer.serialize`` 负责将对应的数组序列化为JSON字符串，``JsonSerializer.deserialize`` 则负责将返回的 JSON 数据反序列化为一个Python的List 或是 Dict。

PAI 提供的预置的 XGBoost Processor, PMML Processor 等默认使用 JSON 格式接收数据和响应结果。Predictor 默认使用 JsonSerializer 处理这些 processor 创建的服务的输入输出数据。

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

PAI 提供了 `TensorFlow Processor <https://help.aliyun.com/document_detail/468737.html>`_ ，支持用户将 TensorFlow 的 SavedModel 直接部署到 PAI 创建推理服务。对应的服务的输入输出消息格式是 ProtoBuffer，具体格式可以见定义文件 `tf_predict.proto <https://github.com/pai-eas/eas-golang-sdk/blob/master/eas/types/tf_predict_protos/tf_predict.proto>`_ 。

SDK预置了 :class:`pai.serializers.TensorFlowSerializer` ，支持用户通过传递 ``numpy.ndarray`` 的方式发送请求给到 TensorFlow Processor 的推理服务，Serializer 负责使用对应的 ``numpy.ndarray`` 生成对应的 ProtoBuffer 消息，并将接收的 ProtoBuffer 消息反序列化为 ``numpy.ndarray`` 。


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
--------------------

PAI 提供了预置的 `PyTorch Processor <https://help.aliyun.com/document_detail/470458.html>`_ ，支持用户将使用 `TorchScript 格式 <https://pytorch.org/docs/stable/jit.html>`_ 的模型部署推理服务。使用 PyTorch Processor 启动的推理服务的输入输出使用 ProtoBuffer 传递数据，具体的 proto 文件格式见链接: `pytorch_predict_proto <https://github.com/pai-eas/eas-golang-sdk/blob/master/eas/types/torch_predict_protos/pytorch_predict.proto>`_ 。


SDK 提供了预置的 :class:`pai.serializers.PyTorchSerializer` ，支持用户使用 ``numpy.ndarray`` 发送请求，并将预测结果转换为 ``numpy.ndarray`` ，由 PyTorchSerializer 负责 ProtoBuff 消息和 ``numpy.ndarray`` 的转换。

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
用户可以根据推理服务支持的数据格式,实现所需 Serializer Class，他仅需继承 :class:`pai.serializers.SerializerBase` ，实现 ``serialize`` 和 ``deserialize`` 方法。

以下示例是一个自定义的 NumpySerializer，当predict被调用时，整体的链路:

1. 客户端： 用户传递 numpy.ndarray, 或是 pandas.DataFrame，作为predict的输入，调用 NumpySerializer.serializer 序列化为 ``npy format``，发送给到服务端。
2. 服务端： 推理服务接收的 npy 格式数据，反序列化数据，获得推理结果，然后接输出的结果，序列化为 npy 格式返回。
3. 客户端： 接收到 npy 格式返回，通过 NumpySerializer.deserialize 反序列化为 numpy.ndarray。


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




本地部署模型
*******************

对于自定义镜像部署，SDK提供了本地执行模式（当前不支持使用 Processor 部署的服务），通过在 ``model.deploy`` 中，传递 ``instance_type="local"`` 参数，指定在本地运行推理服务。 SDK通过 ``docker`` 在本地拉起一个模型服务，相应依赖的 OSS 上的模型，会被下载到本地，然后挂载到本地运行的容器镜像中。


.. code-block:: python

    from pai.predictor import LocalPredictor

    p: LocalPredictor = model.deploy(
        # 指定运行在本地.
        instance_type="local",
        serializer=JsonSerializer()
    )

    p.predict(data)

    # 删除对应的docker容器.
    p.delete_service()
