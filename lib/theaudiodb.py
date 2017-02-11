# -*- coding: UTF-8 -*-
from utils import *

def theaudiodb_albumfind(data):
    if data['album']:
        albums = []
        for item in data['album']:
            albumdata = {}
            albumdata['artist'] = item['strArtist']
            albumdata['album'] = item['strAlbum']
            albumdata['year'] = item.get('intYearReleased', '')
            albumdata['thumb'] = item.get('strAlbumThumb', '')
            albumdata['mbid'] = item['strMusicBrainzID']
            albumdata['relevance'] = '1'
            albums.append(albumdata)
        return albums

def theaudiodb_albumdetails(data):
    if data['album']:
        item = data['album'][0]
        albumdata = {}
        albumdata['album'] = item['strAlbum']
        if item['intYearReleased']:
            albumdata['year'] = item['intYearReleased']
        if item['strStyle']:
            albumdata['styles'] = item['strStyle']
        if item['strGenre']:
            albumdata['genre'] = item['strGenre']
        if item['strLabel']:
            albumdata['label'] = item['strLabel']
        if item['strReleaseFormat']:
            albumdata['type'] = item['strReleaseFormat']
        if item['strAlbumThumbBack']:
            albumdata['back'] = item['strAlbumThumbBack']
        if item['strAlbumSpine']:
            albumdata['spine'] = item['strAlbumSpine']
        if item['strAlbumCDart']:
            albumdata['cdart'] = item['strAlbumCDart']
        if item['intScore']:
            albumdata['rating'] = item['intScore']
        if item['intScoreVotes']:
            albumdata['votes'] = item['intScoreVotes']
        if item['strMood']:
            albumdata['moods'] = item['strMood']
        if item['strTheme']:
            albumdata['themes'] = item['strTheme']
        if item['strMusicBrainzID']:
            albumdata['mbalbumid'] = item['strMusicBrainzID']
        # api inconsistent
        if ('strDescription' in item) and item['strDescription']:
            albumdata['description'] = item['strDescription']
        elif ('strDescriptionEN' in item) and item['strDescriptionEN']:
            albumdata['description'] = item['strDescriptionEN']
        if item['strArtist']:
            artists = []
            artistdata = {}
            artistdata['artist'] = item['strArtist']
            if item['strMusicBrainzArtistID']:
                artistdata['mbartistid'] = item['strMusicBrainzArtistID']
            artists.append(artistdata)
            albumdata['artist'] = artists
        if item['strAlbumThumb']:
            thumb = []
            thumbdata = {}
            thumbdata['thumb'] = item['strAlbumThumb']
            thumbdata['thumbaspect'] = ''
            thumb.append(thumbdata)
            albumdata['thumb'] = thumb
        albumdata['releasetype'] = 'album'
        return albumdata
