# coding = utf-8
from pillow_crawler.downloader.downloader import *
from pillow_crawler.proxy.xdaili_proxy_manager import *
import time


class ProxyDownloader(Downloader):

    def __init__(self, config):
        if "proxy" not in config:
            raise Exception("配置文件缺失proxy")
        proxy_config = config["proxy"]
        if proxy_config["type"]=="xdaili":
            self.proxy_manager = XdailiProxyManager(proxy_config)
        else:
            raise Exception("不合法的代理类型：{}".format(proxy_config["type"]))
        self.proxy_manager.load_proxies()
        self.proxy_manager.start()  # 自检查线程

    def get_web(self, url, params=None):
        """
        get请求页面
        :param url: 页面的地址
        :param params: 请求参数，格式：['key':'value',...]
        :return: 返回的页面内容
        """
        # 获取代理，如果为空则继续尝试获取
        proxy = None
        while not proxy:
            proxy = self.proxy_manager.get_proxy()
            if not proxy:
                time.sleep(5)  # 如果为空5秒钟后重试

        headers = self._mock_http_headers()
        kwargs = {
            "headers": headers,
            "params": params,
            "timeout": 5,
            "proxies": {
                "http": proxy.ip + ":" + proxy.port,
                "https": proxy.ip + ":" + proxy.port
            }
        }
        try:
            response = requests.get(url, **kwargs)
        except:
            # 请求失败，检查是否是代理的原因
            if self.proxy_manager.check_proxy(proxy):
                # 代理可用，任务失败
                raise Exception("get web error")
            else:
                # 代理失效，删除该代理
                self.proxy_manager.del_proxy(proxy)
                raise Exception("proxy fail")
        # 检查返回状态码是否是2**（代表请求成功）
        status_code = str(response.status_code)
        if not status_code.startswith("2"):
            raise Exception("get web error, response.status_code: "+status_code)
        return response.text


if __name__ == '__main__':
    config = {"proxy":{"type":"xdaili","spider_id":"68455fa7c9094730a9e2053c89f5e811","order_no":"YZ20182110186EPZH1G"}}
    downloader = ProxyDownloader(config)
    response = downloader.get_web("http://139.196.149.203:5001/crawler")
    print(response)
    response = downloader.get_web("http://139.196.149.203:5001/crawler")
    print(response)
    response = downloader.get_web("http://139.196.149.203:5001/crawler")
    print(response)