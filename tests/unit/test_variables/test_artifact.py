from __future__ import absolute_import

from pai.pipeline.types.artifact import MaxComputeResourceArtifact
from tests.unit import BaseUnitTestCase


class TestArtifact(BaseUnitTestCase):
    def test_max_compute_artifact(self):
        cases = [
            {
                "name": "table_case1",
                "input": "odps://prj_test/tables/test_table",
                "expected": {
                    "location": {
                        "project": "prj_test",
                        "table": "test_table",
                    }
                },
            },
            {
                "name": "table_case2",
                "input": "odps://prj_test/tables/test_table/pt1=hello/pt2=world",
                "expected": {
                    "location": {
                        "project": "prj_test",
                        "table": "test_table",
                        "partition": "pt1=hello/pt2=world",
                    }
                },
            },
            {
                "name": "table_case3",
                "input": "odps://prj_test/tables/test_table/pt1=hello/pt2=world/?parameter=world",
                "expected": {
                    "location": {
                        "project": "prj_test",
                        "table": "test_table",
                        "partition": "pt1=hello/pt2=world",
                    }
                },
            },
            {
                "name": "volume_case1",
                "input": "odps://prj_volume/volumes/data_store/vpartition/i_am_file.csv",
                "expected": {
                    "location": {
                        "project": "prj_volume",
                        "volume": "data_store",
                        "volumePartition": "vpartition",
                        "file": "i_am_file.csv",
                    }
                },
            },
            {
                "name": "volume_case2",
                "input": "odps://prj_volume/volumes/data_store/vpart/i_am_file.csv?hello=world",
                "expected": {
                    "location": {
                        "project": "prj_volume",
                        "volume": "data_store",
                        "volumePartition": "vpart",
                        "file": "i_am_file.csv",
                    }
                },
            },
            {
                "name": "offline_model_case3",
                "input": "odps://prj_om/offlinemodels/xlab_m_GBDT_LR_1_1685664_v0_m_2",
                "expected": {
                    "name": "xlab_m_GBDT_LR_1_1685664_v0_m_2",
                    "location": {
                        "project": "prj_om",
                        "name": "xlab_m_GBDT_LR_1_1685664_v0_m_2",
                    },
                },
            },
        ]
        for case in cases:
            max_compute_af = MaxComputeResourceArtifact.from_resource_url(case["input"])
            self.assertEqual(
                case["expected"],
                max_compute_af.to_dict(),
                "case:%s, expected: %s, result:%s"
                % (
                    case["name"],
                    case["expected"],
                    max_compute_af.to_dict(),
                ),
            )
