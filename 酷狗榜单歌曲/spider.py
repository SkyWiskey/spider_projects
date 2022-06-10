import time,json,os,re

import requests
from lxml import etree

class KugouMusicSpider(object):
    def __init__(self,file_path,urls):
        self.urls = urls
        self.file_path = file_path
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
        }
        self.time_now = int(time.time()*1000)
    def run(self):
        for url in self.urls:
            resp = requests.get(url,headers=self.headers)
            html = etree.HTML(resp.text)
            list_name = html.xpath("//div[@id='pc_temp_title']/h3/text()")[0]
            print(f'===========正在下载：{list_name}==========')
            re_hash = re.compile('"Hash":"(.*?)"',re.S | re.I)
            re_album_id = re.compile('"album_id":(\d+)',re.S | re.I)
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
                '_': self.time_now
            }
            song_req = requests.get(detail_url, params=params).text
            start = song_req.find('{"status"')
            song_data = json.loads(song_req[start:-2])['data']
            song_url = song_data['play_url']
            song_name = song_data['song_name']
            self.storage_data(song_url,song_name,list_name)
    def storage_data(self,url,name,list_name):
        try:
            file_path = os.path.join(self.file_path,list_name)
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            with open(f'{file_path}/{name}.mp3','wb')as f:
                f.write(requests.get(url,headers=self.headers).content)
            print(f'正在下载:{name}')
        except:
            pass

def main():
    cwd = os.getcwd()
    file_path = os.path.join(cwd,'歌曲')
    if not os.path.exists(file_path):
        os.makedirs(file_path)
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
    spider = KugouMusicSpider(file_path,urls)
    spider.run()
    print('下载完成')

if __name__ == '__main__':
    main()