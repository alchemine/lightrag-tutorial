"""Timer class.

Context and decorator form timer.
"""

import contextlib
from functools import wraps
from time import perf_counter

from src.core.logger import slog


class Timer(contextlib.ContextDecorator):
    """Timer.

    Examples:
        >>> with Timer('Code1'):
        ...     sleep(1)
        * Code1        | 1.00s (0.02m)
    """

    def __init__(self, name="Elapsed time"):
        self.name = name

    def __enter__(self):
        self.start_time = perf_counter()
        return self

    def __exit__(self, *exc):
        elapsed_time = perf_counter() - self.start_time
        slog(f"{'* ' + self.name:15}| {elapsed_time:.2f}s ({elapsed_time/60:.2f}m)")
        return False


def T(fn: callable) -> callable:
    """Timer decorator.

    Example:
        >>> @T
        >>> def f():
        ...     sleep(1)
        * Elapsed time | 1.00s (0.02m)
    """

    @wraps(fn)
    def _log(*args, **kwargs):
        with Timer(fn.__name__):
            rst = fn(*args, **kwargs)
        return rst

    return _log
