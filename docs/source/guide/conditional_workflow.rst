==========================
在工作流中使用条件执行
==========================

PAI的Workflow支持在条件执行，从而支持灵活的Workflow执行。以下的示例中，我们将通过SDK构建带条件执行的工作流。

准备工作
--------

请首先安装PAI SDK，以支持运行以下的示例代码。

.. code:: shell

    python -m pip install https://pai-sdk.oss-cn-shanghai.aliyuncs.com/alipai/dist/alipai-0.3.4a1-py2.py3-none-any.whl

初始化默认的Session，请确认使用的OSS桶所在region和PAI工作空间是一致的。

.. code:: python

    import pai

    print(pai.__version__)

    from pai.core.session import setup_default_session, Session, get_default_session

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



构建Conditional节点
-------------------

以下示例中，我们使用了一个自定义组件，组件会输出一个参数(output parameter)。
这个输出参数，可以用于构建条件判断语句，支持用户构建一个条件节点(ConditionalStep)。
只有相应的条件判断满足之后，对应的节点才会执行，否则对应的节点，以及下游节点会被跳过。

.. code:: python

    from pai.job.common import JobConfig
    from pai.operator.types import PipelineParameter
    from pai.operator import CustomJobOperator
    from pai.pipeline import Pipeline

    # 自定义节点使用的镜像，这里我们使用了PAI仓库内提供的XGBoost社区镜像运行我们的任务。
    image_uri = "registry.{}.aliyuncs.com/pai-dlc/xgboost-training:1.6.0-cpu-py36-ubuntu18.04".format(
        sess.region_id
    )


    output_path_uri = "oss://{bucket_name}.{endpoint}/custom-job-example/output/".format(
        bucket_name=sess.oss_bucket.bucket_name,
        endpoint=sess.oss_bucket.endpoint.strip("https://"),
    )
    print("output_path_uri", output_path_uri)


    # 这里我们构建自定义组件，会写出一个 test_acc 的output_parameter.
    # 这里依赖于我们的命令，或是脚本，将相应的输出参数，写出到 `/ml/output/output_parameters/<OutputParameterName>`
    output_param_name = "test_acc"
    op = CustomJobOperator(
        outputs=[PipelineParameter(name=output_param_name)],
        image_uri=image_uri,
        command=[
            "bash",
            "-c",
            "mkdir -p /ml/output/output_parameters/ && echo 0.99 > /ml/output/output_parameters/%s"
            % output_param_name,
        ],
    )


    # 构建Pipeline中的第一个节点.
    step1 = op.as_step(
        name="step1",
        inputs={
            "job_config": JobConfig.create(
                worker_count=1, worker_instance_type="ecs.c6.large"
            ).to_dict(),
            "output_path": output_path_uri + "step1_output/",
        },
    )

    # 构建Pipeline中的第二个节点
    # 只有上游的output参数(step.outputs.test_acc) 大于 0.8时，才会执行当前节点。
    step2 = op.as_condition_step(
        name="step2",
        condition=step1.outputs[0] > 0.8,
        inputs={
            "job_config": JobConfig.create(
                worker_count=1, worker_instance_type="ecs.c6.large"
            ).to_dict(),
            "output_path": output_path_uri + "step2_output/",
        },
    )

    # 构建Pipeline中的第三个节点
    # 只有上游的output参数(step.outputs.test_acc) 小于 0.8时，才会执行当前节点。
    step3 = op.as_condition_step(
        name="step3",
        condition=step1.outputs[0] <= 0.8,
        inputs={
            "job_config": JobConfig.create(
                worker_count=1, worker_instance_type="ecs.c6.large"
            ).to_dict(),
            "output_path": output_path_uri + "step3_output/",
        },
    )

    # 构建对应的工作流
    # 不满足条件的相应节点，会被跳过(状态：skipped）
    p = Pipeline(steps=[step3, step2, step1])

    p.run("ConditionalPipelineRun")


下载Notebook
----------------

当前示例Notebook下载链接:

:download:`Notebook下载 <../resources/conditional_workflow.ipynb>`
