from __future__ import absolute_import

import json
import re

import six
from odps.df import DataFrame as ODPSDataFrame
from odps.models import (
    Table as ODPSTable,
    Partition as ODPSPartition,
    Volume as ODPSVolume,
)
from odps.models.ml.offlinemodel import OfflineModel as ODPSOfflineModel

from pai.pipeline.types.variable import PipelineVariable


class DataType(object):
    DataSet = "DataSet"
    Model = "Model"
    ModelEvaluation = "ModelEvaluation"


class LocationType(object):
    MaxComputeTable = "MaxComputeTable"
    MaxComputeVolume = "MaxComputeVolume"
    MaxComputeOfflineModel = "MaxComputeOfflineModel"
    OSS = "OSS"


class ModelType(object):
    OfflineModel = "OfflineModel"
    PMML = "PMML"


class PipelineArtifact(PipelineVariable):
    variable_category = "artifacts"

    def __init__(
        self,
        name,
        metadata=None,
        path=None,
        desc=None,
        io_type="inputs",
        value=None,
        from_=None,
        required=None,
        parent=None,
    ):
        super(PipelineArtifact, self).__init__(
            name=name,
            desc=desc,
            io_type=io_type,
            value=value,
            from_=from_,
            required=required,
            parent=parent,
        )
        self.metadata = metadata
        self.path = path

    def validate_from(self, arg):
        if not isinstance(arg, PipelineArtifact):
            raise ValueError(
                "arg is expected to be type of 'PipelineParameter' "
                "but was actually of type '%s'" % type(arg)
            )

        if (
            arg.metadata is not None
            and self.metadata is not None
            and arg.metadata != self.metadata
        ):
            return False

        return True

    # TODO: Artifact value validation
    def validate_value(self, val):
        return True

    @classmethod
    def to_argument_by_spec(cls, val, af_spec, io_type="inputs"):
        af_spec = af_spec.copy()

        name = af_spec.pop("name")
        metadata = LocationArtifactMetadata.from_dict(af_spec.pop("metadata", None))
        desc = af_spec.pop("desc", None)
        from_ = af_spec.pop("from", None)
        required = af_spec.pop("required", None)

        param = PipelineArtifact(
            name=name,
            metadata=metadata,
            io_type=io_type,
            from_=from_,
            required=required,
            desc=desc,
        )
        af_value = LocationArtifactValue.from_resource(val)
        if not param.validate_value(val):
            raise ValueError(
                "Not Validate value for Parameter %s, value(%s:%s)"
                % (name, type(val), val)
            )
        param.value = af_value
        return param.to_argument()

    def to_argument(self):
        arguments = {"name": self.name}

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
            if isinstance(self.value, LocationArtifactValue):
                d["value"] = self.value.to_dict()
            else:
                d["value"] = self.value
        if self.path is not None:
            d["path"] = self.path
        return d


class LocationArtifactMetadata(object):
    def __init__(self, data_type, location_type, type_attributes=None):
        self.data_type = data_type
        self.location_type = location_type
        self.type_attributes = type_attributes or dict()

    def __str__(self):
        return "%s:data_type=%s:location_type=%s" % (
            type(self).__name__,
            self.data_type,
            self.location_type,
        )

    def to_dict(self):
        d = {
            "type": {
                self.data_type: {
                    "locationType": self.location_type,
                }
            }
        }

        d["type"][self.data_type].update(self.type_attributes)

        return d

    @property
    def value(self):
        return self.to_dict()

    def __eq__(self, other):
        if isinstance(other, LocationArtifactMetadata):
            return (
                self.data_type == other.data_type
                and self.location_type == other.location_type
                and self.type_attributes == other.type_attributes
            )
        elif isinstance(other, dict):
            other = self.from_dict(other)
            return self.__eq__(other)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def from_dict(cls, d):
        af_typ = d["type"]
        data_type = list(af_typ.keys())[0]
        type_attributes = af_typ[data_type].copy()
        location_type = type_attributes.pop("locationType", None)
        return cls(
            data_type=data_type,
            location_type=location_type,
            type_attributes=type_attributes,
        )


class LocationArtifactValue(object):
    def __init__(self):
        pass

    @classmethod
    def from_resource(cls, resource, metadata=None):
        from pai.core.artifact import ArchivedArtifact

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
        elif isinstance(
            resource, (ODPSTable, ODPSPartition, ODPSDataFrame, ODPSVolume)
        ):
            return MaxComputeResourceArtifact.from_odps_resource(resource)
        elif isinstance(resource, ArchivedArtifact):
            return resource.value
        elif isinstance(resource, LocationArtifactValue):
            return resource

        raise ValueError("Not support artifact resource:%s", type(resource))

    @classmethod
    def from_raw_value(cls, value, metadata):
        if metadata is None:
            raise ValueError(
                400,
                "ArtifactMetadata should provide while parse artifact value from dict data.",
            )
        if metadata.location_type == LocationType.OSS:
            return OSSArtifact.from_dict(value)
        elif metadata.location_type == LocationType.MaxComputeTable:
            return MaxComputeTableArtifact.from_dict(value)
        elif metadata.location_type == LocationType.MaxComputeOfflineModel:
            return MaxComputeOfflineModelArtifact.from_dict(value)
        elif metadata.location_type == LocationType.MaxComputeVolume:
            return MaxComputeVolumeArtifact.from_dict(value)
        else:
            raise ValueError(
                "Not support artifact location_type: %s", metadata.location_type
            )

    @classmethod
    def get_param_ref(cls, param):
        from pai.pipeline import PipelineParameter

        if not param:
            return

        elif isinstance(param, PipelineParameter):
            ref = param.enclosed_fullname
        elif isinstance(param, six.string_types):
            ref = "{{inputs.parameters.%s}}" % param
        else:
            raise ValueError(
                "expect PipelineParameter or string, but given %s", type(param)
            )
        return ref


class MaxComputeResourceArtifact(LocationArtifactValue):
    MaxComputeResourceUrlPattern = re.compile(
        r"odps://(?P<project>[^/]+)/(?P<resource_type>(?:tables)|(?:volumes)|(?:offlinemodels))/"
        r"(?P<resource_name>[^/]+)/?(?P<sub_resource>[^\?]+)?(?P<arguments>[.*])?"
    )

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
            table = matches.group("resource_name")
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
            file_name = sub_resource[idx + 1 :]
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
        if not isinstance(
            resource, (ODPSTable, ODPSPartition, ODPSDataFrame, ODPSVolume)
        ):
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
            partition = ",".join(
                ["%s=%s" % (k, v) for k, v in resource.partition_spec.kv.items()]
            )
            return MaxComputeTableArtifact(
                project=project, partition=partition, table=table
            )
        elif isinstance(resource, ODPSOfflineModel):
            project = resource.project.name
            offlinemodel = resource.name
            return MaxComputeOfflineModelArtifact(
                project=project, offline_model=offlinemodel
            )
        # TODO: ODPSVolume Support
        elif isinstance(resource, ODPSVolume):
            pass


class MaxComputeTableArtifact(MaxComputeResourceArtifact):
    def __init__(self, table, project, endpoint=None, partition=None):
        super(MaxComputeTableArtifact, self).__init__(
            project=project, endpoint=endpoint
        )
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

    @classmethod
    def value_from_param(cls, table_name, partition=None):
        table_ref = cls.get_param_ref(table_name)
        partition_ref = cls.get_param_ref(partition)
        if not table_ref:
            raise ValueError("MaxComputeTableArtifact require table not be None")
        d = {
            "location": {
                "table": table_ref,
            }
        }

        if partition_ref is not None:
            d["location"]["partition"] = partition_ref
        return json.dumps(d)


class MaxComputeOfflineModelArtifact(MaxComputeResourceArtifact):
    def __init__(self, offline_model, project, endpoint=None):
        super(MaxComputeOfflineModelArtifact, self).__init__(
            project=project, endpoint=endpoint
        )
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
        super(MaxComputeVolumeArtifact, self).__init__(
            project=project, endpoint=endpoint
        )
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
        return cls(
            volume=volume,
            project=project,
            file_name=file,
            endpoint=endpoint,
            partition=partition,
        )


class OSSArtifact(LocationArtifactValue):
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
