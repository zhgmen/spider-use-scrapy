# -*- coding: utf-8 -*-
import scrapy

from scrapy.http.response.text import TextResponse
class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['www.douban.com']
    start_urls = ['https://www.douban.com/']
    def start_requests(self):
        login_url = 'https://accounts.douban.com/j/mobile/login/basic'
        data = {
            'ck': '',
            'name': '17694476929',
            'password': '1111111',
            'remember': 'false',
            'ticket': '',
        }

        yield scrapy.FormRequest(url=login_url,formdata=data,callback=self.parse)

    def parse(self, response):
        print("="*30)
        print(response.url)

        print(response.text)
        print("=" * 30)
    def img2text(self):
        pass


