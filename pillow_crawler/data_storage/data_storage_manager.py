# coding=utf-8
from pillow_crawler.system.singleton import *
from pillow_crawler.data_storage.mysql_storage import *
from pillow_crawler.data_storage.file_storage import *


@singleton
class DataStorageManager:

    def __init__(self, config):
        # 解析配置文件
        if not "data_storage" in config:
            raise Exception("配置文件缺少data_storage配置")
        else:
            self.data_storage_dict = {}
            d_configs = config["data_storage"]
            for d_config in d_configs:
                d_type = d_config["type"]
                d_name = d_config["name"]
                if d_type=="mysql":
                    # 创建MySQL存储
                    self.data_storage_dict[d_name] = MySqlStorage(d_config)
                elif d_type=="file":
                    # 创建文件系统存储
                    self.data_storage_dict[d_name] = FileStorage(d_config)

    def get_data_storage(self, name):
        return self.data_storage_dict[name]