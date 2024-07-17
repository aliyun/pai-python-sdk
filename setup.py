from __future__ import absolute_import

import os

from setuptools import find_packages, setup

pkg_root = os.path.dirname(os.path.abspath(__file__))

REQUIREMENTS_FILE = "requirements/requirements.txt"
PACKAGE_NAME = os.getenv("PACKAGE_NAME", "pai")

version_data = {}
with open(os.path.join(pkg_root, "pai/version.py")) as fp:
    exec(fp.read(), version_data)
version = version_data["VERSION"]


def read_requirements():
    with open(os.path.join(pkg_root, REQUIREMENTS_FILE), "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]


long_description = None
if os.path.exists("README.md"):
    with open("README.md") as f:
        long_description = f.read()

setup(
    name=PACKAGE_NAME,
    python_requires=">=3.8",
    version=version,
    setup_requires=["setuptools_scm"],
    description="Alibaba Cloud PAI Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://www.aliyun.com/product/bigdata/product/learn",
    packages=find_packages(include=["pai", "pai.*"]),
    install_requires=read_requirements(),
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
