======================
快速开始
======================

用户可以基于 **PAI Python SDK** 在 PAI 使用云上的资源完成模型的训练，部署，端到端得串联机器学习流程。

在本示例中，我们使用 PyTorch 训练模型，将产出的模型部署为在线服务，然后调用测试部署的服务。

安装
-------------------------------------------

请通过以下命令安装 PAI Python SDK（请使用Python >= 3.6）。

.. parsed-literal::

    python -m pip install |release_pkg|



初始化配置
-------------------------------------------

SDK依赖于PAI在阿里云上提供的服务，首次使用需要用户配置访问密钥，使用的工作空间，以及OSS Bucket。请在终端上通过以下命令进行配置。


.. code-block::

    python -m pai.toolkit.config



提交训练作业
-----------------------------------

:class:`pai.estimator.Estimator` 支持将本地的训练脚本提交到云端执行，当前示例中，我们在 PyTorch 提供 `MNIST 示例 <https://github.com/pytorch/examples/blob/main/mnist/main.py>`_ 基础上，修改了模型保存部分的代码，作为训练脚本提交训练。

:download:`点击下载训练脚本 <./resources/torch_mnist/main.py>`

.. code-block:: python

    from pai.estimator import Estimator
    from pai.image import retrieve

    # 获取PAI支持的最新的PyTorch镜像
    torch_image_uri = retrieve(framework_name="PyTorch", accelerator_type="GPU").image_uri

    est = Estimator(
        entry_point="main.py",
        image_uri=torch_image_uri,
        instance_type="ecs.gn6i-c4g1.xlarge", # 4vCPU 15GB 1*NVIDIA T4
        hyperparameters={
            "epochs": 5,
            "batch-size": 64 * 4,
        },
    )
    est.fit()


对于训练作业的详细介绍，可以见文档: :doc:`user-guide/estimator` 。

部署模型
-----------------------------------
:class:`pai.estimator.Estimator` 训练获得的模型默认存储到用户的OSS bucket中，我们将通过 :class:`pai.model.Model` 将训练获得的模型，部署为在线推理服务。

.. code-block:: python

    from pai.model import Model, InferenceSpec
    from pai.predictor import Predictor

    # 使用PAI提供的 PyTorch Processor 加载模型，构建在线服务
    infer_spec = InferenceSpec(processor="pytorch_cpu_1.10")

    m = Model(
        model_data=est.model_data(),
        inference_spec=infer_spec,
    )

    p: Predictor = m.deploy(
        service_name="torch_mnist_example",
        instance_type="ecs.c6.xlarge",
    )

对于模型部署的详细介绍，可以见文档: :doc:`user-guide/model` 。

调用推理服务
------------------------------------

部署模型返回 :class:`pai.predictor.Predictor` 指向创建的推理服务，可以通过 :meth:`pai.predictor.Predictor.predict` 方法向推理服务发送预测请求。


.. code-block:: python

    import numpy as np

    dummy_input = np.random.rand((2, 1, 28, 28)).astype(np.float32)
    result = p.predict(
        data = dummy_input,
    )

    print(result)
    print(np.argmax(result, 1))

    # 测试完成后删除服务
    p.delete_service()
