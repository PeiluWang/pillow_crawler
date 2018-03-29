# coding=utf-8
from pillow_crawler.system.singleton import *
from pillow_crawler.data_storage.mysql_storage import *
from pillow_crawler.data_storage.file_storage import *
import logging


@singleton
class DataStorageManager:

    def __init__(self, config):
        self.sys_log = logging.getLogger("sys")
        self.sys_log.debug("DataStorageManager init begin")
        # 解析配置文件
        if "data_storage" not in config:
            raise Exception("配置文件缺少data_storage配置")
        else:
            self.data_storage_dict = {}
            d_configs = config["data_storage"]
            for d_config in d_configs:
                d_type = d_config["type"]
                d_name = d_config["name"]
                if d_type == "mysql":
                    # 创建MySQL存储
                    self.data_storage_dict[d_name] = MySqlStorage(d_config)
                elif d_type == "file":
                    # 创建文件系统存储
                    self.data_storage_dict[d_name] = FileStorage(d_config)
        self.sys_log.debug("DataStorageManager init done")

    def get_data_storage(self, name):
        if name not in self.data_storage_dict:
            raise Exception("invalid data storage name: %s" % name)
        return self.data_storage_dict[name]