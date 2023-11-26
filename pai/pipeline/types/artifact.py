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

from __future__ import absolute_import

import json
import re
from abc import ABCMeta, abstractmethod

import six
from odps.df import DataFrame as ODPSDataFrame
from odps.models import Partition as ODPSPartition
from odps.models import Table as ODPSTable
from odps.models import Volume as ODPSVolume
from odps.models.ml.offlinemodel import OfflineModel as ODPSOfflineModel
from six import with_metaclass

from pai.common.oss_utils import OssUriObj
from pai.common.utils import is_iterable
from pai.pipeline.types.variable import PipelineVariable


class ArtifactMetadataUtils(object):
    """Util class using for create artifact metadata."""

    @staticmethod
    def maxc_table():
        """Return metadata represent a MaxComputeTable."""
        return LocationArtifactMetadata(
            data_type=DataType.DataSet,
            location_type=LocationType.MaxComputeTable,
        )

    @staticmethod
    def oss_dataset():
        return LocationArtifactMetadata(
            data_type=DataType.DataSet, location_type=LocationType.OSS
        )

    @staticmethod
    def maxc_offlinemodel():
        return LocationArtifactMetadata(
            data_type=DataType.Model, location_type=LocationType.MaxComputeOfflineModel
        )

    @staticmethod
    def maxc_volume():
        return LocationArtifactMetadata(
            data_type=DataType.DataSet, location_type=LocationType.MaxComputeVolume
        )

    @staticmethod
    def raw():
        return LocationArtifactMetadata(data_type=DataType.Any)


class DataType(object):
    DataSet = "DataSet"
    Model = "Model"
    Any = "Any"
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
    """Input/output artifact definition of the Pipeline and operator.

    Examples:

        from pai.operator.types import MetadataBuilder, PipelineArtifact
        from pai.operator import ContainerOperator

        op = ContainerOperator(
            image_uri="python:3",
            inputs=[
                PipelineArtifact(name="foo", metadata=MetadataBuilder.to_dict()),
            ]

        )
        pass

    """

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
        required=False,
        repeated=False,
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
        self.repeated = repeated
        self._count = None

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        if not self.repeated:
            raise ValueError("no repeated artifact do not has count attribute.")

        if not isinstance(value, six.integer_types) or value <= 0:
            raise ValueError("invalid count for repeated artifact:%s" % value)

        self._count = value

    def reset_count(self):
        self._count = None

    def validate_from(self, arg):
        if isinstance(arg, PipelineArtifact):
            source = arg
            if source.repeated and not source.parent:
                raise ValueError("repeated artifact could not assign entirely.")
        elif isinstance(arg, PipelineArtifactElement):
            source = arg.artifact
        else:
            raise ValueError(
                "arg is expected to be type of 'PipelineParameter' "
                "but was actually of type '%s'" % type(arg)
            )

        if (
            source.metadata is not None
            and self.metadata is not None
            and source.metadata != self.metadata
        ):
            return False
        return True

    def assign(self, arg):
        def _validate(item):
            if isinstance(
                item, (PipelineArtifact, PipelineArtifactElement)
            ) and not self.validate_from(item):
                raise ValueError(
                    "invalid assignment. %s left: %s, right: %s"
                    % (self.fullname, self, arg)
                )
            elif not isinstance(
                item, (PipelineArtifact, PipelineArtifactElement)
            ) and not self.validate_value(item):
                raise ValueError("Value(%s) is invalid value for %s" % (item, self))

        if self.repeated:
            if is_iterable(arg):
                value = [item for item in arg]
            else:
                value = [arg]
            for item in value:
                _validate(item)

            self.value = value
        else:
            _validate(arg)
            if isinstance(arg, (PipelineArtifact, PipelineArtifactElement)):
                self.from_ = arg
            else:
                # We need to transform artifact input value input to standard artifact value
                # which PAIFlow service recognized.
                self.value = self._translate_value(arg)["value"]

    def __getitem__(self, key):
        if not self.repeated:
            raise KeyError("no repeated artifact is not indexable.")

        if isinstance(key, six.integer_types):
            return PipelineArtifactElement(self, key)
        elif isinstance(key, slice):
            if key.stop is None:
                raise ValueError(
                    "slice of repeated artifact should have stop property."
                )
            start, stop, step = key.indices(key.stop)
            indexes = range(stop)[start:stop:step]
            return [
                PipelineArtifactElement(artifact=self, index=idx) for idx in indexes
            ]

        raise KeyError("please provide integer to index the artifact element.")

    # TODO: Artifact value validation
    def validate_value(self, val):
        return True

    def normalized_name(self, index):
        return "%s_%s" % (self.name, index)

    def depend_steps(self):
        def _depend_step(value):
            if isinstance(value, PipelineArtifact) and value.parent:
                return value.parent
            elif isinstance(value, PipelineArtifactElement) and value.artifact.parent:
                return value.artifact.parent

        if self.from_:
            return filter(None, [_depend_step(self.from_)])
        elif self.repeated and self.value:
            return filter(None, [_depend_step(item) for item in self.value])

    def translate_argument(self, arg):
        argument = {"name": self.name}
        if self.repeated:
            arg_list = arg if isinstance(arg, list) else [arg]
            results = [
                {"name": self.normalized_name(idx), "value": self._translate_value(v)}
                for idx, v in enumerate(arg_list)
            ]
            argument["value"] = results
        else:
            art_value = self._translate_value(arg)
            argument["value"] = art_value["value"]
            argument["metadata"] = art_value["metadata"]

        return argument

    def _translate_value(self, val):
        if isinstance(self.metadata, ArtifactMetadataBase):
            md_val = self.metadata.to_dict()
        else:
            md_val = self.metadata

        try:
            af_value = LocationArtifactValue.from_resource(val)
            value = json.dumps(af_value.to_dict(), sort_keys=True)
        except ValueError:
            value = val

        if (
            isinstance(self.metadata, LocationArtifactMetadata)
            and self.metadata.is_raw()
        ):
            metadata = LocationArtifactValue.metadata_from_value(val)
            if metadata:
                md_val = metadata.to_dict()

        return {
            "value": value,
            "metadata": md_val,
        }

    def to_argument(self):
        argument = {"name": self.name}
        if self.repeated:
            values = []
            for idx, item in enumerate(self.value):
                if isinstance(item, (PipelineArtifact, PipelineArtifactElement)):
                    values.append(
                        {
                            "name": self.normalized_name(idx),
                            "from": item.enclosed_fullname,
                        }
                    )
                else:
                    values.append(
                        {
                            "name": self.normalized_name(idx),
                            "value": None,
                        }
                    )
            argument["value"] = values
        elif self.from_:
            argument["from"] = self.from_.enclosed_fullname
        else:
            argument["value"] = self.value
        return argument

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
        d["required"] = self.required
        if self.repeated:
            d["repeated"] = self.repeated
        return d


class PipelineArtifactElement(object):
    def __init__(self, artifact, index):
        self.artifact = artifact
        self.index = index
        self._from = None
        self._value = None

    @property
    def name(self):
        return "%s_%s" % (self.artifact.name, self.index)

    @property
    def fullname(self):
        return ".".join(
            [
                self.artifact.parent.ref_name,
                self.artifact.io_type,
                self.artifact.variable_category,
                self.name,
            ]
        )

    @property
    def enclosed_fullname(self):
        return "{{%s}}" % self.fullname

    @property
    def parent(self):
        return self.artifact.parent


class ArtifactMetadataBase(with_metaclass(ABCMeta)):
    @abstractmethod
    def to_dict(self):
        pass


class LocationArtifactMetadata(ArtifactMetadataBase):
    def __init__(self, data_type, location_type=None, type_attributes=None):
        self.data_type = data_type
        self.location_type = location_type
        self.type_attributes = type_attributes or dict()

    def __str__(self):
        return "%s:data_type=%s:location_type=%s" % (
            type(self).__name__,
            self.data_type,
            self.location_type,
        )

    def is_raw(self):
        return self.data_type == DataType.Any and self.location_type is None

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
        if self.data_type == DataType.Any:
            return True
        elif isinstance(other, LocationArtifactMetadata):
            return other.data_type == DataType.Any or (
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
        """Get artifact value from input resource and artifact metadata.

        Args:
            resource: Input resource which can be ODPS url, OSS url, PyODPS table object, etc.
            metadata: Metadata for the input artifact.

        Returns:
            LocationArtifactValue: A artifact value parsed from input resource.

        """
        from pai.pipeline.artifact import ArchivedArtifact

        if isinstance(resource, six.string_types):
            if resource.startswith("odps://"):
                val, _ = MaxComputeResourceArtifact.from_resource_url(resource)
                return val
            elif resource.startswith("oss://"):
                val, _ = OSSArtifact.from_resource_url(resource)
                return val
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

        raise ValueError("Not supported artifact resource:%s", type(resource))

    @classmethod
    def metadata_from_value(cls, resource):
        """Try to get metadata from raw input for the artifact.

        Args:
            resource: Input for the artifact.

        Returns:
            (ArtifactMetadataBase): Metadata for the input artifact value.

        """
        from pai.pipeline.artifact import ArchivedArtifact

        if isinstance(resource, six.string_types):
            if resource.startswith("odps://"):
                _, metadata = MaxComputeResourceArtifact.from_resource_url(resource)
            elif resource.startswith("oss://"):
                _, metadata = OSSArtifact.from_resource_url(resource)
            else:
                return None
        elif isinstance(resource, (ODPSTable, ODPSPartition, ODPSDataFrame)):
            metadata = ArtifactMetadataUtils.maxc_table()
        elif isinstance(resource, ArchivedArtifact):
            try:
                metadata = LocationArtifactMetadata.from_dict(resource.metadata)
            except (KeyError, ValueError):
                return None
        else:
            return None
        return metadata

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
        from pai.pipeline.types import PipelineParameter

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

    def to_dict(self):
        pass


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
        """Parse MaxCompute(ODPS) resource in url schema and returns artifact value and metadata.

        Args:
            resource_url: An ODPS(MaxCompute) table, tablePartition, offline-model or volume in url schema.

        Returns:
            tuple: A tuple of  MaxCompute artifact value and artifact metadata.

        """
        matches = cls.MaxComputeResourceUrlPattern.match(resource_url)
        if not matches:
            raise ValueError("Not support MaxCompute resource url format.")
        resource_type = matches.group("resource_type")
        project = matches.group("project")
        if resource_type == "tables":
            table = matches.group("resource_name")
            partition = matches.group("sub_resource")
            return (
                MaxComputeTableArtifact(
                    project=project,
                    table=table,
                    partition=partition.strip("/") if partition else None,
                ),
                ArtifactMetadataUtils.maxc_table(),
            )
        elif resource_type == "volumes":
            volume = matches.group("resource_name")
            sub_resource = matches.group("sub_resource").strip("/")
            idx = sub_resource.find("/")
            partition = sub_resource[:idx]
            file_name = sub_resource[idx + 1 :]
            return (
                MaxComputeVolumeArtifact(
                    project=project,
                    volume=volume,
                    partition=partition,
                    file_name=file_name,
                ),
                ArtifactMetadataUtils.maxc_volume(),
            )

        elif resource_type == "offlinemodels":
            name = matches.group("resource_name")
            return (
                MaxComputeOfflineModelArtifact(
                    project=project,
                    offline_model=name,
                ),
                ArtifactMetadataUtils.maxc_offlinemodel(),
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
    """OSSArtifact instance represent a OSS artifact value."""

    def __init__(self, bucket, key, endpoint, role_arn=None):
        """

        Args:
            bucket: OSS bucket name.
            key: OSS object key.
            endpoint: Endpoint for the OSS bucket.
            role_arn: RoleArn used for OSS access.
        """
        super(OSSArtifact, self).__init__()
        self.bucket = bucket
        self.endpoint = endpoint
        self.role_arn = role_arn
        self.key = key

    def to_dict(self):
        d = {
            "location": {
                "endpoint": self.endpoint,
                "bucket": self.bucket,
                "key": self.key,
            }
        }

        if self.role_arn:
            d["location"]["rolearn"] = self.role_arn

        return d

    @classmethod
    def from_resource_url(cls, resource):
        """Initialize a OSSArtifact instance from URL in OSS schema.
        Args:
            resource: URL in OSS schema.
        Returns:
            OSSArtifact instance.
        """
        bucket_name, object_key, endpoint, role_arn = OssUriObj.parse(resource)
        return (
            cls(
                bucket=bucket_name, key=object_key, endpoint=endpoint, role_arn=role_arn
            ),
            ArtifactMetadataUtils.oss_dataset(),
        )

    @classmethod
    def from_dict(cls, d):
        if not d["location"].get("bucket"):
            return
        bucket = d["location"]["bucket"]
        key = d["location"]["key"]
        endpoint = d["location"].get("endpoint")
        rolearn = d["location"].get("rolearn")
        return OSSArtifact(bucket=bucket, key=key, endpoint=endpoint, role_arn=rolearn)
