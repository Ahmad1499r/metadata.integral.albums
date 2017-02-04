#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# INFO
# allmusic (no album review allowed)
# musicbrainz

# ARTWORK
# allmusic

import sys
import urllib
import urllib2
import json
import xbmc
import xbmcgui
import xbmcplugin
from theaudiodb import theaudiodb_albumfind
from theaudiodb import theaudiodb_albumdetails
from fanarttv import fanarttv_albumart

ADDONID = sys.modules[ "__main__" ].ADDONID

AUDIODBKEY = '58424d43204d6564696120'
AUDIODBURL = 'http://www.theaudiodb.com/api/v1/json/%s/%s'

FANARTVKEY = 'ed4b784f97227358b31ca4dd966a04f1'
FANARTVURL = 'http://webservice.fanart.tv/v3/music/albums/%s?api_key=%s'

def log(txt):
    if isinstance (txt,str):
        txt = txt.decode('utf-8')
    message = u'%s: %s' % (ADDONID, txt)
    xbmc.log(msg=message.encode('utf-8'), level=xbmc.LOGDEBUG)

def get_data(url):
    try:
        req = urllib2.urlopen(url)
        response = req.read()
        req.close()
    except:
        response = ''
    return response


class Scraper():
    def __init__(self, action, artist, album, url):
        if action == 'find':
            self.find_album(artist, album)
        elif action == 'getdetails':
            self.get_details(url)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def find_album(self, artist, album):
        # theaudiodb
        query = 'searchalbum.php?s=%s&a=%s' % (urllib.quote_plus(artist), urllib.quote_plus(album))
        url = AUDIODBURL % (AUDIODBKEY, query)
        result = get_data(url)
        if result:
            data = json.loads(result)
            if data:
                albumresults = theaudiodb_albumfind(data)
                if albumresults:
                    self.return_search(albumresults)

    def get_details(self, url):
        # theaudiodb
        result = get_data(url)
        if result:
            data = json.loads(result)
            if data:
                albumresults = theaudiodb_albumdetails(data)
                if albumresults:
                    # fanarttv
                    if albumresults['mbalbumid']:
                        url = FANARTVURL % (albumresults['mbalbumid'], FANARTVKEY)
                        result = get_data(url)
                        if result:
                            data = json.loads(result)
                            if data:
                                artresults = fanarttv_albumart(data)
                                if artresults:
                                    albumresults['thumb'] = albumresults['thumb'] + artresults['thumb']
                                    if not albumresults['cdart']:
                                        albumresults['cdart'] = artresults['cdart']
                    self.return_details(albumresults)

    def return_search(self, data):
        for count, item in enumerate(data):
            listitem = xbmcgui.ListItem(item['album'], thumbnailImage=item['thumb'], offscreen=True)
            listitem.setProperty('relevance', str(1.0 / (count + 1)))
            listitem.setProperty('album.artist', item['artist'])
            listitem.setProperty('album.year', item['year'])
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=item['url'], listitem=listitem, isFolder=True)

    def return_details(self, item):
        listitem = xbmcgui.ListItem(item['album'], offscreen=True)
        listitem.setProperty('album.musicbrainzid', item['mbalbumid'])
        listitem.setProperty('album.artists', str(len(item['artist'])))
        listitem.setProperty('album.genre', item['genre'])
        listitem.setProperty('album.styles', item['styles'])
        listitem.setProperty('album.moods', item['moods'])
        listitem.setProperty('album.themes', item['themes'])
        listitem.setProperty('album.compilation', item['compilation'])
        listitem.setProperty('album.review', item['description'])
        listitem.setProperty('album.release_date', '')
        listitem.setProperty('album.artist_description', item['artist_description'])
        listitem.setProperty('album.label', item['label'])
        listitem.setProperty('album.type', item['type'])
        listitem.setProperty('album.release_type', item['releasetype'])
        listitem.setProperty('album.year', item['year'])
        listitem.setProperty('album.rating', item['rating'])
        listitem.setProperty('album.userrating', '')
        listitem.setProperty('album.votes', item['votes'])
#        listitem.setProperty('album.cdart.url', item['cdart'])
        for count, artist in enumerate(item['artist']):
            listitem.setProperty('album.artist%i.name' % (count + 1), artist['artist'])
            listitem.setProperty('album.artist%i.musicbrainzid' % (count + 1), artist['mbartistid'])
        listitem.setProperty('album.thumbs', str(len(item['thumb'])))
        for count, thumb in enumerate(item['thumb']):
            listitem.setProperty('album.thumb%i.url' % (count + 1), thumb['thumb'])
            listitem.setProperty('album.thumb%i.aspect' % (count + 1), thumb['thumbaspect'])
        xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listitem)
