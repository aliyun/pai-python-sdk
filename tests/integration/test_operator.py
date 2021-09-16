from __future__ import absolute_import

import unittest

from pai.common import ProviderAlibabaPAI
from pai.core.session import EnvType
from pai.operator import SavedOperator
from pai.pipeline import PipelineRunStatus
from tests.integration import BaseIntegTestCase
from pai.common.utils import iter_with_limit
from tests.integration.utils import t_context


@unittest.skipIf(
    t_context.env_type == EnvType.Light,
    "Light Environment do not hold PAI provide SavedOperator.",
)
class TestSavedOperator(BaseIntegTestCase):
    def test_list_operator(self):
        operators = list(
            iter_with_limit(SavedOperator.list(provider=ProviderAlibabaPAI), 2)
        )

        self.assertTrue(len(operators) == 2)

    def test_saved_operator(self):
        op = SavedOperator.get_by_identifier(
            "split",
            provider=ProviderAlibabaPAI,
            version="v1",
        )
        self.assertIsNotNone(op.pipeline_id)
        self.assertEqual(op.identifier, "split")
        self.assertEqual(op.provider, ProviderAlibabaPAI)
        self.assertEqual(op.version, "v1")

        run = op.run(
            job_name="integ_test_save_op_run",
            arguments={
                "execution": self.get_default_maxc_execution(),
                "inputTable": "odps://pai_online_project/tables/%s"
                % self.breast_cancer_dataset.table_name,
                "fraction": 0.7,
            },
        )

        self.assertEqual(run.get_status(), PipelineRunStatus.Succeeded)
