# -*- coding: utf-8 -*-
import scrapy


class Demo2Spider(scrapy.Spider):
    name = 'demo2'
    
    start_urls = ['http://http://spxy.cau.edu.cn/col/col22476/index.html']

    def parse(self, response):
        
        for item in response.css("div[class='teacher'] a"):
            
            url = item.css('::attr(href)').get()
            name = item.css('::attr(title)').get()
            #yield dict(url=url)
            
            yield scrapy.Request(url,callback=self.parse_content, meta={
                'name': name,
                })
            
            
            

    def parse_content(self,response):

        selector = response.css('div[class="info-main"] p')
        content ='{}'.join(selector.css('span::text').getall())
        
        list1 = content.split('：')
        
        length = len(list1)
        for i in range(length-1):
            list2 = list1[i].split('{}')
            list1[i+1] = list2[-1]+'：'+list1[i+1]
            list1[i] = ''.join(list2[:-1])
        list1[-1] = list1[-1].replace('{}','')
        list1[0] = response.meta['name'] + '：' + list1[0]
        for item in list1:
            key, value = item.split('：')
            yield {key: value}
        
