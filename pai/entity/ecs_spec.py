from pai.entity.base import EntityBaseMixin
from pai.schema.ecs_spec_schema import EcsSpecSchema


class EcsSpec(EntityBaseMixin):
    _schema_cls = EcsSpecSchema

    def __init__(
        self,
        accelerator_type=None,
        cpu=None,
        gpu=None,
        gpu_type=None,
        instance_type=None,
        memory=None,
        **kwargs,
    ):
        super(EcsSpec, self).__init__(**kwargs)
        self.accelerator_type = accelerator_type  # type: str
        self.cpu = cpu  # type: int
        self.gpu = gpu  # type: int
        self.gpu_type = gpu_type  # type: str
        self.instance_type = instance_type  # type: str
        self.memory = memory  # type: int

    def __repr__(self):
        if self.accelerator_type.lower() == "gpu":
            return "EcsSpec: InstanceType={} CPU={}vCPU Memory={}G GPU={}*{}".format(
                self.instance_type, self.cpu, self.memory, self.gpu, self.gpu_type
            )
        else:
            return "EcsSpec: InstanceType={} CPU={}vCPU Memory={}G".format(
                self.instance_type, self.cpu, self.memory
            )
