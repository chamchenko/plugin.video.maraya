# -*- coding: utf-8 -*-
# Copyright: (c) 2016, Chamchenko
# GNU General Public License v2.0+ (see LICENSE.txt or https://www.gnu.org/licenses/gpl-2.0.txt)
# This file is part of plugin.video.maraya


from __future__ import unicode_literals
import sys
import traceback
import xbmc

from .vars import *

try:
    from urllib.parse import quote_plus
    from urllib.parse import unquote_plus
    from html.parser import HTMLParser
    import urllib.parse as urlparse
except ImportError:
    from urllib import quote_plus
    from urllib import unquote_plus
    import HTMLParser
    import urlparse



def log(msg, level=xbmc.LOGDEBUG):
    if DEBUG == False and level != xbmc.LOGERROR: return
    if level == xbmc.LOGERROR: msg += ' ,' + traceback.format_exc()
    xbmc.log(ADDON_ID + '-' + ADDON_VERSION + '-' + msg, level)


def getParams():
    return dict(urlparse.parse_qsl(sys.argv[2][1:]))

def formatTitles(title):
    unwantedchars = '-_:|.'
    for c in unwantedchars:
        title = title.replace(c, ' ')
    title = title.replace('مسلسل', '')
    title = title.replace('قناة', '')
    title = title.replace('تلفزيون', '')
    title = ' '.join(title.split())
    return title.encode('utf-8').strip().decode('utf-8')
