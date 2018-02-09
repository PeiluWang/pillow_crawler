# coding=utf-8
import codecs

class Downloader:

    def __init__(self):
        pass

    def get_web(self, url):
        return "normal"


if __name__ == '__main__':
    fo_dict={}
    fo=codecs.open("test.txt","w","utf-8")
    fo.write("haha\n")
    fo_dict["file1"]=fo

    fo2=fo_dict["file1"]
    fo2.write("hoho\n")
    fo2.flush()