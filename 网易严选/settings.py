import pymysql

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='12345',
    database='crawl_spider',
    charset='utf8'
)
