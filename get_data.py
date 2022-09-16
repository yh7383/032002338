#!/usr/bin/python
# -*- coding: UTF-8 -*-
#本程序在get_url运行之后将所需要的url存进url_part
#运行本程序，将得到疫情的具体天数和省份的excel表
#运行本程序，将输出对应天数的热点状况
from asyncio.windows_events import NULL
from datetime import date
import webbrowser
import pandas as pd
import numpy as np
from dataclasses import dataclass
from lib2to3.pygram import pattern_symbols
from pydoc import source_synopsis
from this import d
from urllib import request
import re
from hashlib import md5
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import sys
import asyncio
from base64 import encode
from time import sleep
from turtle import ontimer
from pyppeteer import launch
from selenium import webdriver
a=1
b=1
#存储当天信息
exc1 = {'河北':0,'山西':0,'辽宁':0,'吉林':0,'黑龙江':0,'江苏':0,'浙江':0,'安徽':0,'福建':0,'江西':0,
         '山东':0,'河南':0,'湖北':0,'湖南':0,'广东':0,'海南':0,'四川':0,'贵州':0,'云南':0,
         '陕西':0,'甘肃':0,'青海':0,'台湾':0,'内蒙古':0,'广西':0,'西藏':0,'宁夏':0,'新疆':0,
         '北京':0,'天津':0,'上海':0,'重庆':0,'香港':0,'澳门':0}
exc2 = {'河北':0,'山西':0,'辽宁':0,'吉林':0,'黑龙江':0,'江苏':0,'浙江':0,'安徽':0,'福建':0,'江西':0,
         '山东':0,'河南':0,'湖北':0,'湖南':0,'广东':0,'海南':0,'四川':0,'贵州':0,'云南':0,
         '陕西':0,'甘肃':0,'青海':0,'台湾':0,'内蒙古':0,'广西':0,'西藏':0,'宁夏':0,'新疆':0,
         '北京':0,'天津':0,'上海':0,'重庆':0,'香港':0,'澳门':0}
#df1，df2作为总数据存储新增和无症状
df1 = pd.DataFrame(index=['河北','山西','辽宁','吉林','黑龙江','江苏','浙江','安徽','福建','江西',
         '山东','河南','湖北','湖南','广东','海南','四川','贵州','云南',
         '陕西','甘肃','青海','台湾','内蒙古','广西','西藏','宁夏','新疆',
         '北京','天津','上海','重庆','香港','澳门'])
df2 = pd.DataFrame(index=['河北','山西','辽宁','吉林','黑龙江','江苏','浙江','安徽','福建','江西',
         '山东','河南','湖北','湖南','广东','海南','四川','贵州','云南',
         '陕西','甘肃','青海','台湾','内蒙古','广西','西藏','宁夏','新疆',
         '北京','天津','上海','重庆','香港','澳门'])


def addnum3(data):
    for j in range(0,len(data)):
        if data[j]=='均':
            num=0
            for k in range(0,j):
                if data[k]>='0' and data[k]<='9':
                    num*=10
                    num+=int(data[k])
            for k in range(j+3,j+6):
                exc1[data[j+2:k]]=num
                
def addnum4(data):
    for j in range(0,len(data)):
        if data[j]=='均':
            num=0
            for k in range(0,j):
                if data[k]>='0' and data[k]<='9':
                    num*=10
                    num+=int(data[k])
            for k in range(j+3,j+6):
                exc1[data[j+2:k]]=num

def addnum1(data, i):
    num=0
    for j in range(i,len(data)):
        if('0' <= data[j] and data[j] <= '9'):
            num*=10
            num+=int(data[j])
        else:
            break
    for j in range(i-1,0,-1):
        # print(data[j])
        if data[j]=='，' or data[j]=='；' or data[j]=='\'' or data[j]=='（':
            exc1[data[j+1:i]]=num
            break

def addnum2(data, i):
    num=0
    for j in range(i,len(data)):
        if('0' <= data[j] and data[j] <= '9'):
            num*=10
            num+=int(data[j])
        else:
            break
    #print(num)
    for j in range(i-1,0,-1):
        if data[j]=='，' or data[j]=='；' or data[j]=='\'' or data[j]=='（':
            exc2[data[j+1:i]]=num
            break

def get_xin(list_name):
    for item in list_name:
        pattern = re.compile('新疆生产建设兵团报告新增确诊病例.*?本土病例(.*?)）') #pattern
        xx = pattern.findall(str(item.text))#正则匹配段落
        data = str(xx)
        for i in range(0,len(data)):
            if '1'<=data[i] and data[i]<='9' and not( '1'<=data[i-1] and data[i-1]<='9'):
                addnum1(data,i)#更新有疫情省份的情况
        addnum3(data)#更新只有一个省的情况

def get_wu(list_name):
    for item in list_name:
        pattern = re.compile('新疆生产建设兵团报告新增无症状感染者.*?本土(.*?)）') #pattern
        xx = pattern.findall(str(item.text))#正则匹配段落
        data = str(xx)
        for i in range(0,len(data)):
            if '1'<=data[i] and data[i]<='9' and not( '1'<=data[i-1] and data[i-1]<='9'):
                addnum2(data,i)#更新无症状感染者             
        addnum4(data)#更新只有一个省份有无症状感染的情况

def get_tai(list_name):
    for item in list_name:
        pattern = re.compile('.*?香港特别行政区(.*?)例.*?澳门特别行政区(.*?)例.*?台湾地区(.*?)例（') #pattern
        xx = pattern.findall(str(item.text))
        data = str(xx)#正则匹配段落
        j=1
        for i in range(1,len(data)):#扫描字符串
            if '0' <= data[i] and data[i] <= '9' and data[i-1] == '\'':#开头是数字
                num=0
                for k in range(i,len(data)):#得到数字
                    if '0' <= data[k] and data[k] <= '9':
                        num*=10
                        num+=int(data[k])
                    else:
                        break
                #更新相应数据
                if j==1:
                    exc1['香港']=num
                elif j==2:
                    exc1['澳门']=num
                else:
                    exc1['台湾']=num
                j+=1
                i=k

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

def get_html(options,webs,ii):
    while 1:
        browser = webdriver.Firefox(options=options)
        #声明模拟浏览器，并根据配置进行设置
        browser.get(webs[ii*2])#
        #输入网址，并访问页面（模拟浏览器打开）
        print(webs[ii*2])
        sleep(1)
        n_page_text = browser.page_source 
        #页面的html的element信息         
        soup = BeautifulSoup(n_page_text, 'html.parser')
        list_name = soup.select('.list > div')
        #通过BS4匹配想要的信息（段落的文本信息）
        print(len(list_name))
        if len(list_name)==0: #无信息则访问失败
            browser.quit()
            pass
        else: #有信息则访问成功
            browser.quit()
            break 
    return list_name

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
    options=webdriver.FirefoxOptions()
    options.add_argument('--headless')#无界面浏览
    options.add_argument('blink-settings=imagesEnabled=false')
    #配置浏览器设置
    f=open("url_part",'r')
    webs=f.readlines()
    for ii in range(0,int(len(webs)/2)):
        list_name=get_html(options,webs,ii) #得到html页面段落文本
        get_xin(list_name)#得到新增情况
        get_wu(list_name)#得到无症状情况
        get_tai(list_name)#得到港澳台情况
        store_data(webs,ii)#存储数据
    
if __name__ == '__main__':
    main()