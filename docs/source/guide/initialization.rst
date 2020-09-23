======================
Initialization
======================

PAI SDK依赖于PAI在阿里云上提供的服务, SDK的Session负责与PAI的后端服务，以及依赖的其他阿里云服务进行交互。 Session封装了用户需要提供鉴权凭证Access Key，使用的PAI服务的region, 以及当前使用工作空间。

setup_default_session方法会初始化一个全局默认的session对象, PipelineRun/PipelineTemplate/PipelineStep等默认通过default session去访问PAI Service.


.. note:: 

    目前PAIFlow服务仅在cn-shanghai区域提供，region_id需要设置为cn-shanghai.



.. code-block:: python

    from pai.core.session import setup_default_session
    from pai.pipeline.run import PipelineRun
    from pai.common import ProviderAlibabaPAI


    session = setup_default_session(access_key_id="your_access_key_id", access_key_secret="your_access_key_secret",
        region_id="cn-shanghai")

    for pipeline_info in session.list_pipeline(provider=ProviderAlibabaPAI):
        print(pipeline_info["PipelineId"])

    for run_instance in PipelineRun.list():
        print(run_instance)
    
    for templ in PipelineTemplate.list(provider=ProviderAlibabaPAI):
        print(templ)
