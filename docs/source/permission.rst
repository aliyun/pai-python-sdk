======================
用户权限配置
======================

当用户以 RAM 子账号身份，通过 PAI Python SDK 使用 PAI 时，首先需要为该 RAM 子账号进行授权，主要包括：

- PAI工作空间授权

- OSS 授权

- 模型在线服务(PAI-EAS)授权


工作空间配置
------------------

用户使用 PAI 时，需要指定访问的工作空间。RAM 子账号需要被添加到工作空间内，才能访问和使用对应的工作空间。当用户需要进行模型开发或是部署时，需要在工作空间内是 **算法开发角色** 或是 **管理员角色**。

如何添加和修改工作空间内的成员以及其权限，请查看相关文档: `管理成员 <https://help.aliyun.com/document_detail/326194.html#section-ajl-hie-emf>`_ 。


OSS 授权
------------------

PAI 默认使用 OSS Bucket存储用户的代码，输出模型。RAM 子账号需要有权限能够访问当前配置的OSS Bucket，用于代码上传，或是模型保存。用户可以参考以下自定义权限策略，对RAM子账号进行权限配置 ，其中 ``<yourBucketName>`` 需要替换为需要使用的 OSS Bucket的名称。

.. code-block:: json

	{
		"Version": "1",
		"Statement": [
			{
				"Action": [
					"oss:GetObject",
					"oss:ListObjects",
					"oss:DeleteObject",
					"oss:ListParts",
					"oss:PutObject",
					"oss:AbortMultipartUpload",
					"oss:GetBucketCors",
					"oss:GetBucketCors",
					"oss:DeleteBucketCors"
				],
				"Resource": [
					"acs:oss:*:*:<yourBucketName>",
					"acs:oss:*:*:<yourBucketName>/*"
				],
				"Effect": "Allow"
			},
			{
				"Action": [
					"oss:ListBuckets"
				],
				"Resource": "*",
				"Effect": "Allow"
			}
		]
	}


对于 OSS RAM Policy的更加详细的介绍，可以见文档: `RAM Policy概述 <https://help.aliyun.com/document_detail/100680.htm#concept-y5r-5rm-2gb>`_ 。


模型在线服务权限配置
---------------------

PAI-EAS 是 PAI 提供的模型在线推理产品，RAM 子账号需要配置相应的权限才能够调用 PAI-EAS 提供的 API 部署推理服务。

- 为 RAM 用户授予 PAI-EAS 的管理权限:

PAI-EAS 提供系统策略 ``AliyunPAIEASFullAccess`` ，包含了 PAI-EAS 的管理权限。为 RAM 用户授予该权限后， RAM 用户即可拥有使用 PAI-EAS 功能的完整权限。


- 为 RAM 用户进行精细化授权:

PAI-EAS 支持用户通过创建自定义权限策略的方式为 RAM 用户进行精细化授权，详细配置请见文档: `云产品依赖与授权EAS <https://help.aliyun.com/document_detail/130001.html>`_ 。
