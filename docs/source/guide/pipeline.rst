======================
Pipeline
======================

PAIFlow，是PAI平台研发的ML Pipeline Service，提供了机器学习工作流编排和运行管理的功能, 支持通过SDK编排和运行pipeline。

PipelineTemplate
----------------------


PipelineTemplate对象是PAIFlow中的算法组件, 也是一个PAIFlow中可运行的工作流定义, 包含了组件的输入输出信息，以及具体执行的实现（可能是一个DAG执行或是一个单独的镜像执行）。 

用户可以从PAI服务获取保存在PAI后端的算法组件，也可以使用从本地构造的Pipeline/Component对象中抽取出对应的算法组件。 通过template的raw_manifest属性可以获得YAML格式定义的算法组件的schema。

PAI提供了一些公共可读的算法组件，在PipelineTemplate.list方法中, 通过指定provider为ProviderAlibabaPAI，可以拉取到PAI提供的算法组件列表。用户可以通过inputs, outputs属性查看对应组件的输入输出信息。

.. code-block:: python

    from pai.pipeline.template import PipelineTemplate
    from pai.common import ProviderAlibabaPAI

    for templ in PipelineTemplate.list(provider=ProviderAlibabaPAI):
        print(templ.pipeline_id, templ.identifier, templ.provider, templ.version)

    template = next(PipelineTemplate.list(provider=ProviderAlibabaPAI))
    # inspect the inputs and outputs of the template.
    print(template.inputs)
    print(template.outputs)


开发者可以通过指定identifier-provider-version 或是 pipeline_id从PAIFlow获取一个唯一算法组件，区别是前者是由组件开发者在保存组件时指定，而后者是由PAIFlow生成的组件的唯一ID标识。

通过指定组件的必须输入参数信息，用户可以将提交一个运行任务。 以下的的case中，使用了PAI提供的split算法组件，将输入数据表按给定比例拆分到两张新表中。

在提交执行任务后，SDK会在console中输出任务在PAI的管控台中的URL，用户自己也可以通过直接在 `PAI的管控台 <http://baidua.com>`_ 通过返回的运行任务ID或是提交任务名称查找对应的任务实例。 用户可以在详情页面中查看任务执行的执行DAG，执行任务日志，以及执行的输出，并且可以将模型直接推送部署到EAS服务。


.. code-block:: python

    # split-xflow-maxCompute 运行在MaxCompute中，需要指定运行的MaxCompute项目以及执行环境。
    # xflow_execution 作为算法组件的一个输入，标识算法组件的执行MaxCompute引擎。
    xflow_execution = {
        "odpsInfoFile": "/share/base/odpsInfo.ini",
        "endpoint": "http://service.cn-shanghai.maxcompute.aliyun.com/api",
        "logViewHost": "http://logview.odps.aliyun.com",
        "odpsProject": "your_max_compute_project",
    }

    pipeline_run = templ.run(
        job_name="example-split-job",
        arguments={
            "execution":xflow_execution,
            "inputArtifact": "odps://pai_online_project/tables/wumai_data",
            "fraction": 0.7,
            "output1TableName": gen_temp_table(),
            "output2TableName": gen_temp_table(),
        }
    )

    print(pipeline_run.outputs)


Pipeline Build
----------------------


机器学习任务负载，通常并不是只包含一个训练任务, 可能包含了特征处理，数据拆分，训练，模型校验，部署等等。这个过程中主要是不同数据处理/算法组件的协同，算法组件的输入输出。通常的解决方案是将这些上下游的数据处理和算法组件拼接为一个Pipeline，提交作为一个整体的任务执行。

PAIFlow支持将多个算法组件拼接成为一个一个新的Pipeline，新建的复合Pipeline支持输入参数提交运行，或是保存为一个组件，保存的Pipeline组件可以作为一个普通组件直接运行，或是作为新创建的Pipeline的一个节点。


创建一个新的Pipeline主要包括以下流程:

1. 定义Pipeline的输入信息：包括用户的输入参数PipelineParameter或是数据输入PipelineArtifact, 对于数据输入，目前PAIFlow支持OSS上的数据，以及MaxCompute上的Table, Volumes，OfflineModel。

2. 创建Pipeline中的Step，以及step的输入, step的输入可能来自于其他step，也可能来源于当前创建的Pipeline的输入。

3. 指定Pipeline的输出信息: Pipeline可以使用引用的方式使用step节点的输出作为新的Pipeline中的输出。

.. note::

    Pipeline构造函数中的steps和inputs信息并不要求完整输入，Pipeline graph时，是通过Pipeline的outputs和steps，推导他们的依赖，从而构造对应的执行DAG


.. code-block:: python

    def create_composite_pipeline():
        # Define the inputs parameters/artifacts in pipeline
        execution_input = PipelineParameter(name="execution", typ=dict)
        cols_to_double_input = PipelineParameter(name="cols_to_double")
        table_input = PipelineArtifact(name="data_source", metadata=ArtifactMetadata(
                data_type=ArtifactDataType.DataSet,
                location_type=ArtifactLocationType.MaxComputeTable))

        # Pipeline step from remote PAI service.
        type_transform_step = PipelineStep(
            identifier="type-transform-xflow-maxCompute", provider=ProviderAlibabaPAI,
            version="v1", name="typeTransform", inputs={
                "inputArtifact": table_input, "execution": execution_input,
                "outputTable": gen_temp_table(), "cols_to_double": cols_to_double_input,
            }
        )

        split_template = PipelineTemplate.get_by_identifier(identifier="split-xflow-maxCompute",
         provider=ProviderAlibabaPAI, version="v1")

        split_step = split_template.as_step(inputs={"inputArtifact": type_transform_step.outputs[0],
                "execution": execution_input, "output1TableName": gen_temp_table(),
                "fraction": 0.5, "output2TableName": gen_temp_table(),
            })

        p = Pipeline(
            steps=[split_step],
            outputs=split_step.outputs[:2],
        )
        return p



通过指定组件名称和版本，Pipeline可以保存到服务端成为一个可复用组件。 保存组件默认共享给阿里云账号的其他用户, 后续Pipeline的分享和权限管理主要会由当前开发中的工作空间功能负责。

.. code-block:: python

    p = create_composite_pipeline()
    # Run pipeline
    pipeline_run = p.run(job_name="demo-composite-pipeline-run", arguments={
                "execution": xflow_execution,
                "cols_to_double": "time,hour,pm2,pm10,so2,co,no2",
                "data_source": "odps://pai_online_project/tables/wumai_data",
            }, wait=True)

    # Save Pipeline
    p = p.save(identifier="demo-composite-pipeline", version="v1")
    print(p.pipeline_id, p.identifier, p.version, p.provider)


User Defined Component (Beta)
-------------------------------------

PAIFlow支持用户创建自定义运行模板，用户需要提供模板的输入输出信息, 对应的镜像和配置，以及Component执行镜像的Command，构建一个基于镜像的算法组件。

.. code-block:: python

    from pai.pipeline.core import ContainerComponent

    inputs = [
        PipelineParameter(name="xflow_name", typ=str),
    ]
    outputs = [
        PipelineArtifact(name="output1", metadata=ArtifactMetadata(
            data_type=ArtifactDataType.DataSet,
            location_type=ArtifactLocationType.OSS))
    ]

    img_uri = "python:3"
    img_registry_config = {
            "userName": "registry_username",
            "password": "registry_password",
    }

    comp = ContainerComponent(
        image_uri=img_uri,
        image_registry_config=img_registry_config,
        inputs=inputs,
        outputs=outputs,
        command=[
            "python",
            "-c",
            """import sys\nprint(sys.path)\nprint("{{inputs.parameters.xflow_name}}")""",
        ])

    p = comp.save(identifier="test-comp", version=str(time.time()))

