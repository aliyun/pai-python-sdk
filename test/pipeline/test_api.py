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
        run = RunInstance(run_id="flow-lr7pcxkfjqmzi6pwd9", session=self.session)
        pprint(run.get_run_info())
        print("ouputs is")
        pprint(run.get_outputs(depth=2))

    def test_list_pipelines(self):
        pipelines, count = self.session.search_pipeline()

        print(count)
        print(pipelines)


if __name__ == "__main__":
    unittest.main()
