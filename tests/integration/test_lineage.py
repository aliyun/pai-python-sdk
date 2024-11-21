#  Copyright 2023 Alibaba, Inc. or its affiliates.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import logging

from pai.common.logging import get_logger
from pai.tracking import LineageEntity, log_lineage
from tests.integration import BaseIntegTestCase
from tests.unit.utils import mock_env


class TestLineage(BaseIntegTestCase):
    def test_run_in_non_dlc_env(self):
        with self.assertLogs(
            logger=get_logger("pai.tracking.lineage"), level=logging.WARNING
        ) as captured:
            log_lineage(
                input_entities=[
                    LineageEntity(
                        uri="pai://datasets/d-f0mniq7j4cgk2x2rrn/v1",
                        resource_type="dataset",
                        resource_use="train",
                    ),
                ],
                output_entities=[
                    LineageEntity(
                        uri="file:///mnt/model/",
                        resource_type="model",
                        resource_use="extension",
                    )
                ],
            )
            self.assertIn(
                "log_lineage is not supported in non-DLC environment.",
                captured.output[0],
            )

    @mock_env(DLC_JOB_ID="d123456")
    @mock_env(REGION="cn-hangzhou")
    def test_log_lineage_with_no_datasources_config_file_in_dlc(self):
        with self.assertLogs(
            logger=get_logger("pai.tracking.lineage"), level=logging.WARNING
        ) as captured:
            log_lineage(
                input_entities=[
                    LineageEntity(
                        uri="file:///mnt/input/dataset",
                        resource_type="model",
                        resource_use="extension",
                    )
                ],
                output_entities=[
                    LineageEntity(
                        uri="file:///mnt/output/model/model.pth",
                        resource_type="model",
                        resource_use="extension",
                    )
                ],
            )
            self.assertIn(
                "WARNING:pai.tracking.lineage:Error parsing data source JSON or file not found: [Errno 2] No such file or directory: '/var/metadata/config.json'",
                captured.output[0],
            )

    @mock_env(DLC_JOB_ID="d123456")
    @mock_env(REGION="cn-hangzhou")
    def test_valid_log_lineage_in_dlc(self):
        with self.assertLogs(
            logger=get_logger("pai.tracking.lineage"), level=logging.DEBUG
        ) as captured:
            log_lineage(
                input_entities=[
                    LineageEntity(
                        uri="oss://test-bucket.oss-cn-shanghai.aliyuncs.com/models/ALBERTv2-Chinese-NewsBase.pth",
                        resource_type="model",
                        resource_use="base",
                    ),
                    LineageEntity(
                        uri="nas://fsId-mountTarget.cn-hangzhou.nas.aliyuncs.com/nas/mountTarget/",
                        resource_type="dataset",
                        resource_use="train",
                    ),
                    LineageEntity(
                        uri="cpfs://cpfs-0077f18ed141a84e.cn-hangzhou/ptc-00f31da01c2a9c12/exp-005607872325f692/",
                        resource_type="dataset",
                        resource_use="train",
                    ),
                    LineageEntity(
                        uri="bmcpfs://cpfs-291070fd9529c747-000001.cn-wulanchabu.cpfs.aliyuncs.com/",
                        resource_type="dataset",
                        resource_use="train",
                    ),
                    LineageEntity(
                        uri="pai://datasets/d-jipftzxinc7nm1z0uh/v1",
                        resource_type="dataset",
                        resource_use="train",
                    ),
                    LineageEntity(
                        uri="odps://project_mc/tables/flow_model_label_table_v1",
                        resource_type="dataset",
                        resource_use="test",
                    ),
                ],
                output_entities=[
                    LineageEntity(
                        uri="oss://hangzhoutest01.oss-cn-hangzhou-internal.aliyuncs.com/models/model.pth",
                        resource_type="model",
                        resource_use="extension",
                    )
                ],
            )
            self.maxDiff = None
            self.assertEquals(
                "DEBUG:pai.tracking.lineage:[_LineageEntity(Attributes={'Bucket': 'test-bucket', 'Path': 'models/ALBERTv2-Chinese-NewsBase.pth', 'ResourceType': 'model', 'ResourceUse': 'base', 'RegionId': 'cn-shanghai'}, EntityType='oss-file', Name=None, QualifiedName=None), _LineageEntity(Attributes={'Uri': 'nas://fsId-mountTarget.cn-hangzhou.nas.aliyuncs.com/nas/mountTarget/', 'ResourceType': 'dataset', 'ResourceUse': 'train', 'RegionId': 'cn-hangzhou'}, EntityType='nas-file', Name=None, QualifiedName=None), _LineageEntity(Attributes={'Uri': 'cpfs://cpfs-0077f18ed141a84e.cn-hangzhou/ptc-00f31da01c2a9c12/exp-005607872325f692/', 'ResourceType': 'dataset', 'ResourceUse': 'train', 'RegionId': 'cn-hangzhou'}, EntityType='nas-file', Name=None, QualifiedName=None), _LineageEntity(Attributes={'Uri': 'bmcpfs://cpfs-291070fd9529c747-000001.cn-wulanchabu.cpfs.aliyuncs.com/', 'ResourceType': 'dataset', 'ResourceUse': 'train', 'RegionId': 'cn-wulanchabu'}, EntityType='nas-file', Name=None, QualifiedName=None), _LineageEntity(Attributes={'ResourceUse': 'train', 'Provider': 'pai'}, EntityType=None, Name='Aishell_1_subset_qwen', QualifiedName='pai-dataset.d-jipftzxinc7nm1z0uh_v1'), _LineageEntity(Attributes={'ResourceType': 'dataset', 'ResourceUse': 'test'}, EntityType=None, Name=None, QualifiedName='maxcompute-table.project_mc.flow_model_label_table_v1')]",
                captured.output[0],
            )
            self.assertEquals(
                "DEBUG:pai.tracking.lineage:[_LineageEntity(Attributes={'Bucket': 'hangzhoutest01', 'Path': 'models/model.pth', 'ResourceType': 'model', 'ResourceUse': 'extension', 'RegionId': 'cn-hangzhou'}, EntityType='oss-file', Name=None, QualifiedName=None)]",
                captured.output[1],
            )
            self.assertEquals("DEBUG:pai.tracking.lineage:d123456", captured.output[2])

    @mock_env(DLC_JOB_ID="d123456")
    @mock_env(REGION="cn-hangzhou")
    def test_log_lineage_with_invalid_format_input_entities_in_dlc(self):
        with self.assertLogs(
            logger=get_logger("pai.tracking.lineage"), level=logging.WARNING
        ) as captured:
            log_lineage(
                input_entities=[
                    LineageEntity(
                        uri="oss://test-bucket/models/ALBERTv2-Chinese-NewsBase.pth",
                        resource_type="model",
                        resource_use="base",
                    ),
                    LineageEntity(
                        uri="pai://datasets/",
                        resource_type="dataset",
                        resource_use="train",
                    ),
                    LineageEntity(
                        uri="odps://project_mc/flow_model_label_table_v1",
                        resource_type="dataset",
                        resource_use="test",
                    ),
                ],
                output_entities=[
                    LineageEntity(
                        uri="oss://test-bucket.oss-cn-shanghai.aliyuncs.com/model/model.pth",
                        resource_type="model",
                        resource_use="extension",
                    )
                ],
            )
            self.assertIn(
                "input_entities or output_entities is empty, ignore.",
                captured.output[0],
            )

    @mock_env(DLC_JOB_ID="d123456")
    @mock_env(REGION="cn-hangzhou")
    def test_log_lineage_with_invalid_format_output_entities_in_dlc(self):
        with self.assertLogs(
            logger=get_logger("pai.tracking.lineage"), level=logging.WARNING
        ) as captured:
            log_lineage(
                input_entities=[
                    LineageEntity(
                        uri="oss://test-bucket.oss-cn-shanghai.aliyuncs.com/models/ALBERTv2-Chinese-NewsBase.pth",
                        resource_type="model",
                        resource_use="base",
                    ),
                    LineageEntity(
                        uri="pai://datasets/d-jipftzxinc7nm1z0uh/v1",
                        resource_type="dataset",
                        resource_use="train",
                    ),
                    LineageEntity(
                        uri="odps://project_mc/tables/flow_model_label_table_v1",
                        resource_type="dataset",
                        resource_use="test",
                    ),
                ],
                output_entities=[
                    LineageEntity(
                        uri="oss://test-bucket/models/ALBERTv2-Chinese-NewsBase.pth",
                        resource_type="model",
                        resource_use="extension",
                    ),
                    LineageEntity(
                        uri="pai://datasets/",
                        resource_type="dataset",
                        resource_use="val",
                    ),
                    LineageEntity(
                        uri="odps://project_mc/flow_model_label_table_v1",
                        resource_type="dataset",
                        resource_use="test",
                    ),
                ],
            )
            self.assertIn(
                "input_entities or output_entities is empty, ignore.",
                captured.output[0],
            )

    @mock_env(DLC_JOB_ID="d123456")
    @mock_env(REGION="cn-hangzhou")
    def test_log_lineage_with_empty_input_output_entities_in_dlc(self):
        with self.assertLogs(
            logger=get_logger("pai.tracking.lineage"), level=logging.WARNING
        ) as captured:
            log_lineage([], [])
            self.assertIn(
                "input_entities or output_entities is empty, ignore.",
                captured.output[0],
            )
            log_lineage(
                input_entities=[LineageEntity(uri="")],
                output_entities=[LineageEntity(uri="")],
            )
            self.assertIn(
                "input_entities or output_entities is empty, ignore.",
                captured.output[1],
            )
