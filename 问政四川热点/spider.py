import csv
import time

import aiohttp
import asyncio
from  lxml import etree
import pandas as pd


headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'
        }

async def get_response(url):
    async with aiohttp.ClientSession()as session:
        async with session.get(url,headers=headers)as resp:
            if resp.status == 200:
                print(f'正在爬取:{url}')
                parse(await resp.text())

def parse(text):
    html = etree.HTML(text)
    item = dict()
    title = ''.join(t.strip() for t in html.xpath("//h2[@class='clearfix']/text()"))
    article = ''.join(t.strip()  for t in html.xpath("//div[@class='c1']/p[position()>1]/text()"))
    item['title'] = title
    item['article'] = article
    print(item)
    filewriter.writerow(item)

async def spider(url_tasks):
    """"""
    # tasks = [asyncio.create_task(spider()) for i in range(10)]
    # [await t for t in tasks]
    await asyncio.gather(*[get_response(url) for url in url_tasks])

if __name__ == '__main__':
    s = time.perf_counter()
    data = pd.read_csv('datas.csv')
    href_list = data['href'].tolist()


    fp = open('articles.csv','a',encoding='utf8',newline='')
    head = ['title','article']
    filewriter = csv.DictWriter(fp,head)
    filewriter.writeheader()

    # url_taks = []
    # for page in range(1,21):
    #     url = f'https://ly.scol.com.cn/welcome/showlist?keystr=wzrd&total=4955&page={page}'
    #     url_taks.append(url)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider(href_list))
    print(f'用时:{time.perf_counter() - s}')