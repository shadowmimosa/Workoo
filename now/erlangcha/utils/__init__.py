from utils.log import init_log
from utils.soup import DealSoup
from utils.request import DealRequest
from utils.excel_opea import ExcelOpea
from utils.run import run_func, RunFunc
from utils.db import MongoOpea

logger = init_log()
request = DealRequest().run
mongo = MongoOpea()
soup = DealSoup().judge
excel = ExcelOpea()

__all__ = ['logger', 'request', 'mysql']