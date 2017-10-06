from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views import generic
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

import urllib.request
import urllib.parse
import json


def hello(request):
    
    #template_name = 'templates/mainPage/mainPage.html'
    req = urllib.request.Request('http://exp-api:8000/group/all')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    groupList = resp['groups']
    
    #return HttpResponse(groupList)
    return render(request, 'mainPage/mainPage.html', {'groupList':groupList})
    return JsonResponse(resp)
    #return render(request, 'app/mainPage.html')
    

def groupDetail(request):
     req = urllib.request.Request('http://exp-api:8000/group/1')
     resp_json = urllib.request.urlopen(req).read().decode('utf-8')
     resp = json.loads(resp_json)
     group = resp['group']
     size = group['size']
     name = group['name']
     #print(resp)
     #return HttpResponse('Hello group page\n')
     #return HttpResponse(size)
     return render(request, 'mainPage/group.html', {'name': name, 'size':size})
     return JsonResponse(resp)
     
