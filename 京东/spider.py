import time,re

import pymysql
import requests
from lxml import etree
from urllib.parse import quote

class JdProductSpider(object):
    def __init__(self,keyword,pagenum):
        params  =  {'host':'localhost','port':3306,
                    'user':'root','password':'123456',
                    'database':'crawl_spider','charset':'utf8'}
        self.conn = pymysql.connect(**params)
        self.cursor = self.conn.cursor()
        self._sql = None
        self.keyword = keyword
        self.pagenum = pagenum
        self.headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

    def run(self):
        for page in range(1,self.pagenum*2,2):
            print(f'正在爬取第{page}页商品信息...')
            url = f'https://search.jd.com/Search?keyword={quote(self.keyword)}&suggest=1.his.0.0&wq={quote(self.keyword)}&pvid=6083002509f9425e82b8a5f4106d6f4a&page={page}'
            resp = requests.get(url,headers=self.headers).text
            html = etree.HTML(resp)
            self.parse(html)
            time.sleep(2)

    def parse(self,html):
        products = html.xpath("//div[@id='J_goodsList']/ul/li")
        for product in products:
            title = ''.join(product.xpath(".//div[@class='p-name p-name-type-2']/a/em//text()"))
            price_text = ''.join(product.xpath(".//div[@class='p-price']//text()"))
            price = re.sub(r'\s', '', price_text)
            source = product.xpath(".//div[@class='p-shop']//a/@title")[0]
            detail_url = 'https:' + product.xpath(".//div[@class='p-img']/a/@href")[0]
            data = (title,price,source,detail_url)
            self.storage_data(data)
    @property
    def sql(self):
        if not self._sql:
            self._sql = '''insert into jd(title,price,source,detail_url) values(%s,%s,%s,%s)'''
            return self._sql
        return self._sql

    def storage_data(self,data):
        self.cursor.execute(self.sql,data)
        self.conn.commit()

def main():
    keyword = input('请输入商品关键词>>>')
    pagenum = 5
    spider = JdProductSpider(keyword,pagenum)
    spider.run()
    print('爬取完成')

if __name__ == '__main__':
    main()