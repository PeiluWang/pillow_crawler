# coding=utf-8
from enum import Enum
from pillow_crawler.system.singleton import *
from pillow_crawler.downloader.proxy_downloader import *


# 下载器类型枚举
DownloaderType = Enum('DownloaderType',('Normal','Proxy','Selenium','IE'))


@singleton
class DownloaderManager:

    def __init__(self, config):
        # 解析配置文件
        if not "downloader" in config:
            raise Exception("配置文件缺少downloader配置")
        else:
            self.downloader_dict = {}
            d_configs = config["downloader"]
            for d_config in d_configs:
                d_type = d_config["type"]
                d_name = d_config["name"]
                if d_type == "proxy":
                    # 创建proxy downloader
                    downloader = ProxyDownloader(d_config)
                    self.downloader_dict[d_name] = downloader
            # 创建Normal downloader
            self.downloader_dict["Normal"] = Downloader()

    def get_downloader(self, name):
        return self.downloader_dict[name]

