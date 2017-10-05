from django.shortcuts import HttpResponse
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

import urllib.request
import urllib.parse
import json


def hello(request):
    return HttpResponse('Hello main page\n')

def group(request):
     req = urllib.request.Request('http://placeholder.com/v1/api/posts/1')
     resp_json = urllib.request.urlopen(req).read().decode('utf-8')
     resp = json.loads(resp_json)
     print(resp)
     return HttpResponse('Hello group page\n')