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

from __future__ import absolute_import

import logging
import os
import unittest
from unittest.mock import patch

from tests.unit.utils import get_mock_session

test_root = os.path.dirname(os.path.abspath(__file__))


class BaseUnitTestCase(unittest.TestCase):
    """
    Base class for unittest, any test case class should inherit this.
    """

    mock_patches = []

    @classmethod
    def setUpClass(cls):
        super(BaseUnitTestCase, cls).setUpClass()
        cls._log_config()
        cls.mock_patches.append(
            patch("pai.session._default_session", get_mock_session())
        )
        for p in cls.mock_patches:
            p.start()

    @classmethod
    def tearDownClass(cls):
        super(BaseUnitTestCase, cls).tearDownClass()
        for p in cls.mock_patches:
            p.stop()

    @staticmethod
    def _log_config():
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s "
            "- %(message)s",
            datefmt="%Y/%m/%d %H:%M:%S",
        )
