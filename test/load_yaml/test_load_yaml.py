#coding=utf-8
import yaml
import codecs
"""
实验yaml
"""

fi=codecs.open("conf.yaml","r","utf-8")
y = yaml.load(fi)
print (y)

print (y["downloader"])
print (y["data_storage"])

class hello:

    def __init__(self):
        print (self.__class__.__name__)

class child(hello):

    def __init__(self):
        hello.__init__(self)
        print (self.__class__.__name__)

h = child()

