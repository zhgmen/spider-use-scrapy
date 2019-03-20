#coding:utf-8
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import threading
from queue import Queue
import json

flag = 0

class lagouSpider(object):
    def __init__(self, json_queue):
        self.browser = webdriver.Chrome()
        self.browser.get('https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=')
        self.json_queue = json_queue


    def run(self):
        urls = self.browser.find_elements_by_xpath("//a[@class='position_link']")
        for url in urls:
            link = url.get_attribute('href')
            self.get_detail_page(link)
            time.sleep(1)
        self.get_next_page()
 
    def get_next_page(self):
        page = 2
        while True:
            
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight*0.8)')
            next_page = self.browser.find_elements_by_xpath("//span[@action='next']")
            
            if next_page.get_attribute('class') == 'pager_next':
                button.click()

                now_page = self.browser.find_elements_by_xpath("//span[@class='pager_is_current']")

                wait = WebDriverWait(self.browser, 10)
                
                wait.until(EC.text_to_be_present_in_element(now_page,str(page)))
 
                urls = self.browser.find_elements_by_xpath("//a[@class='position_link']")
                for url in urls:
                    link = url.get_attribute('href')
                    self.get_detail_page(link)
                    time.sleep(3)

                time.sleep(1)
                page += 1
            flag = 1 
            print('爬取detail链接完成！')
            break
            
        
        
        
    def get_detail_page(self, url):
        self.browser.execute_script('window.open()')
        self.browser.switch_to.window(self.browser.window_handles[1])
  
        self.browser.get(url)
        try:
            
            selector = etree.HTML(self.browser.page_source)
            company = selector.xpath("//div[@class='company']/text()")[0]
            name = selector.xpath("//span[@class='name']/text()")[0]
            job_request = ''.join(selector.xpath("//dd[@class='job_request']/p/span/text()"))
            labels = '----'.join(selector.xpath("//ul[@class='position-label clearfix']//li/text()"))
            job_detail = ''.join([i.strip() for i in selector.xpath("//dd[@class='job_bt']//text()")])
            address = ''.join(selector.xpath("//div[@class='work_addr']/a/text()")[:-1])
            d = {
                "company": company,
                "name": name,
                "job_request": job_request,
                "labels": labels,
                "job_detail": job_detail,
                "address": address,
                }
            
            self.json_queue.put(d)
            
            self.browser.close()
            self.browser.switch_to.window(self.browser.window_handles[0])
            
        except:
            print('反爬虫！')
            self.browser.close()
            self.browser.switch_to.window(self.browser.window_handles[0])
            time.sleep(30)
        
class Writer(threading.Thread):
    

    def __init__(self, json_queue, writer, *args, **kwargs):
        super(Writer, self).__init__(*args, **kwargs)
        self.json_queue = json_queue
        self.write = writer

    def run(self):
        while True:
            if self.json_queue.empty() and flag==1:
                self.writer.close()
                print("爬取工作完成！")
                break
            data = self.json_queue.get()
            
            json_data = json.dumps(data, ensure_ascii=False)
            print(json_data)
            self.write.write(json_data+'\n')
            
            
        
def main():
    json_queue = Queue(10)
    writer = open('lagou.json','a',encoding='utf-8')
    w = Writer(json_queue, writer)
    w.start()
    

    lagou = lagouSpider(json_queue)
    lagou.run()
    
    
        
        
    

        

if __name__=='__main__':
    main()

'''
def get_Ajax():
    url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    data = {
        'first': 'true',
        'pn': 1,
        'kd': 'python',
        }
    headers = {
        'Cookie': '_ga=GA1.2.985576579.1547168989; user_trace_token=20190111090945-951966a0-153d-11e9-b2f7-5254005c3644; LGUID=20190111090945-95196949-153d-11e9-b2f7-5254005c3644; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221683a75559a471-080ab98dd11556-3c604504-1382400-1683a75559b792%22%2C%22%24device_id%22%3A%221683a75559a471-080ab98dd11556-3c604504-1382400-1683a75559b792%22%7D; LG_LOGIN_USER_ID=ad1967392aacbda90b119133f8e15ab5681cb1870af4d805d32890f03e3c357b; JSESSIONID=ABAAABAAADEAAFI6E39AACA040D42CA53032545002CEED6; _gid=GA1.2.1812822814.1553086280; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_search; _gat=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1553086280,1553086570,1553090273; LGSID=20190320215752-27c2ff47-4b18-11e9-a6f1-525400f775ce; PRE_UTM=; PRE_HOST=cn.bing.com; PRE_SITE=https%3A%2F%2Fcn.bing.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; SEARCH_ID=5de493427ef349d3b8ea2f27a6d6c72b; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1553090276; LGRID=20190320215756-29bb1bf6-4b18-11e9-b1ae-5254005c3644',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
    response = requests.post(url=url, headers=headers, data=data)
    resp = response.json()
    print(resp)
get_Ajax()
'''
