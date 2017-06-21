# -*- coding: UTF-8 -*-

import xbmcaddon

AUDIODBKEY = '58424d43204d6564696120'
AUDIODBURL = 'http://www.theaudiodb.com/api/v1/json/%s/%s'
AUDIODBSEARCH = 'searchalbum.php?s=%s&a=%s'
AUDIODBDETAILS = 'album-mb.php?i=%s'

MUSICBRAINZURL = xbmcaddon.Addon().getSetting('mbsite') + '/ws/2/release/%s'
MUSICBRAINZSEARCH = '?query=release:"%s"%%20AND%%20(artistname:"%s"%%20OR%%20artist:"%s")&fmt=json'
MUSICBRAINZDETAILS = '%s?inc=recordings+release-groups+artists+labels+ratings&fmt=json'

ALLMUSICURL = 'http://www.allmusic.com/%s'
ALLMUSICSEARCH = 'search/albums/%s%%2B%s'
ALLMUSICDETAILS = '%s/releases'

FANARTVKEY = 'ed4b784f97227358b31ca4dd966a04f1'
FANARTVURL = 'http://webservice.fanart.tv/v3/music/albums/%s?api_key=%s'
