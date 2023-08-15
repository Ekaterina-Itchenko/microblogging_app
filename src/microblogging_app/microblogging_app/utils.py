import functools
import logging
from typing import Callable, ParamSpec, TypeVar

from django.db import connection, reset_queries

logger = logging.getLogger(__name__)

RT = TypeVar("RT")
P = ParamSpec("P")


def query_debugger(func: Callable[P, RT]) -> Callable[P, None]:
    """Decorator for calculation a quantity of queries."""

    @functools.wraps(func)
    def inner_func(*args: P.args, **kwargs: P.kwargs) -> None:
        reset_queries()
        start_queries = len(connection.queries)
        func(*args, **kwargs)
        end_queries = len(connection.queries)
        logger.info(msg=f"QUERIES QUANTITY {end_queries - start_queries}")

    return inner_func
