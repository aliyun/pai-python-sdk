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
import logging

from pai.common.logging import (
    _reset_library_root_logger,
    get_log_level,
    get_logger,
    set_log_level_debug,
    set_log_level_info,
)

from .utils import mock_env


@mock_env(PAI_LOG_LEVEL="DEBUG")
def test_log_level():
    _reset_library_root_logger()

    assert get_log_level() == logging.DEBUG


@mock_env(PAI_LOG_LEVEL="INFO")
def test_get_logger():
    _reset_library_root_logger()

    lib_root_logger = get_logger()
    logger = get_logger("pai.abc")

    assert logger.parent == lib_root_logger
    assert lib_root_logger.getEffectiveLevel() == logging.INFO


def test_set_log_level():
    _reset_library_root_logger()

    assert get_log_level() == logging.WARNING

    set_log_level_info()
    assert get_log_level() == logging.INFO

    set_log_level_debug()
    assert get_log_level() == logging.DEBUG
