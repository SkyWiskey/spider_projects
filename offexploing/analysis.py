from pyecharts.charts import WordCloud
import pyecharts.options as opts
import pandas as pd
import jieba
from tqdm import tqdm


data = pd.read_csv('guilin.csv')
data = data.dropna()
comments = data['comment']

contents = ''
for comment in comments:
    contents += comment +'\n'

filter_word = ['the','and','of','on','it','so','an','de','some','by','is'
               ,'to','The','It','og','as','om','be','af','that','we','We'
               ,'for','at','er','in','en','us','my','up','ja','et']

jieba_list = list(jieba.cut(contents))
series_Data = pd.Series(jieba_list)
keyword_counts = series_Data[series_Data.str.len() >= 2]
keyword_counts = keyword_counts[~series_Data.str.contains('|'.join(filter_word))]
keyword_counts = keyword_counts.value_counts()[:50]


wd = WordCloud(init_opts=opts.InitOpts(width='1080px',height='720px'))
wd.set_global_opts(
    title_opts=opts.TitleOpts(title = '桂林外国游客评论')
)
wd.add('',tuple(zip(keyword_counts.index.tolist(),keyword_counts.tolist()))
       ,word_size_range=[20,100],shape='circle')
wd.render('外国游客评论.html')
print('国外游客对桂林评价词云图已经生成')