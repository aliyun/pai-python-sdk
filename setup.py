from __future__ import absolute_import

import os

from setuptools import setup, find_packages

repo_root = os.path.dirname(os.path.abspath(__file__))


def _load_version_info():
    try:
        execfile
    except NameError:
        def execfile(fname, globs, locs=None):
            locs = locs or globs
            exec(compile(open(fname).read(), fname, "exec"), globs, locs)

    version_ns = {}
    execfile(os.path.join(repo_root, 'pai', '_version.py'), version_ns)
    return version_ns['__version__']


requirements = []
with open('requirements.txt') as f:
    requirements.extend(f.read().splitlines())
long_description = None
if os.path.exists('README.md'):
    with open('README.md') as f:
        long_description = f.read()

setup(
    name="alipai",
    python_requires=">=2.7",
    version=_load_version_info(),
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
    ]
)
