# !/usr/local/bin/python3
# -*- coding:utf-8 -*-
#***************************************#
# Author:        zilong.wu@aispeech.com
# Created:       2020-09-26 15:24:33
# Last modified: 2020-09-26 15:24:33
# Filename:      1.py
# Copyright      © Aispeech
#***************************************#
import os
import sys
import json
import pyecharts
from pyecharts.charts.basic_charts.bar import Bar
from pyecharts.charts.basic_charts.pie import Pie
from pyecharts.globals import ThemeType
from interval import Interval
from pyecharts.charts import Grid
from pyecharts.charts import Page
from pyecharts import options as opts
import pandas as pd
from collections import Counter

if __name__ == "__main__":
    file_name = sys.argv[1]
    df = pd.read_excel(file_name)
    companies = df['单位名称'].tolist()
    comp_counter = Counter(companies).most_common(10)
    cc = dict(comp_counter)
    areas = df['所属区域'].tolist()
    area_counter = Counter(areas).most_common()
    dd = dict(area_counter)
    scores = df['总得分'].tolist()
    score_counter = Counter(scores).most_common()
    step_range = [{'<75分':[0,75]}, {'>=75分,<80分':[75,80]},{'>=80分,<85分': [80,85]},{'>=85分,<90分': [85,90]},{'>=90分,<95分': [90,95]},{'>=95分,<100分':[95,100]}]
    score_range = {k: sum(i[1] for i in score_counter if not isinstance(i[0], str) and i[0] < j[1] and i[0] >= j[0]) for kv in step_range for k, j in kv.items()}
    page = Page()
    bar_company = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(list(cc.keys()))
        .add_yaxis("人数", list(cc.values()))
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title = "紧缺人才名单公司分布柱状图", 
                subtitle = "company", 
            )
        )
    )
    page.add(bar_company)
    pie_company = (
        Pie()
        .add("", comp_counter)
        .set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])
        .set_global_opts(title_opts=opts.TitleOpts(
            title="紧缺人才名单公司分布饼图",
            ),
            legend_opts = opts.LegendOpts(
                pos_top = "bottom"
            )
        )
        .set_series_opts(label_opts=opts.LabelOpts(
            formatter="{b}: {c} ({d}%)"))
    )
    page.add(pie_company)

    bar_area = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(list(dd.keys()))
        .add_yaxis("人数", list(dd.values()))
        .set_global_opts(
            title_opts= opts.TitleOpts(
                title = "紧缺人才名单区域分布柱状图", 
                subtitle = "area",
            )
        )
    )
    page.add(bar_area)

    pie_area = (
        Pie()
        .add("", area_counter)
        .set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])
        .set_global_opts(title_opts=opts.TitleOpts(
            title="紧缺人才名单区域分布饼图"
            ),
            legend_opts = opts.LegendOpts(
                #pos_top = "2%",
                pos_top = "bottom"
            )
        )
        .set_series_opts(label_opts=opts.LabelOpts(
            formatter="{b}: {c} ({d}%)"
            )
        )
        #.render("pie_set_color.html")
    )
    page.add(pie_area)
    bar_score = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(list(score_range.keys()))
        .add_yaxis("紧缺人才分数分布区间人数", list(score_range.values()))
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title = "紧缺人才名单分数分布柱状图", 
                subtitle = "score", 
                #pos_bottom = "60%"
            )
        )
    )
    page.add(bar_score)
    pie_score = (
        Pie()
        .add("", list(zip(score_range.keys(), score_range.values())))
        .set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])
        .set_global_opts(title_opts=opts.TitleOpts(
            title="紧缺人才分数分布饼图",
            ),
            legend_opts = opts.LegendOpts(
                pos_top = "bottom"
            )
        )
        .set_series_opts(label_opts=opts.LabelOpts(
            formatter="{b}: {c} ({d}%)"))
    )
    page.add(pie_score)
    page.render('Qp.html')

