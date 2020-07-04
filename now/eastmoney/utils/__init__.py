from utils.log import init_log
from utils.db import MongoOpea
from utils.soup import DealSoup
from utils.request import DealRequest
from utils.excel_opea import ExcelOpea
from utils.run import run_func, RunFunc

logger = init_log()
request = DealRequest().run
soup = DealSoup().judge
mongo = MongoOpea()
excel = ExcelOpea()

__all__ = ['logger', 'request']