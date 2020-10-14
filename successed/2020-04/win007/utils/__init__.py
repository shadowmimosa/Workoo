from utils.log import init_log
from utils.soup import DealSoup
from utils.request import DealRequest
from utils.excel_opea import ExcelOpea

logger = init_log()
request = DealRequest().run
soup = DealSoup().judge
excel = ExcelOpea()

__all__ = ['logger', 'request', 'mysql']