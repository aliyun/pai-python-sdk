# coding: utf-8

from oss2.exceptions import NotFound


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
        return "mock_region"

    @property
    def oss_bucket(self):
        return MockOssBucket()


def get_mock_session():
    return MockSession()
