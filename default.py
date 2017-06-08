# -*- coding: UTF-8 -*-
import sys
import urllib
import urlparse

from lib.scraper import Scraper


class Main:
    def __init__(self):
        action, artist, album, url, key = self._parse_argv()
        Scraper(action, artist, album, url, key)

    def _parse_argv(self):
        params = dict(urlparse.parse_qsl(sys.argv[2].lstrip('?')))
        action = params['action']
        artist = params.get('artist', '')
        album = params.get('title', '')
        url = params.get('url', '')
        key = params.get('key', '')
        return action, artist, album, url, key


if (__name__ == '__main__'):
    Main()
