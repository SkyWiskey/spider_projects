import time

import requests
from lxml import etree

from settings import conn,cursor


class DangdangBookSpider(object):
    def __init__(self,url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'
        }
        self._sql = None
    def run(self):
        resp = requests.get(self.url)
        html = etree.HTML(resp.text)
        # 小说
        book_category_links = html.xpath("//div[@class='sub']/ul/li/a/@href")[3]
        resp = requests.get(book_category_links,headers=self.headers).text
        html = etree.HTML(resp)
        # 小说的分类
        detail_categorys = html.xpath("//dl[@class='primary_dl']//a")
        for category in detail_categorys:
            title = category.xpath(".//@title")[0]
            href_text = category.xpath(".//@href")[0]
            end = href_text.find("#")
            href = href_text[:end]
            self.parse_detail_category_url(title,href)
            time.sleep(3)

    # 小说的每个分类的内容获取
    def parse_detail_category_url(self,category_name,category_url):
        for i in range(1,51):
            print(f'正在爬取分类：{category_name} 第：{i}页')
            url_list = category_url.split('/')
            url = 'https://category.dangdang.com/' + f'pg{i}-' + url_list[-1]
            resp = requests.get(url,headers=self.headers).text
            html = etree.HTML(resp)
            book_lis = html.xpath("//ul[@id='component_59']/li")
            for book in book_lis:
                try:
                    #书籍名称
                    book_title = book.xpath(".//a/@title")[0].strip()
                    # 价格
                    book_price = ''.join(book.xpath(".//p[@class='price']//text()"))
                    # 评论数
                    book_commont_count = book.xpath(".//p[@class='search_star_line']//a/text()")[0].strip()
                    book_infos = ''.join(book.xpath("p[@class='search_book_author']//text()"))
                    info_list = book_infos.split('/')
                    # 作者&译者
                    book_author = info_list[0].strip()
                    # 发布时间
                    book_pub_time = info_list[1].strip()
                    # 出版社
                    book_press = info_list[-1].strip()
                    # 简介
                    book_intro = book.xpath(".//p[@class='detail']/text()")
                    if not book_intro:
                        book_intro = '空'
                    else:
                        book_intro = book_intro[0]
                    data = [category_name,book_title,book_price,book_commont_count,
                            book_author,book_pub_time,book_press,book_intro]
                    self.storage_data(data)
                except:
                    pass

            time.sleep(2)

    # SQL语句
    @property
    def sql(self):
        if not self._sql:
            self._sql = ''' insert into dangdangbook(category,book_title,book_price,book_commont_count,
                        book_author,book_pub_time,book_press,book_intro) values(%s,%s,%s,%s,%s,%s,%s,%s);'''
            return self._sql
        return self._sql

    # 存储到MySQL
    def storage_data(self,data):
        cursor.execute(self.sql,data)
        conn.commit()


def main():
    url = 'http://book.dangdang.com/'
    spider = DangdangBookSpider(url)
    spider.run()

if __name__ == '__main__':
    main()