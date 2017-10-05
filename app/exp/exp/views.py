from django.shortcuts import HttpResponse
import urllib.request
import urllib.parse
import json

def hello(request):
    return HttpResponse('Hello World\n')

def group(request):
    req = urllib.request.Request('http://localhost:8000/group/all')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return resp
    #return HttpResponse('api group\n')
