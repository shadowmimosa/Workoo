from utils.log import init_log
from utils.request import DealRequest
from utils.db import MongoOpea
from utils.run import run_func

logger = init_log()
request = DealRequest().run
mongo = MongoOpea()
request_proxy = DealRequest({
    "http": "http://dynamic.xiongmaodaili.com:8089",
    "https": "http://dynamic.xiongmaodaili.com:8089"
}).run
request_proxy_8088 = DealRequest({
    "http": "http://dynamic.xiongmaodaili.com:8088",
    "https": "http://dynamic.xiongmaodaili.com:8088"
}).run

__all__ = ['logger', 'request', 'mongo']