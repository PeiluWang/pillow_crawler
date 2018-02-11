# coding = utf-8
import threading
"""
线程锁
"""

# 读写文件的同步锁
FILE_LOCK = threading.Lock()

# 讯代理的锁
XDAILI_PROXY_LOCK = threading.Lock()