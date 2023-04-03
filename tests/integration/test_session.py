from tests.integration import BaseIntegTestCase


class TestSession(BaseIntegTestCase):
    def test_provider(self):
        session = self.default_session
        self.assertIsNotNone(session.provider)
