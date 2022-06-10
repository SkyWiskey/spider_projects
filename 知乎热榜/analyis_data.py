import pymysql
from pyecharts.charts import WordCloud
import pyecharts.options as opts
import pandas as pd
import jieba
from tqdm import tqdm

conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='123456',
            database='crawl_spider',
            charset='utf8'
        )
cursor = conn.cursor()
sql = 'select * from zhihu;'
cursor.execute(sql)

titles = cursor.fetchall()
contents = ''
for title in titles:
    t = title[1]
    contents += t +'\n'

jieba_list = list(jieba.cut(contents))
series_Data = pd.Series(jieba_list)
keyword_counts = series_Data[series_Data.str.len() >= 2]
keyword_counts = keyword_counts.value_counts()[:50]

wd = WordCloud(init_opts=opts.InitOpts(width='1080px',height='720px'))
wd.set_global_opts(
    title_opts=opts.TitleOpts(title = '知乎热榜标题分析')
)
wd.add('',tuple(zip(keyword_counts.index.tolist(),keyword_counts.tolist()))
       ,word_size_range=[20,100],shape='diamond'
)
for i in tqdm(range(int(10e6)),ncols=88,desc='词云图生成中...'):
    pass
wd.render('知乎热榜标题.html')