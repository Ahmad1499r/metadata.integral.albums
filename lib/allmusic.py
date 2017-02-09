# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
from utils import *

def allmusic_albumfind(data):
    soup = BeautifulSoup(data, 'html.parser')
    albums = []
    for item in soup.find_all("li", {"class":"album"}):
        coverdata = item.find("div", {"class":"cover"})
        coverlink = coverdata.find("img", {"class":"lazy"})
        if coverlink:
            coverurl = coverlink.get('data-original')
        else:
            coverurl = ''
        data = item.find("div", {"class":"info"})
        albumdata = data.find("div", {"class":"title"})
        albumname = albumdata.find("a").get_text().strip()
        albumurl = ALLMUSICDETAILS % albumdata.find("a").get('href')
        artistdata = data.find("div", {"class":"artist"})
        artistname = artistdata.get_text().strip()
        yeardata = data.find("div", {"class":"year"})
        if yeardata:
            yearvalue = yeardata.get_text().strip()
        else:
            yearvalue = ''
        albumdata = {}
        albumdata['artist'] = artistname
        albumdata['album'] = albumname
        albumdata['year'] = yearvalue
        albumdata['thumb'] = coverurl
        albumdata['url'] = albumurl
        albumdata['relevance'] = '1'
        albums.append(albumdata)
    return albums

def allmusic_albumdetails(data):
    soup = BeautifulSoup(data, 'html.parser')
    albumdata = {}
    missing = []


    if False: #TODO
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

        if item['intScore']:
            albumdata['rating'] = item['intScore']
        else:
            missing.append('rating')
        if item['strMood']:
            albumdata['moods'] = item['strMood']
        else:
            missing.append('moods')
        if item['strTheme']:
            albumdata['themes'] = item['strTheme']
        else:
            missing.append('themes')

        if item['strArtist']:
            artists = []
            artistdata = {}
            artistdata['artist'] = item['strArtist']
            if item['strMusicBrainzArtistID']:
                artistdata['mbartistid'] = item['strMusicBrainzArtistID']
            else:
                artistdata['mbartistid'] = ''
                missing.append('mbartistid')
            artists.append(artistdata)
            albumdata['artist'] = artists
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




        albumdata['releasetype'] = 'album'
        missing.append('back')
        missing.append('spine')
        missing.append('cdart')
        missing.append('mbalbumid')
        missing.append('description')
        missing.append('type')
        missing.append('back')
        missing.append('spine')
        missing.append('cdart')
        missing.append('votes')
        missing.append('compilation')
        missing.append('artist_description')
        for cat in missing:
            if cat in ('thumb', 'artist'):
                albumdata[cat] = []
            else:
                albumdata[cat] = ''
        albumdata['missing'] = missing
        return albumdata
