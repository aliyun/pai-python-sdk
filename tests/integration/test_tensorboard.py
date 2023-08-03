from pai.tensorboard import TensorBoard, TensorBoardStatus
from tests.integration import BaseIntegTestCase


class TestTensorBoard(BaseIntegTestCase):
    def test(self):
        uri = "oss://{}/sdktest/tensorboard_logs/".format(
            self.default_session.oss_bucket.bucket_name
        )
        tb = TensorBoard.create(uri, wait=True)
        self.assertEqual(tb.status, TensorBoardStatus.Running)
        self.assertIsNotNone(tb.app_uri)

        tb.stop()
        tb.start()
        self.assertTrue(TensorBoardStatus.is_running(tb.status))
        tb.delete()
