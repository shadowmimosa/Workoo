from .db import MysqlOpea
from .run import run_func
from .baidu_ocr import BaiduOCR
from .log import init_log

mysql = MysqlOpea()
ocr = BaiduOCR()
logger = init_log()
