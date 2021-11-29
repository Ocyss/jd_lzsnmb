# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author:qiu_lzsnmb
@file:京东试用批量全弃用.py
@time:2021/11/25
"""

import requests
from lxml import etree

# 网页ck
ck = ''

headers = {
    'cookie': ck,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'Referer': 'https://try.jd.com/user/myTrial?page=1&selected=2'
}

# for i in range(1, int(input("请输入要弃用到第几页：  ")) + 1):
for i in range(1, 4):
    url = f'https://try.jd.com/user/myTrial?page={i}&selected=2'
    req = requests.get(url, headers=headers)
    req_et = etree.HTML(req.text)
    evaluate_data = req_et.xpath('//*[@id="tab"]/div[3]/div/div/@activity_id')
    print(evaluate_data)
    for evaluate in evaluate_data:
        Zurl = f'https://try.jd.com/user/giveUpTry?activityId={evaluate}&reason=1%E3%80%81%20%E6%88%91%E7%8E%B0%E5%9C%A8%E4%B8%8D%E6%83%B3/%E6%97%A0%E6%B3%95%E8%AF%95%E7%94%A8%E8%BF%99%E6%AC%BE%E4%BA%A7%E5%93%81%EF%BC%9B'
        zreq = requests.get(Zurl, headers=headers)
        print(zreq.text)
