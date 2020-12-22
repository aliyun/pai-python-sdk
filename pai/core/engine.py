import json
from abc import ABCMeta
from datetime import datetime
from six import with_metaclass


class ComputeEngineType(object):

    MaxCompute = "MaxCompute"


class EngineEnvType(object):

    Production = "prod"
    Develop = "dev"


class ProductType(object):
    MaxCompute = "MaxCompute"
    PAI = "PAI"


class ComputeEngine(with_metaclass(ABCMeta)):
    EngineType = None

    def __init__(self, name, is_default=False):
        self.name = name
        self.is_default = is_default

    def __str__(self):
        return "%s:%s" % (type(self).__name__, self.name)

    def __repr__(self):
        return self.__str__()

    def to_execution_config(self, **kwargs):
        raise NotImplementedError(
            "to_execution_config in ComputeEngine is not implemented."
        )

    @classmethod
    def deserialize(cls, compute_engine_info):
        if "ResourceInstances" not in compute_engine_info:
            raise ValueError(
                "require 'ResourceInstance' in ComputeEngine information dict."
            )

        engine_type = compute_engine_info["ResourceInstances"][0].get("ProductType")

        if not engine_type:
            raise ValueError("engine type not found in the engine instances.")

        for engine_cls in ComputeEngine.__subclasses__():
            if engine_cls.EngineType == engine_type:
                return engine_cls.deserialize(compute_engine_info)
        return cls(
            name=compute_engine_info["Name"],
            is_default=compute_engine_info["IsDefault"],
        )


class MaxComputeEngine(ComputeEngine):
    EngineType = ComputeEngineType.MaxCompute

    def __init__(self, project_instances, workspace_id, **kwargs):
        self.project_instances = project_instances
        self.workspace_id = workspace_id
        super(MaxComputeEngine, self).__init__(**kwargs)

    def to_execution_config(self, env_type=None, **kwargs):
        if env_type and env_type not in [
            EngineEnvType.Production,
            EngineEnvType.Develop,
        ]:
            raise ValueError("invalidate env_type parameter.")

        if len(self.project_instances) == 0:
            raise ValueError("no MaxCompute instance is available.")
        if len(self.project_instances) == 1:
            project_instance = self.project_instances[0]
        else:
            if not env_type:
                env_type = EngineEnvType.Develop
            project_instance = next(
                (
                    instance
                    for instance in self.project_instances
                    if instance.env_type == env_type
                ),
                None,
            )
            if not project_instance:
                raise ValueError(
                    "no MaxCompute project instance match the env_type:%s" % env_type
                )

        return {
            "endpoint": project_instance.endpoint,
            "project": project_instance.project_name,
        }

    @classmethod
    def deserialize(cls, engine_info):
        instances = [
            MaxComputeProjectInstance.create(info)
            for info in engine_info["ResourceInstances"]
        ]

        workspace_id = instances[0].workspace_id

        name = engine_info["Name"]
        is_default = engine_info["IsDefault"]

        return cls(
            project_instances=instances,
            workspace_id=workspace_id,
            name=name,
            is_default=is_default,
        )


class MaxComputeProjectInstance(object):
    """"""

    def __init__(
        self,
        id,
        create_time,
        env_type,
        is_default,
        name,
        resource_groups,
        project_name,
        endpoint,
        workspace_id,
    ):
        self.id = id
        self.create_time = create_time
        self.env_type = env_type
        self.is_default = is_default
        self.name = name
        self.project_name = project_name
        self.endpoint = endpoint
        self.workspace_id = workspace_id
        self.resource_groups = resource_groups
        self.id = id

    @classmethod
    def create(cls, instance_info):
        create_time = (
            datetime.fromtimestamp(int(instance_info["CreateTime"]) / 1000)
            if instance_info.get("CreateTime")
            else None
        )
        env_type = instance_info.get("EnvType")
        is_default = instance_info.get("IsDefault")
        name = instance_info.get("Name")
        resource_groups = [
            ResourceGroup.deserialize(rg_info)
            for rg_info in instance_info["ResourceGroups"]
        ]

        spec_info = json.loads(instance_info["Spec"])
        project_name = spec_info["ProjectName"]
        endpoint = spec_info["Endpoint"]
        workspace_id = instance_info["WorkspaceId"]
        id = instance_info["Id"]
        return cls(
            id=id,
            create_time=create_time,
            env_type=env_type,
            is_default=is_default,
            name=name,
            resource_groups=resource_groups,
            project_name=project_name,
            endpoint=endpoint,
            workspace_id=workspace_id,
        )


class ResourceGroup(object):

    CardTypeCPU = "cpu"
    CardTypeGPU = "gpu"

    ModeShare = "share"
    ModeIsolate = "isolate"

    CommodityCodePaiPrePay = "learn_studioGPU_public_cn"
    CommodityCodePaiPostPay = "pai"
    CommodityCodeMaxComputePostPay = "post-odps"
    CommodityCodeMaxComputePrePay = "odps"

    """
    {
        'CardType': None,
        'CommodityCode': 'post-odps',
        'Mode': 'share',
        'Name': 'aliyun_group_ay20',
        'ProductType': 'MaxCompute',
        'Quotas': [{'Name': 'aliyun',
                  'Spec': '{"cu":"11500","minCu":"2300","parentId":"0"}'}]
    }
    """

    def __init__(self, name, card_type, commodity_code, mode, product_type, quotas):
        self.name = name
        self.card_type = card_type
        self.commodity_code = commodity_code
        self.mode = mode
        self.product_type = product_type
        self.quotas = quotas

    def __str__(self):
        return "%s:%s:%s:%s" % (
            type(self).__name__,
            self.name,
            self.commodity_code,
            self.mode,
        )

    def __repr__(self):
        return self.__str__()

    @classmethod
    def deserialize(cls, resource_group_info):
        name = resource_group_info["Name"]
        card_type = resource_group_info["CardType"]
        commodity_code = resource_group_info["CommodityCode"]
        mode = resource_group_info["Mode"]
        product_type = resource_group_info["ProductType"]
        quotas = resource_group_info["Quotas"]

        return cls(
            name=name,
            card_type=card_type,
            commodity_code=commodity_code,
            mode=mode,
            product_type=product_type,
            quotas=quotas,
        )
