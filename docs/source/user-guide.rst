
用户手册
===========================================


.. note:: 

    目前版本的SDK还未完成模型部署到EAS功能，提交任务后，SDK会打印具体的任务在PAI管理页面的URL，可以在Web页面完成模型的注册和部署.

PAI SDK封装了PAI在阿里云上提供的服务，使得用户能够在代码中已更加灵活的方式调用PAI的服务。SDK目前主要提供了基于PAIFlow(PAI平台的ML Pipeline Service)的Pipeline运行管理功能。

用户可以通过SDK完成Pipeline的构造，提交运行，并且可以将Pipeline保存，用于运行复用或是作为新的Pipeline的一个节点。 提交运行的任务可以在PAI管控台中查看具体的运行DAG，任务日志, 以及任务输出的模型，数据，或是metrics, 输出的模型可以部署到PAI的EAS(Elastic Algorithm Service)服务。


.. toctree::
   :maxdepth: 2

   guide/initialization
   guide/pipeline
   guide/operator
   guide/estimator

