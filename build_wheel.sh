#!/usr/bin/env bash

ROOT_DIR=$(cd "$(dirname "$0")";pwd)
cd ${ROOT_DIR}

python3 setup.py bdist_wheel --universal




