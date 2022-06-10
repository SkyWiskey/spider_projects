import pymysql
import requests
from lxml import etree

class ZhihuBillboard(object):
    def __init__(self):
        params = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'database': 'crawl_spider',
            'charset': 'utf8',
        }
        self.conn = pymysql.connect(**params)
        self.cursor = self.conn.cursor()
        self._sql = None
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
        }

    def run(self):
        url = 'https://www.zhihu.com/billboard'
        resp = requests.get(url,headers =self.headers)
        html = etree.HTML(resp.text)
        hotlist = html.xpath("//a[@class='HotList-item']")

        for item in hotlist:
            title = item.xpath(".//div[@class='HotList-itemTitle']/text()")[0]
            hot = item.xpath(".//div[@class='HotList-itemMetrics']/text()")[0]
            print(title,hot)
            self.storage_data(title,hot)

    @property
    def sql(self):
        if not self._sql:
            self._sql = '''
            insert into zhihu(title,hot) values (%s,%s);
            '''
            return self._sql
        return self._sql

    def storage_data(self,title,hot):
        self.cursor.execute(self.sql,(title,hot))
        self.conn.commit()

def main():
    spider = ZhihuBillboard()
    spider.run()
    print('爬取完成')

if __name__ == '__main__':
    main()