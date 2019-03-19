# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import csv
class DemoPipeline(object):
    def __init__(self):
        self.f = open('demo.json','w', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False)+'\n'
        self.f.write(line)
            
        return item

    def close_spider(self, spider):
        self.f.close()
class DemoDictPipeline(object):
    def __init__(self):
        fieldnames = ['姓名', '职称', '电话', '邮箱', '研究方向', '工作', '获奖', '兼职','照片']
        self.f = open('demo.csv', 'w', newline='', encoding='gbk')
        self.dw = csv.DictWriter(self.f, fieldnames)
        self.dw.writeheader()
        
        
    def process_item(self, item, spider):
        #line = json.dumps(dict(item), ensure_ascii=False)+'\n'
        self.dw.writerow(item)
            
        return item

    def close_spider(self, spider):
        
        self.f.close()
