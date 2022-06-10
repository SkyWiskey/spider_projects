import csv
import time,re,os

import threading
import requests
from lxml import etree

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
}

def crawl(page):
    # 每页
    url = f'https://www.shicimingju.com/category/all_{page}'
    resp = requests.get(url,headers=headers)
    html = etree.HTML(resp.text)
    authors = html.xpath("//h3")
    for author in authors:
        name = author.xpath(".//a/text()")[0]
        href_text = author.xpath(".//a/@href")[0]
        href = 'https://www.shicimingju.com/'+href_text
        # 每个诗人
        new_resp = requests.get(href,headers=headers)
        html = etree.HTML(new_resp.text)
        hrefs = html.xpath("//div[@id='list_nav_part']/a[position()<11]/@href")
        for h in hrefs:
            url = 'https://www.shicimingju.com/' + h
            req = requests.get(url,headers=headers)
            req.encoding = req.apparent_encoding
            html = etree.HTML(req.text)
            poems = html.xpath("//div[@class='shici_list_main']")
            for p in poems:
                title = p.xpath(".//h3/a/text()")[0]
                content_text = ''.join(p.xpath(".//div//text()"))
                content = (re.sub(r'\s','',content_text)).replace('原文展开','').replace('收起','')
                data = [name,title,content]
                storage(data)
                print(data)
    time.sleep(2)

def storage(data):
    if not os.path.exists('诗词'):
        os.mkdir('诗词')
    with open(f'诗词/{data[0]}.csv','a',encoding='utf8',newline='')as csvfile:
        filewriter = csv.writer(csvfile)
        filewriter.writerow(data)

def main():
    threadpool = []
    for page in range(1,3):
        threadpool.append(threading.Thread(target=crawl,args=(str(page),)))
    # 开启线程
    for t in threadpool:
        t.start()
    # 等待所有线程执行完毕
    for t in threadpool:
        t.join()


if __name__ == '__main__':
    main()