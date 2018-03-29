# coding=utf-8
import threading
import re
import time


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
        self.logger_manager = None
        self.sys_log = None
        self.key = "" # 线程的名称+线程id，用于日志分析
        self.__is_busy = False # 是否正在工作
        self.__close = False # 关闭标记位

    def __del__(self):
        pass

    def close(self):
        self.__close = True

    def is_busy(self):
        return self.__is_busy

    def init(self, thread_id, scheduler, data_storage_manager, downloader_manager, logger_manager):
        self.thread_id = thread_id
        self.scheduler = scheduler
        self.data_storage_manager = data_storage_manager
        self.downloader_manager = downloader_manager
        self.logger_manager = logger_manager
        self.sys_log = logger_manager.get_sys_log()
        self.key = self.name + str(self.thread_id)

    def run(self):
        """任务处理线程"""
        self.sys_log.debug(self.key + " start")
        while not self.__close:
            # 设置繁忙状态位，用于判断程序是否结束
            self.__is_busy = False
            # 获取任务，如果队列中没有任务会返回None
            task = self.scheduler.next_task()
            if task is None:
                # 如果没有下一个任务，则休息3秒再检查
                time.sleep(3)
                continue
            self.__is_busy = True
            # 开始执行任务
            self.sys_log.debug(self.key + " " + task.url + " start")
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
                        try:
                            response = downloader.get_web(task.url)
                            self.sys_log.debug(self.key + " " + task.url + " get web done")
                        except Exception as e:
                            # 获取页面失败
                            err_msg = str(e)
                            if err_msg.startswith("get web error"):
                                # 任务有问题，失败次数加一，添加入队列
                                task.fail_count += 1
                                if task.fail_count >= 3:
                                    self.sys_log.error(self.key + " " + task.url + " get web fail 3 times!")
                                else:
                                    self.sys_log.error(self.key + " " + task.url + " get web fail")
                                    self.scheduler.put_task(task)
                            else:
                                # 代理有问题，任务重新加入队列
                                self.sys_log.error(self.key + " " + task.url + " proxy fail")
                                self.scheduler.put_task(task)
                            break
                        rule.process_func(task.url, response)
                        self.sys_log.info(self.key + " " + task.url + " process done")
            if not has_rule_matched:
                self.sys_log.warn(self.key + " " + task.url + " no rule matched")
        self.sys_log.debug(self.key + " close")


def list0_to_str(input_list):
    """
    解析etree时常用的函数
    示例
    输入：['hello']
    输出：‘hello’
    """
    if len(input_list) > 0:
        return str(input_list[0])
    return ""


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


