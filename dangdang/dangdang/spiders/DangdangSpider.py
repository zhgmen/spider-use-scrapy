# -*- coding: utf-8 -*-
import scrapy

from dangdang.items import DangdangItem

class DangdangSpider(scrapy.Spider):
    name = 'dspider'

    allowed_domains = ['dangdang.com']

    start_urls = ['http://search.dangdang.com/?key=python&act=input']

    def parse(self, response):
        content = response.xpath("//div[@id='search_nature_rg']/ul/li")
        
    
    
        for url in content:
            img_url = url.xpath("./a/img/@src")[0]
        
            urlitem = url.xpath("./a/@href")[0]
            urls = response.urljoin(urlitem)
            yield scrapy.Request(url, callback = self.parse_book, meta = {
                'img': img_url,
                })

    def parse_book(self, response):
        item = DangdangItem()
        item['img'] = response.meta['img']
        book = response.xpath("//div[@class='product_main clearfix']")[0]
        name_info = book.xpath(".//div[@class='name_info']")[0]

        item['name'] = name_info.xpath("./h1/@title")[0] # 书名
        item['description'] = name_info.xpath("./h2/span/@title")[0] #简介
        
        
        
        book_info = book.xpath(".//div[@class='messbox_info']")[0]
        
        author , publisher, publish_time = book_info.xpath('./span')
        commond = book_info.xpath("./div/span")[1]
        
        item['commonds'] = commond.xpath('./a/text()')[0] # 评论数
        
        a = author.xpath("./text()")
        b = author.xpath("./a/text()")
        
        a[1:1] = b[:1]
        a[3] = ' '.join(b[1:])
        
        item['author'] = ''.join(a) # 作者
        a = publisher.xpath("./text()")
        b = publisher.xpath("./a/text()")
        item['publisher'] = a[0]+b[0] # 出版社
        item['publish_time'] = publish_time.xpath("./text()")[0] # 出版日期
        

        item['prize'] = book.xpath(".//p[@id='dd-price']/text()")[1] #价格
        item['prize_d'] = book.xpath(".//div[@class='price_m']/text()")[1] # 定价

        yield item

    
    
