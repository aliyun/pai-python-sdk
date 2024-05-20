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
import os
import threading
from typing import Optional

PAI_LOG_LEVEL = "PAI_LOG_LEVEL"


_lock = threading.Lock()
_default_handler: Optional[logging.Handler] = None

_LOG_LEVEL_MAPPING = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

_default_log_level = logging.WARNING


def _get_default_logging_level():
    """Get the default logging level for the pai library."""
    level_str = os.getenv(PAI_LOG_LEVEL, None)
    if level_str:
        if level_str.lower() in _LOG_LEVEL_MAPPING:
            return _LOG_LEVEL_MAPPING[level_str.lower()]
        else:
            logging.getLogger().warning(
                f"Unknown option PAI_LOG_LEVEL={level_str}, "
                f"has to be one of: { ', '.join(_LOG_LEVEL_MAPPING.keys()) }"
            )
    return _default_log_level


def _get_library_name() -> str:
    return __name__.split(".")[0]


def _get_library_root_logger() -> logging.Logger:
    return logging.getLogger(_get_library_name())


def _configure_library_root_logger() -> None:
    global _default_handler

    with _lock:
        if _default_handler:
            return
        handler = logging.StreamHandler()
        library_root_logger = _get_library_root_logger()
        library_root_logger.addHandler(handler)
        library_root_logger.setLevel(_get_default_logging_level())
        library_root_logger.propagate = False
        _default_handler = handler


def _reset_library_root_logger() -> None:
    global _default_handler

    with _lock:
        if not _default_handler:
            return
        library_root_logger = _get_library_root_logger()
        library_root_logger.removeHandler(_default_handler)
        library_root_logger.setLevel(logging.NOTSET)
        _default_handler = None


def get_log_levels_dict():
    return _LOG_LEVEL_MAPPING


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Return a logger with the specified module name.
    """

    if name is None:
        name = _get_library_name()

    _configure_library_root_logger()
    return logging.getLogger(name)


def get_log_level() -> int:
    """
    Return the current level for the "pai" module.

    Returns:
        `int`: The logging level.
    """

    _configure_library_root_logger()
    return _get_library_root_logger().getEffectiveLevel()


def set_log_level(verbosity: int) -> None:
    """
    Set the log level for the pai root logger.
    """

    _configure_library_root_logger()
    _get_library_root_logger().setLevel(verbosity)


def set_log_level_info():
    """Set the log level  to the `INFO` level."""
    return set_log_level(logging.INFO)


def set_log_level_warning():
    """Set the log level to the `WARNING` level."""
    return set_log_level(logging.WARNING)


def set_log_level_debug():
    """Set the log level to the `DEBUG` level."""
    return set_log_level(logging.DEBUG)


def set_log_level_error():
    """Set the log level to the `ERROR` level."""
    return set_log_level(logging.ERROR)
