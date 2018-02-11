# coding = utf-8
import datetime
import requests
import threading
import time


class ProxyManager(threading.Thread):
    """代理管理类"""

    def __init__(self):
        threading.Thread.__init__(self)
        self.proxies = dict()

    def run(self):
        while True:
            time.sleep(3*60)  # 每3分钟检查更新一次
            self.update_proxies()

    def get_proxy(self):
        raise NotImplementedError

    def del_proxy(self):
        raise NotImplementedError

    def load_proxies(self):
        raise NotImplementedError

    def update_proxies(self):
        raise NotImplementedError

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
        print(response.text)
        # 检查返回状态码是否是2**（代表请求成功）
        status_code = str(response.status_code)
        if not status_code.startswith("2"):
            return False
        return True


class Proxy:

    def __init__(self, ip=None, port=None):
        self.ip = ip
        self.port = port
        self.create_time = datetime.datetime.now()
        self.last_use_time = None
        self.use_count = 0
        self.key = self.ip + ":" + self.port

if __name__ == '__main__':
    proxy_manager = ProxyManager()
    proxy = Proxy("115.217.253.61", "32279")
    print(proxy_manager.check_proxy(proxy))
