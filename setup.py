from __future__ import absolute_import

import sys
import os

from setuptools import setup, find_packages

repo_root = os.path.dirname(os.path.abspath(__file__))

requirements = [
    "aliyun-python-sdk-core==2.13.25",
    "aliyun-python-sdk-sts>=3.0.2",
    "graphviz>=0.14",
    "numpy>=1.16.0",
    "oss2>=2.8.0",
    "pyodps>=0.9.3.2",
    "pyyaml>=5.3.1",
    "six>=1.15.0",
    "importlib_metadata==2.0.0",
    "docker>=4.4.0",
]


if sys.version_info < (3, 8):
    requirements.append("importlib_metadata == 2.1.0")

if sys.version_info < (3, 4):
    requirements.append("enum34 >= 1.1.6")

long_description = None
if os.path.exists("README.md"):
    with open("README.md") as f:
        long_description = f.read()

setup(
    name="alipai",
    python_requires=">=2.7",
    version="0.1.7",
    description="Alibaba Cloud PAI Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
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
