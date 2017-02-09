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
from musicbrainz import musicbrainz_albumfind
from musicbrainz import musicbrainz_albumdetails
from allmusic import allmusic_albumfind
from allmusic import allmusic_albumdetails
from fanarttv import fanarttv_albumart
from utils import *

def get_data(url):
    try:
        print '======= ALBUM URL ======='
        print url
        req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        request = urllib2.urlopen(req)
        response = request.read()
        print '======= ALBUM RESPONSE ======='
        print 'response'
        print '=========================='
        request.close()
    except:
        print '======= ALBUM RESPONSE ======='
        print '>>> FAILED! <<<'
        print '=========================='
        response = ''
    return response


class Scraper():
    def __init__(self, action, artist, album, url):
        if action == 'find':
            print '======= ALBUM FIND ======='
            result = self.find_album(artist, album)
            if result:
                self.return_search(result)
        elif action == 'getdetails':
            print '======= ALBUM DETAILS ======='
            result = self.get_details(url)
            if result:
                self.return_details(result)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def find_album(self, artist, album):
        # theaudiodb
#        query = AUDIODBSEARCH % (urllib.quote_plus(artist), urllib.quote_plus(album))
#        url = AUDIODBURL % (AUDIODBKEY, query)
#        result = get_data(url)
#        if not result:
#            return
#        data = json.loads(result)
#        if not data:
#            return
#        albumresults = theaudiodb_albumfind(data)
        # musicbrainz
#        query = MUSICBRAINZSEARCH % (urllib.quote_plus(artist), urllib.quote_plus(album))
#        url = MUSICBRAINZURL % query
#        xbmc.sleep(1000) # musicbrainz limit
#        result = get_data(url)
#        if not result:
#            return
#        data = json.loads(result)
#        if not data:
#            return
#        albumresults = musicbrainz_albumfind(data)
        # allmusic
        query = ALLMUSICSEARCH % (urllib.quote_plus(artist), urllib.quote_plus(album))
        url = ALLMUSICURL % query
        result = get_data(url)
        if not result:
            return
        albumresults = allmusic_albumfind(result)
        return albumresults

    def get_details(self, url):
        # theaudiodb
#        result = get_data(url)
#        if not result:
#            return
#        data = json.loads(result)
#        if not data:
#            return
#        albumresults = theaudiodb_albumdetails(data)
#        if not albumresults:
#            return
        # musicbrainz
#        xbmc.sleep(1000) # musicbrainz limit
#        result = get_data(url)
#        if not result:
#            return
#        data = json.loads(result)
#        if not data:
#            return
#        albumresults = musicbrainz_albumdetails(data)
#        if not albumresults:
#            return
        # allmusic
        result = get_data(url)
        if not result:
            return
        albumresults = allmusic_albumdetails(result)
        if not albumresults:
            return
        # fanarttv
#        if albumresults['mbalbumid']:
#            url = FANARTVURL % (albumresults['mbalbumid'], FANARTVKEY)
#            result = get_data(url)
#            if result:
#                data = json.loads(result)
#                if data:
#                    artresults = fanarttv_albumart(data)
#                    if artresults:
#                        albumresults['thumb'] = albumresults['thumb'] + artresults['thumb']
#                        if not albumresults['cdart']:
#                            albumresults['cdart'] = artresults['cdart']
        return albumresults

    def return_search(self, data):
        for count, item in enumerate(data):
            listitem = xbmcgui.ListItem(item['album'], thumbnailImage=item['thumb'], offscreen=True)
            listitem.setProperty('album.artist', item['artist'])
            listitem.setProperty('album.year', item['year'])
            listitem.setProperty('relevance', item['relevance'])
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
