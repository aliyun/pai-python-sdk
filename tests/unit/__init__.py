from __future__ import absolute_import

import logging
import os
import unittest
from collections import namedtuple

import oss2
from odps import ODPS
from six.moves import configparser
from six.moves.configparser import DEFAULTSECT

from pai.core.session import setup_default_session
from pai.core.workspace import Workspace

_test_root = os.path.dirname(os.path.abspath(__file__))

OSSInfo = namedtuple(
    "OSSInfo", [
        "bucket",
        "endpoint",
        "rolearn",
    ]
)


class BaseUnitTestCase(unittest.TestCase):
    """
    Base class for unittest, any test case class should inherit this.
    """

    @classmethod
    def setUpClass(cls):
        super(BaseUnitTestCase, cls).setUpClass()
        cls._log_config()

    @classmethod
    def tearDownClass(cls):
        super(BaseUnitTestCase, cls).tearDownClass()

    @staticmethod
    def _log_config():
        logging.basicConfig(level=logging.INFO,
                            format='[%(asctime)s] %(pathname)s:%(lineno)d %(levelname)s '
                                   '- %(message)s',
                            datefmt='%Y/%m/%d %H:%M:%S')
