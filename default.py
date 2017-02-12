# -*- coding: UTF-8 -*-
import sys
import urllib
import urlparse

from lib.scraper import Scraper


class Main:
    def __init__(self):
        action, artist, album, url = self._parse_argv()
        # no support for providing an url through a .nfo file
        if url.startswith('http://'):
            return
        Scraper(action, artist, album, url)

    def _parse_argv(self):
        params = dict(urlparse.parse_qsl(sys.argv[2].lstrip('?')))
        action = params['action']
        artist = params.get('artist', '')
        album = params.get('title', '')
        url = params.get('url', '')
        return action, artist, album, url


if (__name__ == '__main__'):
    Main()
