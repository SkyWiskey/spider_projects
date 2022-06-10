import time
import json
import os

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 忽略requests证书警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class QuanjingImageSpider(object):
    time_now = int(time.time()*1000)
    def __init__(self,keyword,pagenum):
        self.keyword = keyword
        self.pagenum = pagenum
        self.headers = {
            'Referer': 'https://www.quanjing.com/search.aspx?q=%E6%98%A5%E8%8A%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
        }

    def run(self):
        url = 'https://www.quanjing.com/Handler/SearchUrl.ashx?'
        for page in range(1,self.pagenum+1):
            params = {
                't': 7701,'callback': 'searchresult',
                'q': self.keyword,'stype': 1,
                'pagesize': 100,'pagenum': page,
                'imageType': 2,'fr': 1,
                'sortFlag': 1,'_': self.time_now
            }
            resp = requests.get(url,params=params,headers=self.headers)
            self.parse(resp.text)
            time.sleep(2)

    def parse(self,text):
        start = text.find('{"pageindex"')
        end = text.find('"}]}')+len('"}]}')
        json_data = json.loads(text[start:end])
        for image in json_data['imglist']:
            image_url = image['imgurl']
            image_id = image['pic_id']
            self.storage_data(image_url,image_id)

    def storage_data(self,image_url,image_id):
        print(f'正在下载：{image_url}')
        file_path = os.path.join('图片',self.keyword)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        with open(f'{file_path}/{image_id}.png','wb')as f:
            f.write(requests.get(image_url,verify=False).content)

def main():
    if not os.path.exists('图片'):
        os.mkdir('图片')
    keyword = input('请输入图片类型>>')
    pagenum = int(input('请输入页数,每页100张>>>'))
    spider = QuanjingImageSpider(keyword,pagenum)
    spider.run()
    print('图片下载完成')

if __name__ == '__main__':
    main()
