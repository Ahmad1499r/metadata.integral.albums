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
    except:
        response = ''
    return response


class Scraper():
    def __init__(self, action, artist, album, url):
        self.start = 0
        if action == 'find': # only useful for manual search, search both/all providers?
            result = self.find_album(artist, album, 'theaudiodb')
            if not result:
                result = self.find_album(artist, album, 'musicbrainz')
            #TODO search allmusic.. is it likely an album does not exist on musicbrainz, but does on allmusic?
            if result:
                self.return_search(result)
        elif action == 'getdetails':
            url = json.loads(url)
            artist = url['artist'].encode('utf-8')
            album = url['album'].encode('utf-8')
            mbid = url['mbid']
            details = {}
            mbresult = Thread(target = self.get_details, args = (mbid, 'musicbrainz', details))
            adresult = Thread(target = self.get_details, args = (mbid, 'theaudiodb', details))
            ftresult = Thread(target = self.get_details, args = (mbid, 'fanarttv', details))
            amresult = Thread(target = self.get_details, args = ([artist, album], 'allmusic', details))
            mbresult.start()
            adresult.start()
            ftresult.start()
            amresult.start()
            mbresult.join()
            adresult.join()
            ftresult.join()
            amresult.join()
            result = self.compile_results(details)
            if result:
                self.return_details(result)
        if self.start: # musicbrainz ratelimit
            self.end = time.time()
            if self.end - self.start < 1:
                diff = int((1 - (self.end - self.start)) * 1000) + 100 # wait max 1.1 sec.
                xbmc.sleep(diff)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def find_album(self, artist, album, site):
        # theaudiodb
        if site == 'theaudiodb':
            url = AUDIODBURL % (AUDIODBKEY, AUDIODBSEARCH % (urllib.quote_plus(artist), urllib.quote_plus(album)))
            scraper = theaudiodb_albumfind
        # musicbrainz
        elif site == 'musicbrainz':
            url = MUSICBRAINZURL % (MUSICBRAINZSEARCH % (urllib.quote_plus(artist), urllib.quote_plus(album)))
            scraper = musicbrainz_albumfind
        # allmusic
        elif site == 'allmusic':
            url = ALLMUSICURL % (ALLMUSICSEARCH % (urllib.quote_plus(artist), urllib.quote_plus(album)))
            scraper = allmusic_albumfind
        result = get_data(url)
        if site == 'musicbrainz':
            self.start = time.time()
        if not result:
            return
        if not site == 'allmusic':
            result = json.loads(result)
        albumresults = scraper(result)
        return albumresults

    def get_details(self, mbid, site, details):
        # theaudiodb
        if site == 'theaudiodb':
            url = AUDIODBURL % (AUDIODBKEY, AUDIODBDETAILS % mbid)
            albumscraper = theaudiodb_albumdetails
        # musicbrainz
        elif site == 'musicbrainz':
            url = MUSICBRAINZURL % (MUSICBRAINZDETAILS % mbid)
            albumscraper = musicbrainz_albumdetails
        # fanarttv
        elif site == 'fanarttv':
            url = FANARTVURL % (mbid, FANARTVKEY)
            albumscraper = fanarttv_albumart
        # allmusic
        elif site == 'allmusic':
            found = self.find_album(mbid[0], mbid[1], 'allmusic')
            if found:
                url = ALLMUSICDETAILS % found[0]['mbid'] # = url
                albumscraper = allmusic_albumdetails
            else:
                return
        result = get_data(url)
        if site == 'musicbrainz':
            self.start = time.time()
        if not result:
            return
        if not site == 'allmusic':
            result = json.loads(result)
        albumresults = albumscraper(result)
        if not albumresults:
            return
        details[site] = albumresults

    def compile_results(self, details):
        #TODO implement user preferences
        result = {}
        thumbs = []
        # merge results
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
        if result: # provide artwork from all scrapers
            result['thumb'] = thumbs
        return result

    def return_search(self, data):
        for count, item in enumerate(data):
            listitem = xbmcgui.ListItem(item['album'], thumbnailImage=item['thumb'], offscreen=True)
            listitem.setProperty('album.artist', item['artist'])
            listitem.setProperty('album.year', item['year'])
            listitem.setProperty('relevance', item['relevance'])
            url = {'artist':item['artist'], 'album':item['album'], 'mbid':item['mbid']}
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=json.dumps(url), listitem=listitem, isFolder=True)

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
        if 'compilation' in item: # do we need to set this? if so, is this a 'various artist album' or a 'greatest hits album by a single artist' ?
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
        if 'rating' in item: # check what format it needs to be
            listitem.setProperty('album.rating', item['rating'])
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
