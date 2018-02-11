# coding=utf-8
"""
简单的flask服务器，用于检测爬虫的请求
"""
from flask import Flask, request
from flask_cors import CORS, cross_origin
import json

# 创建app
app = Flask(__name__)
# 支持跨域访问
CORS(app)


# 测试爬虫页面，打印爬取信息
@app.route("/crawler")
def crawler_test():
    print("==GET:/crawler===============")
    print("method:\t{}".format(request.method))
    print("ip:\t{}".format(request.remote_addr))
    if request.headers.getlist("X-Forwarded-For"):
        print("ip X_Forwarded_FOR:\t{}".format(request.headers.getlist('X-Forwarded-For')[0]))
    print("form:\t{}".format(json.dumps(request.form)))
    print("args:\t{}".format(json.dumps(request.args)))
    print("cookies: {}".format(json.dumps(request.cookies)))
    print("headers: \n--------------\n{}\n--------------\n".format(str(request.headers).strip()))
    print("=============================")

    response = "ip:\t{}\n<br/>".format(request.remote_addr)
    response += "headers: \n<br/>{}\n<br/>".format(str(request.headers).strip())
    return response


# 简单页面示例
@app.route("/")
def index():
    return "This is crawler test server"


# 路径参数示例
@app.route("/hi/")
@app.route("/hi/<user_name>")
def hello(user_name=None):
    return "Your Majesty, I am at your service! %s" % (user_name)

if __name__ == "__main__":
    # 绑定端口，开启服务：5001
    app.run('0.0.0.0', port=5001, debug=True)
