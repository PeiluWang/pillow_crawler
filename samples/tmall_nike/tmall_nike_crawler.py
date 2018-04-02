# coding=utf-8
import time
import random
from lxml import etree
from pillow_crawler.main.crawler_manager import *
from pillow_crawler.crawler.base_crawler import *


class TmallNikeCrawler(BaseCrawler):
    """
    天猫耐克品牌商店爬取
    """

    def __init__(self):
        BaseCrawler.__init__(self)
        self.crawler_rules = [
            CrawlerRule(
                url_pattern=r"https://list\.tmall\.com/search_product\.htm*",
                process_func=self.process_search_product,
                # downloader_name="xdaili_proxy"
            ),
            CrawlerRule(
                url_pattern=r"https://list\.tmall\.com/search_shopitem\.htm*",
                process_func=self.process_search_shopitem,
                downloader_name="downloader1"
            )
        ]

    def process_search_product(self, url, response):
        # 获取存储器
        file_storage = self.data_storage_manager.get_data_storage("file1")
        # mysql_storage = self.data_storage_manager.get_data_storage("mysql1")
        # 解析页面
        selector = etree.HTML(response)
        # 解析页面信息
        # 内容列表
        list_area = selector.xpath("//div[@id='J_ItemList\']/div")
        add_count = 0
        for item_area in list_area:
            shop = item_area.xpath("div[1]/div[1]/a")[0]
            # 商店名称
            shop_name = shop.text
            # 商店链接地址
            shop_url = shop.get("href")
            # 商店所在地（省、市）
            location_txt = list0_to_str(item_area.xpath("div[1]/div[1]/p[2]/text()"))
            location = location_txt.strip(u"所在地：")
            # 更多商品的链接地址
            more_shop_url = list0_to_str(item_area.xpath("div[2]/p/a/@href"))
            data = [shop_name, location, shop_url, more_shop_url]
            data = [str(x) for x in data]
            # print(shop_name)
            file_storage.save("tmall_nike.shop.txt", "\t".join(data))
            # 添加更多商品的链接地址到任务列表中
            if add_count >= 1:
                continue
            add_count += 1
            # self.scheduler.put_url("https://list.tmall.com/" + more_shop_url)
        # 获取翻页信息
        page_area = selector.xpath("//a[@class='ui-page-next']")
        if len(page_area) > 0:
            next_page_url = page_area[0].get("href")
            next_page_url = "https://list.tmall.com/search_product.htm" + next_page_url
            time.sleep(random.randint(2, 4))  # 随机睡2~4秒防止被封IP
            print("next page: " + next_page_url)
            self.scheduler.put_url(next_page_url)

    def process_search_shopitem(self, url, response):
        # 获取存储器
        file_storage = self.data_storage_manager.get_data_storage("file1")
        # mysql_storage = self.data_storage_manager.get_data_storage("mysql1")
        # 解析页面
        selector = etree.HTML(response)
        # 获取页面信息
        html = etree.tostring(selector)
        # print(html.decode("utf-8"))
        list_area = selector.xpath("//div[@id='J_ItemList\']/div")
        for item_area in list_area:
            price = item_area.xpath("div/p[1]/em/text()")[0]
            item_name = item_area.xpath("div/p[2]/a")[0].get("title")
            deal_num = item_area.xpath("div/p[3]/span[1]/em/text()")[0].strip(u"笔")
            comment_num = item_area.xpath("div/p[3]/span[2]/a/text()")[0]
            data = [price, item_name, deal_num, comment_num]
            # print(item_name)
            file_storage.save("tmall_nike.item.txt", "\t".join(data))
        # 获取翻页信息
        page_area = selector.xpath("//a[@class='ui-page-next']")
        if len(page_area) > 0:
            next_page_url = page_area[0].get("href")
            next_page_url = "https://list.tmall.com/search_shopitem.htm" + next_page_url
            print("next page: " + next_page_url)
            self.scheduler.put_url(next_page_url)


def main():
    # 创建爬虫管理器，加载配置文件
    config_filepath = "conf.yaml"
    crawler_manager = CrawlerManager(config_filepath)
    # 创建爬虫，添加初始任务
    tmall_crawlers = [TmallNikeCrawler() for i in range(1)]
    crawler_manager.set_crawlers(tmall_crawlers)
    # crawler_manager.add_task("https://list.tmall.com/search_product.htm?q=%C4%CD%BF%CB&style=w")
    crawler_manager.add_task("https://list.tmall.com/search_shopitem.htm?user_id=612456912&from=_1_&"
                             "stype=searchsearch_shopitem.htm?user_id=612456912&q=%C4%CD%BF%CB&sort=s&"
                             "cat=2&from=_1_&is=p")
    crawler_manager.start()
    crawler_manager.join()


if __name__ == '__main__':
    main()
