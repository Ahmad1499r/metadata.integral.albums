# -*- coding: UTF-8 -*-

import sys
import time
import urllib
import urllib2
import json
from threading import Thread
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
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
        req = urllib2.Request(url, headers={'User-Agent': 'Intergral Albums Scraper/%s ( http://kodi.tv )' % xbmcaddon.Addon().getAddonInfo('version')})
        request = urllib2.urlopen(req)
        response = request.read()
        request.close()
    except urllib2.HTTPError, error:
        print '============================================='
        print str(error.code)
        print str(error.reason)
        print '-------------------------------------------'
        response = ''
    return response


class Scraper():
    def __init__(self, action, artist, album, url):
        self.start = 0
        if action == 'find':
            result = self.find_album(artist, album, 'theaudiodb')
            if not result:
                result = self.find_album(artist, album, 'musicbrainz')
            #TODO search allmusic?
            if result:
                self.start = time.time()
                self.return_search(result)
        elif action == 'getdetails':
            details = {}
            mbresult = Thread(target = self.get_details, args = (url, 'musicbrainz', details))
            adresult = Thread(target = self.get_details, args = (url, 'theaudiodb', details))
            ftresult = Thread(target = self.get_details, args = (url, 'fanarttv', details))
            mbresult.start()
            adresult.start()
            ftresult.start()
            mbresult.join()
            if details['musicbrainz'] and ('amlink' in details['musicbrainz']):
                amsearch = True
                amresult = Thread(target = self.get_details, args = (details['musicbrainz']['amlink'], 'allmusic', details))
                amresult.start()
            else:
                #TODO search allmusic?
                amsearch = False
            adresult.join()
            ftresult.join()
            if amsearch:
                amresult.join()
            result = self.compile_results(details)
            if result:
                self.return_details(result)
        if self.start: # musicbrainz ratelimit
            self.end = time.time()
            if self.end - self.start < 1:
                diff = int((1 - (self.end - self.start)) * 1000) + 1
                xbmc.sleep(diff)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def find_album(self, artist, album, scraper):
        # theaudiodb
        if scraper == 'theaudiodb':
            query = AUDIODBSEARCH % (urllib.quote_plus(artist), urllib.quote_plus(album))
            url = AUDIODBURL % (AUDIODBKEY, query)
            result = get_data(url)
            if not result:
                return
            data = json.loads(result)
            if not data:
                return
            albumresults = theaudiodb_albumfind(data)
            return albumresults
        # musicbrainz
        elif scraper == 'musicbrainz':
            query = MUSICBRAINZSEARCH % (urllib.quote_plus(artist), urllib.quote_plus(album))
            url = MUSICBRAINZURL % query
            result = get_data(url)
            if not result:
                return
            data = json.loads(result)
            if not data:
                return
            albumresults = musicbrainz_albumfind(data)
            return albumresults
        # allmusic
        elif scraper == 'allmusic':
            query = ALLMUSICSEARCH % (urllib.quote_plus(artist), urllib.quote_plus(album))
            url = ALLMUSICURL % query
            result = get_data(url)
            if not result:
                return
            albumresults = allmusic_albumfind(result)
            return albumresults

    def get_details(self, mbid, scraper, details):
        # theaudiodb
        if scraper == 'theaudiodb':
            url = AUDIODBURL % (AUDIODBKEY, AUDIODBDETAILS % mbid)
            result = get_data(url)
            if not result:
                return
            data = json.loads(result)
            if not data:
                return
            albumresults = theaudiodb_albumdetails(data)
            if not albumresults:
                return
            details[scraper] = albumresults
        # musicbrainz
        elif scraper == 'musicbrainz':
            url = MUSICBRAINZURL % (MUSICBRAINZDETAILS % mbid)
            self.start = time.time()
            result = get_data(url)
            if not result:
                return
            data = json.loads(result)
            if not data:
                return
            albumresults = musicbrainz_albumdetails(data)
            if not albumresults:
                return
            details[scraper] = albumresults
        # allmusic
        elif scraper == 'allmusic':
            url = ALLMUSICDETAILS % mbid # = url
            result = get_data(url)
            if not result:
                return
            albumresults = allmusic_albumdetails(result)
            if not albumresults:
                return
            details[scraper] = albumresults
        # fanarttv
        elif scraper == 'fanarttv':
            url = FANARTVURL % (mbid, FANARTVKEY)
            result = get_data(url)
            if not result:
                return
            data = json.loads(result)
            if not data:
                return
            albumresults = fanarttv_albumart(data)
            if not albumresults:
                return
            details[scraper] = albumresults

    def compile_results(self, details):
        result = {}
        thumbs = []
        # merge results (and thumbs separately)
        if 'musicbrainz' in details:
            for k, v in details['musicbrainz'].items():
                result[k] = v
        if 'theaudiodb' in details:
            for k, v in details['theaudiodb'].items():
                result[k] = v
                if k == 'thumb':
                    thumbs += v
        if 'fanarttv' in details:
            for k, v in details['fanarttv'].items():
                result[k] = v
                if k == 'thumb':
                    thumbs += v
        if 'allmusic' in details:
            for k, v in details['allmusic'].items():
                result[k] = v
                if k == 'thumb':
                    thumbs += v
        if result:
            result['thumb'] = thumbs
        return result

    def return_search(self, data):
        for count, item in enumerate(data):
            listitem = xbmcgui.ListItem(item['album'], thumbnailImage=item['thumb'], offscreen=True)
            listitem.setProperty('album.artist', item['artist'])
            listitem.setProperty('album.year', item['year'])
            listitem.setProperty('relevance', item['relevance'])
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=item['url'], listitem=listitem, isFolder=True)

    def return_details(self, item):
        listitem = xbmcgui.ListItem(item['album'], offscreen=True)
        if 'mbalbumid' in item:
            listitem.setProperty('album.musicbrainzid', item['mbalbumid'])
        if 'artist' in item:
            listitem.setProperty('album.artists', str(len(item['artist'])))
            for count, artist in enumerate(item['artist']):
                listitem.setProperty('album.artist%i.name' % (count + 1), artist['artist'])
                listitem.setProperty('album.artist%i.musicbrainzid' % (count + 1), artist['mbartistid'])
        if 'genre' in item:
            listitem.setProperty('album.genre', item['genre'])
        if 'styles' in item:
            listitem.setProperty('album.styles', item['styles'])
        if 'moods' in item:
            listitem.setProperty('album.moods', item['moods'])
        if 'themes' in item:
            listitem.setProperty('album.themes', item['themes'])
        if 'compilation' in item: # do we need to set this? if so is this a 'various artist album' or a 'greatest hits album by a single artist' ?
            listitem.setProperty('album.compilation', item['compilation'])
        if 'description' in item:
            listitem.setProperty('album.review', item['description'])
        if 'releasedate' in item: # do we use this, does it need to be in a specific format ?
            listitem.setProperty('album.release_date', item['releasedate'])
        if 'artist_description' in item:
            listitem.setProperty('album.artist_description', item['artist_description'])
        if 'label' in item:
            listitem.setProperty('album.label', item['label'])
        if 'type' in item:
            listitem.setProperty('album.type', item['type'])
        if 'releasetype' in item: # this is always 'album' ?
            listitem.setProperty('album.release_type', item['releasetype'])
        if 'year' in item:
            listitem.setProperty('album.year', item['year'])
        if 'rating' in item:
            listitem.setProperty('album.rating', item['rating'])
        if 'userrating' in item: # don't think we need to set this ?
            listitem.setProperty('album.userrating', '')
        if 'votes' in item:
            listitem.setProperty('album.votes', item['votes'])
        if 'cdart' in item:
            listitem.setProperty('album.cdart.url', item['cdart'])
        if 'thumb' in item:
            listitem.setProperty('album.thumbs', str(len(item['thumb'])))
            for count, thumb in enumerate(item['thumb']):
                listitem.setProperty('album.thumb%i.url' % (count + 1), thumb['thumb'])
                listitem.setProperty('album.thumb%i.aspect' % (count + 1), thumb['thumbaspect'])
        xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listitem)
