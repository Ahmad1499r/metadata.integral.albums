#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import urllib
import xbmc
import xbmcplugin
import xbmcaddon

ADDON = xbmcaddon.Addon()
ADDONID = ADDON.getAddonInfo('id')
VERSION = ADDON.getAddonInfo('version')

def log(txt):
    if isinstance (txt,str):
        txt = txt.decode('utf-8')
    message = u'%s: %s' % (ADDONID, txt)
    xbmc.log(msg=message.encode('utf-8'), level=xbmc.LOGDEBUG)

def get_params():
    param = {}
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2].replace('?', '').rstrip('/').split('&')
        for item in params:
            splitparams = item.split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param


class Main:
    def __init__(self):
        action, artist, album, url = self._parse_argv()
        if (artist and album) or url:
            from lib.scraper import Scraper
            Scraper(action, artist, album, url)
        else:
            xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def _parse_argv(self):
        artist = ''
        album = ''
        url = ''
        params = get_params()
        action = params['action']
        if 'artist' in params:
            artist = urllib.unquote_plus(params['artist'])
        if 'title' in params:
            album = urllib.unquote_plus(params['title'])
        if 'url' in params:
            url = urllib.unquote_plus(params['url'])
        return action, artist, album, url


if (__name__ == '__main__'):
    log('script version %s started' % VERSION)
    Main()
    log('script version %s ended' % VERSION)
