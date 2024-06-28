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

import functools
import importlib.util
import random
import re
import socket
import string
import sys
import time
import warnings
from datetime import datetime
from functools import lru_cache
from typing import Callable, Dict, List, Optional, Union

from semantic_version import Version

from pai.common.consts import (
    INSTANCE_TYPE_LOCAL,
    INSTANCE_TYPE_LOCAL_GPU,
    FileSystemInputScheme,
)
from pai.version import VERSION

DEFAULT_PLAIN_TEXT_ALLOW_CHARACTERS = string.ascii_letters + string.digits + "_"


def is_iterable(arg):
    try:
        _ = iter(arg)
        return True
    except TypeError:
        return False


def random_str(n):
    """Random string generation with lower case letters and digits.

    Args:
        n: Size of generated random string.

    Returns:
        str: generated random string.

    """
    return "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(n)
    )


def camel_to_snake(name):
    """Convert a name from camel case to snake case."""
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def snake_to_camel(name):
    """Convert a name from snake case to camel case."""
    return "".join([w.title() for w in name.split("_")])


def make_list_resource_iterator(method: Callable, **kwargs):
    """Wrap resource list method as an iterator.

    Args:
        method: Resource List method.
        **kwargs: arguments for the method.

    Yields:
        A resource iterator.
    """

    from pai.api.base import PaginatedResult

    page_number = kwargs.get("page_number", 1)
    page_size = kwargs.get("page_size", 10)

    while True:
        kwargs.update(page_number=page_number, page_size=page_size)
        result = method(**kwargs)
        if isinstance(result, PaginatedResult):
            total_count = result.total_count
            result = result.items
        else:
            total_count = None
        for item in result:
            yield item

        if len(result) == 0 or len(result) < page_size:
            return
        if total_count and page_number * page_size >= total_count:
            return

        page_number += 1


def to_plain_text(
    input_str: str, allowed_characters=DEFAULT_PLAIN_TEXT_ALLOW_CHARACTERS, repl_ch="_"
):
    """Replace characters in input_str if it is not in allowed_characters."""
    return "".join([c if c in allowed_characters else repl_ch for c in input_str])


def http_user_agent(user_agent: Optional[Union[Dict, str]] = None) -> str:
    """Generate HTTP User-Agent that represents current client."""
    ua = f"pai-python-sdk/{VERSION}; python/{sys.version.split()[0]}"
    if isinstance(user_agent, dict):
        ua += "; " + "; ".join(f"{k}/{v}" for k, v in user_agent.items())
    elif isinstance(user_agent, str):
        ua += "; " + user_agent
    return ua


def is_notebook() -> bool:
    """Return True if current environment is notebook."""
    try:
        from IPython import get_ipython

        shell = get_ipython().__class__.__name__
        for parent_cls in shell.__mro__:
            if parent_cls.__name__ == "ZMQInteractiveShell":
                return True
        return False
    except (NameError, ImportError):
        return False


def is_local_run_instance_type(instance_type: str) -> bool:
    """Return True if instance_type is local run instance type."""
    return instance_type and instance_type.strip() in [
        INSTANCE_TYPE_LOCAL_GPU,
        INSTANCE_TYPE_LOCAL,
    ]


def generate_repr(repr_obj, *attr_names: str, **kwargs) -> str:
    """Generate a string representation of the given object.

    Args:
        repr_obj: The object used to generate the string representation.
        attr_names: A list of attribute names to include in the string representation.

    Returns:
        str: A string representation of the object.

    """
    attrs = {name: getattr(repr_obj, name) for name in attr_names}
    attrs.update(kwargs)
    attr_repr = ", ".join(["{}={}".format(k, v) for k, v in attrs.items()])
    cls_name = repr_obj.__class__.__name__

    return f"{cls_name}({attr_repr})"


def to_semantic_version(version_str: str) -> Version:
    """Convert version_str to semantic version.

    Convert version_str to semantic version, if version_str is not a valid
    semantic version, return '0.0.0'.

    Args:
        version_str[str]: Version string, such as '1.0.0', '1.0.0-rc1', '1.0.0+build.1'.

    Returns:
        :class:`semantic_version.Version`: Semantic version.
    """
    try:
        return Version.coerce(version_str)
    except ValueError:
        # if version_str is not a valid semantic version, return '0.0.0'
        return Version.coerce("0.0.0")


def is_odps_table_uri(uri: str) -> bool:
    """Return True if uri is an odps table input URI.

    Args:
        uri (str): URI of input table, such as 'odps://<project_name>/tables/<table_name>'.

    Examples:
        >>> is_odps_table_uri('odps://<project_name>/tables/<table_name>')
        True

    """
    if not uri.startswith("odps://"):
        return False
    info = uri[7:].split("/", 2)
    if len(info) != 3:
        return False
    return info[1] == "tables"


def is_filesystem_uri(uri: str) -> bool:
    """Return True if uri is a filesystem input URI.

    Args:
        uri (str): URI of input NAS, such as 'nas://<FileSystemId>/path/to/data/directory/'.

    Examples:
        # Standard or Extreme file system type
        >>> is_filesystem_uri('nas://<FileSystemId>/path/to/data/directory/')
        True
        # CPFS file system type
        >>> is_filesystem_uri('cpfs://<FileSystemId>/<ProtocolServiceId>/<ExportId>')
        True

    """
    schemas = {
        v for k, v in FileSystemInputScheme.__dict__.items() if not k.startswith("__")
    }

    return any(uri.startswith(f"{schema}://") for schema in schemas)


def is_dataset_id(item: str) -> bool:
    """Return True if given input is a dataset ID.

    Args:
        item (str): user input dataset ID.

    Examples:
        >>> is_dataset_id('d-ybko3rap60c4gs9flc')
        True
    """
    return item.startswith("d-")


@lru_cache()
def is_domain_connectable(domain: str, port: int = 80, timeout: int = 1) -> bool:
    """Check if the domain is connectable."""

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set the timeout for the socket
    sock.settimeout(timeout)
    try:
        # Get the IP address of the domain
        ip = socket.gethostbyname(domain)
        # Try to connect to the IP address on specific port (default 80, HTTP)
        sock.connect((ip, port))
        # If the connection is successful, return True
        return True
    except (socket.timeout, socket.gaierror, socket.error):
        # If there is an error connecting, return False
        return False
    finally:
        # Close the socket
        sock.close()


def experimental(callable_entity):
    """Decorator to mark functions or classes as experimental"""

    @functools.wraps(callable_entity)
    def wrapper(*args, **kwargs):
        message = f"{callable_entity.__name__} is experimental and may change or be removed in future releases."
        warnings.warn(message, category=FutureWarning, stacklevel=2)
        return callable_entity(*args, **kwargs)

    return wrapper


def retry(max_attempts=3, wait_secs=1, exceptions=(Exception,), report_retries=True):
    """Decorator to make functions retry by config"""

    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    result = func(*args, **kwargs)
                    return result
                except exceptions as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise  # Re-raise the last exception when all the attempts have failed
                    if report_retries:
                        warnings.warn(f"Retry {attempts}/{max_attempts} failed: {e}")
                    time.sleep(wait_secs)

        return wrapper

    return decorator_retry


def print_table(headers: List[str], rows: List[List[str]]):
    """Give headers and rows, print as table to stdout."""

    length = len(headers)
    for row in rows:
        if len(row) != length:
            raise ValueError("Unable to print table, headers length mismatch with rows")

    column_widths = [
        max(len(str(value)) for value in column) for column in zip(headers, *rows)
    ]
    header_row = " | ".join(
        f"{header:<{column_widths[i]}}" for i, header in enumerate(headers)
    )

    print(header_row)
    print("-" * len(header_row))
    for row in rows:
        print(
            " | ".join(
                f"{str(value):<{column_widths[i]}}" for i, value in enumerate(row)
            )
        )


def is_package_available(package_name: str) -> bool:
    """Check if the package is available in the current environment."""
    return True if importlib.util.find_spec(package_name) is not None else False


def timestamp(sep: str = "-", utc: bool = False) -> str:
    """Return a timestamp with millisecond precision.

    Args:
        sep: The separator between date and time.
        utc: Whether to use UTC time.

    Returns:
        str: A timestamp with millisecond precision.

    """
    if utc:
        res = datetime.utcnow().strftime("%Y%m%d-%H%M%S-%f")[:-3]
    else:
        res = datetime.now().strftime("%Y%m%d-%H%M%S-%f")[:-3]
    if sep != "-":
        res = res.replace("-", sep)
    return res


def name_from_base(base_name: str, sep: str = "-") -> str:
    """Return a name with base_name and timestamp.

    Args:
        base_name: The base name of the returned name.
        sep: The separator between base_name and timestamp.

    Returns:
        str: A name with base_name and timestamp.

    """
    return "{base_name}{sep}{timestamp}".format(
        base_name=base_name, sep=sep, timestamp=timestamp(sep=sep, utc=False)
    )
