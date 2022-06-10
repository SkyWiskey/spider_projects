import threading
from queue import Queue
from urllib.parse import quote
from uuid import uuid4
import time
import os
import requests


class BaiduImageProduce(threading.Thread):
    def __init__(self,page_queue,data_queue,keyword,*args,**kwargs):
        super(BaiduImageProduce, self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.data_queue = data_queue
        self.keyword = keyword
        self.headers = {
            'Cookie': 'BDqhfp=%E6%98%9F%E6%98%9F%26%260-10-1undefined%26%260%26%261; PSTM=1635647537; BAIDUID=12FE04D9061BC58E404117AFE83361B6:FG=1; BIDUPSID=67304EBF36A1D9129F4C525130D31730; __yjs_duid=1_0067c0014efb6dea8dc475204fc2c71b1635653733651; BDUSS=tzOWtqWUZ1b1Y3YWs4QjZZYXJuVUwzV1FFcWtBZzA5ci1UR0x5QkVlQmRkTVpoRVFBQUFBJCQAAAAAAAAAAAEAAAApnj990NzS1bey1~bO0sPDw8MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAF3nnmFd555hSk; BDUSS_BFESS=tzOWtqWUZ1b1Y3YWs4QjZZYXJuVUwzV1FFcWtBZzA5ci1UR0x5QkVlQmRkTVpoRVFBQUFBJCQAAAAAAAAAAAEAAAApnj990NzS1bey1~bO0sPDw8MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAF3nnmFd555hSk; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=35266_35105_35239_35457_34584_34517_35327_35316_26350; delPer=0; PSINO=1; BA_HECTOR=a004a4agaha12g2h8o1gr5j0b0r; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; userFrom=www.baidu.com; firstShowTip=1; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; indexPageSugList=%5B%22%E6%98%9F%E6%98%9F%22%2C%22%E5%8A%A8%E6%80%81%E6%98%9F%E7%A9%BA%22%2C%22%E5%8A%A8%E6%80%81%E6%B3%A1%E6%B2%AB%22%5D; cleanHistoryStatus=0; ab_sr=1.0.1_NDc5ZjEzZTBlNjZhMmZkMjQ1NDI4NzM3M2Y4OTk4ZDczM2Q5ZWIyZjcyZDgwOTI2ZmE0NWRiMGQxNWY4N2I5NzM5MzE3N2I0Y2E2MDI3NjhmMzMxMWIzYzM2YzQzODcwYzdmNDU3NTEwNGQwMTQyZGY3ZmMwYWY5ZDg1MGY4YzE3M2M4NzIxNjBjNDM0NDIwOGQ2ZjUyZGZiMDBiMDkxOGIzMmYwMDVmMjY5NjBkNDJhYTdjMjZhODAyYzBjNWFl',
            'Referer': 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1639107605150_R&pv=&ic=0&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=&ie=utf-8&sid=&word={}'.format(quote(keyword)),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
        }

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.get_image_url(url)
            time.sleep(2)

    def get_image_url(self,url):
        html = requests.get(url,headers = self.headers).json()
        links = html['data']
        page = int(url.split('pn=')[-1].split('&')[0])//30
        print(f'===========正在下载第{page}页图片===========')
        for link in links:
            if link:
                image_url = link['thumbURL']
                self.data_queue.put(image_url)


class BaiduImageConsume(threading.Thread):
    def __init__(self,page_queue,data_queue,filename,*args,**kwargs):
        super(BaiduImageConsume, self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.data_queue = data_queue
        self.filename = filename

    def run(self):
        while True:
            try:
                if self.page_queue.empty() and self.data_queue.empty():
                    break
                image_url = self.data_queue.get()
                with open('{}/{}.png'.format(self.filename,uuid4()),'wb') as f:
                    f.write(requests.get(image_url).content)
                print('下载了图片:{}'.format(image_url))
            except Exception as e:
                print(e)

def main():
    keyword = input('请输入想要爬取的图片关键词>>>')
    pagenum = int(input('请输入想要爬取的页数,每页30张图片>>>'))
    page_queue = Queue(pagenum)
    data_queue = Queue(pagenum*30)
    if not os.path.exists(keyword):
        os.mkdir(keyword)
    filename = keyword

    for page in range(1,pagenum+1):
        params = f'tn=resultjson_com&logid=7067464153408532593&ipn=rj\
        &ct=201326592&is=&fp=result&fr=&word={quote(keyword)}&queryWord={quote(keyword)}\
        &cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&s=&se=\
        &tab=&width=&height=&face=0&istype=2&qc=&nc=1&expermode=&nojc=&isAsync=&pn={page*30}&rn=30\
        &gsm=1e&1639107623094='
        url_head = 'https://image.baidu.com/search/acjson?'
        url = url_head+params
        page_queue.put(url)
    for i in range(5):
        p = BaiduImageProduce(page_queue,data_queue,keyword)
        p.start()
    time.sleep(2)
    for i in range(5):
        p = BaiduImageConsume(page_queue,data_queue,filename)
        p.start()

if __name__ == '__main__':
    main()