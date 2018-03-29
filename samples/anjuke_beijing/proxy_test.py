# coding=utf-8
import time
import random
from lxml import etree
from pillow_crawler.main.crawler_manager import *
from pillow_crawler.crawler.base_crawler import *


class AnjukeBeijingCrawler(BaseCrawler):
    """
    用于爬取安居客北京的数据，用于租房选址
    """
    def __init__(self):
        BaseCrawler.__init__(self)
        self.crawler_rules = [
            CrawlerRule(
                url_pattern=r"http://139\.196\.149\.203/*",
                process_func=self.proxy_test,
                downloader_name="xdaili1_downloader"
            )
        ]

    def proxy_test(self, url, response):
        # 获取存储器
        print("do: "+url)
        print(response)


def main():
    # 创建爬虫管理器，加载配置文件
    config_filepath = "conf.yaml"
    crawler_manager = CrawlerManager(config_filepath)
    # 创建爬虫，添加初始任务
    crawlers = [AnjukeBeijingCrawler() for i in range(1)]
    crawler_manager.set_crawlers(crawlers)
    crawler_manager.add_task("http://139.196.149.203:5001/crawler")
    crawler_manager.start()
    crawler_manager.join()


if __name__ == '__main__':
    main()