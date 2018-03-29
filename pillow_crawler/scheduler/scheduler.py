# coding=utf-8
import queue
import datetime


class Scheduler:

    def __init__(self):
        # 默认队列大小为100k，超过则报错
        self.task_queue = queue.Queue(100000)

    def next_task(self):
        # 获取下一个任务，非阻塞，如果为空则返回None
        try:
            task = self.task_queue.get(False)
        except queue.Empty:
            return None
        task.last_call_time = datetime.datetime.now()
        return task

    def put_task(self, task):
        self.task_queue.put(task, block=True)

    def put_url(self, url):
        self.task_queue.put(CrawlerTask(url))

    def current_task_num(self):
        return self.task_queue.qsize()

    def is_task_empty(self):
        return self.task_queue.empty()


class CrawlerTask:

    def __init__(self, url, fail_count=0, last_call_time = 0):
        self.url = url
        self.fail_count = fail_count
        if last_call_time == 0:
            self.last_call_time = datetime.datetime.now()
        else:
            self.last_call_time = last_call_time

    def __str__(self):
        return """url: {}
fail_count: {}
last_call time: {}
""".format(self.url, self.fail_count, self.last_call_time)

if __name__ == '__main__':
    print(CrawlerTask("http://hellocom",1,0))


