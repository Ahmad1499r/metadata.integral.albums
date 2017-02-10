# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
from utils import *

def allmusic_albumfind(data):
    soup = BeautifulSoup(data, 'html.parser')
    albums = []
    for item in soup.find_all('li', {'class':'album'}):
        coverdata = item.find('div', {'class':'cover'})
        coverlink = coverdata.find('img', {'class':'lazy'})
        if coverlink:
            coverurl = coverlink.get('data-original')
        else:
            coverurl = ''
        releasedata = item.find('div', {'class':'info'})
        albumdata = releasedata.find('div', {'class':'title'})
        albumname = albumdata.find('a').get_text().strip()
        albumurl = ALLMUSICDETAILS % albumdata.find('a').get('href')
        artistdata = releasedata.find('div', {'class':'artist'})
        artistname = artistdata.get_text().strip()
        yeardata = releasedata.find('div', {'class':'year'})
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
    genredata = soup.find("div", {"class":"genre"})
    if genredata:
        genrelist = genredata.find_all('a')
        genres = []
        for genre in genrelist:
            genres.append(genre.get_text())        
        albumdata['genre'] = ', '.join(genres)
    else:
        missing.append('genre')
    styledata = soup.find("div", {"class":"styles"})
    if styledata:
        stylelist = styledata.find_all('a')
        styles = []
        for style in stylelist:
            styles.append(style.get_text())        
        albumdata['styles'] = ', '.join(styles)
    else:
        missing.append('styles')
    mooddata =  soup.find('section', {'class':'moods'})
    if mooddata:
        moodlist = mooddata.find_all('a')
        moods = []
        for mood in moodlist:
            moods.append(mood.get_text())  

        albumdata['moods'] = ', '.join(moods)
    else:
        missing.append('moods')
    themedata = soup.find('section', {'class':'themes'})
    if themedata:
        themelist = themedata.find_all('a')
        themes = []
        for theme in themelist:
            themes.append(theme.get_text())        
        albumdata['themes'] = ', '.join(themes)
    else:
        missing.append('themes')
    albumdata['rating'] = soup.find('div', {'itemprop':'ratingValue'}).get_text().strip()
    albumdata['album'] = soup.find('h1', {'class':'album-title'}).get_text().strip()
    artistdata = soup.find('h2', {'class':'album-artist'})
    artistlinks = artistdata.find_all('a')
    artistlist = []
    for artistlink in artistlinks:
        artistlist.append(artistlink.get_text())
    artists = []
    for item in artistlist:
        artistinfo = {}
        artistinfo['artist'] = item
        artistinfo['mbartistid'] = ''
        artists.append(artistinfo)
    albumdata['artist'] = artists
    thumbdata = soup.find('div', {'class':'album-contain'})
    thumbimg = thumbdata.find('img', {'class':'media-gallery-image'})
    thumb = []
    if thumbimg:
        thumbinfo = {}
        thumbinfo['thumb'] = thumbimg.get('src')
        thumbinfo['thumbaspect'] = ''
        thumb.append(thumbinfo)
    albumdata['thumb'] = thumb
    albumdata['year'] = soup.find('td', {'class':'year'}).get_text().strip()
    albumdata['label'] = soup.find('td', {'class':'label-catalog'}).contents[0].strip()
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
