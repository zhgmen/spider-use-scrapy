# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

'''
class JiepaiPipeline(object):
    def process_item(self, item, spider):
        return item
'''
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class JiepaiPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['img_url']:
            yield scrapy.Request(image_url, meta={
                'path': item['img_path']
                })
    

    def item_completed(self, results, item, info):
        '''
        [(True,
  {'checksum': '2b00042f7481c7b056c4b410d28f33cf',
   'path': 'full/7d97e98f8af710c7e7fe703abc8f639e0ee507c4.jpg',
   'url': 'http://www.example.com/images/product1.jpg'}),
 (True,
  {'checksum': 'b9628c4ab9b595f72f280b90c4fd093d',
   'path': 'full/1ca5879492b8fd606df1964ea3c1e2f4520f076f.jpg',
   'url': 'http://www.example.com/images/product2.jpg'}),
 (False,
  Failure(...))]
        '''
        for ok, x in results:
            if not ok:
                raise DropItem("Item contains no images")
            
        
        #item['img_path'] = image_paths
        return item
    
    def file_path(self, request, response=None, info=None):
        image = request.url.split('/')[-1]
        name = request.meta['path']
        #name = re.sub(r'[？\\*|“<>:/]', '', name)
        filename = u'{0}/{1}'.format(name, image)
        return filename
