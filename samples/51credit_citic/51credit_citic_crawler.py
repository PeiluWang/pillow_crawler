# coding=utf-8
import sys
sys.path.append('../../')
from lxml import etree
import random
from pillow_crawler.main.crawler_manager import *
from pillow_crawler.crawler.base_crawler import *


class TestCrawler(BaseCrawler):

    def __init__(self):
        BaseCrawler.__init__(self, "51CreditCardCitic")
        self.crawler_rules = [
            CrawlerRule(
                url_pattern=r"https?://kaku\.51credit\.com/citic*",
                process_func=self.process_extract_credit_card,
            )
        ]

    def process_extract_credit_card(self, url, response):
        # 获取存储器
        file_storage = self.data_storage_manager.get_data_storage("current_dir")
        # 解析页面
        selector = etree.HTML(response)
        # 获取页面信息
        result = selector.xpath("//div[@class='content-w']/div[@class='content']/div[@class='iteam']")
        for div in result:
            # 卡名称
            card_name = div.xpath("div[1]/a[2]")[0].text
            card_cash_type = div.xpath("div[2]/div[1]/span[1]/i")[0].text
            card_org = div.xpath("div[2]/div[1]/span[2]/i")[0].text
            card_rank = div.xpath("div[2]/div[1]/span[3]/i")[0].text
            cash_amount = div.xpath("div[2]/div[1]/span[4]/i")[0].text
            free_interest = div.xpath("div[2]/div[1]/span[5]/i")[0].text
            score_rule = div.xpath("div[2]/div[2]/p[1]")[0].text
            free_policy = div.xpath("div[2]/div[2]/p[2]")[0].text
            data = [card_name,card_cash_type,card_org,card_rank,cash_amount,free_interest,score_rule,free_policy]
            file_storage.save("citic_card.txt", "\t".join(data))
        # 翻页信息
        result = selector.xpath("//div[@class='page-box']/ul/li[@class='next-page']/a")
        if (result is not None) and len(result) > 0:
            next_page_href = result[0].get("href")
            time.sleep(random.randint(2,4)) # 随机睡2~4秒防止被封IP
            self.scheduler.put_url("https:" + next_page_href)


def main():
    # 创建爬虫管理器，加载配置文件
    config_filepath = "conf.yaml"
    crawler_manager = CrawlerManager(config_filepath)
    # 创建爬虫，添加初始任务
    crawlers = [TestCrawler() for i in range(3)]
    crawler_manager.set_crawlers(crawlers)
    crawler_manager.add_task("https://kaku.51credit.com/citic/")
    # 开启爬取
    crawler_manager.start()
    crawler_manager.join()

if __name__ == '__main__':
    main()
