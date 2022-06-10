import requests
import csv
import time

class tencent_careers_spider(object):
    def __init__(self):
        self.headers = {
            'referer': 'https://careers.tencent.com/search.html?index=2&keyword=python',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
        }
        self.url = 'https://careers.tencent.com/tencentcareer/api/post/Query?'
        self.pageiter = int(input('请输入页数,每页10个职位>>>'))
    def get_data(self):
        for page in range(1,self.pageiter+1):
            print(f'正在爬取第{page}页...')
            params = f'timestamp=1632624636963&keyword=python&pageIndex={page}&pageSize=10&language=zh-cn&area=cn'
            url = self.url + params
            resp = requests.get(url,headers = self.headers)
            json_data = resp.json()['Data']['Posts']
            self.download_data(json_data)
            time.sleep(0.5)

    def download_data(self,json_data):
        for data in json_data:
            job_name = data['RecruitPostName']
            job_loca = data['LocationName']
            job_type = data['CategoryName']
            job_lastpubtime = data['LastUpdateTime']
            job_responsibility = data['Responsibility']
            job_detail_link = data['PostURL']
            with open('tencent_careers.csv','a',encoding='utf8')as csvfile:
                filewriter = csv.writer(csvfile,delimiter = ',')
                filewriter.writerow([job_name,job_type,job_loca,job_lastpubtime,job_responsibility,job_detail_link])
                filewriter.writerow('-'*100)

if __name__ == '__main__':
    tencent_spider = tencent_careers_spider()
    tencent_spider.get_data()
    print('爬取完成！')