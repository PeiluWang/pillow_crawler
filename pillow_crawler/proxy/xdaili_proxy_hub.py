# coding = utf-8
from pillow_crawler.proxy.proxy_hub import *
import datetime
import requests
import json
import logging


class XdailiProxyHub(ProxyHub):

    def __init__(self, config):
        ProxyHub.__init__(self)
        self.sys_log.debug("..XdailiProxyHub init begin")
        self.spider_id = config["spider_id"].strip()
        self.order_no = config["order_no"].strip()
        self.proxy_request_api = "http://api.xdaili.cn/xdaili-api/greatRecharge/getGreatIp?spiderId={}&orderno={}\
        &returnType=2&count=10".format(self.spider_id, self.order_no)
        self.load_proxies()
        self.sys_log.debug("..XdailiProxyHub init done")

    def load_proxies(self):
        """加载代理"""
        self.sys_log.debug("....load proxies")
        response = requests.get(self.proxy_request_api)
        status_code = str(response.status_code)
        if not status_code.startswith("2"):
            raise Exception("get web error, response.status_code: "+status_code)
        response_obj = json.loads(response.text)
        if not response_obj["ERRORCODE"] == "0":
            raise Exception("request proxy failed! error code: "+response_obj["ERRORCODE"])
        self._lock.acquire()
        for proxy_obj in response_obj["RESULT"]:
            proxy = Proxy(proxy_obj["ip"], proxy_obj["port"])
            self.proxies[proxy.key] = proxy
        self._lock.release()
        self.sys_log.debug("....proxies number: %d" % len(self.proxies))
        self.sys_log.debug("....%s" % str(list(self.proxies.keys())))


if __name__ == '__main__':
    config = {}
    config["spider_id"] = "68455fa7c9094730a9e2053c89f5e811"
    config["order_no"] = "YZ20183231685CN2h6c"
    xm = XdailiProxyHub(config)
    p = xm.get_proxy()
    print(p.key)
    xm.del_proxy(p)

