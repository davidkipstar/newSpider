# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item,Field

class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    timestamp = scrapy.Field()
    body  = scrapy.Field()
    h1 = scrapy.Field()
    h2 = scrapy.Field()
    author = scrapy.Field()
    pass
class SnapshotItem(scrapy.Item):
    url = scrapy.Field()
    timestamp  = scrapy.Field()
    rank = scrapy.Field()
    pass