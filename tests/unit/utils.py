# coding: utf-8

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

import hashlib
import os
import re

import mock
import six
import yaml

from tests.test_data import OPERATOR_MANIFEST_DIR

ODPS_TABLE_RE = (
    r"odps://(?P<project>[^/]+)/tables/(?P<table_name>[^/]+)(?P<partition>.*)"
)


def load_operator_manifest():
    file_names = os.listdir(OPERATOR_MANIFEST_DIR)
    manifests = []
    for name in file_names:
        with open(os.path.join(OPERATOR_MANIFEST_DIR, name), "r") as f:
            raw = f.read()
            manifest = yaml.load(raw, yaml.FullLoader)
            manifests.append(manifest)
    return manifests


class MockOssBucket(object):
    def put_object_from_file(self, key, filename, headers=None, progress_callback=None):
        return "mock_put_result"

    @property
    def bucket_name(self):
        return "mock_bucket"

    def head_object(self, key, headers=None, params=None):
        return True

    @property
    def endpoint(self):
        return "mock_oss_endpoint"


class MockSession(object):
    @property
    def provider(self):
        return "mock_provider"

    @property
    def region_id(self):
        return "cn-hangzhou"

    @property
    def is_inner(self):
        return True

    @property
    def oss_bucket(self):
        return MockOssBucket()

    def get_pipeline(self, identifier, provider=None, version="v1"):
        manifest, uuid = self._load(
            identifier=identifier, provider=provider, version=version
        )
        if not manifest:
            raise ValueError(
                "Manifest not found: %s, %s, %s" % (identifier, provider, version)
            )
        data = {
            "Manifest": manifest,
            "PipelineId": uuid,
            "WorkspaceId": "MockWorkspaceId",
        }
        return data

    @classmethod
    def _load(cls, identifier, provider, version):
        manifests = load_operator_manifest()
        for manifest in manifests:
            metadata = manifest["metadata"]
            uuid = metadata["uuid"]
            if (
                metadata["identifier"] == identifier
                and metadata["provider"] == provider
                and metadata["version"] == version
            ):
                return manifest, uuid
        return None, None

    @property
    def _is_inner(self):
        return False


def get_mock_session():
    return MockSession()


def _extract_odps_table_info_from_url(resource):
    matches = re.match(ODPS_TABLE_RE, resource)
    if not matches:
        raise ValueError("Not support ODPSTable resource schema.")

    project, table, partition = (
        matches.group("project"),
        matches.group("table_name"),
        matches.group("partition").strip("/"),
    )
    return project, table, partition


def extract_odps_table_info(data):
    from odps import DataFrame as ODPSDataFrame
    from odps.models import Table
    from odps.models.partition import Partition

    if isinstance(data, ODPSDataFrame):
        data = data.data

    if isinstance(data, Table):
        return "%s.%s" % (data.project.name, data.name), None
    elif isinstance(data, Partition):
        return "%s.%s" % (data.table.project.name, data.table.name), data.spec
    elif isinstance(data, six.string_types):
        return _extract_odps_table_info_from_url(data)
    else:
        raise ValueError("Not support ODPSTable input(type:%s)" % type(data))


def file_checksum(file_name, hash_type="md5"):
    if hash_type.lower() != "md5":
        raise ValueError("not support hash type")

    hash_md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(256 * 1024), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def mock_env(**kwargs):
    """Decorator to set environment variables for a test function."""
    return mock.patch.dict(os.environ, kwargs)
