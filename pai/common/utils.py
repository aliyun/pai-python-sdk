from __future__ import absolute_import

import random
import re
import string
import sys
from typing import Callable, Dict, Optional, Union

from pai import __version__
from pai.common.consts import INSTANCE_TYPE_LOCAL, INSTANCE_TYPE_LOCAL_GPU

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
            result = result.items
        for item in result:
            yield item

        if len(result) == 0 or len(result) < page_size:
            return
        page_number += 1


def to_plain_text(
    input_str: str, allowed_characters=DEFAULT_PLAIN_TEXT_ALLOW_CHARACTERS, repl_ch="_"
):
    """Replace characters in input_str if it is not in allowed_characters."""
    return "".join([c if c in allowed_characters else repl_ch for c in input_str])


def http_user_agent(user_agent: Optional[Union[Dict, str]] = None) -> str:
    """Generate HTTP User-Agent that represents current client."""
    ua = f"pai-python-sdk/{__version__}; python/{sys.version.split()[0]}"
    if isinstance(user_agent, dict):
        ua += "; " + "; ".join(f"{k}/{v}" for k, v in user_agent.items())
    elif isinstance(user_agent, str):
        ua += "; " + user_agent
    return ua


def is_notebook() -> bool:
    """Return True if current environment is notebook."""
    try:
        shell = get_ipython().__class__.__name__
        for parent_cls in shell.__mro__:
            if parent_cls.__name__ == "ZMQInteractiveShell":
                return True
        return False
    except NameError:
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
