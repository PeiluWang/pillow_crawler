# coding = utf-8
from pillow_crawler.downloader.downloader import *
from pillow_crawler.proxy.xdaili_proxy_hub import *
import time
import logging


class ProxyDownloader(Downloader):

    def __init__(self, config, proxy_hub_manager):
        Downloader.__init__(self)
        self.sys_log.debug("..ProxyDownloader init begin")
        if "proxy_name" not in config:
            raise Exception("配置文件缺失proxy")
        proxy_name = config["proxy_name"]
        self.proxy_hub = proxy_hub_manager.get_proxy_hub(proxy_name)
        self.sys_log.debug("..ProxyDownloader init done")

    def close(self):
        self.proxy_hub.close()

    def get_web(self, url, params=None):
        """
        get请求页面
        :param url: 页面的地址
        :param params: 请求参数，格式：['key':'value',...]
        :return: 返回的页面内容
        """
        # 获取代理，如果为空则意味着当前代理都已失效，需要等待系统加载代理
        proxy = None
        while not proxy:
            proxy = self.proxy_hub.get_proxy()
            if not proxy:
                time.sleep(5)  # 如果为空5秒钟后重试

        headers = self._mock_http_headers()
        kwargs = {
            "headers": headers,
            "params": params,
            "timeout": 5,
            "proxies": {
                "http": proxy.ip + ":" + proxy.port,
            }
        }
        # "http": proxy.ip + ":" + proxy.port,
        # "https": proxy.ip + ":" + proxy.port
        try:
            self.sys_log.debug(">>>request use proxy: " + proxy.key)
            response = requests.get(url, **kwargs)
        except Exception as e:
            print(e)
            # 请求失败，检查是否是代理的原因
            if self.proxy_hub.check_proxy(proxy):
                # 代理可用，任务失败，代理失败次数+1
                self.proxy_hub.set_proxy_fail(proxy)
                self.sys_log.debug(">>>request fail but proxy is available: " + proxy.key)
                raise Exception("get web error")
            else:
                # 代理失效，删除该代理
                self.proxy_hub.del_proxy(proxy)
                self.sys_log.debug(">>>proxy is unavailable: " + proxy.key)
                raise Exception("proxy fail")
        # 检查返回状态码是否是2**（代表请求成功）
        status_code = str(response.status_code)
        if not status_code.startswith("2"):
            raise Exception("get web error, response.status_code: "+status_code)
        response.encoding = self.get_charset(response.text)
        return response.text


if __name__ == '__main__':
    config = {"proxy":{"type":"xdaili","spider_id":"68455fa7c9094730a9e2053c89f5e811","order_no":"YZ20183231685CN2h6c"}}
    downloader = ProxyDownloader(config)
    response = downloader.get_web("http://139.196.149.203:5001/crawler")
    print(response)