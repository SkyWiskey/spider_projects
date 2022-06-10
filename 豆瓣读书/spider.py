import time
import re

import requests
import pymysql
from lxml import etree
from urllib.parse import quote

class DoubanBookSpider(object):
    def __init__(self,keyword,pagenum):
        self.keyword = keyword
        self.pagenum = pagenum
        params = {
            'host': 'localhost', 'port': 3306,
            'user': 'root', 'password': '123456',
            'database': 'crawl_spider', 'charset': 'utf8'
        }
        self.conn = pymysql.connect(**params)
        self.cursor = self.conn.cursor()
        self._sql = None
        self.headers = {
                'Cookie': 'bid=Osy-EVfqvCk; __gads=ID=d4f9305d7191d433-22a4901a4ecf003a:T=1638234183:RT=1638234183:S=ALNI_MZh1i0ycPX7ySS2C2hkaTNe3s_9bw; ll="118241"; gr_user_id=df96dfb4-2d6a-4a3d-bb19-627cc2b49c7c; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=4039fa66-4f4b-4c29-a47f-5d6a033d7ce3; gr_cs1_4039fa66-4f4b-4c29-a47f-5d6a033d7ce3=user_id%3A0; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1643939078%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DPAEXxnpDuI3wf4bE3C03XGAyPlundERHI_vfJptLvmwEyKFMAhZveHsUFnBb_DwH%26wd%3D%26eqid%3Dd5dc7e580044026c0000000261fc84ff%22%5D; _pk_ses.100001.3ac3=*; ap_v=0,6.0; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_4039fa66-4f4b-4c29-a47f-5d6a033d7ce3=true; __utmc=30149280; __utma=30149280.261967570.1638234182.1640403808.1643939078.5; __utmz=30149280.1643939078.5.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt_douban=1; __utmz=81379588.1643939078.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=81379588.2099958529.1643939078.1643939078.1643939078.1; __utmc=81379588; __utmt=1; _vwo_uuid_v2=D232D22289DE2C2577245ABE7763DC2FE|d2d47e8effab6b7bc6d7c35398900219; _ga=GA1.1.261967570.1638234182; _ga_RXNMP372GL=GS1.1.1643939329.1.0.1643939335.54; viewed="4822685_35546622"; _pk_id.100001.3ac3=c198968bd0de658c.1643939078.1.1643939367.1643939078.; __utmb=30149280.8.10.1643939078; __utmb=81379588.8.10.1643939078',
                'Referer': 'https://book.douban.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
        }
        self.url = 'https://book.douban.com/'

    def run(self):
        for page in range(self.pagenum):
            url = f'https://book.douban.com/tag/{quote(self.keyword)}?start={20*page}&type=T'
            resp = requests.get(url,headers=self.headers).text
            html = etree.HTML(resp)
            self.parse(html)
            time.sleep(2)

    def parse(self,html):
        book_lis = html.xpath("//li[@class='subject-item']")
        for book in book_lis:
            title = book.xpath(".//h2/a/@title")[0]
            score = book.xpath(".//span[@class='rating_nums']/text()")[0]
            com_count_text = book.xpath(".//span[@class='pl']/text()")[0]
            com_count = re.sub(r'\s|(|)','',com_count_text)
            info_texts = book.xpath(".//div[@class='pub']/text()")[0]
            infos = re.sub(r'\s','',info_texts)
            intro = book.xpath(".//div[@class='info']/p/text()")[0]
            detail_url = book.xpath(".//h2/a/@href")[0]
            book_data = (title,score,com_count,infos,intro,detail_url)
            self.storage_data(book_data)
    @property
    def sql(self):
        if not self._sql:
            self._sql = '''insert into douban_book(title,score,com_count,infos,intro,detail_url) values(%s,%s,%s,%s,%s,%s);'''
            return self._sql
        return self._sql

    def storage_data(self,data):
        self.cursor.execute(self.sql,data)
        self.conn.commit()

def main():
    keyword = input('请输入数据类型>>>')
    pagenum = int(input('请输入页数,每页20本书籍>>>'))
    spider = DoubanBookSpider(keyword,pagenum)
    spider.run()
    print('爬取完成')

if __name__ == '__main__':
    main()