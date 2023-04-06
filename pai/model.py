import copy
import distutils.dir_util
import json
import logging
import os.path
import posixpath
import shlex
import shutil
import tempfile
import textwrap
import time
from typing import Any, Dict, List, Optional, Tuple, Union

from addict import Dict as AttrDict

from .common.consts import ModelFormat
from .common.docker_utils import run_container
from .common.oss_utils import OssUriObj, download, is_oss_uri, upload
from .common.utils import makedirs, random_str, to_plain_text
from .predictor import LocalPredictor, Predictor
from .serializers import SerializerBase
from .session import Session, config_default_session

DEFAULT_SERVICE_PORT = 8000


logger = logging.getLogger(__name__)

DEFAULT_MODEL_PATH = "/eas/workspace/model/"


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
            f"<ResourceConfig:cpu={self.cpu} memory={self.memory}MB gpu={self.gpu or 0}"
            f" gpu_memory={self.gpu_memory or 0}GB>"
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

    @classmethod
    def from_serving_container(
        cls,
        image_uri: str,
        environment_variables: Dict[str, str] = None,
        port: int = DEFAULT_SERVICE_PORT,
        command: Union[str, List[str]] = None,
        requirements: Optional[List[str]] = None,
        requirements_path: Optional[str] = None,
    ) -> "InferenceSpec":
        """Build a InferenceSpec object that serving the model with the given docker
        image.

        Args:
            image_uri (str): Docker image URI used to run the prediction service.
            port (int): Exposed port of the server in container. the prediction request
                will be forward to the port. The environment variable ``LISTEN_PORT``
                in the container will be set to this value.
            environment_variables (Dict[str, str]): Environment variables to be set to
                the running container.
            requirements (List[str], optional): A list of Python package dependency, it
                will be installed before the serving container run.
            requirements_path (str, optional): The path of the requirements.txt in the
                running container.
            command (Union[str, List[str]]): The command to be invoked when the
                container is started.

        Returns:
            :class:`pai.model.InferenceSpec`: A InferenceSpec instance.

        """

        if isinstance(command, (list, tuple)):
            command = " ".join([shlex.quote(s) for s in command])
        container_spec = {
            "image": image_uri,
            "port": port,
            "script": command,
            "env": [
                {"name": key, "value": str(value)}
                for key, value in environment_variables.items()
            ]
            if environment_variables
            else [],
        }

        if requirements or requirements_path:
            prepare = dict()
            if requirements:
                prepare["pythonRequirements"] = requirements
            if requirements_path:
                prepare["pythonRequirementsPath"] = requirements_path
            container_spec["prepare"] = prepare
        d = {
            "containers": [container_spec],
        }
        return cls(**d)

    def is_container_serving(self):
        return "containers" in self._cfg_dict

    @classmethod
    @config_default_session
    def from_serving_script(
        cls,
        entry_point: str,
        image_uri: str,
        port: int = DEFAULT_SERVICE_PORT,
        source_dir: Optional[str] = None,
        environment_variables: Optional[Dict[str, str]] = None,
        requirements: Optional[List[str]] = None,
        session: Optional[Session] = None,
    ) -> "InferenceSpec":
        """A convenient method to create a InferenceSpec instance that serving the model
        with given scripts.

        Examples::

            spec = InferenceSpec.from_serving_script(
                entry_point="run.py",
                source_dir="./model_server/",
                image_uri="<YourImageUri>",
            )

            m = Model(
                model_data="oss://<YourOssBucket>/path/to/your/model",
                inference_spec=spec,
            )
            m.deploy(
                instance_type="ecs.c6.xlarge"
            )


        Args:
            entry_point (str): The entry point file used to launch the model server,
                which can be a `.py` or `.sh` file.
            source_dir (str, optional): Local path to the source code directory to be
                uploaded and used for the model server.
            image_uri (str): The Docker image used to run the prediction service.
            port (int): Expose port of the server in container, the prediction request
                will be forward to the port. The environment variable ``LISTEN_PORT``
                in the container will be set to this value.
            environment_variables (Dict[str, str], optional): Dictionary of environment
                variable key-value pairs to set on the running container.
            requirements (List[str], optional): A list of Python package dependency, it
                will be installed before the serving container run.
            session (Session, optional): A PAI session instance used for communicating
                with PAI service.

        Returns:
            :class:`pai.model.InferenceSpec`: An InferenceSpec instance.
        """
        # upload local script data to the OSS bucket.
        code_mount_path = "/ml/usercode/"
        if entry_point.endswith(".py"):
            launch_command = f"python {entry_point}"
        elif entry_point.endswith(".sh"):
            launch_command = f"sh {entry_point}"
        else:
            launch_command = f"./{entry_point}"

        # build the command for serving container.
        command = textwrap.dedent(
            f"""\
        set -e
        mkdir -p {code_mount_path} && cd {code_mount_path}
        {launch_command}
        """
        )

        script_data = cls._upload_source_dir(
            entry_point, source_dir=source_dir, session=session
        )
        if source_dir and os.path.exists(os.path.join(source_dir, "requirements.txt")):
            requirements_path = posixpath.join(code_mount_path, "requirements.txt")
        else:
            requirements_path = None

        environment_variables = environment_variables or dict()
        inference_spec = cls.from_serving_container(
            image_uri=image_uri,
            port=port,
            environment_variables=environment_variables,
            command=command,
            requirements=requirements,
            requirements_path=requirements_path,
        )

        # mount the uploaded serving scripts to the serving container.
        script_mount_config = {
            "mount_path": code_mount_path,
            "oss": {
                "path": script_data,
            },
        }

        if len(inference_spec.storage) > 1:
            inference_spec.storage.append(script_mount_config)
        else:
            inference_spec.storage = [script_mount_config]

        return inference_spec

    @classmethod
    def _upload_source_dir(cls, entry_point, source_dir, session):
        """Upload source files to OSS bucket."""
        if not source_dir:
            # if source code directory is not provided, upload the entry_point file.
            if not os.path.exists(entry_point):
                raise ValueError(f"Entry point file does not exist: {entry_point}.")
            upload_source_file = entry_point
        else:
            if not os.path.exists(source_dir):
                raise ValueError(
                    f"Input source code path does not exist: {source_dir}."
                )
            if not os.path.isdir(source_dir):
                raise ValueError(
                    f"Input source code path should be a directory: {source_dir}."
                )

            if not os.path.exists(os.path.join(source_dir, entry_point)):
                raise ValueError(
                    f"Entry point file does not exist: "
                    f"{os.path.join(source_dir, entry_point)}."
                )
            upload_source_file = source_dir

        target_dir = session.get_storage_path_by_category(category="inference_src")
        # upload local script data to the OSS bucket.
        upload(
            upload_source_file,
            target_dir,
            session.oss_bucket,
        )
        return os.path.join(f"oss://{session.oss_bucket.bucket_name}", target_dir)

    @config_default_session
    def mount(
        self, source: str, mount_path: str, session: Session = None
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

        Examples::
            # Mount a OSS storage path to the running container.
            >>> inference_spec.mount("oss://<YourOssBucket>/path/to/directory/model.json",
            ...  "/ml/model/")

            # 'Mount' a local path to the running container.
            >>> inference_spec.mount("/path/to/your/data/", "/ml/model/")

        """

        # TODO: supports more storages, such as NAS, PAI Dataset, PAI CodeSource, etc.
        if not isinstance(source, str):
            raise ValueError(
                "Parameter source only support a OSS path in OSS URI format."
            )

        # Get current storage configs.
        if "storage" in self._cfg_dict:
            configs = self._cfg_dict.get("storage", [])
        else:
            configs = []

        # check if mount path is already used.
        for conf in configs:
            if conf.get("mount_path") == mount_path:
                raise ValueError(
                    f"Mount path {mount_path} is already used by other storage."
                )

        # build new storage config.
        if is_oss_uri(source):
            oss_uri_obj = OssUriObj(source)
            storage_config = {
                "mount_path": mount_path,
                "oss": {"path": oss_uri_obj.get_dir_uri()},
            }
        elif os.path.exists(source):
            # if source is a local path, upload it to OSS bucket and use OSS URI
            # as storage source.
            oss_path = session.get_storage_path_by_category("model_data")
            oss_uri = upload(
                source_path=source, oss_path=oss_path, oss_bucket=session.oss_bucket
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

        configs.append(storage_config)
        self.storage = configs
        return storage_config


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

    @config_default_session
    def __init__(
        self,
        model_data: str,
        inference_spec: InferenceSpec,
        session: Session = None,
    ):

        if not model_data and "model_data" in inference_spec:
            model_data = inference_spec.model_data
        self.model_data = model_data
        self.inference_spec = inference_spec
        self.session = session

    def _download_model_data(self, target_dir):
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

            makedirs(target_dir)
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

        dest_oss_path = self.session.get_storage_path_by_category(category="model_data")
        upload_model_data = upload(
            source_path=self.model_data,
            oss_path=dest_oss_path,
            oss_bucket=self.session.oss_bucket,
        )
        return upload_model_data

    def _get_inference_spec(self):
        return self.inference_spec

    def deploy(
        self,
        service_name: Optional[str] = None,
        instance_count: Optional[int] = 1,
        instance_type: Optional[str] = None,
        resource_config: Optional[Union[Dict[str, int], ResourceConfig]] = None,
        resource_id: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        wait: bool = True,
        serializer: Optional["SerializerBase"] = None,
    ):
        """Deploy a prediction service with the model."""
        if instance_type == "local":
            return self._deploy_local(serializer=serializer, wait=wait)
        else:
            return self._deploy(
                service_name=service_name,
                instance_count=instance_count,
                instance_type=instance_type,
                resource_config=resource_config,
                resource_id=resource_id,
                options=options,
                wait=wait,
                serializer=serializer,
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
        options: Dict[str, Any] = None,
        wait: bool = True,
        serializer: "SerializerBase" = None,
    ):
        """Create a prediction service."""
        if not service_name:
            service_name = self._generate_service_name()
            logger.info(
                "Service name is not specified, using a generated service"
                f" name to create the service: service_name={service_name}"
            )

        self.model_data = self._upload_model_data()

        config = self._build_service_config(
            service_name=service_name,
            instance_count=instance_count,
            instance_type=instance_type,
            resource_config=resource_config,
            resource_id=resource_id,
            options=options,
        )

        self._service_name = self.session.service_api.create(config=config)
        predictor = Predictor(
            service_name=service_name, session=self.session, serializer=serializer
        )
        print(
            "View the service detail by accessing the console URI: \n{}".format(
                predictor.console_uri
            )
        )
        if wait:
            predictor.wait_for_ready()
            time.sleep(5)

        return predictor

    def _build_service_config(
        self,
        service_name: str = None,
        instance_count: int = None,
        instance_type: str = None,
        resource_config: Union[ResourceConfig, Dict[str, Any]] = None,
        resource_id: str = None,
        options: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Build a service config dictionary used to create a PAI EAS service."""

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

        if self.model_data:
            # if model_data is an OSS URI string with endpoint, truncate the endpoint.
            if not inference_spec.is_container_serving():
                oss_uri_obj = OssUriObj(self.model_data)
                model_path_uri = "oss://{bucket_name}/{key}".format(
                    bucket_name=oss_uri_obj.bucket_name,
                    key=oss_uri_obj.object_key,
                )
                inference_spec.add_option("model_path", model_path_uri)
            else:
                inference_spec.mount(
                    self.model_data,
                    mount_path=DEFAULT_MODEL_PATH,
                )

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
                "bind": "/eas/workspace/model/",
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

            # download data from OSS bucket and mount to local.
            # Example OSS storage config:
            # "storage": [
            #     {
            #         "mount_path": "/data_oss",
            #         "oss": {
            #             "endpoint": "oss-cn-shanghai-internal.aliyuncs.com",
            #             "path": "oss://bucket/path/"
            #         }
            #     }
            # ]
            for idx, storage in enumerate(self.inference_spec.storage):
                store_dir = os.path.join(work_dir, f"storage_{idx}")
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
        container_run = run_container(
            image_uri=container_spec["image"],
            port=container_spec.get("port"),
            environment_variables=env_vars,
            command=container_spec.get("command"),
            volumes=volumes,
        )

        if wait:
            container_run.wait_for_ready()
            # ensure the server is ready.
            # TODO(liangquan): Check if the server is ready by using the health
            #  check probe (or readiness probe?)
            time.sleep(5)
        return LocalPredictor(
            container_id=container_run.container.id,
            port=container_run.port,
            serializer=serializer,
        )


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
            name="example_xgb_model"
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

    @config_default_session
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
            session=session,
        )

    def deploy(
        self,
        service_name: Optional[str] = None,
        instance_count: Optional[int] = 1,
        instance_type: Optional[str] = None,
        resource_config: Optional[Union[Dict[str, int], ResourceConfig]] = None,
        resource_id: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        wait: bool = True,
        serializer: Optional["SerializerBase"] = None,
    ):
        """Deploy an online prediction service.

        Args:
            service_name (str, optional): Name for the online prediction service. The name
                must be unique in a region.
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

            options (Dict[str, Any], optional): Advanced deploy parameters used
                to create the online prediction service.
            wait (bool): Whether the call should wait until the online prediction
                service is ready (Default True).
            serializer (:class:`pai.predictor.serializers.BaseSerializer`, optional): A
                serializer object used to serialize the prediction request and
                deserialize the prediction response.
        Returns:
            :class:`pai.predictor.Predictor` : A PAI ``Predictor`` instance used for
                making prediction to the prediction service.
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
        )
