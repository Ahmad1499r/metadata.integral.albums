# -*- coding: UTF-8 -*-
from utils import *

def musicbrainz_albumfind(data):
    if data['release-groups']:
        albums = []
        for item in data['release-groups']:
            albumdata = {}
            albumdata['artist'] = item['artist-credit'][0]['artist']['name']
            albumdata['album'] = item['title']
            albumdata['year'] = ''
            albumdata['thumb'] = ''
            albumdata['mbid'] = item['id']
            albumdata['relevance'] = str(100.00 / int(item['score']))
            albums.append(albumdata)
        return albums

def musicbrainz_albumdetails(data):
    albumdata = {}
    albumdata['album'] = data['title']
    albumdata['mbalbumid'] = data['id']
    if data['first-release-date']:
        albumdata['year'] = data['first-release-date'][:4]
        albumdata['releasedate'] = data['first-release-date']
    if data['rating'] and data['rating']['value']:
        albumdata['rating'] = str(data['rating']['value'])
        albumdata['votes'] = str(data['rating']['votes-count'])
    if data['secondary-types']:
        albumdata['type'] = data['secondary-types'][0]
    if data['secondary-types'] and (data['secondary-types'][0] == 'Compilation'):
        albumdata['compilation'] = 'true'
    else:
        albumdata['compilation'] = 'false'
    if data['artist-credit']:
        artists = []
        for artist in data['artist-credit']:
            artistdata = {}
            artistdata['artist'] = artist['name']
            artistdata['mbartistid'] = artist['artist']['id']
            artists.append(artistdata)
        albumdata['artist'] = artists
    albumdata['releasetype'] = 'album'
    return albumdata
