import time
import json
import csv
import os

import requests

class VphSpider(object):
    def __init__(self,keyword,pagenum,file_path):
        self.keyword = keyword
        self.pagenum = pagenum
        self.file_path = file_path
        self.time_now = int(time.time()*1000)
        self.pid_url = 'https://mapi.vip.com/vips-mobile/rest/shopping/pc/search/product/rank?'
        self.product_url = 'https://mapi.vip.com/vips-mobile/rest/shopping/pc/product/module/list/v2?'
        self.headers = {
                'cookie': 'vip_cps_cid=1637377980641_2d88d390b8a8f1dcea8d51bd21bace51; PAPVisitorId=67eb1dbb5e41b32e5b3cf8a667fbc678; vip_new_old_user=1; mars_pid=0; vip_cps_cuid=CU1643436178964ce77deb01f1e7076c; cps_share=cps_share; vip_wh=VIP_NH; vip_address=%257B%2522pname%2522%253A%2522%255Cu5e7f%255Cu4e1c%255Cu7701%2522%252C%2522pid%2522%253A%2522104104%2522%252C%2522cname%2522%253A%2522%255Cu5e7f%255Cu5dde%255Cu5e02%2522%252C%2522cid%2522%253A%2522104104101%2522%257D; vip_province=104104; vip_province_name=%E5%B9%BF%E4%B8%9C%E7%9C%81; vip_city_name=%E5%B9%BF%E5%B7%9E%E5%B8%82; vip_city_code=104104101; user_class=a; VipUINFO=luc%3Aa%7Csuc%3Aa%7Cbct%3Ac_new%7Chct%3Ac_new%7Cbdts%3A0%7Cbcts%3A0%7Ckfts%3A0%7Cc10%3A0%7Crcabt%3A0%7Cp2%3A0%7Cp3%3A1%7Cp4%3A0%7Cp5%3A0%7Cul%3A3105; mst_area_code=104104; mars_sid=a035f5c51a8c30df905b46e7e4e8b1fe; visit_id=299F3C598445039685FDDF8BD6B715BE; cps=adp%3Antq8exyc%3A%40_%401643436238200%3Amig_code%3A4f6b50bf15bfa39639d85f5f1e15b10f%3Aac014miuvl0000b5sq8cnvd7pvc9fzge; vpc_uinfo=fr713:0,fr674:D1,fr1051:0,fr766:0,fr259:S0-4,fr896:0,fr0901:0,fr863:0,fr392:310505,fr398:0,fr408:0,fr251:A,fr344:0,fr444:A,fr848:0,fr249:A1,fr328:3105,fr902:0,fr901:0; vip_tracker_source_from=; vipshop_passport_src=https%3A%2F%2Fdetail.vip.com%2Fdetail-1711797210-6919605951349976154.html; VipDFT=0; vip_access_times=%7B%22list%22%3A7%2C%22detail%22%3A0%7D; pg_session_no=20; mars_cid=1637377977209_ab7fe5ea15483fbb451567d67d634f90',
                'referer': 'https://category.vip.com/',
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
        }
    def run(self):
        for page in range(self.pagenum):
            params = {
                'callback': 'getMerchandiseIds',
                'app_name': 'shop_pc',
                'app_version': 4.0,
                'warehouse': 'VIP_NH',
                'fdc_area_id': '104104101',
                'client': 'pc',
                'mobile_platform': 1,
                'province_id': 104104,
                'api_key': '70f71280d5d547b2a7bb370a529aeea1 ',
                'mars_cid': '1637377977209_ab7fe5ea15483fbb451567d67d634f90',
                'wap_consumer': 'a',
                'standby_id': 'nature',
                'keyword': self.keyword,
                'sort': 0,
                'pageOffset': 120*page,
                'channelId': 1,
                'gPlatform': 'PC',
                'batchSize': 120,
                '_': self.time_now
            }
            time.sleep(2)
            self.get_pid(params)

    def get_pid(self,params):
        resp = requests.get(self.pid_url,params=params,headers=self.headers).text
        start = resp.find('{"code"')
        end = resp.find(']}}')+len(']}}')
        pid_data = json.loads(resp[start:end])['data']['products']
        for data in pid_data:
            pid = data['pid']
            self.crawl_data(pid)

    def crawl_data(self,pid):
        params = {
            'callback': 'getMerchandiseDroplets1',
            'app_name': 'shop_pc',
            'app_version': 4.0,
            'warehouse': 'VIP_NH',
            'fdc_area_id': 104104101,
            'client': 'pc',
            'mobile_platform': 1,
            'province_id': 104104,
            'api_key': '70f71280d5d547b2a7bb370a529aeea1',
            'mars_cid': '1637377977209_ab7fe5ea15483fbb451567d67d634f90',
            'wap_consumer': 'a',
            'productIds': pid,
            'scene': 'search',
            'standby_id': 'nature',
            'extParams': '{"stdSizeVids":"","preheatTipsVer":"3","couponVer":"v2","exclusivePrice":"1","iconSpec":"2x","ic2label":1}',
            '_': self.time_now
        }
        resp = requests.get(self.product_url,params=params,headers=self.headers).text
        start = resp.find('{"code"')
        end = resp.find('"}}')+len('"}}')
        product_data = json.loads(resp[start:end])['data']['products']
        for data in product_data:
            name = data['title']
            brand = data['brandShowName']
            picture = data['squareImage']
            discount = data['price']['saleDiscount']
            product_id = data['productId']
            price = data['price']['salePrice']
            self.storage_data(name,brand,discount,price,product_id,picture)

    def storage_data(self,name,brand,discount,price,product_id,picture):
        with open(f'{self.file_path}/商品信息.csv', 'a', encoding='utf8', newline='') as f:
            filewriter = csv.writer(f)
            filewriter.writerow([name,brand,discount,price,product_id])

        image_path = os.path.join(self.file_path,'images')
        if not os.path.exists(image_path):
            os.makedirs(image_path)

        with open(f'{image_path}/{product_id}.png','wb')as f:
            f.write(requests.get(picture,headers=self.headers).content)
        print('存储了一条信息...')

def main():
    keyword = input('请输入商品名称>>>')
    pagenum = int(input('请输入页数,每页120个商品>>>'))

    cwd = os.getcwd()
    file_path = os.path.join(cwd,'products',keyword)
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    csv_head = ['name','brand','discount','price','product_id']
    with open(f'{file_path}/商品信息.csv','a',encoding='utf8',newline='')as f:
        filewriter = csv.writer(f)
        filewriter.writerow(csv_head)
    spider = VphSpider(keyword,pagenum,file_path)
    spider.run()
    print('爬取完成')

if __name__ == '__main__':
    main()