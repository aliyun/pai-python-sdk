import json
import logging
import typing
from typing import Any, Dict, Union

import six
from marshmallow import (
    INCLUDE,
    Schema,
    fields,
    post_dump,
    post_load,
    pre_load,
    validate,
)

from .base import BaseAPIResourceSchema

logger = logging.getLogger(__name__)

if typing.TYPE_CHECKING:
    from pai.entity.service import (
        ComputeConfig,
        NetworkConfig,
        ServiceConfig,
        ServiceRpcConfig,
        StorageConfig,
    )


class EasServiceConfigMetadataSchema(Schema):
    class Meta(object):
        unknown = INCLUDE

    name = fields.String()
    cpu = fields.Integer()
    memory = fields.Integer()
    gpu = fields.Integer()
    instance = fields.Integer()
    resource_id = fields.String()


class EasServiceConfigCloudNetworkingSchema(Schema):
    class Meta(object):
        unknown = INCLUDE


class EasServiceConfigCloudComputingSchema(Schema):
    class Meta(object):
        unknown = INCLUDE

    instance_type = fields.Str()


class EasServiceConfigCloudSchema(Schema):
    class Meta(object):
        unknown = INCLUDE

    computing = fields.Nested(EasServiceConfigCloudComputingSchema)
    networking = fields.Nested(EasServiceConfigCloudNetworkingSchema)


class EasServiceConfigCloud(Schema):
    """


    {
        "cloud": {
        "computing": {
            "instance_type": "ecs.c6.large"
        },
        "networking": {
            "default_route": "eth0",
            "destination_cidrs": "192.168.0.1/8",
            "security_group_id": "sg-uf68sxd8cxajzc5mzjne",
            "vpc_id": "vpc-uf6t31q3xii741wfpru3d",
            "vswitch_id": "vsw-uf6kv5tuc5dgdmdw67ah2"
        }
    }
    """


class ServiceConfigSchema(
    Schema,
):
    class Meta(object):
        unknown = INCLUDE
        # additional = ("compute_target",)

    name = fields.String()
    metadata = fields.Nested(EasServiceConfigMetadataSchema)
    cloud = fields.Nested(EasServiceConfigCloudSchema)
    model_path = fields.String()
    oss_endpoint = fields.String()

    model_config = fields.Dict()
    processor = fields.Raw()
    processor_type = fields.String(
        validate=validate.OneOf(choices=("python", "java", "cpp"))
    )
    processor_path = fields.String()
    processor_entry = fields.String()
    # containers = fields.String()
    docker_auth = fields.String(data_key="dockerAuth")

    @post_load(pass_original=True)
    def make(self, data, original, **kwargs):
        from pai.entity.service import ServiceConfig

        metadata = data.pop("metadata", dict())
        name = data.get("name") or metadata.get("name")
        instance_count = metadata.get("instance")
        blue_green_release = metadata.get("release")
        service_group_name = metadata.get("group")
        traffic_state = metadata.get("traffic_state")
        role = metadata.get("role")
        token = data.pop("token", None)
        processor_parameters = data.pop("processor_params", None)

        processor = self._make_processor(original)
        compute_target = self._make_compute_target(original)
        network_config = self._make_network_config(original)
        storage_config = self._make_storage_config(original)
        rpc_config = self._make_rpc_config(original)
        warmup_data_path = original.get("warm_up_data_path")
        plugin_configs = original.get("plugins", None)

        # extra_config = self._make_extra_config(original.copy())

        return ServiceConfig(
            name=name,
            role=role,
            blue_green_release=blue_green_release,
            compute_target=compute_target,
            processor=processor,
            processor_parameters=processor_parameters,
            instance_count=instance_count,
            model_path=data.get("model_path"),
            model_entry=data.get("model_entry"),
            oss_endpoint=data.get("oss_endpoint"),
            warmup_data_path=warmup_data_path,
            service_group_name=service_group_name,
            traffic_state=traffic_state,
            rpc_config=rpc_config,
            network_config=network_config,
            storage_configs=storage_config,
            plugins=plugin_configs,
            token=token,
            original=original,
            # extra_config=extra_config,
        )

    @classmethod
    def _make_plugin_configs(cls, original):
        pass

    @classmethod
    def _make_storage_config(cls, original):
        from pai.entity.service import StorageConfig

        data = original.get("storage", [])
        if not data:
            return
        results = []
        for d in data:
            conf = StorageConfig.from_dict(d)
            if conf:
                results.append(conf)

        return results

    @classmethod
    def _make_network_config(cls, original):
        from pai.entity.service import NetworkConfig

        """Make a NetworkConfig instance from config dict.

        Example networking config.
        {
            "cloud": {
                "networking": {
                    "vpc_id": "vpc-uf6t31q3xii741wfpru3d",
                    "security_group_id": "sg-uf63t5b2wnmth1focgmp",
                    "vswitch_id": "vsw-uf6px500gvwtdd5lygbrm",
                    "destination_cidrs": "10.0.0.0/24",
                    "default_route": "eth1"
                }
            }
        }

        """
        networking = original.get("cloud", {}).get("networking", dict())
        if not networking:
            return
        config = NetworkConfig(
            vpc_id=networking.get("vpc_id"),
            security_group_id=networking.get("security_group_id"),
            vswitch_id=networking.get("vswitch_id"),
            destination_cidrs=networking.get("destination_cidrs"),
            default_route=networking.get("default_rout"),
        )
        return config

    @classmethod
    def _make_rpc_config(cls, original):
        from pai.entity.service import ServiceRpcConfig

        metadata = original.get("metadata", dict())
        if not metadata:
            return
        config = ServiceRpcConfig(
            batching=metadata.get("rpc.batching"),
            keepalive=metadata.get("rpc.keepalive"),
            io_threads=metadata.get("rpc.io_threads"),
            max_batch_size=metadata.get("rpc.max_batch_size"),
            max_batch_timeout=metadata.get("rpc.max_batch_timeout"),
            max_queue_size=metadata.get("rpc.max_queue_size"),
            worker_threads=metadata.get("rpc.worker_threads"),
        )
        return config

    @classmethod
    def _make_warmup_config(cls, original):
        data_path = original.get("warm_up_data_path")
        if not data_path:
            return

        original.get("metadata", dict()).get("")

    @classmethod
    def _make_extra_config(cls, data: Dict[str, Union[str, Dict]]):
        exclude_keys = [
            "metadata",
            "processor",
            "processor_type",
            "processor_path",
            "processor_entry",
            "processor_mainclass",
            "model_path",
            "oss_endpoint",
            "containers",
            "dockerAuth",
            "cloud",
            "model_entry",
            "token",
        ]

        for key in exclude_keys:
            data.pop(key, None)
        return data

    @classmethod
    def _make_compute_target(cls, data):
        from pai.entity.service import ComputeConfig

        metadata = data.get("metadata", dict())
        cpu = metadata.get("cpu")
        memory = metadata.get("memory")
        gpu = metadata.get("gpu")
        resource_id = metadata.get("resource")
        worker_count = metadata.get("worker_count")

        cloud = data.get("cloud")
        if cloud and cloud.get("computing") and cloud.get("computing", "instance_type"):
            instance_type = cloud.get("computing").get("instance_type")
        else:
            instance_type = None

        if instance_type:
            # Config by VM InstanceType
            compute_target = ComputeConfig.from_instance_type(
                instance_type=instance_type,
                resource_id=resource_id,
                worker_count=worker_count,
            )
            if cpu is not None:
                compute_target.cpu = cpu
                compute_target.gpu = gpu
                compute_target.memory = memory
        else:
            # Config by Instance resource request.
            compute_target = ComputeConfig.from_resource_config(
                cpu=cpu,
                memory=memory,
                gpu=gpu,
                resource_id=resource_id,
            )
        return compute_target

    @classmethod
    def _make_processor(cls, data):
        from pai.entity.service import ContainerProcessor, CustomProcessor

        if data.get("processor"):
            return data.get("processor")
        elif data.get("containers"):
            return ContainerProcessor.from_api_object(data)
        elif data.get("processor_type"):
            return CustomProcessor.from_api_object(data)
        else:
            return

    @post_dump(pass_original=True)
    def post_dump_process(self, data, original: "ServiceConfig", **kwargs):
        result = original.extra_config if original.extra_config else dict()
        if original.name:
            result.update({"name": original.name})
        if original.processor:
            result = self.patch_processor(result, processor=original.processor)
        if original.instance_count:
            result.setdefault("metadata", dict())
            result["metadata"]["instance"] = original.instance_count

        if original.blue_green_release:
            result.setdefault("metadata", dict())
            result["metadata"]["release"] = original.blue_green_release

        if original.service_group_name:
            result.setdefault("metadata", dict())
            result["metadata"]["group"] = original.service_group_name

        if original.role:
            result.setdefault("metadata", dict())
            result["metadata"]["role"] = original.role

        if original.traffic_state is not None:
            result.setdefault("metadata", dict())
            result["metadata"]["traffic_state"] = original.traffic_state

        if original.token is not None:
            result["token"] = original.token

        if original.model_path:
            result["model_path"] = original.model_path

        if original.model_entry:
            result["model_entry"] = original.model_entry

        if original.compute_config:
            result = self.patch_compute_target(
                result, compute_target=original.compute_config
            )
        if original.network_config:
            result = self.patch_networking_config(
                result, network_config=original.network_config
            )

        if original.storage_configs:
            result = self.patch_storage_config(result, original.storage_configs)

        if original.plugins:
            result = self.patch_plugins(result, original.plugins)

        if original.rpc_config:
            result = self.patch_rpc_config(result, rpc_config=original.rpc_config)

        return result

    @classmethod
    def patch_compute_target(
        cls, config: Dict[str, Union[str, Dict]], compute_target: "ComputeConfig"
    ):
        if not compute_target:
            return config

        if compute_target.worker_count:
            config.setdefault("metadata", dict())
            config["metadata"]["worker_count"] = compute_target.worker_count

        if compute_target.instance_type:
            config.setdefault("cloud", dict())
            config["cloud"]["computing"] = {
                "instance_type": compute_target.instance_type
            }
        if compute_target.resource_id:
            config.setdefault("metadata", dict())
            config["metadata"]["resource"] = compute_target.resource_id

        if compute_target.cpu:
            config.setdefault("metadata", dict())
            resource_config = {
                "cpu": compute_target.cpu,
                "memory": compute_target.memory,
                "gpu": compute_target.gpu,
            }
            config["metadata"].update(resource_config)

        return config

    @classmethod
    def patch_processor(cls, config, processor):
        from pai.entity.service import ContainerProcessor, CustomProcessor

        if isinstance(processor, (ContainerProcessor, CustomProcessor)):
            config.update(processor.to_api_object())
        elif isinstance(processor, six.string_types):
            config.update(
                {
                    "processor": processor,
                }
            )
        return config

    @classmethod
    def patch_rpc_config(cls, config, rpc_config: "ServiceRpcConfig") -> Dict[str, Any]:
        if not rpc_config:
            return config

        config.setdefault("metadata", dict())
        if rpc_config.keepalive:
            config["metadata"]["rpc.keepalive"] = rpc_config.keepalive

        if rpc_config.io_threads:
            config["metadata"]["rpc.io_threads"] = rpc_config.io_threads

        if rpc_config.batching:
            config["metadata"]["rpc.batching"] = rpc_config.batching
            if rpc_config.max_batch_size:
                config["metadata"]["rpc.max_batch_size"] = rpc_config.max_batch_size
            if rpc_config.max_batch_timeout:
                config["metadata"][
                    "rpc.max_batch_timeout"
                ] = rpc_config.max_batch_timeout
            if rpc_config.max_queue_size:
                config["metadata"]["rpc.max_queue_size"] = rpc_config.max_queue_size
            if rpc_config.worker_threads:
                config["metadata"]["rpc.worker_threads"] = rpc_config.worker_threads

        return config

    @classmethod
    def patch_networking_config(cls, config, network_config: "NetworkConfig"):
        if not network_config:
            return config
        config.setdefault("cloud", dict())
        data = {
            "vpc_id": network_config.vpc_id,
            "security_group_id": network_config.security_group_id,
            "vswitch_id": network_config.vswitch_id,
            "destination_cidrs": network_config.destination_cidrs,
            "default_route": network_config.default_route,
        }
        data = {k: v for k, v in data.items() if v is not None}
        config["cloud"]["networking"] = data
        return config

    @classmethod
    def patch_storage_config(
        cls,
        config,
        storage_configs: typing.List[Union["StorageConfig", Dict[str, Any]]],
    ):
        from pai.entity.service import StorageConfig

        if not storage_configs:
            return config
        results = []
        for c in storage_configs:
            if isinstance(c, StorageConfig):
                results.append(c.to_dict())
            else:
                results.append(c)
        config["storage"] = results

        return config

    @classmethod
    def patch_plugins(cls, config: Dict[str, Any], plugins: typing.List[Dict]):
        if plugins:
            config["plugins"] = plugins

        return config


class ServiceSchema(BaseAPIResourceSchema):
    """Dataset schema.
    API Object Example:

        {
            "AccessToken": "Y2I4YzIwM2I0NjFlNWU3ZGMwNThkNGJkN2VkN2UwNzQ4ZGVmNjZkMA==",
            "CallerUid": "1157703270994901",
            "Cpu": 2,
            "CreateTime": "2022-07-12T06:24:48Z",
            "CurrentVersion": 1,
            "Gpu": 0,
            "Image": "",
            "LatestVersion": 1,
            "Memory": 4000,
            "Message": "Successfully synchronized resources",
            "Namespace": "dsdssd",
            "ParentUid": "1157703270994901",
            "PendingInstance": 1,
            "Reason": "WAITING",
            "Resource": "",
            "RunningInstance": 0,
            "ServiceId": "eas-m-wfhyu5vturbgpro8j5",
            "ServiceName": "dsdssd",
            "Status": "Waiting",
            "TotalInstance": 1,
            "Weight": 100,
        }
    """

    class Meta(object):
        unknown = INCLUDE

    FieldNameMapping = {
        "CreateTime": "create_time",
        "UpdateTime": "modified_time",
        "ServiceName": "name",
        "ServiceConfig": "config",
    }

    name = fields.Str()

    status = fields.Str()

    running_instance = fields.Int()
    pending_instance = fields.Int()
    total_instance = fields.Int()
    latest_version = fields.Int()
    access_token = fields.Str()
    message = fields.Str()
    weight = fields.Int()
    config = fields.Nested(ServiceConfigSchema)
    extra_data = fields.Str()
    service_group = fields.Str()

    # Load only fields.
    create_time = fields.DateTime()
    modified_time = fields.DateTime()
    service_id = fields.Str()

    @pre_load
    def _pre_load_process(self, data, **kwargs):
        if "config" not in data:
            return data

        if isinstance(data["config"], six.string_types):
            data["config"] = json.loads(data["config"])
        return data

    @post_load(pass_original=True)
    def _make(self, data, original, **kwargs):
        from pai.entity.service import Service

        return self.make_or_reload(Service, data)
