import requests
import re
import os
from urllib.parse import quote


# 图虫网图片下载
image_id_re = re.compile('"image_id":"(\d+)"')
keyword = input('请输入想要下载的图片类型>>>')
pagenum = int(input('请输入页数,每页100张图片>>>'))
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'Accept-Encoding':''
}
def get_image():
    image_url_list = []
    for i in range(1,pagenum+1):
        url = 'https://stock.tuchong.com/search?&page={}&platform=image&size=100&sortBy=0&term={}'.format(i,quote(keyword))
        html = requests.get(url,headers = headers)
        # print(html.text)
        image_id_list = image_id_re.findall(html.text)
        # print(image_id_list)
        for image_id in image_id_list:
            image_url_list.append('https://cdn3-banquan.ituchong.com/weili/l/{}.webp'.format(image_id))
    return image_url_list

def download_image(image_url_list,keyword):
    cwd = os.getcwd()
    file_name = os.path.join(cwd, '图虫网图片下载', keyword)
    if not os.path.exists(keyword):
        os.mkdir(file_name)
    try:
        for index,image_url in enumerate(image_url_list,start=1):
            print('正在下载url:',image_url)
            with open(file_name+f'\\{index}.webp','wb')as f:
                f.write(requests.get(image_url,headers = headers).content)
    except:
        pass

if __name__ =='__main__':
    image_url_list = get_image()
    download_image(image_url_list,keyword)
    print(f'《{keyword}》类型图片下载完成')

