# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from dangdang import settings

class DangdangPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(
            host = "localhost",
            db = "root",
            user = "zhgmen",
            passwd = "dangdang",
            charset = 'utf-8'
            )
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        self.insert(item)
        
        return item
    def open_spider(self):
        pass
    de

    def insert(self, item):
        sql = ''
        self.cursor.execute(sql,())
        self.conn.commit()
    def close_spider(self):
        self.cursor.close()
        self.conn.close()
