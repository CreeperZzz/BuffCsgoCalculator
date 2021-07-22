import json
import random
import sys
import time

from bs4 import BeautifulSoup
import requests


# 绿宝石 刺刀: https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id=42402&tag_ids=447129&page_num=1
# 略磨薄荷: https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id=43160&page_num=1
# 渐变蝴蝶: https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id=42556&page_num=1


def cal_ratio(price, fl, basefl, base):
    return float(price) / (base * (basefl/float(fl[:6])))


def cal_fade(price, fade, basefd, base):
    return float(price) / (base * (float(fade)/basefd))


def crawl(url: 'url', cookie, i):
    response = requests.get(
        url.format(i),
        cookies=cookie)
    d = json.loads(response.text)
    item_dict = d['data']['items']
    return [(i['price'], i['asset_info']['paintwear'], i['asset_info']['info']['metaphysic']['data']['name']) for i in item_dict]


if __name__ == '__main__':

    cookie_str = r'NTES_YD_PASSPORT=CeE4LD_rNrZXV_FuifnBFuho0VWSFCBHZhYga7Jelzh9Mmy6MT5QSOw5vNfM.dnlT6B7n3xTmvQSZ.GdTvAz.NYAJGwt2t8iJwMbGJoHlRxLVKkDGPyq1FSUXx2m0o0_Z3Cj__acqIGscJ7Li6HkksK35zUtlm29OxfTZHTnECv2V2e0Rla08fbB7kxKTFC.Ho3c0yzhR0PdXgmAw9Sjk7PRf; Device-Id=R6qyQm7k1al1xmaihrS7; Locale-Supported=zh-Hans; game=csgo; _ga=GA1.2.2141887760.1626846964; _gid=GA1.2.600373646.1626846964; NTES_YD_SESS=lJJEqxo0RtOfIq_wAHeQlENK_dngLO..N1obFxyGWWPHMmy6MT5QSOw5vNfM.dnlT6B7n3xTmvQr8n85Sn0nL6GJYp3tn3vX.gTgSboynjwIU96QDOPTnhWffhpLAg2BZl56eZL_WSenemcDTMKf_JCTcOV9tWvP46gEorGcsBoYap8N9js97WBdblYtroCVIfiP5Vn5Qz5x7R_dOz3oQPN1en2mq62E39hVLyPdKgswY; S_INFO=1626847002|0|3&80##|15802288113; P_INFO=15802288113|1626847002|1|netease_buff|00&99|null&null&null#fuj&350200#10#0|&0|null|15802288113; remember_me=U1094208324|vegmSQ38YCHiJUpTjxlebRl527CTulEN; session=1-wGm3T-GzT9ylKDZRvh9sAm6rW2sg_pGsfsjxWXemJHzI2046219292; csrf_token=IjM2ODc0YTdhYTJiZTdiN2Q5ZmU4NzEwNTBkN2EwNzE2N2FmOGI2YWQi.E9nAKg.3gfw8fPLqrqTGHAIabMQqhC6cf0'
    cookie = {i: j for i, j in [i.split('=', 1) for i in cookie_str.split(';')]}
    url = 'https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id=42556&page_num={}'

    pages = 1

    while True:
        time.sleep(1)
        try:
            response = requests.get(rf'https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id=42556&page_num={pages}',
                                    cookies=cookie)
            d = json.loads(response.text)
            print(f'page: {pages} reach')
        except json.decoder.JSONDecodeError:
            print(f'page: {pages} retry')
            continue
        p = int(d['data']['total_page'])
        if pages == p:
            break
        else:
            pages = p

    print(pages)
    price_list = []

    i = 1
    while i <= pages:
        time.sleep(1)
        try:
            price_list.extend(crawl(url, cookie, i))
            print(f'page:{i} loaded')
            i+=1
        except json.decoder.JSONDecodeError:
            print(f'page:{i} retry')
            continue


    base = float(price_list[int(len(price_list)/2)][0])

    # basefl = float(price_list[int(len(price_list)/2)][1][:6])
    # list = [(cal_ratio(i[0], i[1], basefl, base), i) for i in price_list]

    basefd = float(price_list[int(len(price_list)/2)][2][:-1])
    list = [(cal_fade(i[0], i[2][:-1], basefd, base), i) for i in price_list]

    list.sort(key = lambda i: i[0])
    for i in list:
        print(i)

