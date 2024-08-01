=====================
使用预训练模型
=====================

本文介绍如何使用PAI提供的预训练模型，进行模型部署和微调训练。

预训练模型（pre-trained model）是通过在大规模数据集上进行训练，从而学习到数据的特征表示的深度学习模型。
因为模型是通过大规模的数据进行预训练，因而可以通过少量的数据集进行训练，避免从头训练模型的高额成本。
在应用时，预训练模型可以被作为基础模型，然后在特定任务的有标注数据集上进行微调，从而适应特定任务的要求。

PAI在公共模型仓库中，提供了不同领域，包括计算机视觉、自然语言处理、语音等常见的热门预训练模型，
例如 ``Bert``、``ChatGLM``、``LLama2``、``StableDiffusion 1.5`` 等，
支持用户在PAI上基于这些预训练模型进行微调训练，或是直接部署模型服务。


查看PAI提供的预训练模型
********************************

我们可以通过参数 ``model_provider`` 为 ``pai``，获取公共模型仓库下的模型。
``model_provider=pai`` 的公共模型仓库中的模型，里面包含了 ``pai`` 团队提供的模型，也包含一些热门的社区模型，
支持用户在PAI上快速部署模型服务，或是基于这些模型进行微调训练。

通过 `阿里云PAI控台 <https://pai.console.aliyun.com/>`_ 的 **快速开始** 入口，用户可以查看PAI提供的预训练模型列表。
通过这些模型卡片，用户可以查看模型的详细介绍，包括模型推理服务的输入输出格式，以及模型微调训练的数据格式。


查看公共模型仓库模型列表代码示例：

.. code-block:: python

    from pai.model import RegisteredModel

    # 列出所有的 model_provider=pai 下的模型
    for m in RegisteredModel.list(model_provider="pai"):
        print(m)


部署模型服务
********************************

PAI公共模型仓库中的模型，默认包含了模型部署信息 :class:`pai.model.InferenceSpec`，
它包含了模型推理服务使用的镜像，推理服务代码等信息。用户指定模型服务使用的机器资源，服务名称即可将模型部署为在线服务。


以 ``bert-base-uncased`` 模型为示例部署模型推理服务：

.. code-block:: python

    from pai.model import RegisteredModel

    # 获取PAI提供的Bert模型
    m = RegisteredModel("bert-base-uncased", model_provider="pai")

    # 当前模型配置使用的Task
    # bert模型配置的Task是 text-classification，可以用于文本分类任务
    print(m.task)

    # 查看模型的部署配置
    print(m.inference_spec)


    # 用户配置使用的机器实例资源，以及服务名称，即可将模型部署为在线服务
    p = m.deploy(
        # 服务名称
        service_name="bert_example",
        # 机器实例类型
        instance_type="ecs.c6.xlarge",
    )

    # 调用模型推理服务
    res = p.predict(
        {
            "data": "weather is good, but I am not happy."
        }
    )
    print(res)
    # [{'label': 'negative', 'score': 0.9699936509132385}]


使用预训练模型进行微调训练
********************************

PAI公共仓库中的部分模型，也提供了微调训练算法，支持用户提供自己的数据集，能够基于预训练模型进行微调训练。

以 ``bert-base-uncased`` 模型为示例，使用PAI提供的算法进行微调训练的示例代码如下。
训练任务将使用情感分类公开数据集 `sst2 <https://huggingface.co/datasets/sst2>`_ ，对模型进行微调，从而获得一个情感分类模型。

.. code-block:: python

    from pai.model import RegisteredModel, ModelTrainingRecipe

    # 获取PAI提供的Bert模型
    m = RegisteredModel("bert-base-uncased", model_provider="pai")
    training_recipe = m.training_recipe()

    training_recipe = ModelTrainingRecipe(
        model_name = "bert-base-uncased",
        model_provider = "pai",
        instance_type = "ecs.c6.xlarge",
        # 训练任务的超参数
        hyperparameters={
            "max_epochs": 1,
            "learning_rate": 0.00001,
            "batch_size": 16,
            "save_steps": 2000,
        },
    )

    # 查看模型微调算法输入定义
    print(training_recipe.input_channels)
    # 查看模型微调算法超参数定义
    print(training_recipe.hyperparameter_definitions)
    # 查看默认训练输入数据
    print(training_recipe.default_inputs)

    # 提交微调训练作业
    job = training_recipe.train(
        job_name="train_recipe_example",
        # 配置使用用户在OSS Bucket上的数据作为训练数据
        # inputs={
        #     "train": "oss://<YourOssBucket>/<Path/to/Data>"
        # }
    )
    # 获取微调后模型路径
    print(training_recipe.model_data())

    # 使用PAI提供的推理服务配置部署模型
    predictor = training_recipe.deploy(
        service_name="bert_example",
    )

用户可以通过PAI ModelGallery提供的模型卡片上的文档，查看具体模型模型的微调训练数据格式。
