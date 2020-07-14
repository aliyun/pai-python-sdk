from __future__ import absolute_import

from pai import ProviderAlibabaPAI
from pai.pipeline import Pipeline
from test import BaseTestCase


class TestEstimatorBase(BaseTestCase):

    # def setUp(self):
    #     pass
    #
    #
    # def tearDown(self):
    #     pass

    def test_estimator_from_pipeline(self):
        identifier = "logisticregression-binary-xflow-ODPS"
        version = "v1"
        provider = ProviderAlibabaPAI
        p = Pipeline.get_by_identifier(session=self.session, identifier=identifier,
                                       provider=provider, version=version)

        parameters = {
            "__xflowProject": "algo_public",
            "epsilon": 1e-06,
            "maxIter": 100,
            # "regularizedType": "l1",
            "regularizedLevel": 1.0,
        }
        est = p.to_estimator(parameters=parameters)

        self.assertEqual(est.get_identifier(), identifier)
        self.assertEqual(est.get_version(), version)
        self.assertEqual(est.get_provider(), provider)
        self.assertEqual(est.get_pipeline_id(), p.pipeline_id)

        model_name = "ut_estimator_from_pipeline"
        project = self.session.odps_project
        fit_args = {
            "inputArtifact": "odps://{project_name}/tables/{table_name}".format(
                project_name=project, table_name="test_table"),
            "labelColName": "_c2",
            "featureColNames": "",
            "modelName": model_name
        }

        _ = est.fit(wait=True, job_name="ut_pipeline_test", args=fit_args)

        # assert odps offlineModel exists
        self.assertTrue(
            self.session.odps_client.exist_offline_model(name=model_name, project=project))

        # model = job.create_model(artifact="outputArtifact")
        # model.deploy()

    def test_new_composite_pipeline_to_estimator(self):
        pass
