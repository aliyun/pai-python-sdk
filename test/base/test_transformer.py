from __future__ import absolute_import

from pai import ProviderAlibabaPAI
from pai.job import JobStatus
from pai.pipeline import Pipeline
from test import BaseTestCase


class TestTransformer(BaseTestCase):

    def init_base_transformer(self):
        identifier = "dataSource-xflow-maxCompute"
        version = "v1"
        provider = ProviderAlibabaPAI

        p = Pipeline.get_by_identifier(session=self.session, identifier=identifier,
                                       provider=provider, version=version)
        parameters = {
            "__XFlow_project": "algo_public",
            "__XFlow_execution": {
                # "odpsInfoFile": "/share/base/odpsInfo.ini",
                "endpoint": "http://service.cn-shanghai.maxcompute.aliyun.com/api",
                "logViewHost": "http://logview.odps.aliyun.com",
                "odpsProject": "wyl_test",
            },
        }
        transformer = p.to_transformer(parameters=parameters)
        return p, transformer

    def init_composite_transformer(self):
        pass

    def test_transformer_init(self):
        p, transformer = self.init_base_transformer()
        self.assertEqual(p.identifier, transformer.get_identifier())
        self.assertEqual(p.version, transformer.get_version())
        self.assertEqual(p.pipeline_id, transformer.get_pipeline_id())
        self.assertEqual(p.provider, transformer.get_provider())

    def test_base_transformer_sync_run(self):
        _, transformer = self.init_base_transformer()

        run_args = {
            "tableName": "pai_online_project.wumai_data",
        }

        job = transformer.transform(wait=True, job_name="test_transform_job", args=run_args)
        self.assertEqual(JobStatus.Succeeded, job.get_status())

    def test_base_transformer_async_run(self):
        _, transformer = self.init_base_transformer()
        run_args = {
            "tableName": "pai_online_project.wumai_data",
        }
        job = transformer.transform(wait=False, job_name="test_transform_job", args=run_args)
        self.assertEqual(JobStatus.Running, job.get_status())
        job.attach()
        self.assertEqual(JobStatus.Succeeded, job.get_status())

    def test_multiple_call_transform(self):
        _, transformer = self.init_base_transformer()
        run_args = {
            "tableName": "pai_online_project.wumai_data",
        }
        job1 = transformer.transform(wait=False, job_name="test_transform_job", args=run_args)
        self.assertEqual(transformer.last_job, job1)
        job2 = transformer.transform(wait=False, job_name="test_transform_job", args=run_args)
        self.assertEqual(transformer.last_job, job2)
        self.assertNotEqual(job1, job2)

