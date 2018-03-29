# coding = utf-8
import datetime
import requests
import threading
import time
import logging


class ProxyHub(threading.Thread):
    """代理管理类"""

    def __init__(self):
        threading.Thread.__init__(self)
        self.sys_log = logging.getLogger("sys")
        self.proxies = dict()
        self.__close = False
        self._lock = threading.Lock()

    def run(self):
        count = 0
        while not self.__close:
            time.sleep(1)
            count += 1
            # 每1秒检查一次是否跳出线程，每5秒检查代理是否需要更新
            if count < 5:
                continue
            count = 0
            self.update_proxies()

    def close(self):
        self.__close = True

    def get_proxy(self):
        """获取代理，可以考虑引入失败次数"""
        if len(self.proxies) == 0:
            return None
        self._lock.acquire()
        # 按使用次数排序，返回失败次数最少且使用次数最少的
        proxy = sorted(self.proxies.items(), key=lambda x: x[1].use_count)[0][1]
        # 更新代理的信息
        self.proxies[proxy.key].use_count += 1
        self.proxies[proxy.key].last_use_time = datetime.datetime.now()
        self._lock.release()
        return proxy

    def set_proxy_fail(self, proxy):
        """设置代理失败次数"""
        self._lock.acquire()
        if proxy.key in self.proxies:
            self.proxies[proxy.key].fail_count += 1
        self._lock.release()

    def del_proxy(self, proxy):
        """删除代理"""
        self._lock.acquire()
        if proxy.key in self.proxies:
            del self.proxies[proxy.key]
            self.sys_log.debug("delete proxy: " + str(proxy.key))
            self.sys_log.debug("remain proxy number: %d" % len(self.proxies))
        self._lock.release()

    def load_proxies(self):
        raise NotImplementedError

    def update_proxies(self):
        """ 判断代理数，不足则更新否则不更新"""
        self._lock.acquire()
        count = len(self.proxies)
        self._lock.release()
        if count >= 1:
            return
        self.load_proxies()

    def check_proxy(self, proxy):
        """检查代理是否存活"""
        proxy_config = {
            "http": proxy.ip + ":" + proxy.port,
            "https": proxy.ip + ":" + proxy.port
        }
        try:
            response = requests.get("http://139.196.149.203:5001/crawler", proxies=proxy_config, timeout=3)
        except:
            return False
        # 检查返回状态码是否是2**（代表请求成功）
        status_code = str(response.status_code)
        if not status_code.startswith("2"):
            return False
        return True

XDAILI_PROXY_LOCK = threading.Lock()
KUAIDAILI_PROXY_LOCK = threading.Lock()


class Proxy:

    def __init__(self, ip=None, port=None):
        self.ip = ip
        self.port = port
        self.create_time = datetime.datetime.now()
        self.last_use_time = None
        self.use_count = 0
        self.fail_count = 0
        self.key = self.ip + ":" + self.port

if __name__ == '__main__':
    proxy_manager = ProxyHub()
    proxy = Proxy("115.217.253.61", "32279")
    print(proxy_manager.check_proxy(proxy))
