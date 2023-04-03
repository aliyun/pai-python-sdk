提交训练作业
==================================

SDK 提供了 HighLevel 的训练 API： :class:`pai.estimator.Estimator` 支持用户提交训练作业到PAI。

使用 ``Estimator`` 提交训练作业的主要流程包括：

- 用户在本地准备训练作业脚本。

- :class:`pai.estimator.Estimator` 配置训练作业的脚本路径，超参，训练镜像，训练资源等训练作业信息。

- 调用 :meth:`pai.estimator.Estimator.fit` , 指定训练数据，提交训练作业。

示例代码如下:

.. code-block:: python

    from pai.estimator import Estimator

    est = Estimator(
        entry_point="<LaunchScript>",
        source_dir="<LocalSourceCodeDirectory>"
        image_uri="<YourTrainingImageUri>"
        instance_type="ecs.c6.xlarge",
        hyperparameters={
            "n_estimators": 500,
            "max_depth": 5,
        },
    )

    est.fit(
        inputs={
            "train_data": "oss://<YourOssBucket>/path/to/train/data/",
        }
    )


以下文档中将围绕使用 ``Estimator`` 提交训练作业，展开做介绍。

准备训练脚本
****************

Estimator 支持将用户编写的本地训练脚本提交到云上执行，用户的作业需要遵循以下规范:

- 训练作业超参读取:

用户通过 ``hyperparameters`` 指定的作业超参会通过 Command Arguments 的方式传递给到训练脚本，用户的训练代码可以通过 Python 的标准库 `argparse <https://docs.python.org/3/library/argparse.html>`_ 进行解析，获取输入超参信息。
``hyperparameters`` 同时也会被保存到 ``/ml/input/config/hyper-parameters.json`` 文件，用户也可以通过超参文件获取输入信息。

- 训练作业模型保存:

训练产出的模型要求写出到 ``/ml/output/model/`` 路径，才能被持久化保存。对应的目录是训练作业的默认输出Channel路径，详细可见训练作业的输入输出。


训练代码示例如下:

.. code-block:: python

    import argparse

    def train(args):
        """用户的模型训练代码"""
        pass

    def save_model():
        """保存模型到 /ml/output/model/ 目录下"""
        pass

    def run():
        # 用户训练作业的超参
        parser = argparse.ArgumentParser(description="XGBoost train arguments")
        parser.add_argument(
            "--n_estimators", type=int, default=500, help="The number of base model."
        )
        parser.add_argument(
            "--objective", type=str, help="Objective function used by XGBoost"
        )

        args, _ = parser.parse_known_args()
        print(vars(args))

        # 作业训练代码，在训练结束之后，写出模型到输出模型路径
        train(args)
        save_model()


    if __name__ == "__main__":
        run()



使用Shell作为启动脚本
--------------------------------

:class:`pai.estimator.Estimator` 提交的训练作业支持使用 Shell 作为训练的启动脚本，作业的超参同样以命令行参数，以及文件的形式传递给到执行的 Shell 脚本

以下示例中，我们通过 Shell 脚本，使用 PyTorch 提供的 `launch utils <https://pytorch.org/docs/stable/distributed.html#launch-utility>`_ 启动 `PyTorch DDP（Distributed Data Parallel） <https://pytorch.org/tutorials/intermediate/ddp_tutorial.html>`_ 训练，将超参信息传递给到模型的训练脚本，训练代码可以通过 arguments 的方式读取到作业超参信息。


.. code-block:: shell

    # filename: run.sh

    # get gpu count
    gpu_count=`nvidia-smi --query-gpu=name --format=csv,noheader | wc -l`
    echo GPU COUNT $gpu_count

    # launch PyTorch DDP
    python -m torch.distributed.launch \
            --master_addr=$MASTER_ADDR \
            --master_port=$MASTER_PORT \
            --nproc_per_node=$gpu_count \
            --nnodes=$WORLD_SIZE \
            --node_rank=$RANK \
            <YOUR_TRAINING_SCRIPT> \
            # passing all arguments (hyperparameters) to the training script
            "$@"

使用以上的 Shell 可以作为一个 PyTorch DDP 训练作业的启动脚本，提交训练作业。

.. code-block:: python


    est = Estimator(
        entry_point="run.sh",       # 使用以上的 shell 作为启动脚本.
        source_dir="./train_src",
        image_uri="<YourTrainingImageURI>"
        instance_count=2,
    )
    est.fit


训练代码的依赖
--------------------

当用户的训练脚本有额外的 Python 包依赖，训练使用的镜像中没有提供时，用户可以通过在训练代码目录下编写 `requirements.txt <https://pip.pypa.io/en/stable/reference/requirements-file-format/>`_ ，相应的三方库依赖会在用户脚本执行前被安装到作业环境中。

.. code-block:: shell

    |-- train_src                       # 用户指定上传的训练脚本目录
        |-- requirements.txt            # 作业的requirements信息
        `-- train.py                    # 训练脚本entry_point
        `-- utils.py


对于以上的目录结构，当用户指定 ``source_dir="./train_src"`` 时， train_src 目录会被打包上传，对应的 ``train_src/requirements.txt`` 会被安装到作业执行环境。


使用PAI提供的公共镜像
************************

用户在通过 :class:`pai.estimator.Estimator` 提交训练作业时，需要指定作业的运行镜像，镜像中需要包含作业脚本的执行依赖，例如使用的机器学习框架。对于常见的机器学习框架，PAI 提供了公共镜像供用户使用，通过 :func:`pai.image.retrieve` 方法，用户可以通过指定机器学习框架的方式，获取 PAI 公共镜像。

.. note::

    用户可以通过 `PAI 公共镜像 <https://help.aliyun.com/document_detail/202834.html>`_ 查看PAI提供的镜像内安装的 Python 三方库信息。

.. code-block:: python

    from pai.image import retrieve, list_images

    # 获取PAI提供TensorFlow, 版本为2.3的CPU训练镜像
    print(retrieve(framework_name="TensorFlow", framework_version="2.3"))

    # 获取PAI提供的最新的TensorFlow的GPU训练镜像
    print(retrieve(framework_name="TensorFlow", framework_version="latest", accelerator="GPU"))

    # 获取PAI提供的机器学习框架镜像
    image_infos = list_images(framework_name="TensorFlow", image_scope=ImageScope.TRAINING)
    for image_info in image_infos:
        print(image_info)



通过 :func:`pai.image.retrieve` 默认返回用于训练的镜像，可以用于提交训练作业。PAI 也提供了用于推理以及开发的镜像，分别可以用于创建推理服务，以及 Notebook 实例，通过 ``image_scope`` 参数可以获得不同应用场景下的镜像。

.. code-block:: python

    from pai.image import retrieve, ImageScope


    # 获取PAI提供PyTorch 1.12版本的CPU推理镜像
    retrieve(framework_name="PyTorch", framework_version="1.12", image_scope=ImageScope.INFERENCE)

    # 获取PAI提供最新的PyTorch CPU开发镜像，支持用户在PAI-DSW创建新的Notebook
    retrieve(framework_name="PyTorch", framework_version="latest", image_scope=ImageScope.DEVELOP)



运行训练作业
********************

用户通过构建 :class:`pai.estimator.Estimator` 指定训练作业的脚本目录，启动脚本，超参，机器资源等，然后通过 ``.fit`` 接口提交训练作业。fit 方法在提交作业之后，会打印训练作业的控制台URL，并持续打印作业的输出日志信息，直到训练作业结束退出（作业状态为成功，失败，或是被停止）。 用户可以通过作业URL，去控制台查看作业执行详情，日志，机器的资源使用情况，训练的Metric信息。

默认 fit 在作业执行完成之后退出，用户可以通过 ``estimator.model_data()`` 获得最后一次提交作业的产出的模型。

示例代码如下:

.. code-block:: python

    from pai.estimator import Estimator
    from pai.image import retrieve

    # 获取PAI支持的最新 XGBoost 镜像
    xgb_image_uri = retrieve("XGBoost").image_uri

    est = Estimator(
        # 训练作业的启动脚本, 在source_dir指定的目录下。
        entry_point="train.py",
        # 训练作业脚本所在目录, 可选。当目录中有 requirements.txt 文件时，对应的依赖会被自动安装，然后再启动用户的训练脚本。
        source_dir="./train_src/",
        # 训练作业使用的镜像
        image_uri=xgb_image_uri,
        # 训练作业使用的机器类型， 支持的机器类型见文档 https://help.aliyun.com/document_detail/171758.html#section-55y-4tq-84y
        instance_type="ecs.c6.xlarge",
        # 训练作业的超参，以命令行 arguments 的方式传递给到训练脚本
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


训练作业的输入输出
********************

Estimator 提交的训练作业，支持用户将数据存储挂载到作业执行容器中，从而支持用户以读写本地文件的方式访问训练数据，或是写出训练产出的模型/Checkpoints。每一个输入输出被称为 ``Channel`` ，包含了实际的数据存储路径地址，以及 Channel 名称。

- 训练作业的输入Channel

:meth:`pai.estimator.Estimator.fit` 的 inputs 参数输入是作业的输入 Channel ，其中Key是输入Channel的名称 (ChannelName)，Value是输入数据的存储路径。目前Estimator支持使用 OSS 或是 NAS 上的数据作为训练作业输入 (格式见以下示例代码)。 对应的输入数据路径会被挂载到 ``/ml/input/data/{ChannelName}`` 路径下。用户的训练作业脚本可以通过读取本地文件的方式获得指定的输入数据。


.. code-block:: python

    estimator.fits(
        inputs={
            # 使用OSS数据作为输入, 对应的输入挂载到 /ml/input/data/train/ 目录
            "train": "oss://{YourOssBucket}/path-to-train-data,
            # 使用NAS上的数据作为输入, 对应的path会被挂载到 /ml/input/data/test/ 目录
            "test": "nas://{YourNasId}.{RegionId}/path—to-test-data,
        }
    )


- 训练作业的输出Channel

通过 Estimator 的 output_path 参数，用户可以指定输出路径的存储路径，当用户没有提供时，则会基于当前使用的 OSS Bucket 生成一个默认的输出存储路径。Estimator 提交的训练作业，默认构建两个输出Channel，分别是 ``model`` 和 ``checkpoints`` ，Estimator 基于 output_path 会分别生成两个存储路径，挂载到容器内的 ``/ml/output/model/`` 和 ``/ml/output/checkpoints/`` 目录。 提交训练作业之后，用户可以通过 :meth:`pai.estimator.Estimator.model_data` 以及 :meth:`pai.estimator.Estimator.checkpoints_data` 方法获取两个输出Channel的数据存储路径。

用户的训练代码需要产出的模型写出到 ``/ml/output/model/`` 路径，产出的模型才能被保存，并且应用于下游的任务。


.. code-block:: python


    est = Estimator(
        entry_point="main.py",
        image_uri="<TrainingImageUri>",
        # 可选, 如果用户没有指定，则使用当前session配置的OSS Bucket生成一个路径
        output_path="oss://{YOUR_BUCKET_NAME}/path/to/training-output/",
    )

    est.fit()

    # model_data() 返回的是作业输出的OSS URI路径，可以用于下游的推理。
    # 对应路径下的数据，是训练脚本写出到 `/ml/output/model`的文件.
    print(estimator.model_data())


完整的训练作业的输入输出目录结构示例，可以见下图:

.. code-block:: shell

    /ml
    |-- usercode                        # 用户代码加载到/ml/usercode目录，这里也是用户代码的工作目录.
    |   |-- requirements.txt
    |   `-- train.py
    |-- input                           # 作业输入数据和配置信息
    |   `-- config
    |       |-- hyper-parameters.json   # 作业的输入超参也可以通过读取 /ml/input/config/hyper-parameters.json 获得
    |   `-- data                        # 作业的InputChannels: 以下目录包含了两个channel: train_data和test_data.
    |       |-- test_data               # /ml/input/data/下的每一个目录表示一个输入channel
    |       |   `-- test.csv
    |       `-- train_data
    |           `-- train.csv
    `-- output                          # 作业的输出Channels: 默认包含两个OutputChannel: model/checkpoints
            `-- model
            `-- checkpoints


训练任务的Metric
********************

在机器学习模型的训练中，依赖于 Metric 追踪训练过程，评估输出模型的性能。PAI的训练服务支持使用正则表达式从训练任务日志中采集模型的Metric。

用户的训练脚本需要将Metric信息打印输出到日志，然后通过 ``Estimator`` 的 ``metric_definitions`` 传递需要捕获的 Metric 的正则表达式。PAI的训练服务会使用这些正则表达式从日志输出中捕获和抽取Metrics，用户既可以在作业的控制台详情页内实时得查看训练任务输出的Metric信息。

.. code-block:: python

    est = Estimator(
        image_uri=image_uri,
        entry_point="train.py",
        instance_type="ecs.c6.large",
        metric_definitions=[
            {
                "Name": "accuracy",
                "Regex": r".*accuracy=([-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?).*",
            },
            {
                "Name": "loss",
                "Regex": r".*loss="
                r"([-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?).*",
            },
        ],
    )



本地执行训练作业
********************

在云上的训练作业调试较为困难，因而 ``Estimator`` 也提供了本地执行的模式，用于方便用户在本地环境中，模拟执行作业，调试相应的脚本。当构建 ``Estimator`` 时，传递的 ``instance_type="local"``，则对应的训练作业会在本地环境中，通过 `docker <https://www.docker.com/products/docker-desktop/>`_ 运行对应的作业，模拟训练作业的执行。


.. note::

    当运行在本地模式下，无法使用 ``NAS`` 类型的数据集，而用户传递的OSS数据集会被下载到本地，然后通过挂载的方式注入到作业环境中。


.. code-block:: python

    estimator = Estimator(
        image_uri=image_uri,
        entry_point="train.py",
        # instance_type=local 表示运行在本地环境。
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
