# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyProjectItem(scrapy.Item):
    """有名人の引用アイテム."""
    author = scrapy.Field()
    text = scrapy.Field()
    tags = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()
