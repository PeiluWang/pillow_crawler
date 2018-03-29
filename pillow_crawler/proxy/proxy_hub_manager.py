# coding=utf-8
import logging
from pillow_crawler.proxy.xdaili_proxy_hub import *
from pillow_crawler.proxy.kuaidaili_proxy_hub import *


class ProxyHubManager:
    """
    所有代理中心的管理模块
    """

    def __init__(self, config):
        self.sys_log = logging.getLogger("sys")
        self.sys_log.debug("ProxyHubManager init begin")
        # 解析配置文件
        if "proxy" not in config:
            self.sys_log.debug("no proxy config")
        else:
            self.proxy_hub_dict = {}
            proxy_configs = config["proxy"]
            for proxy_config in proxy_configs:
                proxy_type = proxy_config["type"]
                proxy_name = proxy_config["name"]
                proxy_hub = None
                if proxy_type == "xdaili": # 讯代理
                    proxy_hub = XdailiProxyHub(proxy_config)
                elif proxy_type == "kuaidaili": # 快代理
                    proxy_hub = KuaidailiProxyHub()
                else:
                    raise Exception("invalid proxy_type: %s" % proxy_type)
                self.proxy_hub_dict[proxy_name] = proxy_hub
                proxy_hub.start()  # 自检查线程
        self.sys_log.debug("ProxyHubManager init done")

    def get_proxy_hub(self, name):
        if name not in self.proxy_hub_dict:
            raise Exception("invalid proxy hub name: %s" % name)
        return self.proxy_hub_dict[name]

    def close(self):
        # 关闭proxy_hub自查线程
        for proxy_name in self.proxy_hub_dict:
            self.proxy_hub_dict[proxy_name].close()
            self.sys_log.debug("ProxyHub: " + proxy_name + " close")
