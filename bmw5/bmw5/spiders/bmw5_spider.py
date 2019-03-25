# -*- coding: utf-8 -*-
import scrapy
from bmw5.items import Bmw5Item

class Bmw5SpiderSpider(scrapy.Spider):
    name = 'bmw5_spider'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/65.html']

    def parse(self, response):
        divs = response.xpath("//div[@class='uibox']")[1:]
        for div in divs:
            title = div.xpath("./div/a/text()").get()
            urls = div.xpath("./div/ul/li/a/img/@src").getall()
            urls = [response.urljoin(url) for url in urls]
            item = Bmw5Item(title=title, image_urls=urls)


            yield item



