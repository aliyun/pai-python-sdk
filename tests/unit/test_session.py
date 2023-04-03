import json
import tempfile
from unittest.case import TestCase

from pai.session import Session


class TestSession(TestCase):
    def test_save_config(self):
        d = {
            "access_key_id": "AccessKeyId",
            "access_key_secret": "AccessKeySecret",
            "region_id": "cn-hangzhou",
            "security_token": "SecurityToken",
            "oss_bucket_name": "oss_bucket_name",
        }

        s = Session(**d)
        tmp = tempfile.mktemp()
        s.save_config(tmp)
        with open(tmp, "r") as f:
            res = json.load(f)

        self.assertEqual(res, d)
