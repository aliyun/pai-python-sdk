使用工作流
===========================================


PAI SDK封装了PAI在阿里云上提供的服务，使得用户能够在代码中已更加灵活的方式调用PAI的服务。

用户可以通过SDK完成Pipeline的构造，提交运行，并且可以将Pipeline保存，用于运行复用或是作为新的Pipeline的一个节点。 提交运行的任务可以在PAI管控台中查看具体的运行DAG，任务日志, 以及任务输出的模型，数据，或是metrics, 输出的模型可以部署到PAI的EAS(Elastic Algorithm Service)服务。


.. toctree::
    :maxdepth: 1

    pipeline/pipeline
    pipeline/custom_job
    pipeline/custom_operator
    pipeline/conditional_workflow
