# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AliexpressItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
      title=scrapy.Field()
      category=scrapy.Field()
      itemVariation=scrapy.Field()
      seller=scrapy.Field()
      itemSpecifics=scrapy.Field()
      description=scrapy.Field()
      url=scrapy.Field()
      id=scrapy.Field()
   