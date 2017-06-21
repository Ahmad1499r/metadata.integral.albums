# -*- coding: UTF-8 -*-
from utils import *

def musicbrainz_albumfind(data):
    if data['releases']:
        albums = []
        for item in data['releases']:
            albumdata = {}
            if item.get('artist-credit'):
                artists = []
                artistdisp = ""
                for artist in item['artist-credit']:
                    artistdata = {}
                    artistdata['artist'] = artist['artist']['name']
                    artistdata['mbartistid'] = artist['artist']['id']
                    artistdata['artistsort'] = artist['artist']['sort-name']
                    artistdisp = artistdisp + artist['artist']['name']
                    artistdisp = artistdisp + artist.get('joinphrase', '')
                    artists.append(artistdata)
            albumdata['artist'] = artists
            albumdata['artist_description'] = artistdisp
            if item['label-info']:
                albumdata['label'] = item['label-info'][0]['label']['name']
            albumdata['album'] = item['title']
            # Get year from release event dates
            if item['release-events']:
              albumdata['year'] = item['release-events'][0]['date'][:4]
            albumdata['thumb'] = ''
            albumdata['releaseid'] = item['id'] # release queried
            if item['release-group']:
                albumdata['releasegroupid'] = item['release-group']['id']
            albumdata['relevance'] = str(100.00 / int(item['score']))
            albums.append(albumdata)
        return albums

def musicbrainz_albumdetails(data):
    albumdata = {}
    albumdata['album'] = data['title']
    albumdata['releaseid'] = data['id'] # release queried
    if data['release-group']:
        albumdata['releasegroupid'] = data['release-group']['id']
        if data['release-group']['first-release-date']:
            albumdata['year'] = data['release-group']['first-release-date'][:4]
            albumdata['releasedate'] = data['release-group']['first-release-date']
        if data['release-group']['rating'] and data['release-group']['rating']['value']:
            albumdata['rating'] = str(int((float(data['release-group']['rating']['value']) * 2) + 0.5))
            albumdata['votes'] = str(data['release-group']['rating']['votes-count'])
        if data['release-group']['secondary-types']:
            albumdata['type'] = '%s; %s' % (data['release-group']['primary-type'], data['release-group']['secondary-types'][0])
        if data['release-group']['secondary-types'] and (data['release-group']['secondary-types'][0] == 'Compilation'):
            albumdata['compilation'] = 'true'
    if data.get('artist-credit'):
        artists = []
        artistdisp = ""
        for artist in data['artist-credit']:
            artistdata = {}
            artistdata['artist'] = artist['artist']['name']
            artistdata['mbartistid'] = artist['artist']['id']
            artistdata['artistsort'] = artist['artist']['sort-name']
            artistdisp = artistdisp + artist['artist']['name']
            artistdisp = artistdisp + artist.get('joinphrase', '')
            artists.append(artistdata)
        albumdata['artist'] = artists
        albumdata['artist_description'] = artistdisp
    if data['label-info']:
        albumdata['label'] = data['label-info'][0]['label']['name']
    albumdata['releasetype'] = 'album' # Kodi internal flag, always album
    return albumdata
