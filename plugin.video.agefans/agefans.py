#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import requests
from urllib2 import unquote


class Agefans(object):
    def __init__(self, plugin):
        self.__baseurl = 'https://api.agefans.app/v2'
        self.__plugin = plugin
        self.__cache = plugin.get_storage('cache')


    def get_rank(self, show_detail):
        j = self.__get('/rank')
        pre = j['AniRankPre']
        items = []

        for ani in pre:
            item = {}
            item['label'] = ani['Title']
            item['path'] = self.__plugin.url_for(show_detail, aid=ani['AID'])
            items.append(item)

        return items


    def __get(self, url):
        r = requests.get(self.__baseurl + url)
        return json.loads(r.text)
