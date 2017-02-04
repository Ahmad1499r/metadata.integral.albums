#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def theaudiodb_albumfind(data):
    if data['album']:
        albums = []
        for item in data['album']:
            albumdata = {}
            albumdata['artist'] = item['strArtist']
            albumdata['album'] = item['strAlbum']
            albumdata['year'] = item.get('intYearReleased', '')
            albumdata['thumb'] = item.get('strAlbumThumb', '')
            albumdata['url'] = 'http://www.theaudiodb.com/api/v1/json/1/album-mb.php?i=%s' % item['strMusicBrainzID']
            albumdata['relevance'] = '1'
            albums.append(albumdata)
        return albums

def theaudiodb_albumdetails(data):
    if data['album']:
        item = data['album'][0]
        albumdata = {}
        missing = []
        albumdata['album'] = item['strAlbum']
        if item['intYearReleased']:
            albumdata['year'] = item['intYearReleased']
        else:
            missing.append('year')
        if item['strStyle']:
            albumdata['styles'] = item['strStyle']
        else:
            missing.append('styles')
        if item['strGenre']:
            albumdata['genre'] = item['strGenre']
        else:
            missing.append('genre')
        if item['strLabel']:
            albumdata['label'] = item['strLabel']
        else:
            missing.append('label')
        if item['strReleaseFormat']:
            albumdata['releasetype'] = item['strReleaseFormat']
        else:
            missing.append('releasetype')
        if item['strAlbumThumbBack']:
            albumdata['back'] = item['strAlbumThumbBack']
        else:
            missing.append('back')
        if item['strAlbumSpine']:
            albumdata['spine'] = item['strAlbumSpine']
        else:
            missing.append('spine')
        if item['strAlbumCDart']:
            albumdata['cdart'] = item['strAlbumCDart']
        else:
            missing.append('cdart')
        if item['intScore']:
            albumdata['rating'] = item['intScore']
        else:
            missing.append('rating')
        if item['intScoreVotes']:
            albumdata['votes'] = item['intScoreVotes']
        else:
            missing.append('votes')
        if item['strMood']:
            albumdata['moods'] = item['strMood']
        else:
            missing.append('moods')
        if item['strTheme']:
            albumdata['themes'] = item['strTheme']
        else:
            missing.append('themes')
        if item['strMusicBrainzID']:
            albumdata['mbalbumid'] = item['strMusicBrainzID']
        else:
            missing.append('mbalbumid')
        # api inconsistent
        if ('strDescription' in item) and item['strDescription']:
            albumdata['description'] = item['strDescription']
        elif ('strDescriptionEN' in item) and item['strDescriptionEN']:
            albumdata['description'] = item['strDescriptionEN']
        else:
            missing.append('description')
        if item['strArtist']:
            artist = []
            artistdata = {}
            artistdata['artist'] = item['strArtist']
            if item['strMusicBrainzArtistID']:
                artistdata['mbartistid'] = item['strMusicBrainzArtistID']
            else:
                artistdata['mbartistid'] = ''
                missing.append('mbartistid')
            artist.append(artistdata)
            albumdata['artist'] = artist
        else:
            missing.append('artist')
        if item['strAlbumThumb']:
            thumb = []
            thumbdata = {}
            thumbdata['thumb'] = item['strAlbumThumb']
            thumbdata['thumbaspect'] = ''
            thumb.append(thumbdata)
            albumdata['thumb'] = thumb
        else:
            missing.append('thumb')
        missing.append('type')
        missing.append('compilation')
        missing.append('artist_description')
        for cat in missing:
            if cat in ('thumb', 'artist'):
                albumdata[cat] = []
            else:
                albumdata[cat] = ''
        albumdata['missing'] = missing
        return albumdata
