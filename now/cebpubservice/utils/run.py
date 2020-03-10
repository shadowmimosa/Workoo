import traceback
import inspect
from types import MethodType, FunctionType

from utils.log import logger, DEBUG


def run_func(func, *args, **kwargs):
    # # if isinstance(func, (MethodType, FunctionType)):
    # if inspect.isfunction(func) or inspect.ismethod(func):
    #     if DEBUG:
    #         return func(*args, **kwargs)
    #     else:
    #         try:
    #             return func(*args, **kwargs)
    #         except:
    #             logger.error(
    #                 "--->Error: The function {} is wrong, the error is {}".
    #                 format(func.__name__, traceback.format_exc()))
    #             return False

    # else:
    #     logger.error("--->Error: The type {} is wrong, the func is {}".format(
    #         type(func), func))
    #     return False

    if DEBUG:
        return func(*args, **kwargs)
    else:
        try:
            return func(*args, **kwargs)
        except:
            logger.error(
                "--->Error: The function {} is wrong, the error is {}".format(
                    func.__name__, traceback.format_exc()))
            return False
