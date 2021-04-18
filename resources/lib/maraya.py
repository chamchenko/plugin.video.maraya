# -*- coding: utf-8 -*-
# Copyright: (c) 2016, Chamchenko
# GNU General Public License v2.0+ (see LICENSE.txt or https://www.gnu.org/licenses/gpl-2.0.txt)
# This file is part of plugin.video.maraya

from __future__ import unicode_literals

import sys
import json
import urlquick
import xbmcgui
import xbmcplugin
import inputstreamhelper
import YDStreamExtractor

from .tools import *
from .livetv import browseLiveTV
from .tvshows import browseCategories
from .tvshows import getTvShows
from .tvshows import getSeasons
from .tvshows import getEpisodes
from .create_item import addDir
from .vars import *


class MARAYA(object):
    def __init__(self):
        log('__init__')
    def buildMenu(self):
        for item in MAIN_MENU: addDir(*item)
    def browseLive(self):
        browseLiveTV()
    def browseShowsMenu(self):
        browseCategories()
    def browseShows(self, category_id):
        getTvShows(category_id)
    def browseSeasons(self, showId):
        getSeasons(showId)
    def browseEpisodes(self, seasonID):
        getEpisodes(seasonID)


    def playLive(self, name, playbackURL):
        log(" playLive: %s" % name)
        liz = xbmcgui.ListItem(name, path=playbackURL)
        liz.setProperty(INPUTSTREAM_PROP,'inputstream.adaptive')
        liz.setProperty('inputstream.adaptive.manifest_type', 'hls')
        liz.setProperty('inputstream.adaptive.stream_headers', 'User-Agent=%s' % USER_AGENT)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem=liz)


    def playVideo(self, name, infos, liz=None):
        log(" playVideo: %s" % name)
        infos = json.loads(infos)
        streamID = infos['streamID']
        source = infos['source']
        youtube_id = infos['youtube_id']
        if source == 'youtube':
            log(" Resolving: %s" % (URL_YOUTUBE % youtube_id))
            playbackURL = YDStreamExtractor.getVideoInfo(URL_YOUTUBE % youtube_id).streamURL()
            liz = xbmcgui.ListItem(name, path=playbackURL)
        else:
            log(" Fetching url: %s" % (EPISODE_URL%streamID))
            json_parser = json.loads(
                            urlquick.get(EPISODE_URL % streamID,
                                max_age=-1).text)
            playbackURL = json_parser['settings']['protocols']['hls']
            liz = xbmcgui.ListItem(name, path=playbackURL)
            liz.setProperty('inputstream.adaptive.manifest_type', 'hls')
            liz.setProperty(INPUTSTREAM_PROP,'inputstream.adaptive')
            liz.setProperty('inputstream.adaptive.stream_headers', 'User-Agent=%s' % USER_AGENT)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem=liz)

        
params=getParams()
try: url=unquote_plus(params["url"])
except: url=None
try: name=unquote_plus(params["name"]).encode('utf-8').strip().decode('utf-8')
except: name=None
try: mode=int(params["mode"])
except: mode=None
log("Mode: "+str(mode))
log("URL : "+str(url))
log("Name: "+str(name))

if  mode==None: MARAYA().buildMenu()
elif mode == 1: MARAYA().browseLive()
elif mode == 2: MARAYA().browseShowsMenu()
elif mode == 3: MARAYA().browseShows(url)
elif mode == 4: MARAYA().browseSeasons(url)
elif mode == 5: MARAYA().browseEpisodes(url)
elif mode == 8: MARAYA().playLive(name, url)
elif mode == 9: MARAYA().playVideo(name, url)

xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
