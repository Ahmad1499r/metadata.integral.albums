# -*- coding: UTF-8 -*-

import os
import sys
import urllib
import urlparse
import xbmcplugin
import xbmcaddon

ADDON = xbmcaddon.Addon()
ADDONID = ADDON.getAddonInfo('id')
VERSION = ADDON.getAddonInfo('version')

from lib.scraper import Scraper


class Main:
    def __init__(self):
        action, artist, album, url = self._parse_argv()
        Scraper(action, artist, album, url)

    def _parse_argv(self):
        params = dict(urlparse.parse_qsl(sys.argv[2].lstrip('?')))
        action = params['action']
        artist = urllib.unquote_plus(params.get('artist', ''))
        album = urllib.unquote_plus(params.get('title', ''))
        url = urllib.unquote_plus(params.get('url', ''))
        return action, artist, album, url


if (__name__ == '__main__'):
    Main()
