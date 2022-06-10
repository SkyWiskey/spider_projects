import requests
from openpyxl import Workbook

def getUserInfo():
    headers = {
            'cookie': 'innersign=0; bsource=search_baidu; _uuid=96C77836-3D7A-3F68-0AC3-CBBC9B499B0015654infoc; buvid3=0667FE13-3B3C-4AF4-9F1D-2F8AAF373B50148798infoc; fingerprint=2df7d11d68f34e7dd79166998985fe7f; buvid_fp=0667FE13-3B3C-4AF4-9F1D-2F8AAF373B50148798infoc; buvid_fp_plain=C7C61711-44C7-42D6-87A6-1A5A3136D97A167620infoc; SESSDATA=39eaebef%2C1645943730%2C3b217%2A81; bili_jct=09df693cc05df604fb8818b5425a99f5; DedeUserID=351541394; DedeUserID__ckMd5=8d5c63b55bd83763; sid=cee0jids; bp_video_offset_351541394=563592059627234389; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1630391761; Hm_lpvt_8a6e55dbd2870f0f5bc9194cddf32a02=1630391761',
            'referer': 'https://t.bilibili.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }
    result = []
    for mid in range(1,5000):
        try:
            print('正在爬取用户id号为:{}的用户信息'.format(mid))
            url = 'https://api.bilibili.com/x/space/acc/info?mid={}&jsonp=jsonp'.format(mid)
            url2 = 'https://api.bilibili.com/x/relation/stat?vmid={}&jsonp=jsonp'.format(mid)
            url3 = 'https://api.bilibili.com/x/space/upstat?mid={}&jsonp=jsonp'.format(mid)
            html1 = requests.get(url,headers = headers)
            html2 = requests.get(url2,headers = headers)
            html3 = requests.get(url3,headers = headers)
            user_name = html1.json()['data']['name']
            user_gender = html1.json()['data']['sex']
            user_photo_link = html1.json()['data']['face']
            user_level = html1.json()['data']['level']
            user_sign = html1.json()['data']['sign']
            user_title = html1.json()['data']['official']['title']
            user_fans_num = html2.json()['data']['follower']
            user_focu_num = html2.json()['data']['following']
            user_praise_num = html3.json()['data']['likes']
            user_play_amount = html3.json()['data']['archive']['view']
            data = [user_name,user_gender,user_level,user_fans_num,user_praise_num,
                    user_play_amount,user_focu_num,user_title,user_sign,user_photo_link]
            result.append(data)
        except:
            pass
    return result


def storage_data(result):
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(['用户名称', '性别', '等级', '粉丝数', '或赞数', '视频播放量', '关注数', '头衔', '个人简介', '头像链接'])
    for data in result:
        sheet.append(data)
    workbook.save('B站用户信息.xlsx')
if __name__ == '__main__':
    result = getUserInfo()
    storage_data(result)
    print('B站用户信息爬取并存储完成')
