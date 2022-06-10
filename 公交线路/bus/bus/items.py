# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BusItem(scrapy.Item):
    city_name = scrapy.Field()
    line_name = scrapy.Field()
    line_sites = scrapy.Field()
    run_time = scrapy.Field()
    ticket_price = scrapy.Field()
    company = scrapy.Field()
    last_update_time = scrapy.Field()
