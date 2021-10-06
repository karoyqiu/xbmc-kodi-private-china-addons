#!/usr/bin/python
# -*- coding: utf-8 -*-
from xbmcswift2 import Plugin
from agefans import Agefans


plugin = Plugin()


@plugin.route('/')
def index():
    items = [
        {
            'label': u'排行榜',
            'path': plugin.url_for('show_rank'),
        }
    ]

    return items


@plugin.cached_route('/rank')
def show_rank():
    agefans = Agefans(plugin)
    return agefans.get_rank('show_detail')


@plugin.cached_route('/detail/<aid>')
def show_detail(aid):
    agefans = Agefans(plugin)
    return agefans.get_detail(aid, 'show_playlist')


@plugin.route('/playlist/<aid>/<index>')
def show_playlist(aid, index):
    index = int(index)
    agefans = Agefans(plugin)
    return agefans.get_playlist(aid, index)


if __name__ == '__main__':
    plugin.run()
