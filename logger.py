import logging
import logging.handlers
import datetime

logger = logging.getLogger("mylogger")
logger.setLevel(logging.INFO)
formatter = logging.Formatter(fmt="%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s - %(message)s",
                                  datefmt="%m/%d/%Y %I:%M:%S %p")

console = logging.StreamHandler() # 配置日志输出到控制台
# console.setLevel(logging.INFO) # 设置输出到控制台的最低日志级别
console.setFormatter(formatter)  # 设置格式
logger.addHandler(console)

rf_handler = logging.handlers.TimedRotatingFileHandler(
    "crawler.log",
    when="midnight",
    interval=1,
    backupCount=7,
    atTime=datetime.time(0, 0, 0, 0),
)
# rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
rf_handler.setFormatter(formatter)

logger.addHandler(rf_handler)

