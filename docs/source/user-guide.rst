
User Guide
===========================================

v1版本的SDK提供的功能主要包括以下:

.. note:: 

    目前版本的SDK并未将PMML部署到EAS功能打通，提交任务后，SDK会打印具体的任务在Web页面的URL，可以在Web页面完成模型的注册和部署.


Session
-------------------------------------------

Session负责与PAI的后端服务，以及依赖的其他阿里云服务，例如STS, MaxCompute, OSS交互。 他使用API鉴权所需的access key初始化，提供了PAIFlow的Pipeline/Run资源管控的接口。

.. code-block:: python

    from pai.session import Session
    from pai import ProviderAlibabaPAI
    from pai.pipeline import RunStatus
    session = Session(access_key="your_access_key", access_key_secret="your_access_key_secret", region_id="cn-shanghai")

    # 搜索provider为PAI, 并且identifier中包含`xflow`的pipeline
    pipeline_infos = session.list_pipeline(identifier="xflow", fuzzy=True, provider=ProviderAlibabaPAI, page_size=50)

    # 使用identifier/provider/version获取某一个具体的Pipeline Info，需要有对应的Pipeline的``GetPipeline``权限
    pipeline_info = session.get_by_identifier(identifier="logisticregression-binary-xflow-maxCompute", provider=ProviderAlibabaPAI, version="v1")

    # 获取最近提交的，状态为成功的任务信息
    run_infos = session.list_run(status="Succeeded", sorted_by="startedAt", sorted_sequence="desc", page_size=100)



Pipeline Manifest
-------------------------------------------

PAIFlow，是PAI平台研发的ML Pipeline Service，提供了机器学习工作流编排和运行管理的功能, 他支持在页面上使用可视化方式编排机器学习工作流(开发中,PAI Studio的重构版本），也支持使用API的方式编排和提交任务。 

PAIFlow使用yaml格式的Pipeline Manifest描述一个具体的可运行的工作流，这个工作流的实现可以是一个具体的镜像，或是一个由多个Pipeline拼接组成的复合工作流。保存在PAIFlow服务的Pipeline Manifest使用identifier-provider-version三元组或是PipelineId进行唯一标识，区别是前者是由Pipeline的创建者指定，后者则是由PAIFlow后端生成。

GetPipeline请求返回的Manifest中`spec`中则包含了Pipeline Manifest的签名, 包括Pipeline的inputs和outputs的参数信息。
如果需要获得Pipeline的具体实现的完整Manifest，则需要用户拥有对应的Pipeline的DescribePipeline权限，使用session.describe_pipeline则能获得对应的Pipeline Manifest的完整定义。

.. note:: 

    PAI平台目前提供了一些基于XFlow的基础Pipeline，用户可以使用*provider=pai.ProviderAlibabaPAI*作为过滤器获得PAI提供的基础Pipeline, PAI分享提供的Pipeline默认授予了用户DescribePipeline权限.



Pipeline Manifest的例子:

.. code-block:: python

    >> pipeline_info = session.get_by_identifier(identifier="logisticregression-binary-xflow-maxCompute", 
        provider=ProviderAlibabaPAI, version="v1")
    >> print(pipeline_info["Manifest“])
    apiVersion: "core/v1"
    metadata:
      provider: "pai"
      version: "v1"
      identifier: "logisticregression-binary-xflow-maxCompute"
      uuid: "3m6y9hew3p47tqp801"
      namespace: null
      labels: null
      spec:
    inputs:
      artifacts:
      - name: "inputArtifact"
        metadata:
          type:
          DataSet:
              locationType: "MaxComputeTable"
        required: true
        parameters:
      - name: "execution"
        type: "Map"
        desc: "必选，执行环境"
        required: false
      - name: "labelColName"
        type: "String"
        desc: "逻辑回归算法的输入字段"
        required: true
      - name: "featureColNames"
        type: "String"
        desc: "输入表中选择的用于训练的特征列名"
        required: true
      - name: "itemDelimiter"
        type: "String"
        desc: "当输入表数据为稀疏格式时，kv间的分割符"
        value: " "
        required: false
      - name: "kvDelimiter"
        type: "String"
        desc: "当输入表数据为稀疏格式时，key和value的分割符"
        value: ":"
        required: false
      - name: "epsilon"
        type: "Double"
        value: ""
        required: false
      - name: "maxIter"
        type: "Int"
        value: ""
        required: false
      - name: "regularizedLevel"
        type: "Double"
        value: ""
        required: false
      - name: "modelName"
        type: "String"
        required: true
      - name: "goodValue"
        type: "Int"
        desc: null
        value: ""
        required: false
      - name: "generatePmml"
        type: "Bool"
        desc: null
        value: false
        required: false
      - name: "endpoint"
        type: "String"
        desc: null
        value: ""
        required: false
      - name: "bucket"
        type: "String"
        desc: null
        value: ""
        required: false
      - name: "path"
        type: "String"
        desc: null
        value: ""
        required: false
      - name: "rolearn"
        type: "String"
        value: ""
        required: false
      - name: "overwrite"
        type: "Bool"
        desc: null
        value: true
        required: false
    outputs:
        artifacts:
        - name: "outputArtifact"
          metadata:
              type:
              Model:
                  locationType: "MaxComputeOfflineModel"
                  modelType: "OfflineModel"
          value: "{\"name\": \"{{inputs.parameters.modelName}}\", \"location\": {\"name\"\
              : \"{{inputs.parameters.modelName}}\"}}"
          required: false
        - name: "OSSArtifact"
          metadata:
              type:
              Model:
                  locationType: "OSS"
                  modelType: "PMML"
          value: "{\"location\": {\"bucket\": \"{{inputs.parameters.bucket}}\", \"endpoint\"\
              : \"{{inputs.parameters.endpoint}}\", \"rolearn\": \"{{inputs.parameters.rolearn}}\"\
              }}"
          required: false


Pipeline Run
-------------------------------------------

用户可以拉取Pipeline，根据Pipeline的Manifest提供输入的数据/参数，直接运行Pipeline。


.. code-block:: python

    from pai.pipeline import Pipeline

    default_project = "your_odps_project"

    # 以LogisticRegression为例
    pipeline = Pipeline.get_by_identifier(identifier="logisticregression-binary-xflow-maxCompute", 
        provider=ProviderAlibabaPAI, version="v1", session=session)
    
    # 基于XFlow的算法需要提供相应的MaxCompute执行环境
    xflow_execution = {
        "odpsInfoFile": "/share/base/odpsInfo.ini",
        "endpoint": "http://service.cn-shanghai.maxcompute.aliyun.com/api",
        "logViewHost": "http://logview.odps.aliyun.com",
        "odpsProject": default_project,
    }

    # 异步提交运行任务
    run_instance = pipeline.run(wait=False, job_name="test", arguments={
                "inputArtifact": "odps://pai_online_project/tables/iris_data",
                "execution": xflow_execution,
                "regularizedType": "l2",
                "modelName": "test_iris_model",
                "goodValue": 1,
                "featureColNames": "f1,f2,f3,f4",
                "labelColName": "type",
    })

    # 等待Run任务完成
    run_instance.wait(log_outputs=True)

    print(run_instance.get_status())
    print(run_instance.get_outputs())


Composite Pipeline
-------------------------------------------

.. note::
    PAIFlow 1.0版本还不支持自定义镜像上传，目前用户只能使用PAI提供的XFlow相关的算法模块进行拼装运行。

PAIFlow支持将多个Pipeline进行拼接, 拼接后的Pipeline可以作为工作流模板，在输入参数后直接运行，或是提交保存在PAIFlow进行复用(作为一个工作流模板提供参数直接运行，或则作为其他复合Pipeline的子节点进行拼接)。


.. code-block:: python

    # 创建一个复合Pipeline
    def create_composite_pipeline(session):
        # 定义复合Pipeline的identifier, version, 默认当前Session对应的主账号UID作为Pipeline的provider。
        p = Pipeline.new_pipeline(identifier="test-data-source-type-transform",
                            version="v2",
                            session=session)

        # 定义复合pipeline的输入参数
        # 包括MaxCompute的运行环境，输入表名称，以及数据表中需要转为浮点数的列
        execution_input = p.create_input_parameter("execution", "map", required=True)
        cols_to_double_input = p.create_input_parameter("cols_to_double", str, required=True)
        input_table_name = p.create_input_parameter("table_name", str, required=True)


        # 创建一个新的Pipeline的子节点, 指定子节点的输入
        data_source_step = p.create_step("dataSource-xflow-maxCompute",
                                         provider=ProviderAlibabaPAI,
                                         version="v1", name="dataSource",
                                         arguments= {
                                            "execution": execution_input,
                                            "tableName": input_table_name,

                                         })

        # 创建一个新的Pipeline子节点，该子节点依赖于dataSource节点的输出，作为输入。
        type_transform_step = p.create_step("type-transform-xflow-maxCompute",
                                            provider=ProviderAlibabaPAI,
                                            version="v1", name="typeTransform",
                                            arguments={
                                                "inputArtifact": data_source_step.outputs["outputArtifact"],
                                                "execution": execution_input,
                                                "outputTable":"pai_temp_181827919_818182838",
                                                "cols_to_double": cols_to_double_input,
                                            })

        # 指定复合pipeline定义的输出信息
        p.create_output_artifact("transformedArtifact",
                                 type_transform_step.outputs["outputArtifact"])
        return p
    
    # 新的复合Pipeline instance.
    p = create_composite_pipeline(session)
    # 新的复合Pipeline可以直接提交运行
    p.run(job_name="demo-composite-pipeline-run", arguments={
            "execution": {
                "odpsInfoFile": "/share/base/odpsInfo.ini",
                "endpoint": "http://service.cn-shanghai.maxcompute.aliyun.com/api",
                "logViewHost": "http://logview.odps.aliyun.com",
                "odpsProject": "default_project",
            },
            "cols_to_double": "time,hour,pm2,pm10,so2,co,no2",
            "table_name": "pai_online_project.wumai_data",
        }, wait=False)

    # 也可以保存到服务端
    pipeline_id = session.create_pipeline(p.to_dict())
    # 这个Pipeline后续可以作为其他复合pipeline的子节点使用，


Estimator
-------------------------------------------


SDK支持Pipeline作为一个Estimator调用fit接口, 向服务端提交一个任务, 返回一个EstimatorJob，它与提交的任务关联.

返回的Job实例，支持管理任务运行，获取Estimator的运行返回结果，能够使用返回的Model Artifact创建一个Model对象 (Model部署到EAS尚未完成).


.. code-block:: python

    pipeline = Pipeline.get_by_identifier(logisticregression-binary-xflow-maxCompute",
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
    job.attach(log_outputs=False, timeout=240)
    print(job.get_status())
    print(job.get_outputs())

    model = est.create_model(output_name="outputArtifact")


    # OfflineModel支持获得一个OfflineTransformer, 用于批量预测
    transformer = model.transformer()
    tf_job = transformer.transform("odps://pai_sdk_test/tables/test_dataset", wait=False)



XFlow Algorithm
-------------------------------------------


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

    run_job.attach()
    offline_model = run_job.create_model(output_name="outputArtifact")
