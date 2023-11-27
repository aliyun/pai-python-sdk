===================
准备模型训练代码
===================

在模型开发过程中，开发者可以使用 ``PyTorch``，``TensorFlow``，``XGBoost``，``ScikitLearn``
等机器学习框架编写模型训练代码，然后通过执行训练代码，完成模型训练。

当训练代码被提交到PAI执行时，PAI会按照训练作业规范准备超参，和训练输入数据，然后运行训练代码。

本文档将介绍提交到PAI运行的训练代码的最佳实践，包括如何获取超参，读取输入数据，保存输出模型等。


训练作业超参
*****************

在机器学习中，算法开发者通常需要训练任务提交之前，设置任务的超参，例如学习率，迭代次数，训练batch的大小等。
PAI支持通过 :class:`~pai.estimator.Estimator` 的 ``hyperparameters`` 参数配置训练作业的超参，
训练代码可以通过读取文件或是环境变量的方式获取到设置的超参。

以下示例中，训练作业的超参为 ``{"batch_size": 32, "learning_rate": 0.01}``。

.. code-block:: python
    :emphasize-lines: 6,7,8,9
    :caption: submit_job.py

    est = Estimator(
        command="python train.py",
        # 待上传执行的代码目录
        source_dir="<YourTrainingCodeDir>",
        image_uri="<TrainingImageUir>",
        instance_type="ecs.c6.xlarge",
        # 训练作业超参
        hyperparameters={
            "batch_size": 32,
            "learning_rate": 0.01,
        }
    )

超参会以一个JSON文件的形式准备到训练作业环境中。

.. code-block:: json
    :caption: /ml/input/config/hyperparameters.json

    {
        "batch_size": "32",
        "learning-rate": "0.01"
    }


读取超参文件
-------------------------------

通过读取 ``/ml/input/config/hyperparameters.json`` 文件， 训练代码可以获取到当前作业配置的超参。

.. code-block:: python
    :caption: train.py

    import os

    # 超参文件存储路径
    hp_path = "/ml/input/config/hyperparameters.json"
    # 也可以通过环境变量的方式获取到超参路径
    # hp_path = os.path.join(os.environ.get("PAI_CONFIG_DIR"), "hyperparameters.json")

    # 读取超参信息
    with open(hp_path, "r") as f:
        hps = json.load(f)
    print(hps)



使用 ``argparse`` 读取超参
-------------------------------

训练作业默认会注入环境变量 ``PAI_USER_ARGS``，以 ``argparse`` 的方式拼接了超参，例如
``{"batch_size": 32, "learning_rate": 0.01}`` 超参信息，``PAI_USER_ARGS`` 环境变量的值为
``--batch_size 32 --learning_rate 0.01``。

通过在启动命令中使用 ``PAI_USER_ARGS`` 环境变量，可以将超参以 ``argparse`` 的方式传递给训练脚本，
示例代码如下：


.. code-block:: python
    :emphasize-lines: 4

    est = Estimator(
        # 在启动命令中引用环境变量 PAI_USER_ARGS
        # 最终的启动命令为: python train.py --batch_size 32 --learning_rate 0.01 --training_method lora
        command="python train.py $PAI_USER_ARGS",
        image_uri="<TrainingImageUir>",
        instance_type="ecs.c6.xlarge",
        hyperparameters={
            "batch_size": 32,
            "learning_rate": 0.01,
            "training_method": "lora"
        }
    )


训练代码中可以通过 ``argparse`` 读取超参，示例代码如下：

.. code-block:: python
    :caption: train.py

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--learning_rate", type=float, default=0.01)
    parser.add_argument("--training_method", type=str, default="lora")
    args = parser.parse_args()

    print(args.batch_size)
    print(args.learning_rate)
    print(args.training_method)


读取输入数据
*****************

模型开发过程中，依赖使用数据完成模型训练、测试、评估等任务。PAI支持开发者使用云上的存储，包括OSS、NAS、MaxCompute表等，作为训练作业的输入数据。
在提交训练作业时，可以通过 :meth:`~pai.estimator.Estimator.fit` 方法的 ``inputs`` 参数传递训练数据。
``inputs`` 参数是一个字典， 其中Key是输入数据的名称 (Name)，Value是输入数据的存储路径，例如以下示例:

.. code-block:: python

    # 提交训练作业
    estimator.fit(
        # 训练作业有两个输入数据，分别为'train'和'test'
        inputs={
            "train": "oss://<YourOssBucket>/train/data/train.csv",
            "test": "oss://<YourOssBucket>/test/data/",
        }
    )


- OSS/NAS类型的数据默认以挂载的方式准备到训练作业中，训练代码可以通过 ``/ml/input/data/{channel_name}``
  目录直接读取到NAS/OSS存储上的数据。

- 使用MaxCompute表的数据时，PAI会将元数据信息以及访问凭证写入到训练作业环境中，从而支持用户使用 ``PyODPS`` 等工具读取数据。

对于如何使用数据详细的介绍，可以见文档: :doc:`/user-guide/training/use-data`。


保存训练模型
***************

在训练任务完成之后，作业使用的机器实例会被释放，因而需要将训练得到的模型保存到持久化存储中。
在提交训练作业时，PAI会生成一个OSS路径，挂载到训练作业的 ``/ml/output/model/`` 目录，作为模型保存目录。
训练代码可以通过将模型写出到 ``/ml/output/model`` 目录，从而将模型保存到OSS。
在提交训练任务之后，通过 :meth:`pai.estimator.EstimatorBase.model_data` 方法，
可以获取到输出模型所在的OSS路径，示例如下:

.. code-block:: python

    from pai.estimator import Estimator

    estimator = Estimator(
        command="python train.py",
        source_dir="<YourTrainingCodeDir>",
        image_uri="<TrainingImageUri>",
    )
    estimator.fit()

    # 获取输出模型的OSS路径
    print(estimator.model_data())


以下训练代码中，将一个 ``PyTorch`` 模型保存到指定的模型保存目录。

.. code-block:: python
    :caption: train.py

    import os
    import torch
    import torch.nn as nn

    class ToyModel(nn.Module):
        def __init__(self):
            super(ToyModel, self).__init__()

            self.net1 = nn.Linear(10, 10)
            self.relu = nn.ReLU()
            self.net2 = nn.Linear(10, 5)

        def forward(self, x):
            return self.net2(self.relu(self.net1(x)))


    def __init__
        model = ToyModel()
        train(model)
        # 模型保存目录
        save_model_dir = "/ml/output/model/"
        # 通过环境变量获取模型保存目录
        # save_model_dir = os.environ.get("PAI_OUTPUT_MODEL")
        # 将模型保存到指定
        torch.save(model.state_dict(), os.path.join(save_model_dir, "model.pth"))


当使用HuggingFace ``transformers`` 库提供的Trainer进行训练，可以通过 `trainer.save_model <https://huggingface.co/docs/transformers/main_classes/trainer#transformers.Trainer.save_model>`_ 保存模型。

.. code-block:: python
    :caption: train.py

    from transformers import Trainer

    # init
    trainer = Trainer(
        # the instantiated 🤗 Transformers model to be trained
        model=model,
        # more training args...
    )
    # training loop
    trainer.train()

    output_model_dir = "/ml/output/model/"
    # after training, save the model.
    trainer.save_model(output_dir=output_model_dir)


附录：训练作业预置环境变量
******************************

用户在PAI提交的训练作业需要按规范读取超参、获取数据路径，以及写出模型到指定路径。
PAI的训练服务会将这些信息以环境变量的形式注入到训练作业的容器中，用户可以在训练脚本，
或是训练作业的启动命令 ``Estimator`` 的 ``command`` 参数，通过环境变量获取到超参、输入数据路径、保存模型路径等信息。


PAI_HPS_{hyperparameter_name}
------------------------------------------------

单个训练作业超参的值，会以环境变量的形式注入到训练作业的容器中。对于超参名中，环境变量中不支持的字符（默认的环境变量仅支持使用字母、数字、以及下划线），会被替换为下划线。

例如用户指定了超参 ``{"epochs": 10, "batch-size": 32, "train.learning_rate": 0.001}``, 对应的环境变量信息为以下:

.. code-block:: shell

    PAI_HPS_EPOCHS=10
    PAI_HPS_BATCH_SIZE=32
    PAI_HPS_TRAIN_LEARNING_RATE=0.001


PAI_USER_ARGS
------------------------------------------------

训练作业的所有超参信息，会以 ``PAI_USER_ARGS`` 环境变量，使用 ``--{hyperparameter_name} {hyperparameter_value}`` 的形式，注入到训练作业的容器中。

例如训练作业指定了超参 ``hyperparameters={"epochs": 10, "batch-size": 32, "learning-rate": 0.001`` ，则 ``PAI_USER_ARGS`` 环境变量的值为:


.. code-block:: shell

    PAI_USER_ARGS="--epochs 10 --batch-size 32 --learning-rate 0.001"


PAI_HPS
------------

用户的训练作业的超参信息，会以JSON格式，通过 ``PAI_HPS`` 环境变量注入到训练作业的容器中。

例如用户传递了超参 ``{"epochs": 10, "batch-size": 32}`` ，则 ``PAI_HPS`` 环境变量的值为:

.. code-block:: shell

    PAI_HPS={"epochs": 10, "batch-size": 32}


PAI_INPUT_{channel_name}
------------------------------------------------

训练作业的输入数据，会以挂载的形式，挂载到训练作业执行环境中，用户可以通过读取本地文件的方式读取到OSS、NAS上的数据。对于每一个输入的数据，会以 ``PAI_INPUT_{channel_name}`` 的环境变量，注入到训练作业的容器中。


.. code-block:: shell

    PAI_INPUT_TRAIN=/ml/input/data/train/
    PAI_INPUT_TEST=/ml/input/data/test/test.csv

对应的数据存储路径会被挂载到容器中，用户可以通过这些本地路径信息，直接读取到输入的数据。


PAI_OUTPUT_{channel_name}
------------------------------------------------

默认训练作业会创建三个个输出 ``Channel``，分别为 ``model``、``checkpoints``，以及 ``logs``，
分别用于存储模型输出、训练checkpoints和TensorBoard logs。
每一个Channel对应一个OSS URI，以及对应的挂载路径。
用户可以通过 ``PAI_OUTPUT_{channel_name}`` 环境变量，获取到对应的文件路径。

.. code-block:: shell

    PAI_OUTPUT_MODEL=/ml/output/model/
    PAI_OUTPUT_CHECKPOINTS=/ml/output/checkpoints/
    PAI_OUTPUT_TENSORBOARD=/ml/output/tensorboard/

通过将需要保存的模型，或是checkpoints，保存到这些路径下，PAI的训练服务会自动将这些文件上传到相应的OSS路径下。


附录：训练作业目录结构
**************************

完整的训练作业的输入输出目录结构示例，可以见下图:

.. code-block:: shell

    /ml
    |-- usercode                        # 用户代码加载到/ml/usercode目录，这里也是用户代码的工作目录. 可以通过环境变量 `PAI_WORKING_DIR` 获得.
    |   |-- requirements.txt
    |   `-- train.py
    |-- input                           # 作业输入数据和配置信息
    |   `-- config                      # config目录包含了作业的配置信息, 可以通过 `PAI_CONFIG_DIR` 获取.
    |       |-- hyperparameters.json    # 训练作业超参文件
    |   `-- data                        # 作业的InputChannels: 以下目录包含了两个channel: train_data和test_data.
    |       |-- test_data
    |       |   `-- test.csv
    |       `-- train_data
    |           `-- train.csv
    `-- output                          # 作业的输出Channels，Estimator提交的训练作业默认包含三个OutputChannel: model/checkpoints/logs
            `-- model                   # 通过环境变量 `PAI_OUTPUT_{CHANNEL_NAME}` 可以获输出路径.
            `-- checkpoints
            `-- logs
