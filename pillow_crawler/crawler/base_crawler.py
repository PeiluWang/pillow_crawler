# coding=utf-8
import threading
import re


class BaseCrawler(threading.Thread):

    def __init__(self, name=None):
        threading.Thread.__init__(self)
        """初始化变量"""
        self.crawler_rules = []
        self.thread_id = None
        # 设置爬虫名称，如果没有则用类名称代替
        if name:
            self.name = name
        else:
            self.name = self.__class__.__name__
        self.scheduler = None
        self.data_storage_manager = None
        self.downloader_manager = None

    def __del__(self):
        """删除变量"""
        print("关闭爬虫")

    def init(self, thread_id, scheduler, data_storage_manager, downloader_manager):
        self.thread_id = thread_id
        self.scheduler = scheduler
        self.data_storage_manager = data_storage_manager
        self.downloader_manager = downloader_manager

    def run(self):
        """任务处理线程"""
        while True:
            # 获取任务，如果队列中没有任务会阻塞
            task = self.scheduler.next_task()
            has_rule_matched = False
            # 查看处理规则匹配
            for rule in self.crawler_rules:
                if rule.url_pattern.match(task.url):
                    # 规则匹配，使用该规则处理任务
                    has_rule_matched = True
                    if not rule.download_page:
                        rule.process_func(task.url, None)
                    else:
                        if rule.downloader_name is None:
                            downloader = self.downloader_manager.get_downloader("Normal")
                        else:
                            downloader = self.downloader_manager.get_downloader(rule.downloader_name)
                        response = downloader.get_web(task.url)
                        rule.process_func(task.url, response)
            if not has_rule_matched:
                print("no rule mached! abandon!")


class CrawlerRule:

    def __init__(self, url_pattern, process_func, downloader_name="Normal", download_page=True):
        self.url_pattern = re.compile(url_pattern)
        self.process_func = process_func
        self.downloader_name = downloader_name
        self.download_page = download_page

    def __str__(self):
        return """url_pattern: {}
process_func: {}
download_type: {}
download_page: {}
        """.format(self.url_pattern, self.process_func, self.download_name, self.download_page)


if __name__ == '__main__':
    crawlerRule = CrawlerRule("",None,"name")
    print(crawlerRule)


