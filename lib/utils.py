# -*- coding: UTF-8 -*-

AUDIODBKEY = '58424d43204d6564696120'
AUDIODBURL = 'http://www.theaudiodb.com/api/v1/json/%s/%s'
AUDIODBSEARCH = 'searchalbum.php?s=%s&a=%s'
AUDIODBDETAILS = 'album-mb.php?i=%s'

MUSICBRAINZURL = 'http://musicbrainz.org/ws/2/release-group/%s'
MUSICBRAINZSEARCH = '?query=artist:"%s"%%20AND%%20releasegroup:"%s"%%20AND%%20primarytype:album&fmt=json'
MUSICBRAINZDETAILS = '%s?inc=ratings%%2Bartist-credits&fmt=json'

ALLMUSICURL = 'http://www.allmusic.com/%s'
ALLMUSICSEARCH = 'search/albums/%s%%2B%s'
ALLMUSICDETAILS = '%s/releases'

FANARTVKEY = 'ed4b784f97227358b31ca4dd966a04f1'
FANARTVURL = 'http://webservice.fanart.tv/v3/music/albums/%s?api_key=%s'
