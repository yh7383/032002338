#本程序爬取卫健委每日疫情通报的url和日期
#数据用url_part文件存储
from pydoc import source_synopsis
from urllib import request
import re
import time
import random
from hashlib import md5
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import sys
import cProfile
f=open('url_part','w', encoding='utf-8')

all_url = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd{}.shtml'
        

def get_html1(url): #获得每个页面的html
    headers =  {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27',
            'Referer' : 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml',
            'Cookie': 'yfx_c_g_u_id_10006654=_ck22091015454118598777723981237; sVoELocvxVW0S=5DSg3AJl0Eh2sJMRS0xBrJW.qk641GDuqy0w_08ci5Ki5RdtDaxR5X6SCxJU2lUT2JAIRrk5bgMicvJNmcncBLA; insert_cookie=91349450; _gscu_2059686908=62796040qrs9mc90; _gscbrs_2059686908=1; yfx_f_l_v_t_10006654=f_t_1662795941823__r_t_1662866266927__v_t_1662876292876__r_c_1; security_session_verify=ce983d3c2eeacced2208f3cd4fc9e426; sVoELocvxVW0T=53STdBCWwGhlqqqDkt0rQtG6hvNNyjExrIU3bZflvEnBgUiy0rpSXvPhIFquw.HpHkcLWwzYGQ6eEHopJXmPiqMH7P7nL09.CikMkdGvjHqdEVKzpKiFU60R530mcGomp82jqaQL3a.guQHYmHnb8EGk9nyNGpDJtpIqUlaBaWa4wQtfM3rt96HTunysuql4i5fPS4RFVke8_drqEBZUr9U8w4Ft1xHFp8bgYNqx9XEZOpYCBVMHCFEDNKT2fB88YtHP1XwYLY6rySFRX0sxoeyl3y8i5WhmKypGqBUkoSGuy.tTEACdvFM9IJQglti.iCaRYfu4_EvP28kJ69CTWulvhNH1OSwC6nG1zr6BzkvTG'
        }
    req = request.Request(url=url, headers=headers)#发送访问请求
    html = request.urlopen(req).read().decode('utf-8')#得到html页面element，并设置编码方式
    return html

def parse_html(one_url):#
    one_html = get_html1(one_url)#得到html格式的页面
    soup = BeautifulSoup(one_html,'html.parser')#生成beautiful soup解析对象
    list_name = soup.select('.list > ul > li > a')#寻找每日通报的url
    list_date = soup.select('.list > ul > li > span')#寻找每日通报的日期
    for item,date in zip(list_name,list_date):
        href = 'http://www.nhc.gov.cn/' + item['href']#组成url
        dat = date.text#获得日期
        #存入数据
        f.write(href)
        f.write('\n')
        f.write(dat)
        f.write('\n')
        

def run():
    for i in range(1,42):
        if i==1:
            url = all_url.format('')
        else:
            url = all_url.format('_'+str(i))
        parse_html(url)#搜索每一个页面


if __name__ == '__main__':
    run()
    