#  Copyright 2024 Alibaba, Inc. or its affiliates.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import distutils.dir_util
import json
import os
import posixpath
import re
import shlex
import shutil
import tempfile
import textwrap
import typing
from typing import Any, Dict

from pai.session import Session

from ..common.consts import INSTANCE_TYPE_LOCAL_GPU
from ..common.docker_utils import ContainerRun, run_container
from ..common.logging import get_logger
from ..common.oss_utils import OssUriObj, download, is_oss_uri

if typing.TYPE_CHECKING:
    from ..estimator import Estimator


logger = get_logger(__name__)


class _TrainingEnv(object):
    ENV_PAI_HPS = "PAI_HPS"
    ENV_PAI_HPS_PREFIX = "PAI_HPS_"
    ENV_PAI_USER_ARGS = "PAI_USER_ARGS"
    ENV_PAI_INPUT_PREFIX = "PAI_INPUT_"
    ENV_PAI_OUTPUT_PREFIX = "PAI_OUTPUT_"
    ENV_PAI_WORKING_DIR = "PAI_WORKING_DIR"


class _TrainingJobConfig(object):
    WORKING_DIR = "/ml/usercode/"
    INPUT_CONFIG_DIR = "/ml/input/config/"
    INPUT_DATA_DIR = "/ml/input/data/"
    OUTPUT_DIR = "/ml/output/"


_ENV_NOT_ALLOWED_CHARS = re.compile(r"[^a-zA-Z0-9_]")
_TRAINING_LAUNCH_SCRIPT_TEMPLATE = textwrap.dedent(
    """\
#!/bin/sh

env

# change to working directory
if [ -n "$PAI_WORKING_DIR" ]; then
    echo "Change to Working Directory", $PAI_WORKING_DIR
    mkdir -p $PAI_WORKING_DIR && cd $PAI_WORKING_DIR
fi

# install requirements
if [ -e "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt"
    python -m pip install -r requirements.txt
fi

echo "User program launching"
echo "-----------------------------------------------------------------"

sh {0}
"""
)


class LocalTrainingJob(object):
    """A class that represents a local training job running with docker container."""

    def __init__(
        self,
        estimator: "Estimator",
        inputs: Dict[str, Any],
        instance_type: str = None,
        temp_dir: str = None,
        job_name: str = None,
    ):
        self.estimator = estimator
        self.inputs = inputs
        self.tmp_dir = temp_dir or tempfile.mkdtemp()
        self.job_name = job_name
        self.instance_type = instance_type
        logger.info("Local TrainingJob temporary directory: {}".format(self.tmp_dir))
        self._container_run: ContainerRun = None

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if self._container_run:
            container = self._container_run.container
            container_name, container_id, status = (
                container.name,
                container.id,
                container.status,
            )
        else:
            container_name, container_id, status = None, None, None
        return f"LocalTrainingJob(container_name={container_name}, container_id={container_id}, status={status})"

    @property
    def session(self) -> Session:
        return self.estimator.session

    def prepare_env(self) -> Dict[str, str]:
        """Prepare environment variables for the training job."""

        # Hyperparameters environment variables
        def _normalize_name(name: str) -> str:
            # replace all non-alphanumeric characters with underscore
            return _ENV_NOT_ALLOWED_CHARS.sub("_", name).upper()

        env = {}
        user_args = []
        for name, value in self.estimator.hyperparameters.items():
            env[_TrainingEnv.ENV_PAI_HPS_PREFIX + _normalize_name(name)] = str(value)
            user_args.extend(["--" + name, shlex.quote(str(value))])
        env[_TrainingEnv.ENV_PAI_USER_ARGS] = " ".join(
            [shlex.quote(v) for v in user_args]
        )
        env[_TrainingEnv.ENV_PAI_HPS] = json.dumps(
            {name: str(value) for name, value in self.estimator.hyperparameters.items()}
        )

        # Environments for input channel
        for name, value in self.inputs.items():
            if (is_oss_uri(value) and value.endswith("/")) or os.path.isdir(value):
                env[
                    _TrainingEnv.ENV_PAI_INPUT_PREFIX + _normalize_name(name)
                ] = posixpath.join(_TrainingJobConfig.INPUT_DATA_DIR, name)
            else:
                file_name = os.path.basename(value)
                env[
                    _TrainingEnv.ENV_PAI_INPUT_PREFIX + _normalize_name(name)
                ] = posixpath.join(_TrainingJobConfig.INPUT_DATA_DIR, name, file_name)

        # Environments for output channel.
        # By default, TrainingJob invoked by Estimator will have two output channels:
        # 'model' and 'checkpoints'
        output_channel = ["model", "checkpoints"]
        for name in output_channel:
            env[
                _TrainingEnv.ENV_PAI_OUTPUT_PREFIX + _normalize_name(name)
            ] = posixpath.join(_TrainingJobConfig.OUTPUT_DIR, name)

        env[_TrainingEnv.ENV_PAI_WORKING_DIR] = _TrainingJobConfig.WORKING_DIR
        return env

    def run(self):
        """Run estimator job in local with docker."""
        output_model_path = self.output_path()
        os.makedirs(output_model_path, exist_ok=True)
        volumes = {}

        tmp_dir = tempfile.mkdtemp()
        # 1. Prepare source code to directory /ml/usercode
        user_code_dir = os.path.join(self.tmp_dir, "user_code")
        if is_oss_uri(self.estimator.source_dir):
            raise RuntimeError("OSS source code is not supported in local training.")
        shutil.copytree(self.estimator.source_dir, user_code_dir)
        volumes[user_code_dir] = {
            "bind": _TrainingJobConfig.WORKING_DIR,
            "mode": "rw",
        }

        # 2. Prepare input data for training job.
        input_data = self.prepare_input_data()
        for host_path, container_path in input_data.items():
            volumes[host_path] = {
                "bind": container_path,
                "mode": "rw",
            }

        # 3. Prepare input config files, such as hyperparameters.json,
        # training-job.json, etc.
        input_config_path = os.path.join(tmp_dir, "config")
        os.makedirs(input_config_path, exist_ok=True)
        self.prepare_input_config(input_config_path=input_config_path)
        volumes[input_config_path] = {
            "bind": _TrainingJobConfig.INPUT_CONFIG_DIR,
            "mode": "rw",
        }

        execution_dir = os.path.join(tmp_dir, "config", "execution")
        os.makedirs(execution_dir, exist_ok=True)
        command_path = os.path.join(execution_dir, "command.sh")
        with open(command_path, "w") as f:
            f.write(self.estimator.command)
        launch_script_path = os.path.join(input_config_path, "launch.sh")
        with open(launch_script_path, "w") as f:
            f.write(
                _TRAINING_LAUNCH_SCRIPT_TEMPLATE.format(
                    posixpath.join(
                        _TrainingJobConfig.INPUT_CONFIG_DIR, "execution/command.sh"
                    )
                )
            )

        # 4. Config output model channel
        volumes[output_model_path] = {
            "bind": posixpath.join(_TrainingJobConfig.OUTPUT_DIR, "model"),
            "mode": "rw",
        }

        gpu_count = (
            -1 if self.instance_type.strip() == INSTANCE_TYPE_LOCAL_GPU else None
        )
        self._container_run = run_container(
            environment_variables=self.prepare_env(),
            image_uri=self.estimator.image_uri,
            entry_point=[
                "/bin/sh",
                posixpath.join(_TrainingJobConfig.INPUT_CONFIG_DIR, "launch.sh"),
            ],
            volumes=volumes,
            working_dir=_TrainingJobConfig.WORKING_DIR,
            gpu_count=gpu_count,
        )

    def prepare_input_config(self, input_config_path):
        """Prepare input config for TrainingJob, such as hyperparameters.json,
        trainingjob.json."""
        with open(os.path.join(input_config_path, "hyperparameters.json"), "w") as f:
            hps = self.estimator.hyperparameters or dict()
            f.write(json.dumps({k: str(v) for k, v in hps.items()}))

    def prepare_input_data(self) -> Dict[str, str]:
        """Prepare input data config."""
        input_data_configs = {}

        for name, input_data in self.inputs.items():
            local_channel_path = os.path.join(self.tmp_dir, f"input/data/{name}")
            os.makedirs(local_channel_path, exist_ok=True)
            input_data_configs[local_channel_path] = posixpath.join(
                _TrainingJobConfig.INPUT_DATA_DIR, name
            )
            if is_oss_uri(input_data):
                oss_uri_obj = OssUriObj(input_data)
                oss_bucket = self.session.get_oss_bucket(oss_uri_obj.bucket_name)
                os.makedirs(local_channel_path, exist_ok=True)
                download(
                    oss_uri_obj.object_key,
                    local_path=local_channel_path,
                    bucket=oss_bucket,
                )
                input_data_configs[local_channel_path] = posixpath.join(
                    _TrainingJobConfig.INPUT_DATA_DIR, name
                )
            else:
                # If the input data is local files, copy the input data to a
                # temporary directory.
                if not os.path.exists(input_data):
                    raise ValueError(
                        "Input data not exists: name={} input_data={}".format(
                            name, input_data
                        )
                    )
                elif os.path.isdir(input_data):
                    distutils.dir_util.copy_tree(input_data, local_channel_path)
                else:
                    shutil.copy(
                        input_data,
                        os.path.join(local_channel_path, os.path.basename(input_data)),
                    )

        return input_data_configs

    def wait(self, show_logs: bool = True):
        self._container_run.watch(show_logs=show_logs)

    def output_path(self, channel_name="model"):
        return os.path.join(self.tmp_dir, "output", f"{channel_name}/")

    def is_succeeded(self):
        """Return True if the training job is succeeded, otherwise return False."""
        return self._container_run.is_succeeded()
