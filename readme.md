# pillow_crawler

[TOC]

## 概述

pillow_crawler是一个轻量、易用、易扩展的爬虫框架，可以处理日常的简单爬虫任务。

同时pillow_crawler也支持扩展成分布式集群模式。


## 系统要求

Python 3.4+

依赖库：
* yaml：``` pip3 install PyYaml```
* requests: ```pip3 install requests```
* lxml: ```pip3 install lxml```
* mysqlclient: ```pip3 install mysqlclient```

备注：
安装mysqlclient时有可能遇到错误：```mysql_config not found```。

该错误的原因为没有在系统路径中找到mysql_config文件，需要先安装Mysql，之后把mysql_config文件添加到系统路径中。

通常该文件所在的路径为/usr/local/mysql/bin/，故添加命令为：
```
export PATH=${PATH}:/usr/local/mysql/bin/
```

## 运行

```
cd samples
python tmall_anta_crawler.py
```

## 参考

https://github.com/Pingze-github/proxy-finder
https://www.zhihu.com/question/42139379
