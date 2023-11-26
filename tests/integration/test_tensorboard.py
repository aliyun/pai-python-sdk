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
