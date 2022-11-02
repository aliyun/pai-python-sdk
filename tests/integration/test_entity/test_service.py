import time

from Tea.exceptions import UnretryableException

from pai.common.oss_utils import truncate_endpoint
from pai.entity.service import ComputeConfig, Service, ServiceStatus, TrafficState
from tests.integration import BaseIntegTestCase
from tests.integration.utils import make_eas_service_name, make_resource_name
from tests.test_data import PMML_MODEL_PATH


class TestEasServiceAPI(BaseIntegTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestEasServiceAPI, cls).setUpClass()
        bucket = cls.default_session.oss_bucket
        cls.model_path = cls.upload_file(
            bucket, "sdk-test/model_api/pmml/", PMML_MODEL_PATH
        )

    def test_base(self):
        # Test EasService deploy
        name = make_resource_name("base", sep="_", time_suffix=False)
        eas_service = Service.deploy(
            name=name,
            instance_count=2,
            compute_config=ComputeConfig.from_resource_config(
                cpu=1,
                memory=2000,
            ),
            model_path=self.model_path,
            processor="pmml",
            wait_for_ready=True,
            token="ExampleToken",
        )

        self.assertTrue(eas_service.name == name)
        self.assertEqual(eas_service.total_instance, 2)
        self.assertTrue(eas_service.compute_config.cpu, 1)
        self.assertTrue(eas_service.compute_config.memory, 2000)
        self.assertTrue(eas_service.processor, "pmml")
        self.assertIsNotNone(eas_service.access_token)
        self.assertEqual(eas_service.model_path, truncate_endpoint(self.model_path))
        self.assertEqual(eas_service.status, ServiceStatus.Running)
        self.assertEqual(eas_service.access_token, "ExampleToken")

        # Test EasService scale
        eas_service.scale(instance_count=1)
        self.assertEqual(eas_service.total_instance, 1)
        eas_service.scale(
            compute_target=ComputeConfig.from_resource_config(
                cpu=2,
                memory=4000,
            )
        )

        self.assertEqual(eas_service.compute_config.cpu, 2)
        self.assertEqual(eas_service.compute_config.memory, 4000)
        # Test EasService stop/delete
        eas_service.stop(wait=True)
        self.assertEqual(eas_service.status, ServiceStatus.Stopped)
        eas_service.delete()

    def test_blue_green_deploy(self):
        blue_name = make_eas_service_name("blue_green_deploy")
        blue_service: Service = Service.deploy(
            name=blue_name,
            compute_config=ComputeConfig.from_resource_config(
                cpu=1,
                memory=2000,
            ),
            instance_count=1,
            model_path=self.model_path,
            processor="pmml",
            wait_for_ready=True,
        )
        self.assertTrue(blue_service.status == ServiceStatus.Running)
        self.assertTrue(blue_service.name == blue_name)
        blue_service_predictor = blue_service.get_predictor()
        self.assert_endpoint_valid(blue_service_predictor)

        green_service_1: Service = blue_service.blue_green_deploy(
            compute_target=ComputeConfig.from_resource_config(
                cpu=1,
                memory=2000,
            ),
            model_path=self.model_path,
            processor="pmml",
            wait_for_ready=True,
            token="HelloWorld",
        )
        green_service_1.adjust_traffic(50)
        self.assertEqual(green_service_1.weight, 50)
        self.assertNotEqual(green_service_1.name, blue_name)
        blue_service.delete()
        self.wait_for_service_deleted(blue_service.name)
        self.assert_endpoint_valid(blue_service_predictor)
        green_service_1.delete()

    @classmethod
    def wait_for_service_deleted(cls, service_name):
        while True:
            try:
                Service.get(service_name)
                time.sleep(5)
            except UnretryableException as e:
                print(e)
                break

    def assert_endpoint_valid(self, predictor):
        result = predictor.predict(
            [
                {
                    "pm10": 1.0,
                    "so2": 2.0,
                    "co": 0.5,
                },
                {
                    "pm10": 1.0,
                    "so2": 2.0,
                    "co": 0.5,
                },
            ]
        )
        self.assertEqual(len(result), 2)

    def test_group_deploy(self):
        service_name_1 = make_eas_service_name("group_deploy_1")
        service_name_2 = make_eas_service_name("group_deploy_2")
        group_name = make_eas_service_name("group")

        service_1 = Service.group_deploy(
            name=service_name_1,
            service_group_name=group_name,
            compute_target=ComputeConfig.from_resource_config(
                cpu=1,
                memory=2000,
            ),
            model_path=self.model_path,
            processor="pmml",
            traffic_state=TrafficState.TRAFFIC_STATE_GROUPING,
        )
        service_1_predictor = service_1.get_predictor()
        self.assert_endpoint_valid(service_1_predictor)

        service_group_predictor = service_1.get_service_group_predictor()
        self.assert_endpoint_valid(service_group_predictor)

        service_2 = Service.group_deploy(
            name=service_name_2,
            service_group_name=group_name,
            compute_target=ComputeConfig.from_resource_config(
                cpu=1,
                memory=2000,
            ),
            model_path=self.model_path,
            processor="pmml",
            traffic_state=TrafficState.TRAFFIC_STATE_GROUPING,
        )

        service_2_predictor = service_2.get_predictor()
        self.assert_endpoint_valid(service_2_predictor)

        service_1.stop()
        self.assert_endpoint_valid(service_group_predictor)
        service_1.delete()
        service_2.delete()

    # def test_delete_service(self):
    #     for s in EasService.list(page_size=50):
    #         if s.status == EasServiceStatus.Running and (
    #             s.name.startswith("sdktest") or s.name.startswith("example_")
    #         ):
    #             s.delete()
