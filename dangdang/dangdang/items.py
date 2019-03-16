# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DangdangItem(scrapy.Item):
    
    # define the fields for your item here like:
    img = scrapy.Field()
    name = scrapy.Field()

    author = scrapy.Field()

    publisher = scrapy.Field()
    
    prize = scrapy.Field()

    prize_d = scrapy.Field()
    
    commonds = scrapy.Field()

    publish_time = scrapy.Field()

    description = scrapy.Field()

    
