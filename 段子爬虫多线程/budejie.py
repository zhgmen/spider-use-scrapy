# -*- coding: utf-8 -*-

from queue import Queue
from lxml import etree
from urllib import request
import threading
import csv


class Spider(threading.Thread):
    def __init__(self, url_queue, joke_queue, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.url_queue = url_queue
        self.joke_queue = joke_queue

    def run(self):
        while True:
            if self.url_queue.empty():
                print('页面下载完成！')
                break
            url = self.url_queue.get()
            self.parse_url(url)
    def parse_url(self, url):
        domin_url = 'http://www.budejie.com'
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            }
        req = request.Request(url, headers=header)
        resp = request.urlopen(req)
        html = resp.read().decode('utf-8')
        selector = etree.HTML(html)
        jokes = selector.xpath("//div[@class='j-r-list-c-desc']")
        for joke in jokes:
            j_text = joke.xpath('a/text()')[0]
            j_link = domin_url+joke.xpath('a/@href')[0]
            
            self.joke_queue.put((j_link, j_text))
                   

class Writer(threading.Thread):
    def __init__(self, url_queue, joke_queue, writer, lock, *args, **kwargs):
        super(Writer, self).__init__(*args, **kwargs)
        self.url_queue = url_queue
        self.joke_queue = joke_queue
        self.writer = writer
        self.lock = lock

    def run(self):
        while True:
            if self.url_queue.empty() and self.joke_queue.empty():
                print('写入完成！')
                
                break
            
            link, joke = self.joke_queue.get()
            self.lock.acquire()
            self.writer.writerow((link, joke))
            self.lock.release()
            print('保存一条')
            
            
        
    


def main():
    url_queue = Queue(50)
    joke_queue = Queue(500)
    gLock = threading.Lock()
    for i in range(1,51):
        url = 'http://www.budejie.com/text/%d' % i
        url_queue.put(url)
        
    fp = open('jokes.csv', 'a', newline='', encoding='gb18030')
    writer = csv.writer(fp)
    writer.writerow(('link', 'content'))

    for i in range(5):
        s = Spider(url_queue, joke_queue)
        s.start()

    for i in range(5):
        w = Writer(url_queue, joke_queue, writer, gLock)
        w.start()
        
        
    
if __name__=='__main__':
    main()
