from django.shortcuts import render_to_response, render
from django.templatetags.static import static
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
def getResultPage():
    return render_to_response('people.html')

def getSuccessfulResponse(request,data=None):
    res = {}
    if data is None:
        res = {"result":"ok"}
    else:
        res = data
    print res
    url = static('json/jsonData.json')

    print url
    f=open("static/json/jsonData.json",'w')
    f.write(json.dumps(res))
    f.flush()

    f.close()


    #d = serializers.serialize('json',res)
    return render(request, 'timeline.html')
