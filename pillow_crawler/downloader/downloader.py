# coding=utf-8
import codecs
import requests


class Downloader:
    """
    一般网页的下载器，未用代理、selenium动态加载
    """
    def __init__(self):
        pass

    def get_web(self, url, params=None):
        """
        get请求页面
        :param url: 页面的地址
        :param params: 请求参数，格式：['key':'value',...]
        :return: 返回的页面内容
        """
        headers = self._mock_http_headers()
        kwargs = {
            "headers": headers,
            "params": params,
            "timeout": 5
        }
        response = requests.get(url, **kwargs)
        # 检查返回状态码是否是2**（代表请求成功）
        status_code = str(response.status_code)
        if not status_code.startswith("2"):
            raise Exception("get web error, response.status_code: "+status_code)
        return response.text

    def _mock_http_headers(self):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36",
        }
        return headers

if __name__ == '__main__':
    downloader = Downloader()
    response = downloader.get_web("http://139.196.149.203:5001/crawler")
    print(response)