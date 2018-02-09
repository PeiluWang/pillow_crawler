# coding=utf-8
import sys
import MySQLdb
import re
import datetime
from pillow_crawler.system.dict_util import *
from pillow_crawler.data_storage.data_storage import *


class MySqlStorage(DataStorage):

    def __init__(self, config):
        try:
            check_key(config, ["name", "url", "username", "password"])
        except Exception as e:
            raise Exception("MySQL配置文件错误: "+str(e))
        self.__name = config["name"]
        self.__url = config["url"]
        self.__username = config["username"]
        self.__password = config["password"]
        # 解析url
        match_result = re.match(
            r'mysql://(?P<host>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(?P<port>\d{1,5})/?(?P<dbname>\w*)', self.__url)
        if match_result:
            self.__host = match_result.group("host")
            self.__port = int(match_result.group("port"))
            self.__dbname = match_result.group("dbname")
        else:
            raise Exception("解析url失败，url格式不正确："+str(self.__url))
        self.conn = None
        self.cur = None

    def __del__(self):
        if self.conn:
            self.close_connection()

    def open_connection(self):
        self.conn = MySQLdb.connect(
            host=self.__host,
            port=self.__port,
            user=self.__username,
            passwd=self.__password,
            db=self.__dbname,
        )
        self.cur = self.conn.cursor()

    def close_connection(self):
        self.cur.close()
        self.conn.close()

    def save(self, table_name, data):

        if not data or not isinstance(data, (list, tuple)):
            return

        def __to_sql_str(item):
            if item is None:
                return u"NULL"
            if isinstance(item, (int, float, bool)):
                return u"{}".format(item)
            elif isinstance(item, (str, datetime.datetime)):
                return u"'{}'".format(item)
            else:
                raise Exception(u"不正确的数据类型"+str(type(item)))

        data_sql_str = ",".join(map(__to_sql_str, data))
        sql = u"INSERT INTO `{}` VALUES ({});".format(table_name, data_sql_str)

        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            raise Exception("插入数据错误：{}".format(e))


if __name__ == '__main__':
    config = {"url": "mysql://172.16.80.126:3306/test", "name": "mysql1", "username": "geality", "password": "Upa1234!"}
    mysqlStorage = MySqlStorage(config)
    mysqlStorage.open_connection()
    mysqlStorage.save("test", [1, 'col2', datetime.datetime.now()])
    mysqlStorage.save("test", [2, 'col2', None])