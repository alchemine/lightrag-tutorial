"""Utility module.

Commonly used functions and classes are here.
"""

from itertools import starmap
from datetime import datetime

import numpy as np

# from tabulate import tabulate


# tprint = lambda dic: print(
#     tabulate(dic, headers="keys", tablefmt="psql")
# )  # print with fancy 'psql' format
vars_ = lambda obj: {k: v for k, v in vars(obj).items() if not k.startswith("__")}
str2dt = lambda s, format="%Y-%m-%d": datetime.datetime.strptime(s, format)
dt2str = lambda dt, format="%Y-%m-%d": dt.strftime(format)


def str2bool(s: str | bool) -> bool:
    """String to boolean."""
    if isinstance(s, bool):
        return s
    if s.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif s.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise ValueError(f"Invalid input: {s} (type: {type(s)})")


class MetaSingleton(type):
    """Meta singleton.

    Example:
        >>> class A(metaclass=MetaSingleton):
        ...     pass
        >>> a1 = A()
        >>> a2 = A()
        >>> assert a1 is a2
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonManager:
    """Singleton manager
    This class assures that only one instance is created.

    Attributes:
        instance: Singleton instance
    """

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instances = {}
        return super().__new__(cls)

    def get_instance(self, key):
        """Get or create an instance for the given key"""
        if key not in self.instances:
            self.instances[key] = object()  # 실제 인스턴스 생성 로직으로 대체해야 함
        return self.instances[key]

    def set_instance(self, key, instance):
        """Set an instance for the given key"""
        self.instances[key] = instance

    def has_instance(self, key):
        """Check if an instance exists for the given key"""
        return key in self.instances


SINGLETON_MANAGER = SingletonManager()
