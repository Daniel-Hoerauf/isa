from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.template import loader
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse


def hello(request):
    return render(request, 'exp.html')
    #return HttpResponse('Hello API\n')

def group(request):
    req = urllib.request.Request('http://models-api:8000/group/all')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return JsonResponse(resp)

def group_index(request):
    req = urllib.request.Request('http://models-api:8000/group/all')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    #groups = Group.objects.all()
    #return render(request, 'students-all.html', {'groups': groups})
    return JsonResponse(resp)

def get_group(request, group):
    req = urllib.request.Request('http://models-api:8000/group/1')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return JsonResponse(resp)
