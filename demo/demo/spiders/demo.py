# -*- coding: utf-8 -*-
import scrapy
import re

class DemoSpider(scrapy.Spider):
    name = 'demo'
    
    start_urls = ['http://env.dhu.edu.cn/6959/list.htm']

    def parse(self, response):
        selector = response.css("div[class='b articlecontent '] p")
        for item in selector.css('a'):
            
            url = item.css('::attr(href)').get()
            name = item.css('::text').get()
            #yield dict(url=url)
            
            yield scrapy.Request(url,callback=self.parse_content, meta={
                'name': name,
                })
            
            
            
            

    def parse_content(self,response):

        selector = response.css('div[class="Article_Content"] p')
        content =''.join(selector.css('span::text').getall())
        content.replace('\xa0', '')
        list1 = content.split('。')
        '''
        for i in list1:
            yield {'key': i}
        '''
        list2 = ['职称', '电话', '邮箱', '研究方向', '工作', '获奖', '兼职', 'TEL：', 'EMAIL：', 'mail：']
        list3 = []
        d = {'姓名': ' ', '职称': ' ', '电话': ' ', '邮箱': ' ', '研究方向': ' ', '工作': ' ', '获奖': ' ', '兼职': ' '}
        d1 = {}
        for idx1 in list1:
            
            for idx2 in list2:
                n = idx1.find(idx2)
                if n != -1:
                    d1[idx2] = n
                
            for key,value in sorted(d1.items(), key=lambda x: x[1]):
                list3.append(key)
                

            len3 = len(list3)
            self.log(list3)
            if len3 >= 2:
                for i in range(len3):
                    idx3 = list3[i]
                    if i == len3-1:
                        try:
                            
                            r = re.search(idx3 + '(.*?)$', idx1, re.IGNORECASE)
                            d[idx3] = r.group(1)
                        except:
                            pass
                    else:
                        try:
                            
                            r = re.search(idx3 + '(.*?)' + list3[i+1], idx1, re.IGNORECASE)
                        
                            d[idx3] = r.group(1)
                        except:
                            pass
            else:
                if list3:
                    
                    r = re.search(list3[0] + '(.*?)$', idx1, re.IGNORECASE)
                    d[list3[0]] = r.group(1)
            d1 = {}  
            list3 = []
            
            
            if 'TEL：' not in d:
                pass
            else:
                    
                d['电话'] = d['TEL：']
                del d['TEL：']
            
            if 'EMAIL：' not in d:
                pass
            else:
                    
                d['邮箱'] = d['EMAIL：']
                del d['EMAIL：']
            if 'mail：'not in d:
                pass
            else:
                    
                d['邮箱'] = d['mail：']
                del d['mail：']
        d['姓名'] = response.meta['name']
                    
        yield d        


          
            
             
                
                
