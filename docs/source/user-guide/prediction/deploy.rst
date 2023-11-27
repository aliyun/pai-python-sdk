========================
部署模型服务
========================

`模型服务PAI-EAS <https://www.aliyun.com/product/bigdata/learn/eas>`_ 是阿里云提供的模型在线服务，支持用户将模型一键部署为在线推理服务，或是AI-Web应用。

本文档介绍如何使用PAI Python SDK通过自定义镜像部署模型推理服务。


模型部署流程
****************************

将模型部署为一个在线服务，用户需要首先准备使用的模型，以及推理服务代码，然后配置运行的环境，包括使用的镜像，运行的机器实例类型等，创建一个推理服务。

通过SDK创建推理服务的示例代码如下:

.. code-block:: python

    from pai.model import InferenceSpec, Model, container_serving_spec
    from pai.image import retrieve, ImageScope

    # 1. 配置模型推理服务使用的镜像，推理服务代码
    # 获取PAI提供的PyTorch最新版本的推理镜像
    torch_image = retrieve("PyTorch", framework_version="latest",
        image_scope=ImageScope.INFERENCE)
    inference_spec = container_serving_spec(
        # 推理服务的启动命令
        command="python app.py",
        # 推理服务使用的本地代码路径
        source_dir="./src/"
        # 使用的推理镜像
        image_uri=torch_image.image_uri,
        # 使用的第三方依赖
        requirements=[
            "flask"
        ]
    )

    # 2. 使用待部署的模型配置一个Model对象
    model = Model(
        # model_data 可以是OSS Bucket上已有的模型，或是本地路径的模型
        model_data="oss://<YourBucket>/path-to-model-data",
        inference_spec=inference_spec,
    )

    # 3. 部署模型到PAI-EAS，创建在线推理服务，返回Predictor对象
    predictor = model.deploy(
        service_name="example_torch_service",
        instance_type="ecs.c6.xlarge",
    )

    # 4. 测试推理服务
    res = predictor.predict(data=data)


准备推理服务代码
****************************

模型推理服务需要能够接受用户的API请求，返回模型预测结果。用户可以通过常见Web服务框架编写一个推理服务，例如使用 `Flask <https://flask.palletsprojects.com/en/2.0.x/>`_ 、`FastAPI <https://fastapi.tiangolo.com/>`_ 等框架编写一个推理服务。

使用Flask框架编写一个推理服务示例代码:

.. code-block:: python
    :caption: app.py

    import json
    from flask import Flask, request
    import os

    app = Flask(__name__)
    model = None
    # 默认模型文件路径
    MODEL_PATH = "/eas/workspace/model/"

    def load_model():
        """加载模型"""


    def predict_fn(data):
        """使用模型处理推理请求"""


    @app.route("/", methods=["POST"])
    def predict():
        data = json.loads(request.data)
        return predict_fn(data)


    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=int(os.environ.get("LISTENING_PORT", 8000)))



基于FastAPI编写推理服务代码：

.. code-block:: python

    import asyncio
    from random import random
    from fastapi import FastAPI, Request
    import uvicorn, json, datetime

    # 默认模型加载路径
    MODEL_PATH = "/eas/workspace/model/"

    app = FastAPI()

    def predict_fn():
        """使用模型处理推理请求"""
        return [random() for _ in range(10)]

    @app.post("/")
    async def create_item(request: Request):
        print("Make mock prediction starting ...")
        # Mock prediction
        return predict_fn()

    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000, workers=1)


创建模型的推理配置
****************************

使用自定义镜像部署的方式部署模型时，需要将推理服务运行所需的代码准备到运行容器、构建镜像并推送到镜像仓库。
SDK提供便利方法，支持将本地的代码以及基础镜像的方式构建推理服务，而无需构建镜像。
:meth:`~pai.model.container_serving_spec` 支持通过指定一个本地代码文件目录（参数 ``source_dir`` ），
SDK会将代码目录打包上传到OSS Bucket，然后将OSS Bucket的路径挂载到运行容器中。用户指定的启动命令可以拉起推理服务。


.. code-block:: python

    from pai.model import container_serving_spec

    inference_spec = container_serving_spec(
        # 用户推理程序所在的本地目录路径，会被上传到OSS Bucket，然后挂载到运行容器，默认为 /ml/usercode/
        source_dir="./src",
        # 服务启动命令。当用户指定了 source_dir，则默认使用 /ml/usercode 作为工作目录执行command。
        command="python run.py",
        # 用户的推理服务程序，需要监听该端口。
        image_uri="<ServingImageUri>",
        # 服务依赖的第三方包，会在服务启动之前安装到容器中。
        requirements=[
            "fastapi",
            "uvicorn",
        ]
    )
    print(inference_spec.to_dict())

当用户有还有更多的数据、代码或是模型准备到推理服务的容器内时，
可以使用 :meth:`~pai.model.InferenceSpec.mount` 方法，将一个本地目录数据或是OSS上的数据路径挂载到在线服务容器中。

.. code-block:: python

    # 将本地的数据上传到OSS，然后挂载到容器的 `/ml/tokenizers` 目录下
    inference_spec.mount("./bert_tokenizers/", "/ml/tokenizers/")

    # 挂载用户存储在OSS Bucket上的数据到容器的 `/ml/data` 目录下
    inference_spec.mount("oss://<YourOssBucket>/path/to/data", "/ml/data/")


使用PAI提供的公共镜像
******************************

PAI提供了一些常见的框架的推理镜像，包括 ``TensorFlow``、``PyTorch``、``XGBoost`` 等，支持用户快速创建推理服务。
用户可以通过 :func:`~pai.image.list_images` ，:func:`~pai.image.retrieve` 方法中传递
``image_scope=ImageScope.INFERENCE`` 获取到相应的推理镜像，然后使用镜像部署的方式部署模型。

.. code-block:: python

    from pai.image import retrieve, ImageScope, list_images

    # 获取PAI提供的所有 PyTorch 推理镜像
    for image_info in list_images(framework_name="PyTorch", image_scope=ImageScope.INFERENCE):
        print(image_info.image_uri)


    # 获取PAI提供的PyTorch 1.12版本的CPU推理镜像
    print(retrieve(framework_name="PyTorch", framework_version="1.12", image_scope=ImageScope.INFERENCE).image_uri)

    # 获取PAI提供的PyTorch 1.12版本的GPU推理镜像
    print(retrieve(framework_name="PyTorch", framework_version="1.12",
        accelerator_type="GPU", image_scope=ImageScope.INFERENCE).image_uri)

    # 获取PAI提供的PyTorch 最新版本的GPU推理镜像
    print(retrieve(framework_name="PyTorch", framework_version="latest",
        accelerator_type="GPU", image_scope=ImageScope.INFERENCE).image_uri)



部署在线推理服务
********************

用户使用推理配置 :class:`~pai.model.InferenceSpec` 和模型数据地址 ``model_data``,
可以构建模型对象 :class:`pai.model.Model`。通过调用模型对象的 :meth:`pai.model.Model.deploy`
方法设置推理服务名称，使用的机器实例等，可以在PAI创建一个推理服务。

.. code-block:: python

    from pai.model import Model

    model = Model(
        # model_data 模型所在的路径，可以是OSS URI，或是是本地路径。对于本地路径的模型，默认会被上传到OSS Bucket上。
        model_data="oss://<YourBucket>/path-to-model-data",
        # 模型推理配置
        inference_spec=container_serving_spec(
            source_dir="./src",
            command="python run.py",
            image_uri="<ServingImageUri>",
            requirements=[
                "fastapi",
                "uvicorn",
            ]
        )
    )

    # 部署到PAI-EAS
    predictor = m.deploy(
        # 推理服务的名称
        service_name="example_xgb_service",
        # 服务使用的机器类型
        instance_type="ecs.c6.xlarge",
        # 机器实例/服务的个数
        instance_count=2,
        # 一些高阶参数，详细请见服务参数文档：https://help.aliyun.com/document_detail/450525.html
        options={
            "metadata.rpc.batching": True,
            "metadata.rpc.keepalive": 50000,
            "metadata.rpc.max_batch_size": 16,
            "warm_up_data_path": "oss://<YourOssBucketName>/path-to-warmup-data",
        },
    )


当部署到用户专有资源组时，可以通过 ``resource_config`` 参数指定每一个服务实例的资源配置。

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
        # 部署到用户的专有资源组
        resource_id="<YOUR_EAS_RESOURCE_GROUP_ID>",
    )

    print(predictor.access_token)
    print(predictor.endpoint)
