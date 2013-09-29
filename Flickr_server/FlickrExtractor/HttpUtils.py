__author__ = 'krishnan_narayan'

from django.core import serializers
from django.http import HttpResponse
import json

def getBadRequestJsonResponse(message=None, errorCode=407):
    res = {}
    res.errorMsg = ""
    res.errorCode = ""
    if message is not None:
        res.errorMsg = message
    res.errorCode = errorCode



    return HttpResponse(json.dumps(res), content_type='application/json')

def getSuccessfulResponse(data=None):
    res = {}
    if data is None:
        res = {"result":"ok"}
    else:
        res = data
    #d = serializers.serialize('json',res)
    return HttpResponse(json.dumps(res), content_type='application/json')
