# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from wxapp.items import WxappItem
class WxappSpiderSpider(CrawlSpider):
    name = 'wxapp_spider'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=2&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'.+ortal.php?mod=list&catid=2&page=\d{1,3}'), follow=True),
        Rule(LinkExtractor(allow=r'.+/article-.+\.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        
        title =  response.xpath('//div[@class="cl"]/h1/text()').get()
        author =  response.xpath('//p[@class="authors"]/a/text()').get()
        date =  response.xpath('//span[@class="time"]/text()').get()
        focus =  response.xpath('//div[@class="focus_num cl"]/a/text()').get()
        quote =  response.xpath('//div[@class="blockquote"]/p/text()').get()
        content = ''.join(response.xpath('//td[@id="article_content"]//text()').getall())
        
        item = WxappItem(title=title, quote=quote, author=author, date=date,focus=focus, content=content)

        yield item
