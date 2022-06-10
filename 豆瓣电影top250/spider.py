import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook


def spider(page):
    for i in range(page):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(25 * i)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62'
        }
        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.text, 'lxml')
        results = soup.select('#wrapper .grid_view li .item')
        print(results)
        parse(results)


def parse(results):
    for result in results:
        try:
            file_name = result.select_one(' .info .hd .title').text.strip().replace(' ', '').replace('/', '')
            file_score = result.select_one(' .info .bd .star .rating_num').text.strip().replace(' ', '').replace('/',
                                                                                                                 '')
            file_comment_number = result.select(' .info .bd .star span')[3].text.strip().replace(' ', '').replace('/',
                                                                                                                  '')
            file_quote = result.select_one(' .info .bd .quote').text.strip().replace(' ', '').replace('/', '')
            file_comment_number = file_comment_number[:file_comment_number.find('人')]
            file_url = result.select_one(' .info .hd a')['href']
            # 电影id再链接最后,用split()拆分 取出id编号
            file_url_split = file_url.strip().split('/')
            file_id = file_url_split[4]
            # print(file_id)
            file_infos = result.select_one(' .info .bd p').text.strip()
            # print(file_infos)
            # 导演/主演/年份/地区/类型 split()拆分
            file_infos_split = file_infos.split('\n')
            # print(file_infos_split)
            file_infos_split1 = file_infos_split[0]  # 导演和演员信息
            # print(file_infos_split1)
            file_infos_split2 = file_infos_split[1]  # 年份、地点、类型信息
            # print(file_infos_split2)
            file_infos_1 = file_infos_split1.split('\xa0\xa0\xa0')  # 将导演和演员的信息用'\xa0\xa0\xa0'拆分
            # print(file_infos_1)
            file_director = file_infos_1[0].strip().split(':')[1]  # 导演
            # print(file_director)
            file_actors = file_infos_1[1].strip().split(':')[1]  # 主演
            # print(file_actors)
            file_infos_2 = file_infos_split2.split('/')  # 将年份、地点、类型信息用'/'进行拆分
            file_year = file_infos_2[0].strip()  # 年份
            file_country = file_infos_2[1].strip()  # 地区
            file_type = file_infos_2[2].strip()  # 类型

            data = [file_name, file_score, file_id, file_director, file_actors, file_year, file_country,
                    file_type, file_comment_number, file_quote, file_url]
            sheet.append(data)
        except:
            pass
    workbook.save(filename='豆瓣电影top250.xlsx')


workbook = Workbook()
sheet = workbook.active
sheet.append(
    ['电影名称', '评分', 'id', '导演', '主演', '年份', '国家', '类型', '评价人数', '摘要', '电影链接']
)

spider(10)
print('豆瓣电影top250信息下载完成')

