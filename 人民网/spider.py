import requests
from lxml import etree

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}

def crawler():
    url = 'http://cpc.people.com.cn/'
    resp = requests.get(url,headers=HEADERS)
    resp.encoding = resp.apparent_encoding
    html = etree.HTML(resp.text)
    lis = html.xpath("//div[@id='main']//ul[@class='list-nav1']/li")
    for li in lis[1:5]:
        href = li.xpath(".//a/@href")[0]
        parse(href)

def parse(url):
    if url.endswith('html'):
        resp = requests.get(url,headers=HEADERS)
        resp.encoding = resp.apparent_encoding
        html = etree.HTML(resp.text)
        detail_links = html.xpath("//div[@class='fl']/ul/li/a/@href")
        for link in detail_links:
            if not link.startswith('http'):
                link = 'http://cpc.people.com.cn/' + link
            print(link)

    print()

crawler()