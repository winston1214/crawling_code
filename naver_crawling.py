import requests
import lxml.html
import pandas as pd
import re
import string
import bs4
from urllib.request import urlopen
import urllib
import time
keyword = input('검색어를 입력하시오 : ')
# df = pd.DataFrame(columns = ['title','abstract','url'])
word_encode = urllib.parse.quote(keyword)
df_list = []
idx = 0
start=1
while True:
    url='https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}&pd=1&start={}'.format(word_encode,start)
    source = urlopen(url).read() #url 열기
    source = bs4.BeautifulSoup(source,'html.parser')
    title_path =  source.find_all('a',{'class':'news_tit'})
    abstract_path = source.find_all('a',{'class':'api_txt_lines dsc_txt_wrap'})
    for i in range(len(title_path)):
        title = title_path[i].get('title')
#         print(title)
        abstract = abstract_path[i].text
        link = title_path[i].get('href')
        df = pd.DataFrame({'title':[title],'abstract':[abstract],'url':[link]})
        df_list.append(df)
#         df.loc[i,'title'] = title
#         df.loc[i,'abstract'] = abstract
#         df.loc[i,'url'] = link
#         df_list.append(df)
    current_page = source.find_all('a',{'aria-pressed':'true'})[0].text
    last_page = source.find_all('a',{'aria-pressed':'false'})[-1].text
    print(start)
    if int(current_page)>int(last_page):
        break
    else:
        start += 10
    time.sleep(0.5)
df_list = pd.concat(df_list)
df_list.to_excel('{}_result.xlsx'.format(keyword),index=False)
print('저장 완료되었습니다.')