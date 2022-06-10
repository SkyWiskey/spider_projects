import time,re

import requests
import pymysql
from lxml import etree

class HotSearchSpider(object):
    def __init__(self,urls):
        params = {
            'host':'localhost','port':3306,
            'user':'root','password':'123456',
            'database':'crawl_spider','charset':'utf8'
        }
        self.conn = pymysql.connect(**params)
        self.cursor = self.conn.cursor()
        self._sql = None
        self.urls = urls
        self.headers = {
            'Cookie': 'SUB=_2AkMWrxWof8NxqwJRmf8RzmvmbotyyADEieKg8-RzJRMxHRl-yT9jqkYztRB6PS87Rc0ABL7taFrc1EAhDB-R1vuuIEMY; _s_tentry=www.baidu.com; UOR=www.baidu.com,s.weibo.com,www.baidu.com; Apache=1934413930464.016.1644217869417; SINAGLOBAL=1934413930464.016.1644217869417; ULV=1644217869424:1:1:1:1934413930464.016.1644217869417:',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
        }

    def run(self):
        for url in self.urls:
            print(f'正在爬取：{url}')
            resp = requests.get(url,headers=self.headers)
            resp.encoding = resp.apparent_encoding
            html = etree.HTML(resp.text)
            self.parse(html)
            time.sleep(2)

    def parse(self,html):
        trs = html.xpath("//div[@class='data']/table/tbody/tr")
        for tr in trs:
            try:
                title = tr.xpath(".//td[2]/a/text()")[0].strip()
                hot = tr.xpath(".//td[2]/span/text()")[0]
                hot = re.sub(r'\s','',hot)
                href = 'https://s.weibo.com' + tr.xpath(".//td[2]/a/@href")[0]
                if not href.endswith('top'):
                    pass
                self.storage_data(title,hot,href)
            except:
                pass

    @property
    def sql(self):
        if not self._sql:
            self._sql = '''insert into weibo values(%s,%s,%s,%s)'''
            return self._sql
        return self._sql

    def storage_data(self,title,hot,href):
        self.cursor.execute(self.sql,(time.strftime('%Y-%m-%d'),title,hot,href))
        self.conn.commit()

def main():
    urls = ['https://s.weibo.com/top/summary?cate=realtimehot',
            'https://s.weibo.com/top/summary?cate=entrank',]
    spider = HotSearchSpider(urls)
    spider.run()
    print(f'微博热搜榜、文娱榜爬取完成')
if __name__ == '__main__':
    main()