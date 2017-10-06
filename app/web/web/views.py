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
    name = []
    size = []
    gid = []
    for i in groupList:
        name.append(i['name'])
        size.append(i['size'])
        gid.append(i['id'])
    
    #return HttpResponse(groupList)
    return render(request, 'mainPage/mainPage.html', {'name':name, 'size':size, 'groupList':groupList})
    return JsonResponse(resp)
    #return render(request, 'app/mainPage.html')
    

def groupDetail(request):
    if request.method=='GET':
        gid = request.GET.get('id')
        if gid is None:
            return HttpResponse("error")
        req = urllib.request.Request('http://exp-api:8000/group/all')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        groups = resp['groups']
        group = groups
        for i in groups:
            if i['id'] == int(gid):
                group = i
                break
     #print(resp)
     #return HttpResponse('Hello group page\n')
     #return HttpResponse(size)
        return render(request, 'mainPage/group.html', {'group':group})
        #return JsonResponse(resp)
     
