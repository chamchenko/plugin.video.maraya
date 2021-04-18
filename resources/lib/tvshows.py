# -*- coding: utf-8 -*-
# Copyright: (c) 2016, Chamchenko
# GNU General Public License v2.0+ (see LICENSE.txt or https://www.gnu.org/licenses/gpl-2.0.txt)
# This file is part of plugin.video.maraya



from __future__ import unicode_literals
import json
import xbmcplugin
import sys
import urlquick

from .vars import *
from .tools import *
from .create_item import addDir
from .create_item import addLink
from datetime import datetime

def browseCategories():
    log('browseCategories')
    log(" Fetching url: %s" % CATEGORIES_URL)
    categories = json.loads(
                    urlquick.get(CATEGORIES_URL,
                            headers=headers).text)
    for category in categories:
        category_id = category['id']
        category_name = formatTitles(category['name'])
        addDir(category_name, category_id, 3)


def getTvShows(category_id):
    log('getTvShows')
    xbmcplugin.setContent(int(sys.argv[1]), 'videos')
    SHOWS_PARAMS.update({'genre': category_id})
    log(" Fetching url: %s" % SHOWS_URL)
    log(" Fetching params: %s" % SHOWS_PARAMS)
    apijson = json.loads(
                    urlquick.get(SHOWS_URL,
                        headers=headers,
                        params=SHOWS_PARAMS).text)
    next_page = apijson['blocks'][0]['next_page']
    for item in apijson['blocks'][0]['projects']:
        title = formatTitles(item['title'])
        showId = item['id']
        thumb = item['image']
        try:
            fanart = IMG_BASE_URL % (item['cover']['fullhd'])
        except:
            fanart = thumb
        infoList = {
                        "mediatype": "tvshows",
                        "title": title,
                        "TVShowTitle": title,
                    }
        infoArt = {
                    "thumb": thumb,
                    "poster": thumb,
                    "fanart": fanart,
                    "icon": thumb,
                    "logo": thumb
                }
        infos = json.dumps({
                                'showId': showId,
                                'thumb': thumb,
                            })
        xbmcplugin.addSortMethod(int(sys.argv[1]) , xbmcplugin.SORT_METHOD_LABEL)
        xbmcplugin.addSortMethod(int(sys.argv[1]) , xbmcplugin.SORT_METHOD_TITLE)
        addDir(title, showId, 4, infoArt, infoList,0, showId)

def getSeasons(showId):
    log('getSeasons')
    xbmcplugin.setContent(int(sys.argv[1]), 'videos')
    log(" Fetching url: %s" % (SHOWS_URL + showId))
    apijson = json.loads(
                    urlquick.get(SHOWS_URL + showId,
                        headers=headers).text)
    for idx, block in enumerate(apijson['blocks']):
        if block['block_type'] == 'block_seasons':
            block_idx = idx
    for season in apijson['blocks'][block_idx]['seasons']:
        title = 'Season %s' % season['title']
        seasonID = season['id']
        thumb = season['cover']['small']
        fanart = season['cover']['big']
        infoList = {
                        "mediatype": "seasons",
                        "title": title,
                    }
        infoArt = {
                    "thumb": thumb,
                    "poster": thumb,
                    "fanart": fanart,
                    "icon": thumb,
                    "logo": thumb
                }
        xbmcplugin.addSortMethod(int(sys.argv[1]) , xbmcplugin.SORT_METHOD_LABEL)
        xbmcplugin.addSortMethod(int(sys.argv[1]) , xbmcplugin.SORT_METHOD_TITLE)
        addDir(title, seasonID, 5, infoArt, infoList)


def getEpisodes(seasonID):
    log('getEpisodes')
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    EPISODES_PARAMS.update({'season': seasonID})
    log(" Fetching url: %s" % EPISODES_URL)
    log(" Fetching params: %s" % EPISODES_PARAMS)
    items = json.loads(
                urlquick.get(EPISODES_URL,
                    params=EPISODES_PARAMS,
                    headers=headers).text)
    showTitle = formatTitles(items['blocks'][0]['projects'][0]['program_title'])
    episode_mode = 'up'
    firstep_title = items['blocks'][0]['projects'][0]['title']
    firstep_numb = items['blocks'][0]['projects'][0]['episode']
    if ('الأولى' in firstep_title and  firstep_numb != 1):
        episode_mode = 'down'
    count_ep = len(items['blocks'][0]['projects'])
    for item in items['blocks'][0]['projects']:
        streamID = item['id']
        season = item['season_number']
        plot = formatTitles(item['title'])
        if episode_mode == 'up':
            episode = item['episode']
        else:
            episode = count_ep - item['episode'] + 1
        thumb = item['image']
        aired = str(datetime.fromtimestamp(item['published'])).split(' ')[0]
        try:
            duration = item['duration']['total']
        except:
            duration = 0
        source = item['source']
        youtube_id = item['source_id']
        infos = json.dumps({'streamID': streamID, 'source': source, 'youtube_id': youtube_id})
        infoLabels = {
                        "mediatype": "episode",
                        "title": showTitle,
                        "episode": episode,
                        "season": season,
                        "aired": aired,
                        "plot": plot,
                        "duration": duration,
                        "TVShowTitle": showTitle
                    }
        infoArt = {
                    "thumb":thumb,
                    "poster":thumb,
                    "fanart":thumb,
                    "icon":thumb,
                    "logo":thumb
                }
        xbmcplugin.addSortMethod(int(sys.argv[1]) , xbmcplugin.SORT_METHOD_EPISODE)
        addLink(showTitle, infos, 9, infoLabels, infoArt)
