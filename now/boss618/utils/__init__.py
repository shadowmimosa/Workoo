from utils.log import init_log
from utils.request import DealRequest
from utils.db import MongoOpea
from utils.run import run_func

logger = init_log()
request = DealRequest().run
mongo = MongoOpea()

__all__ = ['logger', 'request', 'mongo']