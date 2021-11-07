# -*- coding: utf-8 -*-
# @Time : 2021/10/23 17:39
import random
import time
import jieba.analyse
import requests
from lxml import etree

jieba.setLogLevel(jieba.logging.INFO)
ck = ''

headers = {
    'cookie': ck,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
}


# 评价生成
def generation(pname, _class=0, _type=1):
    # 0是追评 1是评价
    # class 0是评价 1是提取id
    try:
        name = jieba.analyse.textrank(pname, topK=5, allowPOS='n')[0]
    except:
        name = "宝贝"
    if _class == 1:
        return name
    else:
        datas = {
            1: {
                "开始": [
                    "考虑买这个$之前我是有担心过的，因为我不知道$的质量和品质怎么样，但是看了评论后我就放心了。",
                    "买这个$之前我是有看过好几家店，最后看到这家店的评价不错就决定在这家店买 ",
                    "看了好几家店，也对比了好几家店，最后发现还是这一家的$评价最好。",
                    "看来看去最后还是选择了这家。",
                    "之前在这家店也买过其他东西，感觉不错，这次又来啦。",
                    "这家的$的真是太好用了，用了第一次就还想再用一次。"
                ],
                "中间": [
                    "收到货后我非常的开心，因为$的质量和品质真的非常的好！",
                    "拆开包装后惊艳到我了，这就是我想要的$!",
                    "快递超快！包装的很好！！很喜欢！！！",
                    "包装的很精美！$的质量和品质非常不错！",
                    "收到快递后迫不及待的拆了包装。$我真的是非常喜欢",
                    "真是一次难忘的购物，这辈子没见过这么好用的东西！！"
                ],
                "结束": [
                    "经过了这次愉快的购物，我决定如果下次我还要买$的话，我一定会再来这家店买的。",
                    "不错不错！",
                    "我会推荐想买$的朋友也来这家店里买",
                    "真是一次愉快的购物！",
                    "大大的好评!以后买$再来你们店！(￣▽￣)",
                    "大家可以买来试一试，真的是太爽了，一晚上都沉浸在爽之中"
                ]
            },
            0: {
                "开始": [
                    "用了这么久的 $ ,东西是真的好用，真的难忘上一次购买时使用的激动，",
                    "使用了几天 $ ",
                    "这是我买到的最好用的$ ",
                    "我草，是真的好用啊，几天的体验下来，真是怀恋当初购买时下单的那一刻的激动!!!!!!!!!",
                    "我草，用了几天下来，$ 变得好大好大，这精致的外观，这细腻的皮肤，摸上去，真是令人激动！",
                    "$  这小家伙，真是太令人愉悦了，用了都说好好好好！",
                    "不用睡不着觉，这家店的 $ 真是太好用了。",
                    "真是牛逼啊，一天不用难受一天，用了一天难受一年！"
                ],
                "中间": [
                    "东西还行,",
                    "确实是好东西，推荐大家购买,",
                    "$  的质量真的非常不错！",
                    "$  真是太好用了，真是个宝贝，难忘的宝贝!!",
                    "$  短短几天的体验，令人一生难忘",
                    "$  用了这么久了，它长的真是太可爱了",
                    "这可真是个小宝贝！",
                    "五星好评，安排上，太好用拉！！！"
                ],
                "结束": [
                    "推荐大家来尝试",
                    "这家店给我对于$能做成这样刷新了世界观!",
                    "真是一次愉快的购物！",
                    "以后买$还来这家店，就没见过这么好用的东西！",
                    "下次还来这家店买 $ ，就没见过这么牛逼的东西",
                    "东西很好，孩子很喜欢",
                    "现在睡觉都抱着  $  睡觉，真是太好用了",
                    "令人难玩的一次购物"
                ]
            }
        }
        if _type == 1:
            # return 5, '东西很好，孩子很喜欢，每天晚上不抱着碎觉，就完全睡不着。买的时候看见评论里都说好就买了，看到发货的时候挺激动的，到了之后，满怀期待一激动得从快递员那里拿回了寝室，试一下，结果挺不错啊！而且客服小姐姐也特别的好，很有礼貌，客服小姐姐也是秒回我的疑问呢，嘻嘻，下次还会回购哒。'
            comments = datas[_type]
            return random.randint(3, 5), (
                    random.choice(comments["开始"]) + random.choice(comments["中间"]) + random.choice(
                comments["结束"])).replace(
                "$", name)
        elif _type == 0:
            comments = datas[_type]
            return (
                    random.choice(comments["开始"]) + random.choice(comments["中间"]) + random.choice(
                comments["结束"])).replace(
                "$", name)


# 查询全部评价
def all_evaluate():
    N = {}
    url = 'https://club.jd.com/myJdcomments/myJdcomment.action?'
    req = requests.get(url, headers=headers)
    req_et = etree.HTML(req.text)
    evaluate_data = req_et.xpath('//*[@id="main"]/div[2]/div[1]/div/ul/li')
    # print(evaluate)
    for i, ev in enumerate(evaluate_data):
        na = ev.xpath('a/text()')[0]
        try:
            num = ev.xpath('b/text()')[0]
        except IndexError:
            num = 0
        N[na] = int(num)
    return N


# 普通评价
def ordinary(N):
    Order_data = []
    req_et = []
    for i in range((N['待评价订单'] // 20) + 1):
        url = f'https://club.jd.com/myJdcomments/myJdcomment.action?sort=0&page={i + 1}'
        req = requests.get(url, headers=headers)
        req_et.append(etree.HTML(req.text))
    for i in req_et:
        Order_data.extend(i.xpath('//*[@id="main"]/div[2]/div[2]/table/tbody'))
    if len(Order_data) != N['服务评价']:
        Order_data = []
        for i in req_et:
            Order_data.extend(i.xpath('//*[@id="main"]/div[2]/div[2]/table'))

    print(f"当前共有{N['待评价订单']}个评价。")
    for i, Order in enumerate(Order_data):
        oid = Order.xpath('tr[@class="tr-th"]/td/span[3]/a/text()')[0]
        oname = Order.xpath('tr[@class="tr-bd"]/td[1]/div[1]/div[2]/div/a/text()')[0]
        pid = Order.xpath('tr[@class="tr-bd"]/td[1]/div[1]/div[2]/div/a/@href')[0]

        pid = pid.replace('//item.jd.com/', '').replace('.html', '')

        print(f"\t{i}.开始评价订单\t{oname}[{oid}]")
        url2 = f"https://club.jd.com/myJdcomments/saveProductComment.action"
        xing, Str = generation(oname)
        print(f'\t\t评价内容,星级{xing}：', Str)
        data2 = {
            'orderId': oid,
            'productId': pid,  # 商品id
            'score': str(xing),  # 商品几星
            'content': bytes(Str, encoding="gbk"),  # 评价内容
            'saveStatus': '1',
            'anonymousFlag': '1'
        }
        pj2 = requests.post(url2, headers=headers, data=data2)
        time.sleep(5)
        N['待评价订单'] -= 1
    return N


# 晒单评价
def sunbw(N):
    Order_data = []
    for i in range((N['待晒单'] // 20) + 1):
        url = f"https://club.jd.com/myJdcomments/myJdcomment.action?sort=1&page={i + 1}"
        req = requests.get(url, headers=headers)
        req_et = etree.HTML(req.text)
        Order_data.extend(req_et.xpath('//*[@id="evalu01"]/div[2]/div[1]/div[@class="comt-plist"]/div[1]'))
    print(f"当前共有{N['待晒单']}个需要晒单。")
    for i, Order in enumerate(Order_data):
        oname = Order.xpath('ul/li[1]/div/div[2]/div[1]/a/text()')[0]
        pid = Order.xpath('@pid')[0]
        oid = Order.xpath('@oid')[0]

        print(f'\t开始晒单{i},{oname}')
        # 获取图片
        pname = generation(pname=oname, _class=1)
        url1 = f"https://club.jd.com/discussion/getProductPageImageCommentList.action?productId={pid}"
        imgdata = requests.get(url1, headers=headers).json()
        if imgdata["imgComments"]["imgCommentCount"] == 0:
            url1 = "https://club.jd.com/discussion/getProductPageImageCommentList.action?productId=1190881"
            imgdata = requests.get(url1, headers=headers).json()
        imgurl = imgdata["imgComments"]["imgList"][0]["imageUrl"]

        #
        print(f'\t\t图片url={imgurl}')
        url2 = "https://club.jd.com/myJdcomments/saveShowOrder.action"  # 提交晒单
        headers['Referer'] = 'https://club.jd.com/myJdcomments/myJdcomment.action?sort=1'
        headers['Origin'] = 'https://club.jd.com'
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        data = {
            'orderId': oid,
            'productId': pid,
            'imgs': imgurl,
            'saveStatus': 3
        }
        req_url2 = requests.post(url2, data={
            'orderId': oid,
            'productId': pid,
            'imgs': imgurl,
            'saveStatus': 3
        }, headers=headers)
        # print(f'\t\t\t{req_url2.text}')
        print('完成')
        time.sleep(5)
        N['待晒单'] -= 1
    return N


# 追评
def review(N):
    req_et = []
    Order_data = []
    for i in range((N['待追评'] // 20) + 1):
        url = f"https://club.jd.com/myJdcomments/myJdcomment.action?sort=3&page={i + 1}"
        req = requests.get(url, headers=headers)
        req_et.append(etree.HTML(req.text))
    for i in req_et:
        Order_data.extend(i.xpath('//*[@id="main"]/div[2]/div[2]/table/tr[@class="tr-bd"]'))
    if len(Order_data) != N['待追评']:
        Order_data = []
        for i in req_et:
            Order_data.extend(i.xpath('//*[@id="main"]/div[2]/div[2]/table/tbody/tr[@class="tr-bd"]'))

    print(f"当前共有{N['待追评']}个需要追评。")
    for i, Order in enumerate(Order_data):
        oname = Order.xpath('td[1]/div/div[2]/div/a/text()')[0]
        _id = Order.xpath('td[3]/div/a/@href')[0]
        # date = Order.xpath('td[2]/div/text()')[0]
        print(f'\t开始第{i}，{oname}')
        url1 = "https://club.jd.com/afterComments/saveAfterCommentAndShowOrder.action"
        pid, oid = _id.replace('http://club.jd.com/afterComments/productPublish.action?sku=', "").split('&orderId=')
        context = generation(oname, _type=0)
        print(f'\t\t追评内容：{context}')
        req_url1 = requests.post(url1, headers=headers, data={
            'orderId': oid,
            'productId': pid,
            'content': bytes(context, encoding="gbk"),
            'anonymousFlag': 1,
            'score': 5
        })
        # print(f'\t\t\tr{req_url1.text}')
        print('完成')
        time.sleep(5)
        N['待追评'] -= 1
    return N


# 服务评价
def Service_rating(N):
    Order_data = []
    req_et = []
    for i in range((N['服务评价'] // 20) + 1):
        url = f"https://club.jd.com/myJdcomments/myJdcomment.action?sort=4&page={i + 1}"
        req = requests.get(url, headers=headers)
        req_et.append(etree.HTML(req.text))
    for i in req_et:
        Order_data.extend(i.xpath('//*[@id="main"]/div[2]/div[2]/table/tbody/tr[@class="tr-bd"]'))
    if len(Order_data) != N['服务评价']:
        Order_data = []
        for i in req_et:
            Order_data.extend(i.xpath('//*[@id="main"]/div[2]/div[2]/table/tr[@class="tr-bd"]'))
    print(f"当前共有{N['服务评价']}个需要服务评价。")
    for i, Order in enumerate(Order_data):
        oname = Order.xpath('td[1]/div[1]/div[2]/div/a/text()')[0]
        oid = Order.xpath('td[4]/div/a[1]/@oid')[0]
        print(f'\t开始第{i}，{oname}')
        url1 = f'https://club.jd.com/myJdcomments/insertRestSurvey.action?voteid=145&ruleid={oid}'
        data1 = {
            'oid': oid,
            'gid': '32',
            'sid': '186194',
            'stid': '0',
            'tags': '',
            'ro591': f'591A{random.randint(3, 5)}',  # 商品符合度
            'ro592': f'592A{random.randint(3, 5)}',  # 店家服务态度
            'ro593': f'593A{random.randint(3, 5)}',  # 快递配送速度
            'ro899': f'899A{random.randint(3, 5)}',  # 快递员服务
            'ro900': f'900A{random.randint(3, 5)}'  # 快递员服务
        }
        pj1 = requests.post(url1, headers=headers, data=data1)
        print("\t\t", pj1.text)
        time.sleep(5)
        N['服务评价'] -= 1
    return N


def No():
    print()
    N = all_evaluate()
    for i in N:
        print(i, N[i], end="----")
    print()
    return N


def main():
    print("开始京东批量评价！\n")
    N = No()
    if not N:
        print('Ck出现错误，请重新抓取！')
        exit()
    if N['待评价订单'] != 0:
        print("1.开始普通评价")
        N = ordinary(N)
        N = No()
    if N['待晒单'] != 0:
        print("2.开始晒单评价")
        N = sunbw(N)
        N = No()
    if N['待追评'] != 0:
        print("3.开始批量追评！")
        N = review(N)
        N = No()
    if N['服务评价'] != 0:
        print('4.开始服务评价')
        N = Service_rating(N)
        N = No()
    print("全部完成啦！")


if __name__ == '__main__':
    main()
