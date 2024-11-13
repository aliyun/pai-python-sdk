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
import os
import shutil
import tempfile
from unittest.case import TestCase

from pai.common.consts import DEFAULT_CONFIG_PATH
from pai.session import (
    Session,
    get_default_session,
    load_default_config_file,
    setup_default_session,
)

from .utils import mock_env

DEFAULT_CONFIG_PATH_BK = DEFAULT_CONFIG_PATH + ".bk"


class TestSession(TestCase):
    def setUp(self):
        if os.path.exists(DEFAULT_CONFIG_PATH):
            self.local_config = load_default_config_file(DEFAULT_CONFIG_PATH)
            os.environ["PAI_WORKSPACE_ID"] = self.local_config["workspace_id"]
            os.environ["REGION"] = self.local_config["region_id"]
            shutil.move(DEFAULT_CONFIG_PATH, DEFAULT_CONFIG_PATH_BK)

    def tearDown(self):
        os.environ.pop("PAI_WORKSPACE_ID", None)
        os.environ.pop("REGION", None)
        if os.path.exists(DEFAULT_CONFIG_PATH_BK):
            shutil.move(DEFAULT_CONFIG_PATH_BK, DEFAULT_CONFIG_PATH)

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
    def test_get_default_session_in_dsw(self):
        s = get_default_session()
        self.assertEqual(s.region_id, self.local_config["region_id"])
        self.assertEqual(s.workspace_id, self.local_config["workspace_id"])

    @mock_env(DLC_JOB_ID="dlcv25vrbljblbgh")
    def test_get_default_session_in_dlc(self):
        s = get_default_session()
        self.assertEqual(s.region_id, self.local_config["region_id"])
        self.assertEqual(s.workspace_id, self.local_config["workspace_id"])

    def test_set_default_session(self):
        setup_default_session(region_id="cn-hangzhou", workspace_id="workspace_id")
        s = get_default_session()
        self.assertEqual(s.workspace_id, "workspace_id")
        self.assertEqual(s.region_id, "cn-hangzhou")
