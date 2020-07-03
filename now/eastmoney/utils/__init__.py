from utils.log import init_log
from utils.db import MongoOpea
from utils.soup import DealSoup
from utils.request import DealRequest
from utils.run import run_func, RunFunc

logger = init_log()
request = DealRequest().run
soup = DealSoup().judge
mongo = MongoOpea()

__all__ = ['logger', 'request']