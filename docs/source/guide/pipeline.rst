======================
构建和运行工作流
======================

PAIFlow，是PAI平台研发的Workflow Service，提供了机器学习工作流编排和运行管理的功能, 支持通过SDK编排和运行Workflow。

组件
----------------------


Operator是PAI Pipeline Service中的算法组件, 也是一个PAIFlow中可运行的组件定义, 包含了组件的输入输出信息，以及具体执行的实现（可能是一个DAG执行或是一个单独的镜像执行）。

用户可以从PAI服务获取保存在PAI后端的算法组件，也可以使用从本地构造的Pipeline/Operator对象中抽取出对应的算法组件。 通过operator的raw_manifest属性可以获得YAML格式定义的算法组件的schema。

PAI提供了一些公共的算法组件，在SavedOperator.list方法中, 通过指定provider为ProviderAlibabaPAI，可以拉取到PAI提供的算法组件列表。用户可以通过inputs, outputs属性查看对应组件的输入输出信息。

.. code-block:: python

    from pai.operator import SavedOperator
    from pai.common import ProviderAlibabaPAI

    for op in SavedOperator.list(provider=ProviderAlibabaPAI):
        print(op.pipeline_id, op.identifier, op.provider, op.version)

    op = next(SavedOperator.list(provider=ProviderAlibabaPAI))
    # inspect the inputs and outputs of the operator.
    print(op.inputs)
    print(op.outputs)


开发者可以通过指定identifier-provider-version 或是 pipeline_id从PAIFlow获取一个唯一算法组件，区别是前者是由组件开发者在保存组件时指定，而后者是由PAIFlow生成的组件的唯一ID标识。

通过指定组件的必须输入参数信息，用户可以将提交一个运行任务。 以下的的例子中，使用了PAI提供的split算法组件，将输入数据表按给定比例拆分到两张新表中。

在提交执行任务后，SDK会在console中输出任务在PAI的管控台中的URL，用户自己也可以通过直接在 `PAI的管控台 <https://pai.data.aliyun.com/console>`_ 通过返回的运行任务ID或是提交任务名称查找对应的任务实例。 用户可以在详情页面中查看任务执行的执行DAG，执行任务日志，以及执行的输出，并且可以将模型直接推送部署到EAS服务。


.. code-block:: python

    from pai.common.utils import gen_temp_table

    op = SavedOperator.get_by_identifier(identifier="split", provider=ProviderAlibabaPAI, version="v1")
    print(op.inputs)

    # split 运行在MaxCompute中，需要指定运行的MaxCompute项目以及执行环境。
    # maxc_execution 作为算法组件的一个输入，标识算法组件的执行MaxCompute引擎。
    maxc_execution = {
        "odpsInfoFile": "/share/base/odpsInfo.ini",
        "endpoint": "http://service.cn-shanghai.maxcompute.aliyun.com/api",
        "odpsProject": "YOUR_MAX_COMPUTE_PROJECT",
    }

    pipeline_run = op.run(
        job_name="example-split-job",
        arguments={
            "execution":maxc_execution,
            "inputArtifact": "odps://pai_online_project/tables/wumai_data",
            "fraction": 0.7,
            "output1TableName": gen_temp_table(),
            "output2TableName": gen_temp_table(),
        }
    )

    print(pipeline_run.outputs)


构建工作流
----------------------


机器学习任务负载，通常并不是只包含一个训练任务, 可能包含了特征处理，数据拆分，训练，模型校验，部署等等。这个过程中主要是不同数据处理/算法组件的协同，算法组件的输入输出。通常的解决方案是将这些上下游的数据处理和算法组件拼接为一个Pipeline，提交作为一个整体的任务执行。

PAI Pipeline Service支持将多个算法组件拼接成为一个一个新的Pipeline，新建的复合Pipeline可以通过提供输入参数提交运行，或是保存为一个复合工作流组件。

保存的Pipeline组件可以作为一个普通组件直接运行(如以上的PipelineTemplate中的例子)，或是作为新创建的Pipeline的一个节点。


创建一个新的Pipeline主要包括以下流程:

1. 定义Pipeline的输入信息：包括用户的输入参数PipelineParameter或是数据输入PipelineArtifact, 对于数据输入，目前PAI Pipeline Service支持OSS上的数据，以及MaxCompute上的Table, Volumes，OfflineModel。

2. 创建Pipeline中的Step，以及step的输入, step的输入可能来自于其他step，也可能来源于当前创建的Pipeline的输入。

3. 指定Pipeline的输出信息: Pipeline可以使用引用的方式使用step节点的输出作为新的Pipeline中的输出。


.. code-block:: python

    from pai.pipeline.types import PipelineParameter, PipelineArtifact, ArtifactMetadata, ArtifactDataType, ArtifactLocationType
    from pai.pipeline import PipelineStep, Pipeline
    from pai.operator import SavedOperator

    def create_composite_pipeline():
        # 定义当前的Pipeline的Inputs
        execution_input = PipelineParameter(name="execution", typ=dict)
        cols_to_double_input = PipelineParameter(name="cols_to_double")
        table_input = PipelineArtifact(name="dataSource", metadata=ArtifactMetadata(
                data_type=ArtifactDataType.DataSet,
                location_type=ArtifactLocationType.MaxComputeTable))

        # 指定identifier-provider-version, 使用一个已经保存的组件，作为Pipeline的一个Step
        type_transform_step = PipelineStep(
            identifier="type-transform-xflow-maxCompute", provider=ProviderAlibabaPAI,
            version="v1", name="typeTransform", inputs={
                "inputArtifact": table_input, "execution": execution_input,
                "outputTable": gen_temp_table(), "cols_to_double": cols_to_double_input,
            }
        )

        # PipelineTemplate也可以作为一个Step构建Pipeline
        split_operator = SavedOperator.get_by_identifier(identifier="split-xflow-maxCompute",
         provider=ProviderAlibabaPAI, version="v1")

        split_step = split_operator.as_step(inputs={"inputArtifact": type_transform_step.outputs[0],
                "execution": execution_input, "output1TableName": gen_temp_table(),
                "fraction": 0.5, "output2TableName": gen_temp_table(),
            })

        # Pipeline构造函数中的steps和inputs信息并不要求完整输入，Pipeline graph时，是通过Pipeline的outputs和steps，推导他们的依赖，从而构造对应的执行DAG
        p = Pipeline(
            steps=[split_step],
            outputs=split_step.outputs[:2],
        )
        return p


通过指定组件名称和版本，Pipeline可以保存到服务端成为一个可复用组件。 保存组件默认共享给阿里云账号的其他用户, 后续Pipeline的分享和权限管理主要会由当前开发中的工作空间功能负责。

.. code-block:: python

    p = create_composite_pipeline()
    # 输入Pipeline运行所需参数(arguments）后，提交到PAI Service运行
    pipeline_run = p.run(job_name="demo-composite-pipeline-run", arguments={
                "execution": maxc_execution,
                "cols_to_double": "time,hour,pm2,pm10,so2,co,no2",
                "data_source": "odps://pai_online_project/tables/wumai_data",
            }, wait=True)

    # 指定identifier和版本保存Pipeline
    p = p.save(identifier="demo-composite-pipeline", version="v1")
    print(p.pipeline_id, p.identifier, p.version, p.provider)
