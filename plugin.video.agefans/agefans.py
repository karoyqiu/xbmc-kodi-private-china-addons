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


    def get_rank(self, page, show_detail):
        j = self.__get('/rank?page={0}'.format(page + 1))
        pre = j['AniRankPre']
        items = []
        lastNo = 0

        for ani in pre:
            lastNo = ani['NO']
            item = {}
            item['label'] = u'{0}. {1}'.format(lastNo, ani['Title'])
            item['path'] = self.__plugin.url_for(show_detail, aid=ani['AID'])
            item['thumbnail'] = ani['PicSmall']
            items.append(item)

        return items, j['AllCnt'] > lastNo


    def get_detail(self, aid, show_playlist):
        j = self.__get('/detail/' + aid)
        info = j['AniInfo']
        playlists = info[u'R在线播放All']
        cache = { 'playlists': playlists }
        self.__cache[aid] = cache

        items = []

        for i in range(len(playlists)):
            playlist = playlists[i]
            n = len(playlist)
            if n == 0:
                continue

            item = {}
            item['label'] = u'播放列表 {0}'.format(i + 1)
            item['path'] = self.__plugin.url_for(show_playlist, aid=aid, index=i)
            items.append(item)

        return items


    def get_playlist(self, aid, index):
        playlist = self.__cache[aid]['playlists'][index]
        items = []

        for eps in playlist:
            item = {}
            item['label'] = eps['Title']
            item['path'] = unquote(eps['PlayVid']).decode('utf-8')
            item['is_playable'] = True
            items.append(item)

        return items


    def __get(self, url):
        r = requests.get(self.__baseurl + url)
        return json.loads(r.text)
