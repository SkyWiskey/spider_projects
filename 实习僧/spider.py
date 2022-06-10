# 一、
#字体反爬虫
# import requests
# from lxml import etree
# import time
# import csv
#
# def shixiseng():
#     headers = {
#     'Host': 'www.shixiseng.com',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
#     }
#     url = 'https://www.shixiseng.com/interns?keyword=python&page=1&type=intern'
#     resp = requests.get(url,headers = headers)
#     html = etree.HTML(resp.text)
#     one = ''.encode('utf8')
#     two = ''.encode('utf8')
#     three = ''.encode('utf8')
#     four = ''.encode('utf8')
#     five= ''.encode('utf8')
#     zero = ''.encode('utf8')
#     eigthy = '0'.encode('utf8')
#     eight_hunred = ''.encode('utf8')
    # salarys = html.xpath("//span[@class='day font']/text()")
    # for salary in  salarys:
    #     numbers = salary.encode('utf8').replace(zero,b'0').replace(one,b'1').replace(two,b'2').\
    #     replace(three,b'3').replace(four,b'4').replace(five,b'5').replace(eigthy,b'80').replace(eight_hunred,b'800')
    #     print(numbers.decode('utf8'))
    #     break
#     titles = html.xpath("//a[@class='title ellipsis font']/text()")
#     c = '' 'Python工程师'
#     c2 = '实习'  'Python实习生'
#     c3 = ''  'Python工程师'
#     c4 = '开发' 'Python开发工程师'
#     c5 = '实习' 'python工程师实习生'
#     c6 = '实习' 'python实习生'
#     c7 = '' 'python前端工程师'
#     python = ''.encode('utf8')
#     Python = ''.encode('utf8')
#     a = ''.encode('utf8')
#     b = ''.encode('utf8')
#     c = ''.encode('utf8')
#     for title in titles:
#         title = title.encode('utf8').replace(python,b'python').replace(Python,b'Python').\
#             replace(a,'生'.encode('utf8')).replace(b,'工程师'.encode('utf8')).replace(c,'前端'.encode('utf8'))
#         print(title.decode('utf8'))
#
# shixiseng()


# 二、
# 先爬取详情页链接再爬取内容没有字体反爬虫
import requests
from lxml import etree
import time
import csv

headers = {
    'Host': 'www.shixiseng.com',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
}
def ShixisengSpider(url):
    resp = requests.get(url,headers = headers)
    html = etree.HTML(resp.text)
    links = html.xpath("//div[@class='f-l intern-detail__job']/p/a/@href")
    for link in links:
        parse_url(link)
        time.sleep(1)
def parse_url(link):
    resp = requests.get(link,headers=headers)
    html = etree.HTML(resp.text)
    title = html.xpath("//div[@class='new_job_name']/span/text()")[0]
    salary = html.xpath("//span[@class='job_money cutom_font']/text()")[0]
    location = html.xpath("//span[@class='job_position']/@title")[0]
    weekday = html.xpath("//span[@class='job_week cutom_font']/text()")[0]
    practice_time = html.xpath("//span[@class='job_time cutom_font']/text()")[0]
    job_need = html.xpath("//div[@class='job_detail']/p/text()")
    job_responsibility =' '.join(i.strip().replace(' ','').replace('\n','') for i in job_need)
    result = [title,salary,location,weekday,practice_time,job_responsibility]
    with open('shixiseng.csv','a',encoding='utf8',newline='')as csvfile:
        filewriter = csv.writer(csvfile)
        filewriter.writerow(result)
        print(f'存储了一条职位信息...')

def main():
    csvfile_head = ['工作名称','薪水','地点','工作量','时长','工作职责']
    with open('shixiseng.csv','a',encoding='utf8',newline='')as csvfile:
        filewriter = csv.writer(csvfile)
        filewriter.writerow(csvfile_head)
    url = 'https://www.shixiseng.com/interns?keyword=python&page=1&type=intern'
    ShixisengSpider(url)
if __name__ == '__main__':
    main()
    print('实习僧岗位爬取结束')