# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChinazItem(scrapy.Item):
    title = scrapy.Field()
    src = scrapy.Field()
