from pai.common import ProviderAlibabaPAI
from pai.entity.algorithm import Algorithm
from tests.integration import BaseIntegTestCase


class TestAlgorithmAPI(BaseIntegTestCase):
    def test_base(self):
        algos = Algorithm.list(algorithm_provider=ProviderAlibabaPAI)
        self.assertTrue(len(algos) > 0)

        versions = algos[0].list_versions()
        self.assertTrue(len(versions) > 0)

        algo = Algorithm.get_by_name(
            algorithm_name=algos[0].algorithm_name,
            algorithm_provider=ProviderAlibabaPAI,
        )

        self.assertEqual(algo.algorithm_name, algos[0].algorithm_name)
        self.assertIsNotNone(algo)
