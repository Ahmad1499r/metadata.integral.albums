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
            albumdata['descriptionEN'] = item['strDescription']
        elif ('strDescriptionEN' in item) and item['strDescriptionEN']:
            albumdata['descriptionEN'] = item['strDescriptionEN']
        if item['strDescriptionDE']:
            albumdata['descriptionDE'] = item['strDescriptionDE']
        if item['strDescriptionFR']:
            albumdata['descriptionFR'] = item['strDescriptionFR']
        if item['strDescriptionCN']:
            albumdata['descriptionCN'] = item['strDescriptionCN']
        if item['strDescriptionIT']:
            albumdata['descriptionIT'] = item['strDescriptionIT']
        if item['strDescriptionJP']:
            albumdata['descriptionJP'] = item['strDescriptionJP']
        if item['strDescriptionRU']:
            albumdata['descriptionRU'] = item['strDescriptionRU']
        if item['strDescriptionES']:
            albumdata['descriptionES'] = item['strDescriptionES']
        if item['strDescriptionPT']:
            albumdata['descriptionPT'] = item['strDescriptionPT']
        if item['strDescriptionSE']:
            albumdata['descriptionSE'] = item['strDescriptionSE']
        if item['strDescriptionNL']:
            albumdata['descriptionNL'] = item['strDescriptionNL']
        if item['strDescriptionHU']:
            albumdata['descriptionHU'] = item['strDescriptionHU']
        if item['strDescriptionNO']:
            albumdata['descriptionNO'] = item['strDescriptionNO']
        if item['strDescriptionIL']:
            albumdata['descriptionIL'] = item['strDescriptionIL']
        if item['strDescriptionPL']:
            albumdata['descriptionPL'] = item['strDescriptionPL']
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
            thumb.append(item['strAlbumThumb'])
            albumdata['thumb'] = thumb
        albumdata['releasetype'] = 'album'
        return albumdata
