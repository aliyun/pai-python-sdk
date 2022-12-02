====================================
自定义训练作业
====================================

以下例子展示了如何通过PAI
SDK，使用本地Python脚本和自定义镜像在PAI-DLC上执行一个训练作业。同时这个自定义作业可以作为一个节点任务，用于构建工作流，提交到PAI的Workflow中执行。

准备工作.
---------

请首先安装PAI SDK，以支持运行以下的示例代码。

.. code:: shell

    python -m pip install https://pai-sdk.oss-cn-shanghai.aliyuncs.com/alipai/dist/alipai-0.3.4a1-py2.py3-none-any.whl



.. code:: python

    import sys

    import pai

    print(pai.__version__)

    from pai.core.session import setup_default_session, Session, get_default_session
    from pai.job.common import JobConfig
    import oss2


初始化默认的Session，请确认使用的OSS桶所在region和PAI工作空间是一致的。

.. code:: python

    sess = get_default_session()

    if not sess:
        print("config session")
        sess = setup_default_session(
            access_key_id="<YourAccessKeyId>",
            access_key_secret="<YourAccessKeySecret>",
            region_id="<RegionIdWorking>",
            workspace_id="<YourWorkspaceId>",
            oss_bucket_name="<YourOssBucketName>",
        )
        # 将当前的配置持久化到 ~/.pai/config.json，SDK默认从对应的路径读取配置初始化默认session。
        sess.persist_config()

准备训练数据
------------

这里我们使用sklearn上的IRIS鸢尾花数据集作为训练数据，获得的数据集导出为CSV后，上传到OSS，供后续的训练作业使用。

-  job_train_data_uri: 作业数据集地址

我们的训练数据集作业地址,
由被挂载的作业训练容器，对应的日志会以arguments (–train
/ml/input/data/train/train.csv)形式传递给到作业中

-  job_output_path_uri: 作业输出地址

作业的输出OSS地址，会被挂载到作业容器的\ ``/ml/output``\ 目录下，作业输出的模型，会被持久化到OSS的相应路径下。

.. code:: python

    # 如果本地没有SKLearn，Pandas的包，请执行以下的命令安装.
    # !{sys.executable} -m pip install scikit-learn pandas

.. code:: python

    from sklearn import datasets
    import pandas as pd
    import numpy as np

    iris = datasets.load_iris()
    df = pd.DataFrame(
        data=np.c_[iris["data"], iris["target"]],
        columns=iris["feature_names"] + ["target"],
    )
    df.to_csv("train.csv", sep=",", index=False)

    oss_bucket = sess.oss_bucket  # type: oss2.Bucket

    oss_bucket.put_object_from_file(
        "custom-job-example/train-data/train.csv", filename="train.csv"
    )

    job_train_data_uri = (
        "oss://{bucket_name}.{endpoint}/custom-job-example/train-data/train.csv".format(
            bucket_name=oss_bucket.bucket_name,
            endpoint=oss_bucket.endpoint.strip("https://"),
        )
    )
    print(job_train_data_uri)

    job_output_path_uri = (
        "oss://{bucket_name}.{endpoint}/custom-job-example/output/".format(
            bucket_name=oss_bucket.bucket_name,
            endpoint=oss_bucket.endpoint.strip("https://"),
        )
    )
    print(job_output_path_uri)



准备训练的脚本
--------------

我们这里使用XGBoost进行训练，以下的脚本，使用上述准备的数据集进行训练，测试。

-  作业定义的参数会以arguments的方式，拉起用户指定的训练脚本。

-  在OSS上的数据会被挂载到容器上，并且以arguments的方式，将数据文件的挂载地址传递给到训练脚本。

-  指定的作业输出的OSS路径，会被挂载到 ``/ml/output`` 目录下。
   训练脚本将模型，以及结果metric写出到相应的本地目录下，即可保存作业的训练产出到OSS。


.. code:: python

    import argparse
    import os


    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn import metrics

    from xgboost import XGBClassifier

    TRAINING_BASE_DIR = "/ml/"
    TRAINING_CODE_DIR = os.path.join(TRAINING_BASE_DIR, "code/")
    TRAINING_OUTPUT_MODEL_DIR = os.path.join(TRAINING_BASE_DIR, "output/model/")
    TRAINING_OUTPUT_PARAMETER_DIR = os.path.join(TRAINING_BASE_DIR, "output/output_parameters/")


    def load_train_test(data_path):
        df = pd.read_csv(data_path, sep=",")
        train, test = train_test_split(df, test_size=0.3)
        train_y = train["target"]
        train_x = train.drop(["target"], axis=1)
        test_y = test["target"]
        test_x = test.drop(["target"], axis=1)
        return train_x, train_y, test_x, test_y


    def main():
        parser = argparse.ArgumentParser(description="XGBoost train example")
        # 用户指定的任务参数
        parser.add_argument(
            "--n_estimators", type=int, default=500, help="The number of base model."
        )
        parser.add_argument(
            "--objective", type=str, default="multi:softmax", choices=["multi:softmax", "multi:softprob"],
            help="Objective function used by XGBoost, supported objective: {'multi:softmax', 'multi:softprob'}", )

        parser.add_argument(
            "--max_depth", type=int, default=3, help="The maximum depth of the tree.",
        )

        parser.add_argument(
            "--eta", type=float, default=0.2, help="Step size shrinkage used in update to prevents overfitting.",
        )

        # 作业数据的数据，也通过arguments的方式传递给到训练脚本.
        parser.add_argument(
            "--train_data", type=str, help="Input train data path."
        )
        args, _ = parser.parse_known_args()


        # 读取传入到容器内的数据
        train_x, train_y, test_x, test_y = load_train_test(args.train_data)

        # 这里使用XGBoost的SKLearn API进行作业训练.
        clf = XGBClassifier(max_depth=args.max_depth,
                            eta=args.eta,
                            n_estimators=args.n_estimators,
                            objective=args.objective)
        clf.fit(train_x, train_y)
        y_pred = clf.predict(test_x)
        accuracy = metrics.accuracy_score(test_y, y_pred)

        # 写出作业在测试集上的精度到 /ml/output/output_parameters/test-accuracy 文件
        print("Output model accuracy=%s" % accuracy)
        os.makedirs(TRAINING_OUTPUT_PARAMETER_DIR, exist_ok=True)
        with open(os.path.join(TRAINING_OUTPUT_PARAMETER_DIR, "test-accuracy"), "w") as f:
            f.write(str(accuracy))

        # 写出作业产出模型到 /ml/output/model/
        os.makedirs(TRAINING_OUTPUT_MODEL_DIR, exist_ok=True)
        clf.save_model(f"{TRAINING_OUTPUT_MODEL_DIR}xgb_model")
        print(f"Save model succeed: model_path={TRAINING_OUTPUT_MODEL_DIR}xgb_model")


    if __name__ == "__main__":
        main()



启动作业进行训练
----------------

我们使用CustomJob拉起对应的作业

-  CustomJob将相关的代码上传到OSS
   对应的source_code目录的文件会被打包上传到OSS中，然后传递到作业容器目录:
   ``/ml/code``\ 。

-  将指定数据，以及代码准备到训练作业容器中，通过arguments传递训练的数据，以及参数给到作业脚本，启动作业。

以下的作业脚本的作业脚本，启动命令如下。

.. code:: shell


   python xgb_train.py \
   --n_estimators 500 \
   --objective multi:softmax \
   --max_depth 5 \
   --train_data /ml/input/data/train_data/train.csv

作业的输入数据默认挂载到
``/ml/input/data/{input_name}/``\ 目录下，传入的输出路径(``output_path``)会挂载到\ ``/ml/output``\ 路径下。
默认的文件目录结构如下:

.. code:: shell

   /ml
   |-- input                                       // 作业输入path
   |   `-- data                                    // 数据数据所在目录，每一个子文件夹表示一个具体输入
   |       |-- test
   |       `-- train_data
   `-- output                                    // 输出的path, 作业指定的OutputPath（OSS）会被挂载到这个目录下.
       |-- model
       `-- output_parameters
           `-- test_accurary.txt

.. code:: python

    from pai.job import CustomJob

    from pai.operator.types import (
        PipelineParameter,
        PipelineArtifact,
        ArtifactMetadataUtils,
    )

    # 这里我们使用XGBoost的社区镜像运行脚本，相应的镜像中已经预安装了xgboost, pandas等相关的Python库。
    image_uri = "registry.{}.aliyuncs.com/pai-dlc/xgboost-training:1.6.0-cpu-py36-ubuntu18.04".format(
        sess.region_id
    )

    job = CustomJob(
        entry_point="xgb_train.py",
        # 训练作业使用的代码文件夹
        source_code=source_code_dir,
        # 训练作业使用镜像
        image_uri=image_uri,
        # 训练作业参数，通过arguments传递给到脚本.
        parameters={
            "n_estimators": 500,
            "objective": "multi:softmax",
            "max_depth": 5,
        },
    )


    # 用户可以通过LocalRun的方式，在本地调试对应的脚本。
    # job.local_run 通过运行一个Docker container的方式，模拟的作业的执行。
    # 相应的传入的数据，会被mount到Docker container中，然后以arguments的方式传递给到脚本。

    # job.local_run(
    #     inputs={
    #         "train_data": "./train.csv",
    #     },
    #     output_path="./output/"
    # )


    # 提交任务
    job_id = job.run(
        name="custom-job-example",
        # 作业的执行配置
        job_config=JobConfig.create(worker_count=1, worker_instance_type="ecs.c6.large"),
        inputs={
            "train_data": job_train_data_uri,
        },
        output_path=job_output_path_uri,
    )

训练产出的模型可以通过OSS
client下载到本地应用，也可以直接在PAI的控制台上，使用PAI-EAS进行部署。

.. code:: python

    from pai.common.oss_utils import parse_oss_url

    model_url = job_output_path_uri + "model/xgb_model"
    print(model_url)
    object_key = parse_oss_url(model_url).object_key
    oss_bucket.get_object_to_file(object_key, "xgb_model")



（可选）自定义作业任务作为组件保存
------------------------------------------

以上构建的\ ``CustomJob``\ 实例可以作为一个Workflow的组件复用。
用户可以在这个组件上使用不同的参数，数据集，或是计算资源配置运行相应的脚本作业。同时这个组件也可以作为工作流中的节点，构建一个Workflow。

.. code:: python

    from pai.operator import CustomJobOperator, RegisteredComponent

    import time


    # 构建一个Workflow的组件，由Workflow服务来提交对应的作业
    op: CustomJobOperator = job.as_component(
        inputs=[
            PipelineArtifact(
                "train_data",
                metadata=ArtifactMetadataUtils.oss_dataset(),
            )
        ],
        outputs=[PipelineParameter("test-accuracy")],
    )


    # 组件可以注册保存到PAI的服务后端

    version = "v-%s" % int(time.time())
    op.save(identifier="xgb-example", version=version)
    # 从后端获取保存的组件
    registered_op = RegisteredComponent.get_by_identifier(
        identifier="xgb-example", version=version
    )

    print(registered_op)
    print(registered_op.inputs)


    # 使用保存的组件运行拉起对应的作业
    registered_op.run(
        job_name="Hello",
        arguments={
            "job_config": JobConfig.create(
                worker_count=1, worker_instance_type="ecs.c6.large"
            ).to_dict(),
            "output_path": job_output_path_uri,
            "train_data": job_train_data_uri,
        },
    )



（可选）构建Workflow
--------------------------------


对应的作业任务组件能够用于构建一个Workflow
DAG，以下的样例中，使用了上述的脚本构建了包含条件分支判断的Workflow。

当节点\ ``train-step-1``\ 在测试集上的精度低于0.90时运行\ ``train-step-2``,
而在精度高于0.90时运行\ ``train-step-3``\ 。

.. code:: python

    from pai.pipeline import Pipeline

    step1 = op.as_step(
        name="train-step-1",
        inputs={
            "job_config": JobConfig.create(
                worker_count=1, worker_instance_type="ecs.c6.large"
            ).to_dict(),
            "output_path": job_output_path_uri + "train-step-1/",
            "train_data": job_train_data_uri,
            "n_estimators": 500,
        },
    )

    step2 = op.as_condition_step(
        name="train-step-2",
        condition=step1.outputs["test-accuracy"] <= 0.90,
        inputs={
            "job_config": JobConfig.create(
                worker_count=1, worker_instance_type="ecs.c6.large"
            ).to_dict(),
            "output_path": job_output_path_uri + "train-step-2/",
            "train_data": job_train_data_uri,
            "n_estimators": 500,
        },
        depends=[step1],
    )

    step3 = op.as_condition_step(
        name="train-step-3",
        condition=step1.outputs["test-accuracy"] > 0.90,
        inputs={
            "job_config": JobConfig.create(
                worker_count=1, worker_instance_type="ecs.c6.large"
            ).to_dict(),
            "output_path": job_output_path_uri + "train-step-3/",
            "train_data": job_train_data_uri,
            "n_estimators": 1000,
        },
        depends=[step1],
    )

    p = Pipeline(
        steps=[step2, step3],
    )

    p.run("example-custom-job-workflow")


下载Notebook
----------------

当前示例Notebook下载链接:

:download:`Notebook下载 <../resources/custom_job.ipynb>`
