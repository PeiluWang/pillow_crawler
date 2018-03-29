# coding=utf-8
import codecs
import requests
import re
import logging
import random


class Downloader:
    """
    一般网页的下载器，未用代理、selenium动态加载
    """
    def __init__(self):
        self.sys_log = logging.getLogger("sys")
        pass

    def get_web(self, url, params=None):
        """
        get请求页面
        :param url: 页面的地址
        :param params: 请求参数，格式：['key':'value',...]
        :return: 返回的页面内容
        """
        headers = self._mock_http_headers()
        kwargs = {
            "headers": headers,
            "params": params,
            "timeout": 5
        }
        response = requests.get(url, **kwargs)
        # 检查返回状态码是否是2**（代表请求成功）
        status_code = str(response.status_code)
        if not status_code.startswith("2"):
            raise Exception("get web error, response.status_code: "+status_code)
        response.encoding = self.get_charset(response.text)
        return response.text

    def get_charset(self, page):
        """
        判断页面编码
        :param page:
        :return:
        """
        match_obj = re.search(r"<meta charset=\"(.+?)\"\s*/?>", page)
        valid_charset = {"utf-8", "gbk", "gb2312", "gb18030"}
        if match_obj:
            charset_txt = match_obj.group(1).strip()
            # 检查charset的合法性
            if charset_txt == "utf-8" or charset_txt == "utf8":
                charset_txt = "utf-8"
            if charset_txt in valid_charset:
                self.sys_log.debug("charset: "+charset_txt)
                return charset_txt
            self.sys_log.error("invalid charset: "+charset_txt)
        # 没有找到编码，默认返回utf8
        self.sys_log.error("invalid charset, no charset matched")
        return "utf-8"

    def _mock_http_headers(self):
        random_ip = self._random_ip()
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "*",
            "Accept-Language": "zh-CN",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
        }
        return headers

    def _random_ip(self):
        """随机生成ip"""
        ip1 = random.randint(10, 245)
        ip2 = random.randint(10, 245)
        ip3 = random.randint(10, 245)
        ip4 = random.randint(10, 245)
        return "%d.%d.%d.%d" % (ip1, ip2, ip3, ip4)


if __name__ == '__main__':
    downloader = Downloader()
    response = downloader.get_web("https://kaku.51credit.com/citic/")
    print(response)
    fo = codecs.open("testpage.html","w","utf-8")
    fo.write(response)
    fo.close()
