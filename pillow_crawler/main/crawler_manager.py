# coding=utf-8
import codecs
import yaml
from pillow_crawler.data_storage.data_storage_manager import *
from pillow_crawler.downloader.downloader_manager import *
from pillow_crawler.schedular.schedular import *


class CrawlerManager:
    """所有爬虫的管理模块
    也是爬虫线程的启动与管理模块
    """
    def __init__(self, config_file_path):
        # 爬虫线程存储列表
        self.crawlers = []
        # 加载配置文件
        fi = codecs.open(config_file_path, "r", "utf-8")
        config = yaml.load(fi)
        fi.close()
        # 生成管理对象
        self.data_storage_manager = DataStorageManager(config)
        self.downloader_manager = DownloaderManager(config)
        self.schedular = Schedular()

    def set_crawlers(self, crawlers):
        # 注入管理对象
        thread_id = 0
        for crawler in crawlers:
            crawler.init(thread_id, self.schedular, self.data_storage_manager, self.downloader_manager)
            thread_id += 1
        self.crawlers.extend(crawlers)

    def add_task(self, url):
        self.schedular.put_url(url)

    def start(self):
        for crawler in self.crawlers:
            crawler.start()

    def join(self):
        for crawler in self.crawlers:
            crawler.join()

    def stop(self):
        for crawler in self.crawlers:
            if crawler.is_alive():
                crawler.terminate()




