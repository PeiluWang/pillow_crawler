# coding = utf-8
import logging
import logging.config
import time

mylog = logging.getLogger("myapp")
mylog.setLevel(logging.DEBUG)

logger_format = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt = "%Y-%m-%d %H:%M:%S")

# 添加TimedRotatingFileHandler
# 定义一个1秒换一次log文件的handler
# 保留3个旧log文件
filehandler = logging.handlers.TimedRotatingFileHandler("myapp.log", when='S', interval=1, backupCount=3)
# 设置后缀名称，跟strftime的格式一样
filehandler.suffix = "%Y-%m-%d.log"
filehandler.setFormatter(logger_format)
mylog.addHandler(filehandler)

# 控制台
console_handler = logging.StreamHandler()
console_handler.setFormatter(logger_format)
mylog.addHandler(console_handler)

while True:
    time.sleep(0.1)
    mylog.debug("test")