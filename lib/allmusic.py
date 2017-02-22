# -*- coding: UTF-8 -*-
import time
import datetime
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
        albumurl = albumdata.find('a').get('href')
        artistdata = releasedata.find('div', {'class':'artist'})
        if not artistdata: # classical album
            continue
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
        albumdata['mbid'] = albumurl # url
        albumdata['relevance'] = '1'
        albums.append(albumdata)
    return albums

def allmusic_albumdetails(data):
    soup = BeautifulSoup(data, 'html.parser')
    albumdata = {}
    releasedata = soup.find("div", {"class":"release-date"})
    if releasedata:
        dateformat = releasedata.find('span').get_text()
        if len(dateformat) > 4:
            try:
                albumdata['releasedate'] = datetime.datetime(*(time.strptime(dateformat, '%B %d, %Y')[0:6])).strftime('%Y-%m-%d')
            except:
                albumdata['releasedate'] = datetime.datetime(*(time.strptime(dateformat, '%B, %Y')[0:6])).strftime('%Y-%m')
        else:
            albumdata['releasedate'] = releasedata.find('span').get_text()
    genredata = soup.find("div", {"class":"genre"})
    if genredata:
        genrelist = genredata.find_all('a')
        genres = []
        for genre in genrelist:
            genres.append(genre.get_text())        
        albumdata['genre'] = ' / '.join(genres)
    styledata = soup.find("div", {"class":"styles"})
    if styledata:
        stylelist = styledata.find_all('a')
        styles = []
        for style in stylelist:
            styles.append(style.get_text())        
        albumdata['styles'] = ' / '.join(styles)
    mooddata =  soup.find('section', {'class':'moods'})
    if mooddata:
        moodlist = mooddata.find_all('a')
        moods = []
        for mood in moodlist:
            moods.append(mood.get_text())  

        albumdata['moods'] = ' / '.join(moods)
    themedata = soup.find('section', {'class':'themes'})
    if themedata:
        themelist = themedata.find_all('a')
        themes = []
        for theme in themelist:
            themes.append(theme.get_text())        
        albumdata['themes'] = ' / '.join(themes)
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
    if thumbimg:
        thumb = []
        thumb.append(thumbimg.get('src'))
        albumdata['thumb'] = thumb
    yeardata = soup.find('td', {'class':'year'})
    if yeardata:
        albumdata['year'] = yeardata.get_text().strip()
    labeldata = soup.find('td', {'class':'label-catalog'})
    if labeldata:
        albumdata['label'] = labeldata.contents[0].strip()
    albumdata['releasetype'] = 'album'
    return albumdata
