# coding=utf-8
import time
from pillow_crawler.main.crawler_manager import *
from pillow_crawler.crawler.base_crawler import *


class TmallAntaCrawler(BaseCrawler):
    """
    天猫安踏品牌商店爬取
    """
    def __init__(self):
        BaseCrawler.__init__(self)
        self.crawler_rules = [
            CrawlerRule(
                url_pattern = r"https?://localhost.*",
                process_func=self.process_search_product
            ),
            CrawlerRule(
                url_pattern=r"https?://139\.196\.149\.203.*",
                process_func=self.process_search_product,
                downloader_name="xdaili_proxy"
            )
        ]

    def process_search_product(self, url, response):
        key = self.name+str(self.thread_id)+" "+str(url)+" "+str(response)
        print(key)
        # storage = self.data_storage_manager.get_data_storage("current_dir")
        # storage.save("tmall_anta3.txt", key)
        time.sleep(2)
        self.schedular.put_url(url)


def main():
    # 创建爬虫管理器，加载配置文件
    config_filepath = "common_conf.yaml"
    crawler_manager = CrawlerManager(config_filepath)
    # 创建爬虫，添加初始任务
    tmall_crawlers = [TmallAntaCrawler() for i in range(1)]
    crawler_manager.set_crawlers(tmall_crawlers)
    crawler_manager.add_task("https://list.tmall.com/search_product.htm?q=%C4%CD%BF%CB&style=w")
    # crawler_manager.add_task("http://139.196.149.203:5001/crawler")
    crawler_manager.start()
    crawler_manager.join()

if __name__ == '__main__':
    main()