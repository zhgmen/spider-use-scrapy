# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib import request
from scrapy.pipelines.images import ImagesPipeline
from bmw5 import settings
class Bmw5Pipeline(object):
    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)))
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def process_item(self, item, spider):
        title = item['title']
        img_path = os.path.join(self.path,title)
        if not os.path.exists(img_path):
            os.mkdir(img_path)
        urls = item['urls']
        for url in urls:
            img_name = url.split('_')[-1]
            request.urlretrieve(url, os.path.join(img_path, img_name))


        return item
class BmwImagesPipeline(ImagesPipeline):
    
    def get_media_requests(self, item, info):
        request_objs = super(BmwImagesPipeline, self).get_media_requests(item, info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        path = super(BmwImagesPipeline, self).file_path(request, response=None, info=None)
        title = request.item.get('title')
        store = settings.IMAGES_STORE
        title_path = os.path.join(store, title)
        if not os.path.exists(title_path):
            os.mkdir(title_path)
        file = path.replace('full/', '')
        return os.path.join(title_path,file)




            

        
    