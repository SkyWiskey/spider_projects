import requests

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}
url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?'
data = {
    'on': 'true',
    'page': 1,
    'pageSize': 15,
    'conditionType': 1,
}
resp =requests.post(url,data=data).text
print(resp)