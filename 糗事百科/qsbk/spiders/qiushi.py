# -*- coding: utf-8 -*-
import scrapy
from qsbk.items import QsbkItem

class QiushiSpider(scrapy.Spider):
    name = 'qiushi'
    allowed_domains = ['qiushibaike.com']
    domain = 'https://www.qiushibaike.com'
    start_urls = ['https://www.qiushibaike.com/text/']

    def parse(self, response):
        urls = response.css("a[class='contentHerf']::attr(href)").getall()
        for url in urls:
            
            yield scrapy.Request(url=self.domain+url, callback=self.parse_content)
        

           
        nextpage = response.xpath("//ul[@class='pagination']/li/a")[-1]
        if nextpage.xpath('./span/@class').extract()[0] == 'next':
            yield scrapy.Request(url = self.domain + nextpage.xpath('./@href').extract()[0], callback=self.parse)
           

    def parse_content(self, response):
        item = QsbkItem()
        item['content'] = '\n'.join(response.xpath("//div[@class='content']/text()").extract())

        yield item
        
            
