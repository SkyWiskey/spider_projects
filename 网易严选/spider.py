import time

import requests

class CrawlYou163:
    """网易严选商品信息爬取"""
    def __init__(self,keyword,pagenum):
        self.headers = {
            'Referer': 'http://you.163.com/search?keyword=%E6%8B%96%E9%9E%8B&timestamp=1651818273053&_stat_search=hot&searchWordSource=8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
        }
        self.keyword = keyword
        self.pagenum = pagenum


    def run(self):
        url = 'http://you.163.com/xhr/search/search.json?'
        for page in range(1,self.pagenum+1) :
            params = {
                '__timestamp': int(time.time()*1000),
                'page': 1,
                'sortType': 0,
                'categoryId': 0,
                'descSorted': 'true',
                'matchType': 0,
                'floorPrice': -1,
                'upperPrice': -1,
                'stillSearch': 'false',
                'searchWordSource': 1,
                'size': 40,
                'keyword': self.keyword,
                'needPopWindow': 'true'
            }
            resp = requests.get(url,params=params,headers=self.headers).json()
            self.parse(page,resp)

    def parse(self,page,resp):
        if resp['data']['directly'] == None:
            print(f'抱歉，您要找的"{self.keyword}"还未上架')
        else:
            print(f'正在解析第{page}页数据')
            intro_data = resp['data']['directly']['searcherResult']['pagination']
            size = intro_data['size']
            total = intro_data['total']
            total_page = intro_data['totalPage']
            product_data = resp['data']['directly']['searcherResult']['result']
            for data in product_data:
                title = data['name']
                id = data['id']
                price = data['retailPrice']
                desc = data['simpleDesc']
                print([title,id,price,desc])

    def storage(self):
        pass

def main():
    keyword = '拖鞋'
    pagenum = 1
    spider = CrawlYou163(keyword,pagenum)
    spider.run()

if __name__ == '__main__':
    main()