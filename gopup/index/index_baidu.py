#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 0021
# @Author  : justin.郑 3907721@qq.com
# @File    : index_baidu.py
# @Desc    : 获取百度指数

import time
import json
import logging

import pandas as pd
import requests
from gopup.utils.proxy import ProxyClient


def decrypt(t: str, e: str) -> str:
    """
    解密函数
    :param t:
    :type t:
    :param e:
    :type e:
    :return:
    :rtype:
    """
    n, i, a, result = list(t), list(e), {}, []
    ln = int(len(n) / 2)
    start, end = n[ln:], n[:ln]
    a = dict(zip(end, start))
    return "".join([a[j] for j in e])


def get_ptbk(uniqid: str, cookie: str, proxies: ProxyClient = None, retries=3) -> str:
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "index.baidu.com",
        "Referer": "http://index.baidu.com/v2/main/index.html",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    session = requests.Session()
    session.headers.update(headers)
    session.proxies = proxies.to_dict() if proxies else None
    for _ in range(retries):
        try:
            resp = session.get(url=f"http://index.baidu.com/Interface/ptbk?uniqid={uniqid}")
            json_data = resp.json()
            logging.info(json_data)
            ptbk = json_data["data"]
            return ptbk
        except Exception as e:
            logging.error(e)
            time.sleep(5)
    else:
        raise Exception('failed to get ptbk')


def baidu_interest_index(word, cookie, proxies: ProxyClient = None):
    """
    百度指数 人群画像兴趣分布
    :param word: 关键词
    :param cookie:
    :param proxies: 代理
    :return:
        desc    兴趣分类
        tgi     TGI指数
        word_rate   关键词分布比率
        all_rate    全网分布比率
        period      周期范围
    """
    try:
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Cookie": cookie,
            "DNT": "1",
            "Host": "zhishu.baidu.com",
            "Pragma": "no-cache",
            "Proxy-Connection": "keep-alive",
            "Referer": "zhishu.baidu.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        url = "http://index.baidu.com/api/SocialApi/interest?wordlist[]=%s" % word
        r = requests.get(url=url, headers=headers, proxies=proxies.to_dict() if proxies else None)
        logging.info(r.text)
        data = json.loads(r.text)['data']
        period = "%s|%s" % (data['startDate'], data['endDate'])

        age_list = data['result'][0]['interest']
        age_df = pd.DataFrame(age_list)

        all_list = data['result'][1]['interest']
        all_df = pd.DataFrame(all_list)
        all_df.drop(["tgi", "typeId"], axis=1, inplace=True)

        res_df = pd.merge(age_df, all_df, on='desc')
        res_df['period'] = period
        res_df.drop(["typeId"], axis=1, inplace=True)
        res_df.rename(columns={'rate_x': 'word_rate', 'rate_y': 'all_rate'}, inplace=True)
        return res_df
    except Exception as e:
        logging.error(e)
        return None


def baidu_gender_index(word, cookie, proxies: ProxyClient = None):
    """
    百度指数 人群画像性别分布
    :param word: 关键词
    :param cookie:
    :param proxies: 代理
    :return:
        desc    性别
        tgi     TGI指数
        word_rate   关键词分布比率
        all_rate    全网分布比率
        period      周期范围
    """
    try:
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Cookie": cookie,
            "DNT": "1",
            "Host": "zhishu.baidu.com",
            "Pragma": "no-cache",
            "Proxy-Connection": "keep-alive",
            "Referer": "zhishu.baidu.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        url = "http://index.baidu.com/api/SocialApi/baseAttributes?wordlist[]=%s" % word
        r = requests.get(url=url, headers=headers, proxies=proxies.to_dict() if proxies else None)
        logging.info(r.json())
        data = json.loads(r.text)['data']
        period = "%s|%s" % (data['startDate'], data['endDate'])

        age_list = data['result'][0]['gender']
        age_df = pd.DataFrame(age_list)

        all_list = data['result'][1]['gender']
        all_df = pd.DataFrame(all_list)
        all_df.drop(["tgi", "typeId"], axis=1, inplace=True)

        res_df = pd.merge(age_df, all_df, on='desc')
        res_df['period'] = period
        res_df.drop(["typeId"], axis=1, inplace=True)
        res_df.rename(columns={'rate_x': 'word_rate', 'rate_y': 'all_rate'}, inplace=True)
        return res_df
    except Exception as e:
        logging.error(e)
        return None


def baidu_age_index(word, cookie, proxies: ProxyClient = None):
    """
    百度指数 人群画像年龄分布
    :param word: 关键词
    :param cookie:
    :param proxies: 代理
    :return:
        desc    年龄范围
        tgi     TGI指数
        word_rate   关键词分布比率
        all_rate    全网分布比率
        period      周期范围
    """
    try:
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Cookie": cookie,
            "DNT": "1",
            "Host": "zhishu.baidu.com",
            "Pragma": "no-cache",
            "Proxy-Connection": "keep-alive",
            "Referer": "zhishu.baidu.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        url = "http://index.baidu.com/api/SocialApi/baseAttributes?wordlist[]=%s" % word
        r = requests.get(url=url, headers=headers, proxies=proxies.to_dict() if proxies else None)
        logging.info(r.json())
        data = json.loads(r.text)['data']
        period = "%s|%s" % (data['startDate'], data['endDate'])

        age_list = data['result'][0]['age']
        age_df = pd.DataFrame(age_list)

        all_list = data['result'][1]['age']
        all_df = pd.DataFrame(all_list)
        all_df.drop(["tgi", "typeId"], axis=1, inplace=True)

        res_df = pd.merge(age_df, all_df, on='desc')
        res_df['period'] = period
        res_df.drop(["typeId"], axis=1, inplace=True)
        res_df.rename(columns={'rate_x': 'word_rate', 'rate_y': 'all_rate'}, inplace=True)
        return res_df
    except Exception as e:
        logging.error(e)
        return None


def baidu_atlas_index(word, cookie, date=None, proxies: ProxyClient = None):
    """
    百度指数 需求图谱
    :param word: 关键词
    :param cookie:
    :param date: 周期
    :param proxies: 代理
    :return:
        period  周期范围
        word    相关词
        pv      搜索热度
        ratio   搜索变化率
    """

    try:
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Cookie": cookie,
            "DNT": "1",
            "Host": "zhishu.baidu.com",
            "Pragma": "no-cache",
            "Proxy-Connection": "keep-alive",
            "Referer": "zhishu.baidu.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        if date == None:
            date = ""
        url = "http://index.baidu.com/api/WordGraph/multi?wordlist[]=%s&datelist=%s" % (word, date)
        r = requests.get(url=url, headers=headers, proxies=proxies.to_dict() if proxies else None)
        logging.info(r.json())
        data = json.loads(r.text)['data']
        wordlist = data['wordlist'][0]['wordGraph']
        res_list = []
        for word in wordlist:
            tmp = {
                "word": word['word'],
                "pv": word['pv'],
                "ratio": word['ratio'],
                "period": data['period']
                # "sim": word['sim']
            }
            res_list.append(tmp)
        df = pd.DataFrame(res_list)
        return df
    except Exception as e:
        logging.error(e)
        return None


def baidu_search_index(word, start_date, end_date, cookie, type="all", proxies: ProxyClient = None):
    """百度搜索数据
    start_date: 日期格式 2021-11-15
    type: 1. all: PC+移动 2. pc: PC 3. wise: 移动
    """
    try:
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Cookie": cookie,
            "Host": "index.baidu.com",
            "Referer": "http://index.baidu.com/v2/main/index.html",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        }
        w = '{"name":"%s","wordType":1}' % word

        url = 'http://index.baidu.com/api/SearchApi/index?area=0&word=[[%s]]&startDate=%s&endDate=%s' % (
            w,
            start_date,
            end_date,
        )

        r = requests.get(url=url, headers=headers, proxies=proxies.to_dict() if proxies else None)
        logging.info(r.json())
        data = r.json()["data"]
        all_data = data["userIndexes"][0][type]["data"]
        uniqid = data["uniqid"]
        ptbk = get_ptbk(uniqid, cookie)
        result = decrypt(ptbk, all_data).split(",")
        result = [int(item) if item != "" else 0 for item in result]
        temp_df_7 = pd.DataFrame(
            [pd.date_range(start=start_date, end=end_date), result],
            index=["date", word],
        ).T
        temp_df_7.index = pd.to_datetime(temp_df_7["date"])
        del temp_df_7["date"]
        return temp_df_7
    except Exception as e:
        logging.error(e)
        return None


def baidu_info_index(word, start_date, end_date, cookie, proxies: ProxyClient = None):
    # 百度资讯指数
    try:
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Cookie": cookie,
            "Host": "index.baidu.com",
            "Referer": "http://index.baidu.com/v2/main/index.html",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
        }
        w = '{"name":"%s","wordType":1}' % word

        url = 'http://index.baidu.com/api/FeedSearchApi/getFeedIndex?area=0&word=[[%s]]&startDate=%s&endDate=%s' % (
            w,
            start_date,
            end_date,
        )

        r = requests.get(url=url, headers=headers, proxies=proxies.to_dict() if proxies else None)
        logging.info(r.json())
        data = r.json()["data"]
        all_data = data["index"][0]["data"]
        uniqid = data["uniqid"]
        ptbk = get_ptbk(uniqid, cookie, proxies=proxies)
        result = decrypt(ptbk, all_data).split(",")
        result = [int(item) if item != "" else 0 for item in result]
        temp_df_7 = pd.DataFrame(
            [pd.date_range(start=start_date, end=end_date), result],
            index=["date", word],
        ).T
        temp_df_7.index = pd.to_datetime(temp_df_7["date"])
        del temp_df_7["date"]
        return temp_df_7
    except Exception as e:
        logging.error(e)
        return None


def baidu_media_index(word, start_date, end_date, cookie, proxies: ProxyClient = None):
    # 百度媒体指数
    try:
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Cookie": cookie,
            "Host": "index.baidu.com",
            "Referer": "http://index.baidu.com/v2/main/index.html",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
        }
        w = '{"name":"%s","wordType":1}' % word

        url = 'http://index.baidu.com/api/NewsApi/getNewsIndex?area=0&word=[[%s]]&startDate=%s&endDate=%s' % (
            w,
            start_date,
            end_date,
        )

        r = requests.get(url=url, headers=headers, proxies=proxies.to_dict() if proxies else None)
        logging.info(r.json())
        data = r.json()["data"]
        all_data = data["index"][0]["data"]
        uniqid = data["uniqid"]
        ptbk = get_ptbk(uniqid, cookie)
        result = decrypt(ptbk, all_data).split(",")
        result = [int(item) if item != "" else 0 for item in result]
        temp_df_7 = pd.DataFrame(
            [pd.date_range(start=start_date, end=end_date), result],
            index=["date", word],
        ).T
        temp_df_7.index = pd.to_datetime(temp_df_7["date"])
        del temp_df_7["date"]
        return temp_df_7
    except Exception as e:
        logging.error(e)
        return None


if __name__ == "__main__":
    cookie = 'BDUSS=HQyaE9oTXQ0fkFxNUhESzkxNmdGaVFuRmRoQldJYWhVeWlpUXBSVEhNSlVybTFoSVFBQUFBJCQAAAAAAAAAAAEAAAA4yPIeeWVhaHdpbjEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFQhRmFUIUZhT'
    data = baidu_search_index(word="极限挑战", start_date='2021-04-01', end_date='2021-06-19', cookie=cookie)
    print(data)
