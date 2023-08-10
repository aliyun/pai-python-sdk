提交训练作业
==================================

PAI Python SDK提供了更易用的API，支持用户提交训练作业到PAI，使用云上资源运行。当前文档主要介绍用户如何准备训练作业脚本，以及如何使用SDK提交训练作业。

概要介绍
********************
SDK提供了HighLevel的训练API： :class:`pai.estimator.Estimator` 支持用户提交训练作业到PAI。

使用 ``Estimator`` 提交训练作业的主要流程包括：

- 用户准备训练作业脚本。

- 使用 :class:`pai.estimator.Estimator` 配置使用的训练脚本、作业启动命令、超参、训练镜像、训练资源等作业信息。

- 通过 :meth:`pai.estimator.Estimator.fit` 方法, 指定训练数据，提交训练作业。

示例代码如下:

.. code-block:: python

    from pai.estimator import Estimator

    # 通过 Estimator 配置训练作业的信息
    est = Estimator(
        command="<LaunchCommand>"
        source_dir="<SourceCodeDirectory>"
        image_uri="<TrainingImageUri>"
        instance_type="<TrainingInstanceType>",
        hyperparameters={
            "n_estimators": 500,
            "max_depth": 5,
        },
    )

    # 指定训练数据，提交训练作业
    est.fit(
        inputs={
            "train_data": "oss://<YourOssBucket>/path/to/train/data/",
        }
    )

    # 获取输出模型路径
    print(est.model_data())


以下文档将围绕使用 ``Estimator`` 提交训练作业，展开做介绍。

准备训练脚本
****************

``Estimator`` 支持将用户编写的本地训练脚本提交到云上执行，PAI的训练服务会按一定的规范准备训练作业环境，运行训练脚本。

用户准备的训练代码示例如下:

.. code-block:: python

    import argparse

    def train(hps, train_data, test_data):
        """用户的模型训练代码"""
        pass

    def save_model(model):
        """保存模型"""
        # 通过环境变量获取输出模型路径，默认为 `/ml/output/model/`
        output_model_path = os.environ.get("PAI_OUTPUT_MODEL")

        # 将模型写出到 output_model_path 路径下 ..
        pass

    def load_hyperparameters():
        """读取输入超参"""
        # 通过环境变量 PAI_CONFIG_DIR 获取超参保存目录，默认为 `/ml/input/config/`
        hps_path = os.path.join(os.environ.get("PAI_CONFIG_DIR"), "hyperparameters.json")
        with open(hps_path, "r") as f:
            hyperparameters = json.load(f)
        return hyperparameters

    def run():
        # 1. 加载用户训练作业的超参
        hps = load_hyperparameters()
        print("Hyperparameters: ", hps)

        # 2. 训练作业的输入数据
        # 通过est.fit()方法用户可以指定存储在 NAS 或是 OSS 上训练数据，将数据准备到训练容器中。
        # 训练脚本可以通过环境变量（PAI_INPUT_{CHANNEL_NAME}）获取输入数据的本地路径.
        train_data = os.environ.get("PAI_INPUT_TRAIN")
        test_data = os.environ.get("PAI_INPUT_TEST")

        model = train(hps, train_data, test_data)

        # 3. 作业训练代码，在训练结束之后，写出模型到输出模型路径
        save_model(model)


    if __name__ == "__main__":
        run()


用户的训练脚本需要遵循规范，读取超参，输入数据，然后在训练结束后写出模型。

- 训练作业超参:

当用户通过 :class:`pai.estimator.Estimator` 的 ``hyperparameters`` 参数配置了训练作业的超参，超参文件 ``hyperparameters.json`` 会被准备到 ``PAI_CONFIG_DIR`` 环境变量指定目录下（默认为 ``/ml/input/config/``)。训练作业脚本可以通过读取 ``{PAI_CONFIG_DIR}/hyperparameters.json`` 文件获取到相应的超参。

例如用户传递的训练作业超参为 ``hyperparameters={"batch_size": 32, "learning_rate": 0.01}``，则超参文件 ``{PAI_CONFIG_DIR}/hyperparameters.json`` 内容为:

.. code-block:: json

    {
        "batch_size": "32",
        "learning-rate": "0.01"
    }


- 训练作业的输入数据

用户可以通过 :meth:`pai.estimator.Estimator.fit` 的 ``inputs`` 参数指定训练所需的输入数据，输入参数需要是一个Dict， 其中Key是输入数据的名称 (ChannelName)，Value是输入数据的存储路径，例如以下示例:

.. code-block:: python

    estimator.fits(
        inputs={
            "train": "oss://<YourOssBucket>/train/data/train.csv",
            "test": "oss://<YourOssBucket>/test/data/",
        }
    )

对应的输入数据路径会被挂载到 ``/ml/input/data/{ChannelName}`` 路径下，用户的训练代码可以通过环境变量 ``PAI_INPUT_{ChannelName}`` 获取到数据的本地路径，用户的训练作业脚本可以通过读取本地文件的方式获得指定的输入数据。以上的示例中，我们能够通过 ``PAI_INPUT_TRAIN`` 和 ``PAI_INPUT_TEST`` 环境变量获取到输入的OSS URI对应的本地路径。



- 训练作业模型保存:

训练作业的输出模型需要写出到指定路径，才能将模型持久化保存。用户可以通过 ``PAI_OUTPUT_MODEL`` 环境变量获取到模型保存路径（默认为 ``/ml/output/model`` ），然后将模型写出到对应路径。


获取PAI提供的公共镜像
************************

用户在通过 :class:`pai.estimator.Estimator` 提交训练作业时，需要指定作业的运行镜像，镜像中需要包含作业脚本的执行依赖，例如使用的机器学习框架。对于常见的机器学习框架，PAI提供了公共镜像供用户使用，通过 :func:`pai.image.retrieve` 方法，用户可以通过指定机器学习框架的方式，获取PAI提供的公共镜像。

.. note::

    用户可以通过 `PAI 公共镜像文档 <https://help.aliyun.com/document_detail/202834.html>`_ 查看 PAI 提供的镜像内安装的 Python 三方库信息。

.. code-block:: python

    from pai.image import retrieve, list_images, ImageScope


    # 获取PAI提供的所有 PyTorch 训练镜像
    for image_info in list_images(framework_name="PyTorch"):
        print(image_info)

    # 获取PAI提供的 TensorFlow 2.3版本的CPU训练镜像
    print(retrieve(framework_name="TensorFlow", framework_version="2.3"))

    # 获取PAI提供的最新的TensorFlow的GPU训练镜像
    # 通过参数 framework_version="latest"，retrieve 方法会返回最新的 TensorFlow 镜像
    print(retrieve(framework_name="TensorFlow", framework_version="latest",
        accelerator_type="GPU"))

    # 获取PAI提供的PyTorch 1.12版本的GPU训练镜像
    print(retrieve(framework_name="PyTorch", framework_version="1.12",
         accelerator_type="GPU"))


安装训练代码的依赖
********************

当用户的训练脚本有额外的Python包依赖，训练使用的镜像中没有提供时，用户可以通过在训练代码目录下编写 `requirements.txt <https://pip.pypa.io/en/stable/reference/requirements-file-format/>`_ ，相应的三方库依赖会在用户脚本执行前被安装到作业环境中。

例如以下示例中，用户准备了训练脚本目录, `train_src`，可以在对应的目录下准备所需的 `requirements.txt`，然后在 Estimator 构建时指定 ``source_dir="train_src"`` 。 ``train_src`` 目录会被打包上传，对应的依赖 ``train_src/requirements.txt`` 会在训练脚本运行前安装到作业执行环境。


.. code-block:: shell

    |-- train_src                       # 用户指定上传的训练脚本目录
        |-- requirements.txt            # 作业的requirements信息
        `-- train.py                    # 训练脚本，用户可以通过 python train.py 的命令拉起脚本
        `-- utils.py



运行训练作业
********************

用户通过构建 :class:`pai.estimator.Estimator` 指定训练作业的脚本目录、启动脚本、超参、机器资源等，然后通过 ``.fit`` 接口提交训练作业。``fit`` 方法在提交作业之后，会打印训练作业的控制台URL，并持续打印作业的输出日志信息，直到训练作业结束退出（作业状态为成功，失败，或是被停止）。 用户可以通过作业URL，去控制台查看作业执行详情，日志，机器的资源使用情况，训练作业的Metrics等信息。

默认 ``fit`` 方法在作业执行完成之后退出，用户可以通过 ``estimator.model_data()`` 获得提交作业的产出的模型的OSS路径。

示例代码如下：

.. code-block:: python

    from pai.estimator import Estimator
    from pai.image import retrieve

    # 获取PAI支持的最新 PyTorch 镜像
    torch_image_uri = retrieve("PyTorch", accelerator_type="GPU").image_uri

    est = Estimator(
        # 训练作业的启动命令
        command="python train.py",
        # 训练作业脚本， 可以是一个本地目录相对路径或是绝对路径，或是 OSS 上的tar包（例如 oss://<YourOssBucket>/your-code-path-to/source.tar.gz）
        # 当目录中有 requirements.txt 文件时，对应的依赖会被自动安装，然后再启动用户的训练脚本。
        source_dir="./train_src/",
        # 训练作业使用的镜像
        image_uri=torch_image_uri,
        # 训练作业使用的机器类型， 支持的机器类型见文档 https://help.aliyun.com/document_detail/171758.html#section-55y-4tq-84y
        instance_type="ecs.c6.xlarge",
        # 训练作业的超参
        hyperparameters={
            "n_estimators": 500,
            "objective": "reg:squarederror",
            "max_depth": 5,
        },
        # 训练作业名称前缀，用户提交的训练作业使用的Name为 `{base_job_name}_{submitted-datetime}`
        base_job_name="example_train_job",
    )

    # 提交训练作业，同时打印训练作业的Web详情页URL。fit 调用默认等待到作业终止（成功，失败，会是被停止）。
    est.fit()

    # 输出的模型路径
    est.model_data()


使用TensorBoard
******************************

`TensorBoard <https://www.tensorflow.org/tensorboard/get_started>`_ 是一个用于机器学习实验的可视化工具包，他支持用户跟踪和可视化机器学习实验指标，例如损失和准确性、可视化模型图、查看直方图、显示图像等。PAI支持使用TensorBoard可视化云上训练作业的训练过程，用户可以在训练脚本中将TensorBoard日志写出到指定的路径，然后可以通过PAI提供的TensorBoard服务，查看训练作业写出的日志。

训练脚本写出TensorBoard日志的示例代码如下：

.. code-block:: python

    import torch
    from torch.utils.tensorboard import SummaryWriter
    import os

    # 训练脚本需要将TensorBoard日志写出到环境变量PAI_OUTPUT_LOGS指定的目录下
    writer = SummaryWriter(log_dir=os.environ.get("PAI_OUTPUT_LOGS"))

    writer.add_scalar("train/loss", 0.1, 1)
    writer.add_image("train/image", torch.rand(3, 64, 64), 1)
    writer.flush()


用户可以通过 ``Estimator`` 的 ``tensorboard`` 方法，在PAI上启动一个TensorBoard应用，查看训练作业的TensorBoard日志。

.. code-block:: python

    estimator = Estimator(
        image_uri="<TrainingImageUri>",
        entry_point="train.py",
        instance_type="<TrainingInstanceType>",
    )
    estimator.fit(wait=False)

    # 启动TensorBoard服务，查看训练作业的TensorBoard日志
    estimator.tensorboard()

    # 查看TensorBoard 应用的控制台链接
    print(tensorboard.app_uri)

    # 在使用完成之后，删除TensorBoard应用
    tensorboard.delete()


.. note::

    在PAI使用TensorBoard的账号和权限要求可以参考帮助文档 `创建及管理Tensorboard应用 <https://help.aliyun.com/zh/pai/user-guide/create-and-manage-tensorboard-tasks>`_ 。每一个阿里云子账号下最多能够创建5个TensorBoard应用，如果超出限制，创建时会返回 ``TensorboardLimitExceeded`` 错误，用户需要先停止或是删除之前创建的TensorBoard任务。


本地执行训练作业
********************

在云上的训练作业调试较为困难，因而 ``Estimator`` 也提供了本地执行的模式，用于方便用户在本地环境中，模拟执行作业，调试相应的脚本。当构建 ``Estimator`` 时，传递的 ``instance_type="local"``，则对应的训练作业会在本地环境中，通过 `docker <https://www.docker.com/products/docker-desktop/>`_ 运行对应的作业，模拟训练作业的执行。


.. code-block:: python

    estimator = Estimator(
        image_uri=image_uri,
        entry_point="train.py",
        # instance_type="local" 表示运行在本地环境。
        instance_type="local",
    )

    estimator.fit(
        inputs={
            # local 模式下，OSS上的数据会被下载到本地，然后挂载到工作容器内。
            "train": "oss://<BucketName>/path-to-data/",
            # local 模式下，支持本地文件数据，对应的数据会被挂载到相应的channel目录
            "test": "/data/to/test/data"
        }
    )

    # 返回一个本地的模型输出目录
    print(estimator.model_data())




附录：训练作业预置环境变量
******************************


用户在PAI提交的训练作业需要按规范读取超参、获取数据路径，以及写出模型到指定路径。PAI的训练服务会将这些信息以环境变量的形式注入到训练作业的容器中，用户可以在训练脚本，或是训练作业的启动命令 ``Estimator.command``，通过环境变量获取到超参、输入数据路径、保存模型路径等信息。


PAI_HPS_{HYPERPARAMETER_NAME}
------------------------------------------------

单个训练作业超参的值，会以环境变量的形式注入到训练作业的容器中。对于超参名中，环境变量中不支持的字符（默认的环境变量仅支持使用字母、数字、以及下划线），会被替换为下划线。

例如用户指定了超参 ``{"epochs": 10, "batch-size": 32, "train.learning_rate": 0.001}``, 对应的环境变量信息为以下:

.. code-block:: shell

    PAI_HPS_EPOCHS=10
    PAI_HPS_BATCH_SIZE=32
    PAI_HPS_TRAIN_LEARNING_RATE=0.001

用户可以在训练启动命令中直接引用这些环境变量，例如:

.. code-block:: python

    est = Estimator(
        command="python train.py --epochs $PAI_HPS_EPOCHS --batch-size $PAI_HPS_BATCH_SIZE",
        hyperparameters={
            "epochs": 10,
            "batch-size": 32,
        },
        # more arguments for estimator..
    )

以上的方式传递的参数，训练脚本 ``train.py`` 可以通过标准库 `argparse <https://docs.python.org/3/library/argparse.html>`_ 库获取输入参数。


PAI_USER_ARGS
------------------------------------------------

训练作业的所有超参信息，会以 ``PAI_USER_ARGS`` 环境变量，使用 ``--{hyperparameter_name} {hyperparameter_value}`` 的形式，注入到训练作业的容器中。

例如训练作业指定了超参 ``hyperparameters={"epochs": 10, "batch-size": 32, "learning-rate": 0.001`` ，则 ``PAI_USER_ARGS`` 环境变量的值为:


.. code-block:: shell

    PAI_USER_ARGS="--epochs 10 --batch-size 32 --learning-rate 0.001"


用户可以在启动命令中引用环境变量，例如以下的实例中，训练作业脚本会以 ``python train.py --epochs 10 --batch-size 32 --learning-rate 0.001`` 的命令执行。

.. code-block:: python

    est = Estimator(
        command="python train.py $PAI_USER_ARGS",
        hyperparameters={
            "epochs": 10,
            "learning-rate": 0.001
            "batch-size": 32,
        },
        # more arguments for estimator..
    )

PAI_HPS
------------

用户的训练作业的超参信息，会以JSON格式，通过 ``PAI_HPS`` 环境变量注入到训练作业的容器中。

例如用户传递了超参 ``{"epochs": 10, "batch-size": 32}`` ，则 ``PAI_HPS`` 环境变量的值为:

.. code-block:: shell

    PAI_HPS={"epochs": 10, "batch-size": 32}


PAI_INPUT_{channel_name}
------------------------------------------------

训练作业的输入数据，会以挂载的形式，挂载到训练作业执行环境中，用户可以通过读取本地文件的方式读取到 OSS，NAS 上的数据。对于每一个输入的数据，会以 ``PAI_INPUT_{channel_name}`` 的环境变量，注入到训练作业的容器中。

例如用户 `est.fit(inputs={"train": "oss://<BucketName>/path-to-data/", "test": "oss://<BucketName>/path-to/data/test.csv"})`，对应的环境变量如下：

.. code-block:: shell

    PAI_INPUT_TRAIN=/ml/input/data/train/
    PAI_INPUT_TEST=/ml/input/data/test/test.csv

对应的数据存储路径会被挂载到容器中，用户可以通过这些本地路径信息，直接读取到输入的数据。


.. note::

    ``PAI_INPUT_{ChannelName}`` 指向用户传入的数据路径，如果用户指定一个OSS目录（以 "/" 结尾），则 PAI的训练服务会将输入存储作为目录进行挂载，环境变量指向对应的数据目录。如果用户传递了一个OSS文件路径，PAI的训练服务会挂载对应的文件目录，环境变量会指OSS URI对应的实际文件。

    例如以上示例中 ``train`` 是一个输入文件，test 是一个输入目录，那么 ``PAI_INPUT_TRAIN`` 指向 ``/ml/input/data/train/train.csv``， ``PAI_INPUT_TEST`` 指向 ``/ml/input/data/test/``。



PAI_OUTPUT_{channel_name}
------------------------------------------------

默认训练作业会创建两个输出 ``Channel``，分别为 ``model`` 和 ``checkpoints``，分别用于存储模型输出和训练checkpoints。每一个Channel对应一个OSS URI，以及对应的挂载路径。用户可以通过 ``PAI_OUTPUT_{channel_name}`` 环境变量，获取到对应的文件路径。

.. code-block:: shell

    PAI_OUTPUT_MODEL=/ml/output/model/
    PAI_OUTPUT_CHECKPOINTS=/ml/output/checkpoints/


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
    |       |-- hyperparameters.json    # 训练作业超参.
    |   `-- data                        # 作业的InputChannels: 以下目录包含了两个channel: train_data和test_data.
    |       |-- test_data
    |       |   `-- test.csv
    |       `-- train_data
    |           `-- train.csv
    `-- output                          # 作业的输出Channels: 默认包含两个OutputChannel: model/checkpoints
            `-- model                   # 通过环境变量 `PAI_OUTPUT_{CHANNEL_NAME}` 可以获输出路径.
            `-- checkpoints
            `-- logs
