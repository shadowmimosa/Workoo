from loguru import logger
from functools import wraps
from types import MethodType, FunctionType

from config import DEBUG


@logger.catch(reraise=True)
def reraise(func, *args, **kwargs):
    return func(*args, **kwargs)


@logger.catch()
def unraise(func, *args, **kwargs):
    return func(*args, **kwargs)


class RunFunc(object):
    def __init__(self, target='', default=None, raise_err=False):
        self.target = target
        self.default = default
        if raise_err is None and DEBUG:
            raise_err = True
        self.raise_err = raise_err

        super().__init__()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.raise_err:
                return self.reraise(func, *args, **kwargs)
            else:
                return self.unraise(func, *args, **kwargs)

        return wrapper

    @logger.catch(reraise=True)
    def reraise(self, func, *args, **kwargs):
        return func(*args, **kwargs)

    @logger.catch()
    def unraise(self, func, *args, **kwargs):
        return func(*args, **kwargs)


def run_func(target='', default=None, raise_err=None):
    if raise_err is None and DEBUG:
        raise_err = True

    def decorator(func):
        def wrapper(*args, **kwargs):
            if raise_err:
                return reraise(func, *args, **kwargs)
            else:
                return unraise(func, *args, **kwargs)

        return wrapper

    return decorator