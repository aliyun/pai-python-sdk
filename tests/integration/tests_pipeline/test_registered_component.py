from __future__ import absolute_import

from pai.common import ProviderAlibabaPAI
from pai.pipeline import PipelineRunStatus
from pai.pipeline.component import RegisteredComponent
from tests.integration import BaseIntegTestCase


class TestRegisteredComponent(BaseIntegTestCase):
    def test_list(self):
        ops = RegisteredComponent.list(provider=ProviderAlibabaPAI)
        self.assertTrue(len(ops) > 0)

    def test_run(self):
        op = RegisteredComponent.get_by_identifier(
            "split",
            provider=ProviderAlibabaPAI,
        )
        self.assertIsNotNone(op.pipeline_id)
        self.assertEqual(op.identifier, "split")
        self.assertEqual(op.provider, ProviderAlibabaPAI)
        self.assertEqual(op.version, "v1")

        run = op.run(
            job_name="integ_test_save_op_run",
            arguments={
                "execution": self.get_default_maxc_execution(),
                "inputTable": "odps://{}/tables/{}".format(
                    self.breast_cancer_dataset.default_dataset_project,
                    self.breast_cancer_dataset.table_name,
                ),
                "fraction": "0.7",
            },
        )

        self.assertEqual(run.get_status(), PipelineRunStatus.Succeeded)
