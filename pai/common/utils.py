from __future__ import absolute_import

import random
import re
import string
from typing import Callable

import six

from .. import __version__

DEFAULT_PLAIN_TEXT_ALLOW_CHARACTERS = string.ascii_letters + string.digits + "_"


def iter_with_limit(iterator, limit):
    if not isinstance(limit, six.integer_types) or limit <= 0:
        raise ValueError("'limit' should be positive integer")
    idx = 0
    for item in iterator:
        yield item
        idx += 1
        if idx >= limit:
            return


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


def default_user_agent() -> str:
    """Generate default User-Agent that represents current client."""
    return "PAI-Python-SDK/{}".format(__version__)
