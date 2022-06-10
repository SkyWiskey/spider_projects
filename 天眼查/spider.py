import time,re

import pymysql
import requests
from lxml import etree
import pandas as pd


headers = {
        'Cookie': 'aliyungf_tc=8088a4047b963fc4324f3cac31028f63cb945f5ba0a43f4146ea7cbc30a36924; acw_tc=781bad3a16427633488912337e481b3cfcbc45b8f8b82fa99b2264b292c3bd; csrfToken=EL8M1-qxlWvuuPYFtTCIlqau; jsid=SEO-BAIDU-ALL-SY-000001; TYCID=8e1fcb007aaa11ec96bb2b0b6a60f35a; ssuid=2529432534; sajssdk_2015_cross_new_user=1; bannerFlag=true; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1642763351; show_activity_id_27=27; _ga=GA1.2.45712755.1642763352; _gid=GA1.2.156905286.1642763352; searchSessionId=1642763379.16030725; relatedHumanSearchGraphId=23402373; relatedHumanSearchGraphId.sig=xQxyUIDqVdMkulWk5m_htP28Pzw8_eM8tUMIyK4_qqs; refresh_page=0; CT_TYCID=f9228d08f6d549e18e9d21ec04591246; creditGuide=1; RTYCID=2ecba6e6aba846fba81183ac02cddeaa; bannerHide=notlogin; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217e7c53724665e-03a4abc1f3d6e8-f791b31-1327104-17e7c5372472ad%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2217e7c53724665e-03a4abc1f3d6e8-f791b31-1327104-17e7c5372472ad%22%7D; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1642763530; cloud_token=0600d54fbc894f8da52d3054a35afda9; cloud_utm=0c4a66ba654c4cdcb58fcba5ac25fd68',
        'Referer': 'https://www.tianyancha.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}

def get_company_id(company_name):
    """拿到company_id"""
    url = f'https://www.tianyancha.com/search?key={company_name}'
    resp = requests.get(url,headers=headers).text
    href = re.findall(r'https://www.tianyancha.com/company/(\d+)',resp)
    company_id = href[0]
    return company_id

def get_html(company_id):
    """请求网页 获取相应"""
    url = f'https://www.tianyancha.com/company/{company_id}'
    html = requests.get(url,headers=headers)
    h_text = html.text
    return h_text

def parse_h_text(company_name,company_id,h_text):
    """分析网页 提取数据"""
    html = etree.HTML(h_text)
    tr_list = html.xpath("//table[@class='table -striped-col -breakall']/tbody/tr")
    info_key_list = [
        ['法定代表人','经营状态','天眼评分'],['成立日期'],['注册资本'],
        ['实缴资本','工商注册号'],['统一社会信用代码','纳税人识别号','组织机构代码'],
        ['营业期限','纳税人资质','核准日期'],['企业类型','行业','人员规模'],
        ['参保人数','登记机关'],['曾用名','英文名称'],['注册地址'],['经营范围']
    ]
    company_item = dict(company_name = company_name,company_id = company_id)
    for index,tr in enumerate(tr_list):
        if index == 0 or index == 4 or index ==5 or index ==6:
            """当一行tr有三个td标签时"""
            company_item[info_key_list[index][0]] = re.sub(r'\s','',''.join(
                tr.xpath(".//td[2]//text()")).strip())
            company_item[info_key_list[index][1]] = re.sub(r'\s','',''.join(
                tr.xpath(".//td[4]//text()")).strip())
            company_item[info_key_list[index][2]] = re.sub(r'\s','',''.join(
                tr.xpath(".//td[6]//text()")).strip())
        if index == 3 or index == 7 or index == 8:
            """当一行tr有两个td标签时"""
            company_item[info_key_list[index][0]] = re.sub(r'\s','',''.join(
                tr.xpath(".//td[2]//text()")).strip())
            company_item[info_key_list[index][1]] = re.sub(r'\s','',''.join(
                tr.xpath(".//td[4]//text()")).strip())
        else:
            """当一行tr仅有一个个td标签时"""
            company_item[info_key_list[index][0]] = re.sub(r'\s','',''.join(
                tr.xpath(".//td[2]//text()")).strip())
    company_item['天眼评分'] = company_item['天眼评分'].split('+')[0].split('评分')[-1][:2]
    company_item['法定代表人'] = company_item['法定代表人'].split('任职')[0][1:]
    return company_item

def save_csv(item_list):
    """写入csv文件"""
    df = pd.DataFrame(item_list)
    df.to_csv('tianyancha_company_info.csv',encoding='utf8')

def save_to_mysql(item_list):
    """写入到MySQL数据库中"""
    conn = pymysql.Connect(
        host='localhost',port=3306,user='root',password='123456',database='crawl_spider',charset='utf8'
    )
    cursor = conn.cursor()
    try:
        for item in item_list:
            sql = """insert into tianyancha(company_name,company_id,master,status,score) values
                        (%s,%s,%s,%s,%s) """
            cursor.execute(sql,(item['company_name'],item['company_id'],
                                item['法定代表人'],item['经营状态'],item['天眼评分']))
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    company_item_list = list()
    company_name_list = ['上海江湾化工装备有限公司','上海利民电镀厂','河南省帝鑫企业管理咨询有限公司']
    while len(company_name_list) > 0:
        """错误自动处理"""
        company_name = company_name_list.pop()
        try:
            company_id = get_company_id(company_name)
            h_text = get_html(company_id)
            company_item = parse_h_text(company_name,company_id,h_text)
            company_item_list.append(company_item)
        except:
            company_name_list.append(company_name)
        # time.sleep(1)
    save_csv(company_item_list)
    # save_to_mysql(company_item_list)


    # for company_name in company_name_list:
    #     print(f'正在爬取-{company_name}-公司信息')
    #     company_id = get_company_id(company_name)
    #     h_text = get_html(company_id)
    #     company_item = parse_h_text(company_name,company_id,h_text)
    #     company_item_list.append(company_item)
    #     time.sleep(2)
    # save_csv(company_item_list)

### 问题1：company_id需要单独获取 否则可能会影响后面程序的运行
### 问题2：实现程序自动错误处理
### 问题3：如果突然停电怎，怎么办  -- 断点续爬
### 问题4：数据存储在数据库里面(MongoDb)