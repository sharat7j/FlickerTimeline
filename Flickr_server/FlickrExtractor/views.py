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
            list = getPhotosByTag(r)
            details = getInfoOnRelatedPhotos(list)
            if details is not None:
                data = generateTimelineJson(tag, details)

            return HttpUtils.getSuccessfulResponse(data)
        except:
            return HttpUtils.getBadRequestJsonResponse("Error Retrieving photos for tag", 404)


    else:
        return HttpUtils.getBadRequestJsonResponse("No tag received", 404)

def getPhotosByTag(tag):
        try:
            url = Flickr_Urls._SEARCH_URL.format(tag).encode('utf-8')
            photoList = urllib2.urlopen(url).read().decode('utf-8')
            #photos = json.loads(photoList, 'utf-8')
            list = models.RelatedList(photoList)._photoList
            return list
        except Exception as e:
            raise e.message()


def getInfoOnRelatedPhotos(photoList):
    # get info on each photo and
    outputPhotoList = []
    dateConflictHash = {}
    count = 0

    if photoList is not None and count < 10:
        for photo in photoList:
            url = Flickr_Urls._GET_INFO_URL.format(photo._id).encode('utf-8')
            photoInfo = urllib2.urlopen(url).read().decode('utf-8')
            info = photo.populatePhotoInfo(photoInfo)
            if info is not None:
                #to do:  resolve conflicting taken dates
                outputPhotoList.append(info)
            count = count + 1
    # generate json data for timeline of photos
        return outputPhotoList
    else:
        return None


def generateTimelineJson(tag, photoInfoList):

    output = {}
    date = []
    for item in photoInfoList:
        dict = {}
        s = item._takenDate.split(" ")[0].encode('utf-8')

        dict["startDate"] = s.replace("-",",")
        dict["headline"] = item._title
        dict["text"] = item._description
        dict["asset"] = {"media": item._image_url,
                 "credit": item._ownerUserName,
                 "caption": "views : {0}".format(item._views)}
        date.append(dict)



    header = {"headline" : "Yahoo Hackathon Timeline",
              "type" : "default",
              "text" : "Timeline view for {0}".format(tag).encode('utf-8'),
              "start_date": "2012,1,26",
              "date" : date}
    output['timeline'] = header

    return output
