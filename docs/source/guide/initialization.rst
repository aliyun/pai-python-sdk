======================
快速开始
======================

PAI SDK依赖于PAI在阿里云上提供的服务, SDK的Session负责与PAI的后端服务，以及依赖的其他阿里云服务进行交互。 Session封装了用户需要提供鉴权凭证Access Key，使用的PAI服务的region, 以及当前使用工作空间。

请登录阿里云的控制台，获取使用的鉴权凭证和当前可用PAI工作空间:

-  AccessKeyId和AccessKeySecret

请通过
`RAM控制台 <https://ram.console.aliyun.com/manage/ak?spm=a2c8b.12215454.top-nav.dak.1704336aEeHgvy>`__
获取当前账号使用的AK信息

-  WorkspaceId

通过
`PAI的控制台 <https://pai.console.aliyun.com/?spm=a2c4g.11186623.0.0.506a7ba7JBg0qi&regionId=cn-hangzhou#/workspace/list>`__
查看你所在的AI工作空间ID.

-  OSS Bucket Name

通过 `OSS控制台 <https://oss.console.aliyun.com/>`__ 查看可用的OSS
Bucket，请确认使用的OSS region和工作空间是一致的。


.. code-block:: python

    from pai.core.session import setup_default_session, get_default_session
    from pai.pipeline.run import PipelineRun
    from pai.common import ProviderAlibabaPAI
    from pai.operator import SavedOperator

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

    for run_instance in PipelineRun.list():
        print(run_instance)

    for templ in SavedOperator.list(provider=ProviderAlibabaPAI):
        print(templ)
