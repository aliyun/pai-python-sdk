# PAI Python SDK

[English](./README.md) \| 简体中文

PAI Python SDK是阿里云 [机器学习平台 PAI(Platform for Artificial Intelligence)](https://www.aliyun.com/product/bigdata/learn) 提供的Python SDK，提供了更易用的HighLevel API，支持机器学习工程师简单地使用Python在PAI完成模型训练和部署，串联机器学习的流程。

## 🔧 安装

使用以下命令安装PAI Python SDK（支持Python版本 \>= 3.6，建议使用Python版本 \>= 3.8）：

```shell
python -m pip install alipai
```

## 📖 文档

请通过访问 [PAI Python SDK文档](https://alipai.readthedocs.io/) 或是查看 [docs](./docs) 目录下的文件获取SDK的详细文档，包括用户指南和API文档。

## 🛠 使用示例

- 提交自定义训练任务

以下代码演示了如何通过SDK提交一个自定义的训练作业:

```python
from pai.estimator import Estimator
from pai.image import retrieve

est = Estimator(
    # 获取PAI提供的最新PyTorch镜像
    image_uri=retrieve(
        framework_name="PyTorch", framework_version="latest"
    ).image_uri,
    command="echo hello",
    # 可选，指定source_dir上传你的训练代码：
    # source_dir="./train_src",
    instance_type="ecs.c6.large",
)
# 提交训练任务
est.fit()
print(est.model_data())

```

- 部署大语言模型

PAI提供了大量预训练模型，可以使用PAI Python SDK轻松部署：

```python
from pai.model import RegisteredModel

# 获取PAI提供的QWen-7b模型
qwen_model = RegisteredModel("qwen-7b-chat-lora", model_provider="pai")
# 部署模型
p = qwen_model.deploy(service_name="qwen_service")
# 调用服务
p.predict(
    data={
        "prompt": "如何安装PyTorch？",
        "system_prompt": "表现得像一位有5年以上经验的程序员。",
        "temperature": 0.8,
    }
)
```

更多功能介绍，请参阅 [PAI Python SDK文档](https://alipai.readthedocs.io/) 。

## 🤝 贡献代码

我们欢迎为PAI Python SDK贡献代码。请阅读 [CONTRIBUTING](./CONTRIBUTING.md) 文件了解如何为本项目贡献代码。

## 📝 许可证

PAI Python SDK是由阿里云开发，并根据Apache许可证（版本2.0）授权使用。

## 📬 联系方式

如需支持或咨询，请在GitHub仓库中提交issue，或通过钉钉群联系我们：

<img src="./assets/dingtalk-group.png" alt="DingTalkGroup" width="500"/>
