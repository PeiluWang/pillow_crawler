# coding = utf-8
import logging
import logging.config
import os
from pillow_crawler.system.singleton import *
"""
logging模块参考：
https://docs.python.org/2/library/logging.config.html#module-logging.config
"""


@singleton
class LoggerManager:

    def __init__(self, config):
        # 解析配置文件，检查参数合法性
        if "log" not in config:
            raise Exception("配置文件缺少log配置")
        log_configs = config["log"]
        if "log_dir" not in log_configs:
            raise Exception("配置文件缺少log_dir配置")
        self.log_dir = log_configs["log_dir"]
        if not os.path.exists(self.log_dir):
            raise Exception("日志文件夹路径不存在：%s"%self.log_dir)
        self.log_level = "DEBUG"
        if "log_level" in log_configs:
            self.log_level = log_configs["log_level"].strip().upper()
        # 初始化logger
        self.sys_log = self.__init_sys_log()
        self.sys_log.debug("LoggerManager init done")

    def __init_sys_log(self):
        # 初始化系统日志模块
        sys_log = logging.getLogger("sys")
        logger_level = logging.DEBUG
        if self.log_level == "DEBUG":
            logger_level = logging.DEBUG
        elif self.log_level == "INFO":
            logger_level = logging.INFO
        elif self.log_level == "WARN":
            logger_level = logging.WARN
        elif self.log_level == "ERROR":
            logger_level = logging.ERROR
        else:
            raise Exception("配置选项log_level值错误: %s"%self.log_level)
        sys_log.setLevel(logger_level)
        # formatter
        sys_log_format = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        # 添加TimeRotatingFileHandler，每天切割日志文件，保留全部日志
        log_file = self.log_dir + "/sys.log"
        file_handler = logging.handlers.TimedRotatingFileHandler(log_file, when='D', interval=1, backupCount=0)
        file_handler.suffix = "%Y-%m-%d.log"
        file_handler.setFormatter(sys_log_format)
        sys_log.addHandler(file_handler)
        # 控制台输出
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(sys_log_format)
        sys_log.addHandler(console_handler)
        return sys_log

    def get_sys_log(self):
        return self.sys_log

