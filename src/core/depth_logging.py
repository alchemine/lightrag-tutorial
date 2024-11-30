"""DepthLogger class.

Log depth of code.
"""

import contextlib
from collections import defaultdict
from functools import wraps

from src.core.timer import Timer
from src.core.logger import slog


class DepthManager(contextlib.ContextDecorator):
    """Code Depth Manager.

    Attributes:
        depth (int): Current depth of code
        depths (dict): Depths of codes
    """

    depth = 1
    depths = defaultdict(lambda: 1)

    @classmethod
    def __enter__(cls):
        cls.depth += 1
        return cls

    @classmethod
    def __exit__(cls, *exc):
        cls.depths[cls.depth] = 1  # reset
        cls.depth -= 1
        cls.depths[cls.depth] += 1
        return False


def D(fn):
    """Depth logging decorator.

    Example:
        >>> @D
        >>> def f():
        ...     # Depth: 1
        ...     g()
        >>> @D
        >>> def g():
        ...     # Depth: 2
        ...     # do something
    """

    def _print_fn(name, args, fn):
        """Print depth of code.

        Args:
            name (str): Function name
            args (tuple): Arguments of the function
            fn (callable): Function
        """
        logs = f"{'  ' + name:15}| "
        if len(args) > 0 and isinstance(
            args[0], object
        ):  # if function is method or main function
            logs = f"{logs}{fn.__module__.split('.')[-1]}."
        slog(f"{logs}{fn.__name__}()")

    @wraps(fn)
    def _log(*args, **kwargs):
        name = ".".join(
            [str(DepthManager.depths[d]) for d in range(1, DepthManager.depth + 1)]
        )
        _print_fn(name, args, fn)

        with DepthManager():
            with Timer(name):
                rst = fn(*args, **kwargs)

        return rst

    return _log
