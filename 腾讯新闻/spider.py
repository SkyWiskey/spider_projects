import time,csv

import requests
import pymysql

class NewsSpider(object):
    def __init__(self,pagenum):
        self.pagenum = pagenum
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'
        }

    def run(self):
        for page in range(self.pagenum):
            print(f'正在爬取第{page+1}页')
            url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?'
            params = {
                'sub_srv_id': '24hours',
                'srv_id': 'pc',
                'offset': page*20,
                'limit': 20,
                'strategy': 1,
                'ext': '{"pool":["top"],"is_filter":7,"check_type":true}'
            }
            resp = requests.get(url,params=params,headers=self.headers).json()
            self.parse(resp)
            time.sleep(2)

    def parse(self,resp):
        datas = resp['data']['list']
        for data in datas:
            id = data['article_id']
            category_cn = data['category_cn']
            title = data['title']
            pub_time = data['update_time']
            href = data['url']
            result = [title,id,category_cn,pub_time,href]
            self.storage_data(result)

    def storage_data(self,data):
        with open('news_qq.csv', 'a', encoding='utf8', newline='') as csvfile:
            filewrite = csv.writer(csvfile)
            filewrite.writerow(data)
        print('存储了一条信息')


def main():
    csv_head = ['title','id','category','pub_time','href']
    with open('news_qq.csv','a',encoding='utf8',newline='')as csvfile:
        filewrite = csv.writer(csvfile)
        filewrite.writerow(csv_head)
    pagenum = 5
    spider = NewsSpider(pagenum)
    spider.run()
    print(f'爬取完成,页数：{pagenum}')
if __name__ == '__main__':
    main()