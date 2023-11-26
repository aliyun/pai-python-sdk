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

import json
import tempfile
from unittest.case import TestCase

from pai.session import Session


class TestSession(TestCase):
    def test_save_config(self):
        d = {
            "region_id": "cn-hangzhou",
            "workspace_id": "workspace_id",
            "oss_bucket_name": "oss_bucket_name",
            "oss_endpoint": "oss_endpoint",
        }

        s = Session(**d)
        tmp = tempfile.mktemp()
        s.save_config(tmp)
        with open(tmp, "r") as f:
            res = json.load(f)

        self.assertEqual(res, d)
