# coding: utf-8

import os

import yaml

from pai.core.session import EnvType
from tests.test_data import OPERATOR_MANIFEST_DIR


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
    def env_type(self):
        return EnvType.PublicCloud

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
