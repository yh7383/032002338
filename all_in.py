#本代码合成前三个代码
#运行本程序先生成需要访问的url
#然后访问对应的网站，生成并输出每日热点并且把疫情数据存入excel表中
#运行完这些之后可以根据提示选择想要的可视化图
from pydoc import source_synopsis
from urllib import request
import re
import random
from hashlib import md5
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from asyncio.windows_events import NULL
from datetime import date
import webbrowser
import numpy as np
from dataclasses import dataclass
from lib2to3.pygram import pattern_symbols
from pydoc import source_synopsis
from this import d
from urllib import request
import re
from hashlib import md5
import sys
import asyncio
from base64 import encode
from time import sleep
from turtle import ontimer
from pyppeteer import launch
from selenium import webdriver
from operator import index
from pyecharts.charts import Line
from pyecharts.commons.utils import JsCode
import webbrowser
from time import strptime
from datetime import datetime
import pandas as pd  #pandas是强大的数据处理库
from pyecharts.charts import Map
from pyecharts import options as opts
import cProfile

a=1
b=1
exc1 = {'河北':0,'山西':0,'辽宁':0,'吉林':0,'黑龙江':0,'江苏':0,'浙江':0,'安徽':0,'福建':0,'江西':0,
         '山东':0,'河南':0,'湖北':0,'湖南':0,'广东':0,'海南':0,'四川':0,'贵州':0,'云南':0,
         '陕西':0,'甘肃':0,'青海':0,'台湾':0,'内蒙古':0,'广西':0,'西藏':0,'宁夏':0,'新疆':0,
         '北京':0,'天津':0,'上海':0,'重庆':0,'香港':0,'澳门':0}
exc2 = {'河北':0,'山西':0,'辽宁':0,'吉林':0,'黑龙江':0,'江苏':0,'浙江':0,'安徽':0,'福建':0,'江西':0,
         '山东':0,'河南':0,'湖北':0,'湖南':0,'广东':0,'海南':0,'四川':0,'贵州':0,'云南':0,
         '陕西':0,'甘肃':0,'青海':0,'台湾':0,'内蒙古':0,'广西':0,'西藏':0,'宁夏':0,'新疆':0,
         '北京':0,'天津':0,'上海':0,'重庆':0,'香港':0,'澳门':0}
df1 = pd.DataFrame(index=['河北','山西','辽宁','吉林','黑龙江','江苏','浙江','安徽','福建','江西',
         '山东','河南','湖北','湖南','广东','海南','四川','贵州','云南',
         '陕西','甘肃','青海','台湾','内蒙古','广西','西藏','宁夏','新疆',
         '北京','天津','上海','重庆','香港','澳门'])
df2 = pd.DataFrame(index=['河北','山西','辽宁','吉林','黑龙江','江苏','浙江','安徽','福建','江西',
         '山东','河南','湖北','湖南','广东','海南','四川','贵州','云南',
         '陕西','甘肃','青海','台湾','内蒙古','广西','西藏','宁夏','新疆',
         '北京','天津','上海','重庆','香港','澳门'])
f=open('url_part','w', encoding='utf-8')
all_url = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd{}.shtml'

def addnum3(data):
    for j in range(0,len(data)):
        if data[j]=='均':
        #识别到“均”后开始搜索
            num=0
            for k in range(0,j):
            #向前搜索数字
                if data[k]>='0' and data[k]<='9':
                    num*=10
                    num+=int(data[k])
            for k in range(j+3,j+6):
            #向后搜索省份
                exc1[data[j+2:k]]=num                

def addnum4(data):
    #只有一个省份无症状感染者的特殊情况
    for j in range(0,len(data)):
        if data[j]=='均':
            num=0
            for k in range(0,j):
            #向前搜数字
                if data[k]>='0' and data[k]<='9':
                    num*=10
                    num+=int(data[k])
            for k in range(j+3,j+6):
            #向后搜省份
                exc1[data[j+2:k]]=num

def addnum1(data, i):
    num=0
    for j in range(i,len(data)):
        #向后扫描数字
        if('0' <= data[j] and data[j] <= '9'):
            num*=10
            num+=int(data[j])
        else:
            break
    for j in range(i-1,0,-1):
        #向前扫描省份
        if data[j]=='，' or data[j]=='；' or data[j]=='\'' or data[j]=='（':
            exc1[data[j+1:i]]=num
            #将数字加入对应的省份
            break

def addnum2(data, i):
    num=0
    for j in range(i,len(data)):
    #识别数字
        if('0' <= data[j] and data[j] <= '9'):
            num*=10
            num+=int(data[j])
        else:
            break
    for j in range(i-1,0,-1):
    #识别省份
        if data[j]=='，' or data[j]=='；' or data[j]=='\'' or data[j]=='（':
            exc2[data[j+1:i]]=num
            break

def get_xin(list_name):
    for item in list_name:
        pattern = re.compile('新疆生产建设兵团报告新增确诊病例.*?本土病例(.*?)）') #pattern
        xx = pattern.findall(str(item.text))
        #通过正则匹配整个文本信息
        data = str(xx) #转换成字符串格式
        for i in range(0,len(data)):
            if '1'<=data[i] and data[i]<='9' and not( '1'<=data[i-1] and data[i-1]<='9'):
                #识别到第一个数字
                addnum1(data,i)
                #通过第一个数字向前匹配省份
        addnum3(data) #均在同一个省份的情况

def get_wu(list_name):
    for item in list_name:
        pattern = re.compile('新疆生产建设兵团报告新增无症状感染者.*?本土(.*?)）') #pattern
        xx = pattern.findall(str(item.text))
        #用正则匹配到本土新增的省份文段
        data = str(xx)
        for i in range(0,len(data)):
            if '1'<=data[i] and data[i]<='9' and not( '1'<=data[i-1] and data[i-1]<='9'):
                addnum2(data,i)
                #锁定新增无症状感染者的省份和人数             
        addnum4(data) #在只有一个省份出现的特殊情况

def get_tai(list_name):
    for item in list_name:
        pattern = re.compile('.*?香港特别行政区(.*?)例.*?澳门特别行政区(.*?)例.*?台湾地区(.*?)例（') #pattern
        xx = pattern.findall(str(item.text))
        data = str(xx)
        #正则匹配到数字
        j=1
        for i in range(1,len(data)):#扫描字符串
            if '0' <= data[i] and data[i] <= '9' and data[i-1] == '\'':#开头是数字
                num=0
                #识别数字
                for k in range(i,len(data)):
                    if '0' <= data[k] and data[k] <= '9':
                        num*=10
                        num+=int(data[k])
                    else:
                        break
                #将数字加入到省份信息的dict
                if j==1:
                    exc1['香港']=num
                elif j==2:
                    exc1['澳门']=num
                else:
                    exc1['台湾']=num
                j+=1
                i=k

def get_html(webs,ii):
    while a==b:
        n_page_text=get_html1(webs[ii*2])        
        #得到html信息       
        soup = BeautifulSoup(n_page_text, 'html.parser')
        #通过html信息生成soup
        list_name = soup.select('.list > div')
        #div标签后所有文本信息
        print(len(list_name))
        if len(list_name)==0:
            pass
        else:
            break 
    return list_name

def hot(webs,ii):
    list_sheng=list(df1.index)
    print(webs[ii*2+1])#热点日期
    print("的热点：\n")
    for sheng in list_sheng:
        if df1[webs[ii*2+1]][sheng]!=0:#这天有疫情
            print(sheng)
            if df1[webs[ii*2+3]][sheng]==0:#前一天无疫情
                print('出现疫情\n')
            elif df1[webs[ii*2+3]][sheng]>=df1[webs[ii*2+1]][sheng]:#疫情增加
                print('疫情有所好转\n')
            else:#疫情减少
                print('疫情更加严重\n')
        else:#疫情结束
            if df1[webs[ii*2+3]][sheng]>0:
                print(sheng)
                print('疫情清零\n') 

def store_data(webs,ii):
    #更新当天情况
    print(ii*2+3)
    print(webs[ii*2+3])
    df1[webs[ii*2+3]]=pd.Series(exc1)
    df2[webs[ii*2+3]]=pd.Series(exc2)
    if ii-1>=0:#更新前一天的港澳台
        df1[webs[ii*2+1]]["台湾"]-=exc1["台湾"]
        df1[webs[ii*2+1]]["香港"]-=exc1["香港"]
        df1[webs[ii*2+1]]["澳门"]-=exc1["澳门"]
        hot(webs,ii)#输出热点
    #输出所有情况
    print(df1)
    print(df2)
    #查看当天热点
    for key1,key2 in zip(exc1,exc2):#重置
        exc1[key1]=0
        exc2[key2]=0   
    #存入excel
    writer = pd.ExcelWriter('1.xlsx')
    df1.to_excel(writer)
    writer.save()
    writer = pd.ExcelWriter('2.xlsx')
    df2.to_excel(writer)
    writer.save()

def main():
    f=open("url_part",'r')
    webs=f.readlines()
    for ii in range(0,int(len(webs)/2)):
        list_name=get_html(webs,ii) 
        get_xin(list_name)
        get_wu(list_name)
        get_tai(list_name)
        store_data(webs,ii)
           
def get_html1(url):
    headers =  {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27',
            'Referer' : 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml',
            'Cookie': 'yfx_c_g_u_id_10006654=_ck22091015454118598777723981237; sVoELocvxVW0S=5DSg3AJl0Eh2sJMRS0xBrJW.qk641GDuqy0w_08ci5Ki5RdtDaxR5X6SCxJU2lUT2JAIRrk5bgMicvJNmcncBLA; insert_cookie=91349450; _gscu_2059686908=62796040qrs9mc90; _gscbrs_2059686908=1; yfx_f_l_v_t_10006654=f_t_1662795941823__r_t_1662866266927__v_t_1662876292876__r_c_1; security_session_verify=ce983d3c2eeacced2208f3cd4fc9e426; sVoELocvxVW0T=53STdBCWwGhlqqqDkt0rQtG6hvNNyjExrIU3bZflvEnBgUiy0rpSXvPhIFquw.HpHkcLWwzYGQ6eEHopJXmPiqMH7P7nL09.CikMkdGvjHqdEVKzpKiFU60R530mcGomp82jqaQL3a.guQHYmHnb8EGk9nyNGpDJtpIqUlaBaWa4wQtfM3rt96HTunysuql4i5fPS4RFVke8_drqEBZUr9U8w4Ft1xHFp8bgYNqx9XEZOpYCBVMHCFEDNKT2fB88YtHP1XwYLY6rySFRX0sxoeyl3y8i5WhmKypGqBUkoSGuy.tTEACdvFM9IJQglti.iCaRYfu4_EvP28kJ69CTWulvhNH1OSwC6nG1zr6BzkvTG'
    }
    req = request.Request(url=url, headers=headers)
    html = request.urlopen(req).read().decode('utf-8')
    return html

def parse_html(one_url):
    # 调用请求函数，获取一级页面
    one_html = get_html1(one_url)#得到html格式的页面
    soup = BeautifulSoup(one_html,'html.parser')
    list_name = soup.select('.list > ul > li > a')
    list_date = soup.select('.list > ul > li > span')
    for item,date in zip(list_name,list_date):
        href = 'http://www.nhc.gov.cn/' + item['href']
        dat = date.text
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
        parse_html(url)

def q_r(a):
    province = list(df1.index)
    gdp = list(df1[a+'\n'])

    cc = [list(z) for z in zip(province,gdp)]
    c = (
        Map(init_opts=opts.InitOpts(width="1000px", height="600px")) #可切换主题
        .set_global_opts(
            title_opts=opts.TitleOpts(title=a+"单位:人"),
            visualmap_opts=opts.VisualMapOpts(
                min_=0,
                max_=100,
                range_text = ['确诊人数，颜色区间:', ''],  #分区间
                is_piecewise=True,  #定义图例为分段型，默认为连续的图例
                pos_top= "middle",  #分段位置
                pos_left="left",
                orient="vertical",
                split_number=10  #分成10个区间
            )
        )
        .add("GDP",cc,maptype="china")
        .render("Map2.html")
    )
    webbrowser.open_new_tab("Map2.html")

def w_r(a):
    province = list(df2.index)
    gdp = list(df2[a+'\n'])

    cc = [list(z) for z in zip(province,gdp)]
    c = (
        Map(init_opts=opts.InitOpts(width="1000px", height="600px")) #可切换主题
        .set_global_opts(
            title_opts=opts.TitleOpts(title=a+"单位:人"),
            visualmap_opts=opts.VisualMapOpts(
                min_=0,
                max_=100,
                range_text = ['确诊人数，颜色区间:', ''],  #分区间
                is_piecewise=True,  #定义图例为分段型，默认为连续的图例
                pos_top= "middle",  #分段位置
                pos_left="left",
                orient="vertical",
                split_number=10  #分成10个区间
            )
        )
        .add("GDP",cc,maptype="china")
        .render("Map2.html")
    )
    webbrowser.open_new_tab("Map2.html")

def q_s(a):
    x_data = list(df1.columns)
    y_data = list(df1.loc[a])

    background_color_js = (
        "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
        "[{offset: 0, color: '#c86589'}, {offset: 1, color: '#06a7ff'}], false)"
    )
    area_color_js = (
        "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
        "[{offset: 0, color: '#eb64fb'}, {offset: 1, color: '#3fbbff0d'}], false)"
    )

    c = (
        Line(init_opts=opts.InitOpts(bg_color=JsCode(background_color_js)))
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="注册总量",
            y_axis=y_data,
            is_smooth=True,
            is_symbol_show=True,
            symbol="circle",
            symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(color="#fff"),
            label_opts=opts.LabelOpts(is_show=True, position="top", color="white"),
            itemstyle_opts=opts.ItemStyleOpts(
                color="red", border_color="#fff", border_width=3
            ),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            areastyle_opts=opts.AreaStyleOpts(color=JsCode(area_color_js), opacity=1),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=a+"疫情情况",
                pos_bottom="5%",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(color="#fff", font_size=16),
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                boundary_gap=False,
                axislabel_opts=opts.LabelOpts(margin=30, color="#ffffff63"),
                axisline_opts=opts.AxisLineOpts(is_show=False),
                axistick_opts=opts.AxisTickOpts(
                    is_show=True,
                    length=25,
                    linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                position="right",
                axislabel_opts=opts.LabelOpts(margin=20, color="#ffffff63"),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=2, color="#fff")
                ),
                axistick_opts=opts.AxisTickOpts(
                    is_show=True,
                    length=15,
                    linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                ),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
        .render("line_color_with_js_func.html")
    )
    webbrowser.open_new_tab("line_color_with_js_func.html")

def w_s(a):
    x_data = list(df2.columns)
    y_data = list(df2.loc[a])

    background_color_js = (
        "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
        "[{offset: 0, color: '#c86589'}, {offset: 1, color: '#06a7ff'}], false)"
    )
    area_color_js = (
        "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
        "[{offset: 0, color: '#eb64fb'}, {offset: 1, color: '#3fbbff0d'}], false)"
    )

    c = (
        Line(init_opts=opts.InitOpts(bg_color=JsCode(background_color_js)))
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="注册总量",
            y_axis=y_data,
            is_smooth=True,
            is_symbol_show=True,
            symbol="circle",
            symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(color="#fff"),
            label_opts=opts.LabelOpts(is_show=True, position="top", color="white"),
            itemstyle_opts=opts.ItemStyleOpts(
                color="red", border_color="#fff", border_width=3
            ),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            areastyle_opts=opts.AreaStyleOpts(color=JsCode(area_color_js), opacity=1),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=a+"疫情情况",
                pos_bottom="5%",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(color="#fff", font_size=16),
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                boundary_gap=False,
                axislabel_opts=opts.LabelOpts(margin=30, color="#ffffff63"),
                axisline_opts=opts.AxisLineOpts(is_show=False),
                axistick_opts=opts.AxisTickOpts(
                    is_show=True,
                    length=25,
                    linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                position="right",
                axislabel_opts=opts.LabelOpts(margin=20, color="#ffffff63"),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=2, color="#fff")
                ),
                axistick_opts=opts.AxisTickOpts(
                    is_show=True,
                    length=15,
                    linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                ),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
        .render("line_color_with_js_func.html")
    )
    webbrowser.open_new_tab("line_color_with_js_func.html")

def main_2():
    while 1==1:
        print("你想要关于新增确症病例（1）还是无症状感染者的数据（2）？\n")
        a=input()
        if a=='1':
            print("你想要关于某天全国状况（1）还是某省的疫情变化（2）？\n")
            a=input()
            if a=='1':
                print("请输入日期：\n")
                a=input()
                q_r(a)
            else:
                print("请输入省份：\n")
                a=input()
                q_s(a)
        else:
            print("你想要关于某天全国状况（1）还是某省的疫情变化（2）？\n")
            a==input()
            if a=='1':
                print("请输入日期：\n")
                a=input()
                w_r(a)
            else:
                print("请输入省份：\n")
                a=input()
                w_s(a)
        print("如果想结束请输入：结束，否则继续：\n")
        a=input()
        if a=='结束':
            break
        else:
            pass

if __name__ == '__main__':
    run()
    cProfile.run('run()')
    # main()
    # main_2()