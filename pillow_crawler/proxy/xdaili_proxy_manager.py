# coding = utf-8
from pillow_crawler.proxy.proxy_manager import *
from pillow_crawler.system.thread_lock import *
import datetime
import requests
import json


class XdailiProxyManager(ProxyManager):

    def __init__(self, config):
        ProxyManager.__init__(self)
        self.spider_id = config["spider_id"].strip()
        self.order_no = config["order_no"].strip()
        self.proxy_request_api = "http://api.xdaili.cn/xdaili-api/greatRecharge/getGreatIp?spiderId={}&orderno={}\
        &returnType=2&count=2".format(self.spider_id, self.order_no)

    def get_proxy(self):
        """获取代理"""
        if len(self.proxies) == 0:
            return None
        XDAILI_PROXY_LOCK.acquire()
        # 按使用次数排序，返回使用最少的
        proxy = sorted(self.proxies.items(), key=lambda x: x[1].use_count)[0][1]
        # 更新代理的信息
        self.proxies[proxy.key].use_count += 1
        self.proxies[proxy.key].last_use_time = datetime.datetime.now()
        XDAILI_PROXY_LOCK.release()
        return proxy

    def del_proxy(self, proxy):
        """删除代理"""
        XDAILI_PROXY_LOCK.acquire()
        if proxy.key in self.proxies:
            del self.proxies[proxy.key]
        XDAILI_PROXY_LOCK.release()
        print(len(self.proxies))

    def load_proxies(self):
        """加载代理"""
        response = requests.get(self.proxy_request_api)
        status_code = str(response.status_code)
        if not status_code.startswith("2"):
            raise Exception("get web error, response.status_code: "+status_code)
        response_obj = json.loads(response.text)
        if not response_obj["ERRORCODE"] == "0":
            raise Exception("request proxy failed! error code: "+response_obj["ERRORCODE"])
        XDAILI_PROXY_LOCK.acquire()
        for proxy_obj in response_obj["RESULT"]:
            proxy = Proxy(proxy_obj["ip"], proxy_obj["port"])
            self.proxies[proxy.key] = proxy
        XDAILI_PROXY_LOCK.release()
        print(str(self.proxies))
        print(len(self.proxies))

    def update_proxies(self):
        """ 判断代理数过多不更新"""
        XDAILI_PROXY_LOCK.acquire()
        count = len(self.proxies)
        XDAILI_PROXY_LOCK.release()
        if count >= 3:
            return
        self.load_proxies()


if __name__ == '__main__':
    config = {}
    config["spider_id"] = "68455fa7c9094730a9e2053c89f5e811"
    config["order_no"] = "YZ20182110186EPZH1G"
    xm = XdailiProxyManager(config)
    xm.load_proxies()
    p = xm.get_proxy()
    print(p.key)
    xm.del_proxy(p)

