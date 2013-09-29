from django.http import request
from django.http import response
import HttpUtils
import urllib2
import json
from models import Flickr
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger('Search')
@csrf_exempt
def search(request, tag=None):

    if tag is not None:
        r = tag;
        logger.debug('Found request as %s', r )
        f = Flickr()
        f.getPhotos(r)
        return HttpUtils.getSuccessfulResponse()

    else:
        return HttpUtils.getBadRequestJsonResponse("No tag received", 404)

def getPhotos(self, tag):
        try :
            url = self._SEARCH_URL.format(tag).encode('utf-8')
            photoList = urllib2.urlopen(url).read().decode('utf-8');
            photos = json.loads(photoList, 'utf-8')
            return photos
        except Exception as e:
            raise e.message()
