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
            albumdata['url'] = MUSICBRAINZURL % (MUSICBRAINZDETAILS % item['id'])
            albumdata['relevance'] = str(100.00 / int(item['score']))
            albums.append(albumdata)
        return albums

def musicbrainz_albumdetails(data):
    albumdata = {}
    missing = []
    albumdata['album'] = data['title']
    albumdata['mbalbumid'] = data['id']
    if data['first-release-date']:
        albumdata['year'] = data['first-release-date']
    else:
        missing.append('year')
    if data['rating'] and data['rating']['value']:
        albumdata['rating'] = str(data['rating']['value'])
        albumdata['votes'] = str(data['rating']['votes-count'])
    else:
        missing.append('rating')
        missing.append('votes')
    if data['secondary-types']:
        albumdata['type'] = data['secondary-types'][0]
    else:
       missing.append('type')
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
    else:
        missing.append('artist')
    albumdata['releasetype'] = 'album'
    missing.append('styles')
    missing.append('genre')
    missing.append('label')
    missing.append('back')
    missing.append('spine')
    missing.append('cdart')
    missing.append('moods')
    missing.append('themes')
    missing.append('description')
    missing.append('thumb')
    missing.append('artist_description')
    for cat in missing:
        if cat in ('thumb', 'artist'):
            albumdata[cat] = []
        else:
            albumdata[cat] = ''
    albumdata['missing'] = missing
    return albumdata
