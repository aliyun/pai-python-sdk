================
自定义工作流组件
================

在以下示例中，我们基于自定义镜像和Python脚本，构建了一个自定义任务组件。这个自定义组件能够注册保存到PAI的后端，也能够用于构建工作流，然后提交到PAI的工作流服务执行。

准备工作
--------

请首先安装PAI SDK，以支持运行以下的示例代码。

.. code:: shell

    python -m pip install https://pai-sdk.oss-cn-shanghai.aliyuncs.com/alipai/dist/alipai-0.3.4a1-py2.py3-none-any.whl


初始化默认的Session，请确认使用的OSS桶所在region和PAI工作空间是一致的。

.. code:: python

    # 初始化Session
    import pai
    
    print(pai.__version__)
    
    from pai.core.session import setup_default_session, Session
    
    sess = Session.current()
    
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
    
    assert sess.oss_bucket is not None



准备数据
--------

我们构建的组件脚本，会去读取OSS上的数据集进行训练，输出模型。在这里，我们使用SKLearn提供的iris数据，上传到OSS，作为组件的输入准备。

-  train_data_uri: 训练使用的数据集OSS URI

-  test_data_uri: 测试使用的数据集OSS URI.

-  output_path_uri: 组件输出的OSS URI.

.. code:: python

    from sklearn import datasets
    from sklearn.model_selection import train_test_split
    import pandas as pd
    import numpy as np
    
    oss_bucket = sess.oss_bucket  # type: oss2.Bucket
    
    iris = datasets.load_iris()
    df = pd.DataFrame(
        data=np.c_[iris["data"], iris["target"]],
        columns=iris["feature_names"] + ["target"],
    )
    
    train, test = train_test_split(df, test_size=0.3)
    
    # 上传训练数据集
    train.to_csv("train.csv", sep=",", index=False)
    oss_bucket.put_object_from_file(
        "custom-job-example/train-data/train.csv", filename="train.csv"
    )
    
    # 上传测试数据集
    test.to_csv("test.csv", sep=",", index=False)
    oss_bucket.put_object_from_file(
        "custom-job-example/test-data/test.csv", filename="test.csv"
    )
    
    train_data_uri = (
        "oss://{bucket_name}.{endpoint}/custom-job-example/train-data/train.csv".format(
            bucket_name=oss_bucket.bucket_name,
            endpoint=oss_bucket.endpoint.strip("https://"),
        )
    )
    test_data_uri = (
        "oss://{bucket_name}.{endpoint}/custom-job-example/test-data/test.csv".format(
            bucket_name=oss_bucket.bucket_name,
            endpoint=oss_bucket.endpoint.strip("https://"),
        )
    )
    
    print("train_data_uri", train_data_uri)
    print("test_data_uri", test_data_uri)
    
    output_path_uri = "oss://{bucket_name}.{endpoint}/custom-job-example/output/".format(
        bucket_name=oss_bucket.bucket_name,
        endpoint=oss_bucket.endpoint.strip("https://"),
    )
    print("output_path_uri", output_path_uri)



构建自定义组件
--------------

自定义组件定义的作业，会被提交运行在PAI-DLC Job上:

-  用户通过提供一个作业运行的脚本，以及使用的镜像，定义自定义任务的逻辑。

-  作业使用脚本会被上传到当前Session的OSS
   Bucket上，当PAI-DLC作业拉起时会被准备到执行的环境中。

- 组件的参数，会通过arguments的方式传递给到这个任务脚本，以下：

.. code-block::

    python <entry_point> --arg1 value1 --arg2 value2


- 输入的OSS数据， 会通过mount的方式挂载到作业容器上，用户可以通过本地的方式读取到对应的数据。
  输入的数据的本地文件路径也会一个arguments的方式传递给到训练脚本。




组件使用的脚本文件:

.. code:: python

    import argparse
    import os
    
    import pandas as pd
    from joblib import dump
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score
    
    TRAINING_BASE_DIR = "/ml/"
    TRAINING_OUTPUT_MODEL_DIR = os.path.join(TRAINING_BASE_DIR, "output/model/")
    
    TRAINING_OUTPUT_ACCURACY_PATH = os.path.join(
        TRAINING_BASE_DIR, "output/output_parameters/test-accuracy"
    )
    
    
    def load_dataset(path):
        if not os.path.exists(path):
            raise ValueError("Input data path not exists: {}".format(path))
    
        if os.path.isfile(path):
            file_path = path
        else:
            # use first file in the channel dir.
            file_name = next(
                iter(
                    [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
                ),
                None,
            )
            if not file_name:
                raise ValueError(f"Not found input file in channel path: {path}")
            file_path = os.path.join(path, file_name)
        df = pd.read_csv(
            filepath_or_buffer=file_path,
            sep=",",
        )
    
        y = df["target"]
        x = df.drop(["target"], axis=1)
        return x, y
    
    
    def main():
        parser = argparse.ArgumentParser(description="RandomForest train.")
        parser.add_argument(
            "--n_estimator", type=int, default=100, help="The number of trees in the forest"
        )
        parser.add_argument(
            "--criterion",
            type=str,
            default="gini",
            choices=["gini", "entropy"],
            help="The function to measure the quality of a split, supported criteria: {'gini', 'entropy'}",
        )
    
        parser.add_argument(
            "--max_depth",
            type=int,
            default=10,
            help="The maximum depth of the tree.",
        )
    
        parser.add_argument(
            "--train",
            type=str,
            default=None,
            help="Input train data path.",
        )
        parser.add_argument(
            "--test",
            type=str,
            default=None,
            help="Input train data path.",
        )
    
        args, _ = parser.parse_known_args()
    
        estimator = RandomForestClassifier(
            n_estimators=args.n_estimator,
            criterion=args.criterion,
            max_depth=args.max_depth,
            oob_score=True,
        )
        train_x, train_y = load_dataset(args.train)
        estimator = estimator.fit(train_x, train_y)
        print(
            "oob_score for the train dataset: train:oob_score={0}".format(
                estimator.oob_score_
            )
        )
    
        # 使用测试集评估模型，将模型在测试集上的精度到 /ml/output/output_parameters/test_accuracy 文件
        if args.test:
            print("Score the model with test dataset: {}".format(args.test))
            test_x, test_y = load_dataset(args.test)
            pred_y = estimator.predict(test_x)
            accuracy = accuracy_score(test_y, pred_y)
            print("classifier accuracy score: test:accuracy={0}".format(accuracy))
            os.makedirs(os.path.dirname(TRAINING_OUTPUT_ACCURACY_PATH), exist_ok=True)
            with open(TRAINING_OUTPUT_ACCURACY_PATH, "w") as f:
                f.write(str(accuracy))
    
        # 将训练获得的模型写出到 /ml/output/model/model.pkl
        os.makedirs(TRAINING_OUTPUT_MODEL_DIR, exist_ok=True)
        model_path = os.path.join(TRAINING_OUTPUT_MODEL_DIR, "model.pkl")
        dump(estimator, model_path)
        print(f"model dump succeed: {model_path}")
    
    
    if __name__ == "__main__":
        main()



.. code:: python

    from pai.operator import CustomJobOperator
    from pai.operator.types import (
        PipelineArtifact,
        PipelineParameter,
        ArtifactMetadataUtils,
    )
    
    from pai.job.common import JobConfig
    
    
    # 我们使用了PAI仓库内的社区版本的XGBoost镜像，作为作业执行的镜像.
    image_uri = "registry.{}.aliyuncs.com/pai-dlc/xgboost-training:1.6.0-cpu-py36-ubuntu18.04".format(
        sess.region_id
    )
    
    
    # 构建作业组件.
    operator = CustomJobOperator(
        # 作业组件的EntryPoint，相应的脚本会以 python <entry_point> --arg1 value1 --arg2 value2 的方式拉起。
        entry_point="train.py",
        # 作业使用的本地脚本目录：会被打包上传到OSS Bucket，当作业运行时准备到执行环境中。
        source_code=source_code_dir,
        # 作业脚本运行使用的脚本
        image_uri=image_uri,
        # 定义组件的输入:
        # 这个组件会有两个OSS的输入：train 和 test.
        parameters={
            "n_estimator": 100,
            "max_depth": 10,
            "criteria": "gini",
        },
        inputs=[
            PipelineArtifact(
                name="train",
                metadata=ArtifactMetadataUtils.oss_dataset(),
            ),
            PipelineArtifact(
                name="test",
                metadata=ArtifactMetadataUtils.oss_dataset(),
            ),
        ],
        # 这个组件的输出参数
        outputs=[PipelineParameter("test-accuracy")],
    )
    
    # 查看组件的输入输出
    print(operator.inputs)
    print(operator.outputs)


.. code:: python

    # 将自定义任务提交运行
    run = operator.run(
        # 任务运行的名称
        job_name="ExampleCustomOpRun",
        # 作业的输出路径，输出路径会被挂载到 /ml/output 目录下。
        output_path=output_path_uri,
        # 作业的执行配置: 使用的worker的数量，实例类型
        # 支持的实例类型，以及计费说明参加文档：https://help.aliyun.com/document_detail/171758.html
        job_config=JobConfig.create(worker_count=1, worker_instance_type="ecs.c6.large"),
        # 组件的输入
        inputs={
            "train": train_data_uri,
            "test": test_data_uri,
            "n_estimator": 200,
        },
    )



.. code:: python

    from pai.pipeline import Pipeline
    
    step_train_1 = operator.as_step(
        name="TrainStep1",
        inputs={
            "job_config": JobConfig.create(
                worker_count=1, worker_instance_type="ecs.c6.large"
            ).to_dict(),
            "output_path": output_path_uri + "train_step_output/",
            "train": train_data_uri,
            "test": test_data_uri,
            "n_estimator": 2000,
            "criteria": "entropy",
            "max_depth": 20,
        },
    )
    
    step_train_2 = operator.as_step(
        name="TrainStep2",
        inputs={
            "job_config": JobConfig.create(
                worker_count=1, worker_instance_type="ecs.c6.large"
            ).to_dict(),
            "output_path": output_path_uri + "train_step_output/",
            "train": test_data_uri,
            "n_estimator": 100,
            "criteria": "gini",
            "max_depth": 200,
        },
    )
    
    step_train_2.after(step_train_1)
    
    p = Pipeline(steps=[step_train_2, step_train_1])
    
    run = p.run("ExamplePipeline")


下载Notebook
----------------

当前示例Notebook下载链接:

:download:`Notebook下载 <../resources/custom_operator.ipynb>`



