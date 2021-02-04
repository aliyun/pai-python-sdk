from __future__ import absolute_import

import logging
import os
import unittest
from mock import patch

from tests.unit.utils import get_mock_session

test_root = os.path.dirname(os.path.abspath(__file__))


class BaseUnitTestCase(unittest.TestCase):
    """
    Base class for unittest, any test case class should inherit this.
    """

    @classmethod
    def setUpClass(cls):
        super(BaseUnitTestCase, cls).setUpClass()
        cls._log_config()
        cls.patch_mock_session()

    @classmethod
    def patch_mock_session(cls):
        patch("pai.core.session.Session._default_session", get_mock_session()).start()

    @classmethod
    def tearDownClass(cls):
        super(BaseUnitTestCase, cls).tearDownClass()

    @staticmethod
    def _log_config():
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] %(pathname)s:%(lineno)d %(levelname)s "
            "- %(message)s",
            datefmt="%Y/%m/%d %H:%M:%S",
        )
