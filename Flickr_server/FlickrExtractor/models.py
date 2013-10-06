from django.db import models

import json
import logging

logger = logging.getLoggerClass()
# Create your models here.
class Photo():
    _id = ""
    _image_url = ""
    _thumb_url = ""
    _owner = ""
    _secret = ""
    _server = ""
    _farm = ""
    _title = ""
    _dateUploaded = ""
    _ownerUserName = ""
    _description = ""
    _postedDate = ""
    _takenDate = ""
    _lastUpdated = ""
    _views = ""

    def __init__(self, photo_id):
        self._id = photo_id

    def populatePhotoInfo(self, photoInfoString):
        if photoInfoString is not None:
            photoInfoJson = json.loads(photoInfoString, 'utf-8')
            if photoInfoJson is not None and photoInfoJson['photo'] is not None:
                self._dateUploaded = photoInfoJson['photo']['dateuploaded']
                self._ownerUserName = photoInfoJson['photo']['owner']['username']
                self._description = photoInfoJson['photo']['description']['_content']
                self._postedDate = photoInfoJson['photo']['dates']['posted']
                self._takenDate = photoInfoJson['photo']['dates']['taken']
                self._lastUpdated = photoInfoJson['photo']['dates']['lastupdate']
                self._views = photoInfoJson['photo']['views']

            return self
        else:
            return None


    def getImageUrl(self):
        # Create image url from this photo
        # refer http://www.flickr.com/services/api/misc.urls.html
        if self._id and self._farm is not None and self._server is not None and self._secret is not None:
            self._image_url = ("http://farm{0}.staticflickr.com/{1}/{2}_{3}.jpg").format(self._farm, self._server,
                                                                                         self._id, self._secret)
            self._thumb_url = ("http://farm{0}.staticflickr.com/{1}/{2}_{3}_t.jpg").format(self._farm, self._server,
                                                                                           self._id, self._secret)


class RelatedList():
    _photoList = []
    _photoListJson = ""
    #_totalResults = ""
    def __init__(self, photoListJsonString):
        self._photoList=[]
        self.extractPhotos(photoListJsonString)


    def extractPhotos(self, jsonString):
        try:
            self._photoListJson = json.loads(jsonString, 'utf-8')
            if self._photoListJson is not None:
                if self._photoListJson['photos'] is not None:
                    if self._photoListJson['photos']['total'] is not None:
                        self._totalResults = self._photoListJson['photos']['total']
                    if self._photoListJson['photos']['photo'] is not None and self._photoListJson['photos'][
                        'photo'].__len__() > 0:
                        for pic in self._photoListJson['photos']['photo']:
                            p = Photo(pic['id'])
                            p._owner = pic['owner']
                            p._secret = pic['secret']
                            p._server = pic['server']
                            p._farm = pic['farm']
                            p._title = pic['title']
                            p.getImageUrl()
                            self._photoList.append(p)

        except Exception as e:
            logger.debug("Exception occurred in creating json list: Message - ", e);

    def getPhotoList(self):
        return self._photoList

