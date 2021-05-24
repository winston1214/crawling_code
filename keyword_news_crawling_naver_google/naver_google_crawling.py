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
    key_list= [searching]
    if '+' in searching:
        key_list = list(map(lambda x: ''.join(filter(str.isalnum, x)),searching.split('+')))
    while True:
        url='https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}&pd=1&start={}'.format(word_encode,start)
        source = urlopen(url).read() #url 열기
        source = bs4.BeautifulSoup(source,'html.parser')
        title_path =  source.find_all('a',{'class':'news_tit'})
        abstract_path = source.find_all('a',{'class':'api_txt_lines dsc_txt_wrap'})
        if len(title_path) == 0:
            root = tk.Tk()
            msg = messagebox.showerror(title = "No news",message = 'please search other keyword')
            if msg == 'ok':
                root.destroy()
                break
        for i in range(len(title_path)):
            title = title_path[i].get('title')
            for key in key_list:
                if key in title:
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
    if df_list: 
        df_list = pd.concat(df_list)
        new_string = ''.join(filter(str.isalnum, searching))
        df_list.to_excel('naver_{}_result.xlsx'.format(new_string),index=False)
        root2 = tk.Tk()
        msg = messagebox.showinfo(title='Save msg',message='Save!')
        if msg == 'ok':
            root2.destroy()

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
    if len(article_list) == 0:
        root = tk.Tk()
        msg = messagebox.showerror(title = "No news",message = 'please search other keyword')
        if msg == 'ok':
            root.destroy()
    else:
        key_list= [searching]
        if '+' in searching:
            key_list = list(map(lambda x: ''.join(filter(str.isalnum, x)),searching.split('+')))
        for i in range(len(article_list)):
            title = article_list[i].text
            for key in key_list:
                if key in title:
                    link = base_url + article_list[i].get('href')[1:]
                    df = pd.DataFrame({'title':[title],'url':[link]})
                    df_list.append(df)
        if df_list:
            google_df = pd.concat(df_list)
            new_string = ''.join(filter(str.isalnum, searching))
            google_df.to_excel('''google_{}_result.xlsx'''.format(new_string),index=False)
            root2 = tk.Tk()
            msg = messagebox.showinfo(title='Save msg',message='Save!')
            if msg == 'ok':
                root2.destroy()
