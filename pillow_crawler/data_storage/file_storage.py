# coding=utf-8
import codecs
from pillow_crawler.data_storage.data_storage import *
from pillow_crawler.system.thread_lock import *


class FileStorage(DataStorage):

    def __init__(self, config):
        self.name = config["name"]
        self.file_dir = config["file_dir"]
        self.file_cur = {}

    def __del__(self):
        for key in self.file_cur:
            print("delete")
            self.file_cur[key].close()

    def save(self, file_name, row):
        file_path = self.file_dir + "/" + file_name
        print(row+" |||| " +file_path+" "+str(len(self.file_cur)))
        if file_path in self.file_cur:
            fo = self.file_cur[file_path]
        else:
            FILE_LOCK.acquire()
            if file_path in self.file_cur:
                fo = self.file_cur[file_path]
            else:
                print(row+ " |||| create")
                fo = codecs.open(file_path, "w", "utf-8")
                self.file_cur[file_path] = fo
            FILE_LOCK.release()
            print(row + " |||| after create: "+str(len(self.file_cur)))
        fo.write(row + "\n")
        fo.flush()