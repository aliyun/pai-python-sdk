from __future__ import absolute_import

import json
import re

import six
from enum import Enum
from odps.df import DataFrame as ODPSDataFrame
from odps.models import Table as ODPSTable, Partition as ODPSPartition, Volume as ODPSVolume
from odps.models.ml.offlinemodel import OfflineModel as ODPSOfflineModel

from pai.pipeline.types.variable import PipelineVariable


class PipelineArtifact(PipelineVariable):
    variable_category = "artifacts"

    def __init__(self, name, metadata=None, path=None, desc=None, kind="inputs", default=None,
                 from_=None, required=None, parent=None):
        super(PipelineArtifact, self).__init__(name=name, desc=desc, kind=kind,
                                               value=default, from_=from_,
                                               required=required, parent=parent)
        self.metadata = metadata
        self.path = path

    def validate_from(self, arg):
        if not isinstance(arg, PipelineArtifact):
            raise ValueError("arg is expected to be type of 'PipelineParameter' "
                             "but was actually of type '%s'" % type(arg))

        if arg.metadata is not None and self.metadata is not None and arg.metadata != self.metadata:
            return False

        return True

    # TODO: Artifact value validation
    def validate_value(self, val):
        return True

    @classmethod
    def to_argument_by_spec(cls, val, af_spec, kind="inputs"):
        af_spec = af_spec.copy()

        name = af_spec.pop("name")
        metadata = ArtifactMetadata.from_dict(af_spec.pop("metadata", None))
        desc = af_spec.pop("desc", None)
        from_ = af_spec.pop("from", None)
        required = af_spec.pop("required", None)

        param = PipelineArtifact(name=name, metadata=metadata, kind=kind, from_=from_,
                                 required=required, desc=desc)
        af_value = ArtifactValue.from_resource(val)
        if not param.validate_value(val):
            raise ValueError(
                "Not Validate value for Parameter %s, value(%s:%s)" % (name, type(val), val))
        param.value = af_value
        return param.to_argument()

    def to_argument(self):
        arguments = {
            "name": self.name
        }

        if self.from_ is not None:
            if isinstance(self.from_, PipelineArtifact):
                arguments["from"] = "{{%s}}" % self.from_.fullname
            else:
                arguments["from"] = self.from_
        elif self.value is not None:
            arguments["value"] = json.dumps(self.value.to_dict(), sort_keys=True)
        return arguments

    def to_dict(self):
        d = super(PipelineArtifact, self).to_dict()
        d["metadata"] = self.metadata.to_dict()
        if self.value is not None:
            if isinstance(self.value, ArtifactValue):
                d["value"] = self.value.to_dict()
            else:
                d["value"] = self.value
        if self.path is not None:
            d["path"] = self.path
        return d


class ArtifactMetadata(object):

    def __init__(self, data_type, location_type, model_type=None, path=None):
        self.data_type = data_type
        self.location_type = location_type
        self.model_type = model_type
        self.path = path

    def __str__(self):
        return '{%s}:{locationType:%s, modelType:%s}' % (self.data_type,
                                                         self.location_type,
                                                         self.model_type)

    def to_dict(self):
        d = {
            "type": {
                self.data_type.value: {
                    "locationType": self.location_type.value,
                }
            }
        }

        if self.model_type is not None:
            d["type"][self.data_type.value]["modelType"] = self.model_type.value
        if self.path is not None:
            d["path"] = self.path

        return d

    @property
    def value(self):
        return self.to_dict()

    def __eq__(self, other):
        if isinstance(other, ArtifactMetadata):
            return self.data_type == other.data_type \
                   and self.location_type == other.location_type \
                   and self.model_type == other.model_type
        elif isinstance(other, dict):
            other = self.from_dict(other)
            return self.__eq__(other)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def from_dict(cls, d):
        af_typ = d["type"]

        data_type = ArtifactDataType(list(af_typ.keys())[0])
        location_type = ArtifactLocationType(af_typ[data_type.value]["locationType"])
        model_type = None
        if "modelType" in af_typ[data_type.value]:
            model_type = ArtifactModelType(af_typ[data_type.value]["modelType"])
        path = d.get("path")

        return cls(data_type=data_type, location_type=location_type,
                   model_type=model_type, path=path)


class ArtifactValue(object):

    def __init__(self):
        pass

    @classmethod
    def from_resource(cls, resource, metadata=None):
        if isinstance(resource, six.string_types):
            if resource.startswith("odps://"):
                return MaxComputeResourceArtifact.from_resource_url(resource)
            elif resource.startswith("oss://"):
                return OSSArtifact.from_resource_url(resource)
            else:
                try:
                    resource_dict = json.loads(resource)
                except json.JSONDecodeError:
                    raise ValueError("Not support artifact url schema:%s", resource)
                return cls.from_raw_value(resource_dict, metadata)
        elif isinstance(resource, (ODPSTable, ODPSPartition, ODPSDataFrame, ODPSVolume)):
            return MaxComputeResourceArtifact.from_odps_resource(resource)
        elif isinstance(resource, ArtifactEntity):
            return resource.value
        elif isinstance(resource, ArtifactValue):
            return resource

        raise ValueError("Not support artifact resource:%s", type(resource))

    @classmethod
    def from_raw_value(cls, value, metadata):
        if metadata is None:
            raise ValueError(
                400, "ArtifactMetadata should provide while parse artifact value from dict data.")
        if metadata.location_type == ArtifactLocationType.OSS:
            return OSSArtifact.from_dict(value)
        elif metadata.location_type == ArtifactLocationType.MaxComputeTable:
            return MaxComputeTableArtifact.from_dict(value)
        elif metadata.location_type == ArtifactLocationType.MaxComputeOfflineModel:
            return MaxComputeOfflineModelArtifact.from_dict(value)
        elif metadata.location_type == ArtifactLocationType.MaxComputeVolume:
            return MaxComputeVolumeArtifact.from_dict(value)
        else:
            raise ValueError("Not support artifact location_type: %s", metadata.location_type)


class MaxComputeResourceArtifact(ArtifactValue):
    MaxComputeResourceUrlPattern = re.compile(
        r"odps://(?P<project>[^/]+)/(?P<resource_type>(?:tables)|(?:volumes)|(?:offlinemodels))/"
        r"(?P<resource_name>[^/]+)/?(?P<sub_resource>[^\?]+)?(?P<arguments>[.*])?")

    def __init__(self, project, endpoint=None):
        super(MaxComputeResourceArtifact, self).__init__()
        self.project = project
        self.endpoint = endpoint

    def to_dict(self):
        d = {
            "location": {
                "project": self.project,
            }
        }
        if self.endpoint:
            d["location"]["endpoint"] = self.endpoint
        return d

    @classmethod
    def from_resource_url(cls, resource_url):
        matches = cls.MaxComputeResourceUrlPattern.match(resource_url)
        if not matches:
            raise ValueError("Not support MaxCompute resource url format.")
        resource_type = matches.group("resource_type")
        project = matches.group("project")
        if resource_type == "tables":
            table = matches.group('resource_name')
            partition = matches.group("sub_resource")
            return MaxComputeTableArtifact(
                project=project,
                table=table,
                partition=partition.strip("/") if partition else None,
            )
        elif resource_type == "volumes":
            volume = matches.group("resource_name")
            sub_resource = matches.group("sub_resource").strip("/")
            idx = sub_resource.find("/")
            partition = sub_resource[:idx]
            file_name = sub_resource[idx + 1:]
            return MaxComputeVolumeArtifact(
                project=project,
                volume=volume,
                partition=partition,
                file_name=file_name,
            )

        elif resource_type == "offlinemodels":
            name = matches.group("resource_name")
            return MaxComputeOfflineModelArtifact(
                project=project,
                offline_model=name,
            )
        else:
            raise ValueError("Not support MaxCompute resource type :%s" % resource_type)

    @classmethod
    def from_odps_resource(cls, resource):
        if not isinstance(resource, (ODPSTable, ODPSPartition, ODPSDataFrame, ODPSVolume)):
            raise ValueError("Not support resource type:%s" % type(resource))

        if isinstance(resource, ODPSDataFrame):
            resource = resource.data

        if isinstance(resource, ODPSTable):
            project = resource.project.name
            table = resource.name
            return MaxComputeTableArtifact(
                project=project,
                table=table,
            )
        elif isinstance(resource, ODPSPartition):
            table = resource.table.name
            project = resource.table.project.name
            partition = ','.join(["%s=%s" % (k, v) for k, v in resource.partition_spec.kv.items()])
            return MaxComputeTableArtifact(
                project=project,
                partition=partition,
                table=table
            )
        elif isinstance(resource, ODPSOfflineModel):
            project = resource.project.name
            offlinemodel = resource.name
            return MaxComputeOfflineModelArtifact(
                project=project,
                offline_model=offlinemodel
            )
        # TODO: ODPSVolume Support
        elif isinstance(resource, ODPSVolume):
            pass


class MaxComputeTableArtifact(MaxComputeResourceArtifact):

    def __init__(self, table, project, endpoint=None, partition=None):
        super(MaxComputeTableArtifact, self).__init__(project=project, endpoint=endpoint)
        self.table = table
        self.partition = partition

    def to_dict(self):
        d = super(MaxComputeTableArtifact, self).to_dict()
        d["location"]["table"] = self.table
        if self.partition:
            d["location"]["partition"] = self.partition
        return d

    @classmethod
    def from_dict(cls, d):
        table = d["location"]["table"]
        project = d["location"].get("project")
        endpoint = d["location"].get("endpoint")
        partition = d["location"].get("partition")
        return cls(table=table, project=project, endpoint=endpoint, partition=partition)


class MaxComputeOfflineModelArtifact(MaxComputeResourceArtifact):

    def __init__(self, offline_model, project, endpoint=None):
        super(MaxComputeOfflineModelArtifact, self).__init__(project=project, endpoint=endpoint)
        self.offline_model = offline_model

    def to_dict(self):
        d = super(MaxComputeOfflineModelArtifact, self).to_dict()
        d["location"]["name"] = self.offline_model
        d["name"] = self.offline_model
        return d

    @classmethod
    def from_dict(cls, d):
        project = d["location"]["project"]
        name = d["location"]["name"]
        endpoint = d["location"].get("endpoint")
        return cls(offline_model=name, project=project, endpoint=endpoint)


class MaxComputeVolumeArtifact(MaxComputeResourceArtifact):

    def __init__(self, volume, project, file_name, endpoint=None, partition=None):
        super(MaxComputeVolumeArtifact, self).__init__(project=project, endpoint=endpoint)
        self.volume = volume
        self.partition = partition
        self.file_name = file_name

    def to_dict(self):
        d = super(MaxComputeVolumeArtifact, self).to_dict()
        d["location"]["volume"] = self.volume
        d["location"]["volumePartition"] = self.partition
        d["location"]["file"] = self.file_name
        return d

    @classmethod
    def from_dict(cls, d):
        endpoint = d["location"].get("endpoint", None)
        project = d["location"]["project"]
        volume = d["location"]["volume"]
        partition = d["location"].get("volumePartition", None)
        file = d["location"].get("file", None)
        return cls(volume=volume, project=project, file_name=file, endpoint=endpoint,
                   partition=partition)


class OSSArtifact(ArtifactValue):

    def __init__(self, bucket, key, endpoint, rolearn):
        super(OSSArtifact, self).__init__()
        self.bucket = bucket
        self.endpoint = endpoint
        self.rolearn = rolearn
        self.key = key

    def to_dict(self):
        d = {
            "location": {
                "endpoint": self.endpoint,
                "bucket": self.bucket,
                "key": self.key,
                "rolearn": self.rolearn,
            }
        }
        return d

    # TODO: OSS Artifact Implementation
    @classmethod
    def from_resource_url(cls):
        pass

    @classmethod
    def from_dict(cls, d):
        if not d["location"].get("bucket"):
            return
        bucket = d["location"]["bucket"]
        key = d["location"]["key"]
        endpoint = d["location"].get("endpoint")
        rolearn = d["location"].get("rolearn")
        return OSSArtifact(bucket=bucket, key=key, endpoint=endpoint, rolearn=rolearn)


class ArtifactDataType(Enum):
    DataSet = "DataSet"
    Model = "Model"
    ModelEvaluation = "ModelEvaluation"


class ArtifactLocationType(Enum):
    MaxComputeTable = "MaxComputeTable"
    MaxComputeVolume = "MaxComputeVolume"
    MaxComputeOfflineModel = "MaxComputeOfflineModel"
    OSS = "OSS"


class ArtifactModelType(Enum):
    OfflineModel = "OfflineModel"
    PMML = "PMML"


class ArtifactEntity(object):
    """Artifact instance, hold the information of metadata and value of artifact."""

    def __init__(self, metadata, value, name, producer, artifact_id):
        """ArtifactEntity class constructor.

        Args:
            metadata (:class:`~.pai.pipeline.artifact.ArtifactMetadata`): Artifact metadata info.
            value (:class:`~.pai.pipeline.artifact.ArtifactValue`): Artifact value.
            name (str): name of artifact, actually, it is the name of artifact in manifest of
                source pipeline.
            producer (str): Producer of the artifact, identified by step name of pipeline.
            artifact_id (str): Unique artifact identifier in pipeline service.
        """
        self.name = name
        self.metadata = metadata
        self.value = value
        self.producer = producer
        self.artifact_id = artifact_id

    def __repr__(self):
        return '%s: {Name:%s, Metadata:%s}' % (type(self).__name__, self.name, self.metadata)

    @classmethod
    def from_run_output(cls, output):
        """ Build new ArtifactInfo instance from Run output json.

        Output Example:

        {'Info':
         {'value':
         '{"location": {"table": "pai_temp_77c08aeb2e514c9d8649feba4a88ee77"}}',
         'metadata': {'path': '/tmp/outputs/artifacts/outputArtifact/data',
          'type': {'DataSet': {'locationType': 'MaxComputeTable'}}}},
          'Name': 'outputArtifact',
          'Producer': 'flow-ec67rsug8kyly4049z',
          'CreateTime': 1595214018000,
          'Type': 'DataSet',
          'Id': 'artifact-e0xdqhsfhqctxkpyli'
        }

        Args:
            output (dict): Run output return by pipeline service.
        Returns:
            ArtifactEntity: ArtifactInfo instance.
        """

        name = output["Name"]
        metadata = ArtifactMetadata.from_dict(output["Info"]["metadata"])
        value = ArtifactValue.from_resource(output["Info"]["value"], metadata=metadata)
        producer = output["Producer"]
        artifact_id = output["Id"]
        return ArtifactEntity(metadata=metadata, value=value, name=name, producer=producer,
                              artifact_id=artifact_id)

    @property
    def is_model(self):
        return self.metadata.data_type == ArtifactDataType.Model
