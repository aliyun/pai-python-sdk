from __future__ import absolute_import

import os
import unittest
from pprint import pprint

from pai import RunInstance
from test import BaseTestCase

from pai.common import ProviderAlibabaPAI

_test_root = os.path.dirname(os.path.abspath(__file__))


class TestPaiFlowAPI(BaseTestCase):

    def test_list_pipeline(self):
        pipeline_infos, total_count = self.session.search_pipeline(
            provider=ProviderAlibabaPAI, page_size=50, page_num=1)
        if total_count > 0:
            self.assertTrue(len(pipeline_infos) > 0)

    def test_pipeline_create(self):
        pass

    def test_pipeline_update_privilege(self):
        pass

    def test_run_wait(self):
        pass

    def test_list_run(self):
        pass

    def test_get_run_detail(self):
        pass

    def test_get_log(self):
        pass

    def test_manifest_run(self):
        pass

    def test_composite_pipeline_run(self):
        pass

    def test_run_status_manager(self):
        pass

    def test_run_outputs(self):
        run_id = 'flow-mm1sljb2a6etgdjlvq'
        node_id = 'node-wr2ez8v7updhsjssjr'
        run_instance = RunInstance(run_id=run_id,
                                   session=self.session)
        outputs = run_instance.get_outputs(node_id=node_id)
        print(outputs)

    def test_list_pipelines(self):
        pipelines, count = self.session.search_pipeline(provider=ProviderAlibabaPAI)
        self.assertTrue(len(pipelines) > 0)
        self.assertTrue(count > 0)


if __name__ == "__main__":
    unittest.main()
