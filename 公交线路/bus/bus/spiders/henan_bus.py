import re

import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from bus.items import BusItem


class HenanBusSpider(scrapy.Spider):
    name = 'henan_bus'
    allowed_domains = ['8684.cn']
    start_urls = ['https://beijing.8684.cn/']

    # rules = (
    #     Rule(LinkExtractor(allow=r'.+8684\.cn/$'),callback='parse_item',follow=True),
    # )
    def parse(self, response):
        city_name = response.xpath("//span[@class='title']/text()").get()
        city_name = re.sub('公交线路','',str(city_name))
        if city_name != None:
            num_href_list = response.xpath("//div[@class='bus-layer depth w120']/div[1]/div/a/@href").getall()
            for num_href in num_href_list:
                num_href = response.urljoin(num_href)
                yield scrapy.Request(url=num_href,callback=self.parse_lines,meta={'info':city_name})

    def parse_lines(self,response):
        city_name = response.meta.get('info')
        all_lines = response.xpath("//div[@class='list clearfix']/a")
        for line in all_lines:
            href = response.urljoin(line.xpath(".//@href").get())
            line_name = line.xpath(".//@title").get()
            yield scrapy.Request(url=href,callback=self.parse_detail_line,meta={'info':(city_name,line_name)})

    def parse_detail_line(self,response):
        city_name,line_name = response.meta.get('info')
        run_time = response.xpath("//ul[@class='bus-desc']/li[1]/text()").get()
        ticket_price = response.xpath("//ul[@class='bus-desc']/li[2]/text()").get()
        company = response.xpath("////ul[@class='bus-desc']/li[3]/a/@title").get()
        last_update_time = response.xpath("//ul[@class='bus-desc']/li[4]/span/text()").get()
        line_sites = ''
        aria_lables = response.xpath("//div[@class='service-area']/div[@class='bus-lzlist mb15'][1]/ol/li")
        for aria in aria_lables:
            site = aria.xpath(".//a/@aria-label").get()
            line_sites += str(site) + '<->'

        yield BusItem(city_name = city_name,line_name = line_name,run_time = run_time,
                      ticket_price = ticket_price,company = company,last_update_time = last_update_time,
                      line_sites = line_sites)

