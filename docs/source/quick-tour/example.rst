======================
简单示例
======================

本文档以一个简单的 ``PyTorch`` 模型为示例，介绍如何使用 ``PAI Python SDK`` 在PAI平台完成模型开发和部署。

模型开发
-----------------------------------

我们将使用 ``PyTorch`` 编写一个简单模型进行训练，并将代码保存在 ``train_src/train.py``。

训练代码如下:

.. code-block:: python
    :caption: train_src/train.py

    import os
    import torch
    import torch.nn as nn

    class ToyModel(nn.Module):
        """Simple Toy Model"""
        def __init__(self):
            super(ToyModel, self).__init__()

            self.net1 = nn.Linear(10, 10)
            self.relu = nn.ReLU()
            self.net2 = nn.Linear(10, 5)

        def forward(self, x):
            return self.net2(self.relu(self.net1(x)))

    def train(model):
        """mock training loop"""
        pass

    if __name__ == "__main__":
        model = ToyModel()
        train(model)
        # 需要将模型保存到指定目录
        save_model_dir = os.environ.get("PAI_OUTPUT_MODEL")
        # 保存模型
        m = torch.jit.script(model)
        m.save(os.path.join(save_model_dir, "pytorch.pth"))

通过SDK提供的 :class:`~pai.estimator.Estimator`，在配置训练作业使用的镜像、机器规格之后，
我们可以将训练代码提交到PAI执行。

.. code-block:: python
    :caption: submit_job.py

    from pai.estimator import Estimator
    from pai.image import retrieve

    # 配置训练作业
    est = Estimator(
        # 训练作业启动命令
        command="python train.py",
        # 训练作业代码所在目录，对应目录将被上传到OSS Bucket上
        source_dir="train_src/",
        # 训练作业镜像: 使用PAI提供的最新的PyTorch CPU镜像
        image_uri=retrieve(framework_name="PyTorch", framework_version="latest").image_uri,
        # 训练使用的机器实例类型
        instance_type="ecs.c6.xlarge",
    )
    # 提交训练作业到PAI，等待训练完成
    est.fit()
    # 查看输出模型的OSS路径
    print(est.model_data())

训练任务产出的模型默认被保存到用户的OSS bucket中, 可以通过 :meth:`~pai.estimator.Estimator.model_data`
方法获取模型的OSS路径。


部署模型
-----------------------------------

在部署模型之前，我们首先需要准备推理服务的代码，它提供HTTP接口，负责接收预测请求，使用模型进行推理，返回预测结果。

当前示例我们将使用 ``Flask`` 编写一个简单的推理服务，保存为 ``inference_src/app.py`` 文件。

推理服务代码如下:

.. code-block:: python
    :caption: inference_src/app.py

    import json
    from flask import Flask, request
    import os
    import torch
    import numpy as np

    app = Flask(__name__)
    model = None
    # 模型文件路径
    MODEL_PATH = "/eas/workspace/model/"

    def load_model():
        """加载模型"""
        global model
        model = torch.jit.load(os.path.join(MODEL_PATH, "pytorch.pth"))
        model.eval()

    @app.route("/", methods=["POST"])
    def predict():
        data = np.asarray(json.loads(request.data)).astype(np.float32)
        output_tensor = model(torch.from_numpy(data))
        pred_res = output_tensor.detach().cpu().numpy()
        return json.dumps(pred_res.tolist())

    if __name__ == "__main__":
        load_model()
        app.run(host="0.0.0.0", port=int(os.environ.get("LISTENING_PORT", 8000)))


我们将基于PAI提供的 ``PyTorch`` 推理镜像，在PAI创建在线推理服务，示例代码如下：

.. code-block:: python
    :caption: deploy.py

    from pai.model import Model, InferenceSpec, container_serving_spec
    from pai.predictor import Predictor
    from pai.image import retrieve, ImageScope


    m = Model(
        model_data=est.model_data(),
        # 指定模型推理使用的镜像，推理代码，以及依赖的包.
        inference_spec = container_serving_spec(
            # 推理服务的启动命令
            command="python app.py",
            # 推理服务代码所在目录
            source_dir="./inference_src/",
            # 获取PAI提供的PyTorch推理镜像
            image_uri=retrieve(framework_name="PyTorch",
                               framework_version="latest",
                               image_scope=ImageScope.INFERENCE).image_uri,
            # 推理服务的第三方依赖
            requirements=[
                "flask==2.0.0",
                "Werkzeug==2.3.4",
            ],
        )
    )

    # 部署模型到PAI
    p: Predictor = m.deploy(
        service_name="torch_example",
        instance_type="ecs.c6.large"
    )



调用推理服务
------------------------------------

推理服务支持通过HTTP API的方式调用，部署模型返回的 :class:`~pai.predictor.Predictor`
对象指向创建的推理服务，可以通过 :meth:`~pai.predictor.Predictor.raw_predict`
方法向推理服务发送推理请求，拿到预测结果。

.. code-block:: python
    :caption: prediction.py

    import numpy as np

    dummy_input = np.random.rand(1, 10, 10).tolist()
    result = p.raw_predict(
        data = dummy_input,
    )
    print(result.json())

    # 测试完成后删除服务
    p.delete_service()
