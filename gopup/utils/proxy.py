#!/usr/bin/env python
# coding=utf-8

'''
Author       : taoqitian
Date         : 2021-11-26 11:20:06
LastEditors  : taoqitian
LastEditTime : 2021-11-26 14:54:59
Description  : 代理类
FilePath     : /gopup/proxy.py
'''


class ProxyMeta:
    def __init__(self, host, port, user=None, password=None):
        self._host = host
        self._port = port
        self._user = user
        self._pass = password

    def to_url(self):
        if not all([self._host, self._port]):
            raise ValueError('host and port must be specified')
        if not all([self._user, self._pass]):
            return f'http://{self._host}:{self._port}'
        else:
            return f'http://{self._user}:{self._pass}@{self._host}:{self._port}'


class ProxyClient:
    def __init__(self, http_proxy_meta: ProxyMeta, https_proxy_meta: ProxyMeta = None):
        self._http_proxy_meta = http_proxy_meta
        self._https_proxy_meta = https_proxy_meta or http_proxy_meta

    def to_dict(self):
        return {'http': self._http_proxy_meta.to_url(), 'https': self._https_proxy_meta.to_url()}

    def test(self):
        import requests

        target_url = 'https://www.baidu.com'
        session = requests.Session()
        try:
            session.proxies = self.to_dict()
            resp = session.get(url=target_url)
            print(resp.text)
        except Exception as e:
            print(str(e))
