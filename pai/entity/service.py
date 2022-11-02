import base64
import json
import logging
import time
import urllib.request
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import six
from six.moves.urllib import parse

from pai.common.consts import FrameworkTypes, ModelFormat
from pai.common.oss_utils import parse_oss_url
from pai.common.utils import print_msg
from pai.decorator import config_default_session
from pai.entity.base import EntityBaseMixin
from pai.predictor import Predictor
from pai.schema.service_schema import ServiceConfigSchema, ServiceSchema

NETWORK_TYPE_TYPE_INTERNET = "INTERNET"
NETWORK_TYPE_TYPE_INTRANET = "INTRANET"


class CustomProcessor(object):
    def __init__(
        self,
        processor_type: str,
        processor_path: str,
        processor_entry: str = None,
        processor_main_class: str = None,
    ) -> None:
        self.processor_type = processor_type
        self.processor_path = processor_path
        self.processor_entry = processor_entry
        self.processor_main_class = processor_main_class

    def to_api_object(self):
        d = {
            "processor_type": self.processor_type,
            "processor_path": self.processor_path,
        }
        if self.processor_main_class:
            d.update(
                {
                    "processor_mainclass": self.processor_main_class,
                }
            )
        elif self.processor_entry:
            d.update(
                {
                    "processor_entry": self.processor_entry,
                }
            )
        return d

    @classmethod
    def from_api_object(cls, data: Dict[str, Any]) -> "CustomProcessor":
        return cls(
            processor_type=data.get("processor_type"),
            processor_path=data.get("processor_path"),
            processor_entry=data.get("processor_entry"),
            processor_main_class=data.get("processor_mainclass"),
        )


class ContainerSpec(object):
    def __init__(self, command: str, image: str, port: str) -> None:
        self.command = command
        self.image = image
        self.port = port

    def to_api_object(self) -> Dict[str, Union[int, str]]:
        d = {"command": self.command, "image": self.image, "port": self.port}
        return d

    @classmethod
    def from_api_object(cls, data: Dict[str, Union[int, str]]) -> "ContainerSpec":
        return cls(**data)


class ContainerProcessor(object):
    """Represent A Container Processor"""

    def __init__(
        self,
        container_specs: List[ContainerSpec],
        docker_password: str = None,
        docker_username: str = None,
    ) -> None:
        self.container_specs = container_specs
        self.docker_password = docker_password
        self.docker_username = docker_username

    def to_api_object(
        self,
    ) -> Dict[str, Union[List[Dict[str, Union[int, str]]], bytes]]:
        d = {
            "containers": [c.to_api_object() for c in self.container_specs],
            "dockerAuth": base64.b64encode(
                "{}:{}".format(self.docker_username, self.docker_password).encode()
            ),
        }
        return d

    @classmethod
    def from_api_object(cls, data: Dict[str, Any]) -> "ContainerProcessor":
        containers = [
            ContainerSpec.from_api_object(item) for item in data["containers"]
        ]
        if data.get("dockerAuth"):
            docker_username, docker_password = (
                base64.b64decode(data.get("dockerAuth")).decode("utf-8").split(":", 1)
            )
        else:
            docker_username, docker_password = None, None

        return cls(
            container_specs=containers,
            docker_username=docker_username,
            docker_password=docker_password,
        )


class ProcessorCodeMapping(object):
    """PAI-EAS BuildIn Processor:
    https://help.aliyun.com/document_detail/111029.html
    """

    def from_model_format(self, model_format):
        pass


class BuildInProcessor(object):
    """
    https://help.aliyun.com/document_detail/111029.html

    """

    def __init__(self, processor_code):
        self.processor_code = processor_code

    def __str__(self):
        return "Processor:{}".format(self.processor_code)

    def get_ser_des(self):
        """Get serializer and deserializer.

        Returns:
            Tuple: A tuple of Serializer and Deserializer used by the Processor.
        """

    PMML = "pmml"
    SavedModelProcessor = "tensorflow_cpu_"

    SupportedFrameworkAcceleratorVersionConfig = {
        "tensorflow": {
            "cpu": ["1.12", "1.14", "1.15", "2.3"],
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

    _BuildInProcessor = {
        "tensorflow": {
            "cpu": {""},
            "gpu": {},
        },
        "pytorch": {},
    }

    # Hard code default processor for specific model format.
    ModelFormatProcessorMapping = {
        ModelFormat.PMML: "pmml",
        ModelFormat.SavedModel: "tensorflow_cpu_1.15",
        ModelFormat.TorchScript: "pytorch_cpu_1.6",
        ModelFormat.FrozenPb: "pytorch_cpu_1.6",
        ModelFormat.CaffePrototxt: "caffe_cpu",
        ModelFormat.ONNX: "onnx_cu100",
        ModelFormat.ALinkModel: "alink_pai_processor",
    }

    @classmethod
    def list_by_framework(cls, framework, framework_version=None):
        pass

    @classmethod
    def from_framework_version(
        cls, framework, framework_version=None, accelerator=None
    ):
        pass

    @classmethod
    def from_model_format(cls, model_format: str) -> str:
        if model_format in cls.ModelFormatProcessorMapping:
            return cls.ModelFormatProcessorMapping[model_format]


class ComputeConfig(object):
    def __init__(
        self,
        cpu: Optional[int] = 0,
        memory: Optional[int] = 0,
        gpu: Optional[int] = 0,
        gpu_memory: int = 0,
        instance_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        worker_count: None = None,
    ) -> None:
        self.cpu = cpu
        self.memory = memory
        self.gpu = gpu
        self.gpu_memory = gpu_memory
        self.instance_type = instance_type
        self.resource_id = resource_id
        self.worker_count = worker_count

    @classmethod
    def from_instance_type(
        cls,
        instance_type: str,
        resource_id: Optional[str] = None,
        worker_count: None = None,
    ) -> "ComputeConfig":
        return cls(
            instance_type=instance_type,
            resource_id=resource_id,
            worker_count=worker_count,
        )

    @classmethod
    def from_resource_config(
        cls,
        cpu: Optional[int],
        memory: Optional[int],
        gpu: Optional[int] = 0,
        resource_id: None = None,
        worker_count: None = None,
    ) -> "ComputeConfig":
        return cls(
            cpu=cpu,
            memory=memory,
            gpu=gpu,
            resource_id=resource_id,
            worker_count=worker_count,
        )


class TrafficState(object):
    TRAFFIC_STATE_STANDALONE = "standalone"
    TRAFFIC_STATE_GROUPING = "grouping"
    TRAFFIC_STATE_BLUE_GREEN = "blue-green"


logger = logging.getLogger(__name__)


class ServiceStatus(object):
    """All EAS inference service status."""

    Creating = "Creating"
    Deploying = "Deploying"
    Running = "Running"
    Waiting = "Waiting"
    Pending = "Pending"
    Scaling = "Scaling"
    HotUpdate = "HotUpdate"
    Updating = "Updating"
    Deleting = "Deleting"
    Stopping = "Stopping"
    Starting = "Starting"
    Stopped = "Stopped"
    Failed = "Failed"
    DeleteFailed = "DeleteFailed"

    @classmethod
    def completed_status(cls):
        return [
            cls.Running,
            cls.Stopped,
            cls.Failed,
            cls.DeleteFailed,
        ]


class ServiceRpcConfig(object):
    def __init__(
        self,
        batching=None,
        keepalive=None,
        io_threads=None,
        max_batch_size=None,
        worker_threads=None,
        max_queue_size=None,
        max_batch_timeout=None,
    ):
        self.batching = batching
        self.keepalive = keepalive
        self.io_threads = io_threads
        self.max_batch_size = max_batch_size
        self.worker_threads = worker_threads
        self.max_queue_size = max_queue_size
        self.max_batch_timeout = max_batch_timeout


class WarmupConfig(object):
    def __init__(
        self,
        data_path=None,
        warmup_count=None,
    ):
        self.data_path = data_path
        self.warmup_count = warmup_count


class NetworkConfig(object):
    """
       "vpc_id": "vpc-uf6t31q3xii741wfpru3d",
    "security_group_id": "sg-uf6hqpcwt49z8n36jx5j",
    "vswitch_id": "vsw-uf6px500gvwtdd5lygbrm",
    "default_route": "eth1",
    "destination_cidrs": "10.0.0.0/8"

    """

    def __init__(
        self,
        vpc_id=None,
        security_group_id=None,
        vswitch_id=None,
        destination_cidrs=None,
        default_route=None,
    ):
        self.vpc_id = vpc_id
        self.security_group_id = security_group_id
        self.vswitch_id = vswitch_id
        self.destination_cidrs = destination_cidrs
        self.default_route = default_route


class StorageConfig(object):
    config_key = None

    def __init__(self, mount_path):
        self.mount_path = mount_path

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        mount_path = data.get("mount_path")
        if not mount_path:
            return

        subclasses = [s for s in cls.__subclasses__() if s.config_key in data]
        if len(subclasses) == 1:
            subcls = subclasses[0]
            return subcls.from_dict(data)
        elif len(subclasses) == 0:
            return data
        else:
            logger.warning(
                "More than one storage config is found, using the first.: %s", data
            )
            subcls = subclasses[0]
            return subcls.from_dict(data)

    def to_dict(self):
        pass


class ImageStorageConfig(StorageConfig):
    config_key = "image"

    def __init__(self, path=None, image=None, mount_path=None):
        super(ImageStorageConfig, self).__init__(mount_path)
        self.image = image
        self.path = path

    def to_dict(self):
        return {
            "mount_path": self.mount_path,
            self.config_key: {
                "image": self.image,
                "path": self.path,
            },
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            mount_path=data.get("mount_path"),
            image=data.get(cls.config_key, dict()).get("image"),
            path=data.get(cls.config_key, dict()).get("path"),
        )


class OssStorageConfig(StorageConfig):
    config_key = "oss"

    def __init__(self, path=None, endpoint=None, mount_path=None):
        super(OssStorageConfig, self).__init__(mount_path)
        self.path = path
        self.endpoint = endpoint

    def to_dict(self):
        return {
            "mount_path": self.mount_path,
            self.config_key: {
                "path": self.path,
                "endpoint": self.endpoint,
            },
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            mount_path=data.get("mount_path"),
            path=data.get(cls.config_key, dict()).get("path"),
            endpoint=data.get(cls.config_key, dict()).get("endpoint"),
        )


class NfsStorageConfig(StorageConfig):
    config_key = "nfs"

    def __init__(self, path=None, mount_path=None, server=None, read_only=None):
        super(NfsStorageConfig, self).__init__(mount_path)
        self.path = path
        self.server = server
        self.read_only = read_only

    def to_dict(self):
        return {
            "mount_path": self.mount_path,
            self.config_key: {
                "path": self.path,
                "server": self.server,
                "readOnly": self.read_only,
            },
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            mount_path=data.get("mount_path"),
            path=data.get(cls.config_key, dict()).get("path"),
            server=data.get(cls.config_key, dict()).get("server"),
            read_only=data.get(cls.config_key, dict()).get("readOnly"),
        )


class ServiceConfig(object):
    def __init__(
        self,
        name: str,
        service_group_name: str = None,
        blue_green_release: bool = None,
        token: str = None,
        role: str = None,
        instance_count: int = None,
        compute_target: ComputeConfig = None,
        processor: Union[CustomProcessor, ContainerProcessor, str] = None,
        processor_parameters: List[str] = None,
        model_path: str = None,
        oss_endpoint: str = None,
        traffic_state: str = None,
        model_entry: str = None,
        warmup_data_path: str = None,
        rpc_config: Union[Dict, ServiceRpcConfig] = None,
        network_config: Union[Dict[str, Any], NetworkConfig] = None,
        storage_configs: List[Union[Dict[str, Any], StorageConfig]] = None,
        plugins: List[Dict[str, Any]] = None,
        extra_config: Dict[str, Any] = None,
        original: Dict[str, Any] = None,
        # **kwargs
    ):
        # Service name
        self.name = name
        self.instance_count = instance_count
        self.role = role

        self.blue_green_release = blue_green_release
        self.service_group_name = service_group_name

        # Computing resource
        self.compute_config: ComputeConfig = compute_target

        # Processor
        self.processor = processor
        self.processor_parameters = processor_parameters

        # model_path
        model_path, endpoint = self.parse_model_path(model_path, oss_endpoint)
        self.model_path = model_path
        self.oss_endpoint = oss_endpoint
        self.traffic_state = traffic_state
        self.token = token
        self.model_entry = model_entry
        self.warmup_data_path = warmup_data_path
        self.rpc_config = rpc_config
        self.network_config = network_config
        self.storage_configs = storage_configs
        self.plugins = plugins
        self.original = original
        self.extra_config = extra_config

    @classmethod
    def parse_model_path(cls, model_path, oss_endpoint=None):
        if oss_endpoint is not None or model_path is None:
            return model_path, oss_endpoint

        parsed_oss = parse_oss_url(model_path)
        if not parsed_oss.endpoint:
            return model_path, None

        model_path = "oss://{}/{}".format(parsed_oss.bucket_name, parsed_oss.object_key)
        return model_path, parsed_oss.endpoint

    @classmethod
    def from_api_object(cls, api_object) -> "ServiceConfig":
        return ServiceConfigSchema().load(api_object)

    def to_api_object(self):
        return ServiceConfigSchema().dump(self)


class ConfigAttr(dict):
    def __init__(self, config: "ServiceConfigV2", parent, name):
        super(ConfigAttr, self).__init__()
        self._config: ServiceConfigV2 = config
        self._parent = parent
        self._name = name

    def __hash__(self):
        return hash(json.dumps(self))

    def _get_path_to_node(self):
        """Get JSON node path to attribute node."""
        node = self
        traveled = set(self)
        path_to_attrs = [self._name]

        while node._parent:
            if node._parent in traveled:
                raise ValueError(
                    "Circle detected while get json path of the attribute."
                )
            traveled.add(node._parent)

            path_to_attrs.append(node._parent._name)
            node = node._parent
        path_to_attrs.reverse()

        return path_to_attrs

    def __setattr__(self, key, value):
        if key.startswith("_"):
            self.__dict__[key] = value
            return

        if len(self) == 0:
            self[key] = value

        path_to_attrs = self._get_path_to_node()
        node: Dict = self._config
        for name in path_to_attrs:
            node.setdefault(name, dict())
            node = node[name]
        node[key] = value

    def __getattr__(self, key):
        if len(self) == 0:
            self[key] = ConfigAttr(config=self._config, parent=self, name=key)
            return self[key]
        else:
            if key in self:
                if isinstance(self[key], dict):
                    res = ConfigAttr(config=self._config, parent=self, name=key)
                    res.update(self[key])
                    return res
                else:
                    return self[key]
            else:
                return ConfigAttr(config=self._config, parent=self, name=key)


# class ConfigAttrList(object):
#     def __init__(self, config, parent, name, value=None):
#         self.config = config
#         self.parent = parent
#         self.name = name
#         self.value = None
#
#     def __setattr__(self, key, value):
#         pass
#
#     def __getattr__(self, item):
#         pass
#


class ServiceConfigV2(dict):
    def __init__(self, *args, **kwargs):
        super(ServiceConfigV2, self).__init__(*args, **kwargs)

    def __getattr__(self, key):
        if key in self:
            if isinstance(self[key], dict):
                res = ConfigAttr(config=self, parent=None, name=key)
                res.update(self[key])
                return res
            else:
                return self[key]
        else:
            return ConfigAttr(config=self, parent=None, name=key)

    def __setattr__(self, key, value):
        self[key] = value

    @classmethod
    def from_api_object(cls, data: Union[Dict, str]):
        if isinstance(data, six.string_types):
            data = json.loads(data)

    @classmethod
    def from_json(cls, data: Union[Dict, str]):
        return cls.from_api_object(data)

    def to_dict(self):
        d = dict()
        d.update(self)
        return d


class Service(EntityBaseMixin):
    _schema_cls = ServiceSchema

    def __init__(
        self,
        name,
        session=None,
        status=None,
        internet_endpoint=None,
        intranet_endpoint=None,
        latest_version=None,
        current_version=None,
        reason=None,
        message=None,
        resource_id=None,
        weight=None,
        config=None,
        access_token=None,
        service_id=None,
        service_group=None,
        extra_data=None,
        **kwargs,
    ):
        super(Service, self).__init__(session=session)
        self._name: str = name
        self._config: ServiceConfig = config
        self._status: str = status
        self._reason: str = reason
        self._message: str = message
        self._internet_endpoint: str = internet_endpoint
        self._intranet_endpoint: str = intranet_endpoint
        self._latest_version: int = latest_version
        self._current_version: int = current_version
        self._resource_id: str = resource_id
        self._weight: Union[float, int] = weight
        self._access_token: str = access_token
        self._service_id = service_id
        self._extra_data = extra_data
        self._service_group = service_group
        self._total_instance = kwargs.pop("total_instance", None)
        self._running_instance = kwargs.pop("running_instance", None)

    def __repr__(self):
        return "{}:{} status={} reason={} message={}".format(
            type(self).__name__, self.name, self.status, self.reason, self.message
        )

    @property
    def id(self):
        return self._service_id

    @property
    def name(self):
        return self._name

    @property
    def status(self):
        return self._status

    @property
    def reason(self):
        return self._reason

    @property
    def message(self):
        return self._message

    @property
    def internet_endpoint(self):
        return self._internet_endpoint

    @property
    def intranet_endpoint(self):
        return self._intranet_endpoint

    @property
    def latest_version(self):
        return self._latest_version

    @property
    def current_version(self):
        return self._current_version

    @property
    def resource_id(self):
        return self._resource_id

    @property
    def service_group_name(self):
        return self._service_group

    @property
    def config(self):
        if not self._config:
            self.refresh_state()
        return self._config

    @property
    def compute_target(self) -> ComputeConfig:
        return self.config.compute_config

    @property
    def processor(self):
        return self.config.processor

    @property
    def access_token(self):
        return self._access_token

    @property
    def model_path(self):
        return self.config.model_path

    @property
    def service_id(self):
        return self._service_id

    @property
    def weight(self):
        return self._weight

    @property
    def total_instance(self):
        if not self._config:
            self.refresh_state()
        return self._total_instance

    @property
    def blue_green_services(self):
        if not self._extra_data:
            return []
        extra_data = json.loads(self._extra_data)
        return [self.get(name) for name in extra_data.get("blue_green_services", [])]

    @classmethod
    @config_default_session
    def get(cls, name, session=None) -> "Service":
        return cls.from_api_object(session.service_api.get(name=name), session=session)

    @classmethod
    def _make_service_config(
        cls,
        name,
        instance_count,
        compute_target,
        processor,
        model_path,
        service_group_name=None,
        blue_green_release=None,
        traffic_state=None,
        token=None,
        model_entry=None,
        extra_config=None,
    ):
        config = ServiceConfig(
            name=name,
            instance_count=instance_count,
            compute_target=compute_target,
            processor=processor,
            model_path=model_path,
            service_group_name=service_group_name,
            blue_green_release=blue_green_release,
            traffic_state=traffic_state,
            model_entry=model_entry,
            token=token,
        )
        return config

    def update(
        self,
        processor,
        model,
    ):
        pass

    def switch_version(self, version):
        """Switch service to target version.

        Args:
            version: Target version

        Returns:

        """
        if self._current_version == version:
            raise ValueError("Target version equals to current version.")

        if version > self._latest_version:
            raise ValueError("Target version greater than latest version.")
        self.session.service_api.update_version(self.name, version=version)

    def scale(self, instance_count=None, compute_target=None, wait=True):
        config = ServiceConfig(
            name=self.name, instance_count=instance_count, compute_target=compute_target
        )
        self.session.service_api.update(name=self.name, config=config)

        if wait:
            self.wait_for_ready()

    def stop(self, wait=True):
        self.session.service_api.stop(name=self.name)
        if wait:
            status = ServiceStatus.Stopped
            unexpected_status = ServiceStatus.completed_status()
            unexpected_status.remove(status)
            unexpected_status.remove(ServiceStatus.Running)
            self.wait_for_status(
                status=status,
                unexpected_status=unexpected_status,
            )

    def delete(self):
        self.session.service_api.delete(name=self.name)
        self.session.service_api.refresh_entity(self.name, self)

    def refresh_state(self):
        self.session.service_api.refresh_entity(self.name, self)

    @classmethod
    @config_default_session
    def deploy(
        cls,
        name,
        compute_config: Union[ComputeConfig],
        processor: Union[CustomProcessor, ContainerProcessor, str],
        model_path,
        instance_count=1,
        traffic_state=None,
        token=None,
        extra_config=None,
        model_entry=None,
        session=None,
        wait_for_ready=False,
    ):
        config = cls._make_service_config(
            name=name,
            instance_count=instance_count,
            compute_target=compute_config,
            processor=processor,
            model_path=model_path,
            extra_config=extra_config,
            traffic_state=traffic_state,
            model_entry=model_entry,
            token=token,
        )

        name = session.service_api.create(config=config)
        service = cls.get(name, session=session)

        if wait_for_ready:
            service.wait_for_ready()
        return service

    def blue_green_deploy(
        self,
        compute_target: Union[ComputeConfig],
        processor: Union[CustomProcessor, ContainerProcessor, str],
        instance_count=1,
        model_path=None,
        model_entry=None,
        token=None,
        wait_for_ready=False,
        **kwargs,
    ):

        config = self._make_service_config(
            name=self.name,
            instance_count=instance_count,
            compute_target=compute_target,
            processor=processor,
            model_path=model_path,
            blue_green_release=True,
            token=token,
            model_entry=model_entry,
            **kwargs,
        )
        green_service_name = self.session.service_api.create(config=config)
        green_service = self.get(green_service_name, session=self.session)
        if wait_for_ready:
            green_service.wait_for_ready()
        return green_service

    @classmethod
    @config_default_session
    def group_deploy(
        cls,
        name,
        service_group_name,
        compute_target: Union[ComputeConfig],
        processor: Union[CustomProcessor, ContainerProcessor, str],
        traffic_state=TrafficState.TRAFFIC_STATE_STANDALONE,
        instance_count=1,
        model_path=None,
        model_entry=None,
        token=None,
        session=None,
        wait_for_ready=True,
        **kwargs,
    ):
        config = cls._make_service_config(
            name=name,
            service_group_name=service_group_name,
            instance_count=instance_count,
            compute_target=compute_target,
            processor=processor,
            model_path=model_path,
            token=token,
            model_entry=model_entry,
            traffic_state=traffic_state,
            **kwargs,
        )

        service_name = session.service_api.create(config=config)
        service = cls.get(service_name, session=session)
        if wait_for_ready:
            service.wait_for_ready()
        return service

    @classmethod
    @config_default_session
    def deploy_by_config(
        cls, config: Union[Dict[str, Any], ServiceConfig], session=None
    ):
        if isinstance(config, ServiceConfig):
            config = config.to_api_object()
        name = session.service_api.create(config=config)
        return cls.get(name, session=session)

    @classmethod
    @config_default_session
    def deploy_v2(cls, config: ServiceConfigV2, session=None):
        name = session.service_api.create(config=config)
        return cls.get(name)

    @classmethod
    @config_default_session
    def list(
        cls,
        filter=None,
        order=None,
        page_number=None,
        page_size=None,
        sort=None,
        session=None,
    ) -> List["Service"]:
        res = session.service_api.list(
            filter=filter,
            order=order,
            page_number=page_number,
            page_size=page_size,
            sort=sort,
        )
        return [Service.from_api_object(item, session=session) for item in res.items]

    def wait_for_ready(self, timeout: int = 1200, interval: int = 3) -> None:
        """Wait until the service enter status running.

        Args:
            timeout: Wait timeout in seconds.
            interval: Interval between the get service requests (in seconds).

        Returns:

        """
        print_msg("Service waiting for ready: {}".format(self))
        unexpected_status = ServiceStatus.completed_status()
        unexpected_status.remove(ServiceStatus.Running)

        self.wait_for_status(
            status=ServiceStatus.Running,
            unexpected_status=unexpected_status,
            timeout=timeout,
            interval=interval,
        )

    def adjust_traffic(self, weight):
        if weight < 0 or weight > 100:
            raise ValueError("Invalid weight value, weight should be [0, 100]")
        self.session.service_api.release(name=self.name, weight=weight)
        self.refresh_state()

    def wait_for_status(self, status, unexpected_status, timeout=600, interval=3):
        start_time = datetime.now()
        last_status = self.status
        last_msg = self.message
        time.sleep(interval)

        while True:
            self.session.service_api.refresh_entity(self.name, self)

            # Check the service status
            if self.status == status:
                return self.status
            elif unexpected_status and self.status in unexpected_status:
                # Unexpected terminated status
                raise RuntimeError(
                    "The Service terminated unexpectedly: name={} status={} reason={} message={}.".format(
                        self.name, self.status, self.reason, self.message
                    )
                )
            elif (
                last_status == self.status and self.message == last_msg
            ) and self.status != ServiceStatus.Waiting:
                # if service.status and service.message is not changed, do not print the service status/message.
                pass
            else:
                print_msg(
                    "Refresh Service status: name={} status={} reason={} message={}".format(
                        self.name, self.status, self.reason, self.message
                    )
                )

            if (datetime.now() - start_time).seconds > timeout:
                raise RuntimeError(
                    "Waiting for Service ready timeout: name={} status={} message={} timeout={}.".format(
                        self.name, self.status, self.message, timeout
                    )
                )

            last_status = self.status
            last_msg = self.message
            time.sleep(interval)

    def predict(self, content, serializer=None):
        """

        Args:
            content:
            serializer:

        Returns:

        """
        predictor = self.get_predictor(serializer=serializer)

        result = predictor.predict(content)
        predictor.destruct()
        return result

    def get_service_group_predictor(self, serializer=None):
        serializer = serializer or self.get_default_serializer()
        predictor = Predictor(
            service_name=self.service_group_name,
            access_token=self.access_token,
            endpoint=self.get_prediction_endpoint(),
            serializer=serializer,
        )
        return predictor

    def get_predictor(self, serializer=None):
        """

        Args:
            serializer:

        Returns:

        """
        serializer = serializer or self.get_default_serializer()

        predictor = Predictor(
            service_name=self.get_predictor_service_name(),
            access_token=self.access_token,
            endpoint=self.get_prediction_endpoint(),
            serializer=serializer,
        )
        return predictor

    def get_group_predictor(self, serializer=None):
        pass

    def get_prediction_endpoint(self, network_type=NETWORK_TYPE_TYPE_INTERNET):
        if network_type == NETWORK_TYPE_TYPE_INTERNET:
            parsed = parse.urlparse(self.internet_endpoint)
        else:
            parsed = parse.urlparse(self.internet_endpoint)
        parsed = parsed._replace(path="")._replace(query="")
        return parse.urlunparse(parsed)

    @property
    def is_group_deploy(self):
        """Returns if the service is deployed in group mode."""
        if not self.config:
            self.refresh_state()
        return bool(self.config.service_group_name)

    def get_predictor_service_name(self):
        if not self.config:
            self.refresh_state()

        # If in group deploy mode, API URI path for the specific service should be:
        # <endpoint>/api/predict/<group_name>.<service_name>
        # Documents: https://help.aliyun.com/document_detail/433127.html
        if self.is_group_deploy:
            return "{}.{}".format(self.service_group_name, self.name)
        else:
            return self.name

    def get_default_serializer(self):
        """Get default serializer using in prediction.

        Returns:
            Serializer instance

        """

        from pai.serializers import BaseSerializer, JsonSerializer, TorchSerializer

        if not isinstance(self.processor, str):
            return BaseSerializer()

        if self.processor.lower() == BuildInProcessor.PMML:
            return JsonSerializer()
        elif self.processor.startswith(FrameworkTypes.TensorFlow.lower()):
            return self.build_tensorflow_serializer()
        elif self.processor.startswith(FrameworkTypes.PyTorch.lower()):
            return TorchSerializer()
        else:
            return BaseSerializer()

    def inspect_tensorflow_signature_def(self):
        """Inspect TensorFlow serving model signature by send request to the service.

        PAI-EAS TensorFlow processor provide API using for inspect model signature def.

        Example API return body:
        {
            "signature_name": "serving_default",
            "inputs": [
                {
                    "name": "flatten_input",
                    "shape": [
                        -1,
                        28,
                        28
                    ],
                    "type": "DT_FLOAT"
                }
            ],
            "outputs": [
                {
                    "name": "dense_1",
                    "shape": [
                        -1,
                        10
                    ],
                    "type": "DT_FLOAT"
                }
            ]
        }

        Returns:
            tuple: A tuple of TensorFlowSerializer and TensorFlowDeserializer.

        """
        request = urllib.request.Request(
            url=self.internet_endpoint,
            headers={
                "Authorization": self.access_token,
            },
        )
        resp = urllib.request.urlopen(request)
        signature_def = json.load(resp)
        return signature_def

    def build_tensorflow_serializer(self):

        from pai.serializers import TensorFlowSerializer

        signature_def = self.inspect_tensorflow_signature_def()
        serializer = TensorFlowSerializer.from_signature_def(signature_def)
        return serializer
