# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawldataItem(scrapy.Item):
    ProductURL = scrapy.Field()
    ProductID = scrapy.Field()
    ProductName = scrapy.Field()
    Category = scrapy.Field()
    Price = scrapy.Field()
    Material = scrapy.Field()
    Dimensions = scrapy.Field()
