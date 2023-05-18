PAI Python SDK 文档
===========================================

**PAI (Platform for Artificial Intelligence)** 是阿里云提供的机器学习平台，支持用户在云上完成从数据处理、训练、模型管理、到模型部署的端到端的机器学习流程。

**PAI Python SDK** 是PAI提供的Python SDK，提供了更易用的HighLevel API，支持算法工程师简单地使用Python在PAI完成模型训练和部署，串联机器学习的流程。


概览
--------


.. toctree::
    :maxdepth: 1
    :caption: GettingStarted

    getting_started
    permission


.. toctree::
    :maxdepth: 1
    :caption: UserGuide

    user-guide/estimator
    user-guide/model


.. toctree::
    :maxdepth: 1
    :caption: Tutorial

    训练和部署 PyTorch 模型<tutorial/pytorch_mnist/pytorch_mnist>
    训练和部署 XGBoost 模型<tutorial/xgboost_breast_cancer/xgboost_breast_cancer>
    训练和部署 Tensorflow 模型<tutorial/tensorflow_image_classification/tensorflow_image_classification>
    基于HuggingFace BERT训练和部署情感分类模型<tutorial/huggingface_bert/huggingface_bert>
    使用ModelScope ViT训练和部署图片分类模型<tutorial/modelscope_vit/modelscope_vit>



.. toctree::
    :maxdepth: 1
    :caption: Reference

    reference
    PAI帮助文档 <https://help.aliyun.com/product/30347.html>
