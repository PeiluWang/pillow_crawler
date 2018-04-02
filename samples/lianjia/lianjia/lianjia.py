# coding=utf-8
import sys

sys.path.append('../../')
from lxml import etree
import random
from pillow_crawler.main.crawler_manager import *
from pillow_crawler.crawler.base_crawler import *


class LianjiaCrawler(BaseCrawler):
    def __init__(self):
        BaseCrawler.__init__(self, "Lianjia")
        self.base_url = "https://sh.lianjia.com"
        self.total_page = 0
        self.cur_page = 0
        self.crawler_rules = [
            CrawlerRule(
                url_pattern=r"https://sh.lianjia.com/ershoufang/rs*",
                process_func=self.process_lianjia_item,
            ),
            CrawlerRule(
                url_pattern=r"https://sh.lianjia.com/ershoufang/pg*",
                process_func=self.process_lianjia_item,
            )
        ]

    def process_lianjia_item(self, url, response):
        # 获取存储器
        file_storage = self.data_storage_manager.get_data_storage("current_dir")
        # 解析页面
        selector = etree.HTML(response)
        # 获取页面信息
        result = selector.xpath("/html/body/div[4]/div[1]/ul/li")
        for div in result:
            # 显示名称
            house_name = div.xpath("div[1]/div[1]/a")[0].text
            house_location = div.xpath("div[1]/div[2]/div/text()")[0]
            data = [house_name, house_location]
            file_storage.save("lianjia.txt", "\t".join(data))
        # 翻页信息
        result = selector.xpath("/html/body/div[4]/div[1]/div[7]/div[2]/div")[0]
        if result is not None:
            self.total_page = eval(result.get('page-data'))['totalPage']
            self.cur_page += 1
            if not self.cur_page > self.total_page:
                time.sleep(random.randint(2, 4))  # 随机睡2~4秒防止被封IP
                self.scheduler.put_url(self.base_url + str(result.get('page-url')).format(page=self.cur_page))


def main():
    # 创建爬虫管理器，加载配置文件
    config_filepath = "conf.yaml"
    crawler_manager = CrawlerManager(config_filepath)
    # 创建爬虫，添加初始任务
    crawlers = [LianjiaCrawler() for i in range(3)]
    crawler_manager.set_crawlers(crawlers)
    crawler_manager.add_task("https://sh.lianjia.com/ershoufang/rs%E4%B8%8A%E6%B5%B7%E5%BA%B7%E5%9F%8E/")
    # 开启爬取
    crawler_manager.start()
    crawler_manager.join()


if __name__ == '__main__':
    main()
