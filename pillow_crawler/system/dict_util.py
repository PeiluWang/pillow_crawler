# coding=utf-8
"""
词典辅助类
"""


def check_key(dict, keys):
    for key in keys:
        if key not in dict:
            raise Exception(key+"不存在")


def check_string_not_null(str, name):
    if str is None or str.strip() == "":
        raise Exception(name+"为空")