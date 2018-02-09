# coding=utf-8
import re

url = "https://www.cnblogs.com/wenweiblog/p/7216102.html"
url_pattern = re.compile(r"https://www\.(\w+)\.com/(\w+)/.+")
result = url_pattern.match(url)
if result:
    print(result.group())
    print(result.group(1))
    print(result.group(2))
else:
    print("no match")

a = list(range(10))
b = list(range(11,15))
print(a)
print (b)
a.extend(b)
print(a)