from django.shortcuts import render_to_response, render
from django.templatetags.static import static
__author__ = 'krishnan_narayan'

from django.core import serializers
from django.http import HttpResponse
import urllib2
import urlparse
import json

def getBadRequestJsonResponse(message=None, errorCode=407):
    res = {}
    res["errorMsg"] = ""
    res["errorCode"] = ""
    if message is not None:
        res["errorMsg"] = message
    res["errorCode"] = errorCode


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
<<<<<<< HEAD
    return HttpResponse(json.dumps(res), content_type='application/json')


def sendRequest(urlString=None):
    if urlString is None:
        return getBadRequestJsonResponse("No Url Specified", 404)
    else:
        try:
            # parse url string to url
            data = urllib2.urlopen(urlString).read().decode('utf-8')
            return data
        except Exception as e:
            return getBadRequestJsonResponse("Mangled url generated for the search term", 403)





def url_fix(s, charset='utf-8'):
    """Sometimes you get an URL by a user that just isn't a real
    URL because it contains unsafe characters like ' ' and so on.  This
    function can fix some of the problems in a similar way browsers
    handle data entered by the user:

    """
    if s is not None:
        return urllib2.quote(s)
    else:
        return None

=======
    return render(request, 'timeline.html')
>>>>>>> working proto
