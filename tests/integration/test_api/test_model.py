from pai.common.consts import ModelFormat
from pai.model import Model, ModelVersion
from pai.predictor.service import ComputeConfig, ServiceStatus
from tests.integration import BaseIntegTestCase
from tests.integration.utils import make_resource_name
from tests.test_data import PMML_MODEL_PATH


class TestModel(BaseIntegTestCase):
    model_path = None

    @classmethod
    def setUpClass(cls):
        super(TestModel, cls).setUpClass()
        bucket = cls.default_session.oss_bucket
        cls.model_path = cls.upload_file(
            bucket, "sdk-test/models/pmml/", PMML_MODEL_PATH
        )

    def test_model_base(self):
        model_name = make_resource_name("base")
        model_version = ModelVersion(
            uri=self.model_path,
            version="1.2.0",
            name=model_name,
            model_format=ModelFormat.PMML,
        )
        model_version.register()

        self.assertEqual(model_version.version, "1.2.0")
        self.assertIsNotNone(model_version.model_id)
        models = Model.list()
        self.assertTrue(len(models) > 0)
        models = Model.list(name=model_name)
        self.assertTrue(len(models) > 0)

        m = ModelVersion.get(
            model_id=model_version.model_id, version=model_version.version
        )

        self.assertEqual(m.inference_spec["processor"], "pmml")
        self.assertEqual(m.version, model_version.version)
        self.assertEqual(m.model_id, model_version.model_id)

        model = Model.get(id=model_version.model_id)
        self.assertTrue(len(model.list_versions()) >= 1)
        model_version.delete()
        model.delete()

    def test_model_deploy(self):
        model_version = ModelVersion(
            uri=self.model_path,
            version="1.2.0",
            name=make_resource_name("deploy"),
            model_format=ModelFormat.PMML,
        )

        eas_service = model_version.deploy(
            service_name=make_resource_name("model_deploy", sep="_", time_suffix=False),
            compute_target=ComputeConfig.from_resource_config(
                cpu=2,
                memory=4000,
            ),
            wait_for_ready=True,
        )
        self.assertEqual(eas_service.status, ServiceStatus.Running)
        eas_service.delete()

    def test_model_blue_green_deploy(self):
        model_version = ModelVersion(
            uri=self.model_path,
            version="1.2.0",
            model_format=ModelFormat.PMML,
        )

        service_name = make_resource_name(
            "model_blue_green_deploy", sep="_", time_suffix=False
        )
        blue_eas_service = model_version.deploy(
            service_name=service_name,
            compute_target=ComputeConfig.from_resource_config(
                cpu=2,
                memory=4000,
            ),
            wait_for_ready=True,
        )
        self.assertEqual(blue_eas_service.status, ServiceStatus.Running)
        green_eas_service = model_version.blue_green_deploy(
            service_name=service_name,
            compute_target=ComputeConfig.from_resource_config(
                cpu=2,
                memory=4000,
            ),
            wait_for_ready=True,
        )

        self.assertTrue(
            service_name in green_eas_service.name
            and len(green_eas_service.name) > len(service_name)
        )
        names = [s.name for s in green_eas_service.blue_green_services]

        self.assertTrue(blue_eas_service.name in names)
        self.assertTrue(green_eas_service.name in names)

        blue_eas_service.delete()
        green_eas_service.delete()
