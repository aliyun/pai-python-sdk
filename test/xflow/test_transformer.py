from __future__ import absolute_import

from pai.job import JobStatus
from pai.xflow.transformer import XFlowOfflineModelTransformer, ODPSDataSource

from test import BaseTestCase


class TestTransformer(BaseTestCase):

    # Train offline model
    @classmethod
    def setUpClass(cls):
        super(TestTransformer, cls).setUpClass()

    # TODO: wait for artifact value format
    @classmethod
    def prepare_offline_model(cls):
        pass

    # remove useless offline model
    @classmethod
    def tearDownClass(cls):
        super(TestTransformer, cls).tearDownClass()

    def testXFlowOfflineModel(self):
        offline_model = XFlowOfflineModelTransformer(
            session=self.session,
            model=self.model
        )
        # offline_model.transform()

    def testNormalize(self):
        pass


class TestODPSDataSource(BaseTestCase):

    def test_data_source(self):
        tf = ODPSDataSource(session=self.session)
        job_name = "test_data_source"
        run_job = tf.transform(table_name="pai_online_project.wumai_data", wait=False, job_name=job_name)
        self.assertEqual(run_job.get_status(), JobStatus.Running)
        self.assertEqual(run_job.name, job_name)
        run_job.attach()
        self.assertNotEqual(run_job.get_status(), JobStatus.Running)
