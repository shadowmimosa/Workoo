import traceback
from types import MethodType, FunctionType

from config import DEBUG, LOGGER
# from utils import DEBUG, LOGGER


def run_func(func, *args, **kwargs):
    if isinstance(func, (MethodType, FunctionType)):
        if DEBUG:
            return func(*args, **kwargs)
        else:
            try:
                return func(*args, **kwargs)
            except:
                LOGGER.error(
                    "--->Error: The function {} is wrong, the error is {}".
                    format(func.__name__, traceback.format_exc()))

    else:
        LOGGER.error("--->Error: The type {} is wrong, the func is {}".format(
            type(func), func))
