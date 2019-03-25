# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors
class JianshuPipeline(object):

    def __init__(self):
        data = {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "root",
            "password": "zhgmen",
            "database": "jianshu",
            "charset": "utf8"
        }
        self.conn = pymysql.connect(**data)
        self.cursor = self.conn.cursor()

        self.creat_table()
        self._sql = None

    def process_item(self, item, spider):
        self.cursor.execute(self.sql,(item['title'],item['content'],item['article_id'],item['origin_url'],item['author'],item['avatar']))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql  = '''
                    INSERT INTO article
                    (title,content,article_id,origin_url,author,avatar) 
                    VALUES (%s,%s,%s,%s,%s,%s);
                '''
        return self._sql



    def creat_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS article (
                id INT(9) PRIMARY KEY  AUTO_INCREMENT ,
                title VARCHAR(255),
                content LONGTEXT,
                article_id VARCHAR(20),
                origin_url VARCHAR (255),
                author VARCHAR (20),
                avatar VARCHAR (255)   
                );
            '''
        self.cursor.execute(sql)
        self.conn.commit()
    def close_spider(self, spider):
        self.close()
    def close(self):
        self.cursor.close()
        self.conn.cursor()

class JianshuTwistedPipeline(object):
    def __init__(self):
        data = {
            "host": '127.0.0.1',
            "port": 3306,
            "user": "root",
            "password": "zhgmen",
            "database": "jianshu",
            "charset": "utf8",
            "cursorclass": cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **data)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = '''
                        INSERT INTO article
                        (title,content,article_id,origin_url,author,avatar) 
                        VALUES (%s,%s,%s,%s,%s,%s)
                    '''
        return self._sql

    def process_item(self,item,spider):
        defer = self.dbpool.runInteraction(self.insert_item,item)
        defer.addErrback(self.handle_error, item, spider)

    def handle_error(self,error,item,spider):
        print(error)

    def insert_item(self, cursor, item):
        cursor.execute(self.sql, (item['title'],item['content'],item['article_id'],item['origin_url'],item['author'],item['avatar']))
