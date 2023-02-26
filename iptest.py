from lxml import html
etree=html.etree
import requests
import os
import time
import pandas as pd
import re
from sqlalchemy import create_engine
import random

def run():
    ip_list=[]
    port_list=[]
    anynomous_degree_list=[]
    type_list=[]
    loc_list=[]
    speed_list=[]
    verify_time_list=[]
    proxy_format_list=[]

    url = 'https://www.kuaidaili.com/free/inha/{}/'
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70'}
    for i in range(1,10):
        response = requests.get(url=url.format(i), headers=header)
        html_page=etree.HTML(response.text)
        topic=html_page.xpath('.//div[@class="body"]//div[@id="content"]//table/thead/tr/th/text()')
        content=html_page.xpath('.//div[@class="body"]//div[@id="content"]//table/tbody/tr/td/text()')
        for j in range(len(content)):
            if j%8==0:
                ip_list.append(content[j])
            elif j%8==1:
                port_list.append(content[j])
            elif j%8 == 2:
                anynomous_degree_list.append(content[j])
            elif j % 8 == 3:
                type_list.append(content[j])
            elif j % 8 == 4:
                loc_list.append(content[j])
            elif j % 8 == 5:
                speed_list.append(content[j])
            elif j % 8 == 6:
                verify_time_list.append(content[j])
            else:
                pass
        time.sleep(1+random.randint(1,5)*0.1)
        for j in range(len(ip_list)):
            proxy_format_dict = {}
            proxy_format_dict[type_list[j]]=ip_list[j]+":"+port_list[j]
            # print(proxy_format_dict)
            proxy_format_list.append(proxy_format_dict)

        # print(proxy_format_list)
    return  proxy_format_list #使用的是list，不用存数据库，也不能直接存进数据库（dataframe需要字典），但可直接使用

def checkip(proxy_format_list,myurl):
    high_quality=[]
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70'}
    for li in proxy_format_list:
        try:
            response=requests.get(url=myurl,headers=header,proxies=li,timeout=0.2)
            if response.status_code==200:
                high_quality.append(li)
        except Exception as e:
            print(e)
    return high_quality




def getinfo():
    list=run()
    url='https://www.baidu.com/'
    usefulip=checkip(list,url)
    print(len(usefulip))
    print(usefulip)
    # df=pd.DataFrame(data=dict)
    # save2sql('ip',df)
    print('ok')
    pass


def save2disk(name,result):
    file = os.getcwd() + "/" + name + ".txt"
    output=open(file,'a',encoding='utf8')
    output.write(result)
    output.close()
    pass

def save2sql(name,df):
    connection = create_engine("mysql+pymysql://{}:{}@{}:{}/{}?charset={}".format('root', '123456', '127.0.0.1', '3306',
                                                                                  'test', 'utf8mb4'))
    df.to_sql(name, connection, if_exists='replace', index=False)

if __name__=="__main__":
    getinfo()

