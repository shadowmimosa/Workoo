from .log import init_log
from .soup import DealSoup
from .request import DealRequest
from .run import run_func
from .signer import magic
from .excel_opea import ExcelOpea

logger = init_log()
soup = DealSoup().judge
request = DealRequest().run
excel = ExcelOpea()

request_proxy = DealRequest({
    "http": "http://dynamic.xiongmaodaili.com:8089",
    "https": "http://dynamic.xiongmaodaili.com:8089"
}).run
