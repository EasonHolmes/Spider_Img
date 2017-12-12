# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class PaimgItem(Item):
    # 这两个字段 image_urls images是ImagesPipeline存放需要的
    image_urls = Field()
    images = Field()

    name = Field()
