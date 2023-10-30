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
