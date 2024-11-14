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
from unittest.mock import patch

from alibabacloud_credentials.credentials import Credential

from pai.session import Session, _init_default_session_from_env
from tests.unit import BaseUnitTestCase
from tests.unit.utils import mock_env


class TestSession(BaseUnitTestCase):
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

    @mock_env(DSW_INSTANCE_ID="dsw-378f4930c04191016")
    @mock_env(PAI_WORKSPACE_ID="1234567")
    @mock_env(REGION="cn-hangzhou")
    def test_init_default_session_from_env_in_dsw(self):
        mock_cred = Credential()
        with patch(
            "pai.session.Session._get_default_credential_client", return_value=mock_cred
        ):
            with patch(
                "pai.session.Session.get_default_oss_storage",
                return_value=("bucket", "endpoint"),
            ):
                s = _init_default_session_from_env()
                self.assertEqual(s.workspace_id, "1234567")
                self.assertEqual(s.region_id, "cn-hangzhou")

    @mock_env(DLC_JOB_ID="dlcv25vrbljblbgh")
    @mock_env(PAI_WORKSPACE_ID="1234567")
    @mock_env(REGION="cn-shanghai")
    def test_init_default_session_from_env_in_dlc(self):
        mock_cred = Credential()
        with patch(
            "pai.session.Session._get_default_credential_client", return_value=mock_cred
        ):
            with patch(
                "pai.session.Session.get_default_oss_storage",
                return_value=("bucket", "endpoint"),
            ):
                s = _init_default_session_from_env()
                self.assertEqual(s.workspace_id, "1234567")
                self.assertEqual(s.region_id, "cn-shanghai")
