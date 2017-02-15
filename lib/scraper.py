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
        if action == 'find':
            result = self.find_album(artist, album, 'musicbrainz')
            if result:
                self.return_search(result)
        elif action == 'getdetails':
            details = {}
            if url.startswith('http://'):
                if url.startswith('http://www.theaudiodb.com/'):
                    site = 'theaudiodb-nfo'
                elif url.startswith('http://www.allmusic.com/'):
                    site = 'allmusic-nfo'
                else:
                    return
                thread = Thread(target = self.get_details, args = (url, site, details))
                thread.start()
                thread.join()
            else:
                url = json.loads(url)
                artist = url['artist'].encode('utf-8')
                album = url['album'].encode('utf-8')
                mbid = url['mbid']
                threads = []
                for item in [[mbid, 'musicbrainz'], [mbid, 'theaudiodb'], [mbid, 'fanarttv'], [[artist, album], 'allmusic']]:
                    thread = Thread(target = self.get_details, args = (item[0], item[1], details))
                    threads.append(thread)
                    thread.start()
                for thread in threads:
                    thread.join()
            result = self.compile_results(details)
            if result:
                self.return_details(result)
        # musicbrainz ratelimit
        if self.start:
            self.end = time.time()
            if self.end - self.start < 1:
                # wait max 1.1 second
                diff = int((1 - (self.end - self.start)) * 1000) + 100
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
        elif site == 'theaudiodb-nfo':
            site = 'theaudiodb'
            url = mbid
        elif site == 'allmusic-nfo':
            site = 'allmusic'
            url = mbid
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
        # use musicbrainz artist list as they provide mbid's, these can be passed to the artist scraper
        result['artist'] = details['musicbrainz']['artist']
        # provide artwork from all scrapers for getthumb option
        if result:
            result['thumb'] = thumbs
        data = self.user_prefs(details, result)
        return data

    def user_prefs(self, details, result):
        # user preferences
        lang = 'description' + xbmcaddon.Addon().getSetting('lang')
        if 'theaudiodb' in details:
            if lang in details['theaudiodb']:
                result['description'] = details['theaudiodb'][lang]
            elif 'descriptionEN' in details['theaudiodb']:
                result['description'] = details['theaudiodb']['descriptionEN']
        genre = xbmcaddon.Addon().getSetting('genre')
        if (genre in details) and ('genre' in details[genre]):
            result['genre'] = details[genre]['genre']
        style = xbmcaddon.Addon().getSetting('style')
        if (style in details) and ('styles' in details[style]):
            result['styles'] = details[style]['styles']
        mood = xbmcaddon.Addon().getSetting('mood')
        if (mood in details) and ('moods' in details[mood]):
            result['moods'] = details[mood]['moods']
        theme = xbmcaddon.Addon().getSetting('theme')
        if (theme in details) and ('themes' in details[theme]):
            result['themes'] = details[theme]['themes']
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
        if 'votes' in item:
            listitem.setProperty('album.votes', item['votes'])
        if 'cdart' in item:
            listitem.setProperty('album.cdart.url', item['cdart'])
        if 'thumb' in item:
            listitem.setProperty('album.thumbs', str(len(item['thumb'])))
            for count, thumb in enumerate(item['thumb']):
                listitem.setProperty('album.thumb%i.url' % (count + 1), thumb)
        xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listitem)
