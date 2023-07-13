import json
from tqdm import tqdm
from selenium.webdriver import Chrome
from selenium import webdriver
import time
import argparse

def crawler(args):
    data_dir = args.data_dir
    data_dir = 'HealthCareMagic-100k.json'
    with open(data_dir,'r') as f:
        data = json.load(f)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized"); # 시작할때 최대창을 띄워라
    browser = webdriver.Chrome('chromedriver', options=options)
    output_ls = []
    start = args.start_num
    end = args.end_num
    for idx,i in tqdm(enumerate(data[start:end])):
        output_dic = {}
        inst = i['instruction']
        browser.get(f'https://www.deepl.com/translator#en/ko/{inst}') # 사이트 접속
        if idx == 0:
            time.sleep(10)
        else:
            time.sleep(3)
        browser.implicitly_wait(3) # 묵시적으로 5초동안 대기해라(쪼매 줄여도 됨)
        inst_text = browser.find_element_by_xpath('//*[@id="panelTranslateText"]/div[1]/div[2]/section[2]/div[3]/div[1]/d-textarea/div/p').text
        output_dic['instruction'] = inst_text
  
        input_sentence = i['input']
        browser.get(f'https://www.deepl.com/translator#en/ko/{input_sentence}') # 사이트 접속
        time.sleep(3)
        browser.implicitly_wait(3) # 묵시적으로 5초동안 대기해라(쪼매 줄여도 됨)
        text = browser.find_element_by_xpath('//*[@id="panelTranslateText"]/div[1]/div[2]/section[2]/div[3]/div[1]/d-textarea/div/p').text
        output_dic['input'] = text
  
        output_sentence = i['output']
        browser.get(f'https://www.deepl.com/translator#en/ko/{output_sentence}') # 사이트 접속
        time.sleep(3)
        browser.implicitly_wait(3) # 묵시적으로 5초동안 대기해라(쪼매 줄여도 됨)
        text = browser.find_element_by_xpath('//*[@id="panelTranslateText"]/div[1]/div[2]/section[2]/div[3]/div[1]/d-textarea/div/p').text
        output_dic['output'] = text
        output_ls.append(output_dic)
    browser.quit()
  
    with open(f'korean_translation_data/HealthCareMagic-100k_{start}_{end}.json','wt',encoding='utf-8') as f:
        json.dump(output_ls,f,ensure_ascii=False)
      
    print(f'Save {start}-{end}')
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir',help='json file path')
    parser.add_argument('--start_num',help='start_index')
    parser.add_argument('--end_num',help='end_index')
​
    args = parser.parse_args()
    cralwer(args)
