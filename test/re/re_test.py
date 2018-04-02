# coding=utf-8
import re

url = "https://sh.lianjia.com/ershoufang/pg1rs%E4%B8%8A%E6%B5%B7%E5%BA%B7%E5%9F%8E/"
url_pattern = re.compile(r"https://sh.lianjia.com/ershoufang/pg*")
result = url_pattern.match(url)
if result:
    print("match")
else:
    print("no match")

a = list(range(10))
b = list(range(11, 15))
print(a)
print(b)
a.extend(b)
print(a)
