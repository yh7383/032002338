#本程序用于可视化处理
#在运行本程序之前应该先运行，get_url,get_data
#运行本程序，按照说明输入将可以得到某天全国疫情总体情况，某省有疫情以来感染人数所有情况
from operator import index
import  pandas as pd
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.commons.utils import JsCode
import urllib
import webbrowser
from time import strptime
from datetime import datetime
import pandas as pd  #pandas是强大的数据处理库
from pyecharts.charts import Map
from pyecharts import options as opts

#某天新增确症人数状况
def q_r(a):
    data = pd.read_excel("q_r.xlsx")
    province = list(data["省份"])#得到省份信息
    gdp = list(data[a+'\n'])#得到当天感染人数信息

    cc = [list(z) for z in zip(province,gdp)]
    c = (#生成地图
        Map(init_opts=opts.InitOpts(width="1000px", height="600px")) #可切换主题
        .set_global_opts(
            title_opts=opts.TitleOpts(title=a+"单位:人"),
            visualmap_opts=opts.VisualMapOpts(
                min_=0,
                max_=50,
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
#某天新增无症状感染者状况
def w_r(a):
    data = pd.read_excel("w_r.xlsx")
    province = list(data["省份"])#得到省份信息
    gdp = list(data[a+'\n'])#得到对应日期感染人数

    cc = [list(z) for z in zip(province,gdp)]
    c = (#生成地图
        Map(init_opts=opts.InitOpts(width="1000px", height="600px")) #可切换主题
        .set_global_opts(
            title_opts=opts.TitleOpts(title=a+"单位:人"),
            visualmap_opts=opts.VisualMapOpts(
                min_=0,
                max_=50,
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
#某省新增确症人数折线图
def q_s(a):
    data = pd.read_excel("q_s.xlsx",index_col=0)

    x_data = list(data.loc["省份"])#得到所有日期
    y_data = list(data.loc[a])#得到对应省份感染情况
    #生成折线图
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
#某省新增无症状感染者折线图
def w_s(a):
    data = pd.read_excel("w_s.xlsx",index_col=0)

    x_data = list(data.loc["省份"])#得到时间信息
    y_data = list(data.loc[a])#得到省份感染信息
    #生成折线图
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

def main():
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
    main()