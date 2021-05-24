import pandas as pd
import bs4
from urllib.request import urlopen
import urllib
import time
import tkinter as tk
from tkinter import messagebox
def naver(keyword):
    searching = '''{}'''.format(keyword)
    searching = searching.strip()
    word_encode = urllib.parse.quote(searching)
    df_list = []
    start=1
    while True:
        url='https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}&pd=1&start={}'.format(word_encode,start)
        source = urlopen(url).read() #url 열기
        source = bs4.BeautifulSoup(source,'html.parser')
        title_path =  source.find_all('a',{'class':'news_tit'})
        abstract_path = source.find_all('a',{'class':'api_txt_lines dsc_txt_wrap'})
        for i in range(len(title_path)):
            title = title_path[i].get('title')
            
            abstract = abstract_path[i].text
            link = title_path[i].get('href')
            df = pd.DataFrame({'title':[title],'abstract':[abstract],'url':[link]})
            df_list.append(df)
        current_page = source.find_all('a',{'aria-pressed':'true'})[0].text
        last_page = source.find_all('a',{'aria-pressed':'false'})[-1].text
        if int(current_page)>int(last_page):
            break
        else:
            start += 10
        time.sleep(0.5)
        print('크롤링 중')
    df_list = pd.concat(df_list)
    new_string = ''.join(filter(str.isalnum, searching))
    df_list.to_excel('naver_{}_result.xlsx'.format(new_string),index=False)
    root = tk.Tk()
    msg = messagebox.showinfo(title='Save msg',message='Save!')
    if msg == 'ok':
        root.destroy()

def google(keyword):
    searching = '''{}'''.format(keyword)
    searching = searching.strip()
    period = 'when:7d'
    word_encode = urllib.parse.quote(searching+period)
    base_url = 'https://news.google.com/'
    url = 'https://news.google.com/search?q={}&hl=ko&gl=KR&ceid=KR:ko'.format(word_encode)
    source = urlopen(url).read() #url 열기
    source = bs4.BeautifulSoup(source,'html.parser')
    df_list = []
    article_list = source.find_all('a',{'class':'DY5T1d RZIKme'})
    for i in range(len(article_list)):
        title = article_list[i].text
        link = base_url + article_list[i].get('href')[1:]
        df = pd.DataFrame({'title':[title],'url':[link]})
        df_list.append(df)
    google = pd.concat(df_list)
    new_string = ''.join(filter(str.isalnum, searching))
    google.to_excel('''google_{}_result.xlsx'''.format(new_string),index=False)
    root = tk.Tk()
    msg = messagebox.showinfo(title='Save msg',message='Save!')
    if msg == 'ok':
        root.destroy()