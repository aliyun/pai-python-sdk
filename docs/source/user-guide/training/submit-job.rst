===================
提交训练作业
===================

SDK提供了HighLevel的训练API： :class:`~pai.estimator.Estimator` 支持用户提交训练作业到PAI，使用示例如下。

.. code-block:: python

    from pai.estimator import Estimator
    from pai.model import container_serving_spec

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

    # 下载模型到本地
    est.create_model().download("./model/")


本文档将介绍通过SDK配置和提交训练作业。

使用训练脚本
*****************

通过 :class:`~pai.estimator.Estimator` 的 ``source_dir`` 参数，
算法开发者可以配置需要上传执行的训练代码目录。在训练作业提交之后，
相应的代码会被上传到用户OSS，在训练作业启动之前被下载到训练作业的执行环境中。

用户训练代码目录示例:

.. code-block:: shell

    |-- train_src         # 用户指定上传的训练脚本目录
        `-- train.py        # 训练脚本，用户可以通过 python train.py 的命令拉起脚本
        `-- utils.py


通过 ``Estimator`` 设置使用的训练代码目录（可以是绝对路径或是相对路径）。

.. code-block:: python

    est = Estimator(
        command="python train.py",
        # 可以通过相对路径或是绝对路径的方式指定代码.
        source_dir="train_src/",
        source_dir="/home/foo/code/train_src/",
    )

训练代码会被下载到作业执行环境的 ``/ml/usercode`` 目录下，作业启动命令的工作目录也是 ``/ml/usercode`` 目录。

.. code-block:: shell

    |-- /ml/usercode/       # 训练作业代码所在目录。
        `-- train.py
        `-- utils.py

用户也可以通过传递一个OSS Bucket路径，作为训练代码。

.. code-block:: python

    from pai.common.oss_utils import upload

    # 上传代码到OSS，返回一个OSS URI
    code_uri = upload(
        local_path="./train_src/",
        oss_path="path/for/code/"
    )
    # code_uri: oss://<YourOssBucket>/path/for/code/

    est = Estimator(
        command="python train.py",
        # 使用OSS上的训练代码
        source_dir=code_uri,
    )


配置训练作业镜像
*****************

在提交执行训练作业时，用户需要配置作业运行使用的镜像 ( :class:`~pai.estimator.Estimator` 的 ``image_uri``
参数），镜像内包含训练作业执行所需的依赖，例如Python、CUDA、机器学习框架、以及依赖的第三方库等，从而支持训练代码运行。

用户可以配置使用阿里云镜像仓库内的镜像，也可以使用PAI提供的公共镜像（推荐）。对于常见的机器学习框架，PAI提供了公共镜像供用户使用，用户可以通过以下的代码获取镜像信息：

.. note::

    用户可以通过PAI `公共镜像文档 <https://help.aliyun.com/zh/pai/user-guide/public-images>`_ 查看PAI提供的镜像内安装的Python三方库信息。

.. note::

    企业版容器镜像服务ACR默认需要通过用户的VPC访问镜像仓库，具体请参考文档： `配置专有网络的访问控制 <https://help.aliyun.com/zh/acr/user-guide/configure-access-over-vpcs>`_。
    训练作业的机器实例位于云产品PAI的VPC环境内，需要通过配置 :class:`~pai.estimator.Estimator` 的 ``user_vpc_config`` 参数，将训练作业实例与用户VPC网络进行连接，训练作业才能通过用户VPC访问到企业版镜像仓库，拉取镜像。


.. code-block:: python

    from pai.image import retrieve, list_images

    # 获取PAI提供的最新的PyTorch的GPU训练镜像
    # 通过参数 framework_version="latest"，retrieve 方法会返回最新的 PyTorch 镜像
    print(retrieve(framework_name="TensorFlow", framework_version="latest",
        accelerator_type="GPU"))

    # 获取PAI提供的 TensorFlow 2.3版本的CPU训练镜像
    print(retrieve(framework_name="TensorFlow", framework_version="2.3"))

    # 获取PAI提供的PyTorch 1.12版本的GPU训练镜像
    print(retrieve(framework_name="PyTorch", framework_version="1.12",
        accelerator_type="GPU"))


    # 获取PAI提供的所有 PyTorch 训练镜像
    for image_info in list_images(framework_name="PyTorch"):
        print(image_info)




安装训练代码依赖
************************************************

当训练代码有额外的Python包依赖，可以通过在训练代码目录下编写 `requirements.txt <https://pip.pypa.io/en/stable/reference/requirements-file-format/>`_ ，相应的三方库依赖会在用户脚本执行前被安装到作业环境中。

配置使用 ``requirements.txt`` 的训练代码目录示例如下：

.. code-block:: shell

    |-- train_src                       # 训练作业配置使用的脚本目录
        |-- requirements.txt            # 作业的requirements信息
        `-- train.py
        `-- utils.py



执行训练作业
*****************

用户通过构建 :class:`~pai.estimator.Estimator` 指定训练作业的脚本目录、启动脚本、超参、机器资源等，
然后通过 :meth:`~pai.estimator.Estimator.fit` 方法提交训练作业。在提交作业之后，SDK会打印训练作业的控制台URL，
并持续打印作业的输出日志信息，直到训练作业结束退出（作业状态为成功，失败，或是被停止）。

用户可以通过作业URL，去控制台查看作业执行详情、日志、机器的资源使用情况、以及训练作业的Metrics等信息。
在作业执行完成之后退出，可以通过 :meth:`~pai.estimator.Estimator.model_data` 方法获得提交作业的产出的模型的OSS路径。

示例代码如下：

.. code-block:: python

    from pai.estimator import Estimator
    from pai.image import retrieve

    # 获取PAI支持的最新 PyTorch 镜像
    torch_image_uri = retrieve("PyTorch", accelerator_type="GPU").image_uri

    est = Estimator(
        # 训练作业的启动命令
        command="python train.py",
        # 训练作业脚本所在目录
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

    # 提交训练作业，同时打印训练作业的Web详情页URL。
    # fit 方法默认等待到作业终止（成功，失败，会是被停止）。
    est.fit()

    # 输出的模型路径
    est.model_data()


下载输出模型
*****************

训练作业执行完成之后，用户可以通过 :meth:`pai.estimator.Estimator.model_data`
获得提交作业的产出的模型的OSS路径。用户可以通过SDK提供的
``download`` 方法下载模型到本地，也可以使用 ``ossutil`` 命令行工具下载模型。


使用 ``pai.common.oss_utils.download`` 方法下载模型到本地:

.. code-block:: python

    from pai.common.oss_utils import download

    # 下载模型到本地
    download(oss_path=est.model_data(), local_path="./model/")


通过 ``ossutil`` 命令行工具下载模型到本地。

.. code-block:: shell

    ossutil cp -r <YourModelDataOssURI> ./model/

对于 ``ossutil`` 命令行工具的使用，可以参考 `ossutil工具使用文档 <https://help.aliyun.com/document_detail/120075.html>`_ 。
