======================
Estimator
======================


SDK支持Pipeline作为一个Estimator调用fit接口, 向服务端提交一个任务, 返回一个EstimatorJob，它与提交的任务关联.

返回的Job实例，支持管理任务运行，获取Estimator的运行返回结果，能够使用返回的Model Artifact创建一个Model对象.


.. code-block:: python

    pipeline = PipelineTemplate.get_by_identifier(logisticregression-binary-xflow-maxCompute",
        provider=ProviderAlibabaPAI, version="v1", session=session)

    # 具体的parameters名称需要和Manifest中inputs的名称匹配
    est = pipeline.to_estimator(parameters={
            "execution": xflow_execution,
            "regularizedType": "l2",
            "regularizedLevel": 1.0,
    })

    # fit参数输入的arguments参数，可以override初始化Estimator时输入的参数
    job = est.fit(wait=False, job_name="test-estimator", arguments={
        "inputArtifact": "odps://pai_online_project/tables/iris_data",
        "goodValue": 1,
        "modelName": "test_iris_model",
        "featureColNames": "f1,f2,f3,f4",
        "labelColName": "type",
        "regularizedLevel": 2.0,
    })

    # 等待任务结束返回
    job.wait_for_completion(show_outputs=False, timeout=240)
    print(job.get_status())
    print(job.get_outputs())

    model = job.create_model(output_name="outputArtifact")



XFlow Algorithm
---------------------


SDK对于部分基础的基于XFlow的算法模块进行了封装，例如LogisticsRegression和RandomForests，使得用户能够简单得使用这些算法模块.

pipeline.to_estimator获得PipelineEstimator不同，封装的算法模块的参数被重写了，它使用一个_compile_args函数完成重写的输入参数与对应的Pipeline Manifest之间的映射.

目前的算法封装模块比较独立，仅便于用户能够简单的使用一个具体的算法模块模块，与Pipeline的拼接组合/运行上并没有联动，这块可能是后续接口改造的一个方向.

以LogisticRegression为例:

.. code-block:: python

    from pai.xflow.classifier import LogisticRegression

    model_name = 'test_iris_model_%d' % (random.randint(0, 999999))
    lr = LogisticRegression(session=self.session, regularized_type="l2",
                            pmml_gen=True, pmml_oss_bucket=oss_bucket,
                            pmml_oss_path=oss_path, pmml_oss_endpoint=oss_endpoint,
                            pmml_oss_rolearn="acs:ram::1557702098194904:role/aliyunodpspaidefaultrole")


    job = lr.fit(wait=True, input_data=dataset1,
                    job_name="pysdk-test-lr-sync-fit",
                    model_name=model_name, good_value=1, label_col="type",
                    feature_cols=["f1", "f2", "f3", "f4"])

    job.wait_for_completion()
    offline_model = job.create_model(output_name="outputArtifact")