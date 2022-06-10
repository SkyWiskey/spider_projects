import scrapy
from chinaz.items import ChinazItem

class ChinazImageSpider(scrapy.Spider):
    name = 'chinaz_image'
    allowed_domains = ['sc.chinaz.com']
    start_urls = ['https://sc.chinaz.com/tupian/index_2.html']

    def parse(self, response):
        image_infos = response.xpath("//div[@class='index_only']//div[@id='container']/div/div/a")

        # 反爬虫-图片懒加载，滚轮没有拖下来，使用伪属性，当图片界面可见，再去加载图片
        # 直接访问Src属性，为空，需要使用伪属性
        for image_info in image_infos:
            title = image_info.xpath(".//img/@alt").get()
            src = response.urljoin(image_info.xpath(".//img/@src2").get().replace('_s',''))
            yield ChinazItem(title=title,src=src)
