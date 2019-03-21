from urllib import request
from lxml import etree
import os
import re

path = 'imges/'
if not os.path.exists(path):
    os.mkdir(path)

def parse_html(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }
    resq = request.Request(url, headers=headers)
    resp = request.urlopen(resq)
    html = resp.read().decode('utf-8')
    selector = etree.HTML(html)
    imgs = selector.xpath("//img[@class='img-responsive lazy image_dta']")
    
    for img in imgs:
        img_url = img.get('data-original')
        suffix = os.path.splitext(img_url)[1]

        
        img_name = img.get('alt') + suffix
        img_name = re.sub('\\/:\*\?"<>|','',img_name)
        #print(img_name)
        
        
        request.urlretrieve(img_url, path+img_name)
      
    



def main():
    
    for i in range(1,101):
        url = 'https://www.doutula.com/photo/list/?page=%d' % i
        parse_html(url)

        break
main()
