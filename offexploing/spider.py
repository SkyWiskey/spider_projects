import csv
import time

import requests
from lxml import etree

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
}

# 爬取数据
def crawler(url):
    resp = requests.get(url,headers=HEADERS).text
    html = etree.HTML(resp)
    lis = html.xpath("//li[@class='thumbnails']//a/@href")
    for li in lis:
        href = 'https://www.offexploring.com' + li
        detail_resp = requests.get(href,headers=HEADERS,timeout=60).text
        detail_html = etree.HTML(detail_resp)
        comment = None
        comment_text = detail_html.xpath("//div[@class='item_content']/text()")
        if comment_text:
            comment = comment_text[0].strip().replace('\n','')
        else:
            comment = ''.join(detail_html.xpath("//div[@class='entry_body']/p/text()")).strip().replace('\n','')
        print(comment)
        with open('guilin.csv', 'a', encoding='utf8', newline='') as f:
            filewriter = csv.writer(f)
            filewriter.writerow([comment])


def main():
    with open('guilin.csv','a',encoding='utf8',newline='')as f:
        filewriter = csv.writer(f)
        filewriter.writerow(['comment'])

    # 自己设置页数
    for page in range(1,11):
        url = f'https://www.offexploring.com/search/place/guilin/page-{page}'
        print(f'正在爬取第{page}页数据')
        crawler(url)
        time.sleep(2)


if __name__ == '__main__':
    main()
