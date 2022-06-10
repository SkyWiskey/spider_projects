import requests
import os
from urllib.parse import quote


keyword = input('请输入想要查询的图片类型>>>')
pagenum = int(input('请输入页数,每页20张>>>'))
headers = {
    'Cookie': 'sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217baff51cd6930-0f7353236bb081-c343365-1327104-17baff51cd7a6a%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%7D%2C%22%24device_id%22%3A%2217baff51cd6930-0f7353236bb081-c343365-1327104-17baff51cd7a6a%22%7D; acw_tc=2760826316307482362476689e9dabcbdcb09ad65a6b85ccfdd20f0587ad1b; SESSION=fd292dae-3e0e-437d-9172-a21dedde646d; JSESSIONID=561C4F0E4D4EE5C88976D07CE8AF9B84; testapp=s%3A_MV97fC8lD8GDtq9b-acRRjm7etzkIWM.wXYxxSr1QQQLldyYNWRDMjlksyvUK%2BwXM7hJg%2BWoPrk; Hm_lvt_3eea10d35cb3423b367886fc968de15a=1630744684,1630748239,1630748254,1630748283; otherImg=618999f74873444f83613ee7d0285132; Hm_lpvt_3eea10d35cb3423b367886fc968de15a=1630748331',
    'Host': '500px.com.cn',
    'Referer': 'https://500px.com.cn/community/search?key={}&searchtype=photos'.format(quote(keyword)),
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

def get_image():
    image_url_list = []
    for page in range(1,pagenum+1):
        url = 'https://500px.com.cn/community/searchv2?&orderBy=alike&key={}\
        &searchType=photoAndGroup&page={}&size=20&type=json'.format(quote(keyword),page)
        html = requests.get(url,headers = headers)
        json_data = html.json()['data']
        for data in json_data:
            image_url_list.append(data['url']['baseUrl'])

    return image_url_list


def download_image(image_url_list):
    if not os.path.exists(keyword):
        os.mkdir(keyword)
    for index,image_url in enumerate(image_url_list,start=1):
        print('正在下载:',image_url)
        with open(keyword+'\\{}.jpg'.format(index),'wb')as f:
            f.write(requests.get(image_url).content)

if __name__ == '__main__':
    image_url_list = get_image()
    download_image(image_url_list)
    print('图片下载完成')