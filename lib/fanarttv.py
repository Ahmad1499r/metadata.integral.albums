#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def fanarttv_albumart(data):
    if 'albums' in data:
        artwork = {}
        thumbs = []
        cdart = ''
        for mbid, art in data['albums'].items():
            if 'albumcover' in art:
                for thumb in art['albumcover']:
                    thumbdata = {}
                    thumbdata['thumb'] = thumb['url']
                    thumbdata['thumbaspect'] = ''
                    thumbs.append(thumbdata)
            if 'cdart' in art:
                cdart = art['cdart'][0]['url']
        artwork['thumb'] = thumbs
        artwork['cdart'] = cdart
        return artwork
