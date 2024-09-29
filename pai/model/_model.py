#  Copyright 2023 Alibaba, Inc. or its affiliates.
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

import copy
import distutils.dir_util
import json
import os.path
import posixpath
import shlex
import shutil
import tempfile
import textwrap
import time
import typing
import warnings
from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union

import requests
from addict import Dict as AttrDict
from oss2 import ObjectIterator

from ..common import ProviderAlibabaPAI, git_utils
from ..common.consts import INSTANCE_TYPE_LOCAL_GPU, ModelFormat, StoragePathCategory
from ..common.docker_utils import ContainerRun, run_container
from ..common.logging import get_logger
from ..common.oss_utils import OssUriObj, download, is_oss_uri, upload
from ..common.utils import (
    generate_repr,
    is_local_run_instance_type,
    random_str,
    to_plain_text,
)
from ..exception import DuplicatedMountException
from ..image import ImageInfo
from ..job._training_job import InstanceSpec, ModelRecipeSpec, UriInput, UserVpcConfig
from ..predictor import AsyncPredictor, LocalPredictor, Predictor, ServiceType
from ..serializers import SerializerBase
from ..session import Session, get_default_session

if typing.TYPE_CHECKING:
    from ..estimator import AlgorithmEstimator
    from ._model_recipe import ModelRecipe, ModelRecipeType, ModelTrainingRecipe

logger = get_logger(__name__)

# Reserved ports for internal use, do not use them for service
_RESERVED_PORTS = [8080, 9090]

# Default model upstream source
MODEL_TASK_CREATED_BY_QUICKSTART = "QuickStart"


class DefaultServiceConfig(object):
    """Default configuration used in creating prediction service."""

    # Listen Port
    listen_port = 8000

    # Default model path in container
    model_path = "/eas/workspace/model/"

    # Default user code path in container
    code_path = "/ml/usercode/"


class StorageConfigBase(metaclass=ABCMeta):
    """Base Storage Configuration."""

    @abstractmethod
    def to_dict(self):
        pass


class RawStorageConfig(StorageConfigBase):
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def to_dict(self):
        return self.config


class OssStorageConfig(StorageConfigBase):
    """Configuration for OSS Storage."""

    def __init__(
        self, mount_path: str, oss_path: str, oss_endpoint: Optional[str] = None
    ) -> None:
        """
        Args:
            mount_path (str): The target path where the OSS storage will be mounted.
            oss_path (str): The source OSS path, must start with `oss://`. e.g. `oss://bucket-name/path/to/data`.
            oss_endpoint (Optional[str]): The endpoint address of the OSS bucket, if not provided,
                the internal endpoint for the bucket will be used.
        """
        self.mount_path = mount_path
        self.oss_path = oss_path
        self.oss_endpoint = oss_endpoint

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "mount_path": self.mount_path,
            "oss": {"path": self.oss_path},
        }

        if self.oss_endpoint:
            d["oss"]["endpoint"] = self.oss_endpoint
        return d


class NfsStorageConfig(StorageConfigBase):
    """Configuration for NFS Storage."""

    def __init__(
        self,
        mount_path: str,
        nfs_server: str,
        nfs_path: str = "/",
        read_only: bool = False,
    ) -> None:
        """
        Args:
            mount_path (str): The target path where the NFS storage will be mounted.
            nfs_server (str): The NFS server address. e.g. `xxx.cn-shanghai.nas.aliyuncs.com'
            nfs_path (str): The source path in the NFS storage, default to '/'.
            read_only (bool): Indicates if the NFS storage should be mounted as read-only, default to False.
        """
        self.mount_path = mount_path
        self.nfs_path = nfs_path
        self.read_only = read_only
        self.nfs_server = nfs_server

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mount_path": self.mount_path,
            "nfs": {
                "path": self.nfs_path,
                "readOnly": self.read_only,
                "server": self.nfs_server,
            },
        }


class NodeStorageConfig(StorageConfigBase):
    """Use to mount the local node disk storage to the container."""

    def __init__(self, mount_path) -> None:
        """
        Args:
            mount_path (str): The target path where the node disk storage will be mounted.
        """
        self.mount_path = mount_path

    def to_dict(self) -> Dict[str, Any]:
        return {
            "empty_dir": {},
            "mount_path": self.mount_path,
        }


class SharedMemoryConfig(StorageConfigBase):
    """Use to configure the shared memory for the container."""

    def __init__(self, size_limit: int) -> None:
        """
        Args:
            size_limit (int): Size limit of the shared memory, in GB.
        """
        self.size_limit = size_limit

    def to_dict(self) -> Dict[str, Any]:
        return {
            "empty_dir": {
                "medium": "memory",
                "size_limit": self.size_limit,
            },
            "mount_path": "/dev/shm",
        }


class ResourceConfig(object):
    """A class that represents the resource used by a PAI prediction service
    instance."""

    def __init__(self, cpu: int, memory: int, gpu: int = None, gpu_memory: int = None):
        """ResourceConfig initializer.

        The public resource group does not support requesting GPU resources with
        `ResourceConfig`. Use the 'gpu' and 'gpu_memory' parameter only for services
        deployed to dedicated resource groups that provide GPU machine instances.

        Args:
            cpu (int): The number of CPUs that each instance requires.
            memory (int): The amount of memory that each instance requires,
                must be an integer, Unit: MB.
            gpu (int): The number of GPUs that each instance requires.
            gpu_memory (int): The amount of GPU memory that each instance requires.
                The value must be an integer, Unit: GB.

                PAI allows memory resources of a GPU to be allocated to multiple instances.
                If you want multiple instances to share the memory resources of a GPU,
                set the gpu parameter to 0. If you set the ``gpu`` parameter to 1, each
                instance occupies a GPU and the gpu_memory parameter does not take effect.

                .. note::

                    **Important** PAI does not enable the strict isolation of GPU memory.
                    To prevent out of memory (OOM) errors, make sure that the GPU memory
                    used by each instance does not exceed the requested amount.
        """
        self.cpu = cpu
        self.memory = memory
        self.gpu = gpu
        self.gpu_memory = gpu_memory

    def __repr__(self):
        return (
            f"ResourceConfig(cpu={self.cpu}, memory={self.memory}MB, gpu={self.gpu or 0},"
            f" gpu_memory={self.gpu_memory or 0}GB)"
        )

    def __str__(self):
        return self.__repr__()

    def to_dict(self):
        """Transform the ResourceConfig instance to a dictionary.

        Returns:
            dict:

        """
        res = {
            "cpu": self.cpu,
            "gpu": self.gpu,
            "gpu_memory": self.gpu_memory,
            "memory": self.memory,
        }

        return {k: v for k, v in res.items() if v is not None}


class InferenceSpec(object):
    """A class used to describe how to create a prediction service.

    InferenceSpec is using to describe how the model is serving in PAI. To view the
    full supported parameters, please see the following hyperlink:
    `Parameters of model services <https://help.aliyun.com/document_detail/450525.htm>`_.

    Example of how to config a InferneceSpec::

        >>> # build an inference_spec that using XGBoost processor.
        >>> infer_spec = InferenceSpec(processor="xgboost")
        >>> infer_spec.metadata.rpc.keepalive  = 1000
        >>> infer_spec.warm_up_data_path = "oss://bucket-name/path/to/warmup-data"
        >>> infer_spec.add_option("metadata.rpc.max_batch_size", 8)
        >>> print(infer_spec.processor)
        xgboost
        >>> print(infer_spec.metadata.rpc.keepalive)
        1000
        >>> print(infer_spec.metadata.rpc.max_batch_size)
        8
        >>> print(infer_spec.to_dict())
        {'processor': 'xgboost', 'metadata': {'rpc': {'keepalive': 1000, 'max_batch_size': 8}},
        'warm_up_data_path': 'oss://bucket-name/path/to/warmup-data'}

    """

    def __init__(self, *args, **kwargs):
        """InferenceSpec initializer.

        Args:
            **kwargs: Parameters of the inference spec.
        """

        properties = kwargs.pop("__properties", [])
        cfg_dict = copy.deepcopy(kwargs)
        cfg_dict = {k: v for k, v in cfg_dict.items() if not k.startswith("_")}
        if args:
            if len(args) > 1:
                raise TypeError()
            cfg_dict.update(args[0])

        super(InferenceSpec, self).__setattr__(
            "_cfg_dict", self._transform_value(cfg_dict)
        )
        super(InferenceSpec, self).__setattr__("__properties", properties)

    def __repr__(self):
        return json.dumps(self.to_dict(), sort_keys=True, indent=4)

    def _transform_value(self, value):
        if isinstance(value, (List, Tuple)):
            return [self._transform_value(item) for item in value]
        elif isinstance(value, (Dict, AttrDict)):
            return AttrDict(
                {key: self._transform_value(value) for key, value in value.items()}
            )
        return value

    def __missing__(self, name):
        return self._cfg_dict.__missing__(name)

    def __setitem__(self, name, value):
        return self._cfg_dict.__setitem__(name, self._transform_value(value))

    def __setattr__(self, name, value):
        if name in getattr(self, "__properties"):
            super(InferenceSpec, self).__setattr__(name, self._transform_value(value))
        else:
            self._cfg_dict.__setattr__(name, self._transform_value(value))

    def __getattr__(self, item):
        if item.startswith("_"):
            return getattr(self, item)
        return self._cfg_dict.__getitem__(item)

    def __contains__(self, item):
        return item in self._cfg_dict

    def to_dict(self) -> Dict:
        """Return a dictionary that represent the InferenceSpec."""
        return self._cfg_dict.to_dict()

    def add_option(self, name: str, value):
        """Add an option to the inference_spec instance.

        Args:
            name (str): Name of the option to set, represented as the JSON path of the
                parameter for the InferenceSpec. To view the full supported parameters,
                please see the following hyperlink: `Parameters of model services
                <https://help.aliyun.com/document_detail/450525.htm>`_.
            value: Value for the option.

        Examples:

            >>> infer_spec = InferenceSpec(processor="tensorflow_gpu_1.12")
            >>> infer_spec.add_option("metadata.rpc.keepalive", 10000)
            >>> infer_spec.metadata.rpc.keepalive
            10000
            >>> infer_spec.to_dict()
            {'processor': 'tensorflow_gpu_1.12', 'metadata': {'rpc': {'keepalive': 10000}}}

        """

        src = self._transform_value(value)
        for k in reversed(name.split(".")):
            src = {k: src}

        self._cfg_dict.update(AttrDict(src))

    def merge_options(self, options: Dict[str, Any]):
        """Merge options from a dictionary."""
        for key, value in options.items():
            self.add_option(key, value)

    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> "InferenceSpec":
        """Initialize a InferenceSpec from a dictionary.

        You can use this method to initialize a InferenceSpec instance
        from a dictionary.

        Returns:
            :class:`pai.model.InferenceSpec`: A InferenceSpec instance.

        """
        config = config or dict()

        return cls(**config)

    def is_container_serving(self):
        return "containers" in self._cfg_dict

    @classmethod
    def _upload_source_dir(cls, source_dir, session):
        """Upload source files to OSS bucket."""

        if not os.path.exists(source_dir):
            raise ValueError(f"Input source code path does not exist: {source_dir}.")
        if not os.path.isdir(source_dir):
            raise ValueError(
                f"Input source code path should be a directory: {source_dir}."
            )

        target_dir = session.get_storage_path_by_category(
            category=StoragePathCategory.InferenceSrc
        )
        # upload local script data to the OSS bucket.
        uploaded_source_code = upload(
            source_dir,
            target_dir,
            session.oss_bucket,
        )

        logger.debug("Uploaded source code to OSS: %s", uploaded_source_code)
        return uploaded_source_code

    def mount(
        self,
        source: str,
        mount_path: str,
        session: Session = None,
        properties: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Mount a source storage to the running container.

        .. note::

            If source is a local path, it will be uploaded to the OSS bucket and
            mounted. If source is a OSS path, it will be mounted directly.

        Args:
            source (str): The source storage to be attached, currently only support OSS
                path in OSS URI format and local path.
            mount_path (str): The mount path in the container.
            session (Session, optional): A PAI session instance used for communicating
                with PAI service.

        Returns:
            Dict[str, Any]: The storage config.

        Raises:
            DuplicateMountException: If the mount path is already used or source OSS
                path is mounted to the container.

        Examples::
            # Mount a OSS storage path to the running container.
            >>> inference_spec.mount("oss://<YourOssBucket>/path/to/directory/model.json",
            ...  "/ml/model/")

            # 'Mount' a local path to the running container.
            >>> inference_spec.mount("/path/to/your/data/", "/ml/model/")

        """
        session = session or get_default_session()

        # TODO: supports more storages, such as NAS, PAI Dataset, PAI CodeSource, etc.
        if not isinstance(source, str):
            raise ValueError(
                "Parameter should be a string which represents an OSS storage path"
                " or a local file path."
            )

        if "storage" in self._cfg_dict:
            storages = copy.deepcopy(self._cfg_dict.get("storage", []))
        else:
            storages = []

        configs = []
        uris = set()
        for s in storages:
            # overwrite the existing mount path
            if s.get("mount_path") == mount_path:
                continue
            oss_uri = s.get("oss", {}).get("path")
            if oss_uri:
                uris.add(oss_uri)
            configs.append(s)

        if is_oss_uri(source):
            oss_uri_obj = OssUriObj(source)
            storage_config = {
                "mount_path": mount_path,
                "oss": {"path": oss_uri_obj.get_dir_uri()},
            }
        elif os.path.exists(source):
            # if source is a local path, upload it to OSS bucket and use OSS URI
            # as storage source.
            oss_path = session.get_storage_path_by_category(
                StoragePathCategory.ModelData
            )
            oss_uri = upload(
                source_path=source, oss_path=oss_path, bucket=session.oss_bucket
            )
            oss_uri_obj = OssUriObj(oss_uri)
            storage_config = {
                "mount_path": mount_path,
                "oss": {"path": oss_uri_obj.get_dir_uri()},
            }
        else:
            raise ValueError(
                "Source path is not a valid OSS URI or a existing local path."
            )

        if properties:
            storage_config.update({"properties": properties})

        # check if the source OSS Path is already mounted to the container.
        if oss_uri_obj.get_dir_uri() in uris:
            raise DuplicatedMountException(
                f"Source OSS path '{oss_uri_obj.get_dir_uri()}' is already "
                f"mounted to the container."
            )

        configs.append(storage_config)
        self.storage = configs
        return storage_config

    def set_model_data(self, model_data: str, mount_path: Optional[str] = None):
        """
        Set the model data for the InferenceSpec instance.

        Args:
            model_data (str): The model data to be set. It must be an OSS URI.
            mount_path (str, optional): The mount path in the container.

        Raises:
            DuplicatedMountException: If the model data is already mounted to the container.
        """

        def is_model_storage(storage: Dict[str, Any]):
            return (
                "properties" in storage
                and storage["properties"].get("resource_type") == "model"
            )

        if not model_data:
            return
        if not self.is_container_serving():
            # if model_data is an OSS URI with endpoint, truncate the endpoint.
            oss_uri_obj = OssUriObj(model_data)
            model_path_uri = "oss://{bucket_name}/{key}".format(
                bucket_name=oss_uri_obj.bucket_name,
                key=oss_uri_obj.object_key,
            )
            self.add_option("model_path", model_path_uri)
        else:
            indexes = [idx for idx, s in enumerate(self.storage) if is_model_storage(s)]
            # replace the first model storage with the model_data.
            if indexes:
                if len(indexes) > 1:
                    logger.warning(
                        "Multiple model storage found in the InferenceSpec,"
                        " use the first one."
                    )
                idx = indexes[0]
                oss_uri_obj = OssUriObj(model_data)

                storage_config = {
                    "path": oss_uri_obj.get_dir_uri(),
                }

                if oss_uri_obj.endpoint:
                    storage_config.update(
                        {
                            "endpoint": oss_uri_obj.endpoint,
                        }
                    )
                self.storage[idx].oss = self._transform_value(storage_config)
            else:
                try:
                    self.mount(
                        model_data,
                        mount_path=mount_path or DefaultServiceConfig.model_path,
                        properties={"resource_type": "model", "resource_use": "base"},
                    )
                except DuplicatedMountException as e:
                    # ignore duplicated mount
                    logger.warning("Model is already mounted the container: %s", e)


def container_serving_spec(
    command: str,
    image_uri: Union[str, ImageInfo],
    source_dir: Optional[str] = None,
    git_config: Optional[Dict[str, Any]] = None,
    port: Optional[int] = None,
    environment_variables: Optional[Dict[str, str]] = None,
    requirements: Optional[List[str]] = None,
    requirements_path: Optional[str] = None,
    health_check: Optional[Dict[str, Any]] = None,
    storage_configs: Optional[List[StorageConfigBase]] = None,
    session: Optional[Session] = None,
) -> InferenceSpec:
    """A convenient function to create an InferenceSpec instance that serving the model
    with given container and script.

    Examples::

        infer_spec: InferenceSpec = container_serving_spec(
            command="python run.py",
            source_dir="./model_server/",
            image_uri="<ServingImageUri>",
        )

        m = Model(
            model_data="oss://<YourOssBucket>/path/to/your/model",
            inference_spec=infer_spec,
        )
        m.deploy(
            instance_type="ecs.c6.xlarge"
        )


    Args:
        command (str): The command used to launch the Model server.
        source_dir (str): A relative path or an absolute path to the source code
            directory used to load model and launch the HTTP server, it will be
            uploaded to the OSS bucket and mounted to the container. If there is a
            ``requirements.txt`` file under the directory, it will be installed before
            the prediction server started.

            If 'git_config' is provided, 'source_dir' should be a relative location
            to a directory in the Git repo. With the following GitHub repo directory
            structure:

            .. code::

                |----- README.md
                |----- src
                            |----- train.py
                            |----- test.py

            if you need 'src' directory as the source code directory, you can assign
            source_dir='./src/'.
        git_config (Dict[str, str]): Git configuration used to clone the repo.
            Including ``repo``, ``branch``, ``commit``, ``username``, ``password`` and
            ``token``. The ``repo`` is required. All other fields are optional. ``repo``
            specifies the Git repository. If you don't provide ``branch``, the default
            value 'master' is used. If you don't provide ``commit``, the latest commit
            in the specified branch is used. ``username``, ``password`` and ``token``
            are for authentication purpose. For example, the following config:

            .. code:: python

                git_config = {
                    'repo': 'https://github.com/modelscope/modelscope.git',
                    'branch': 'master',
                    'commit': '9bfc4a9d83c4beaf8378d0a186261ffc1cd9f960'
                }

            results in cloning the repo specified in 'repo', then checking out the
            'master' branch, and checking out the specified commit.
        image_uri (str): The Docker image used to run the prediction service.
        port (int): Expose port of the server in container, the prediction request
            will be forward to the port. The environment variable ``LISTENING_PORT``
            in the container will be set to this value. Default to 8000.
        environment_variables (Dict[str, str], optional): Dictionary of environment
            variable key-value pairs to set on the running container.
        requirements (List[str], optional): A list of Python package dependency, it
            will be installed before the serving container run.
        requirements_path (str, optional): A absolute path to the requirements.txt in
            the container.
        health_check (Dict[str, Any], optional): The health check configuration. If it
            not set, A TCP readiness probe will be used to check the health of the
            HTTP server.
        storage_configs (List[StorageConfigBase], optional): A list of storage configs
            used to mount the storage to the container. The storage can be OSS, NFS,
            SharedMemory, or NodeStorage, etc.
        session (Session, optional): A PAI session instance used for communicating
            with PAI service.

    Returns:
        :class:`pai.model.InferenceSpec`: An InferenceSpec instance.
    """
    session = session or get_default_session()
    if git_config:
        updated_args = git_utils.git_clone_repo(
            git_config=git_config,
            source_dir=source_dir,
        )
        source_dir = updated_args["source_dir"]

    if not port:
        port = DefaultServiceConfig.listen_port
    elif int(port) in _RESERVED_PORTS:
        raise ValueError(
            "Reserved port {} is not allowed to use as serving port.".format(port),
        )

    if source_dir:
        if not os.path.exists(source_dir):
            raise ValueError("Source directory {} does not exist.".format(source_dir))

        if not os.path.isdir(source_dir):
            raise ValueError(
                "Source directory {} is not a directory.".format(source_dir)
            )

        code_mount_path = DefaultServiceConfig.code_path
        # build the command for serving container.
        command = textwrap.dedent(
            f"""\
        # change working directory to code mount path.
        cd {code_mount_path}
        {command}
        """
        )

        if not requirements_path and os.path.exists(
            os.path.join(source_dir, "requirements.txt")
        ):
            requirements_path = posixpath.join(code_mount_path, "requirements.txt")
    else:
        code_mount_path = None
        requirements_path = None

    if isinstance(image_uri, ImageInfo):
        image_uri = image_uri.image_uri

    environment_variables = environment_variables or dict()
    container_spec = {
        "image": image_uri,
        "port": port,
        "script": command,
        "env": (
            [
                {"name": key, "value": str(value)}
                for key, value in environment_variables.items()
            ]
            if environment_variables
            else []
        ),
    }

    if health_check:
        container_spec["health_check"] = health_check

    if requirements:
        container_spec["prepare"] = {"pythonRequirements": requirements}
        if requirements_path:
            logger.warning(
                "If the parameter 'requirements' is set, the requirements_path "
                "parameter will be ignored."
            )
    elif requirements_path:
        container_spec["prepare"] = {
            "pythonRequirementsPath": requirements_path,
        }
    inference_spec = InferenceSpec(containers=[container_spec])

    if storage_configs:
        storage = [s.to_dict() for s in storage_configs]
        inference_spec.storage = storage

    # mount the uploaded serving scripts to the serving container.
    if source_dir:
        inference_spec.mount(
            source_dir,
            code_mount_path,
            session=session,
        )
    return inference_spec


class _BuiltinProcessor(object):
    """Helper class uses for getting the builtin processor"""

    PMML = "pmml"
    XGBoost = "xgboost"

    SupportedFrameworkAcceleratorVersionConfig = {
        "tensorflow": {
            "cpu": [
                "1.12",
                "1.14",
                "1.15",
                "2.3",
            ],
            "gpu": [
                "1.12",
                "1.14",
                "1.15",
            ],
        },
        "pytorch": {
            "cpu": [
                "1.6",
            ],
            "gpu": [
                "1.6",
            ],
        },
    }

    # Hard code default processor for specific model format.
    ModelFormatDefaultProcessorMapping = {
        ModelFormat.PMML: "pmml",
        ModelFormat.SavedModel: "tensorflow_cpu_2.3",
        ModelFormat.TorchScript: "pytorch_cpu_1.6",
        ModelFormat.FrozenPb: "pytorch_cpu_1.6",
        ModelFormat.CaffePrototxt: "caffe_cpu",
        ModelFormat.ONNX: "onnx_cu100",
    }

    @classmethod
    def get_default_by_model_format(cls, model_format: str) -> str:
        """Get the default processor for a specific model format."""
        if model_format in cls.ModelFormatDefaultProcessorMapping:
            return cls.ModelFormatDefaultProcessorMapping[model_format]

    @classmethod
    def from_framework_version(
        cls, framework_name, framework_version, accelerator=None
    ):
        accelerator = accelerator or "cpu"
        versions = cls.SupportedFrameworkAcceleratorVersionConfig.get(
            framework_name, dict()
        ).get(accelerator, [])
        if framework_version in versions:
            return "{}_{}_{}".format(framework_name, accelerator, framework_version)
        else:
            logger.warning(
                "Could not find the processor for the framework_version({} {}), use the"
                " latest processor".format(framework_name, framework_version)
            )
            return "{}_{}_{}".format(framework_name, accelerator, versions[-1])


class ModelBase(object):
    """A class represent ModelBase."""

    def __init__(
        self,
        model_data: str,
        inference_spec: Optional[InferenceSpec] = None,
        session: Session = None,
    ):
        self.model_data = model_data
        self.inference_spec = inference_spec
        self.session = session or get_default_session()

    def download(self, target_dir: str):
        """Download the model data from OSS to local directory.

        Args:
            target_dir (str): The target directory to download the model data.

        Returns:
            str: Local directory path stores the model data.

        """
        if not self.model_data:
            raise ValueError("Could not find the model data for this model.")
        if not is_oss_uri(self.model_data):
            raise RuntimeError("Download method only support model data stored in OSS.")
        self._download_model_data(target_dir)

        return target_dir

    def _download_model_data(self, target_dir):
        if not self.model_data:
            return
        logger.info(f"Prepare model data to local directory: {target_dir}")
        if self.model_data.startswith("oss://"):
            oss_uri = OssUriObj(self.model_data)
            oss_bucket = self.session.get_oss_bucket(oss_uri.bucket_name)
            download(
                oss_path=oss_uri.object_key,
                local_path=target_dir,
                bucket=oss_bucket,
                un_tar=True,
            )
        else:
            if not os.path.exists(self.model_data):
                raise ValueError(f"Model data path does not exist: {self.model_data}")

            os.makedirs(target_dir, exist_ok=True)
            if os.path.isfile(self.model_data):
                shutil.copy(
                    self.model_data,
                    os.path.join(target_dir, os.path.basename(self.model_data)),
                )
            else:
                distutils.dir_util.copy_tree(self.model_data, target_dir)

    def _upload_model_data(self):
        """Upload the model artifact to OSS bucket if self.model_data is a local
        file path.

        """
        if not self.model_data:
            return
        elif is_oss_uri(self.model_data):
            return self.model_data
        elif not os.path.exists(self.model_data):
            raise RuntimeError(f"Model data path does not exist: {self.model_data}")

        dest_oss_path = self.session.get_storage_path_by_category(
            category=StoragePathCategory.ModelData
        )
        upload_model_data = upload(
            source_path=self.model_data,
            oss_path=dest_oss_path,
            bucket=self.session.oss_bucket,
        )
        return upload_model_data

    def list_model_files(self, uri_format: bool = False) -> Iterator[str]:
        """List model files under the model path.

        Args:
            uri_format (bool): If True, return the model file path in OSS URI format.

        Returns:
            Iterator[str]: Iterator of model files.
        """
        if not self.model_data:
            raise ValueError("Model data path is not specified.")

        if not is_oss_uri(self.model_data):
            raise ValueError("Method only support model data stored in OSS.")

        oss_uri_obj = OssUriObj(self.model_data)
        bucket = self.session.get_oss_bucket(
            bucket_name=oss_uri_obj.bucket_name,
        )

        def _get_relative_path(obj_key: str):
            # if the model_data is reference an object, return the object file
            # name.
            if oss_uri_obj.object_key == obj_key:
                return os.path.basename(obj_key)

            path = obj_key[len(oss_uri_obj.object_key) :]
            return path.lstrip("/") if path.startswith("/") else path

        obj_iter = ObjectIterator(bucket=bucket, prefix=oss_uri_obj.object_key)
        for obj_info in obj_iter:
            if uri_format:
                yield f"oss://{bucket.bucket_name}/{obj_info.key}"
            else:
                yield _get_relative_path(obj_info.key)

    def _get_inference_spec(self):
        return self.inference_spec

    def deploy(
        self,
        service_name: str,
        instance_count: Optional[int] = 1,
        instance_type: Optional[str] = None,
        resource_config: Optional[Union[Dict[str, int], ResourceConfig]] = None,
        resource_id: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        service_type: Optional[str] = None,
        wait: bool = True,
        serializer: Optional["SerializerBase"] = None,
        **kwargs,
    ):
        """Deploy a prediction service with the model."""
        if is_local_run_instance_type(instance_type):
            return self._deploy_local(
                instance_type=instance_type,
                serializer=serializer,
                wait=wait,
            )
        else:
            return self._deploy(
                service_name=service_name,
                instance_count=instance_count,
                instance_type=instance_type,
                resource_config=resource_config,
                resource_id=resource_id,
                service_type=service_type,
                options=options,
                wait=wait,
                serializer=serializer,
                **kwargs,
            )

    def _generate_service_name(self):
        s = os.path.basename(self.model_data.rstrip("/")) + random_str(8)
        return to_plain_text(s)

    def _deploy(
        self,
        service_name: str = None,
        instance_count: int = 1,
        instance_type: str = None,
        resource_config: Union[Dict[str, int], ResourceConfig] = None,
        resource_id: str = None,
        service_type: str = None,
        options: Dict[str, Any] = None,
        wait: bool = True,
        serializer: "SerializerBase" = None,
        labels: Optional[Dict[str, str]] = None,
        **kwargs,
    ):
        """Create a prediction service."""
        if not service_name:
            service_name = self._generate_service_name()
            logger.info(
                "Service name is not specified, using a generated service"
                f" name to create the service: service_name={service_name}"
            )

        config = self._build_service_config(
            service_name=service_name,
            instance_count=instance_count,
            instance_type=instance_type,
            service_type=service_type,
            resource_config=resource_config,
            resource_id=resource_id,
            options=options,
        )
        service_name = self.session.service_api.create(config=config, labels=labels)
        self._wait_service_visible(service_name)
        if service_type == ServiceType.Async:
            predictor = AsyncPredictor(
                service_name=service_name,
                session=self.session,
                serializer=serializer,
            )
        else:
            predictor = Predictor(
                service_name=service_name,
                session=self.session,
                serializer=serializer,
            )
        print(
            "View the service detail by accessing the console URI: \n{}".format(
                predictor.console_uri
            )
        )
        if wait:
            predictor.wait_for_ready()

        return predictor

    def _wait_service_visible(self, service_name, attempts=3, interval=2):
        """Wait for the service to be visible in DescribeService API.

        hack:
        https://aone.alibaba-inc.com/v2/project/1134421/bug#viewIdentifier=5dfb195e2e2b84f6b2f24718&openWorkitemIdentifier=50192431

        """
        while attempts > 0:
            obj = self.session.service_api.get(service_name)
            if "ServiceUid" in obj:
                return
            attempts -= 1
            time.sleep(interval)
        logger.warning("DescribeService API failed to get the Service object.")

    def _build_service_config(
        self,
        service_name: str = None,
        instance_count: int = None,
        instance_type: str = None,
        resource_config: Union[ResourceConfig, Dict[str, Any]] = None,
        resource_id: str = None,
        service_type: str = None,
        options: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Build a service config dictionary used to create a PAI EAS service."""
        self.model_data = self._upload_model_data()

        resource_config = (
            ResourceConfig(**resource_config)
            if resource_config and isinstance(resource_config, dict)
            else None
        )

        if resource_config and instance_type:
            raise ValueError(
                f"Only one of 'instance_type' and 'resource_config' "
                f"is required, but both have been provided: instance_type"
                f"={instance_type}, resource_config="
                f"{resource_config}."
            )

        inference_spec = InferenceSpec(
            self._get_inference_spec().to_dict() if self.inference_spec else dict()
        )
        inference_spec.set_model_data(model_data=self.model_data)
        if service_type:
            inference_spec.add_option("metadata.type", service_type)
            if inference_spec.is_container_serving():
                inference_spec.add_option("metadata.rpc.proxy_path", "/")

        if service_name:
            inference_spec.add_option("name", service_name)

        if instance_count:
            inference_spec.add_option("metadata.instance", instance_count)

        if instance_type:
            inference_spec.add_option("cloud.computing.instance_type", instance_type)
        elif resource_config:
            inference_spec.add_option("metadata.cpu", resource_config.cpu)
            inference_spec.add_option("metadata.memory", resource_config.memory)
            if resource_config.gpu:
                inference_spec.add_option("metadata.gpu", resource_config.gpu)
            if resource_config.gpu_memory:
                inference_spec.add_option(
                    "metadata.gpu_memory", resource_config.gpu_memory
                )
                if resource_config.gpu:
                    logger.warning(
                        "Parameters 'gpu' is set, the 'gpu_memory' parameter "
                        "does not take effect."
                    )

        if resource_id:
            inference_spec.add_option("metadata.resource", resource_id)

        if options:
            inference_spec.merge_options(options=options)

        return inference_spec.to_dict()

    def _deploy_local(
        self,
        instance_type: str,
        serializer: SerializerBase = None,
        wait: bool = True,
    ) -> LocalPredictor:
        """Deploy the model in local using docker."""

        if not self.inference_spec.is_container_serving():
            raise RuntimeError(
                "Currently, only model using the InferenceSpec that serving with"
                " container support local run."
            )

        if len(self.inference_spec.containers) > 1:
            raise RuntimeError(
                "InferenceSpec that serving with multiple container "
                "does not support local run."
            )

        # prepare model data to local
        work_dir = tempfile.mkdtemp()
        model_dir = os.path.join(work_dir, "model")

        self._download_model_data(target_dir=model_dir)
        volumes = {
            model_dir: {
                "bind": DefaultServiceConfig.model_path,
                "mode": "rw",
            }
        }

        # prepare used storage to local directory.
        if "storage" in self.inference_spec:
            # only OSS storage config support local run.
            if any(s for s in self.inference_spec.storage if "oss" not in s):
                raise ValueError(
                    f"Local run only support InferenceSpec using OSS storage config: "
                    f"{self.inference_spec.to_dict()}"
                )
            for idx, storage in enumerate(self.inference_spec.storage):
                store_dir = os.path.join(work_dir, f"storage_{idx}")
                os.makedirs(store_dir, exist_ok=True)
                oss_uri = OssUriObj(storage.oss.path)
                download(
                    oss_path=oss_uri.object_key,
                    local_path=store_dir,
                    bucket=self.session.get_oss_bucket(oss_uri.bucket_name),
                )
                volumes[store_dir] = {"bind": storage.mount_path, "mode": "rw"}

        container_spec = self.inference_spec.containers[0].to_dict()
        env_vars = {
            item["name"]: item["value"] for item in container_spec.get("env", [])
        }

        # build local launch script
        requirements_list = container_spec.get("prepare", dict()).get(
            "pythonRequirements", []
        )
        requirements_path = container_spec.get("prepare", dict()).get(
            "pythonRequirementsPath", None
        )

        # build command to install requirements
        if requirements_list:
            install_requirements = " ".join(
                [
                    shlex.quote(s)
                    for s in ["python", "-m", "pip", "install"] + requirements_list
                ]
            )
        elif requirements_path:
            install_requirements = " ".join(
                [
                    shlex.quote(s)
                    for s in ["python", "-m", "pip", "install", "-r", requirements_path]
                ]
            )
        else:
            install_requirements = ""

        user_scripts = container_spec.get("script", "")
        launch_script = textwrap.dedent(
            f"""\
            set -e
            {install_requirements}
            {user_scripts}
            """
        )

        gpu_count = -1 if instance_type == INSTANCE_TYPE_LOCAL_GPU else None
        container_run = run_container(
            image_uri=container_spec["image"],
            port=container_spec.get("port"),
            environment_variables=env_vars,
            entry_point=[
                "/bin/sh",
                "-c",
                launch_script,
            ],
            volumes=volumes,
            gpu_count=gpu_count,
        )
        predictor = LocalPredictor(
            container_id=container_run.container.id,
            port=container_run.port,
            serializer=serializer,
        )

        if wait:
            predictor.wait_for_ready()

        return predictor

    @classmethod
    def _wait_local_server_ready(
        cls,
        container_run: ContainerRun,
        interval: int = 5,
    ):
        """Wait for the local model server to be ready."""
        while True:
            try:
                # Check whether the container is still running.
                if not container_run.is_running():
                    raise RuntimeError(
                        "Container exited unexpectedly, status: {}".format(
                            container_run.status
                        )
                    )

                # Make a HEAD request to the server.
                requests.head(
                    f"http://127.0.0.1:{container_run.port}/",
                )
                break
            except requests.ConnectionError:
                # ConnectionError means server is not ready.
                logger.debug("Waiting for the container to be ready...")
                time.sleep(interval)
                continue

    def register(
        self,
        model_name: str,
        version: str = None,
        accessibility: Optional[str] = None,
        version_labels: Optional[Dict[str, str]] = None,
        version_description: Optional[str] = None,
        format_type: Optional[str] = None,
        framework_type: Optional[str] = None,
        training_spec: Optional[Dict[str, Any]] = None,
        evaluation_spec: Optional[Dict[str, Any]] = None,
        approval_status: Optional[str] = None,
        metrics: Optional[Dict[str, Any]] = None,
        options: Optional[str] = None,
        model_labels: Optional[Dict[str, str]] = None,
        model_description: Optional[str] = None,
        model_doc: Optional[str] = None,
        origin: Optional[str] = None,
        domain: Optional[str] = None,
        task: Optional[str] = None,
    ) -> "RegisteredModel":
        """Register a model to the PAI model registry.

        Use ``self.model_data`` to register a model to the PAI model registry.

        Args:
            model_name (str): The name of the model. If the model name already exists in
                workspace, the model will be updated with a new model version,
                parameters like ``model_labels``, ``model_description``, ``model_doc``,
                ``origin``, ``domain``, ``task``, ``accessibility`` will be ignored. If
                the model name does not exist, a new model will be created.
            version (str, optional): The version of the model. If not specified, a new
                version will be created. If the version already exists, registration
                will fail.
            accessibility (str, optional): The accessibility of the model. The value
                can be "PUBLIC" or "PRIVATE". Default to "PRIVATE".
            version_labels (dict, optional): The labels of the model version.
            version_description (str, optional): The description of the model version.
            format_type (str, optional): The format type of the model version. The value
                can be "OfflineModel", "SavedModel", "Keras H5", "Frozen Pb",
                "Caffe Prototxt", "TorchScript", "XGBoost", "PMML", "AlinkModel",
                "ONNX". Default to None.
            framework_type (str, optional): The framework type of the model version. The
                value can be "PyTorch", "TensorFlow", "Keras", "Caffe", "Alink",
                "Xflow", "XGBoost". Default to None.
            training_spec (dict, optional): The training spec of the model version.
                Usually, it is got from the training job. Default to None.
            evaluation_spec (dict, optional): The evaluation spec of the model version.
                Usually, it is got from the processing job for evaluation. Default to None.
            approval_status (str, optional): The approval status of the model version.
                The value can be "APPROVED", "PENDING". Default to None.
            metrics (dict, optional): The metrics of the model version.
            options (str, optional): Any other options that you want to pass to the
                model registry. Default to None.
            model_labels (dict, optional): The labels of the model.
            model_description (str, optional): The description of the model.
            model_doc (str, optional): The documentation uri of the model.
            origin (str, optional): The origin of the model. For example, "huggingface",
                "modelscope" etc. Default to None.
            domain (str, optional): The domain that the model is used for. For example,
                "aigc", "audio", "nlp", "cv" etc. Default to None.
            task (str, optional): The task that the model is used for. For example,
                "large-language-model", "text-classification", "image-classification",
                "sequence-labeling" etc. Default to None.

        Returns:
            :class:`pai.model.RegisteredModel`: The registered model object.
        """

        if not self.model_data:
            raise ValueError(
                "Register model failed, ``model_data`` is required to register a model."
            )

        # Ensure model data is uploaded to OSS.
        self.model_data = self._upload_model_data()

        # By specifying model_name with double quotes, the list api will process the
        # precise search. Otherwise, the list api will process the fuzzy search.
        resp = self.session.model_api.list(
            model_name=f'"{model_name}"',
        )
        if resp.total_count == 0:
            model_id = self.session.model_api.create(
                model_name=model_name,
                labels=model_labels,
                model_description=model_description,
                model_doc=model_doc,
                origin=origin,
                domain=domain,
                task=task,
                accessibility=accessibility,
            )
        else:
            model_id = resp.items[0]["ModelId"]

        # TODO support to registry model with evaluation spec
        version_name = self.session.model_api.create_version(
            model_id=model_id,
            uri=self.model_data,
            version_name=version,
            labels=version_labels,
            version_description=version_description,
            format_type=format_type,
            framework_type=framework_type,
            training_spec=training_spec,
            evaluation_spec=evaluation_spec,
            inference_spec=(
                self.inference_spec.to_dict() if self.inference_spec else None
            ),
            approval_status=approval_status,
            metrics=metrics,
            options=options,
        )
        return RegisteredModel(model_name=model_name, model_version=version_name)


class Model(ModelBase):
    """The Class representing a ready-to-deploy model.

    A Model instance includes the model artifact path and information on how to create
    prediction service in PAI (specified by the inference_spec). By calling the
    `model.deploy` method, a prediction service is created in PAI and a
    :class:`pai.predictor.Predictor` instance is returned that can be used to make
    prediction to the service.

    Example::

        from pai.model import Model
        from pai.model import InferenceSpec

        m: Model = Model(
            inference_spec=InferenceSpec(processor="xgboost"),
            model_data="oss://bucket-name/path/to/model",
        )

        # register model to PAI ModelRegistry
        registered_model = m.register(
            model_name="example_xgb_model"
            version="1.0.0",
        )

        # Deploy to model to create a prediction service.
        p: Predictor = m.deploy(
            service_name="xgb_model_service",
            instance_count=2,
            instance_type="ecs.c6.large",
            options={
                "metadata.rpc.batching": true,
                "metadata.rpc.keepalive": 10000
            }
        )

        # make a prediction by send the data to the prediction service.
        result = p.predict([[2,3,4], [54.12, 2.9, 45.8]])

    """

    def __init__(
        self,
        model_data: str = None,
        inference_spec: InferenceSpec = None,
        session: Session = None,
    ):
        """Model initializer.

        Args:
            model_data (str): An OSS URI or file path specifies the location of the
                model. If model_data is a local file path, it will be uploaded to OSS
                bucket before deployment or model registry.
            inference_spec (:class:`pai.model.InferenceSpec`, optional): An
                `InferenceSpec` object representing how to create the prediction service
                using the model.
            session (:class:`pai.session.Session`, optional): A pai session object
                manages interactions with PAI REST API.
        """
        super(Model, self).__init__(
            model_data,
            inference_spec,
            session=session or get_default_session(),
        )

    def deploy(
        self,
        service_name: str,
        instance_count: Optional[int] = 1,
        instance_type: Optional[str] = None,
        resource_config: Optional[Union[Dict[str, int], ResourceConfig]] = None,
        resource_id: Optional[str] = None,
        service_type: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        wait: bool = True,
        serializer: Optional["SerializerBase"] = None,
        **kwargs,
    ):
        """Deploy an online prediction service.

        Args:
            service_name (str, optional): Name for the online prediction service. The
                name must be unique in a region.
            instance_count (int): Number of instance request for the service deploy
                (Default 1).
            instance_type (str, optional): Type of the machine instance, for example,
                'ecs.c6.large'. For all supported instance, view the appendix of the
                link:
                https://help.aliyun.com/document_detail/144261.htm?#section-mci-qh9-4j7
            resource_config (Union[ResourceConfig, Dict[str, int]], optional):
                Request resource for each instance of the service. Required if
                instance_type is not set.  Example config:

                .. code::

                    resource_config = {
                        "cpu": 2,       # The number of CPUs that each instance requires
                        "memory: 4000,  # The amount of memory that each instance
                                        # requires, must be an integer, Unit: MB.
                        # "gpu": 1,         # The number of GPUs that each instance
                                            # requires.
                        # "gpu_memory": 3   # The amount of GPU memory that each
                                            # instance requires, must be an integer,
                                            # Unit: GB.
                    }

            resource_id (str, optional): The ID of the resource group. The service
                can be deployed to ``public resource group`` and
                ``dedicated resource group``.

                * If `resource_id` is not specified, the service is deployed
                    to public resource group.
                * If the service deployed in a dedicated resource group, provide
                    the parameter as the ID of the resource group. Example:
                    "eas-r-6dbzve8ip0xnzte5rp".
            service_type (str, optional): The type of the service.
            options (Dict[str, Any], optional): Advanced deploy parameters used
                to create the online prediction service.
            wait (bool): Whether the call should wait until the online prediction
                service is ready (Default True).
            serializer (:class:`pai.predictor.serializers.BaseSerializer`, optional): A
                serializer object used to serialize the prediction request and
                deserialize the prediction response.
        Returns:
            A ``PredictorBase`` instance used for making prediction to the prediction
            service.
        """
        return super(Model, self).deploy(
            service_name=service_name,
            instance_count=instance_count,
            instance_type=instance_type,
            resource_config=resource_config,
            resource_id=resource_id,
            options=options,
            wait=wait,
            serializer=serializer,
            service_type=service_type,
            **kwargs,
        )


class RegisteredModel(ModelBase):
    """A class that represents a registered model in PAI model registry.

    A RegisteredModel instance has a unique tuple of (model_name, model_version,
    model_provider), and can be used for downstream tasks such as creating an online
    prediction service, or creating an AlgorithmEstimator to start a training job.

    Examples::

        from pai.model import RegisteredModel

        # retrieve a registered model from PAI model registry by
        # specifying the model_name, model_version and model_provider
        m = RegisteredModel(
            model_name="easynlp_pai_bert_small_zh",
            model_version="0.1.0",
            model_provider="pai",
        )


        # deploy the Registered Model to create an online prediction
        # service if the model has inference_spec
        m.deploy()


        # create an AlgorithmEstimator to start a training job if the
        # model has training_spec
        est = m.get_estimator()
        inputs = m.get_estimator_inputs()
        est.fit(inputs)

    """

    def __init__(
        self,
        model_name: str,
        model_version: Optional[str] = None,
        model_provider: Optional[str] = None,
        session: Optional[Session] = None,
        **kwargs,
    ):
        """Get a RegisteredModel instance from PAI model registry.

        Args:
            model_name (str): The name of the registered model.
            model_version (str, optional): The version of the registered model. If not
                provided, the latest version is retrieved from the model registry.
            model_provider (str, optional): The provider of the registered model.
                Currently, only "pai", "huggingface" or None are supported.
            session (:class:`pai.session.Session`, optional): A PAI session object used
                for interacting with PAI Service.
        """
        self.session = session or get_default_session()
        model_info = kwargs.pop("model_info", None)
        if model_info:
            self._model_version_info = kwargs.pop("model_version_info", {})
            self._model_info = model_info
        else:
            self._model_info, self._model_version_info = self._get_model_version_obj(
                model_name=model_name,
                model_version=model_version,
                model_provider=model_provider,
            )

        self.model_id = self._model_info.get("ModelId")
        self.model_name = self._model_info.get("ModelName")
        self.model_provider = self._model_info.get("Provider")
        self.task = self._model_info.get("Task")
        self.domain = self._model_info.get("Domain")
        self.framework_type = self._model_version_info.get("FrameworkType")
        self.source_type = self._model_version_info.get("SourceType")
        self.source_id = self._model_version_info.get("SourceId")
        self.format_type = self._model_version_info.get("FormatType")
        self.uri = self._model_version_info.get("Uri")
        self.model_version = self._model_version_info.get("VersionName")
        self.training_spec = self._model_version_info.get("TrainingSpec")
        self.evaluation_spec = self._model_version_info.get("EvaluationSpec")
        self.compression_spec = self._model_version_info.get("CompressionSpec")
        self.model_labels = {
            lb["Key"]: lb["Value"] for lb in self._model_info.get("Labels", [])
        }
        self.version_labels = {
            lb["Key"]: lb["Value"] for lb in self._model_version_info.get("Labels", [])
        }
        super(RegisteredModel, self).__init__(
            model_data=self.uri,
            inference_spec=InferenceSpec.from_dict(
                self._model_version_info.get("InferenceSpec", dict())
            ),
        )

    def __eq__(self, other: "RegisteredModel") -> bool:
        """Compare two RegisteredModel instances."""
        return (
            isinstance(other, RegisteredModel)
            and self.model_id == other.model_id
            and self.model_version == other.model_version
        )

    def __repr__(self):
        if not self.model_provider:
            return generate_repr(
                self,
                "model_name",
                "model_version",
            )
        else:
            return generate_repr(self, "model_name", "model_version", "model_provider")

    @classmethod
    def list(
        cls,
        model_name: Optional[str] = None,
        model_provider: Optional[str] = None,
        task: Optional[str] = None,
        session: Optional[Session] = None,
    ) -> Iterator["RegisteredModel"]:
        """List registered models in model registry.

        Args:
            model_name (str, optional): The name of the registered model. Default to
                None.
            model_provider (str, optional): The provider of the registered model.
                Optional values are "pai", "huggingface" or None. If None, list
                registered models in the workspace of the current session. Default to
                None.
            task (str, optional): The task of the registered model. Default to None.
            session (Session, optional): A PAI session object used for interacting with
                PAI Service.
        Returns:
            Iterator[RegisteredModel]: An iterator of RegisteredModel instances matching
                the given criteria.
        """
        session = session or get_default_session()
        page_size = 50
        page_number = 1

        while True:
            result = session.model_api.list(
                model_name=model_name,
                provider=model_provider,
                task=task,
                page_size=page_size,
                page_number=page_number,
            ).items
            if not result:
                break

            for item in result:
                model_version_info = item.pop("LatestVersion", {})
                model_info = item
                yield cls(
                    model_name=item["ModelName"],
                    session=session,
                    model_info=model_info,
                    model_version_info=model_version_info,
                )
            page_number += 1

    def list_versions(
        self, model_version: Optional[str] = None
    ) -> Iterator["RegisteredModel"]:
        """List all versions of the registered model.

        Args:
            model_version (str, optional): The version of the registered model. Default
                to None.
        """
        page_size = 50
        page_number = 1

        while True:
            items = self.session.model_api.list_versions(
                model_id=self.model_id,
                page_number=page_number,
                page_size=page_size,
                version_name=model_version,
            ).items
            if not items:
                break
            for item in items:
                yield RegisteredModel(
                    model_name=self.model_name,
                    session=self.session,
                    model_info=self._model_info,
                    model_version_info=item,
                )
            page_number += 1

    def _generate_service_name(self) -> str:
        """Generate a service name for the online prediction service."""
        base_name = self.model_name.lower().replace("-", "_")[:36]
        if base_name.endswith("_"):
            base_name = base_name[:-1]
        gen_name = f"{base_name}_{random_str(8)}"
        return to_plain_text(gen_name)

    def _get_inference_spec(self) -> InferenceSpec:
        """Get the inference_spec of the registered model."""
        return self.inference_spec

    def _get_model_version_obj(
        self,
        model_name: str,
        model_version: Optional[str] = None,
        model_provider: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Get the model info from PAI model registry.

        Args:
            model_name (str): The name of the registered model.
            model_version (str, optional): The version of the registered model. If not
                provided, the latest version is retrieved from the model registry.
            model_provider (str, optional): The provider of the registered model.
                Currently, only "pai" or None are supported. Set it to "pai" to retrieve
                a PAI official model.

        Returns:
            A tuple of model object and model version object.
        """
        if not model_name:
            raise ValueError(
                "Parameter model_name cannot be None or empty. Please provide a valid"
                " model_name."
            )

        # Use model_name to get the model_id
        # By specifying model_name with double quotes, the list api will process the
        # precise search. Otherwise, the list api will process the fuzzy search.
        result = self.session.model_api.list(
            model_name=f'"{model_name}"', provider=model_provider
        )
        if result.total_count == 0:
            raise RuntimeError(
                f"Could not find any Registered Model with the specific"
                f" name='{model_name}' and provider='{model_provider}'. Please check"
                f" the arguments."
            )
        model_obj = result.items[0]
        model_id = model_obj["ModelId"]

        if model_version:
            model_version_obj = self.session.model_api.get_version(
                model_id=model_id, version=model_version
            )
            return model_obj, model_version_obj
        else:
            # Get the latest model version of the specific model if model_version
            # is not provided.
            if "LatestVersion" not in model_obj:
                raise RuntimeError(
                    f"Could not find any model version under the specific"
                    f" name='{model_name}' and provider='{model_provider}'. Please"
                    f" check the arguments."
                )
            return model_obj, model_obj["LatestVersion"]

    def delete(self, delete_all_version: bool = False):
        """Delete the specific registered model from PAI model registry.

        Args:
            delete_all_version (bool): Whether to delete all versions of the registered
                model.
        """
        if delete_all_version:
            self.session.model_api.delete(self.model_id)
        else:
            if not self.model_version:
                logger.warning(
                    "No model version is specified for the registered model, "
                    "skipping deletion."
                )
                return
            self.session.model_api.delete_version(self.model_id, self.model_version)

    def deploy(
        self,
        service_name: Optional[str] = None,
        instance_count: Optional[int] = None,
        instance_type: Optional[str] = None,
        resource_config: Optional[Union[Dict[str, int], ResourceConfig]] = None,
        resource_id: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        service_type: Optional[str] = None,
        wait: bool = True,
        serializer: Optional["SerializerBase"] = None,
        **kwargs,
    ):
        """Deploy an online prediction service with the registered model.

        If the RegisteredModel already has a registered inference_spec, then the model
        can be deployed directly. Give more specific arguments to override the registered
        inference_spec. Otherwise, the model will be deployed through the same process
        as the :meth:`deploy` method of :class:`pai.model.Model`.

        Args:
            service_name (str, optional): Name for the online prediction service. The
                name must be unique in a region.
            instance_count (int, optional): Number of instance requested for the service
                deploy.
            instance_type (str, optional): Type of the machine instance, for example,
                'ecs.c6.large'. For all supported instance, view the appendix of the
                link:
                https://help.aliyun.com/document_detail/144261.htm?#section-mci-qh9-4j7
            resource_config (Union[ResourceConfig, Dict[str, int]], optional):
                Request resource for each instance of the service. Required if
                instance_type is not set.  Example config:

                .. code::

                    resource_config = {
                        "cpu": 2,       # The number of CPUs that each instance requires
                        "memory: 4000,  # The amount of memory that each instance
                                        # requires, must be an integer, Unit: MB.
                        # "gpu": 1,         # The number of GPUs that each instance
                                            # requires.
                        # "gpu_memory": 3   # The amount of GPU memory that each
                                            # instance requires, must be an integer,
                                            # Unit: GB.
                    }

            resource_id (str, optional): The ID of the resource group. The service
                can be deployed to ``public resource group`` and
                ``dedicated resource group``.

                * If `resource_id` is not specified, the service is deployed
                    to public resource group.
                * If the service deployed in a dedicated resource group, provide
                    the parameter as the ID of the resource group. Example:
                    "eas-r-6dbzve8ip0xnzte5rp".
            service_type (str, optional): The type of the service.
            options (Dict[str, Any], optional): Advanced deploy parameters used
                to create the online prediction service.
            wait (bool): Whether the call should wait until the online prediction
                service is ready (Default True).
            serializer (:class:`pai.predictor.serializers.BaseSerializer`, optional): A
                serializer object used to serialize the prediction request and
                deserialize the prediction response.
        Returns:
            A ``PredictorBase`` instance used for making prediction to the prediction
            service.
        """
        if not self._model_version_info:
            raise ValueError("No model version is available for deployment.")

        if not self.inference_spec:
            raise RuntimeError("No inference_spec for the registered model.")

        labels = kwargs.pop("labels", dict())
        if self.model_provider == ProviderAlibabaPAI:
            default_labels = {
                "Task": self.task,
                "RootModelName": self.model_name,
                "RootModelVersion": self.model_version,
                "RootModelID": self.model_id,
                "Domain": self.domain,
                "CreatedBy": MODEL_TASK_CREATED_BY_QUICKSTART,
                "BaseModelUri": self.uri,
            }
            default_labels.update(labels)
            labels = default_labels

        if is_local_run_instance_type(instance_type):
            return self._deploy_local(
                instance_type=instance_type,
                serializer=serializer,
                wait=wait,
            )
        else:
            return self._deploy(
                service_name=service_name,
                instance_count=instance_count,
                instance_type=instance_type,
                resource_config=resource_config,
                resource_id=resource_id,
                service_type=service_type,
                options=options,
                wait=wait,
                serializer=serializer,
                labels=labels,
                **kwargs,
            )

    def _build_service_config(
        self,
        service_name: str = None,
        instance_count: int = None,
        instance_type: str = None,
        resource_config: Union[ResourceConfig, Dict[str, Any]] = None,
        resource_id: str = None,
        service_type: str = None,
        options: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Build a service config dictionary with RegisteredModel's inference_spec.

        When the RegisteredModel builds a service config, it will ignore the model_data
        parameter and use the inference_spec of the RegisteredModel as default config.
        User can override the inference_spec by providing more specific arguments.
        """

        resource_config = (
            ResourceConfig(**resource_config)
            if resource_config and isinstance(resource_config, dict)
            else None
        )

        if resource_config and instance_type:
            raise ValueError(
                f"Only one of 'instance_type' and 'resource_config' is required, but"
                f" both have been provided: instance_type={instance_type},"
                f" resource_config={resource_config}."
            )

        inference_spec = InferenceSpec(
            self._get_inference_spec().to_dict() if self.inference_spec else dict()
        )

        if service_type:
            inference_spec.add_option("metadata.type", service_type)
            if inference_spec.is_container_serving():
                inference_spec.add_option("metadata.rpc.proxy_path", "/")

        if service_name:
            inference_spec.add_option("name", service_name)

        if instance_count:
            inference_spec.add_option("metadata.instance", instance_count)

        if instance_type:
            inference_spec.add_option("cloud.computing.instance_type", instance_type)
        elif resource_config:
            inference_spec.add_option("metadata.cpu", resource_config.cpu)
            inference_spec.add_option("metadata.memory", resource_config.memory)
            if resource_config.gpu:
                inference_spec.add_option("metadata.gpu", resource_config.gpu)
            if resource_config.gpu_memory:
                inference_spec.add_option(
                    "metadata.gpu_memory", resource_config.gpu_memory
                )
                if resource_config.gpu:
                    logger.warning(
                        "Parameters 'gpu' is set, the 'gpu_memory' parameter does not"
                        " take effect."
                    )

        if resource_id:
            inference_spec.add_option("metadata.resource", resource_id)

        if options:
            inference_spec.merge_options(options=options)

        return inference_spec.to_dict()

    def get_recipe_spec(
        self, recipe_type: "ModelRecipeType", method: Optional[str] = None
    ) -> ModelRecipeSpec:
        from ._model_recipe import ModelRecipeType

        if recipe_type == ModelRecipeType.TRAINING:
            raw_spec = self.training_spec
        elif recipe_type == ModelRecipeType.EVALUATION:
            raw_spec = self.evaluation_spec
        elif recipe_type == ModelRecipeType.COMPRESSION:
            raw_spec = self.compression_spec
        else:
            raise ValueError(
                f"Invalid recipe_type: {recipe_type}. Supported recipe types are:"
                f" {ModelRecipeType.supported_types()}"
            )

        if type(self)._is_multiple_spec(raw_spec):
            supported_methods = list(raw_spec.keys())
            if method and method not in supported_methods:
                raise ValueError(
                    "The model recipe does not support the given method:"
                    f" {method}. Supported methods are: {supported_methods}."
                )
            elif method:
                spec = raw_spec.get(method)
            else:
                method = supported_methods[0]
                logger.warning(
                    f"Model recipe contains multiple specs and method is not specified. "
                    f"Default method is used: '{method}'. Supported training methods are:"
                    f" {supported_methods}."
                )
                spec = raw_spec.get(method)
        else:
            if method:
                raise ValueError(
                    "The model recipe contains only one spec, do not specify the method."
                )
            spec = raw_spec
        return ModelRecipeSpec.model_validate(spec)

    def get_training_spec(self, training_method: Optional[str]) -> ModelRecipeSpec:
        from ._model_recipe import ModelRecipeType

        return self.get_recipe_spec(ModelRecipeType.TRAINING, training_method)

    def get_estimator(
        self,
        training_method: Optional[str] = None,
        instance_type: Optional[str] = None,
        instance_count: Optional[int] = None,
        hyperparameters: Optional[Dict[str, Any]] = None,
        base_job_name: Optional[str] = None,
        output_path: Optional[str] = None,
        max_run_time: Optional[int] = None,
        **kwargs,
    ) -> "AlgorithmEstimator":
        """Generate an AlgorithmEstimator.

        Generate an AlgorithmEstimator object from RegisteredModel's training_spec.

        Args:
            training_method (str, optional): Used to select the training algorithm
                that supported by the model. If not specified, the default training
                algorithm will be retrieved from the model version.
            instance_type (str, optional): The machine instance type used to run the
                training job. If not provider, the default instance type will be
                retrieved from the algorithm definition. To view the supported machine
                instance types, please refer to the document:
                https://help.aliyun.com/document_detail/171758.htm#section-55y-4tq-84y.
            instance_count (int, optional): The number of machines used to run the
                training job. If not provider, the default instance count will be
                retrieved from the algorithm definition.
            hyperparameters (dict, optional): A dictionary that represents the
                hyperparameters used in the training job. Default hyperparameters will
                be retrieved from the algorithm definition.
            base_job_name (str, optional): The base name used to generate the training
                job name. If not provided, a default job name will be generated.
            output_path (str, optional): An OSS URI to store the outputs of the training
                jobs. If not provided, an OSS URI will be generated using the default
                OSS bucket in the session. When the `estimator.fit` method is called,
                a specific OSS URI under the output_path for each channel is generated
                and mounted to the training container.
            max_run_time (int, optional): The maximum time in seconds that the training
                job can run. The training job will be terminated after the time is
                reached (Default None).
        Returns:
            :class:`pai.estimator.AlgorithmEstimator`: An AlgorithmEstimator object.
        """
        from ..estimator import AlgorithmEstimator

        warnings.warn(
            "`.get_estimator` is deprecated and will be removed in a future version, you can now use "
            "`.training_recipe` instead.",
            category=FutureWarning,
        )

        if not self.training_spec:
            raise ValueError(
                "The provided registered model does not contain training spec."
            )
        ts = self.get_training_spec(training_method=training_method)
        hyperparameters = hyperparameters or {}
        # TODO: validate the given hyperparameters via algorithm definition
        for hp in ts.hyperparameters:
            if hp.name not in hyperparameters:
                hyperparameters.update(
                    {
                        hp.name: hp.value,
                    }
                )

        if not base_job_name:
            base_job_name = f"{self.model_name}_training" if self.model_name else None

        if not max_run_time:
            max_run_time = (
                ts.scheduler.max_running_time_in_seconds if ts.scheduler else None
            )

        resource_id = kwargs.get("resource_id")
        instance_spec = kwargs.get("instance_spec")
        compute_resource = ts.compute_resource
        if resource_id:
            if instance_type:
                logger.warning(
                    "The instance type is ignored when resource_id is provided."
                )
            instance_spec = instance_type or compute_resource.instance_spec
            if not instance_spec:
                raise ValueError(
                    "Instance spec is required when resource_id is provided."
                )
            instance_spec = InstanceSpec.model_validate(instance_spec)
            instance_count = (
                instance_count
                or compute_resource.instance_count
                or compute_resource.ecs_count
                or 1
            )
        else:
            if instance_spec:
                logger.warning(
                    "The instance spec is ignored when resource_id is not provided."
                )
            instance_type = instance_type or compute_resource.ecs_spec
            instance_count = (
                instance_count
                or compute_resource.ecs_count
                or compute_resource.instance_count
                or 1
            )

        labels = kwargs.pop("labels", dict())
        if self.model_provider == ProviderAlibabaPAI:
            default_labels = {
                "BaseModelUri": self.uri,
                "CreatedBy": MODEL_TASK_CREATED_BY_QUICKSTART,
                "Domain": self.domain,
                "RootModelID": self.model_id,
                "RootModelName": self.model_name,
                "RootModelVersion": self.model_version,
                "Task": self.task,
            }
            default_labels.update(labels)
            labels = default_labels

        return AlgorithmEstimator(
            algorithm_name=ts.algorithm_name,
            algorithm_version=ts.algorithm_version,
            algorithm_provider=ts.algorithm_provider,
            algorithm_spec=ts.algorithm_spec,
            hyperparameters=hyperparameters,
            base_job_name=base_job_name,
            max_run_time=max_run_time,
            instance_type=instance_type,
            instance_count=instance_count,
            instance_spec=instance_spec,
            output_path=output_path,
            labels=labels,
            **kwargs,
        )

    def get_estimator_inputs(self, training_method=None) -> Dict[str, Any]:
        """Get the AlgorithmEstimator's default input channels

        Get the AlgorithmEstimator's default input channels from RegisteredModel's
        training_spec.

        Returns:
            Dict[str, str]: A dict of input channels.
        """

        warnings.warn(
            "`.get_estimator_inputs` is deprecated and will be removed in a future version, you can now use "
            "`.training_recipe().default_inputs` instead.",
            category=FutureWarning,
        )

        default_inputs = (
            self.get_training_spec(training_method=training_method).inputs or []
        )

        ret = {}
        for item in default_inputs:
            if isinstance(item, UriInput):
                ret[item.name] = item.input_uri
            else:
                ret[item.name] = item
        return ret

    def get_eval_processor(
        self,
        base_job_name: Optional[str] = None,
        output_path: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        max_run_time: Optional[int] = None,
        instance_type: Optional[str] = None,
        instance_count: Optional[int] = None,
        user_vpc_config: Optional[UserVpcConfig] = None,
    ):
        """Generate a Processor for model evaluation.

        Generate a Processor object from RegisteredModel's evaluation_spec.

        Args:
            parameters (dict, optional): A dictionary that represents the
                parameters used in the job. Default parameters will
                be retrieved from the evaluation spec.
            base_job_name (str, optional): The base name used to generate the
                job name. If not provided, a default job name will be generated.
            output_path (str, optional): An OSS URI to store the outputs of the
                jobs. If not provided, an OSS URI will be generated using the default
                OSS bucket in the session. When the `estimator.fit` method is called,
                a specific OSS URI under the output_path for each channel is generated
                and mounted to the container.
            max_run_time (int, optional): The maximum time in seconds that the
                job can run. The job will be terminated after the time is
                reached (Default None).
            instance_type (str, optional): The machine instance type used to run the
                job. If not provider, the default instance type will be
                retrieved from the evaluation spec. To view the supported machine
                instance types, please refer to the document:
                https://help.aliyun.com/document_detail/171758.htm#section-55y-4tq-84y.
            instance_count (int, optional): The number of machines used to run the
                job. If not provider, the default instance count will be
                retrieved from the evaluation spec.
            user_vpc_config (:class:`pai.estimator.UserVpcConfig`, optional): The VPC
                configuration used to enable the job instance to connect to the
                specified user VPC. If provided, an Elastic Network Interface (ENI) will
                be created and attached to the job instance, allowing the
                instance to access the resources within the specified VPC. Default to
                None.
        Returns:
            :class:`pai.processor.Processor`: An Processor object.
        """
        from ..processor import Processor

        warnings.warn(
            "`.get_eval_processor` is deprecated and will be removed in a future version, you can now use "
            "`.model_recipe` instead.",
            category=FutureWarning,
        )

        eval_spec = self._get_evaluation_spec()
        if not eval_spec:
            raise ValueError(
                "The provided registered model does not contain evaluation spec."
            )
        eval_spec = ModelRecipeSpec.model_validate(eval_spec)
        if not eval_spec.algorithm_spec:
            raise ValueError(
                "Invalid evaluation spec, the evaluation spec does not contain any"
                " configuration for the evaluation job."
            )
        # workload = eval_spec.get("AlgorithmSpec")

        if not base_job_name:
            base_job_name = f"{self.model_name}_eval" if self.model_name else None

        parameters = parameters or dict()

        for item in eval_spec.hyperparameters:
            if item.name not in parameters:
                parameters[item.name] = item.value
        if not max_run_time:
            max_run_time = eval_spec.scheduler.max_running_time_in_seconds

        compute_resource = eval_spec.compute_resource
        if compute_resource and (not instance_type or not instance_count):
            # If instance_type or instance_count is not provided, use the default
            instance_type = instance_type or compute_resource.ecs_spec
            instance_count = instance_count or compute_resource.ecs_count

        source_dir = None
        code_dir = eval_spec.algorithm_spec.code_dir

        if code_dir and code_dir.location_type == "oss":
            oss_uri_obj = OssUriObj.from_bucket_key_endpoint(
                bucket_name=code_dir.location_value.bucket,
                object_key=code_dir.location_value.key,
                endpoint=code_dir.location_value.endpoint,
            )
            source_dir = oss_uri_obj.uri
        processor = Processor(
            image_uri=eval_spec.algorithm_spec.image,
            command=eval_spec.algorithm_spec.command,
            source_dir=source_dir,
            parameters=parameters,
            max_run_time=max_run_time,
            base_job_name=base_job_name,
            output_path=output_path,
            instance_type=instance_type,
            instance_count=instance_count,
            user_vpc_config=user_vpc_config,
            session=self.session,
        )
        processor.set_input_channels(eval_spec.algorithm_spec.input_channels)
        processor.set_output_channels(eval_spec.algorithm_spec.output_channels)

        return processor

    def get_evaluation_inputs(self) -> Dict[str, Any]:
        """Get the Processor's default input channels

         Get the Processor's default input channels from RegisteredModel's
         evaluation_spec.

        Returns:
            dict[str, str]: A dict of input channels.
        """
        warnings.warn(
            "`.get_eval_inputs` is deprecated and will be removed in a future version, you can now use "
            "`.model_recipe().default_inputs` instead.",
            category=FutureWarning,
        )

        if not self.evaluation_spec:
            raise ValueError(
                "The provided registered model does not contain evaluation spec."
            )
        eval_spec = ModelRecipeSpec.model_validate(self.evaluation_spec)
        inputs = eval_spec.inputs or []
        res = {}

        for item in inputs:
            res[item.name] = item.input_uri if isinstance(item, UriInput) else item
        return res

    @classmethod
    def _is_multiple_spec(cls, spec: Dict[str, Any]) -> bool:
        return not ("AlgorithmSpec" in spec or "AlgorithmName" in spec)

    def _get_evaluation_spec(self):
        """Get the evaluation_spec of the registered model."""
        return self.evaluation_spec

    def training_recipe(self, method: Optional[str] = None) -> "ModelTrainingRecipe":
        """Get the training recipe of the registered model.

        Args:
            method (str, optional): The training method used to select the
                specific training recipe.

        Returns:
            :class:`pai.model.ModelTrainingRecipe`: A ModelTrainingRecipe object.

        """
        from ._model_recipe import ModelTrainingRecipe

        return ModelTrainingRecipe(
            model_name=self.model_name,
            model_version=self.model_version,
            model_provider=self.model_provider,
            method=method,
        )

    def model_recipe(
        self, recipe_type: "ModelRecipeType", method: Optional[str] = None
    ) -> "ModelRecipe":
        """Initialize a ModelRecipe object from the recipe spec of the registered model.

        Args:
            recipe_type (ModelRecipeType): The recipe type used to select the specific model recipe.
                supported recipe types are: "training", "evaluation", "compression".
            method (str, optional): The method used to select the specific model recipe.

        Returns:
            :class:`pai.model.ModelRecipe`: A ModelRecipe object.

        """
        from ._model_recipe import ModelRecipe

        return ModelRecipe(
            model_name=self.model_name,
            model_version=self.model_version,
            model_provider=self.model_provider,
            recipe_type=recipe_type,
            method=method,
        )
