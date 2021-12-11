#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/20 0020
# @Author  : justin.郑 3907721@qq.com
# @File    : index_weibo.py
# @Desc    : 获取微博指数

import datetime
import logging
import re

import matplotlib.pyplot as plt
import pandas as pd
import requests
from gopup.index.cons import index_weibo_headers  # 伪装游览器, 必备
from gopup.utils.proxy import ProxyClient

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 显示中文标签


def _get_items(word="股票"):
    url = "https://data.weibo.com/index/ajax/newindex/searchword"
    payload = {"word": word}
    try:
        res = requests.post(url, data=payload, headers=index_weibo_headers)
        return {word: re.findall(r"\d+", res.json()["html"])[0]}
    except Exception as e:
        logging.error(res.text)
        raise e


def _get_index_data(wid, time_type, proxies: ProxyClient = None):
    url = "http://data.weibo.com/index/ajax/newindex/getchartdata"
    data = {
        "wid": wid,
        "dateGroup": time_type,
    }
    try:
        res = requests.get(
            url, params=data, headers=index_weibo_headers, proxies=proxies.to_dict() if proxies else None
        )
        logging.info(res.text)
        json_df = res.json()
        if json_df['code'] == 101:
            logging.info('no data')
            return pd.DataFrame()
        data = {
            "index": json_df["data"][0]["trend"]["x"],
            "value": json_df["data"][0]["trend"]["s"],
        }
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        raise e


def _process_index(index):
    now = datetime.datetime.now()
    curr_year = now.year
    curr_date = "%04d%02d%02d" % (now.year, now.month, now.day)
    if "月" in index:
        tmp = index.replace("日", "").split("月")
        date = "%04d%02d%02d" % (curr_year, int(tmp[0]), int(tmp[1]))
        if date > curr_date:
            date = "%04d%02d%02d" % (curr_year - 1, int(tmp[0]), int(tmp[1]))
        return date
    return index


def weibo_index(word="python", time_type="3month", proxies: ProxyClient = None):
    """
    :param word: str
    :param time_type: str 1hour, 1day, 1month, 3month （不包含当天）
    :return:
    """
    try:
        dict_keyword = _get_items(word)
        df_list = []
        for keyword, wid in dict_keyword.items():
            df = _get_index_data(wid, time_type, proxies=proxies)
            if df is not None:
                df.columns = ["index", keyword]
                df["index"] = df["index"].apply(lambda x: _process_index(x))
                df.set_index("index", inplace=True)
                df_list.append(df)
        if len(df_list) > 0:
            df = pd.concat(df_list, axis=1)
            if time_type == "1hour" or "1day":
                df.index = pd.to_datetime(df.index)
            else:
                df.index = pd.to_datetime(df.index, format="%Y%m%d")
            return df
    except Exception as e:
        logging.error(e)
        return None


if __name__ == "__main__":
    df_index = weibo_index(word="疫情", time_type="3month")
    print(df_index)
    df_index.plot()
    plt.show()
