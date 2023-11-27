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

    from pai.model import RegisteredModel
    from pai.estimator import AlgorithmEstimator

    # 获取PAI提供的Bert模型
    m = RegisteredModel("bert-base-uncased", model_provider="pai")
    # 获取模型的微调训练算法
    est: AlgorithmEstimator = m.get_estimator()

    # 查看算法的超参数定义描述、输入定义描述，以及输出定义描述。
    print(est.hyperparameter_definitions)
    # [{'DefaultValue': '1',
    # 'Type': 'Int',
    # 'Description': 'Number of epochs to train the model. Each epoch is one complete iteration over the entire training dataset.',
    # 'Required': True,
    # 'Name': 'max_epochs'},
    # {'DefaultValue': '16',
    # 'Type': 'Int',
    # 'Description': 'Number of samples that will be propagated through the model. A higher value might consume more memory.',
    # 'Required': False,
    # 'Name': 'batch_size'},
    # {'DefaultValue': '0.00001',
    # 'Type': 'Float',
    # 'Description': 'The initial learning rate to be used for training. A higher value usually implies more aggression in gradient updates.',
    # 'Required': False,
    # 'Name': 'learning_rate'},
    # {'DefaultValue': '2000',
    # 'Type': 'Int',
    # 'Description': 'Number of updates steps before two checkpoint.',
    # 'Required': False,
    # 'Name': 'save_steps'}
    # ]
    print(est.input_channel_definitions)
    # [{'Description': 'Input channel for pretrained model to be fine-tuned on.',
    # 'Required': True,
    # 'SupportedChannelTypes': ['oss'],
    # 'Properties': {'ResourceUse': 'Base', 'ResourceType': 'Model'},
    # 'Name': 'model'},
    # {'Description': 'Input channel for training dataset.',
    # 'Required': True,
    # 'SupportedChannelTypes': ['oss'],
    # 'Properties': {'ResourceUse': 'Train', 'ResourceType': 'Dataset'},
    # 'Name': 'train'},
    # {'Description': 'Input channel for validation dataset.',
    # 'Required': False,
    # 'SupportedChannelTypes': ['oss'],
    # 'Properties': {'ResourceUse': 'Validation', 'ResourceType': 'Dataset'},
    # 'Name': 'validation'}]


    # 查看算法的默认输入，包含了预训练模型，训练数据，验证数据等
    training_inputs = m.get_estimator_inputs()
    print(training_inputs)
    # {
    #   'model': 'oss://pai-quickstart-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/huggingface/models/bert-base-uncased/main/',
    #   'train': 'oss://pai-quickstart-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/huggingface/datasets/sst2/main/train.json',
    #   'validation': 'oss://pai-quickstart-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/huggingface/datasets/sst2/main/validation.json'
    # }

    # 使用默认输入进行微调训练
    est.fit(inputs=training_inputs)

    # 查看训练输出的模型，默认模型存储在OSS URI上
    print(est.model_data())


以上的训练任务中，我们使用了PAI提供的公共数据集，对模型进行微调训练。当用户需要使用自己的数据集进行微调训练时，需要先将数据准备到OSS，或是NAS上，然后将数据的OSS或是NAS路径，作为训练任务的输入。


使用用户训练数据集提交训练任务：

.. code-block:: python

    from pai.estimator import AlgorithmEstimator

    # 获取模型的微调训练算法
    est: AlgorithmEstimator = m.get_estimator()
    # 配置修改提交的训练算法超参，具体的超参用途可以查看 est.hyperparameter_definitions 中的描述.
    est.hyperparameters = {
        'max_epochs': 1,
        'batch_size': 8,
        'learning_rate': 2e-05,
        'save_steps': 2000
    }

    # 默认的训练输入
    default_training_inputs = m.get_estimator_inputs()
    # 使用用户的数据集进行微调训练
    training_inputs = {
        # 使用PAI提供预训练模型作为基础模型输入
        "model": default_training_inputs["model"],
        # 使用用户的训练和测试数据集
        "train": "oss://<OssBucketName>/my-dataset/train.json",
        "validation": "oss://<OssBucketName>/my-dataset/validation.json"
    }

    est.fit(inputs=training_inputs)

用户可以通过模型卡片上的文档，查看模型的微调训练数据格式。同时也可以参考相应的模型微调训练的默认输入数据格式，进行数据的准备。

下载PAI数据集到本地目录:

.. code-block:: python

    from pai.common.oss_util import download

    # 默认的训练输入
    default_training_inputs = m.get_estimator_inputs()

    # 下载PAI提供的公共训练数据到本地
    download(default_training_inputs["train"], "./train/")
