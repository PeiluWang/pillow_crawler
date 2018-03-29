# coding = utf-8
from pillow_crawler.proxy.proxy_hub import *
from pillow_crawler.system.thread_lock import *
import datetime
import requests
import json
import logging
import threading


class KuaidailiProxyHub(ProxyHub):

    def __init__(self):
        ProxyHub.__init__(self)
        self.sys_log = logging.getLogger("sys")
        self.sys_log.debug("..KuaidailiProxyHub init begin")
        self.proxy_request_api = "http://webapi.http.zhimacangku.com/getip?num=2&type=2&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions="
        self.load_proxies()
        self.sys_log.debug("..KuaidailiProxyHub init done")

    def load_proxies(self):
        """加载代理"""
        self.sys_log.debug("....load proxies")
        response = requests.get(self.proxy_request_api)
        status_code = str(response.status_code)
        if not status_code.startswith("2"):
            raise Exception("get web error, response.status_code: "+status_code)
        response_obj = json.loads(response.text)
        if not response_obj["code"] == 0:
            raise Exception("request proxy failed! error code: " + str(response_obj["code"]))
        self._lock.acquire()
        for proxy_obj in response_obj["data"]:
            proxy = Proxy(proxy_obj["ip"], str(proxy_obj["port"]))
            self.proxies[proxy.key] = proxy
        self._lock.release()
        self.sys_log.debug("....proxies number: %d" % len(self.proxies))
        self.sys_log.debug("....%s" % str(list(self.proxies.keys())))


if __name__ == '__main__':
    xm = KuaidailiProxyHub()
    p = xm.get_proxy()
    print(p.key)
    xm.del_proxy(p)