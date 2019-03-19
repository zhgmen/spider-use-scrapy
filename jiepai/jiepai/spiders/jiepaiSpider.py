# -*- coding: utf-8 -*-
import scrapy
from jiepai.items import JiepaiItem

class JiepaispiderSpider(scrapy.Spider):
    name = 'jiepaiSpider'
    
    start_urls = ['http://www.1jiepai.com/forum-43-1.html']

    def parse(self, response):
        for item in response.css("div[class='simgh'] h2"):
            url = item.css('a::attr(href)').get()
            path = item.css('a::text').get()
            yield scrapy.Request(url, callback=self.parse_img, meta={
                'path': path,
                })

            
        '''
        next_url = response.css("div[class='pg'] a::attr(href)").get()
        if not next_url:
            yield scrapy.Request(next_url, callback=self.parse)
        '''
    def parse_img(self, response):
        
        items = JiepaiItem()

        items['img_path'] = response.meta['path']
            
            #items['img_path'] = item.css('::attr(id)').get()
        items['img_url'] = response.css("div[class='mbn'] img::attr(file)").getall()
            
        yield items
        
            
