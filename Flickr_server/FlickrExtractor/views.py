from django.http import HttpResponse
import os
from django.http import request, HttpResponseRedirect, HttpResponse
from django.http import response
from django.shortcuts import render_to_response, render
from django.template import Context, RequestContext
from django.template.loader import get_template
import HttpUtils
import json
import JSONEncoder
import os
import models
import Flickr_Urls
from django.template.loader import get_template
from django.template import Context

from django.views.decorators.csrf import csrf_exempt

import logging

logger = logging.getLogger('Search')





@csrf_exempt
def search(request):
    req = request.GET
    tag = req['tag']
    tag.replace(' ', '+')
    print tag
    if tag is not None:
        r = HttpUtils.url_fix(tag);
        logger.debug('Found request as %s', r)
        try:
            ps = getPhotosByTag(r)
            details = getInfoOnRelatedPhotos(ps)

            if details is not None:
                data = generateTimelineJson(tag, details)
                # write to json file for generating the timeline
                fileName = writeJson(tag, data)
                t = get_template('timeline.html')
                html = t.render(Context({'file_name': fileName}))
                respond = HttpResponse(html, content_type="text/html")
                respond['Cache-Control'] = "no-cache"
                # return render_to_response('timeline.html', locals(), context_instance = RequestContext(request))

                return respond
        except Exception as e:
            return HttpUtils.getBadRequestJsonResponse("Error Retrieving photos for tag", 404)


def landing(request):
    return render(request, 'index.html')


def process(request):
    tag = request.GET
    return HttpResponseRedirect("/tagSearch/" + tag)


def getPhotosByTag(tag):
    try:
        url = Flickr_Urls._SEARCH_URL.format(tag).encode('utf-8')
        photoList = HttpUtils.sendRequest(url)
        p = models.RelatedList(photoList)._photoList
        return p
    except Exception as e:
        raise e.message()


def getInfoOnRelatedPhotos(photoList):
    # get info on each photo and
    outputPhotoList = []
    dateConflictHash = {}

    if photoList is not None:
        for photo in photoList:
            url = Flickr_Urls._GET_INFO_URL.format(photo._id).encode('utf-8')
            photoInfo = HttpUtils.sendRequest(url)
            info = photo.populatePhotoInfo(photoInfo)
            if info is not None:
                #to do:  resolve conflicting taken dates
                outputPhotoList.append(info)
            count = count + 1
            if count > 10:
                break
                # generate json data for timeline of photos
        return outputPhotoList
    else:
        return None


def writeJson(tag, jsonData):
    if jsonData is not None:
        path = "static/json/"

        filename = "timeline_{0}".format(tag).encode("utf-8")
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(path + filename, 'w')
        data = json.dumps(jsonData).encode('utf-8')
        print data
        with open(path + filename, 'w') as outfile:
            outfile.write(data)
        return filename.encode('utf-8')
    else:
        return None


def generateTimelineJson(tag, photoInfoList):
    output = {}
    date = []
    for item in photoInfoList:
        dict = {}
        s = item._takenDate.split(" ")[0].encode('utf-8')

        dict["startDate"] = s.replace("-", ",")
        dict["headline"] = item._title
        dict["text"] = item._description
        dict["asset"] = {"media": item._image_url,
                         "credit": item._ownerUserName,
                         "caption": "views : {0}".format(item._views)}
        date.append(dict)

    header = {"headline": "Yahoo Hackathon Timeline",
              "type": "default",
              "text": "Timeline view for {0}".format(tag).encode('utf-8'),
              "start_date": "2012,1,26",
              "date": date}
    output['timeline'] = header

    return output


def writeJson(tag, jsonData):
    if jsonData is not None:
        path = "static/site-resources/json/"
        fileName = "timeline_{0}.json".format(tag).encode('utf-8')
        if not os.path.exists(path):
            os.makedirs(path)

        data = json.dumps(jsonData).encode('utf-8')
        with open(path + fileName, "w") as outfile:
            outfile.write(data)
            return (fileName).encode('utf-8')
    else:
        return None
