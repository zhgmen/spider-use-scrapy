# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class ZhipinSpider(CrawlSpider):
    name = 'zhipin'
    allowed_domains = ['zhipin.com']
    start_urls = ['http://zhipin.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.+c100010000/\?query=python&page=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'.+ob_detail/.+\.html'), callback=self.parse_item, follow=False),
    )

    def parse_item(self, response):
        item = {}
        item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
