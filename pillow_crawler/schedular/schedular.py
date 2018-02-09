# coding=utf-8
import queue
import datetime


class Schedular:

    def __init__(self):
        # 默认队列大小为100k，超过则报错
        self.task_queue = queue.Queue(100000)

    def next_task(self):
        return self.task_queue.get()

    def put_task(self, task):
        self.task_queue.put(task, block=True)

    def put_url(self, url):
        self.task_queue.put(CrawlerTask(url))

    def current_task_num(self):
        return self.task_queue.qsize()


class CrawlerTask:

    def __init__(self, url, fail_count=0, last_calltime = 0):
        self.url = url
        self.fail_count = fail_count
        if(last_calltime==0):
            self.last_calltime = datetime.datetime.now()
        else:
            self.last_calltime = last_calltime

    def __str__(self):
        return """url: {}
fail_count: {}
last_call time: {}
""".format(self.url, self.fail_count, self.last_calltime)

if __name__ == '__main__':
    print(CrawlerTask("http://hellocom",1,0))


