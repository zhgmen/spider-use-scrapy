from urllib import request
from lxml import etree
import os
import re
import threading
from queue import Queue


path = 'imges/'
if not os.path.exists(path):
    os.mkdir(path)
    

class Producter(threading.Thread):

    headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            }
    def __init__(self, url_queue, img_queue, *args, **kwargs):
        super(Producter, self).__init__(*args, **kwargs)
        self.url_queue = url_queue
        self.img_queue = img_queue
        

    def run(self):
        while True:
            if self.url_queue.empty():
                
                break
            
            url = self.url_queue.get()
            self.parse_html(url)
            
    def parse_html(self, url):
        
        resq = request.Request(url, headers=self.headers)
        resp = request.urlopen(resq)
        html = resp.read().decode('utf-8')
        selector = etree.HTML(html)
        imgs = selector.xpath("//img[@class='img-responsive lazy image_dta']")
        
        for img in imgs:
            img_url = img.get('data-original')
            suffix = os.path.splitext(img_url)[1]

            
            img_name = img.get('alt') + suffix
            img_name = re.sub('\\/:\*\?"<>|','',img_name)
            self.img_queue.put((img_name, img_url))
            
            
class Consumer(threading.Thread):
    def __init__(self, url_queue, img_queue, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)
        self.url_queue = url_queue
        self.img_queue =img_queue

    def run(self):
        while True:
            if self.url_queue.empty() and self.img_queue.empty():
                print('完成全部下载！')
                break
            img_name, img_url = self.img_queue.get()
            request.urlretrieve(img_url, path+img_name)
            print('图片 %s 下载完成！'% img_name)
    


def main():
    url_queue = Queue(101)
    img_queue = Queue(500)
    
    
    for i in range(1,7):
        url = 'https://www.doutula.com/photo/list/?page=%d' % i
        url_queue.put(url)
        

        

    for i in range(5):
        p = Producter(url_queue, img_queue)
        
        p.start()

    for i in range(5):
        c = Consumer(url_queue, img_queue)
        c.start()

if __name__ == '__main__':
    
    main()
