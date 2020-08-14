from __future__ import absolute_import

from pai.common import ProviderAlibabaPAI
from pai.job import JobStatus
from pai.pipeline.template import PipelineTemplate
from tests import BaseTestCase


class TestTransformer(BaseTestCase):

    @classmethod
    def init_base_transformer(cls):
        identifier = "dataSource-xflow-maxCompute"
        version = "v1"
        provider = ProviderAlibabaPAI

        p = PipelineTemplate.get_by_identifier(identifier=identifier,
                                               provider=provider, version=version)
        parameters = {
            "project": cls.default_xflow_project,
            "execution": cls.get_default_xflow_execution(),
        }
        transformer = p.to_transformer(parameters=parameters)
        return p, transformer

    def test_transformer_init(self):
        p, transformer = self.init_base_transformer()
        self.assertEqual(p.identifier, transformer.identifier)
        self.assertEqual(p.version, transformer.version)
        self.assertEqual(p.pipeline_id, transformer.pipeline_id)
        self.assertEqual(p.provider, transformer.provider)

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
