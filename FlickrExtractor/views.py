from django.http import request
from django.http import response
import HttpUtils
import urllib2
import json
import models
import Flickr_Urls
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger('Search')
@csrf_exempt
def search(request, tag=None):

    if tag is not None:
        r = tag;
        logger.debug('Found request as %s', r )
        try :
            getPhotosByTag(r)
            return HttpUtils.getSuccessfulResponse()
        except:
            return HttpUtils.getBadRequestJsonResponse("Error Retrieving photos for tag", 404)


    else:
        return HttpUtils.getBadRequestJsonResponse("No tag received", 404)

def getPhotosByTag(tag):
        try:
            url = Flickr_Urls._SEARCH_URL.format(tag).encode('utf-8')
            photoList = urllib2.urlopen(url).read().decode('utf-8');
            #photos = json.loads(photoList, 'utf-8')
            list = models.RelatedList(photoList)
            getInfoOnRelatedPhotos(list)
        except Exception as e:
            raise e.message()


def getInfoOnRelatedPhotos(photoList):
    return True
