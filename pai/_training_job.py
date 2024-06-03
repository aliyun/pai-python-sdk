from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_pascal


class BaseAPIModel(BaseModel):

    model_config = ConfigDict(
        alias_generator=to_pascal,
        populate_by_name=True,
    )

    def model_dump(self, **kwargs) -> Dict[str, Any]:
        kwargs.update({"by_alias": True, "exclude_none": True})
        return super().model_dump(**kwargs)


class OssLocation(BaseAPIModel):
    bucket: str
    key: str
    endpoint: Optional[str]


class CodeDir(BaseAPIModel):
    location_value: Union[OssLocation, Dict[str, Any]]
    location_type: str


class HyperParameter(BaseAPIModel):
    value: str
    Name: str


class InstanceSpec(BaseAPIModel):
    memory: str
    cpu: str = Field(alias="CPU")
    gpu: str = Field(alias="GPU")
    shared_memory: Optional[str] = None


class ComputeResource(BaseAPIModel):
    ecs_count: int
    ecs_spec: str
    instance_count: int
    instance_spec: Optional[InstanceSpec] = None


class UriInput(BaseAPIModel):
    name: str
    uri: str = Field(alias="InputUri")


class DatasetInput(BaseAPIModel):
    name: str
    dataset_id: str
    dataset_name: Optional[str] = None


class Channel(BaseAPIModel):
    name: str
    description: Optional[str] = None
    required: Optional[bool] = None
    supported_channel_types: Optional[List[str]] = None
    properties: Optional[Dict[str, Any]] = None


class AlgorithmSpec(BaseAPIModel):
    command: List[str]
    image: str
    supported_channel_types: List[str] = Field(default_factory=list)
    output_channels: List[Channel] = Field(default_factory=list)
    input_channels: List[Channel] = Field(default_factory=list)
    supports_distributed_training: bool = False
    metric_definitions: List = Field(default_factory=list)
    hyperparameter_definitions: List[Dict[str, Any]] = Field(
        default_factory=list, alias="HyperParameter"
    )
    job_type: Literal["PyTorchJob"] = Field(default="PyTorchJob")
    code_dir: Optional[CodeDir] = None


class TrainingJobSpec(BaseAPIModel):
    compute_resource: ComputeResource
    hyperparameters: List[HyperParameter] = Field(
        default_factory=list, alias="HyperParameters"
    )
    inputs: List[Union[UriInput, DatasetInput]] = Field(
        default_factory=list, alias="InputChannels"
    )
    algorithm_spec: Optional[AlgorithmSpec] = None
    algorithm_version: Optional[str] = None
    algorithm_provider: Optional[str] = None
    algorithm_name: Optional[str] = None
