# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
from scrapy.exceptions import DropItem

class ItemsSpecPipeline(object):
  
 def process_item(self, item, spider):
   if item['itemSpecifics']:
    line=item['itemSpecifics']
    print 'LIST', line
    
class ItemExistingPipeline(object):
  #verify if it is a real item
  def process_item(self, item, spider):
   if item['title']!=[]:
     return item
   else:
     raise DropItem()
   
class JsonWithEncodingPipeline(object):

    def __init__(self):
       self.file = codecs.open('scraped_data_utf8.json', 'w', encoding='utf-8')
        
        #self.file = codecs.open('scraped_data_utf8.json', 'w')

    def process_item(self, item, spider):
	#line = json.dumps(dict(item), ensure_ascii=True) + "\n"
	#line = json.dumps({k: str(v) for k, v in self.__dict__.items()}, ensure_ascii=True)+ "\n"
	if item['title']!=[]:
	  line = json.dumps(dict(item), ensure_ascii=False) + "\n"
	  self.file.write(line)
	  return item
	else:
	    raise DropItem()

    def spider_closed(self, spider):
        self.file.close()