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
from nfo import nfo_albumdetails
from fanarttv import fanarttv_albumart
from utils import *
#remove these
import web_pdb
import logging

logging.basicConfig(filename='integralalbumscraper.txt', level=logging.DEBUG)

def get_data(url):
    try:
        logging.debug("Request %s" % url)
        req = urllib2.Request(url, headers={'User-Agent': 'Intergral Albums Scraper/%s ( http://kodi.tv )' % xbmcaddon.Addon().getAddonInfo('version')})
        request = urllib2.urlopen(req)
        response = request.read()
        request.close()
    except:
        response = ''
    return response


class Scraper():
    def __init__(self, action, artist, album, url, key):
        self.start = 0
        if action == 'find':
            result = self.find_album(artist, album, 'musicbrainz')
            if result:
                self.return_search(result)
        elif action == 'resolveid':
            url = {'artist':"", 'album':"", 'releasegroupid':"", 'releaseid':key}
            mbpath = json.dumps(url) # MUSICBRAINZURL % (MUSICBRAINZDETAILS % key)
            listitem = xbmcgui.ListItem(path=mbpath, offscreen = True)
            xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listitem)
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
                mbreleaseid = url['releaseid']
                mbid = url['releasegroupid']
                threads = []
                if not mbid:
                    # Only have releaseid so fetch album, artist and releasegroupid Musicbrainz for other scrapers
                    result = self.get_details(mbreleaseid, 'musicbrainz', details)
                    if result:
                        artist = details['artist_description'].encode('utf-8')
                        album = details['album'].encode('utf-8')
                        mbid = details['releasegroupid']
                        for item in [[mbid, 'theaudiodb'], [mbid, 'fanarttv'], [[artist, album], 'allmusic']]:
                            if self.site_enabled(item[1]):
                                logging.debug("MBID known Fetch from site %s" % item[1])
                                thread = Thread(target = self.get_details, args = (item[0], item[1], details))
                                threads.append(thread)
                                thread.start()
                else:
                    for item in [[mbreleaseid, 'musicbrainz'], [mbid, 'theaudiodb'], [mbid, 'fanarttv'], [[artist, album], 'allmusic']]:
                        if self.site_enabled(item[1]):
                            logging.debug("Fetch from site %s" % item[1])
                            thread = Thread(target = self.get_details, args = (item[0], item[1], details))
                            threads.append(thread)
                            thread.start()
                for thread in threads:
                    thread.join()
#        elif action == 'parsenfo':
#            result = self.parse.nfo(url)
#            if result:
#                self.return_details(result)
#TODO test if url in nfo file
#            if url.startswith('http://'):
#                if url.startswith('http://www.theaudiodb.com/'):
#                    site = 'theaudiodb-nfo'
#                elif url.startswith('http://www.allmusic.com/'):
#                    site = 'allmusic-nfo'
#                else:
#                    return
#                thread = Thread(target = self.get_details, args = (url, site, details))
#                thread.start()
#                thread.join()
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
            url = MUSICBRAINZURL % (MUSICBRAINZSEARCH % ( urllib.quote_plus(album), urllib.quote_plus(artist), urllib.quote_plus(artist)))
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
                logging.debug("Allmusic found %s" % url)
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

#    def parse_nfo(self, path):
#        try:
#            datafile = xbmcvfs.File(PATH)
#            data = datafile.read()
#            datafile.close()
#        except:
#            return
#        return data

    def compile_results(self, details):
        result = {}
        thumbs = []
        # Musicbrainz results take preference
        if 'musicbrainz' in details:
            for k, v in details['musicbrainz'].items():
                result[k] = v
        # Review from TADB or none
        reviewsource = xbmcaddon.Addon().getSetting('review').lower()
        if (reviewsource in details) and ('review' in details[reviewsource]):
            result['review'] = details[reviewsource]['review']
        # Get required values from primary then fallback source
        for keyname in ['genre', 'style', 'mood', 'theme', 'rating']:
            self.value_prime_fallback(keyname, details, result)
        # Artwork from chosen sources merged
        for site in ['theaudiodb', 'fanarttv', 'allmusic']:
            isthumbsource = xbmcaddon.Addon().getSettingBool(site+'thumbs')
            if isthumbsource and (site in details) and ('thumb' in details[site]):
                thumbs += details[site]['thumb']
        if result:
            result['thumb'] = thumbs
        #DEBUG
        json_string = json.dumps(details)
        logging.debug("Details")
        logging.debug("%s" % json_string)          
        json_string = json.dumps(result)
        logging.debug("JSON results")
        logging.debug("%s" % json_string)

        return result

    def value_prime_fallback(self, keyname, details, result):
        # Get required value from primary then fallback source
        source = xbmcaddon.Addon().getSetting(keyname).lower()
        fallback = xbmcaddon.Addon().getSetting(keyname+'fb').lower()
        if source == 'none':
            if keyname in result:
                del result[keyname]
        elif (source in details) and (keyname in details[source]):
            result[keyname] = details[source][keyname]
        elif (fallback in details) and (keyname in details[fallback]):
            result[keyname] = details[fallback][keyname]     
          
    def site_enabled(self, site):
        # Check settings to see if data is to be requested from source site
        # Musicbrainz always queried to get artist credits, tracks and label
        # todo: only needed when "Prefer online info" is enabled for MB re-sync, could avoid making MB request
        if (site == 'musicbrainz'):
            return True
        # Artwork
        for source in ['theaudiodb', 'fanarttv', 'allmusic']:
            if (site == source) and xbmcaddon.Addon().getSettingBool(source+'thumbs'):
                return True
        # General settings, only use fallback site when there is a primary source site
        if xbmcaddon.Addon().getSetting('review').lower() == site:
            return True
        for keyname in ['genre', 'style', 'mood', 'theme', 'rating']:
            source = xbmcaddon.Addon().getSetting(keyname).lower()
            if source == site:
                return True
            elif source != 'none' and xbmcaddon.Addon().getSetting(keyname+'fb').lower() == site:
                return True
        return False
          
    def return_search(self, data):
        for count, item in enumerate(data):
            listitem = xbmcgui.ListItem(item['album'], thumbnailImage=item['thumb'], offscreen=True)
            listitem.setProperty('album.artist', item['artist_description'])
            listitem.setProperty('album.year', item['year'])
            listitem.setProperty('relevance', item['relevance'])
            url = {'artist':item['artist_description'], 'album':item['album'], 'releasegroupid':item['releasegroupid'], 'releaseid':item['releaseid']}
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=json.dumps(url), listitem=listitem, isFolder=True)

    def return_details(self, item):
        listitem = xbmcgui.ListItem(item['album'], offscreen=True)
        if 'releasegroupid' in item:
            listitem.setProperty('album.releasegroupid', item['releasegroupid'])
        if 'releaseid' in item:
            listitem.setProperty('album.releaseid', item['releaseid'])
            listitem.setProperty('album.musicbrainzid', item['releaseid'])            
        if 'artist' in item:
            listitem.setProperty('album.artists', str(len(item['artist'])))
            for count, artist in enumerate(item['artist']):
                listitem.setProperty('album.artist%i.name' % (count + 1), artist['artist'])
                listitem.setProperty('album.artist%i.musicbrainzid' % (count + 1), artist['mbartistid'])
                listitem.setProperty('album.artist%i.sortname' % (count + 1), artist['artistsort'])                
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
        if 'releasedate' in item:
            listitem.setProperty('album.release_date', item['releasedate'])
        if 'artist_description' in item:
            listitem.setProperty('album.artist_description', item['artist_description'])
        if 'label' in item:
            listitem.setProperty('album.label', item['label'])
        if 'type' in item:
            listitem.setProperty('album.type', item['type'])
        if 'compilation' in item:
            listitem.setProperty('album.compilation', item['compilation'])
        # releasetype is flag internal to Kodi, never scraped
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
