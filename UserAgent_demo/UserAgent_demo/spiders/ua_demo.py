# -*- coding: utf-8 -*-
import scrapy


class UaDemoSpider(scrapy.Spider):
    name = 'ua_demo'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/user-agent']

    def parse(self, response):
        print(response.text)
        yield scrapy.Request(url=self.start_urls[0], dont_filter=True)
        # browser = ['Safari','Internet Explorer','Edge','Firefox','Chrome','Mozilla','Opera']

