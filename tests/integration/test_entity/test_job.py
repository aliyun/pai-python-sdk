from pai.api.job_api import JobAPI
from pai.core.session import get_default_session
from pai.entity import CodeSource
from pai.entity.dataset import Dataset
from pai.entity.job import Job, JobSpec
from tests.integration import BaseIntegTestCase
from tests.integration.utils import make_resource_name
from tests.test_data import SCRIPT_DIR_PATH


class TestJobBase(BaseIntegTestCase):

    job_api: JobAPI

    @classmethod
    def setUpClass(cls):
        super(TestJobBase, cls).setUpClass()
        cls.job_api = get_default_session().job_api

    def test_image_list(self):
        images = get_default_session().image_api

        community_images = images.list_community_images()
        self.assertTrue(len(community_images.items) > 0)
        pai_images = images.list_pai_images()

        self.assertTrue(len(pai_images.items) > 0)

    def test_ecs_spec(self):

        gpu_ecs_specs = self.job_api.list_ecs_specs(accelerator_type="gpu")
        self.assertTrue(len(gpu_ecs_specs.items) > 0)

        cpu_ecs_specs = self.job_api.list_ecs_specs(accelerator_type="cpu")
        self.assertTrue(len(cpu_ecs_specs.items) > 0)

    def test_base_run(self):
        sess = get_default_session()
        if not sess.is_inner:
            image_uri = "registry.{}.aliyuncs.com/pai-dlc/xgboost-training:1.6.0-cpu-py36-ubuntu18.04".format(
                sess.region_id
            )
            worker_ecs_spec = "ecs.c6.large"
        else:
            image_uri = "reg.docker.alibaba-inc.com/pai-dlc/xgboost-training:1.6.0-cpu-py36-ubuntu18.04"
            worker_ecs_spec = "pai.1x2.xsmall"
        (train_dataset, test_dataset) = Dataset.list()[:2]
        code = CodeSource.list()[0]
        job = Job(
            display_name=make_resource_name("test_base"),
            job_specs=JobSpec.from_instance_type(
                worker_image=image_uri,
                worker_count=1,
                worker_instance_type=worker_ecs_spec,
            ),
            user_command="echo Hello",
            data_sources=[
                train_dataset.mount(mount_path="/ml/input/data/train/"),
                # test_dataset.mount(mount_path="/ml/input/data/test/"),
            ],
            code_source=code.mount(mount_path="/ml/code/"),
        )

        self.assertIsNone(job.id)
        self.assertIsNone(job.create_time)
        job.run(wait=True)
        self.assertIsNotNone(job.id)
        self.assertTrue(len(Job.list()) > 0)
        self.assertIsNotNone(job.status)
        self.assertIsNotNone(job.reason_code)
        self.assertIsNotNone(job.reason_message)
        self.assertIsNotNone(job.pods)

    def test_from_script(self):
        sess = get_default_session()

        image_uri = "registry.{}.aliyuncs.com/pai-dlc/xgboost-training:1.6.0-cpu-py36-ubuntu18.04".format(
            sess.region_id
        )
        # image_uri = "registry.{}.aliyuncs.com/pai-dlc/tensorflow-training:2.3-cpu-py36-ubuntu18.04".format(sess.region_id)
        # image_uri = "registry.cn-shanghai.aliyuncs.com/pai-dlc/pytorch-training:1.8PAI-gpu-py36-cu101-ubuntu18.04"
        # worker_ecs_spec = "ecs.c6.large"
        oss_bucket = sess.oss_bucket
        output_path = "oss://{bucket_name}.{endpoint}/sdk-test/job-output-path/".format(
            bucket_name=oss_bucket.bucket_name,
            endpoint=oss_bucket.endpoint.lstrip("https://"),
        )

        job: Job = Job.from_script(
            source_dir=SCRIPT_DIR_PATH,
            entry_point="main.py",
            output_path=output_path,
            display_name=make_resource_name("test_script"),
            job_specs=JobSpec.from_resource_config(
                worker_count=1,
                worker_cpu=2,
                worker_memory=4,
                worker_image=image_uri,
            ),
            resource_id="rg1czpuyreszewix",
            # third_party_libs=["tensorflow_datasets"]
        )
        job.run(wait=True)
