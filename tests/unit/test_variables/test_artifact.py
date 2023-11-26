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

from __future__ import absolute_import

from pai.pipeline.component import ContainerComponent
from pai.pipeline.types import (
    DataType,
    LocationArtifactMetadata,
    LocationType,
    PipelineArtifact,
    PipelineParameter,
)
from pai.pipeline.types.artifact import MaxComputeResourceArtifact, OSSArtifact
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
            max_compute_af, metadata = MaxComputeResourceArtifact.from_resource_url(
                case["input"]
            )
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

    def test_repeated_artifact(self):
        container_op = ContainerComponent(
            inputs=[
                PipelineParameter("foo"),
                PipelineArtifact(
                    "input1",
                    repeated=True,
                    metadata=LocationArtifactMetadata(
                        data_type=DataType.DataSet, location_type=LocationType.OSS
                    ),
                ),
                PipelineArtifact(
                    "input2",
                    repeated=True,
                    metadata=LocationArtifactMetadata(
                        data_type=DataType.DataSet, location_type=LocationType.OSS
                    ),
                ),
            ],
            outputs=[
                PipelineArtifact(
                    "output1",
                    repeated=True,
                    metadata=LocationArtifactMetadata(
                        data_type=DataType.DataSet, location_type=LocationType.OSS
                    ),
                ),
            ],
            image_uri="registry.cn-shanghai.aliyuncs.com/paiflow-core/xflow_base:v1.1",
            command="train",
        )

        container_op.set_artifact_count("output1", 3)
        container_op.set_artifact_count("input2", 2)
        parameters, artifacts = container_op.translate_arguments(
            {
                "foo": "bar",
                "input1": [
                    "odps://pai_online_project/tables/wumai_data",
                    "odps://pai_online_project/tables/breast_cancer_data",
                ],
            }
        )

        self.assertEqual([{"name": "foo", "value": "bar"}], parameters)

        self.assertEqual(
            [
                {
                    "name": "input1",
                    "value": [
                        {
                            "name": "input1_0",
                            "value": {
                                "metadata": {
                                    "type": {"DataSet": {"locationType": "OSS"}}
                                },
                                "value": '{"location": {"project": "pai_online_project", "table": '
                                '"wumai_data"}}',
                            },
                        },
                        {
                            "name": "input1_1",
                            "value": {
                                "metadata": {
                                    "type": {"DataSet": {"locationType": "OSS"}}
                                },
                                "value": '{"location": {"project": '
                                '"pai_online_project", "table": '
                                '"breast_cancer_data"}}',
                            },
                        },
                    ],
                },
                {"name": "input2", "value": [None, None]},
                {"name": "output1", "value": [None, None, None]},
            ],
            artifacts,
        )

    def test_oss_artifact(self):
        artifact, metadata = OSSArtifact.from_resource_url(
            "oss://bucket-name.oss-host/path-to-file/file-name"
        )
        self.assertEqual(
            artifact.to_dict(),
            {
                "location": {
                    "endpoint": "oss-host",
                    "bucket": "bucket-name",
                    "key": "path-to-file/file-name",
                }
            },
        )
        self.assertEqual(
            metadata.to_dict(), {"type": {"DataSet": {"locationType": "OSS"}}}
        )
