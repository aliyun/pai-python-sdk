from __future__ import absolute_import

import os
import time
import unittest
from pprint import pprint

import yaml

from pai import RunInstance
from test import BaseTestCase

_test_root = os.path.dirname(os.path.abspath(__file__))


class TestPaiFlowAPI(BaseTestCase):

    def test_list_pipeline(self):
        resp = self.session.list_pipeline(page_size=200)
        pprint(resp)

        for pipeline_outline in resp["Data"]:
            pprint(self.session.list_pipeline_privilege(pipeline_outline["PipelineId"]))

    def test_pipeline_create(self):
        pass

    def test_pipeline_update_privilege(self):
        pass

    @staticmethod
    def data_source_pipeline_arguments_env():
        arguments = {'parameters': [{'from': '{{env.resource.compute.max_compute}}',
                                     'name': '__execution'},
                                    {'name': '__xflowProject', 'value': 'wyl_test'},
                                    {'name': '__project', 'value': 'wyl_test'},
                                    {'name': 'cols_to_double', 'value': 'time,hour,pm2,pm10,so2,co,no2'},
                                    {'name': 'histogram_selected_col_names',
                                     'value': 'hour,pm10,so2,co,no2,pm2'},
                                    {'name': 'sql',
                                     'value': 'select time,hour,(case when pm2>200 then 1 else 0 end),pm10,so2,co,no2 from pai_temp_83935_1099578_1'},
                                    {'name': 'normalize_selected_col_names', 'value': 'pm10,so2,co,no2'},
                                    {'name': 'fraction', 'value': 0.8},
                                    {'name': 'randomforests_feature_col_names', 'value': 'pm10,so2,co,no2'},
                                    {'name': 'randomforests_label_col_names', 'value': '_c2'},
                                    {'name': 'prediction1_feature_col_names', 'value': 'pm10,so2,co,no2'},
                                    {'name': 'prediction1_append_col_names',
                                     'value': 'time,hour,_c2,pm10,so2,co,no2'},
                                    {'name': 'prediction1_result_col_name', 'value': 'prediction_result'},
                                    {'name': 'prediction1_score_col_name', 'value': 'prediction_score'},
                                    {'name': 'prediction1_detail_col_name', 'value': 'prediction_detail'},
                                    {'name': 'evaluate1_label_col_name', 'value': '_c2'},
                                    {'name': 'evaluate1_score_col_name', 'value': 'prediction_score'},
                                    {'name': 'evaluate1_positive_label', 'value': 1},
                                    {'name': 'evaluate1_bin_count', 'value': 1000},
                                    {'name': 'logisticregression_feature_col_names',
                                     'value': 'pm10,so2,co,no2'},
                                    {'name': 'logisticregression_label_col_names', 'value': '_c2'},
                                    {'name': 'logisticregression_good_value', 'value': 1},
                                    {'name': 'prediction2_feature_col_names', 'value': 'pm10,so2,co,no2'},
                                    {'name': 'prediction2_append_col_names',
                                     'value': 'time,hour,_c2,pm10,so2,co,no2'},
                                    {'name': 'prediction2_result_col_name', 'value': 'prediction_result'},
                                    {'name': 'prediction2_score_col_name', 'value': 'prediction_score'},
                                    {'name': 'prediction2_detail_col_name', 'value': 'prediction_detail'},
                                    {'name': 'evaluate2_label_col_name', 'value': '_c2'},
                                    {'name': 'evaluate2_score_col_name', 'value': 'prediction_score'},
                                    {'name': 'evaluate2_positive_label', 'value': 1},
                                    {'name': 'evaluate2_bin_count', 'value': 1000}]}

        env = {'resource': {'compute': {'max_compute': {'__odpsInfoFile': '/share/base/odpsInfo.ini',
                                                        'endpoint': 'http://service.cn-shanghai.maxcompute.aliyun.com/api',
                                                        'logViewHost': 'http://logview.odps.aliyun.com',
                                                        'odpsProject': 'wyl_test',
                                                        'userId': 15577}}},
               'workflowService': {'config': {'endpoint': 'http://service.cn-shanghai.argo.aliyun.com'},
                                   'name': 'argo'}}
        return arguments, env

    def test_pipeline_run_by_id(self):
        pipeline_id = 'fda7f0a92d784864a15a9ae011f3185f'
        pipeline_info = self.session.get_pipeline_by_id(pipeline_id)
        manifest = pipeline_info["Manifest"]
        manifest = yaml.load(manifest, yaml.FullLoader)
        manifest["metadata"]["version"] = "v0.1"

        arguments, env = self.data_source_pipeline_arguments_env()
        name_suffix = str(int(time.time()))
        run_id = self.session.create_pipeline_run("unittest_paiflow_%s" % name_suffix,
                                                  pipeline_id=pipeline_id,
                                                  arguments=arguments,
                                                  no_confirm_required=True)
        self.assertIsNotNone(run_id)
        run = RunInstance(run_id=run_id, session=self.session)
        run.wait()

    def test_run_wait(self):
        pass

    def test_list_run(self):
        run_infos = self.session.list_pipeline_run(status="Succeeded")

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


if __name__ == "__main__":
    unittest.main()
