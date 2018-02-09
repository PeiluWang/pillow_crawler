# coding = utf-8
from pillow_crawler.downloader.downloader import *


class ProxyDownloader(Downloader):

    def __init__(self):
        pass

    def get_web(self, url):
        return "proxy"