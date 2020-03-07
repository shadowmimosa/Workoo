import time
import traceback
from types import MethodType, FunctionType

from config import DEBUG, logger


# def timer(func):
#     '''
#     @summary: cal the time of the fucntion
#     @param : None
#     @return: return the res of the func
#     '''

#     def wrapper(function, *args, **kw):
#         start_time = time.time()
#         # start_time = datetime.datetime.now()
#         res = func(function, *args, **kw)
#         over_time = time.time()
#         # over_time = datetime.datetime.now()
#         print('current Function {0}, run time is {1}'.format(
#             function.__name__, over_time - start_time))
#         # print ('current Function {0} run time is {1}'.format(func.__name__ , (over_time - start_time).total_seconds()))
#         return res

#     return wrapper

# @timer
def run_func(func, *args, **kwargs):
    if isinstance(func, (MethodType, FunctionType)):
        if DEBUG:
            return func(*args, **kwargs)
        else:
            try:
                return func(*args, **kwargs)
            except:
                logger.error(
                    "--->Error: The function {} is wrong, the error is {}".
                    format(func.__name__, traceback.format_exc()))

    else:
        logger.error("--->Error: The type {} is wrong, the func is {}".format(
            type(func), func))
