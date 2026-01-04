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
import json
from dataclasses import dataclass
from typing import List, Optional

from Tea.exceptions import TeaException

from pai.api.lineage import _LineageEntity
from pai.common.logging import get_logger
from pai.common.utils import (
    parse_bmcpfs_uri,
    parse_cpfs_uri,
    parse_local_file_uri,
    parse_nas_uri,
    parse_odps_uri,
    parse_oss_uri,
    parse_pai_dataset_uri,
)
from pai.session import (
    _get_current_region_id,
    _get_dlc_job_id,
    _is_running_in_dlc,
    get_default_session,
)

logger = get_logger(__name__)

# Global default Lineage object used by the program.
_default_lineage = None


@dataclass
class LineageEntity:
    """
    LineageEntity is a class representing lineage entities, including local file paths, datasets, OSS files, NAS files, CPFS, and MaxCompute resources.

    Attributes:
        uri (str): The file URI, supporting the following types:

            - OSS address: Format: oss://<bucket_name>.<region>.<path>, e.g., oss://dlc-upload-test.oss-cn-hangzhou.aliyuncs.com/dataset/
            - Ordinary NAS: Format: nas://<nasfisid>.<region>/subpath/to/dir/, where <nasfisid> represents the NAS file system ID. E.g., nas://fsId-mountTarget.cn-hangzhou.nas.aliyuncs.com/nas/mountTarget/
            - Extreme NAS: Format: nas://<nasfisid>.<region>/subpath/to/dir/, where <nasfisid> represents the NAS file system ID. E.g., nas://007636fd-gfyy.cn-hangzhou.extreme.nas.aliyuncs.com/mnt/foo/
            - CPFS:
                - CPFS1.0 Format: cpfs://<cpfs-fsid>.<region>/subpath/to/dir/, where <cpfs-fsid> is an 8-character ASCII string representing the CPFS file system ID.
                - CPFS2.0 Format: cpfs://<cpfs-fsid>.<region>/<protocolserviceid>/<path>, where <cpfs-fsid> is a 16-character ASCII string representing the CPFS file system ID, and <protocolserviceid> is the protocol service ID. E.g., cpfs://cpfs-00f4b992044a71be.cn-hangzhou/ptc-008727a69e07d3cf/exp-00d695a1b9f6c926/
            - BMCPFS: Format: bmcpfs://<cpfs-fsid>-<cpfs-mountTargetId>.<region>, where <cpfs-fsid> is a 16-character ASCII string representing the CPFS file system ID. E.g.,bmcpfs://cpfs-291070fd9529c747-000001.cn-wulanchabu.cpfs.aliyuncs.com/
            - Local mounted file path: Format: file://<mounted_path>, e.g., file:///mnt/dataset/train.
            - PAI dataset: Format: pai://datasets/<dataset_id>/<dataset_version>, where <dataset_id> is the PAI dataset ID, and <dataset_version> is the PAI dataset version. E.g., pai://datasets/d-f0mniq7j4cgk2x2rrn/v1
            - MaxCompute table: Format: odps://<project_name>/[schema]/tables/<table_name>, where <project_name> is the MaxCompute project name, <schema> is the MaxCompute table schema, optional. (see: https://help.aliyun.com/zh/maxcompute/user-guide/schemas?spm=a2c4g.11186623.0.i64), and <table_name> is the MaxCompute table name. E.g., odps://project_mc/tables/flow_model_label_table_v1
        resource_type (str, optional): The resource type, default as "dataset". Users can customize this. Possible values include:

            - "dataset": Dataset.
            - "model": Model.
            - User-defined types.
        resource_use (str, optional): The resource usage, default as "train". Users can customize this.

            - For "dataset" type, possible values include:
                - "train": Training data.
                - "validation": Validation data.
                - User-defined types.
            - For "model" type, possible values include:
                - "base": Base model.
                - "extension": Extended model.
                - User-defined usages.

    """

    # URI (Uniform Resource Identifier)
    uri: str
    # The resource type, default as "dataset"
    resource_type: Optional[str] = "dataset"
    # The resource usage, default as "train"
    resource_use: Optional[str] = "train"


@dataclass
class _NasDatasourceAttributes:
    file_system_id: str
    path: str


@dataclass
class _PvcDatasourceAttributes:
    cluster_id: str
    name_space: str
    pvc_name: str
    path: str
    pvc_type: str


@dataclass
class _OssDatasourceAttributes:
    uri: str


def _read_metadata_config_in_dlc():
    try:
        with open("/var/metadata/config.json", "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.warning("Error parsing data source JSON or file not found: %s", e)
        return None


def _get_datasource_attributes(source, datasource_type):
    if datasource_type == "nas" or datasource_type == "cpfs":
        return _NasDatasourceAttributes(
            file_system_id=source.get("FileSystemId"), path=source.get("Path")
        )
    if datasource_type == "pvc":
        return _PvcDatasourceAttributes(
            pvc_type=source.get("PvcType"),
            pvc_name=source.get("PvcName"),
            path=source.get("Path"),
            cluster_id=source.get("ClusterId"),
            name_space=source.get("NameSpace"),
        )
    if datasource_type == "oss":
        return _OssDatasourceAttributes(uri=source.get("Uri"))
    return None


def _find_best_match_source(config, mount_path):
    best_match = ""
    best_details = {}

    for source in config.get("DATA_SOURCES", []):
        datasource_type = source.get("DataSourceType")
        mount_path_in_source = source.get("MountPath", "").rstrip("/")

        if mount_path.startswith(mount_path_in_source) and len(
            mount_path_in_source
        ) > len(best_match):
            best_match = mount_path_in_source
            best_details = {
                "datasource_type": datasource_type,
                "datasource_attributes": _get_datasource_attributes(
                    source, datasource_type
                ),
            }

    return best_match, best_details


def _find_datasource_by_mount_path(mount_path: str):
    config = _read_metadata_config_in_dlc()
    if config is None:
        return None, None, None, None

    best_match, best_details = _find_best_match_source(config, mount_path)
    if best_match:
        region_id = config.get("DLC_REGION_ID")
        remaining_path = mount_path[len(best_match) :].lstrip("/")
        return (
            (
                f"{best_details['datasource_attributes'].uri.rstrip('/') + '/'}{remaining_path}"
                if best_details["datasource_type"] == "oss"
                else None
            ),
            region_id,
            (
                best_details["datasource_attributes"]
                if best_details["datasource_type"] == "nas"
                or best_details["datasource_type"] == "cpfs"
                else None
            ),
            (
                best_details["datasource_attributes"]
                if best_details["datasource_type"] == "pvc"
                else None
            ),
        )
    return None, None, None, None


def _fill_lineage_entity(entity: LineageEntity) -> _LineageEntity:
    input_uri = entity.uri
    local_file_path = parse_local_file_uri(input_uri)
    if local_file_path:
        (
            uri,
            region_id,
            nas_entity_attributes,
            pvc_entity_attributes,
        ) = _find_datasource_by_mount_path(local_file_path)
        if nas_entity_attributes:
            _entity = _LineageEntity()
            _entity.EntityType = "nas-file"
            _entity.Attributes = {
                "Uri": uri,
                "ResourceType": entity.resource_type,
                "ResourceUse": entity.resource_use,
                "RegionId": region_id,
                "FileSystemId": nas_entity_attributes.file_system_id,
                "Path": nas_entity_attributes.path,
            }
            return _entity
        if pvc_entity_attributes:
            _entity = _LineageEntity()
            _entity.EntityType = "pvc-file"
            _entity.Attributes = {
                "ResourceType": entity.resource_type,
                "ResourceUse": entity.resource_use,
                "RegionId": region_id,
                "ClusterId": pvc_entity_attributes.cluster_id,
                "NameSpace": pvc_entity_attributes.name_space,
                "PvcName": pvc_entity_attributes.pvc_name,
                "Path": pvc_entity_attributes.path,
                "PvcType": pvc_entity_attributes.pvc_type,
            }
            return _entity
        if uri:
            input_uri = uri
        else:
            logger.warning(f"can not find uri by mount path: {local_file_path}")
    parsed_result = parse_oss_uri(input_uri)
    if parsed_result:
        bucket_name, region_id, path = parsed_result
        _entity = _LineageEntity()
        _entity.EntityType = "oss-file"
        _entity.Attributes = {
            "Bucket": bucket_name,
            "Path": path,
            "ResourceType": entity.resource_type,
            "ResourceUse": entity.resource_use,
            "RegionId": region_id,
        }
        return _entity
    parsed_result = parse_pai_dataset_uri(input_uri)
    if parsed_result:
        dataset_id, dataset_version = parsed_result
        try:
            dataset_detail = get_default_session().dataset_api.get(dataset_id)
            if dataset_detail:
                _entity = _LineageEntity()
                if dataset_detail.get("Provider") == "pai":
                    _entity.QualifiedName = (
                        f"pai-dataset.{dataset_id}_{dataset_version}".format(
                            dataset_id=dataset_id, dataset_version=dataset_version
                        )
                    )
                    _entity.Name = dataset_detail["Name"]
                    _entity.Attributes = {
                        "ResourceUse": entity.resource_use,
                        "Provider": "pai",
                    }
                    return _entity
                else:
                    _entity.QualifiedName = (
                        f"pai-dataset.{dataset_id}_{dataset_version}".format(
                            dataset_id=dataset_id, dataset_version=dataset_version
                        )
                    )
                    _entity.Name = dataset_detail["Name"]
                    _entity.Attributes = {
                        "ResourceType": entity.resource_type,
                        "ResourceUse": entity.resource_use,
                        "RegionId": _get_current_region_id(),
                        "Uri": dataset_detail["Uri"],
                        "VersionName": dataset_version,
                    }
                    return _entity
        except TeaException as e:
            logger.warning(
                f"can not find dataset by dataset_id: {dataset_id}, {str(e)}"
            )
    parsed_result = parse_odps_uri(input_uri)
    if parsed_result:
        project_name, schema, table_name = parsed_result
        _entity = _LineageEntity()
        if schema:
            _entity.QualifiedName = (
                f"maxcompute-table.{project_name}.{schema}.{table_name}".format(
                    project_name=project_name, schema=schema, table_name=table_name
                )
            )
        else:
            _entity.QualifiedName = (
                f"maxcompute-table.{project_name}.{table_name}".format(
                    project_name=project_name, table_name=table_name
                )
            )
        _entity.Attributes = {
            "ResourceType": entity.resource_type,
            "ResourceUse": entity.resource_use,
        }
        return _entity
    return None


class Lineage(object):
    def __init__(self):
        super()

    def log_lineage(
        self, input_entities: List[LineageEntity], output_entities: List[LineageEntity]
    ):
        """
        Recommended to use the log_lineage(input_entities: List[LineageEntity], output_entities: List[LineageEntity])
        function directly.
        """
        session = get_default_session()
        if _is_running_in_dlc():
            _input_entities = []
            _output_entities = []
            for input_entity in input_entities:
                entity = _fill_lineage_entity(input_entity)
                if entity:
                    _input_entities.append(entity)
            for output_entity in output_entities:
                entity = _fill_lineage_entity(output_entity)
                if entity:
                    _output_entities.append(entity)
            if len(_input_entities) == 0 or len(_output_entities) == 0:
                logger.warning("input_entities or output_entities is empty, ignore.")
            else:
                session.lineage_api.log_lineage(
                    _input_entities,
                    _output_entities,
                    _get_dlc_job_id(),
                    session.workspace_id,
                )
                logger.debug(_input_entities)
                logger.debug(_output_entities)
                logger.debug(_get_dlc_job_id())
                logger.debug(session.workspace_id)
        else:
            logger.warning("log_lineage is not supported in non-DLC environment.")


def log_lineage(
    input_entities: List[LineageEntity], output_entities: List[LineageEntity]
):
    """
    Records the lineage relationships generated during model training/data processing, etc. Supported execution
    environments include: DLC. If running in other environments, lineage recording will be ignored.

    Args:
        input_entities (List[LineageEntity]): A list of input entities, each representing the source of data in DLC tasks.
        output_entities (List[LineageEntity]): A list of output entities, each representing the output of data in DLC tasks.
    """
    global _default_lineage
    if not _default_lineage:
        _default_lineage = Lineage()

    _default_lineage.log_lineage(input_entities, output_entities)
