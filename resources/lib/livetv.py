# -*- coding: utf-8 -*-
# Copyright: (c) 2016, Chamchenko
# GNU General Public License v2.0+ (see LICENSE.txt or https://www.gnu.org/licenses/gpl-2.0.txt)
# This file is part of plugin.video.maraya


from __future__ import unicode_literals
import json
import re
import xbmcplugin
import sys
import urlquick

from .vars import *
from .create_item import addLink
from .tools import log
from .tools import formatTitles

def browseLiveTV():
    log(" Fetching url: %s" % URL_LIVES)
    items = json.loads(urlquick.get(URL_LIVES, headers=headers).text)
    for idx, block in enumerate(items['blocks']):
        if block['block_type'] == 'horizontal_channel_list_vod':
            block_idx = idx
    for channel in items['blocks'][block_idx]['channels']:
        playbackURL = channel['streams']['hls']
        if not playbackURL:
            continue
        channel_id = channel['id']
        title = formatTitles(channel['title'])
        thumb = channel['logo']['small']
        fanart = channel['cover']['full']
        infoLabels = {"title":title}
        infoArt = {
                    "thumb": thumb,
                    "poster": thumb,
                    "fanart": fanart,
                    "icon": thumb,
                    "logo": thumb
                }
        addLink(title, playbackURL, 8, infoLabels, infoArt, len(items))
