from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class LocationValueModel(BaseModel):
    Bucket: str
    Key: str
    Endpoint: Optional[str]


class CodeDirModel(BaseModel):
    LocationValue: LocationValueModel
    LocationType: str


class HyperParameter(BaseModel):
    Value: str
    Name: str


class InstanceSpecModel(BaseModel):
    Memory: str
    CPU: str
    GPU: str
    SharedMemory: Optional[str] = None


class ComputeResource(BaseModel):
    EcsCount: int
    EcsSpec: str
    InstanceCount: int
    InstanceSpec: Optional[InstanceSpecModel] = None


class UriInput(BaseModel):
    Name: str
    Uri: str = Field(alias="InputUri")


class DatasetInput(BaseModel):
    Name: str
    DatasetId: str
    DatasetName: Optional[str] = None


class ChannelDefinition(BaseModel):
    Name: str
    Description: Optional[str] = None
    Required: Optional[bool] = None
    SupportedChannelTypes: Optional[List[str]] = None
    Properties: Optional[Dict[str, Any]] = None


class AlgorithmSpecModel(BaseModel):
    Command: List[str]
    Image: str
    SupportedInstanceTypes: List[str] = Field(default_factory=list)
    OutputChannels: List[ChannelDefinition] = Field(
        default_factory=list, Alias="OutputChannels"
    )
    InputChannels: List[ChannelDefinition] = Field(
        default_factory=list, Alias="InputChannels"
    )
    SupportsDistributedTraining: bool = False
    MetricDefinitions: List = Field(default_factory=list)
    HyperParameters: List = Field(default_factory=list)
    JobType: str = Field(default="PyTorchJob")
    CodeDir: Optional[CodeDirModel] = None


class TrainingJobSpec(BaseModel):

    ComputeResource: ComputeResource
    HyperParameters: List[HyperParameter] = Field(default_factory=list)
    InputChannels: List[Union[UriInput, DatasetInput]] = Field(default_factory=list)
    AlgorithmSpec: Optional[AlgorithmSpecModel] = None
    AlgorithmVersion: Optional[str] = None
    AlgorithmProvider: Optional[str] = None
    AlgorithmName: Optional[str] = None
