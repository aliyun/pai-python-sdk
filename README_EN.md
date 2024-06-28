# PAI Python SDK


English \| [简体中文](./README.md)

The PAI Python SDK is provided by Alibaba Cloud\'s [Platform for Artificial Intelligence (PAI)](https://www.aliyun.com/product/bigdata/learn). It offers a user-friendly High-Level API, enabling machine learning engineers to easily train and deploy models on PAI using Python, streamlining the machine learning workflow.

## Installation 🔧

Install the PAI Python SDK using the following command, which supports Python versions \>= 3.8 :

```shell
python -m pip install alipai
```

## 📖 Documentation

Find detailed documentation, including API references and user guides, in the [docs](./docs/) directory or visit [PAI Python SDK Documentation](https://alipai.readthedocs.io/).

## 🛠 Basic Usage

- Submit a custom training job

The following example demonstrates how to submit a custom training job to PAI:

```python
from pai.estimator import Estimator
from pai.image import retrieve

est = Estimator(
    # Retrieve the latest PyTorch image provided by PAI
    image_uri=retrieve(
        framework_name="PyTorch", framework_version="latest"
    ).image_uri,
    command="echo hello",
    # Optionally, specify the source_dir to upload your training code:
    # source_dir="./train_src",
    instance_type="ecs.c6.large",
)

# Submit the training job
est.fit()

print(est.model_data())
```

- Deploy Large Language Model

PAI provides numerous pretrained models that you can easily deploy using the PAI Python SDK:

```python
from pai.model import RegisteredModel

# Retrieve the QWen1.5-7b model provided by PAI
qwen_model = RegisteredModel("qwen1.5-7b-chat", model_provider="pai")

# Deploy the model
p = qwen_model.deploy(service_name="qwen_service")

# Call the service
p.predict(
    data={
        "prompt": "How to install PyTorch?",
        "system_prompt": "You are helpful assistant.",
        "temperature": 0.8,
    }
)

# Call the LLM service with openai SDK.
openai_client = p.openai()
res = openai_client.chat.completions.create(
    model="default",
    max_tokens=1024,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the purpose of life?"}
    ]
)
print(res.choices[0].message.content)


```

For more details, please refer to the [PAI Python SDK Documentation](https://alipai.readthedocs.io/).

## 🤝 Contributing

Contributions to the PAI Python SDK are welcome. Please read our contribution guidelines in the [CONTRIBUTING](./CONTRIBUTING.md) file.

## 📝 License

PAI Python SDK is developed by Alibaba Cloud and licensed under the Apache License (Version 2.0).

## 📬 Contact

For support or inquiries, please open an issue on the GitHub repository or contact us in the DingTalk group:

<img src="./assets/dingtalk-group.png" alt="DingTalkGroup" width="500"/>
