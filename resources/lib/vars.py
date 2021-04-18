# -*- coding: utf-8 -*-
# Copyright: (c) 2016, Chamchenko
# GNU General Public License v2.0+ (see LICENSE.txt or https://www.gnu.org/licenses/gpl-2.0.txt)
# This file is part of plugin.video.maraya


from __future__ import unicode_literals
import xbmcaddon
from xbmc import getInfoLabel
ADDON_ID = 'plugin.video.maraya'
REAL_SETTINGS = xbmcaddon.Addon(id=ADDON_ID)
ADDON_NAME = REAL_SETTINGS.getAddonInfo('name')
SETTINGS_LOC = REAL_SETTINGS.getAddonInfo('profile')
ADDON_PATH = REAL_SETTINGS.getAddonInfo('path')
ADDON_VERSION = REAL_SETTINGS.getAddonInfo('version')
ICON = REAL_SETTINGS.getAddonInfo('icon')
FANART = REAL_SETTINGS.getAddonInfo('fanart')
LANGUAGE = REAL_SETTINGS.getLocalizedString
DEBUG = REAL_SETTINGS.getSetting('Debugging') == 'true'
XBMC_VERSION = int(getInfoLabel("System.BuildVersion").split('-')[0].split('.')[0])
INPUTSTREAM_PROP = 'inputstream' if XBMC_VERSION >= 19 else 'inputstreamaddon'
USER_AGENT = "maraya/1.0.71 (com.Semicolon.Maraya; build:1.0.71.0; iOS 14.4.0) Alamofire/5.2.2"
headers = {"User-Agent": USER_AGENT}

URL_YOUTUBE = 'https://www.youtube.com/embed/%s'
IMG_BASE_URL = 'https://maraya.faulio.com%s'
API_BASE_URL = 'https://maraya.faulio.com/api/v1/'
URL_LIVES = API_BASE_URL + 'page/channels/1'
CATEGORIES_URL = API_BASE_URL + 'genre'
SHOWS_URL = API_BASE_URL + 'project/'
SHOW_URL = API_BASE_URL + 'plus/show'
EPISODES_URL = API_BASE_URL + 'video'
EPISODE_URL = API_BASE_URL + 'video/%s/player'
SHOWS_PARAMS = {'page': 1, 'ipp': 500}
EPISODES_PARAMS = {'ipp': 500}

MAIN_MENU = [('\u0627\u0644\u0645\u0628\u0627\u0634\u0631', "", 1),
             ('\u0643\u0644 \u0627\u0644\u0645\u062d\u062a\u0648\u064a\u0627\u062a', "", 2),]
