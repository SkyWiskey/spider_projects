import hashlib
import random
import time
import requests
import math
# 先查看JS参数
"""
        var t = n.md5(navigator.appVersion)
          , r = "" + (new Date).getTime()
          , i = r + parseInt(10 * Math.random(), 10);
        return {
            ts: r,
            bv: t,
            salt: i,
            sign: n.md5("fanyideskweb" + e + i + "Y2FYu%TNSbMCxc3t2u^XT")
"""

def getTranslate():
    data = {
        'i': keyword,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': salt,
        'sign': sign,
        'lts': ts,
        'bv': bv,
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME'
    }
    # 添加请求头
    headers = {
        'Cookie': 'OUTFOX_SEARCH_USER_ID=1061342857@10.108.160.105; OUTFOX_SEARCH_USER_ID_NCOO=2098070750.4471006; fanyi-ad-id=114757; fanyi-ad-closed=1; STUDY_SESS="O4zwUrtiA/TL4yYbPsKJfB/r5FB2E9HMPR/AOdcH+nt4tsTrBhIcdxoE+K9GBzIQdpKgo70jtMOsFkiTXB3AfBWRGj7N546V0XYmzX2/ResnmjSQDXhwaibZNk5C95ki9ElLPQ26NkG0Dhqs8qd9dzWpdUr6ZAZSwX6xn8dzEfMLhur2Nm2wEb9HcEikV+3FTI8+lZKyHhiycNQo+g+/oA=="; STUDY_INFO="yd.b7db370be1b44e5cb@163.com|8|1414802944|1630195937631"; DICT_SESS=v2|BZejhwGDk06zhLkGnfe40kfhHPK6LTuROfk4QynfkY0JuPLOMn4UERqynLq4nLYfRUW64qB0MzGRkWOfQukMkMRT4RHg4PLQF0; DICT_LOGIN=1||1630195937679; JSESSIONID=aaaVPilZDuGs3_zP5CpUx; ___rl__test__cookies=1630202958987',
        'Referer': 'https://fanyi.youdao.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }
    url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    html = requests.post(url,data = data,headers = headers)
    # 获取JSON数据
    result = html.json()['translateResult'][0][0]['tgt']
    print(f'”{keyword}”的翻译结果为:{result}')

if __name__ == '__main__':
    r = math.floor(time.time() * 1000)
    i = r + int(random.random() * 10)
    salt = i
    ts = r
    print('网易有道在线翻译(自动翻译)小工具👇')
    keyword = input('请输入想要翻译的词语>>>')
    sign = hashlib.md5(("fanyideskweb" + keyword + str(i) + "Y2FYu%TNSbMCxc3t2u^XT").encode('utf8')).hexdigest()
    bv = hashlib.md5("5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36".encode('utf8')).hexdigest()

    getTranslate()