from pprint import pprint

from pai.pipeline import PipelineParameter
from pai.pipeline.template import ContainerTemplate
from pai.pipeline.types import (
    PipelineArtifact,
    ArtifactMetadata,
    ArtifactDataType,
    ArtifactLocationType,
)
from tests.unit import BaseUnitTestCase


class TestContainerTemplate(BaseUnitTestCase):
    def test_manifest(self):
        inputs = [
            PipelineParameter(name="epoch", typ=int),
            PipelineParameter(
                name="regularizedType",
                typ=str,
                default="l1",
            ),
            PipelineArtifact(
                name="dataset",
                metadata=ArtifactMetadata(
                    data_type=ArtifactDataType.DataSet,
                    location_type=ArtifactLocationType.OSS,
                ),
            ),
            PipelineArtifact(
                name="model",
                metadata=ArtifactMetadata(
                    data_type=ArtifactDataType.Model,
                    location_type=ArtifactLocationType.OSS,
                ),
            ),
        ]

        outputs = [
            PipelineArtifact(
                name="output1",
                metadata=ArtifactMetadata(
                    data_type=ArtifactDataType.DataSet,
                    location_type=ArtifactLocationType.OSS,
                ),
            ),
            PipelineArtifact(
                name="output2",
                metadata=ArtifactMetadata(
                    data_type=ArtifactDataType.Model,
                    location_type=ArtifactLocationType.OSS,
                ),
            ),
        ]

        image_registry_config = {
            "userName": "testUserName",
            "password": "testPassword",
        }
        env_vars = {
            "PAI_SOURCE_CODE": "oss://hello/world/source-code.gz.tar",
            "PAI_ENTRY_POINT": "main.py",
        }
        image_uri = "registry.cn-shanghai.aliyuncs.com/paiflow-core/xflow_base:v1.1"
        command = "train"

        templ = ContainerTemplate(
            image_uri=image_uri,
            command=command,
            image_registry_config=image_registry_config,
            inputs=inputs,
            outputs=outputs,
            env=env_vars,
        )
        manifest = templ.to_dict()
        pprint(manifest)

        input_params_spec = manifest["spec"]["inputs"]["parameters"]
        input_artifacts_spec = manifest["spec"]["inputs"]["artifacts"]
        output_artifacts_spec = manifest["spec"]["outputs"]["artifacts"]
        env_spec = manifest["spec"]["container"]["envs"]

        self.assertEqual(
            input_params_spec,
            [
                {"name": "epoch", "type": "Int"},
                {"name": "regularizedType", "type": "String", "value": "l1"},
            ],
        )

        self.assertEqual(
            input_artifacts_spec,
            [
                {
                    "metadata": {"type": {"DataSet": {"locationType": "OSS"}}},
                    "name": "dataset",
                },
                {
                    "metadata": {"type": {"Model": {"locationType": "OSS"}}},
                    "name": "model",
                },
            ],
        )

        self.assertEqual(
            output_artifacts_spec,
            [
                {
                    "metadata": {"type": {"DataSet": {"locationType": "OSS"}}},
                    "name": "output1",
                },
                {
                    "metadata": {"type": {"Model": {"locationType": "OSS"}}},
                    "name": "output2",
                },
            ],
        )

        self.assertEqual(env_spec, env_vars)
        self.assertEqual(manifest["spec"]["container"]["command"], command)
        self.assertEqual(manifest["spec"]["container"]["image"], image_uri)
        self.assertEqual(
            manifest["spec"]["container"]["imageRegistryConfig"], image_registry_config
        )
