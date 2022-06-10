import time,json,os,re

import requests
from lxml import etree
from threading import Thread
from queue import Queue

HEADERS = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
        }
TIME_NOW = int(time.time()*1000)

class KugouProduce(Thread):
    def __init__(self,page_queue,data_queue,*args,**kwargs):
        super(KugouProduce, self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.data_queue = data_queue
    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            resp = requests.get(url,headers=HEADERS)
            html = etree.HTML(resp.text)
            list_name = html.xpath("//div[@id='pc_temp_title']/h3/text()")[0]
            print(f'===========正在下载：{list_name}==========')
            re_hash = re.compile('"Hash":"(.*?)"', re.S | re.I)
            re_album_id = re.compile('"album_id":(\d+)', re.S | re.I)
            hashs = re_hash.findall(resp.text)
            album_ids = re_album_id.findall(resp.text)
            self.parse(hashs,album_ids,list_name)
            time.sleep(2)

    def parse(self,hashs,album_ids,list_name):
        for hash_, album_id in zip(hashs, album_ids):
            detail_url = 'https://wwwapi.kugou.com/yy/index.php'
            params = {
                'r': 'play/getdata',
                'callback': 'jQuery191020222541727053622_1624455576282',
                'hash': hash_,
                'dfid': '1sTpkG39iuyQ1dnQSV1fzDvG',
                'mid': 'a83316d80cea795c7bfbc601f362e41f',
                'platid': '4',
                'album_id': album_id,
                '_': TIME_NOW
            }
            song_req = requests.get(detail_url, params=params).text
            start = song_req.find('{"status"')
            song_data = json.loads(song_req[start:-2])['data']
            song_url = song_data['play_url']
            song_name = song_data['song_name']
            self.data_queue.put((song_url,song_name,list_name))


class KugouConsume(Thread):
    def __init__(self,page_queue,data_queue,*args,**kwargs):
        super(KugouConsume, self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.data_queue = data_queue

    def run(self):
        while True:
            try:
                if self.page_queue.empty() and self.data_queue.empty():
                    break
                song_url,song_name,list_name = self.data_queue.get()
                cwd = os.getcwd()
                file_path = os.path.join(cwd, '歌曲',list_name)
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                with open(f'{file_path}/{song_name}.mp3','wb')as f:
                    f.write(requests.get(song_url,headers=HEADERS).content)
                print(f'正在下载:{song_name}')
            except:
                pass

def main():
    page_queue = Queue(15)
    data_queue = Queue(500)
    urls = ['https://www.kugou.com/yy/rank/home/1-6666.html?from=rank',
            'https://www.kugou.com/yy/rank/home/1-8888.html?from=rank',
            'https://www.kugou.com/yy/rank/home/1-52144.html?from=rank',
            'https://www.kugou.com/yy/rank/home/1-52767.html?from=rank',
            'https://www.kugou.com/yy/rank/home/1-24971.html?from=rank',
            'https://www.kugou.com/yy/rank/home/1-21101.html?from=rank',
            'https://www.kugou.com/yy/rank/home/1-31308.html?from=rank',
            'https://www.kugou.com/yy/rank/home/1-31313.html?from=rank',
            'https://www.kugou.com/yy/rank/home/1-54848.html?from=rank',
            'https://www.kugou.com/yy/rank/home/1-31310.html?from=rank',
            'https://www.kugou.com/yy/rank/home/1-33161.html?from=rank',
            'https://www.kugou.com/yy/rank/home/1-44412.html?from=rank',
            'https://www.kugou.com/yy/rank/home/1-33165.html?from=rank',]
    for url in urls:
        page_queue.put(url)

    for i in range(5):
        t = KugouProduce(page_queue,data_queue)
        t.start()
    for i in range(10):
        t = KugouConsume(page_queue,data_queue)
        t.start()

if __name__ == '__main__':
    main()
    print('酷狗热门榜单歌曲下载完成')