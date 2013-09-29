from django.db import models

import json
# Create your models here.
class Flickr():
    _SEARCH_URL = "http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=785779470c5dc66b0aae9416093f4ee9&sort=&format=json&nojsoncallback=1&tag={0}"
    _GET_INFO_URL = "http://api.flickr.com/services/rest/?method=flickr.photos.getInfo&api_key=785779470c5dc66b0aae9416093f4ee9&format=json&photo_id={0}"


