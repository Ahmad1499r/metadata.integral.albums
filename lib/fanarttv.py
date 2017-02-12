# -*- coding: UTF-8 -*-

def fanarttv_albumart(data):
    if 'albums' in data:
        artwork = {}
        thumbs = []
        for mbid, art in data['albums'].items():
            if 'albumcover' in art:
                for thumb in art['albumcover']:
                    thumbs.append(thumb['url'])
            if 'cdart' in art:
                artwork['cdart'] = art['cdart'][0]['url']
        if thumbs:
            artwork['thumb'] = thumbs
        return artwork
