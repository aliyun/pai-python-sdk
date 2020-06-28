import os
import time
import unittest

from six.moves import configparser

from pai.pipeline import Pipeline
from pai.session import Session
from tests import BaseTestCase

_test_root = os.path.dirname(os.path.abspath(__file__))


class TestPaiFlowAPI(BaseTestCase):

    def setUp(self):
        super(TestPaiFlowAPI, self).setUp()
        self.session = self.get_test_session()

    def tearDown(self):
        pass

    @classmethod
    def get_test_session(cls):
        configs = cls.get_test_config()
        return Session(**configs)

    @classmethod
    def get_test_config(cls):
        cfg_parser = configparser.ConfigParser()
        cfg_parser.read(os.path.join(_test_root, "..", "test.conf"))
        access_key = cfg_parser.get("test", "access_key")
        access_secret = cfg_parser.get("test", "access_secret")
        region = cfg_parser.get("test", "region")

        return {
            "region_id": region,
            "access_key": access_key,
            "access_secret": access_secret
        }

    def test_pipeline_create(self):
        resp = self.session.list_pipeline()
        pass

    @staticmethod
    def data_source_pipeline_arguments_env():
        arguments = {"parameters": {
            "__execution": {
                "accessId": "AccessKeyId",
                "accessKey": "3AccessKeySecret",
                "logViewHost": "http://logview.odps.aliyun.com/",
                "endpoint": "http://service.cn-shanghai.maxcompute.aliyun.com/api",
                "odpsProject": "wyl_test",
                "userId": 15577,
            },
            "tableName": "pai_online_project.wumai_data",
        }},
        env = {
            "workflowService": {
                "name": "argo",
                "config": {
                    "endpoint": "http://service.cn-shanghai.argo.aliyun.com/"
                }
            },
            "resource": {
                "compute": {
                    "max_compute": {
                        "accessId": "AccessKeyId",
                        "accessKey": "3AccessKeySecret",
                        "logViewHost": "http://logview.odps.aliyun.com/",
                        "endpoint": "http://service.cn-shanghai.maxcompute.aliyun.com/api",
                        "odpsProject": "wyl_test",
                        "userId": 15577,
                    }
                }

            }
        }
        return arguments, env

    def test_pipeline_run(self):
        run_name_suffix = str(int(time.time()))
        pipeline_info = self.session.get_pipeline("odps-data-source", "1557702098194904", version="v1")
        manifest = pipeline_info["Manifest"].encode("utf-8")

        arguments, env = self.data_source_pipeline_arguments_env()

        run_id = self.session.create_pipeline_run("unittest_odps_data_source_test_1_%s" % run_name_suffix,
                                                  manifest=manifest,
                                                  arguments=arguments,
                                                  no_confirm_required=True, env=env)
        self.assertIsNotNone(run_id)

        pipeline = Pipeline.load_by_manifest(manifest)
        run_id = pipeline.run("unittest_odps_data_source_test_2_%s" % run_name_suffix, arguments=arguments, env=env)
        self.assertIsNotNone(run_id)

    def test_composite_pipeline_run(self):
        pass

    def test_run_status_manager(self):
        pass


if __name__ == "__main__":
    unittest.main()
