#coding=utf8
import requests
from bs4 import BeautifulSoup
import pymysql

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    database='crawl_spider',
    charset='utf8'
)


class Haoduanzi:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
        }
        self._sql = None

    def crawl(self):
        url = 'http://www.haoduanzi.com/wen/'
        resp = requests.get(url,headers=self.headers)
        resp.encoding = resp.apparent_encoding
        soup = BeautifulSoup(resp.text,'lxml')
        links = soup.select('.list-box li .content a')
        return links
    def parse(self,links):
        datas = []
        for link in links:
            href = link['href']
            resp = requests.get(href,headers=self.headers)
            resp.encoding = resp.apparent_encoding
            soup = BeautifulSoup(resp.text,'lxml')
            title = soup.select_one('h1.arc-title').get_text()
            infos = soup.select('.arc-meta span')
            pub_time = infos[0].get_text()
            author = infos[1].get_text()
            category = infos[2].get_text()
            read_count = infos[-1].get_text()
            content = soup.select_one('.content').get_text().strip()
            data = {'title':title,'pub_time':pub_time,'author':author,
                    'category':category,'read_count':read_count,'content':content}
            datas.append(data)
        return datas

    @property
    def sql(self):
        if not self._sql:
            self._sql = '''insert into haoduanzi(title,pub_time,author,category,read_count,content) 
                            values(%s,%s,%s,%s,%s,%s)'''
            return self._sql
        return self._sql

    def storage(self,datas):
        cursor = conn.cursor()
        for data in datas:
            cursor.execute(self.sql,(data['title'],data['pub_time'],data['author'],
                                     data['category'],data['read_count'],data['content']))
            conn.commit()
            print(data)


    def __call__(self, *args, **kwargs):
        links = self.crawl()
        datas = self.parse(links)
        self.storage(datas)

def main():
    Haoduanzi().__call__()

if __name__ == '__main__':
    main()
