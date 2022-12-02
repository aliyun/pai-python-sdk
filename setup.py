from __future__ import absolute_import

import os

from setuptools import find_packages, setup

pkg_root = os.path.dirname(os.path.abspath(__file__))

PKG_VERSION_FILE = "pai/VERSION"


def read_version():
    with open(os.path.join(pkg_root, PKG_VERSION_FILE), "r") as f:
        return f.readline().strip()


requirements = [
    "aliyun-python-sdk-core==2.13.25",
    "aliyun-python-sdk-sts>=3.0.2",
    # graphviz drop Python2 support in 0.17, drop Python3.6 support in 0.19.1
    # https://graphviz.readthedocs.io/en/latest/changelog.html#version-0-17
    "graphviz<0.17",
    "numpy>=1.16.0",
    "oss2>=2.8.0",
    "pyodps>=0.11.0",
    "pyyaml>=5.3.1",
    "six>=1.15.0",
    "importlib_metadata>=2.0.0, <=2.1.0",
    "docker>=4.4.0",
    "marshmallow",
    "marshmallow-oneofschema==3.0.1",
    "eas_prediction<=0.13",
    "alibabacloud_tea_util>=0.3.6, <1.0.0",
    "alibabacloud_tea_openapi>=0.3.3, <1.0.0",
    "alibabacloud_openapi_util>=0.1.6, <1.0.0",
    "alibabacloud_endpoint_util>=0.0.3, <1.0.0",
]

long_description = None
if os.path.exists("README.md"):
    with open("README.md") as f:
        long_description = f.read()

setup(
    name="alipai",
    python_requires=">=3.6",
    version=read_version(),
    description="Alibaba Cloud PAI Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://www.aliyun.com/product/bigdata/product/learn",
    packages=find_packages(include=["pai", "pai.*"]),
    install_requires=requirements,
    author="Alibaba PAI team",
    keywords="ML Alibaba Cloud PAI Training Inference Pipeline",
    license="Apache License 2.0",
    classifier=[
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
    ],
)
