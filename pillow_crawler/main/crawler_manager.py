# coding=utf-8
import yaml
from pillow_crawler.data_storage.data_storage_manager import *
from pillow_crawler.downloader.downloader_manager import *
from pillow_crawler.proxy.proxy_hub_manager import *
from pillow_crawler.log.logger_manager import *
from pillow_crawler.scheduler.scheduler import *


class CrawlerManager:
    """
    所有爬虫的管理模块
    """
    def __init__(self, config_file_path):
        # 爬虫线程存储列表
        self.crawlers = []
        # 加载配置文件
        fi = codecs.open(config_file_path, "r", "utf-8")
        config = yaml.load(fi)
        fi.close()
        # 初始化日志模块
        self.logger_manager = LoggerManager(config)
        self.sys_log = self.logger_manager.get_sys_log()
        # 初始化数据存储模块
        self.data_storage_manager = DataStorageManager(config)
        # 初始化代理模块
        self.proxy_hub_manager = ProxyHubManager(config)
        # 初始化下载管理模块
        self.downloader_manager = DownloaderManager(config, self.proxy_hub_manager)
        # 初始化调度器
        self.scheduler = Scheduler()
        self.sys_log.debug("CrawlerManager init done")

    def set_crawlers(self, crawlers):
        # 注入管理对象
        thread_id = 0
        for crawler in crawlers:
            crawler.init(thread_id, self.scheduler, self.data_storage_manager, self.downloader_manager,
                         self.logger_manager)
            thread_id += 1
        self.crawlers.extend(crawlers)

    def add_task(self, url):
        self.scheduler.put_url(url)

    def start(self):
        self.sys_log.debug("""
=========================
Crawler Start
crawler number: %d
task number: %d
=========================""" % (len(self.crawlers), self.scheduler.current_task_num()))
        # 启动爬虫
        for crawler in self.crawlers:
            crawler.start()
        # 启动爬虫监控程序，用于在爬取结束时关闭
        monitor = CrawlerMonitor(self.scheduler, self.crawlers, self.proxy_hub_manager)
        monitor.start()

    def join(self):
        for crawler in self.crawlers:
            crawler.join()

    def stop(self):
        for crawler in self.crawlers:
            if crawler.is_alive():
                crawler.terminate()


class CrawlerMonitor(threading.Thread):
    """
    独立的监控线程，如果所有爬虫线程均空闲，则关闭所有爬虫
    """
    def __init__(self, scheduler, crawlers, proxy_hub_manager):
        self.sys_log = logging.getLogger("sys")
        self.sys_log.debug(">>init CrawlerMonitor begin")
        threading.Thread.__init__(self)
        self.scheduler = scheduler
        self.crawlers = crawlers
        self.proxy_hub_manager = proxy_hub_manager
        self.sys_log.debug(">>init CrawlerMonitor complete")

    def __del__(self):
        pass

    def run(self):
        self.sys_log.debug(">>crawler monitor start")
        while True:
            # 检查是否所有的爬虫都不在工作，每10秒检查一次
            time.sleep(10)
            all_crawler_not_busy = True
            for crawler in self.crawlers:
                if crawler.is_busy():
                    all_crawler_not_busy = False
                    break
            if all_crawler_not_busy:
                # 关闭所有爬虫
                self.sys_log.debug("all crawlers are not busy, close all")
                for crawler in self.crawlers:
                    crawler.close()
                # 关闭代理监视线程
                self.proxy_hub_manager.close()
                break
        self.sys_log.debug("CrawlerMonitor close")


