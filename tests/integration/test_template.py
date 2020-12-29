from __future__ import absolute_import

import time

from pai.common import ProviderAlibabaPAI
from pai.pipeline import SavedTemplate
from tests.integration import BaseIntegTestCase
from tests.integration.tests_pipeline import create_simple_composite_pipeline
from pai.common.utils import iter_with_limit


class TestTemplateService(BaseIntegTestCase):
    def test_list_templates(self):
        templates = list(
            iter_with_limit(SavedTemplate.list(provider=ProviderAlibabaPAI), 100)
        )
        self.assertTrue(len(templates) != 0)

    # def test_load_template(self):
    #     component = SavedTemplate.load_by_identifier(
    #         "split-xflow-maxCompute",
    #         provider=ProviderAlibabaPAI,
    #         version="v1",
    #         with_impl=False,
    #     )
    #     self.assertIsNotNone(component.pipeline_id)
    #
    # def test_composite_pipeline_load(self):
    #     p, _, _, _ = create_simple_composite_pipeline()
    #     p = p.save(identifier="test-simple-pipeline", version="v%s" % int(time.time()))
    #
    #     saved_pipeline = SavedTemplate.load(p.pipeline_id, with_impl=True)
    #     self.assertTrue(len(saved_pipeline.steps) == len(p.steps))
    #
    #     inputs_names = [item.name for item in p.inputs]
    #     saved_inputs_names = [item.name for item in saved_pipeline.inputs]
    #     self.assertEqual(inputs_names, saved_inputs_names)
    #
    #     outputs_names = [item.name for item in p.outputs]
    #     saved_outputs_names = [item.name for item in saved_pipeline.outputs]
    #     self.assertEqual(outputs_names, saved_outputs_names)
    #
    #     step_depends = {s.name: sorted([i.name for i in s.depends]) for s in p.steps}
    #     saved_step_depends = {
    #         s.name: sorted([i.name for i in s.depends]) for s in saved_pipeline.steps
    #     }
    #     self.assertEqual(step_depends, saved_step_depends)
