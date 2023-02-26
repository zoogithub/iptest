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

    url = 'https://www.kuaidaili.com/free/inha/{}/'
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70'}
    for i in range(1,60):
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
                pass#付费方式不要了
        time.sleep(1+random.randint(1,5)*0.1)
    data_dict={
        topic[0]: ip_list,
        topic[1]: port_list,
        topic[2]: anynomous_degree_list,
        topic[3]: type_list,
        topic[4]: loc_list,
        topic[5]: speed_list,
        topic[6]: verify_time_list
    }
    return data_dict


def getinfo():
    dict=run()
    df=pd.DataFrame(data=dict)
    save2sql('ip',df)
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

