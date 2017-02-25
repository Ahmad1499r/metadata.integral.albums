# -*- coding: UTF-8 -*-

import xml.etree.ElementTree as xmlparse
from utils import *

def nfo_albumdetails(data):
    try:
        data = xmlparse.fromstring(metadata)
    except:
        return
    albumdata = {}
    if data.find('artistdesc').text:
        albumdata['artist_description'] = data.find('artistdesc').text
    if data.find('musicBrainzAlbumID').text:
        albumdata['mbalbumid'] = data.find('musicBrainzAlbumID').text
    if data.find('compilation').text:
        albumdata['compilation'] = data.find('compilation').text
    if data.find('review').text:
        albumdata['description'] = data.find('review').text
    if data.find('releasetype').text:
        albumdata['releasetype'] = data.find('releasetype').text
    if data.find('type').text:
        albumdata['type'] = data.find('type').text
    if data.find('releasedate').text:
        albumdata['releasedate'] = data.find('releasedate').text
    if data.find('label').text:
        albumdata['label'] = data.find('label').text
    if data.find('rating').text:
        rating = data.find('rating').text
        scale = data.find('rating').attrib.get('max', '')
        # old rating on a 0-5 scale
        if not scale:
            rating = str(float(rating) * 2)
        albumdata['rating'] = rating
    if data.find('votes').text:
        albumdata['votes'] = data.find('votes').text
    if data.find('year').text:
        albumdata['year'] = data.find('year').text
    #if data.find('path').text:
    #    albumdata['path'] = data.find('path').text
    genres = []
    for genre in data.findall('genre'):
        genres.append(genre.text)
    if genres:
        albumdata['genre'] = ' / '.join(genres)
    styles = []
    for style in data.findall('style'):
        styles.append(style.text)
    if genres:
        albumdata['styles'] = ' / '.join(styles)
    moods = []
    for mood in data.findall('mood'):
        moods.append(mood.text)
    if moods:
        albumdata['moods'] = ' / '.join(moods)
    themes = []
    for theme in data.findall('themes'):
        themes.append(theme.text)
    if themes:
        albumdata['themes'] = ' / '.join(themes)
    thumbs = []
    for item in data.findall('thumb'):
        thumbdata = {}
        thumbdata['url'] = item.text
        thumbdata['aspect'] = item.attrib.get('aspect', '')
        thumbdata['spoof'] = item.attrib.get('spoof', '')
        thumbdata['cache'] = item.attrib.get('cache', '')
        thumbs.append(thumbdata)
    if thumbs:
        albumdata['thumb'] = thumbs
    artists = []
    for item in data.findall('albumArtistCredits'):
        artistdata = {}
        artistdata['artist'] = item.find('artist').text
        artistdata['mbartistid'] = item.find('musicBrainzArtistID').text
        artists.append(artistdata)
    if artists:
        albumdata['artists'] = artists
    return albumdata
